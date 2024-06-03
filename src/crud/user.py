from sqlalchemy import select

from crud.base import CRUDBase
from models.entity import User


class CRUDUser(CRUDBase):
    """Круд класс для управления моделью User"""

    async def get_user_by_login(self, login, session) -> User | None:
        """Метод получения объекта пользователя из БД по логину"""
        user_obj = await session.execute(select(User).where(User.login == login))
        return user_obj.scalars().first()


user_crud = CRUDUser(User)