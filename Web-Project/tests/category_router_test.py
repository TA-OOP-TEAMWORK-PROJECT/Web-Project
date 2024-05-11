from fastapi import Response, status
from datetime import timedelta
import pytest
from httpx import AsyncClient
from httpx._client import ASGITransport
from unittest.mock import patch, MagicMock
import sys
sys.path.append('D:\\Telerik\\Week 13 - 19\\Web-Project\\Web-Project\\Web-Project')
from main import app
from common.auth import create_access_token
from data_.models import Category

@pytest.fixture
def admin_token():
    token_data = {'sub': 'gosho123', 'user_id': 1, 'role': 'admin'}
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=3000))


@pytest.fixture
def regular_token():
    token_data = {'sub': 'pesho5', 'user_id': 2, 'role': 'user'}
    return create_access_token(data=token_data, expires_delta=timedelta(minutes=3000))


@pytest.fixture
def admin_user():
    user = MagicMock()
    user.username = 'gosho123'
    user.id = 1
    user.is_admin.return_value = True
    user.first_name = 'Georgi'
    user.last_name = 'Georgiev'
    user.email = 'georgi@teenproblem.com'
    user.hashed_password = 'hashed_password'
    user.role = 'admin'
    return user


@pytest.fixture
def regular_user():
    user = MagicMock()
    user.username = 'pesho5'
    user.id = 2
    user.is_admin.return_value = False
    user.first_name = 'Pesho'
    user.last_name = 'Peshev'
    user.email = 'pesho@teenproblem.com'
    user.hashed_password = 'hashed_password'
    user.role = 'user'
    return user


@pytest.mark.asyncio
async def test_get_all_authenticated_as_admin(admin_token, admin_user):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        with patch('services.category_service.get_all_categories', return_value=[{"id": 1, "title": "Test Category"}]), \
             patch('common.auth.get_current_active_user', return_value=admin_user):
            response = await ac.get("/categories/", headers={"Authorization": f"Bearer {admin_token}"})
            assert response.status_code == 200
            response_data = response.json()

            assert isinstance(response_data, dict)
            assert "Category name: Love & Robots" in response_data
            category_details = response_data["Category name: Love & Robots"]
            assert category_details['Category title'] == 'Love & Robots'
            assert category_details['Description'] == 'love in the era of ai'
            assert 'Last topic is:' in category_details
            assert 'Number of topics in category' in category_details


@pytest.mark.asyncio
async def test_no_categories_available(admin_token, admin_user):
    with patch('data_.database.read_query', return_value=[]):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            with patch('services.category_service.get_all_categories', return_value=[]), \
                 patch('common.auth.get_current_active_user', return_value=admin_user):
                response = await ac.get("/categories/", headers={"Authorization": f"Bearer {admin_token}"})
                assert response.status_code == 200
                response_data = response.json()
                assert "Category name: Love & Robots" in response_data
                assert response_data["Category name: Love & Robots"]["Number of topics in category"] == 0



@pytest.mark.asyncio
async def test_create_category_success(admin_token, admin_user):
    new_category = {
        "title": "Misunderstood Teens",
        "description": "A category dedicated to parents seeking help."
    }
    expected_response = "Category with title Misunderstood Teens was created successfully!"
    with patch('routers.category_router.create', return_value=expected_response) as mock_create, \
         patch('common.auth.get_current_admin_user', return_value=admin_user):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/categories/", json=new_category, headers={"Authorization": f"Bearer {admin_token}"})
            assert response.status_code == 200
            assert response.json() == expected_response
            mock_create.assert_called_once_with(Category(**new_category))

@pytest.mark.asyncio
async def test_create_category_unauthorized(regular_token, regular_user):
    new_category = {
        "title": "No Name",
        "description": "Can't create it, sorry!"
    }
    with patch('routers.category_router.create') as mock_create, \
         patch('common.auth.get_current_active_user', side_effect=Response(status_code=403, content="Access denied")):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            response = await ac.post("/categories/", json=new_category, headers={"Authorization": f"Bearer {regular_token}"})
            assert response.status_code == 403
            assert 'detail' in response.json()
            assert response.json()['detail'] == "Access denied"
            mock_create.assert_not_called()
