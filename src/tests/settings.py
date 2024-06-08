from pydantic_settings import BaseSettings


class TestSettings(BaseSettings):
    test_database_url: str = 'postgresql+asyncpg://test:test@postgres:5432/test'
    
    # Настройки для запуска тестирования в контейнерах
    # service_url: str = 'http://api:8000'
    # redis_host: str = 'redis'
    # redis_port: int = 6379

    # Настройки для локального дебага тестов (без контейнера)
    service_url: str = 'http://127.0.0.1:8000'
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    REDIS_HOST: str ='localhost'
    REDIS_PORT: int = 6380
    class Config:
        env_file = '.env'

test_settings = TestSettings()