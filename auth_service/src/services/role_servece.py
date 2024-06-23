from functools import lru_cache
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUDBase
from models.entity import Role, User, Roles


class RoleService(CRUDBase):
    async def get_by_name(self, name: str, session: AsyncSession) -> Role:
        role = await self.get_by_attribute('name', name, session)

        if not role:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=f"Role '{name}' not found")

        return role

    async def assign_role(self, role: Role, user: User, session: AsyncSession) -> User:
        user.role = role
        await session.commit()
        await session.refresh(user)

        return user

    async def get_default_role(self, session: AsyncSession) -> Role:
        default_role = Roles.user.value

        if not (default_role := await self.get_by_name(default_role, session)):
            default_role = await self.create(default_role, session)

        return default_role

    # async def get(self, session: AsyncSession, role_id: UUID) -> Role | None:
    #     return (await session.scalars(select(Role).where(Role.id == role_id))).first()  # noqa

    # async def get_by_name(self, session: AsyncSession, role_name: str) -> Role | None:
    #     return (await session.scalars(select(Role).where(Role.name == role_name))).first()  # noqa
    #
    # async def create(self, session: AsyncSession, role_data: dict) -> Role:
    #     new_role = Role(**role_data)
    #     session.add(new_role)
    #     await session.commit()
    #
    #     return new_role
    #
    # async def update(self, session: AsyncSession, role: Role, update_data: dict) -> Role:
    #     for key, value in update_data.items():
    #         setattr(role, key, value)
    #     await session.commit()
    #     await session.refresh(role)
    #
    #     return role
    #
    # async def delete(self, session: AsyncSession, role: Role) -> Role:
    #     await session.delete(role)
    #     await session.commit()
    #     return role
    #
    # async def elements(self, session: AsyncSession):
    #     return (await session.scalars(select(Role))).all()
    #
    # async def assign_role(self, session: AsyncSession, role: Role, user: User) -> User:
    #     user.role = role
    #     await session.commit()
    #     await session.refresh(user)
    #
    #     return user
    #
    # async def get_default_role(self, session: AsyncSession) -> Role:
    #     if not (default_role := await self.get_by_name(session, DEFAULT_ROLE_DATA['name'])):
    #         default_role = await self.create(session, DEFAULT_ROLE_DATA)
    #
    #     return default_role


@lru_cache
def get_role_service() -> RoleService:
    return RoleService(Role)
