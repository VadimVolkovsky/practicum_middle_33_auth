from functools import lru_cache
from http import HTTPStatus

from fastapi import Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash, generate_password_hash

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
        user_obj = await user_crud.get_by_attribute('login', user.login, session)
        if user_obj:
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                                detail=f"Login '{user.login}' is already in use")
        return await user_crud.create_user(user, session)

    async def get_user_by_login(self, login: str, session: AsyncSession) -> User:
        user = await user_crud.get_by_attribute('login', login, session)
        if not user:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"User '{login}' not found")
        return user

    async def check_user_credentials(self, login, password, session) -> bool:
        """Метод для проверки логина и пароля пользователя с данными в БД"""
        user_obj = await user_crud.get_by_attribute('login', login, session)
        if user_obj:
            if check_password_hash(user_obj.password, password):
                return True
        return False

    async def update_user_info(
            self,
            user_input_data: UserUpdate,
            user_login: str,
            session: AsyncSession
    ) -> User:
        """Метод для обновления данных пользователя"""
        db_user = await user_crud.get_by_attribute('login', user_login, session)
        if not db_user:
            raise HTTPException(status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
                                detail=f"User with login '{user_login}' does not exist")
        if user_input_data.password:
            user_input_data.password = generate_password_hash(user_input_data.password)
        db_user_updated = await user_crud.update(db_user, user_input_data, session)
        return db_user_updated

    async def add_user_login_history(
            self,
            user_login: str,
            session: AsyncSession
    ) -> None:
        """Метод для сохранения истории входов пользователя"""
        user_data = await user_crud.get_by_attribute('login', user_login, session)
        obj_in = UserLoginHistory(user=user_data.id)
        await user_login_history_crud.create(obj_in, session)

    async def get_user_login_history(self, user: User, session: AsyncSession) -> UserLoginHistoryInDB:
        """
        Метод для получения истории входов пользователя.
        """
        db_data = await user_login_history_crud.get_user_login_history(user, session)
        login_date = [db_obj.login_date for db_obj in db_data]
        user_login_history = UserLoginHistoryInDB(login_date=login_date)
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
