import json

import pytest_asyncio

from models.entity import User
from tests.settings import test_settings
from http import HTTPStatus


@pytest_asyncio.fixture
async def admin_authenticated_client(api_session, admin_user, redis_client):
    login_data = {'username': admin_user.username, 'password': 'test_password'}
    response = await api_session.post(f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/auth/login', json=login_data)
    assert response.status == HTTPStatus.OK
    token = json.loads(response.content.decode())['refresh_token']
    api_session.headers['Authorization'] = f'Bearer {token}'
    yield api_session


@pytest_asyncio.fixture
async def user_authenticated_client(api_session, user, redis_client):
    login_data = {'username': user.username, 'password': 'test_password'}
    response = await api_session.post(f'http://{test_settings.service_host}:{test_settings.service_port}/api/v1/auth/login', json=login_data)
    assert response.status == HTTPStatus.OK
    token = json.loads(response.content.decode())['refresh_token']
    api_session.headers['Authorization'] = f'Bearer {token}'
    yield api_session


@pytest_asyncio.fixture
async def admin_user(db_session, roles):
    admin_role = roles['admin']
    admin_user = User(username='admin_username',
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
    admin_user = User(username='user_username',
                      password='test_password',
                      first_name='test_user_first_name',
                      last_name='test_user_last_name',
                      role=user_role,)
    db_session.add(admin_user)


@pytest_asyncio.fixture(scope='session')
async def default_user(db_session, roles):
    """Возвращает объект пользователя из БД"""
    default_user = User(username='default_username',
                        password='test_password',
                        first_name='test_first_name',
                        last_name='test_last_name',
                        )
    db_session.add(default_user)
    await db_session.commit()
    await db_session.refresh(default_user)
    yield default_user


@pytest_asyncio.fixture(scope='session')
async def authenticated_user(default_user, post_request):
    """Возвращает access и refresh токены авторизованного пользователя"""
    login_data = {'username': default_user.username, 'password': 'test_password'}
    response = await post_request(f'http://127.0.0.1:8000/api/v1/auth/login', data=login_data)
    tokens = response.body
    yield tokens