import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AuthBaseSettings(BaseSettings):
    class Config:
        env_file = '.env'
        extra = 'ignore'


class JaegerSettings(AuthBaseSettings):
    jaeger_host: str = Field(
        default='jaeger_service',
    )
    jaeger_port: int = Field(
        default=6831,
    )
    enable_tracer: bool = Field(default=True)


class AppSettings(AuthBaseSettings):
    project_name: str = Field(default='auth')

    service_host: str
    service_port: int
    service_url: str

    postgres_host: str
    postgres_port: int
    postgres_db: str
    postgres_user: str
    postgres_password: str
    echo: bool = False  # вывод операций с БД в логи

    redis_host: str
    redis_port: int

    authjwt_secret_key: str = "secret"
    authjwt_denylist_enabled: bool = True
    authjwt_denylist_token_checks: set = {"access", "refresh"}
    access_expires: int = 3600
    refresh_expires: int = 86400

    debug: bool = Field(default='False')

    jaeger: JaegerSettings = JaegerSettings()

    @property
    def database_url(self):
        return (f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@'
                f'{self.postgres_host}:{self.postgres_port}/{self.postgres_db}')


app_settings = AppSettings()
