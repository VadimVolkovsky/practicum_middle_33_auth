from http import HTTPStatus

from async_fastapi_jwt_auth import AuthJWT
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import db
import models
from api.v1.serializers.role_serializer import RoleSerializer, RoleCreateSerializer
from db.postgres import get_session
from models.entity import Role, User
from services.role_servece import RoleService, get_role_service

router = APIRouter()


@router.get('', response_model=list[RoleSerializer], status_code=HTTPStatus.OK)
async def get_roles(
        authorize: AuthJWT = Depends(),
        role_service: RoleService = Depends(get_role_service),
        session: AsyncSession = Depends(get_session)):

    # await authorize.jwt_refresh_token_required()
    user_username = await authorize.get_jwt_subject()
    db_user = await session.execute(select(User).where(User.login == user_username))
    user = db_user.scalars().first()

    if user.role.name != 'admin':
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='You have no permission to create role')

    return await role_service.get_list(session)


@router.post('/create', status_code=HTTPStatus.CREATED)
async def create_role(role_data: RoleCreateSerializer, authorize: AuthJWT = Depends(),
                      role_service: RoleService = Depends(get_role_service),
                      session: AsyncSession = Depends(get_session)):

    # await authorize.jwt_refresh_token_required()
    user_username = await authorize.get_jwt_subject()

    db_user = await session.execute(select(User).where(User.login == user_username))
    user = db_user.scalars().first()

    if user.role.name != 'admin':
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail='You have no permission to create role')

    if await role_service.get_by_attribute('name', role_data.name, session):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Role already exists')

    return await role_service.create(role_data, session)
