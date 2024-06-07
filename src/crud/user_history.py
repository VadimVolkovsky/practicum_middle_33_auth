from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.entity import UserLoginHistory, User


class CRUDUserLoginHistory(CRUDBase):
    """Класс для работы с моделью UserLoginHistory в БД"""

    async def get_user_login_history(self, user: User, session: AsyncSession, limit=5) -> UserLoginHistory:
        """
        Метод для получения истории входов пользователя.
        По умолчанию возвращается 5 последних входов
        """
        db_obj = await session.execute(
            select(self.model)
            .where(self.model.user == user.id)
            .order_by(self.model.login_date.desc())
            .limit(limit)
        )
        return db_obj.scalars().all()


user_login_history_crud = CRUDUserLoginHistory(UserLoginHistory)
