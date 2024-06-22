Launch project:
```
cd docker_compose/empty_project/
```

```
docker-compose up --build -d
```

```
docker exec django_practicum python manage.py collectstatic --no-input
```

Open in browser:
```
http://127.0.0.1/admin/
```