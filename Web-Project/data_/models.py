from typing import Optional, List
from fastapi import Query
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime

from data_.database import read_query


class Role:

    ADMIN = 'admin'
    USER = 'user'



class User(BaseModel):

    id: int = None or None
    username: str = Field(max_length=45)
    password: str | None = None
    first_name: str = Field(max_length=45)
    last_name: str = Field(max_length=45)
    email: EmailStr
    date_of_birth: date | None = None
    role: str = Field(default=Role.USER, description="User role, e.g., 'admin', 'user'")
    hashed_password: str | None = None
    disabled: bool | None = None


    @classmethod
    def from_query_result(cls, id: int, username: str, first_name: str, last_name: str, email: str,
                          date_of_birth: date, hashed_password,role):
        return cls(id=id,
                   username=username,
                   first_name=first_name,
                   last_name=last_name,
                   email=email,
                   date_of_birth=date_of_birth,
                   hashed_password=hashed_password,
                   role=role)

    def is_admin(self):
        return self.role == Role.ADMIN

class UserInDB(User):
    hashed_password: str


class LoginData(BaseModel):

    username: str = Field(max_length=45)
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class Message(BaseModel):

    id: int | None = None
    content: str = Field(min_length=1)
    sender_id: int | None = None
    receiver_id: int | None = None
    created_at: datetime = datetime.now()

    @classmethod
    def from_query_result(cls, id, content, sender_id, receiver_id,created_at):
        return cls(
            id=id,
            content=content,
            sender_id=sender_id,
            receiver_id=receiver_id,
            created_id=created_at.strftime('%Y/%m/%d')
       )


class MessageCreate(BaseModel):

    content: str = Field(min_length=1)
    receiver_id: int


class Topic(BaseModel):

    id: int | None = None
    title: str = Field(min_length=1, max_length=150)
    cur_date: datetime = datetime.now()
    last_reply: str | None = None
    user_id: int| None = None
    category_id: int| None = None
    best_reply: int | None = None
    is_locked:bool = Field(default=False)

    @classmethod
    def from_query_result(cls, id, title, cur_date,
                          last_reply, user_id, category_id, is_locked):
        return cls(
            id=id,
            title=title,
            cur_date=cur_date,
            last_reply= 'There are no replies on that topic yet!' if last_reply is None else last_reply,
            user_id=user_id,
            category_id=category_id,
            is_locked=is_locked)


class Category(BaseModel):
    id: int | None = None
    title: str = Field(min_length=1, max_length=150)
    description: str|None = None
    last_topic: str | None = None
    topic_cnt: int | None = None
    is_private: bool = Field(default=False, description="The category is visible for everyone")
    is_locked: bool = Field(default=False)


    @classmethod
    def from_query_result(cls, id, title, description,
                        last_topic, topic_cnt, is_private, is_locked
    ):

        return cls(
                    id= id,
                    title=title,
                    description= 'The title speaks for itself'
                    if description == None else description,
                    last_topic='There are no topics on this category yet'
                                if last_topic == None else last_topic,
                    topic_cnt=0 if topic_cnt == None else topic_cnt,
                    is_private=is_private,
                    is_locked=is_locked
                )


class CategoryAccess(BaseModel):
    category_id: int
    user_id: int
    can_read: bool = Field(default=True, description="The user can read the category")
    can_write: bool = Field(default=True, description="The user can add or edit posts in the category")


    @classmethod
    def from_query_result(cls, user_id,
                          category_id, can_read, can_write
                            ):

        return cls(
                    category_id=category_id,
                    user_id=user_id,
                    can_read=True if can_read == 1 else False,
                    can_write=True if can_write == 1 else False
                )


class AccessRevocation(BaseModel):
    revoke_read: bool = Field(default=False)
    revoke_write: bool = Field(default=False)


class Reply(BaseModel):

    id: int = None or None
    cur_date: datetime = datetime.now()
    content: str = Field(min_length=1)
    likes_cnt: int|None = None
    dislikes_cnt: int|None = 0
    topic_id: int|None = 0


    @classmethod
    def from_query_result(cls, id, cur_date, content, likes_cnt, dislikes_cnt, topic_id):
        return cls(
            id=id,
            cur_date=cur_date,
            content=content,
            likes_cnt=likes_cnt,
            dislikes_cnt=dislikes_cnt,
            topic_id=topic_id)


class Vote(BaseModel):

    reply_id: int = None or None
    users_id: int = None or None
    vote: int


class Conversation(BaseModel):

    username: str = None or None


class VisibilityAuth(BaseModel):
    visibility: int


class TopicQueryParams(BaseModel):
    search: Optional[str] = None
    sort_by: Optional[str] = None
    page: Optional[int] = Query(1, gt=0)
    limit: Optional[int] = Query(10, gt=0)
