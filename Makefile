DOCKER_COMPOSE:=docker compose
EXEC_CORE:=$(DOCKER_COMPOSE) exec auth_api


# work with docker

build:
#	export DOCKER_BUILDKIT=1 && docker build -f auth_service/Dockerfile -t async_api_image .
	$(DOCKER_COMPOSE) build

ps:
	$(DOCKER_COMPOSE) ps

up:
	$(DOCKER_COMPOSE) up


restart:
	$(DOCKER_COMPOSE) restart

down:
	$(DOCKER_COMPOSE) down

pull:
	$(DOCKER_COMPOSE) pull

shell:
	$(EXEC_CORE) bash

flake8:
	$(EXEC_CORE) flake8

test:
	$(EXEC_CORE) pytest

makemigrations_auth:
	$(EXEC_CORE) alembic revision --autogenerate

migrate_auth:
	$(EXEC_CORE) alembic upgrade head

roles_auth:
	$(EXEC_CORE) python src/create_roles.py

superuser_auth:
	$(EXEC_CORE) python src/superuser.py
