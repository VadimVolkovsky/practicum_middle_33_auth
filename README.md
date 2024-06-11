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

## Local run for debug:
#POSTGRES_DB=auth_database
#POSTGRES_USER=app
#POSTGRES_PASSWORD=123qwe
#POSTGRES_HOST=localhost
#POSTGRES_PORT=5433
#REDIS_HOST=localhost
#REDIS_PORT=6380" > .env
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

#### Создание супер пользователя:
```shell script
make superuser
```

#### Остановка контейнеров

```shell script
make down
```