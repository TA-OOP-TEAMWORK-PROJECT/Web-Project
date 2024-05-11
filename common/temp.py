from data_.models import User
from data_.database import read_query


def find_by_username(username: str) -> User | None:
    data = read_query(
        '''SELECT id, username, first_name,
        last_name, email, date_of_birth, hashed_password
        FROM users WHERE username = ?''',
        (username,))