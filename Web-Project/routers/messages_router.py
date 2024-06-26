from typing import Annotated
from fastapi import APIRouter, Depends
from common.auth import get_current_active_user
from data_.models import Message, User, MessageCreate, Conversation
from services import message_service


message_router = APIRouter(prefix='/messages', tags=["Messages"])


@message_router.post('/')
def create_message(message: MessageCreate, current_user:
                   Annotated[User, Depends(get_current_active_user)]):

    return message_service.create_message(message, current_user)


@message_router.get("/{user_id}")
def get_conversation(user_id: int,
                              current_user: Annotated[User, Depends(get_current_active_user)]):

    return message_service.get_conversation(user_id, current_user)


@message_router.get("/")
def get_conversations(current_user: Annotated[User, Depends(get_current_active_user)]):

    return message_service.get_conversations(current_user)
