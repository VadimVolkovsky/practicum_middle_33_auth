import asyncio

import aiohttp
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from db.postgres import Base
from main import app
from models.entity import User, Role, ROLES
from tests.settings import test_settings


@pytest_asyncio.fixture
async def test_db_session():
    engine = create_async_engine(test_settings.test_database_url, echo=True, future=True)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session
        await session.rollback()

    await engine.dispose()


@pytest_asyncio.fixture
async def superuser_authenticated_client(async_client, admin_user):
    login_data = {"login": admin_user.login, "password": "testpassword"}
    response = await async_client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    cookies = response.cookies
    async_client.cookies = cookies
    yield async_client


@pytest_asyncio.fixture(scope='session')
async def async_client(event_loop):
    async with AsyncClient(app=app, base_url=test_settings.service_url) as client:
        yield client


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def api_session(event_loop):
    session = aiohttp.ClientSession()
    yield session
    await session.close()

@pytest_asyncio.fixture
async def admin_user(test_db_session, roles):
    admin_role = roles['admin']
    superuser = User(login="admin_username", password="testpassword", role=admin_role)
    test_db_session.add(superuser)
    await test_db_session.commit()
    await test_db_session.refresh(superuser)
    yield superuser


@pytest_asyncio.fixture
async def roles(test_db_session):
    roles = {role_name: Role(name=role_name) for role_name in ROLES}
    # {"user": Role(**DEFAULT_ROLE_DATA),
    #     "admin": Role(**SUPERUSER_ROLE_DATA),
    #     "testrole": Role(name="testrole", access_level=1)
    # }
    test_db_session.add_all(roles.values())
    await test_db_session.commit()
    yield roles