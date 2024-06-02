from sqlalchemy import select
from werkzeug.security import check_password_hash

from crud.base import CRUDBase
from models.entity import User


class CRUDUser(CRUDBase):
    """Круд класс для управления моделью User"""

    async def check_user_credentials(self, login, password, session):
        """Метод для проверки логина и пароля пользователя с данными в БД"""
        user_obj = await session.execute(select(User).where(User.login == login))
        user_obj = user_obj.scalars().first()
        if user_obj:
            if check_password_hash(user_obj.password, password):
                return True
        return False


user_crud = CRUDUser(User)