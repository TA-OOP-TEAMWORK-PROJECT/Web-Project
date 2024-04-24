from fastapi import Header, HTTPException
from data_.models import User
from passlib.context import CryptContext
from data_.database import insert_query, read_query
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from mariadb import IntegrityError

password_scheme = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = "secret_key"
ALGORITHM = "HS256"


def find_by_username(username: str) -> User | None:
    data = read_query(
        'SELECT * FROM users WHERE username = ?',
        (username,))

    return next((User.from_query_result(*row) for row in data), None)


def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)
    if user and password_scheme.verify(password, user.password):
        return user
    return None


def create_user(user: User) -> User | None:
    hashed_password = password_scheme.hash(user.password)
    try:
        user_id = insert_query("INSERT INTO users (username, password, email, first_name, last_name, date_of_birth) "
                               "VALUES (?, ?, ?, ?, ?, ?)",
                               (user.username, hashed_password, user.email, user.first_name, user.last_name, user.date_of_birth))
        return user.copy(update={"id": user_id, "password": None})

    except IntegrityError:
        return None


def generate_token_for_user(username: str, password: str) -> str | None:
    user_data = read_query("SELECT * FROM users WHERE username = ?", (username,))

    user = user_data[0] if user_data else None

    if user and password_scheme.verify(password, user['password']):
        token = create_access_token(data={"sub": user['username']})

        return token

    return None
#
#
def authenticate_user(token: str) -> bool:
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return True

    except JWTError:
        return None
#
#
def get_user_id_from_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get('sub')
        if not user_id:
            raise HTTPException(status_code=401, detail="Token missing user ID")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
#
#
def from_token(token: str) -> User | None:
        username = get_user_id_from_token(token)
        user_data = read_query("SELECT * FROM users WHERE username = ?", (username,))
        if user_data:
            return User.parse_obj(user_data[0])
        else:
            raise HTTPException(status_code=404, detail="User not found")
#
#
def create_access_token(data: dict[str:str], expires_delta: timedelta = timedelta(minutes=15)) -> str:
    to_encode = data.copy()
    # expire = datetime.now() + expires_delta
    # to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode({data["sub"]:data["sub"]}, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
#
#
def get_token_header(token: str = Header(...)):
    if not authenticate_user(token):
        raise HTTPException(status_code=401, detail="Invalid or missing token")

    return token