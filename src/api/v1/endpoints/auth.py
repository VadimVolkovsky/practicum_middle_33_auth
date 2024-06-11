from http import HTTPStatus

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.auth_jwt import AuthJWTBearer
from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import Page, paginate
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import AppSettings, app_settings
from core.schemas.entity import UserInDB, UserCreate, UserLogin, JWTResponse, UserUpdate, UserLoginHistoryInDB
from db.postgres import get_session
from services import redis
from services.user_service import get_user_service, UserService

router = APIRouter()
auth_dep = AuthJWTBearer()


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


@router.post('/login', response_model=JWTResponse, status_code=HTTPStatus.OK)
async def login(
        user: UserLogin,
        user_service: UserService = Depends(get_user_service),
        authorize: AuthJWT = Depends(auth_dep),
        session: AsyncSession = Depends(get_session)
):
    """
    Эндпоинт авторизации пользователя по логину и паролю.
    В случае усешной авторизации создаются access и refresh токены
    """
    if not await user_service.check_user_credentials(user.email, user.password, session):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Bad email or password")
    access_token = await authorize.create_access_token(subject=user.email)
    raw_jwt = await authorize.get_raw_jwt(encoded_token=access_token)
    access_token_jti = raw_jwt['jti']

    refresh_token = await authorize.create_refresh_token(
        subject=user.email,
        user_claims={'access_token_jti': access_token_jti}
    )
    await user_service.add_user_login_history(user.email, session)
    return JWTResponse(access_token=access_token, refresh_token=refresh_token)


@router.delete('/logout', status_code=HTTPStatus.OK)
async def logout(
        user_service: UserService = Depends(get_user_service),
        authorize: AuthJWT = Depends(auth_dep),
):
    """Эндпоинт разлогинивания пользователя путем добавления его refresh токена в блэк-лист Redis"""
    await authorize.jwt_refresh_token_required()
    raw_jwt = await authorize.get_raw_jwt()
    refresh_token_jti = raw_jwt['jti']
    access_token_jti = raw_jwt['access_token_jti']
    await user_service.redis.setex(refresh_token_jti, app_settings.refresh_expires, 'true')
    await user_service.redis.setex(access_token_jti, app_settings.access_expires, 'true')
    return {"detail": "Logged out successfully"}


@router.post('/refresh')
async def refresh(authorize: AuthJWT = Depends(auth_dep)):
    """
    Эндпоинт получения нового access токена по refresh токену.
    В случае если refresh токен в блэк-листе Redis, новый access токен не выдается
    """
    await authorize.jwt_refresh_token_required()
    current_user = await authorize.get_jwt_subject()
    new_access_token = await authorize.create_access_token(subject=current_user)
    return {"access_token": new_access_token}


@router.post('/user_update', status_code=HTTPStatus.OK)
async def change_user_data(
        user_input_data: UserUpdate,
        authorize: AuthJWT = Depends(auth_dep),
        user_service: UserService = Depends(get_user_service),
        session: AsyncSession = Depends(get_session)
):
    """Эндпоинт для обновления данных пользователя"""
    await authorize.jwt_required()

    # Обновляем данные пользователя в БД
    raw_jwt = await authorize.get_raw_jwt()
    email = raw_jwt['sub']
    await user_service.update_user_info(user_input_data, email, session)
    jti = raw_jwt['jti']
    await user_service.redis.setex(jti, app_settings.refresh_expires, 'true')
    return {"detail": "Data were updated successfully"}


@router.get('/user_login_history', response_model=Page[UserLoginHistoryInDB], status_code=HTTPStatus.OK)
async def get_user_login_history(
        authorize: AuthJWT = Depends(auth_dep),
        user_service: UserService = Depends(get_user_service),
        session: AsyncSession = Depends(get_session)
):
    """Эндпоинт для получения информации об истории входов пользователя"""
    await authorize.jwt_required()
    email = await authorize.get_jwt_subject()
    user = await user_service.get_user_by_email(email, session)
    user_login_history = await user_service.get_user_login_history(user, session)
    return paginate(user_login_history)

