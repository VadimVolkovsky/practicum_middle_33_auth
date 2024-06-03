import logging
from contextlib import asynccontextmanager

import uvicorn
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from redis import Redis
from starlette.responses import JSONResponse

from api.v1.routers import main_router
from core.config import app_settings
from core.logger import LOGGING
from db import redis
from db.postgres import create_database, purge_database
from models.entity import add_default_roles


@asynccontextmanager
async def lifespan(app: FastAPI):
    await purge_database()  # TODO только для отладки приложения
    await create_database()  # TODO только для отладки приложения
    await add_default_roles()  # TODO только для отладки приложения
    redis.redis = Redis(host=app_settings.redis_host, port=app_settings.redis_port)
    yield
    await redis.redis.close()


app = FastAPI(
    title=app_settings.project_name,
    description="Сервис авторизации",
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


app.include_router(main_router, prefix='/api/v1')


# TODO подумать куда вынести
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
