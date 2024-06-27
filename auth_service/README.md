# practicum_middle_33_auth

Инструкция по развертыванию

Выполните в консоли следующие команды:

#### Создание файла окружения с тестовыми данными:

```
touch ./.env & echo "## Run in docker containers:
SERVICE_URL=$SERVICE_HOST:$SERVICE_PORT
SERVICE_HOST=0.0.0.0
SERVICE_PORT=8000

ECHO=False
DEBUG=False

POSTGRES_DB=auth_database
POSTGRES_USER=app
POSTGRES_PASSWORD=123qwe
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
REDIS_HOST=redis
REDIS_PORT=6379
DATABASE_URL=postgresql+asyncpg://app:123qwe@middle_practicum_auth_postgres:5432/auth_database

## Local run for debug:
#POSTGRES_DB=auth_database
#POSTGRES_USER=app
#POSTGRES_PASSWORD=123qwe
#POSTGRES_HOST=localhost
#POSTGRES_PORT=5433
#REDIS_HOST=localhost
#REDIS_PORT=6380
#DATABASE_URL=postgresql+asyncpg://app:123qwe@localhost:5433/auth_database" > .env
```


##### Создание контейнеров

```shell script
make build
```

#### Запуск контейнеров

```shell script
make up
```

#### Создание миграций

```shell script
make makemigrations
```

#### Применение миграций

```shell script
make migrate
```

#### Создание ролей пользователей:
```shell script
make roles_auth
```

#### Создание социальных сетей:
```shell script
make social_networks_auth
```

#### Создание супер пользователя:
```shell script
make superuser
```

#### Остановка контейнеров

```shell script
make down
```