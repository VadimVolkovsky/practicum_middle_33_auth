from async_fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash

from core.schemas.entity import UserCreate, UserLogin
from crud.user import user_crud
from models.entity import User


class UserService:
    """Класс для хранения бизнес-логики модели User"""

    async def create_user(self, user_create: UserCreate, session: AsyncSession):
        user_dto = jsonable_encoder(user_create)
        user = User(**user_dto)
        return await user_crud.create_user(user, session)

    async def check_user_credentials(self, login, password, session) -> bool:
        """Метод для проверки логина и пароля пользователя с данными в БД"""
        user_obj = await user_crud.get_user_by_login(login, session)
        if user_obj:
            if check_password_hash(user_obj.password, password):
                return True
        return False

    async def create_access_token(self, user: UserLogin, authorize: AuthJWT):
        return await authorize.create_access_token(subject=user.login)

    async def create_refresh_token(self, user: UserLogin, authorize: AuthJWT):
        return await authorize.create_refresh_token(subject=user.login)

    async def generate_new_jwt_tokens(self, user: UserLogin, authorize: AuthJWT):
        access_token = await self.create_access_token(user, authorize)
        refresh_token = await self.create_refresh_token(user, authorize)
        return {"access_token": access_token, "refresh_token": refresh_token}


user_service = UserService()
