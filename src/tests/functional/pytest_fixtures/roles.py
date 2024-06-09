import pytest_asyncio

from models.entity import Role, ROLES


@pytest_asyncio.fixture
async def roles(db_session):
    roles = {role_name: Role(name=role_name) for role_name in ROLES}
    db_session.add_all(roles.values())
    await db_session.commit()
    yield roles