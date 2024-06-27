import logging
from contextlib import asynccontextmanager
from http import HTTPStatus

import uvicorn
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI, Request
from fastapi.responses import ORJSONResponse
from fastapi_limiter import FastAPILimiter
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from redis.asyncio import Redis

from helpers.jaeger import configure_tracer
from core.config import app_settings
from core.logger import LOGGING
from db import redis, elastic
from api.v1.routers import main_router


tracer = trace.get_tracer(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if app_settings.jaeger.enable_tracer:
        configure_tracer(
            app_settings.jaeger.jaeger_host,
            app_settings.jaeger.jaeger_port,
            app_settings.project_name,
        )

    redis.redis = Redis(host=app_settings.redis_host, port=app_settings.redis_port)
    await FastAPILimiter.init(redis.redis)
    elastic.es = AsyncElasticsearch(hosts=[f'{app_settings.elastic_host}:{app_settings.elastic_port}'])
    yield
    await redis.redis.close()
    await FastAPILimiter.close()
    await elastic.es.close()


app = FastAPI(
    title=app_settings.project_name,
    description="Информация о фильмах, жанрах и людях, участвовавших в создании произведения",
    version="1.0.0",
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)

@app.middleware("http")
async def before_request(request: Request, call_next):
    request_id = request.headers.get('X-Request-Id')
    if not request_id:
        return ORJSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={'detail': 'X-Request-Id is required'},
        )
    with tracer.start_as_current_span('content_request') as span:
        span.set_attribute('http.request_id', request_id)
        response = await call_next(request)
        return response

FastAPIInstrumentor.instrument_app(app)

app.include_router(main_router, prefix='/api/v1')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
