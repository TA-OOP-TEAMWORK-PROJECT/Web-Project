from pydantic import BaseModel, field_validator, constr, conint, EmailStr
from datetime import date, datetime  # date because it shows the date only / in the database it has time also/


class Role:  #Да се ориентираме по-лесно
    ADMIN = 'admin'
    USER = 'user'


class User(BaseModel):

    id: int | None = None
    username: str    # да има ли рестрикции като на базата данни, за да не гърми там, а тук
    password: str | None = None
    first_name: str
    last_name: str
    email: EmailStr    # email validator online through web client????
    date_of_birth: date
    admin_id: int | None = None
    token_id: int | None = None

    @classmethod
    def from_query_result(cls, id: int, username: str, password: str, first_name: str, last_name: str, email: str,
                          date_of_birth: date):
        return cls(id=id, username=username, password=password, first_name=first_name, last_name=last_name, email=email,
                   date_of_birth=date_of_birth)

    def is_admin(self):
        return self.role == Role.ADMIN

    @field_validator('date_of_birth')
    def date_restr(cls, value):
        if isinstance(value, str):
            try:
                return date.fromisoformat(value)
            except ValueError:
                raise ValueError(f"Invalid date format: {value}")
        return value



class LoginData(BaseModel):
    username: str
    password: str

class Admin(BaseModel):

    id: int | None = None
    users_id: int
    category_id: int


class Message(BaseModel): #date na message?
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
    reply_cnt: int               #Трябра ли да го има в таzи таблица или, когато го визуализираме в приложението можем да отидем до базата през таблицата на Reply
    last_topic: str
    topic_cnt: int
    user_id: int


class Topic(BaseModel):

    id: int | None = None
    title: str
    cur_date: datetime = datetime.now()    #да се сетва по дефолт на днес?
    reply_cnt: int
    view_cnt: int
    last_reply: str
    users_id: int
    category_id: int

    #
    # @field_validator('cur_time')
    # def set_time(cls, value):
    #     return datetime.now()


class Reply(BaseModel):

    id: int | None = None
    cur_date: datetime = datetime.now()
    content: str
    likes_cnt: int
    dislikes_cnt: conint(ge=0)  ## Подсигурява, че неможем да имаме негативен брой ляйк/дисляйк, вместо проверка.
    topic_id: int
    user_id: int
    vote_id: int

    # @field_validator('cur_time')
    # def set_time(cls, value):
    #     return datetime.now()

    # @field_validator('dislikes_cnt')
    # def dislike_restr(cls, value):
    #     if value < 0:
    #         return 0
    #     return value



class Vote(BaseModel):
    users_id: int | None = None
    reply_id: int | None = None
    vote: int | None = None




class Conversation(BaseModel):
    id: int | None = None
    content: list[Message] or None