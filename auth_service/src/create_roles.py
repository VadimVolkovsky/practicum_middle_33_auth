import asyncio
import contextlib

from db.postgres import get_session
from models.entity import Roles, Role

# получение DI через контекстный менеджер
get_async_session_context = contextlib.asynccontextmanager(get_session)


async def add_default_roles():
    """Добавляет роли в БД при старте приложения"""
    async with get_async_session_context() as db_session:
        for role in Roles:
            role_obj = Role(name=role.value)
            db_session.add(role_obj)
            await db_session.commit()
            print(f'Добавлена роль {role.value}')


if __name__ == '__main__':
    asyncio.run(add_default_roles())
