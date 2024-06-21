from redis.asyncio import Redis

from core.config import app_settings

# redis: Redis | None = None
redis: Redis = Redis(host=app_settings.redis_host, port=app_settings.redis_port)


async def get_redis() -> Redis:
    return redis
