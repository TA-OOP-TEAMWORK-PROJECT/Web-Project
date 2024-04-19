
from pydantic import BaseModel,field_validator
from datetime import date, datetime  # date because it shows the date only / in the database it has time also/

class User(BaseModel):

    id: int = None or None
    username: str    # да има ли рестрикции като на базата данни, за да не гърми там, а тук
    password: str   #validator?
    first_name: str
    last_name: str
    email: str    # email validator online through web client????
    date_of_birth: str
    admin_id: int
    token_id: int

    @field_validator('username')
    def username_rest(cls, value):
        if len(value) > 45:
            raise ValueError('Username is too long!')
        return value

    @field_validator('date_of_birth')
    def date_restr(cls, date_value):

        date_obj = datetime.strptime(date_value, '%Y-%m-%d')
        min_date = datetime.strptime('1907-01-01', '%Y-%m-%d')

        year, mount, cur_date = date_value.split('/')
        if not len(year) == 4 and len(mount) == 2 and len(cur_date) == 2: #при положение, че месеца и деня започва с 0
            raise ValueError('Invalid date format')

        if date_obj > date.today():
            raise ValueError('Possibly you are not born in the future')

        if date_obj < min_date:
            raise ValueError('You are not a vempire!')

        return date_obj




class Admin(BaseModel):

    id: int = None or None
    users_id: int
    category_id: int


class Message(BaseModel): #date na message?
    id: int = None or None
    content: str
    sender_id: int
    receiver_id: int


class Category(BaseModel):

    id: int = None or None
    title: str
    description: str
    reply_cnt: int               #Трябра ли да го има в таzи таблица или, когато го визуализираме в приложението можем да отидем до базата през таблицата на Reply
    last_topic: str
    topic_cnt: int
    user_id: int


class Topic(BaseModel):

    id: int = None or None
    title: str
    cur_date: datetime.now()    #да се сетва по дефолт на днес?
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

    id: int = None or None
    cur_date: datetime.now()
    content: str
    likes_cnt: int
    dislikes_cnt: int
    topic_id: int
    user_id: int
    vote_id: int

    # @field_validator('cur_time')
    # def set_time(cls, value):
    #     return datetime.now()

    @field_validator('dislikes_cnt')
    def dislike_restr(cls, value):
        if value < 0:
            return 0
        return value



class Vote(BaseModel):

    id: int = None or None
    upvote: int = 1
    downvote: int = 1

    @field_validator('dislikes_cnt')
    def downvote_restr(cls, value):
        if value < 0:
            return 0
        return value
