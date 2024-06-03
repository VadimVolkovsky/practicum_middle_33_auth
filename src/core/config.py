import os

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings


load_dotenv()


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppSettings(BaseSettings):
    project_name: str = Field(default='auth')

    postgres_host: str = Field(default='localhost')
    postgres_port: int = Field(default=5432)
    postgres_db: str = Field(default='auth_database')
    postgres_user: str = Field(default='app')
    postgres_password: str = Field(default='123qwe')

    redis_host: str = Field(default='redis')
    redis_port: int = Field(default=6379)

    authjwt_secret_key: str = "secret"

    class Config:
        env_file = '.env'


app_settings = AppSettings()
