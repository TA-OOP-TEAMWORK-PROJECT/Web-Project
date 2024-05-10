import pytest
from datetime import date
from data_.models import User
from services.users_service import *
from fastapi import HTTPException
from unittest.mock import patch


@pytest.mark.asyncio
async def test_create_user():
    username = 'testuser'
    password = 'testpassword'
    first_name = 'Test'
    last_name = 'User'
    email = 'test@test.com'
    date_of_birth = date(2000, 1, 1)

    created_user = create(username, password, first_name, last_name, email, date_of_birth)

    assert isinstance(created_user, User)
    assert created_user.username == username
    assert created_user.first_name == first_name
    assert created_user.last_name == last_name
    assert created_user.email == email
    assert created_user.date_of_birth == date_of_birth
    assert created_user.role == 'user'
    assert created_user.hashed_password is not None
    assert created_user.disabled is None

    with pytest.raises(HTTPException) as exc_info:
        create(username, password, first_name, last_name, email, date_of_birth)
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == f'Username {username} is taken.'


@pytest.fixture(autouse=True)
def clean_up():
    yield

    delete_user('testuser')  # Изтриваме потребителя със съответното потребителско име

''''
def delete_user(username: str) -> bool:
    sql = "DELETE FROM users WHERE username = ?"
    result = update_query(sql, (username,))
    return result > 0
'''

@pytest.mark.asyncio
async def test_get_all_users():
    dummy_data = [
        (1, 'user1', 'password1', 'Test1', 'Test2', 'test2@gmail.com', '2000, 1, 1'),
        (2, 'user2', 'password2', 'Test3', 'test4', 'test3@gmail.com', '2000, 1, 2')
    ]
    with patch('services.users_service.all') as mock_all:
        mock_all.return_value = (User.from_query_result(*row) for row in dummy_data)

        users = list(mock_all())