import pytest_asyncio

from models.entity import User


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