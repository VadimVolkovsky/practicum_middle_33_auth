from functools import lru_cache

from fastapi import Depends
from fastapi.encoders import jsonable_encoder
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from werkzeug.security import check_password_hash

from core.schemas.entity import UserCreate
from crud.user import user_crud
from models.entity import User
from services.redis import get_redis


class UserService:
    """Класс для хранения бизнес-логики модели User"""
    def __init__(self, redis: Redis):
        self.redis = redis

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


@lru_cache()
def get_user_service(
        redis: Redis = Depends(get_redis)
) -> UserService:
    """
    Провайдер UserService
    Используем lru_cache-декоратор, чтобы создать объект сервиса в едином экземпляре (синглтона)
    """
    return UserService(redis)
