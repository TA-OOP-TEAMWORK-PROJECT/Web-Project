from typing import Annotated

from fastapi import APIRouter, Response, Header, Depends

from common.auth import User, get_current_active_user, get_current_user
# from common.auth import get_user_or_raise_401
from data_.models import Topic
from services import topic_service, reply_service

topic_router = APIRouter(prefix='/topic')

@topic_router.get('/')
def view_all_topics(
            sort: str = None or None,
            sort_by: str | None = None,
            search: str = None or None):  # search_by: str = None or None

    result = topic_service.search_all_topics(search)

    if sort and (sort == 'asc' or sort == 'desc'):
        return topic_service.sort_all_topics(result, sort_by, is_reverse=sort=='desc')

    return result


@topic_router.get('/{id}')
def view_by_id(id: int, current_user: Annotated[User, Depends(get_current_active_user)]):

    topic = topic_service.get_topic_by_id(id)

    if topic is None:
        return Response(status_code=404)
    else:
        return topic



@topic_router.post('/')
def create_topic(topic: Topic, current_user: Annotated[User, Depends(get_current_active_user)]): #, x_token: str = Header()

    # user = get_user_or_raise_401(x_token)

    topic = topic_service.create(topic)

    return topic_service.create_topic_response(topic) # user


@topic_router.put('/{topic_id}/{reply_id}')  # TODO
def view_reply(topic_id, reply_id, current_user: Annotated[User, Depends(get_current_user)]):

    a = current_user
    b = a.username
    result = reply_service.get_reply(1)

    if result:
        return result

    else:
        return Response(status_code=401)
