import backoff
from redis import Redis


@backoff.on_exception(backoff.expo, ConnectionError)
def pinging_redis(redis_client: Redis) -> bool:
    """Waiting for test Redis service response"""
    return redis_client.ping()


if __name__ == "__main__":
    client = Redis("redis")
    pinging_redis(redis_client=client)
