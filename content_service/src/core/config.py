import os
from logging import config as logging_config

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)
load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class ContentBaseSettings(BaseSettings):
    class Config:
        env_file = '.env'
        extra = 'ignore'


class JaegerSettings(BaseSettings):
    jaeger_host: str = Field(
        default='content_jaeger',
    )
    jaeger_port: int = Field(
        default=6831,
    )
    enable_tracer: bool = Field(default=True)

    class Config:
        env_file = '.env'


class AppSettings(BaseSettings):
    # Настройки для запуска приложения в контейнерах
    project_name: str = 'movies'
    redis_host: str = Field(default='content_redis')
    redis_port: int = Field(default=6379)
    elastic_host: str = Field(default='content_elasticsearch')
    elastic_port: int = Field(default=9200)
    auth_service_host: str = Field(default='auth_nginx')
    auth_service_port: int = Field(default=80)

    jaeger: JaegerSettings = JaegerSettings()

    # Настройки для локального дебага приложения (без контейнера)
    # redis_host: str = Field(default='127.0.0.1')
    # redis_port: int = Field(default=6379)
    # elastic_host: str = Field(default='127.0.0.1')
    # elastic_port: int = Field(default=9200)
    # auth_service_host: str = Field(default='127.0.0.1')
    # auth_service_port: int = Field(default=8000)

    @property
    def auth_check_token_url(self):
        return f'http://{self.auth_service_host}:{self.auth_service_port}/api/v1/auth/check_token'


app_settings = AppSettings()
