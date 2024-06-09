from http import HTTPStatus

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import AppSettings, app_settings
from core.schemas.entity import UserInDB, UserCreate, UserLogin, JWTResponse, UserUpdate, UserLoginHistoryInDB
from db.postgres import get_session
from services import redis
from services.user_service import get_user_service, UserService

router = APIRouter()


@AuthJWT.load_config
def get_config():
    return AppSettings()


@AuthJWT.token_in_denylist_loader
async def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    entry = await redis.redis.get(jti)
    if entry:
        entry = entry.decode()
    return entry and entry == 'true'


@router.post('/signup', response_model=UserInDB, status_code=HTTPStatus.CREATED)
async def create_user(
        user_create: UserCreate,
        user_service: UserService = Depends(get_user_service),
        session: AsyncSession = Depends(get_session)
) -> UserInDB:
    """Эндпоинт создания нового пользователя"""
    return await user_service.create_user(user_create, session)


@router.post('/login', response_model=JWTResponse, status_code=HTTPStatus.CREATED)
async def login(
        user: UserLogin,
        user_service: UserService = Depends(get_user_service),
        authorize: AuthJWT = Depends(),
        session: AsyncSession = Depends(get_session)
):
    """
    Эндпоинт авторизации пользователя по логину и паролю.
    В случае усешной авторизации создаются access и refresh токены
    """
    if not await user_service.check_user_credentials(user.login, user.password, session):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Bad username or password")
    access_token = await authorize.create_access_token(subject=user.login)
    refresh_token = await authorize.create_refresh_token(subject=user.login)
    await user_service.add_user_login_history(user.login, session)
    return JWTResponse(access_token=access_token, refresh_token=refresh_token)


@router.post('/logout', status_code=HTTPStatus.OK)
async def logout(  # TODO нужно ли обнулять все токены юзера со всех устройств ?
        user_service: UserService = Depends(get_user_service),
        authorize: AuthJWT = Depends(),
):
    """Эндпоинт разлогинивания пользователя путем добавления его refresh токена в блэк-лист Redis"""
    await authorize.jwt_refresh_token_required()
    raw_jwt = await authorize.get_raw_jwt()
    jti = raw_jwt['jti']
    await user_service.redis.setex(jti, app_settings.refresh_expires, 'true')
    return {"detail": "Logged out successfully"}


@router.post('/refresh')
async def refresh(authorize: AuthJWT = Depends()):
    """
    Эндпоинт получения нового access токена по refresh токену.
    В случае если refresh токен в блэк-листе Redis, новый access токен не выдается
    """
    await authorize.jwt_refresh_token_required()
    current_user = await authorize.get_jwt_subject()
    new_access_token = await authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.delete('/access-revoke')
async def access_revoke(
        authorize: AuthJWT = Depends(),
        user_service: UserService = Depends(get_user_service)):
    """
    Эндпоинт деактивации access токена путем добавления его в блэк-лист Redis.
    По истечении срока действия токена, он автоматически удаляется из Redis
    """
    await authorize.jwt_required()
    raw_jwt = await authorize.get_raw_jwt()
    jti = raw_jwt['jti']
    await user_service.redis.setex(jti, app_settings.access_expires, 'true')
    return {"detail": "Access token has been revoke"}


@router.delete('/refresh-revoke')
async def refresh_revoke(
        authorize: AuthJWT = Depends(),
        user_service: UserService = Depends(get_user_service)):
    """
    Эндпоинт деактивации refresh токена путем добавления его в блек-лист Redis.
    По истечении срока действия токена, он автоматически удаляется из Redis
    """
    await authorize.jwt_refresh_token_required()
    raw_jwt = await authorize.get_raw_jwt()
    jti = raw_jwt['jti']
    await user_service.redis.setex(jti, app_settings.refresh_expires, 'true')
    return {"detail": "Refresh token has been revoke"}


@router.post('/user_update', status_code=HTTPStatus.OK)
async def change_user_data(
        user_input_data: UserUpdate,
        authorize: AuthJWT = Depends(),
        user_service: UserService = Depends(get_user_service),
        session: AsyncSession = Depends(get_session)
):
    """Эндпоинт для обновления данных пользователя"""
    await authorize.jwt_refresh_token_required()

    # Обновляем данные пользователя в БД
    raw_jwt = await authorize.get_raw_jwt()
    user_login = raw_jwt['sub']
    await user_service.update_user_info(user_input_data, user_login, session)

    """Деактивируем рефреш токен чобы пользователь заново залогинился
    (сейчас можно изменять только ключевые поля - логин или пароль)"""
    jti = raw_jwt['jti']
    await user_service.redis.setex(jti, app_settings.refresh_expires, 'true')

    return {"detail": "Data were updated successfully"}


@router.get('/user_login_history', response_model=UserLoginHistoryInDB, status_code=HTTPStatus.OK)
async def get_user_login_history(
        authorize: AuthJWT = Depends(),
        user_service: UserService = Depends(get_user_service),
        session: AsyncSession = Depends(get_session)
):
    await authorize.jwt_required()
    user_login = await authorize.get_jwt_subject()
    user = await user_service.get_user_by_login(user_login, session)
    return await user_service.get_user_login_history(user, session)
