import fakeredis
import pytest_asyncio
from redis import Redis

from main import app
from services.redis import get_redis
from tests.settings import test_settings


# @pytest_asyncio.fixture
# async def fake_redis():
#     redis = fakeredis.aioredis.FakeRedis(decode_responses=True)
#     yield redis
#     await redis.aclose()
#
#
# @pytest_asyncio.fixture
# def app_with_overridden_redis(fake_redis):
#     app.dependency_overrides[get_redis] = lambda: fake_redis
#     return app
#

@pytest_asyncio.fixture(scope="session")
async def redis_client():
    redis_client = Redis(
        host=test_settings.redis_host,
        port=test_settings.redis_port,
    )
    yield redis_client
    await redis_client.close()