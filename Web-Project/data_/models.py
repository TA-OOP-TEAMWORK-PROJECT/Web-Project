from pydantic import BaseModel, field_validator, constr, conint, EmailStr
from datetime import date, datetime  # date because it shows the date only / in the database it has time also/

from common import auth


class Role:

    ADMIN = 'admin'
    USER = 'user'

class User(BaseModel):

    id: int = None or None
    username: str    # да има ли рестрикции като на базата данни, за да не гърми там, а тук
    password: str
    first_name: str
    last_name: str
    email: EmailStr    # email validator online through web client????
    date_of_birth: date = None or None
    admin_id: int = None or None
    hashed_password: str = None or None
    # disabled: bool | None = None
    #     password: str | None = None

    # @field_validator('hashed_password')
    # def hash_password(cls, User.password):
    #     # pass_value = auth.get_password_hash(pass_value)
    #     return pass_value


    @classmethod
    def from_query_result(cls, id: int, username: str, password: str, first_name: str, last_name: str, email: str,
                          date_of_birth: date):
        return cls(id=id, username=username, password=password, first_name=first_name, last_name=last_name, email=email,
                   date_of_birth=date_of_birth)

    def is_admin(self):
        return self.role == Role.ADMIN

class UserInDB(User):
    hashed_password: str


class LoginData(BaseModel):

    username: str
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
    content: str
    sender_id: int
    receiver_id: int
    created_at: datetime = datetime.now()


class MessageCreate(BaseModel):

    content: str
    receiver_id: int


class Category(BaseModel):

    id: int | None = None
    title: str
    description: str
    reply_cnt: int  # Трябра ли да го има в таzи таблица или, когато го визуализираме в приложението можем да отидем до базата през таблицата на Reply
    last_topic: str
    topic_cnt: int
    user_id: int


class Topic(BaseModel):

    id: int = None or None
    title: str
    cur_date: datetime = datetime.now()
    reply_cnt: int
    view_cnt: int
    last_reply: str | None = None
    user_id: int
    category_id: int
    best_reply :int = None or None
    @classmethod
    def from_query_result(cls, id, title, cur_date, reply_cnt,
                          view_cnt, last_reply, user_id, category_id):
        return cls(
            id=id,
            title=title,
            cur_date=cur_date,
            reply_cnt= 0 if reply_cnt==None else reply_cnt,
            view_cnt=0 if view_cnt==None else view_cnt,
            last_reply=last_reply,
            user_id=user_id,
            category_id=category_id)


class Reply(BaseModel):

    id: int = None or None
    cur_date: datetime = datetime.now()
    content: str
    likes_cnt: int = None or None
    dislikes_cnt: int = None or None ## Подсигурява, че не можем да имаме негативен брой ляйк/дисляйк, вместо проверка.
    topic_id: int


    @classmethod
    def from_query_result(cls, id, cur_date, content, likes_cnt, dislikes_cnt, topic_id, user_id):
        return cls(
            id=id,
            cur_date=cur_date,
            content=content,
            likes_cnt=likes_cnt,
            dislikes_cnt=dislikes_cnt,
            topic_id=topic_id,
            user_id=user_id)


class Vote(BaseModel):

    reply_id: int = None or None
    sender_id: int = None or None
    vote: int


class Conversation(BaseModel):

    id: int | None = None
    content: list[Message] or None