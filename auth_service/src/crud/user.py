from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from models.entity import User


class CRUDUser(CRUDBase):
    """Класс для работы с моделью User в БД"""

    async def create_user(self, user: User, session: AsyncSession) -> User:
        """Создание нового пользователя"""
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


user_crud = CRUDUser(User)
