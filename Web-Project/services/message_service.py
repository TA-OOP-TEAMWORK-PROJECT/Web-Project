from data_.models import Message, MessageCreate, User, Conversation
from fastapi import Response
from data_.database import insert_query, read_query
from datetime import datetime

from services.users_service import find_by_id


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

    message = Message(**message_data.dict(), id=message_id, sender_id=cur_user.id)

    return {
        "Message content": message.content,
        "Sent at": message.created_at.strftime('%d/%m/%Y'),
        "Sent to":  find_by_id(message.receiver_id)
    }
    # return Message(**message_data.dict(), id=message_id, sender_id=cur_user.id)



def get_conversation(receiver_id: int, cur_user: User):


    messages = read_query(
        "SELECT * FROM message WHERE sender_id = ? AND receiver_id = ?",
        (cur_user.id, receiver_id,)
    )

    return [Message.from_query_result(*row) for row in messages]


def get_conversations(user: User):
    sender_user = read_query(
        """
        SELECT DISTINCT users.username
        FROM users
        JOIN message ON users.id = message.receiver_id 
        WHERE message.sender_id = ?
        """,
        (user.id, )
    )

    receiver_user = read_query(
        """
        SELECT DISTINCT users.username
        FROM users
        JOIN message ON users.id = message.sender_id 
        WHERE message.receiver_id = ? """,
        (user.id, )
    )


    sender = get_conv_response([Conversation(username=row[0]) for row in sender_user])
    receiver = get_conv_response([Conversation(username=row[0]) for row in receiver_user])
    a = 5
    result = {
        f"Inbox: {receiver}",
        f"Outbox:{sender}"
    }
    return result


def get_conv_response(conv):
    result = []
    for i in conv:
        result.append(Conversation(username=i.username))

    result_response = []
    for r in result:
        result_response.append(r.username)

    return result_response



# SELECT DISTINCT users.username
#         FROM users
#         JOIN message ON users.id = message.sender_id OR users.id = message.receiver_id
#         WHERE message.sender_id = 1 OR message.receiver_id = 1