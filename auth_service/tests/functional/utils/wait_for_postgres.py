import backoff
from sqlalchemy_utils import database_exists


@backoff.on_exception(backoff.expo, ConnectionError)
def is_db_exist(pg_url: str):
    return database_exists(pg_url)


if __name__ == '__main__':
    pg_url = 'postgresql://test:test@postgres:5432/test'
    is_db_exist(pg_url=pg_url)
