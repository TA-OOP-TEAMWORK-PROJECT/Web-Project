from typing import Annotated

from fastapi import APIRouter, Depends

from common.auth import get_current_active_user
from data_.models import TopicQueryParams, Category, User, VisibilityAuth
from services.category_service import get_all_categories, create, user_access_state
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

@category_router.post('/')
async def create_category(category: Category,
                          current_user: Annotated[User, Depends(get_current_active_user)]):

    return create(category, current_user)


@category_router.put('/{category_id}/visibility')
async def create_category(visibility:VisibilityAuth, category_id: int,
                          current_user: Annotated[User, Depends(get_current_active_user)]):

    return user_access_state(visibility, category_id, current_user)





