from fastapi import APIRouter

from api.v1.endpoints import auth_router

main_router = APIRouter()

main_router.include_router(
    auth_router,
    prefix='/auth',
    tags=['Auth'],
)