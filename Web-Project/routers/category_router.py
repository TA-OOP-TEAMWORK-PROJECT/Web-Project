from fastapi import APIRouter, Depends
from typing import Annotated
from common.auth import User, get_current_active_user, get_current_user, get_current_admin_user
from data_.models import TopicQueryParams
from services.category_service import get_all_categories
from services.category_service import get_topics_for_category, grant_category_read_access


category_router = APIRouter(prefix='/category')

@category_router.get("/")
async def read_categories():
    categories = get_all_categories()
    return categories


@category_router.get('/{category_id}/topics')
def get_topics_by_category(
    category_id: int, user: Annotated[User, Depends(get_current_active_user)],
    params: TopicQueryParams = Depends(),
):
    topics = get_topics_for_category(user, category_id, params.search, params.sort_by, params.page, params.limit)
    return topics


@category_router.post("/{category_id}/users/{user_id}/read")
async def give_read_access(category_id: int, user_id: int, current_admin: Annotated[User, Depends(get_current_admin_user)]):
    result = grant_category_read_access(user_id, category_id)
    return result