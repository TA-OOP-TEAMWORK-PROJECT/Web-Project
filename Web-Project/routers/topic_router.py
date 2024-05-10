from typing import Annotated
from fastapi import APIRouter, Response, Depends
from common.auth import User, get_current_active_user, get_current_user, get_current_admin_user
from data_.models import Topic
from services import topic_service
from services.category_service import category_is_private, get_category_by_id
from services.topic_service import lock, create_topic_response
from services.users_service import users_access_state

topic_router = APIRouter(prefix='/topics')

@topic_router.get('/')
def view_all_topics(
            current_user: Annotated[User, Depends(get_current_active_user)],
            sort: str = None or None,
            sort_by: str | None = None,
            search: str = None or None):

    result = topic_service.search_all_topics(current_user, search)

    if sort and (sort == 'asc' or sort == 'desc'):
        return topic_service.sort_all_topics(result, sort_by, is_reverse=sort=='desc')

    return result


@topic_router.get('/categories/{category_id}/{topic_id}')
def view_by_id(category_id: int, topic_id: int,
               current_user: Annotated[User, Depends(get_current_active_user)]):

    topic = topic_service.get_topic_by_id(topic_id)
    category = get_category_by_id(category_id)

    if category.is_private and not current_user.is_admin():
        if not users_access_state(current_user.id, category_id):
            return Response(status_code=401, content='You are not authorized!')

    if topic is None:
        return Response(status_code=404)
    else:
        return create_topic_response(topic, current_user)


@topic_router.post('/{category_id}')
def create_topic(topic: Topic, category_id: int,
                 current_user: Annotated[User, Depends(get_current_active_user)]):

    category = get_category_by_id(category_id)
    if category.is_private:

        if not users_access_state(current_user.id, category_id):
            return Response(status_code=401, content='You are not authorized!')

    if category.is_locked:
        return Response(status_code=423, content='Category is locked')

    topic = topic_service.create(topic, current_user, category_id)

    return topic


@topic_router.put('/{topic_id}/replies/{reply_id}')
def view_best_reply(topic_id, reply_id,
               current_user: Annotated[User, Depends(get_current_user)]):

    return topic_service.best_reply(topic_id, reply_id, current_user)


@topic_router.put('/lock/{topic_id}')
async def lock_topic(topic_id: int,
                        user: Annotated[User, Depends(get_current_active_user)]):

    if not user.is_admin():
        return Response(status_code=401, content='You are not authorized!')

    return lock(topic_id, user)
