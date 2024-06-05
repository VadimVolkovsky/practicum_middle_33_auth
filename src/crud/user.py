from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.entity import User


class CRUDUser(CRUDBase):
    """Класс для работы с моделью User в БД"""

    async def create_user(self, user: User, session: AsyncSession) -> User:
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def get_user_by_login(self, login, session) -> User | None:
        """Метод получения объекта пользователя из БД по логину"""
        user_obj = await session.execute(select(User).where(User.login == login))
        return user_obj.scalars().first()


user_crud = CRUDUser(User)