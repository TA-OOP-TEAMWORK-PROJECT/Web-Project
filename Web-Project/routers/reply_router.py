from fastapi import APIRouter, Response, Header
from data_.models import Reply, Vote
from services import reply_service

reply_router = APIRouter(prefix='/reply')



@reply_router.post("/")
def create_reply(reply: Reply):

    reply = reply_service.create(reply)

    return reply_service.create_reply_response(reply)  # user

@reply_router.put("/vote/{id}")
def change_vote(new_vote:Vote, id:int): #user

    reply = reply_service.get_by_id(id)   #  за да добавям лайкова или дислайкове


    old_vote_data = reply_service.get_vote_by_reply_id(id)  # за да проверявам как е гласувано последно


    reply_service.vote_change(new_vote, old_vote_data, reply)

'''
Upvote/Downvote a Reply

- Requires authentication
- A user should be able to change their downvotes to upvotes and vice versa but a reply can only be upvoted/downvoted once per user
'''




'''
Choose Best Reply

- Requires authentication
- Topic Author can select one best reply to their Topic
'''
