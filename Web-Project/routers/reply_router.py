from typing import Annotated

from fastapi import APIRouter, Response, Header, Depends

from common.auth import get_current_active_user, User, get_current_user
# from common.auth import get_user_or_raise_401
from data_.models import Reply, Vote
from services import reply_service


reply_router = APIRouter(prefix='/reply')


@reply_router.post("/{topic_id}")
def create_reply(reply: Reply, topic_id,
                 current_user: Annotated[User, Depends(get_current_active_user)]):

    reply = reply_service.create(reply, topic_id)

    if not reply:
        return Response(status_code=404)  # HTTP exeption
    return reply  # user

@reply_router.put("/{reply_id}/vote")
def change_vote(new_vote:Vote, reply_id:int,
                current_user: Annotated[User, Depends(get_current_active_user)]):

    reply = reply_service.get_by_id(reply_id)
    return reply_service.vote_change(new_vote, reply, current_user)
