from core.config import AppSettings

# class TestSettings(BaseSettings):
#     service_host: str
#     service_port: int
#
#     service_url: str
#
#     postgres_host: str
#     postgres_port: int
#     postgres_db: str
#     postgres_user: str
#     postgres_password: str
#
#     redis_host: str
#     redis_port: int
#
#     @property
#     def test_database_url(self):
#         return (f'postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@'
#                 f'{self.postgres_host}:{self.postgres_port}/{self.postgres_db}')
# #
#     class Config:
#         env_file = '.env'

test_settings = AppSettings()
