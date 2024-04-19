from pydantic import BaseModel
from datetime import *



class User(BaseModel):
    id: int | None
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    date_of_birth: str
    admin_id: int
    token_id: int


class Category(BaseModel):
    id: int 
    title: str
    description: str
    reply_cnt: int
    last_topic: int
    topic_cnt: int
    Users_id: int


class Topic(BaseModel):
    id: int | None
    title: str
    date: datetime
    reply_cnt: int
    view_cnt: int
    last_replay: str
    user_id: int
    category_id: int

    @classmethod
    def from_query_result(cls, id, name, description, price, category_id):
        return cls(
            id=id,
            name=name,
            description=description,
            price=price,
            category_id=category_id)


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
    id: int
    users_id:int
    category_id:int

class Vote(BaseModel):
    id: int
    upvote: int
    downvote: int