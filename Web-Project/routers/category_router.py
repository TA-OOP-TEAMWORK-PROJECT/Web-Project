from fastapi import APIRouter, Depends

from data_.models import TopicQueryParams
from services.category_service import get_all_categories
from services.category_service import get_topics_for_category


category_router = APIRouter(prefix='/category')

@category_router.get("/")
async def read_categories():
    categories = get_all_categories()
    return categories



@category_router.get('/{category_id}/topics')
def get_topics_by_category(
    category_id: int,
    params: TopicQueryParams = Depends(),
):
    topics = get_topics_for_category(category_id, params.search, params.sort_by, params.page, params.limit)
    return topics
