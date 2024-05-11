import pytest
from datetime import date
from data_.models import User
from services.users_service import *
from fastapi import HTTPException
from unittest.mock import patch
from common.temp import find_by_username

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

@pytest.mark.asyncio
async def test_get_all_users():
    dummy_data = [
        (1, 'user1', 'password1', 'Test1', 'Test2', 'test2@gmail.com', '2000, 1, 1'),
        (2, 'user2', 'password2', 'Test3', 'test4', 'test3@gmail.com', '2000, 1, 2')
    ]
    with patch('services.users_service.all') as mock_all:
        mock_all.return_value = (User.from_query_result(*row) for row in dummy_data)

        users = list(mock_all())


@pytest.fixture
def mock_find_by_username(monkeypatch):
    def mock_find_by_username(username):
        # Вместо това можете да върнете фиктивен обект User, създаден по ваше желание
        return User(id=1, username=username, first_name="Test", last_name="User", email="test@example.com",
                    date_of_birth=date(2000, 1, 1), hashed_password="hashed_password")
    monkeypatch.setattr('common.temp.find_by_username', mock_find_by_username)

def test_try_login_successful(mock_find_by_username):
    # Тест, когато съществува потребител с подаденото потребителско име и парола
    username = "testuser"
    password = "password123"
    user = try_login(username, password)
    assert user is not None
    assert user.username == username

def test_try_login_unsuccessful(mock_find_by_username):
    # Тест, когато не съществува потребител с подаденото потребителско име или парола
    username = "non_existing_user"
    password = "wrong_password"
    user = try_login(username, password)
    assert user is None