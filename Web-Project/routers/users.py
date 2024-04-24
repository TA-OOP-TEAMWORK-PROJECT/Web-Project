from fastapi import APIRouter, Header, HTTPException
from common.auth import get_user_or_raise_401
from data_.models import User, LoginData
from services import users_service
from common.responses import BadRequest


users_router = APIRouter(prefix='/users')

@users_router.get('/info')
def users_info(x_token: str):
    return get_user_or_raise_401(x_token)

@users_router.post('/login')
def login(data: LoginData):
    user = users_service.try_login(data.username, data.password)
    if user:
        token = users_service.create_access_token({"sub": user.username})
        return {'token': token}
    else:
        return BadRequest('Invalid login data')

@users_router.post('/register')
def register_user(user: User):
    created_user = users_service.create_user(user)
    if not created_user:
        raise BadRequest(f'Username {user.username} is taken!')

    return created_user.dict(exclude={"password"})
