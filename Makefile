.PHONY: shell, test, dev, start, build, migrate, shell_plus

PROJECT_NAME=django_atomic_transactions
DOCKER_COMPOSE=docker-compose -p ${PROJECT_NAME} -f environment/docker-compose.yml
DOCKER_COMPOSE_RUN_WEB=${DOCKER_COMPOSE} run --rm

default: build

build:
	${DOCKER_COMPOSE} build

stop:
	${DOCKER_COMPOSE} stop

rm:
	${DOCKER_COMPOSE} rm -f

start:
	${DOCKER_COMPOSE} up web

dev:
	${DOCKER_COMPOSE_RUN_WEB} --service-ports web dev

uvicorn:
	${DOCKER_COMPOSE_RUN_WEB} --service-ports web uvicorn

test: build
	${DOCKER_COMPOSE_RUN_WEB} web python manage.py test --failfast api

shell:
	${DOCKER_COMPOSE_RUN_WEB} web ash

shell_plus:
	${DOCKER_COMPOSE_RUN_WEB} web python manage.py shell_plus

migrate: build
	${DOCKER_COMPOSE_RUN_WEB} web migrate

# This action will erase all previous data
loaddata: migrate
	${DOCKER_COMPOSE_RUN_WEB} web loaddata
