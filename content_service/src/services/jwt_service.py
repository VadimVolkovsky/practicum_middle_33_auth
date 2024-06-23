import http

import aiohttp
from fastapi import HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.config import app_settings


async def check_token_in_auth_service(credentials: HTTPAuthorizationCredentials) -> dict:
    """
    Запрашиваем у сервиса авторизации актуальность переданного токена.
    В случае успеха - возвращаем данные о пользователе
    В случае неудачи - возвращаем экспешн с описанием ошибки
    # TODO добавить изящную деградацию на случай недоступности сервиса авторизации
    """
    url = app_settings.auth_check_token_url
    token_scheme = credentials.scheme
    token = credentials.credentials
    headers = {'Authorization': f'{token_scheme} {token}'}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers) as response:
            response_body = await response.json()
            if not response.ok:
                raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail=response_body.get('detail'))
            return response_body


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> dict:
        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if not credentials:
            raise HTTPException(status_code=http.HTTPStatus.FORBIDDEN, detail='Invalid authorization code.')
        if not credentials.scheme == 'Bearer':
            raise HTTPException(status_code=http.HTTPStatus.UNAUTHORIZED, detail='Only Bearer token might be accepted')

        response_body = await check_token_in_auth_service(credentials)
        return response_body


security_jwt = JWTBearer()
