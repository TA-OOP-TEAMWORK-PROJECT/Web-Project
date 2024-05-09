from typing import Annotated
from fastapi import APIRouter, Response, Depends
from common.auth import User, get_current_active_user, get_current_user
from data_.models import Topic
from services import topic_service
from services.category_service import category_is_private, get_category_by_id
from services.topic_service import lock
from services.users_service import users_access_state

topic_router = APIRouter(prefix='/topic')

@topic_router.get('/')
def view_all_topics(
            sort: str = None or None,
            sort_by: str | None = None,
            search: str = None or None):

    result = topic_service.search_all_topics(search)

    if sort and (sort == 'asc' or sort == 'desc'):
        return topic_service.sort_all_topics(result, sort_by, is_reverse=sort=='desc')

    return result


@topic_router.get('/{id}')  # da ima read prava
def view_by_id(id: int,
               current_user: Annotated[User, Depends(get_current_active_user)]):

    topic = topic_service.get_topic_by_id(id, current_user)

    if topic is None:
        return Response(status_code=404)
    else:
        return topic


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


@topic_router.put('/{topic_id}/{reply_id}')
def view_best_reply(topic_id, reply_id,
               current_user: Annotated[User, Depends(get_current_user)]):

    return topic_service.best_reply(topic_id, reply_id, current_user)


@topic_router.patch('/lock/{topic_id}')
async def lock_topic(topic_id: int,
                        current_user: Annotated[User, Depends(get_current_active_user)]):

    return lock(topic_id, current_user)
