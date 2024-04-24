from fastapi import HTTPException
from data_.models import User
from services.users_service import authenticate_user, from_token


def get_user_or_raise_401(token: str) -> User:
    if not authenticate_user(token):
        raise HTTPException(status_code=401, detail="Invalid token")
    user = from_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

