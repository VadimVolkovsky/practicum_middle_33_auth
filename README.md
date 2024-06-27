Переименовать все .env.example в .env

Собрать образы
```shell
make build
```

Запустить
```shell
make up
```

_Миграции сервиса admin_panel применяются автоматически при запуске.
Для корректной работы требуется наличие схемы 'content' в БД сервиса admin_panel_postgres_


Создать миграции сервиса auth
```shell
make makemigrations_auth
```

Применить миграции сервиса auth
```shell
make migrate_auth
```

Создать дефолтные роли в сервисе auth
```shell
make roles_auth
```

Создать дефолтные соц сети в сервисе auth
```shell
make social_networks_auth
```

Создать суперюзера в сервисе auth
```shell
make superuser_auth
```


Сервис Jaeger WEB GUI (трассировка запросов)
```
http://0.0.0.0:16686/search
```