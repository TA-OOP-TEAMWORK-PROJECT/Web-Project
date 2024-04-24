from string import punctuation, whitespace, digits, ascii_lowercase, ascii_uppercase
from typing import Optional, List
from data.models import *
from data.database import read_query, insert_query
from mariadb import IntegrityError
from fastapi import HTTPException

_SEPARATOR = ';'




def create(username: str, password: str, first_name: str, last_name: str, email: str, date_of_birth: date) -> User | None:
    try:
       
        existing_user = read_query('SELECT id FROM users WHERE username = ?', (username,))
        if existing_user:
            raise HTTPException(status_code=400, detail=f'Username {username} is taken.')
        
        generated_id = insert_query(
            'INSERT INTO users(username, password, first_name, last_name, email, date_of_birth) VALUES (?,?,?,?,?,?)',
            (username, password, first_name, last_name, email, date_of_birth))

        return User(id=generated_id, username=username, password='', first_name=first_name, last_name=last_name, email=email, date_of_birth=date_of_birth)

    except IntegrityError:
        return None







def all():
    data = read_query('''SELECT id, username, password, first_name, last_name, email, date_of_birth FROM users''')
    return (User.from_query_result(*row) for row in data)





def try_login(username: str, password: str) -> User | None:
    user = find_by_username(username)

    # password = _hash_password(password)
    return user if user and user.password == password else None

def find_by_username(username: str) -> User | None:
    data = read_query(
        'SELECT id, username, password, role FROM users WHERE username = ?',
        (username,))

    return next((User.from_query_result(*row) for row in data), None)

def is_authenticated(token: str) -> bool:
    return any(read_query(
        'SELECT 1 FROM users where id = ? and username = ?',
        # note: this token is not particulary secure, use JWT for real-world user
        token.split(_SEPARATOR)))




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


def validate_input(username: str) -> bool:
    if len(username) < 4 or len(username) > 45:
        return False
    return True