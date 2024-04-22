from fastapi import APIRouter, Query, Response, Header
from fastapi.responses import JSONResponse
from services.users_service import *
from services import users_service
from data.models import *
from common.auth import *
from common.responses import *

users_router = APIRouter(prefix='/users')

def register(data: LoginData):
    if not validate_input(data.username, data.password):
        return BadRequest("Invalid username or password format.")

    user = users_service.create(data.username, data.password)
    if user:
        return user
    else:
        return BadRequest(f'Username {data.username} is taken.')



@users_router.post('/login')
def login (data: LoginData):
    user = users_service.try_login(data.username, data.password)

    if user:
        token = users_service.create_token(user)
        return {'token': token}
    else:
        return BadRequest('Invalid login data')


@users_router.get('/')
def get_users(id: int | None=None):
    return users_service.get_all(id)