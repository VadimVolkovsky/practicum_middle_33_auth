import asyncio

import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from models import Base
from src.main import app
from tests import test_settings


# @pytest_asyncio.fixture(scope='session')
@pytest_asyncio.fixture
async def db_session():
    engine = create_async_engine(test_settings.database_url, future=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session
        await session.rollback()

    await engine.dispose()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def api_session():
    async with AsyncClient(app=app, base_url=test_settings.service_url) as client:
        yield client


# @pytest_asyncio.fixture(scope='session')
# async def api_session(event_loop):
#     session = aiohttp.ClientSession()
#     yield session
#     await session.close()
