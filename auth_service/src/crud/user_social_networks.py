from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.entity import UserSocialNetworks
from .base import CRUDBase


class CRUDUserSocialNetworks(CRUDBase):
    """Класс для работы с моделью UserSocialNetworks в БД"""
    pass

    async def get_user_social_networks(
            self,
            user_id: int,
            session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model)
            .where(self.model.user_id == user_id)
        )
        return db_obj.scalars().all()


user_social_networks_crud = CRUDUserSocialNetworks(UserSocialNetworks)
