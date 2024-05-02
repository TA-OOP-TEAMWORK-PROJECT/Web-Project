from fastapi import APIRouter, Query, Response, Header
from fastapi.responses import JSONResponse
from services.users_service import *
from services import users_service
from data_.models import *
from common.auth import *
# from common.responses import *
from fastapi import HTTPException

users_router = APIRouter(prefix='/users')

# @users_router.get('/info')   #admin
# def users_info(x_token: str = Header()):
#     return get_user_or_raise_401(x_token)


@users_router.post('/register')
def register(user_data: User):
    user = users_service.create(
        user_data.username,
        user_data.password,
        user_data.first_name,
        user_data.last_name,
        user_data.email,
        user_data.date_of_birth,
    )
    if user is not None:
        return {'message': f'User with username {user.username} has been created!'}
    else:
        return {'message': 'Failed to create user.'}, 500

# @users_router.post('/login')
# def login(login_data: LoginData):
#     user = users_service.find_by_username(login_data.username)
#
#     if user:
#         token = users_service.create_access_token(user)
#         return token
#         # return {'message': f'Username {user.username} is logged in!'}
#     else:
#         return Response(status_code=404, content='Invalid login data')  #BadRequest('Invalid login data')
#
#
# @users_router.get('/')
# def get_users(): # само за админ
#     users = users_service.all()
#     return users
