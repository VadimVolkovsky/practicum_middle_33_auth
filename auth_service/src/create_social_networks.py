import asyncio
import contextlib

from db.postgres import get_session
from models.entity import SocialNetworksEnum, SocialNetwork

# получение DI через контекстный менеджер
get_async_session_context = contextlib.asynccontextmanager(get_session)


async def add_default_social_networks():
    """Добавляет социальные сети в БД"""
    async with get_async_session_context() as db_session:
        for social_network in SocialNetworksEnum:
            social_network_obj = SocialNetwork(name=social_network.value)
            db_session.add(social_network_obj)
            await db_session.commit()
            print(f'Добавлена социальная сеть {social_network.value}')


if __name__ == '__main__':
    asyncio.run(add_default_social_networks())
