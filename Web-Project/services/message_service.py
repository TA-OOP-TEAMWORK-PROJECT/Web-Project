from data_.models import Message, MessageCreate, User, Conversation
from fastapi import Response
from data_.database import insert_query, read_query
from services.users_service import is_authenticated
from common.responses import MessageServiceError
from datetime import datetime


def create_message(message_data: MessageCreate, cur_user: User):


    receiver_id = read_query('''
        SELECT id
        FROM users
        WHERE id = ?''',
        (message_data.receiver_id,))

    if not receiver_id:
        return Response(status_code=404)

    message_id = insert_query(
        "INSERT INTO message (content, sender_id, receiver_id, created_at) VALUES (%s, %s, %s, %s)",
        (message_data.content, cur_user.id, message_data.receiver_id, datetime.now())
    )

    return Message(**message_data.dict(), id=message_id, sender_id=cur_user.id)


def get_conversation(receiver_id: int, cur_user: User):


    messages = read_query(
        "SELECT * FROM message WHERE sender_id = ? AND receiver_id = ?",
        (cur_user.id, receiver_id,)
    )

    return [Message.from_query_result(*row) for row in messages]


def get_conversations(user: User):

    users = read_query(
        """
        SELECT DISTINCT users.username
        FROM users
        JOIN message ON users.id = message.sender_id OR users.id = message.receiver_id
        WHERE message.sender_id = %s OR message.receiver_id = %s
        """,
        (user.id, user.id)
    )

    a = [Conversation(username=row[0]) for row in users]
    result = get_conv_response(a)

    a = 5
    return result

def get_conv_response(conv):
    cnt = 0
    conv_dict = {}
    for i in conv:
        conv_dict[
    {
        'username': i.username,
    }
    ] = cnt+1

    return conv_dict