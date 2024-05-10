from typing import Annotated

from fastapi import APIRouter, Depends, Response

from common.auth import get_current_active_user, get_current_admin_user
from data_.models import TopicQueryParams, Category, User, VisibilityAuth, AccessRevocation, Role
from services.category_service import get_all_categories, create, user_access_state, lock
from services.category_service import (get_topics_for_category, grant_category_read_access, grant_category_write_access,
                                       revoke_category_read_or_write_access, get_privileged_users)


category_router = APIRouter(prefix='/categories')

@category_router.get("/") # da ne se vijdat private categories osven za admin ili s prava
async def read_categories(current_user: Annotated[User, Depends(get_current_active_user)]):

    categories = get_all_categories(current_user)
    return categories


@category_router.get('/{category_id}/topics')
async def get_topics_by_category(
    category_id: int, current_user: Annotated[User, Depends(get_current_active_user)],
    params: TopicQueryParams = Depends(),
):
    is_admin = current_user.is_admin()
    topics = get_topics_for_category(current_user.id, category_id, params.search, params.sort_by, params.page, params.limit, is_admin)
    return topics

@category_router.post('/')
async def create_category(category: Category,
                          admin: Annotated[User, Depends(get_current_admin_user)]):
    if not admin:
        return Response(status_code=401, content='You are not authorized!')

    return create(category)


@category_router.put('/{category_id}/visibility')
async def category_access(visibility: VisibilityAuth, category_id: int,
                          admin: Annotated[User, Depends(get_current_admin_user)]):

    if not admin:
        return Response(status_code=401, content='You are not authorized!')

    return user_access_state(visibility, category_id)


@category_router.post("/{category_id}/users/{user_id}/read")
async def give_read_access(category_id: int, user_id: int,
                           admin: Annotated[User, Depends(get_current_admin_user)]):
    if not admin:                                                                             #.Role
        return Response(status_code=401, content='You are not authorized!')
    result = grant_category_read_access(user_id, category_id)
    return result


@category_router.post("/{category_id}/users/{user_id}/write")
async def give_write_access(category_id: int, user_id: int,
                            admin: Annotated[User, Depends(get_current_admin_user)]):
    if not admin:                                                                                                 #.Role
        return Response(status_code=401, content='You are not authorized!')
    result = grant_category_write_access(user_id, category_id)
    return result


@category_router.put("/{category_id}/users/{user_id}/revoke")
async def revoke_access(category_id: int, user_id: int, access: AccessRevocation,
                        admin: Annotated[User, Depends(get_current_admin_user)]):
    if not admin:                                                                                                   #.Role
        return Response(status_code=401, content='You are not authorized!')
    result = revoke_category_read_or_write_access(user_id, category_id, access.revoke_read, access.revoke_write)
    return result


@category_router.get("/{category_id}/privileged-users")
async def view_privileged_users(category_id: int, admin: Annotated[User, Depends(get_current_admin_user)]):
    if not admin:
        return Response(status_code=401, content='You are not authorized!')
    users = get_privileged_users(category_id)
    return {"category_id": category_id, "users": users}


@category_router.put('/lock/{category_id}')
async def lock_category(category_id: int,
                        admin: Annotated[User, Depends(get_current_admin_user)]):

    if not admin:
        return Response(status_code=401, content='You are not authorized!')
    return lock(category_id, admin)
