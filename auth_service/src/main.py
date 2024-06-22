import logging
from contextlib import asynccontextmanager

import uvicorn
from async_fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi_pagination import add_pagination
from redis.asyncio import Redis
from starlette.responses import JSONResponse

from api.v1.routers import main_router
from core.config import app_settings
from core.logger import LOGGING
from models.entity import add_default_roles
from services import redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    if app_settings.debug is True:
        # await purge_database()  # TODO использовать алембик
        # await create_database()  # TODO использовать алембик
        # await add_default_roles()
        pass

    if app_settings.jaeger.enable_tracer:
        configure_tracer(
            settings.jaeger.jaeger_host,
            settings.jaeger.jaeger_port,
            settings.service_name,
        )

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


@app.middleware("http")
async def before_request(request: Request, call_next):
    request_id = request.headers.get("X-Request-Id")
    if not request_id:
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": "X-Request-Id is required"},
        )
    with tracer.start_as_current_span("auth_request") as span:
        span.set_attribute("http.request_id", request_id)
        response = await call_next(request)
        return response


app.include_router(main_router, prefix='/api/v1')
add_pagination(app)


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
        host=app_settings.service_host,
        port=app_settings.service_port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
