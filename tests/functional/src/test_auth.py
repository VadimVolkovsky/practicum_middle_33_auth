import pytest
from http import HTTPStatus


@pytest.mark.parametrize(
    'body, expected_answer',
    [
        ({
             "login": "default_username_2",
             "password": "test_password",
             "first_name": "ivan",
             "last_name": "petrovich"
         }, {'status': HTTPStatus.CREATED}),
        ({
             "login": "default_username_2",
             "first_name": "ivan",
             "last_name": "petrovich"
         }, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
    ]
)
@pytest.mark.asyncio
async def test_create_user(db_session, roles, post_request, body, expected_answer):
    """Тест создание пользователя"""
    url = 'http://127.0.0.1:8000/api/v1/auth/signup'
    response = await post_request(url, data=body)
    status = response.status
    response_body = response.body
    if status == HTTPStatus.CREATED:
        assert 'id' in response_body
        assert body['first_name'] == response_body['first_name']
        assert body['last_name'] == response_body['last_name']


@pytest.mark.parametrize(
    'body, expected_answer',
    [
        ({
             "login": "default_username",
             "password": "test_password"
         }, {'status': HTTPStatus.OK}),
        ({
             "login": "fake_login",
             "password": "fake_pass"
         }, {'status': HTTPStatus.UNAUTHORIZED}),
    ]
)
@pytest.mark.asyncio
async def test_login_user(default_user, post_request, body, expected_answer):
    """Тест входа пользователя"""
    url_login = 'http://127.0.0.1:8000/api/v1/auth/login'
    response = await post_request(url_login, data=body)
    status = response.status
    body = response.body
    if status == HTTPStatus.CREATED:
        assert 'access_token' in body
        assert 'refresh_token' in body
    if status == HTTPStatus.UNAUTHORIZED:
        assert body['detail'] == "Bad username or password"


@pytest.mark.asyncio
async def test_logout_user(authenticated_user, post_request):
    """Тест выхода пользователя"""
    url_logout = 'http://127.0.0.1:8000/api/v1/auth/logout'
    headers = {'Authorization': f'Bearer {authenticated_user['refresh_token']}'}
    response = await post_request(url_logout, headers=headers)
    status = response.status
    body = response.body

    if status == HTTPStatus.OK:
        assert body['detail'] == "Logged out successfully"


@pytest.mark.asyncio
async def test_token_refresh(authenticated_user, post_request):
    """Тест обновления токена access"""
    url_token_refresh = 'http://127.0.0.1:8000/api/v1/auth/refresh'
    headers = {'Authorization': f'Bearer {authenticated_user['refresh_token']}'}
    response = await post_request(url_token_refresh, headers=headers)
    status = response.status
    body = response.body
    if status == HTTPStatus.OK:
        assert 'access_token' in body


@pytest.mark.asyncio
async def test_change_user_data(authenticated_user, post_request):
    """Тест обновления данных пользователя"""
    url_user_update = 'http://127.0.0.1:8000/api/v1/auth/user_update'
    headers = {'Authorization': f'Bearer {authenticated_user['refresh_token']}'}
    body = {"login": "new_username"}

    response = await post_request(url_user_update, data=body, headers=headers)
    status = response.status
    body = response.body
    if status == HTTPStatus.OK:
        assert body['detail'] == "Data were updated successfully"


@pytest.mark.asyncio
async def test_get_user_login_history(authenticated_user, get_request):
    """Тесты получения информации об истории входов пользователя"""
    url_user_login_history = 'http://127.0.0.1:8000/api/v1/auth/user_login_history'
    headers = {'Authorization': f'Bearer {authenticated_user['access_token']}'}
    response = await get_request(url_user_login_history, headers=headers)
    status = response.status
    body = response.body
    if status == HTTPStatus.OK:
        assert 'login_date' in body
