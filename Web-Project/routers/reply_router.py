from typing import Annotated
from fastapi import APIRouter, Response, Depends
from common.auth import get_current_active_user, User
from data_.models import Reply, Vote
from services import reply_service
from services.reply_service import get_category_id_from_reply
from services.users_service import get_user_access

reply_router = APIRouter(prefix='/reply')


@reply_router.post("/{category_id}/{topic_id}") #
def create_reply(reply: Reply, category_id, topic_id,
                 current_user: Annotated[User, Depends(get_current_active_user)]):

    user_access = get_user_access(int(current_user.id), int(category_id))
    if user_access.can_write == 0:
        return Response(status_code=401, content='You are not authorized!')

    reply = reply_service.create(reply, topic_id)

    if not reply:
        return Response(status_code=404)
    return reply

@reply_router.put("/{reply_id}/vote")
def change_vote(new_vote:Vote, reply_id:int,
                current_user: Annotated[User, Depends(get_current_active_user)]):

    user_access = get_user_access(current_user.id, get_category_id_from_reply(reply_id))
    if user_access.can_write == 0:
        return Response(status_code=401, content='You are not authorized!')

    reply = reply_service.get_by_id(reply_id)
    return reply_service.vote_change(new_vote, reply, current_user)
