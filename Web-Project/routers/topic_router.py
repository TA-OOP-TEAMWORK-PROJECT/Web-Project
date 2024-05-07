from typing import Annotated
from fastapi import APIRouter, Response, Depends
from common.auth import User, get_current_active_user, get_current_user
from data_.models import Topic
from services import topic_service


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


@topic_router.get('/{id}')
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

    topic = topic_service.create(topic, current_user, category_id)
    return topic_service.create_topic_response(topic, current_user)


@topic_router.put('/{topic_id}/{reply_id}')
def view_reply(topic_id, reply_id,
               current_user: Annotated[User, Depends(get_current_user)]):


    return topic_service.best_reply(topic_id, reply_id, current_user)



