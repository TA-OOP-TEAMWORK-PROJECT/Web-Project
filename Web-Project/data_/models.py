from typing import Optional, List
from fastapi import Query
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime



class Role:

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'
    GUEST = 'guest'


class User(BaseModel):

    id: int = None or None
    username: str = Field(max_length=45)
    password: str | None = None
    first_name: str = Field(max_length=45)
    last_name: str = Field(max_length=45)
    email: EmailStr
    date_of_birth: date | None = None
    admin_id: int | None = None
    hashed_password: str | None = None
    disabled: bool | None = None
    # roles: List[Role] = ['user']

    @classmethod
    def from_query_result(cls, id: int, username: str, first_name: str, last_name: str, email: str,
                          date_of_birth: date, hashed_password):
        return cls(id=id,
                   username=username,
                   first_name=first_name,
                   last_name=last_name,
                   email=email,
                   date_of_birth=date_of_birth,
                   hashed_password=hashed_password)

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


class Admin(BaseModel):

    id: int | None = None
    users_id: int
    category_id: int


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
            created_id=created_at
       )


class MessageCreate(BaseModel):

    content: str = Field(min_length=1)
    receiver_id: int


class Topic(BaseModel):

    id: int | None = None
    title: str = Field(min_length=1, max_length=150)
    cur_date: datetime = datetime.now()
    reply_cnt: int|None = 0
    view_cnt: int|None = 0
    last_reply: str | None = None
    user_id: int| None = None
    category_id: int| None = None
    best_reply: int | None = None
    @classmethod
    def from_query_result(cls, id, title, cur_date, reply_cnt,
                          view_cnt, last_reply, user_id, category_id):
        return cls(
            id=id,
            title=title,
            cur_date=cur_date,
            reply_cnt= 0 if reply_cnt==None else reply_cnt,
            view_cnt=0 if view_cnt==None else view_cnt,
            last_reply= 'There are no replies on that topic yet!' if last_reply is None else last_reply,
            user_id=user_id,
            category_id=category_id)


class Category(BaseModel):
    id: int | None = None
    title: str=  Field(min_length=1, max_length=150)
    description: str = Field(min_length=1)
    reply_cnt: int | None
    last_topic: str | None
    topic_cnt: int | None
    user_id: int


    @classmethod
    def from_query_result(cls, id, title, description, reply_cnt,
                          last_topic, topic_cnt, user_id
    ):


        return cls(
                    id=id,
                    title=title,
                    description=description,
                    reply_cnt=0 if reply_cnt == None else reply_cnt,
                    last_topic='There are no topics on this category yet'
                                if last_topic == None else last_topic,
                    topic_cnt=0 if topic_cnt == None else topic_cnt,
                    user_id=user_id or None
                )


class Reply(BaseModel):

    id: int = None or None
    cur_date: datetime = datetime.now()
    content: str = Field(min_length=1)
    likes_cnt: int|None = None
    dislikes_cnt: int|None= None ## Подсигурява, че не можем да имаме негативен брой ляйк/дисляйк, вместо проверка.
    topic_id: int|None = None


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
    sender_id: int = None or None
    vote: int


class Conversation(BaseModel):

    username: str = None or None


class TopicQueryParams(BaseModel):
    search: Optional[str] = None
    sort_by: Optional[str] = None
    page: Optional[int] = Query(1, gt=0)
    limit: Optional[int] = Query(10, gt=0)
