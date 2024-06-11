from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from core.config import app_settings
from models import Base

dsn = (f'postgresql+asyncpg://{app_settings.postgres_user}:{app_settings.postgres_password}@'
       f'{app_settings.postgres_host}:{app_settings.postgres_port}/{app_settings.postgres_db}')
engine = create_async_engine(dsn, echo=app_settings.echo, future=True)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def purge_database() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
