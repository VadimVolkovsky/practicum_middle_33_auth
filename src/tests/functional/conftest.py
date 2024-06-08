import asyncio
import subprocess
from typing import Generator

import aiohttp
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from crud.user import user_crud
from db.postgres import Base, get_session
from main import app
from models.entity import User, Role, ROLES
from tests.settings import test_settings


@pytest_asyncio.fixture(scope='session')
async def db_session():
    engine = create_async_engine(test_settings.test_database_url, echo=True, future=True, poolclass=NullPool)
    async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session
        await session.rollback()

    await engine.dispose()



@pytest_asyncio.fixture
async def admin_authenticated_client(api_session, admin_user):
    login_data = {'login': admin_user.login, 'password': 'test_password'}
    response = subprocess.check_output(['curl', '-X', test_settings.service_url])
    response = await api_session.post(f'{test_settings.service_url}/auth/login', json=login_data, ssl=False)
    assert response.status_code == 200
    cookies = response.cookies
    api_session.cookies = cookies
    yield api_session


@pytest_asyncio.fixture(scope='session')
async def async_client():
    async with AsyncClient(app=app, base_url=test_settings.service_url) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
def event_loop() -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def api_session(event_loop):
    session = aiohttp.ClientSession(trust_env=True)
    yield session
    await session.close()

@pytest_asyncio.fixture
async def admin_user(db_session, roles):
    admin_role = roles['admin']
    admin_user = User(login='admin_username3',
                      password='test_password',
                      first_name='test_first_name',
                      last_name='test_last_name',
                      role=admin_role.id,)
    db_session.add(admin_user)
    await db_session.commit()
    await db_session.refresh(admin_user)
    yield admin_user


@pytest_asyncio.fixture
async def roles(db_session):
    roles = {role_name: Role(name=role_name) for role_name in ROLES}
    db_session.add_all(roles.values())
    await db_session.commit()
    yield roles