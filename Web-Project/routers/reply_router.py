from typing import Annotated
from fastapi import APIRouter, Response, Depends
from common.auth import get_current_active_user, User
from data_.models import Reply, Vote
from services import reply_service
from services.category_service import get_category_by_id
from services.reply_service import get_category_id_from_reply
from services.topic_service import get_topic_by_id
from services.users_service import users_access_state

reply_router = APIRouter(prefix='/replies')


@reply_router.post("/categories/{category_id}/topics/{topic_id}")
def create_reply(reply: Reply, category_id, topic_id,
                 current_user: Annotated[User, Depends(get_current_active_user)]):

    category = get_category_by_id(category_id)
    topic = get_topic_by_id(topic_id)
    if category.is_private or category.is_locked:

        if not users_access_state(current_user.id, category_id):
            return Response(status_code=401, content='You are not authorized!')

    if topic.is_locked:
        return Response(status_code=423, content='Category is locked')

    reply = reply_service.create(reply, topic_id)

    if not reply:
        return Response(status_code=404)
    return reply



@reply_router.put("/categories/{category_id}/topics/{topic_id}/vote/{reply_id}")
def change_vote(new_vote:Vote, category_id:int, topic_id: int, reply_id:int,
                current_user: Annotated[User, Depends(get_current_active_user)]):

    topic = get_topic_by_id(topic_id)
    category = get_category_by_id(category_id)

    if category.is_private:
        if not users_access_state(current_user.id, category_id):
            return Response(status_code=401, content='You are not authorized!')

    if topic.is_locked or category.is_locked:
        return Response(status_code=423, content='Topic is locked')

    reply = reply_service.get_by_id(reply_id)
    return reply_service.vote_change(new_vote, reply, current_user)


