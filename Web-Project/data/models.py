from string import punctuation, whitespace, digits, ascii_lowercase, ascii_uppercase
from pydantic import BaseModel, field_validator
from datetime import date, datetime



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




    @field_validator('username')
    def username_check(cls, value):
        if len(value) > 45:
            raise ValueError('Username too long!')
        return value
    
    @field_validator('date_of_birth')
    def validate_date_of_birth(cls, date_value):

        input_date = datetime.striptime(date_value, '%Y-&m-%d')

        if input_date > date.today():
            raise ValueError('Date must be in the past!')
        
        year, mount, cur_date = date_value.split('/')
        if not len(year) == 4 and len(mount) == 2 and len(cur_date) == 2: 
            raise ValueError('Invalid date format')

        return input_date

    @field_validator('password')
    def check_password(cls, value):
    
        if not is_valid_password(value):
            raise ValueError('Invalid password')

        return value

    @field_validator('last_name')
    def check_last_name(cls, value):
        if len(value) > 45:
            return ValueError('Last name must be less than 45 symbols')
        return value
    
    @field_validator('first_name')
    def check_last_name(cls, value):
        if len(value) > 45:
            return ValueError('First name must be less than 45 symbols')
        return value



class Category(BaseModel):
    id: int | None 
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
    id: int | None
    users_id:int
    category_id:int

class Vote(BaseModel):
    id: int | None
    upvote: int
    downvote: int



def is_valid_password(password):
    new_password = password.strip()

    MIN_SIZE = 6
    MAX_SIZE = 50
    password_size = len(new_password)

    if password_size < MIN_SIZE or password_size > MAX_SIZE:
        return False

    valid_chars = {'-', '_', '.', '!', '@', '#', '$', '^', '&', '(', ')'}
    invalid_chars = set(punctuation + whitespace) - valid_chars

    for char in invalid_chars:
        if char in new_password:
            return False

    password_has_digit = False

    for char in password:
        if char in digits:
            password_has_digit = True
            break

    if not password_has_digit:
        return False

    password_has_lowercase = False

    for char in password:
        if char in ascii_lowercase:
            password_has_lowercase = True
            break

    if not password_has_lowercase:
        return False

    password_has_uppercase = False

    for char in password:
        if char in ascii_uppercase:
            password_has_uppercase = True
            break

    if not password_has_uppercase:
        return False

    return True
