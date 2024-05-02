from typing import Annotated

from fastapi import APIRouter, Response, Header, Depends

from common.auth import get_current_active_user, User, get_current_user
# from common.auth import get_user_or_raise_401
from data_.models import Reply, Vote
from services import reply_service

reply_router = APIRouter(prefix='/reply')


@reply_router.post("/")
def create_reply(reply: Reply, current_user: Annotated[User, Depends(get_current_active_user)]):

    reply = reply_service.create(reply)

    return reply_service.create_reply_response(reply)  # user

@reply_router.put("/{id}/vote")
def change_vote(new_vote:Vote, id:int, current_user: Annotated[User, Depends(get_current_active_user)]): #user


    reply = reply_service.get_by_id(id)


    return reply_service.vote_change(new_vote, reply)



