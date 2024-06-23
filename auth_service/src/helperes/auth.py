from functools import wraps
from http import HTTPStatus

from async_fastapi_jwt_auth import AuthJWT
from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.serializers.role_serializer import AssignRoleSerializer, RoleCreateSerializer
from db.postgres import get_session
from helperes.auth_request import AuthRequest
from helperes.exceptions import AuthException
from services.user_service import get_user_service, UserService


def roles_required(roles_list: list[RoleCreateSerializer]):
    def decorator(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):
            user: AssignRoleSerializer = kwargs.get('request').request_user
            if not user or user.role.name not in [x for x in roles_list]:
                raise AuthException(
                    status_code=HTTPStatus.FORBIDDEN, detail='This operation is forbidden for you',
                )
            return await function(*args, **kwargs)
        return wrapper
    return decorator


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request, session: AsyncSession = Depends(get_session),
                       user_service: UserService = Depends(get_user_service)) -> AssignRoleSerializer | None:
        authorize = AuthJWT(req=request)
        # await authorize.jwt_optional()
        user_email = await authorize.get_jwt_subject()

        if not user_email:
            return None

        user = await user_service.get_user_by_email(user_email, session)
        return AssignRoleSerializer.from_orm(user)


async def get_current_user_global(request: AuthRequest, user: AsyncSession = Depends(JWTBearer())):
    request.request_user = user
