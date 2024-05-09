from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from data_.models import LoginData, Token, User
from common.auth import (ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user,
                          create_access_token, get_current_active_user)

from common.auth import current_user

auth_router = APIRouter(prefix='/auth')


@auth_router.post("/login")
async def login_for_access_token(form_data: LoginData) -> Token:

    user_credentials = current_user(form_data.username)

    user = authenticate_user(user_credentials, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)]):

    return get_user_response(current_user)


def get_user_response(user):

    return {
        'Username': user.username,
        'Name': f'{user.first_name} {user.last_name}',
        'Email': user.email,
    }


















# @auth_router.get("/users/me/items/")
# async def read_own_items(current_user: Annotated[User, Depends(get_current_active_user)]):
#
#     return [{"item_id": "Foo", "owner": current_user.username}]

















# from fastapi.security import OAuth2PasswordRequestForm
# from pydantic import BaseModel
# from starlette.requests import Request
