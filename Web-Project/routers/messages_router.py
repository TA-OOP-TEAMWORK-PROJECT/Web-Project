from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, Response


from common.auth import get_current_active_user
from data_.models import Message, User, MessageCreate, Conversation
from services import message_service
from services.users_service import is_authenticated, get_token_header
from common.responses import MessageServiceError

message_router = APIRouter(prefix='/messages', tags=["Messages"])


@message_router.post('/', response_model=Message)
def create_message(message: MessageCreate, current_user: Annotated[User, Depends(get_current_active_user)]):  #token: str = Depends(get_token_header)

    return message_service.create_message(message, current_user)


@message_router.get("/{user_id}", response_model=list[Message])
def get_conversation_endpoint(user_id: int, current_user: Annotated[User, Depends(get_current_active_user)]):

    return message_service.get_conversation(user_id, current_user)

    # except MessageServiceError as e:
    #     raise HTTPException(status_code=404, detail=str(e))


@message_router.get("/", response_model=list[Conversation])
def get_conversations_endpoint(current_user: Annotated[User, Depends(get_current_active_user)]):

    return message_service.get_conversations(current_user)
    # try:
    #     return message_service.get_conversations(current_user)
    # except MessageServiceError as e:
    #     raise HTTPException(status_code=404, detail=str(e))