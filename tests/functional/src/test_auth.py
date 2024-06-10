import pytest
from http import HTTPStatus


@pytest.mark.parametrize(
    'body, expected_answer',
    [
        ({
             "username": "default_username_2",
             "password": "test_password",
             "first_name": "ivan",
             "last_name": "petrovich"
         }, {'status': HTTPStatus.CREATED}),
        ({
             "username": "default_username_2",
             "first_name": "ivan",
             "last_name": "petrovich"
         }, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
    ]
)
@pytest.mark.asyncio
async def test_create_user(db_session, roles, user_anonymous_client, body, expected_answer):
    """Тест создание пользователя"""
    url = 'http://127.0.0.1:8000/api/v1/auth/signup'
    response = await user_anonymous_client.post(url, json=body)
    status = response.status_code
    response_body = response.json()
    if status == HTTPStatus.CREATED:
        assert 'id' in response_body
        assert body['first_name'] == response_body['first_name']
        assert body['last_name'] == response_body['last_name']
    if status == HTTPStatus.UNPROCESSABLE_ENTITY:
        assert 'detail' in response_body


@pytest.mark.parametrize(
    'body, expected_answer',
    [
        ({
             "username": "default_username",
             "password": "test_password"
         }, {'status': HTTPStatus.OK}),
        ({
             "username": "fake_login",
             "password": "fake_pass"
         }, {'status': HTTPStatus.UNAUTHORIZED}),
    ]
)
@pytest.mark.asyncio
async def test_login_user(default_user, user_anonymous_client, body, expected_answer):
    """Тест входа пользователя"""
    url = 'http://127.0.0.1:8000/api/v1/auth/login'
    response = await user_anonymous_client.post(url, json=body)
    status = response.status_code
    response_body = response.json()
    if status == HTTPStatus.OK:
        assert 'access_token' in response_body
        assert 'refresh_token' in response_body
    if status == HTTPStatus.UNAUTHORIZED:
        assert response_body['detail'] == "Bad username or password"


# TODO пофиксить токен на акссес
@pytest.mark.asyncio
async def test_logout_user(user_authenticated_client):
    """Тест выхода пользователя"""
    url = 'http://127.0.0.1:8000/api/v1/auth/logout'
    response = await user_authenticated_client.delete(url)
    status = response.status_code
    response_body = response.json()

    assert status == HTTPStatus.OK
    assert response_body['detail'] == "Logged out successfully"


@pytest.mark.asyncio
async def test_token_refresh(user_authenticated_client):
    """Тест обновления токена access"""
    url = 'http://127.0.0.1:8000/api/v1/auth/refresh'
    response = await user_authenticated_client.post(url)
    status = response.status_code
    response_body = response.json()

    assert status == HTTPStatus.OK
    assert 'access_token' in response_body



# TODO пофиксить токен на акссес
@pytest.mark.asyncio
async def test_change_user_data(user_authenticated_client):
    """Тест обновления данных пользователя"""
    url = 'http://127.0.0.1:8000/api/v1/auth/user_update'
    body = {"username": "new_username"}

    response = await user_authenticated_client.post(url, json=body)
    status = response.status_code
    response_body = response.json()

    assert status == HTTPStatus.OK
    assert response_body['detail'] == "Data were updated successfully"


# TODO пофиксить токен на акссес
@pytest.mark.asyncio
async def test_get_user_login_history(user_authenticated_client):
    """Тесты получения информации об истории входов пользователя"""
    url = 'http://127.0.0.1:8000/api/v1/auth/user_login_history'

    response = await user_authenticated_client.get(url)
    status = response.status_code
    response_body = response.json()

    assert status == HTTPStatus.OK
    assert 'login_date' in response_body


