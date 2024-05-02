from data_.models import Message, MessageCreate, User
from data_.database import insert_query, read_query
from services.users_service import is_authenticated
from common.responses import MessageServiceError
from datetime import datetime


def create_message(message_data: MessageCreate, cur_user: User):
    # user_id = is_authenticated(token)
    # if user_id is None:
    #     raise MessageServiceError("Invalid user.")
    message_id = insert_query(
        "INSERT INTO message (content, sender_id, receiver_id, created_at) VALUES (%s, %s, %s, %s)",
        (message_data.content, cur_user.id, message_data.receiver_id, datetime.now())
    )
    return Message(**message_data.dict(), id=message_id, sender_id=cur_user.id)


def get_conversation(user_id: int, cur_user: User):


    messages = read_query(
        "SELECT * FROM message WHERE sender_id = ? AND receiver_id = ?",
        (cur_user.id, user_id,)
    )
    for message in messages: #?
        if isinstance(message['created_at'], str):
            message['created_at'] = datetime.strptime(message['created_at'], '%Y-%m-%d %H:%M:%S')
    return [Message.parse_obj(message) for message in messages]


def get_conversations(token: str):
    user_id = is_authenticated(token)
    if user_id is None:
        raise MessageServiceError("Invalid user.")

    users = read_query(
        """
        SELECT DISTINCT users.*
        FROM users
        JOIN message ON users.id = message.sender_id OR users.id = message.receiver_id
        WHERE message.sender_id = %s OR message.receiver_id = %s
        """,
        (user_id, user_id)
    )
    return [User.parse_obj(user) for user in users]