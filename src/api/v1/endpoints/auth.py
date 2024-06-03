from http import HTTPStatus

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import AppSettings
from core.schemas.entity import UserInDB, UserCreate, UserLogin, JWTResponse
from db.postgres import get_session
from services.user import user_service

router = APIRouter()


@router.post('/signup', response_model=UserInDB, status_code=HTTPStatus.CREATED)
async def create_user(user_create: UserCreate, session: AsyncSession = Depends(get_session)) -> UserInDB:
    return await user_service.create_user(user_create, session)


@AuthJWT.load_config
def get_config():
    return AppSettings()


@router.post('/login', response_model=JWTResponse, status_code=HTTPStatus.CREATED)
async def login(user: UserLogin, authorize: AuthJWT = Depends(), session: AsyncSession = Depends(get_session)):
    """
    Эндпоинт авторизации пользователя по логину и паролю.
    В случае усешной авторизации создаются access и refresh токены
    """
    if not await user_service.check_user_credentials(user.login, user.password, session):
        raise HTTPException(status_code=401,detail="Bad username or password")

    access_token = await authorize.create_access_token(subject=user.login)
    refresh_token = await authorize.create_refresh_token(subject=user.login)
    return {"access_token": access_token, "refresh_token": refresh_token}



# TODO допилить реализацию
# protect endpoint with function jwt_required(), which requires
# a valid access token in the request headers to access.
# @router.get('/user')
# def user(authorize: AuthJWT = Depends()):
#     authorize.jwt_required()
#     current_user = authorize.get_jwt_subject()
#     return {"user": current_user}
#
#
# @router.post('/refresh')
# def refresh(authorize: AuthJWT = Depends()):
#     """
#     The jwt_refresh_token_required() function insures a valid refresh
#     token is present in the request before running any code below that function.
#     we can use the get_jwt_subject() function to get the subject of the refresh
#     token, and use the create_access_token() function again to make a new access token
#     """
#     authorize.jwt_refresh_token_required()
#
#     current_user = authorize.get_jwt_subject()
#     new_access_token = authorize.create_access_token(subject=current_user)
#     return {"access_token": new_access_token}