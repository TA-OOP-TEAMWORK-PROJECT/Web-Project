from fastapi import APIRouter, Query, Response, Header
from fastapi.responses import JSONResponse
from services.users_service import *
from services import users_service
from data.models import *
from common.auth import *
from common.responses import *
from fastapi import HTTPException


users_router = APIRouter(prefix='/users')



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


        





@users_router.get('/')
def get_users():
    users = users_service.all()
    return users