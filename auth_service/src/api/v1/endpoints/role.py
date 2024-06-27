from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.serializers.role_serializer import RoleSerializer, RoleCreateSerializer, AssignRoleSerializer
from db.postgres import get_session
from helperes.auth import roles_required
from helperes.auth_request import AuthRequest
from models.entity import Roles
from services.role_servece import RoleService, get_role_service
from services.user_service import UserService, get_user_service

router = APIRouter()


@router.get('', response_model=list[RoleSerializer], status_code=HTTPStatus.OK,
            dependencies=[Depends(RateLimiter(times=2, seconds=5))],)
@roles_required(roles_list=[Roles.admin.value])
async def get_roles(request: AuthRequest,
                    role_service: RoleService = Depends(get_role_service),
                    session: AsyncSession = Depends(get_session)):
    # await authorize.jwt_refresh_token_required()

    return await role_service.get_list(session)


@router.post('/create', response_model=RoleSerializer, status_code=HTTPStatus.CREATED,
             dependencies=[Depends(RateLimiter(times=2, seconds=5))],)
@roles_required(roles_list=[Roles.admin.value])
async def create_role(request: AuthRequest,
                      role_data: RoleCreateSerializer,
                      role_service: RoleService = Depends(get_role_service),
                      session: AsyncSession = Depends(get_session)):
    # await authorize.jwt_refresh_token_required()

    if await role_service.get_by_attribute('name', role_data.name, session):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Role already exists')

    return await role_service.create(role_data, session)


@router.post('/assign_user', response_model=AssignRoleSerializer, status_code=HTTPStatus.OK,
             dependencies=[Depends(RateLimiter(times=2, seconds=5))],)
@roles_required(roles_list=[Roles.admin.value])
async def add_role_user(request: AuthRequest,
                        email: str,
                        role_name: str,
                        role_service: RoleService = Depends(get_role_service),
                        user_service: UserService = Depends(get_user_service),
                        session: AsyncSession = Depends(get_session)):
    # await authorize.jwt_refresh_token_required()

    user = await user_service.get_user_by_email(email, session)
    role = await role_service.get_by_name(role_name, session)

    user = await role_service.assign_role(role, user, session)

    return AssignRoleSerializer(
        email=user.email,
        role=RoleSerializer(id=role.id, name=role.name)
    )


@router.post('/cancel_user', response_model=AssignRoleSerializer, status_code=HTTPStatus.OK,
             dependencies=[Depends(RateLimiter(times=2, seconds=5))],)
@roles_required(roles_list=[Roles.admin.value])
async def revoke_role(request: AuthRequest,
                      email: str,
                      role_service: RoleService = Depends(get_role_service),
                      user_service: UserService = Depends(get_user_service),
                      session: AsyncSession = Depends(get_session)):
    # await authorize.jwt_refresh_token_required()

    user = await user_service.get_user_by_email(email, session)
    role = await role_service.get_default_role(session)
    user = await role_service.assign_role(role, user, session)

    return AssignRoleSerializer(
        email=user.email,
        role=RoleSerializer(id=role.id, name=role.name)
    )
