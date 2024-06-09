# practicum_middle_33_auth

Инструкция по развертыванию

Выполните в консоли следующие команды:

#### Создание файла окружения с тестовыми данными:

```
touch ./.env & echo "## Run in docker containers:
POSTGRES_DB=auth_database
POSTGRES_USER=app
POSTGRES_PASSWORD=123qwe
POSTGRES_HOST=middle_practicum_auth_postgres
POSTGRES_PORT=5432
REDIS_HOST=middle_practicum_auth_redis
REDIS_PORT=6379

## Local run for debug:
#POSTGRES_DB=auth_database
#POSTGRES_USER=app
#POSTGRES_PASSWORD=123qwe
#POSTGRES_HOST=localhost
#POSTGRES_PORT=5432
#REDIS_HOST=localhost
#REDIS_PORT=6380" > .env
```


##### Создание контейнеров

```shell script
make build
```

#### Запуск

```shell script
make up
```
#### Остановка

```shell script
make down
```



