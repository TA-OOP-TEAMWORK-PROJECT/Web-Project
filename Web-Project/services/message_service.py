from data_.models import Message, MessageCreate, User
from data_.database import insert_query, read_query
from services.users_service import is_authenticated
from common.responses import MessageServiceError
import datetime


def create_message(message_data: MessageCreate, token: str):
    user_id = is_authenticated(token)
    if user_id is None:
        raise MessageServiceError("Invalid user.")
    message_id = insert_query(
        "INSERT INTO messages (content, sender_id, receiver_id, created_at) VALUES (%s, %s, %s, %s)",
        (message_data.content, user_id, message_data.receiver_id, datetime.datetime.now())
    )
    return Message(**message_data.dict(), id=message_id, sender_id=user_id)


def get_conversation(user_id: int, token: str):
    current_user_id = is_authenticated(token)
    if current_user_id is None:
        raise MessageServiceError("Invalid user.")

    messages = read_query(
        "SELECT * FROM messages WHERE (sender_id = %s AND receiver_id = %s) OR (sender_id = %s AND receiver_id = %s)",
        (current_user_id, user_id, user_id, current_user_id)
    )
    return [Message.parse_obj(message) for message in messages]


def get_conversations(token: str):
    user_id = is_authenticated(token)
    if user_id is None:
        raise MessageServiceError("Invalid user.")

    users = read_query(
        """
        SELECT DISTINCT users.*
        FROM users
        JOIN messages ON users.id = messages.sender_id OR users.id = messages.receiver_id
        WHERE messages.sender_id = %s OR messages.receiver_id = %s
        """,
        (user_id, user_id)
    )
    return [User.parse_obj(user) for user in users]