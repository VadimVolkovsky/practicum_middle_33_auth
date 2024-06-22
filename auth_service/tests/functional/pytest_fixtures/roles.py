import pytest_asyncio

from models.entity import Role, Roles


@pytest_asyncio.fixture
async def roles(db_session):
    roles = {role.value: Role(name=role.value) for role in Roles}
    db_session.add_all(roles.values())
    await db_session.commit()
    yield roles
