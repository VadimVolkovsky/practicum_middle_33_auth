import json
import subprocess

import pytest_asyncio

from models.entity import User
from tests.settings import test_settings


@pytest_asyncio.fixture
async def admin_authenticated_client(api_session, admin_user, redis_client):
    login_data = {'login': admin_user.login, 'password': 'test_password'}
    response = await api_session.post(f'http://{test_settings.service_url}/api/v1/auth/login', json=login_data)
    assert response.status_code == 201
    token = json.loads(response.content.decode())['refresh_token']
    api_session.headers['Authorization'] = f'Bearer {token}'
    yield api_session


@pytest_asyncio.fixture
async def user_authenticated_client(api_session, user, redis_client):
    login_data = {'login': user.login, 'password': 'test_password'}
    response = await api_session.post(f'http://{test_settings.service_url}/api/v1/auth/login', json=login_data)
    assert response.status_code == 201
    token = json.loads(response.content.decode())['refresh_token']
    api_session.headers['Authorization'] = f'Bearer {token}'
    yield api_session


# @pytest_asyncio.fixture
# async def authenticated_user(api_session):
#     async def inner(user):
#         login_data = {'login': user.login, 'password': 'test_password'}
#         response = await api_session.post(f'http://{test_settings.service_url}/api/v1/auth/login', json=login_data)
#         assert response.status_code == 201
#         token = json.loads(response.content.decode())['refresh_token']
#         api_session.headers['Authorization'] = f'Bearer {token}'
#         yield api_session
#
#     return inner




@pytest_asyncio.fixture
async def admin_user(db_session, roles):
    admin_role = roles['admin']
    admin_user = User(login='admin_username',
                      password='test_password',
                      first_name='test_first_name',
                      last_name='test_last_name',
                      role=admin_role,)
    db_session.add(admin_user)
    await db_session.commit()
    await db_session.refresh(admin_user)
    yield admin_user


@pytest_asyncio.fixture
async def user(db_session, roles):
    user_role = roles['user']
    admin_user = User(login='user_username',
                      password='test_password',
                      first_name='test_user_first_name',
                      last_name='test_user_last_name',
                      role=user_role,)
    db_session.add(admin_user)
    await db_session.commit()
    await db_session.refresh(admin_user)
    yield admin_user