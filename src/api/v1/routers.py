from fastapi import APIRouter, Depends

from api.v1.endpoints import auth_router, role_router
from helperes.auth import get_current_user_global

main_router = APIRouter()

main_router.include_router(
    role_router,
    prefix='/role',
    tags=['Role'],
    dependencies=[Depends(get_current_user_global)]
)
main_router.include_router(
    auth_router,
    prefix='/auth',
    tags=['Auth'],
)
