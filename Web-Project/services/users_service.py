from string import punctuation, whitespace, digits, ascii_lowercase, ascii_uppercase
from common import auth
from data_.models import *
from data_.database import read_query, insert_query
from fastapi import HTTPException, Header

_SEPARATOR = ';'
ALGORITHM = "HS256"

def create(username: str, password: str, first_name: str, last_name: str, email: str,
           date_of_birth: date) -> User | None:

    existing_user = read_query('SELECT id FROM users WHERE username = ?', (username,))
    if existing_user:
        raise HTTPException(status_code=400, detail=f'Username {username} is taken.')

    hash_password = auth.get_password_hash(password)

    generated_id = insert_query(
        'INSERT INTO users(username, first_name, last_name, email, date_of_birth, hashed_password) VALUES (?,?,?,?,?,?)',
        (username, first_name, last_name, email, date_of_birth, hash_password))


    return  User(id=generated_id, username=username, password=password, first_name=first_name, last_name=last_name,
                email=email, date_of_birth=date_of_birth, hashed_password=hash_password)

def find_by_username(username: str) -> User | None:
    data = read_query(
        '''SELECT id, username, first_name,
        last_name, email, date_of_birth, hashed_password, role
        FROM users WHERE username = ?''',
        (username,))

    return next((User.from_query_result(*row) for row in data), None)

def find_by_id(id):
    data = read_query(
        '''SELECT username
        FROM users WHERE id = ?''',
        (id,))
    if data:
        return data[0][0]


def users_access_state(user_id, category_id):

    access_data = read_query('''
    SELECT user_id
    FROM category_access
    WHERE category_id = ? AND user_id = ?''',
    (category_id, user_id))

    if not access_data:
        return False

    return True




def all():  # само за админ
    data = read_query('''SELECT id, username, password, first_name, last_name, email, date_of_birth FROM users''')
    return (User.from_query_result(*row) for row in data)





#
# def try_login(username: str, password: str) -> User | None:
#     user = find_by_username(username)
#
#     # password = _hash_password(password)
#     return user if user and user.password == password else None
#
#
# def create_access_token(user: User) -> dict:
#     # note: this token is not particulary secure, use JWT for real-world uses
#     username = f'{user.id}{_SEPARATOR}{user.username}'
#
#     passw = [str(ord(p) + 10) for p in user.password]
#     user.password = ''.join(passw)
#
#     return {'username': username,
#             'password': user.password}
#
#
#
# def from_token(token: str) -> User | None:
#     _, username = token.split(_SEPARATOR)
#
#     return find_by_username(username)
#
#
#
#     return data[0][0]

# def is_authenticated(token: str) -> bool:
#     return any(read_query(
#         'SELECT 1 '
#         'FROM users '
#         'where id = ? and username = ?',
#
#         token.split(_SEPARATOR)))
#
#
# def get_token_header(token: str = Header()):
#     if not is_authenticated(token):
#         raise HTTPException(status_code=401, detail="Invalid or missing token")
#
#     return token  #!!
#
#
#
# def is_valid_password(password):
#     new_password = password.strip()
#
#     MIN_SIZE = 6
#     MAX_SIZE = 50
#     password_size = len(new_password)
#
#     if password_size < MIN_SIZE or password_size > MAX_SIZE:
#         return False
#
#     valid_chars = {'-', '_', '.', '!', '@', '#', '$', '^', '&', '(', ')'}
#     invalid_chars = set(punctuation + whitespace) - valid_chars
#
#     for char in invalid_chars:
#         if char in new_password:
#             return False
#
#     password_has_digit = False
#
#     for char in password:
#         if char in digits:
#             password_has_digit = True
#             break
#
#     if not password_has_digit:
#         return False
#
#     password_has_lowercase = False
#
#     for char in password:
#         if char in ascii_lowercase:
#             password_has_lowercase = True
#             break
#
#     if not password_has_lowercase:
#         return False
#
#     password_has_uppercase = False
#
#     for char in password:
#         if char in ascii_uppercase:
#             password_has_uppercase = True
#             break
#
#     if not password_has_uppercase:
#         return False
#
#     return True
#
#
# def validate_input(username: str) -> bool:
#     if len(username) < 4 or len(username) > 45:
#         return False
#     return True





