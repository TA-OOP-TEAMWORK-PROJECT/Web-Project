from fastapi import APIRouter, Query, Depends
from typing import List
from services.category_service import get_all_categories
from data.models import Category, Topic
from pydantic import BaseModel
from typing import List, Optional
from services.category_service import get_topics_for_category
category_router = APIRouter(prefix='/category')

@category_router.get("/", response_model=List[Category])
async def read_categories():
    categories = get_all_categories()
    return categories

class TopicQueryParams(BaseModel):
    search: Optional[str] = None
    sort_by: Optional[str] = None
    page: Optional[int] = Query(1, gt=0)
    limit: Optional[int] = Query(10, gt=0)

@category_router.get('/{category_id}/topics', response_model=List[Topic])
def get_topics_by_category(
    category_id: int,
    params: TopicQueryParams = Depends(),
):
    topics = get_topics_for_category(category_id, params.search, params.sort_by, params.page, params.limit)
    return topics