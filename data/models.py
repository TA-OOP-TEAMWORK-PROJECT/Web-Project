from typing import Optional
from pydantic import BaseModel, validator
from datetime import datetime, date
from typing import List

class User(BaseModel):
    id: Optional[int] = None
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    date_of_birth: date
    

    @classmethod
    def from_query_result(cls, id: int, username: str, password: str, first_name: str, last_name: str, email: str, date_of_birth: date):
        return cls(id=id, username=username, password=password, first_name=first_name, last_name=last_name, email=email, date_of_birth=date_of_birth)

    def is_admin(self):
        return self.role == Role.ADMIN

class Role:
    CUSTOMER = 'user'
    ADMIN = 'admin'



class LoginData(BaseModel):
    username: str
    password: str


class Topic(BaseModel):
    id: int | None
    title: str
    date: datetime
    reply_cnt: int
    view_cnt: int
    last_reply: str
    users_id: int
    category_id: int

class Category(BaseModel):
    id: int | None 
    title: str
    description: str
    reply_cnt: Optional[int]
    last_topic: Optional[int]
    topic_cnt: Optional[int]
    users_id: int
    
    topics: List[Topic] = []

    @classmethod
    def from_query_result(
        cls,
        id: Optional[int] = None,
        title: str = "",
        description: str = "",
        reply_cnt: Optional[int] = None,
        last_topic: Optional[int] = None,
        topic_cnt: Optional[int] = None,
        users_id: int = 0
    ):
        return cls(
            id=id,
            title=title,
            description=description,
            reply_cnt=reply_cnt,
            last_topic=last_topic,
            topic_cnt=topic_cnt,
            users_id=users_id
        )






    


class Replay(BaseModel):
    id: int | None
    date: datetime
    content: str
    likes_cnt: int
    dislike_cnt: int
    topic_id: int
    user_id: int
    vote_id: int



class message(BaseModel):
    id: int | None
    content: str
    sender_id: int
    receiver_id: int

class Admin(BaseModel):
    id: int | None
    users_id:int
    category_id:int

class Vote(BaseModel):
    id: int | None
    upvote: int
    downvote: int



