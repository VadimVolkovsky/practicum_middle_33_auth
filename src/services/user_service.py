from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import generate_password_hash

from core.schemas.entity import UserCreate, UserUpdate, UserLoginHistory, UserLoginHistoryInDB, UserInDB
from crud.user import user_crud
from crud.user_history import user_login_history_crud
from models.entity import User
from services.redis import get_redis


class UserService:
    """Класс для хранения бизнес-логики модели User"""

    def __init__(self, redis: Redis):
        self.redis = redis

    async def create_user(self, user_create: UserCreate, session: AsyncSession) -> UserInDB:
        """Метод для регистрации нового пользователя"""
        user_dto = jsonable_encoder(user_create)
        user = User(**user_dto)
        user_obj = await user_crud.get_by_attribute('email', user.email, session)
        if user_obj:
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                                detail=f"email '{user.email}' is already in use")
        return await user_crud.create_user(user, session)

    async def get_user_by_email(self, email: str, session: AsyncSession) -> User:
        user = await user_crud.get_by_attribute('email', email, session)
        if not user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"User with email '{email}' not found")
        return user

    async def check_user_credentials(self, email, password, session) -> bool:
        """Метод для проверки логина и пароля пользователя с данными в БД"""
        user_obj = await user_crud.get_by_attribute('email', email, session)
        if user_obj:
            if user_obj.check_password(password):
                return True
        return False

    async def update_user_info(
            self,
            user_input_data: UserUpdate,
            email: str,
            session: AsyncSession
    ) -> User:
        """Метод для обновления данных пользователя"""
        db_user = await user_crud.get_by_attribute('email', email, session)
        if not db_user:
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                                detail=f"User with email '{email}' does not exist")
        if user_input_data.password:
            user_input_data.password = generate_password_hash(user_input_data.password)
        db_user_updated = await user_crud.update(db_user, user_input_data, session)
        return db_user_updated

    async def add_user_login_history(
            self,
            email: str,
            session: AsyncSession
    ) -> None:
        """Метод для сохранения истории входов пользователя"""
        user_data = await user_crud.get_by_attribute('email', email, session)
        obj_in = UserLoginHistory(user_id=user_data.id)
        await user_login_history_crud.create(obj_in, session)

    async def get_user_login_history(self, user: User, session: AsyncSession) -> list[UserLoginHistoryInDB]:
        """
        Метод для получения истории входов пользователя.
        """
        user_login_history = await user_login_history_crud.get_user_login_history(user, session)
        return user_login_history


@lru_cache()
def get_user_service(
        redis: Redis = Depends(get_redis)
) -> UserService:
    """
    Провайдер UserService
    Используем lru_cache-декоратор, чтобы создать объект сервиса в едином экземпляре (синглтона)
    """
    return UserService(redis)
