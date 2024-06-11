DOCKER_COMPOSE:=docker compose
EXEC_CORE:=$(DOCKER_COMPOSE) exec api


# work with docker

build:
	export DOCKER_BUILDKIT=1 && docker build -f ./Dockerfile -t async_api_image .

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

superuser:
	docker exec middle_practicum_api python superuser.py
