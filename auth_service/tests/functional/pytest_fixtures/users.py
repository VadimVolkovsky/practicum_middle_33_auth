import json

import pytest_asyncio

from models.entity import User
from tests import test_settings
from http import HTTPStatus


@pytest_asyncio.fixture
async def admin_authenticated_client(api_session, admin_user, redis_client):
    """Сессия авторизованного админа"""
    login_data = {'email': admin_user.email, 'password': 'test_password'}
    response = await api_session.post(f'http://{test_settings.service_host}:{test_settings.service_port}'
                                      f'/api/v1/auth/login', json=login_data)
    assert response.status_code == HTTPStatus.OK
    access_token = json.loads(response.content.decode())['access_token']
    # refresh_token = json.loads(response.content.decode())['refresh_token']
    # api_session.cookies['access_token'] = access_token
    # api_session.cookies['refresh_token'] = refresh_token
    api_session.headers['Authorization'] = f'Bearer {access_token}'
    yield api_session


@pytest_asyncio.fixture
async def user_authenticated_client(api_session, default_user, redis_client):
    """Сессия авторизованного пользователя"""
    login_data = {'email': default_user.email, 'password': 'test_password'}
    response = await api_session.post(f'http://{test_settings.service_host}:{test_settings.service_port}'
                                      f'/api/v1/auth/login', json=login_data)
    assert response.status_code == HTTPStatus.OK
    access_token = json.loads(response.content.decode())['access_token']
    refresh_token = json.loads(response.content.decode())['refresh_token']
    api_session.cookies['refresh_token'] = refresh_token  # сохраняем рефреш токен в куки для эндпоинта /refresh
    api_session.headers['Authorization'] = f'Bearer {access_token}'
    yield api_session


@pytest_asyncio.fixture
async def user_anonymous_client(api_session, default_user, redis_client):
    """Сессия анонимного пользователя"""
    yield api_session


@pytest_asyncio.fixture
async def admin_user(db_session, roles):
    admin_role = roles['admin']
    admin_user = User(email='admin@mail.ru',
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
    admin_user = User(email='default@mail.ru',
                      password='test_password',
                      first_name='test_user_first_name',
                      last_name='test_user_last_name',
                      role=user_role,)
    db_session.add(admin_user)


@pytest_asyncio.fixture
async def default_user(db_session, roles):
    """Возвращает объект пользователя из БД"""
    default_user = User(email='default@mail.ru',
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
    login_data = {'email': default_user.email, 'password': 'test_password'}
    response = await post_request('http://127.0.0.1:8000/api/v1/auth/login', data=login_data)
    tokens = response.body
    yield tokens
