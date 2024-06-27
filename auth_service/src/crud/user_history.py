from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from models.entity import UserLoginHistory, User


class CRUDUserLoginHistory(CRUDBase):
    """Класс для работы с моделью UserLoginHistory в БД"""

    async def get_user_login_history(self, user: User, session: AsyncSession) -> UserLoginHistory:
        """
        Метод для получения истории входов пользователя.
        """
        db_obj = await session.execute(
            select(self.model)
            .where(self.model.user_id == user.id)
            .order_by(self.model.login_date.desc())
        )
        return db_obj.scalars().all()


user_login_history_crud = CRUDUserLoginHistory(UserLoginHistory)
