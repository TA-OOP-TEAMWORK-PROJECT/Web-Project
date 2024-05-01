from fastapi import APIRouter, Response, Header
# from common.auth import get_user_or_raise_401
from data_.models import Topic
from services import topic_service


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
def view_by_id(id: int):

    topic = topic_service.get_topic_by_id(id)

    if topic is None:
        return Response(status_code=404)
    else:
        return topic




@topic_router.post('/')
def create_topic(topic: Topic): #, x_token: str = Header()

    # user = get_user_or_raise_401(x_token)

    topic = topic_service.create(topic)

    return topic_service.create_topic_response(topic) # user

