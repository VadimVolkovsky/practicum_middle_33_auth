from http import HTTPStatus

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.serializers.role_serializer import RoleSerializer, RoleCreateSerializer, AssignRoleSerializer
from db.postgres import get_session
from models.entity import User
from services.role_servece import RoleService, get_role_service
from services.user_service import UserService, get_user_service

router = APIRouter()


@router.get('', response_model=list[RoleSerializer], status_code=HTTPStatus.OK)
async def get_roles(
        authorize: AuthJWT = Depends(),
        role_service: RoleService = Depends(get_role_service),
        session: AsyncSession = Depends(get_session)):

    # await authorize.jwt_refresh_token_required()
    user_username = await authorize.get_jwt_subject()
    db_user = await session.execute(select(User).where(User.email == user_username))
    user = db_user.scalars().first()

    if user.role.name != 'admin':
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='You have no permission to create role')

    return await role_service.get_list(session)


@router.post('/create', response_model=RoleSerializer, status_code=HTTPStatus.CREATED)
async def create_role(role_data: RoleCreateSerializer, authorize: AuthJWT = Depends(),
                      role_service: RoleService = Depends(get_role_service),
                      session: AsyncSession = Depends(get_session)):

    # await authorize.jwt_refresh_token_required()
    user_username = await authorize.get_jwt_subject()

    db_user = await session.execute(select(User).where(User.email == user_username))
    user = db_user.scalars().first()

    if user.role.name != 'admin':
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='You have no permission to create role')

    if await role_service.get_by_attribute('name', role_data.name, session):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Role already exists')

    return await role_service.create(role_data, session)


@router.post('/assign_user', response_model=AssignRoleSerializer, status_code=HTTPStatus.OK)
async def add_role_user(username: str,
                        role_name: str,
                        role_service: RoleService = Depends(get_role_service),
                        user_service: UserService = Depends(get_user_service),
                        authorize: AuthJWT = Depends(),
                        session: AsyncSession = Depends(get_session)):
    # await authorize.jwt_refresh_token_required()
    user_username = await authorize.get_jwt_subject()
    request_user = await user_service.get_user_by_username(user_username, session)

    if request_user.role.name != 'admin':
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='You have no permission to create role')

    user = await user_service.get_user_by_username(username, session)
    role = await role_service.get_by_name(role_name, session)

    user = await role_service.assign_role(role, user, session)

    return AssignRoleSerializer(
        username=user.email,
        role=RoleSerializer(id=role.id, name=role.name)
    )


@router.post('/cancel_user', response_model=AssignRoleSerializer, status_code=HTTPStatus.OK)
async def revoke_role(
        username: str,
        role_service: RoleService = Depends(get_role_service),
        user_service: UserService = Depends(get_user_service),
        authorize: AuthJWT = Depends(),
        session: AsyncSession = Depends(get_session)):
    # await authorize.jwt_refresh_token_required()
    user_username = await authorize.get_jwt_subject()
    request_user = await user_service.get_user_by_username(user_username, session)

    if request_user.role.name != 'admin':
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='You have no permission to create role')

    user = await user_service.get_user_by_username(username, session)
    role = await role_service.get_default_role(session)
    user = await role_service.assign_role(role, user, session)

    return AssignRoleSerializer(
        username=user.email,
        role=RoleSerializer(id=role.id, name=role.name)
    )
