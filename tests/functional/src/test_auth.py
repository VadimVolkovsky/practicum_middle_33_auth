import pytest
from http import HTTPStatus


@pytest.mark.parametrize(
    'body, expected_answer',
    [
        ({
             "login": "user_login",
             "password": "123qwe",
             "first_name": "ivan",
             "last_name": "petrovich"
         }, {'status': HTTPStatus.CREATED}),
        ({
             "login": "user_login",
             "first_name": "ivan",
             "last_name": "petrovich"
         }, {'status': HTTPStatus.UNPROCESSABLE_ENTITY}),
    ]
)
@pytest.mark.asyncio
async def test_create_user(post_request, body, expected_answer):
    """Тест создание пользователя"""
    url = 'http://127.0.0.1:8000/api/v1/auth/signup'
    response = await post_request(url, data=body)
    status = response.status
    body = response.body
    if status == HTTPStatus.CREATED:
        assert body['login'] == expected_answer['login']
        assert body['first_name'] == expected_answer['first_name']
        assert body['last_name'] == expected_answer['last_name']


@pytest.mark.parametrize(
    'body, expected_answer',
    [
        ({
             "login": "user_login",
             "password": "123qwe"
         }, {'status': HTTPStatus.CREATED}),  # TODO поправить на OK 200
        ({
             "login": "fake_login",
             "password": "fake_pass"
         }, {'status': HTTPStatus.UNAUTHORIZED}),
    ]
)
@pytest.mark.asyncio
async def test_login_user(post_request, body, expected_answer):
    """Тест входа пользователя"""
    body_create_user = {
        "login": "user_login",
        "password": "123qwe",
        "first_name": "ivan",
        "last_name": "petrovich"
    }
    url_create = 'http://127.0.0.1:8000/api/v1/auth/signup'
    url_login = 'http://127.0.0.1:8000/api/v1/auth/login'
    await post_request(url_create, data=body_create_user)
    response = await post_request(url_login, data=body)
    status = response.status
    body = response.body
    if status == HTTPStatus.CREATED:
        assert 'access_token' in body
        assert 'refresh_token' in body
    if status == HTTPStatus.UNAUTHORIZED:
        assert body['detail'] == "Bad username or password"


@pytest.mark.asyncio
async def test_logout_user(post_request):
    """Тест выхода пользователя"""
    body_create_user = {
        "login": "user_login",
        "password": "123qwe",
        "first_name": "ivan",
        "last_name": "petrovich"
    }

    body_user_login = {
             "login": "user_login",
             "password": "123qwe"
         }
    url_create = 'http://127.0.0.1:8000/api/v1/auth/signup'
    url_login = 'http://127.0.0.1:8000/api/v1/auth/login'
    url_logout = 'http://127.0.0.1:8000/api/v1/auth/logout'
    await post_request(url_create, data=body_create_user)
    response = await post_request(url_login, data=body_user_login)

    refresh_token = response.body['refresh_token']
    headers = {'Authorization': f'Bearer {refresh_token}'}
    response = await post_request(url_logout, headers=headers)
    status = response.status
    body = response.body

    if status == HTTPStatus.OK:
        assert body['detail'] == "Logged out successfully"
