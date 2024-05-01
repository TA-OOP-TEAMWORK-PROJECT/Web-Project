from fastapi import APIRouter, Response, Header

# from common.auth import get_user_or_raise_401
from data_.models import Reply, Vote
from services import reply_service

reply_router = APIRouter(prefix='/reply')

'''
Choose Best Reply

- Requires authentication
- Topic Author can select one best reply to their Topic
'''

# @reply_router.get('/{id}')  # да попитам дали така е ок
# def view_reply(x_token=Header()):
#
#     user = get_user_or_raise_401(x_token)
#     result = reply_service.get_reply(user)
#
#     if result:
#         return result
#
#     else:
#         return Response(status_code=401)


@reply_router.post("/")
def create_reply(reply: Reply):

    reply = reply_service.create(reply)

    return reply_service.create_reply_response(reply)  # user

@reply_router.put("/{id}")
def change_vote(new_vote:Vote, id:int): #user

    reply = reply_service.get_by_id(id)   #  за да добавям лайкова или дислайкове


    return reply_service.vote_change(new_vote, reply)



