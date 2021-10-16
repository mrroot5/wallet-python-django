.PHONY: shell, test, dev, start, build, migrate, shell_plus

PROJECT_NAME=django_atomic_transactions
DOCKER_COMPOSE=docker-compose -p ${PROJECT_NAME} -f environment/docker-compose.yml
LOCAL_USER="--user=$(shell id -u):$(shell id -g)"
DOCKER_COMPOSE_RUN_WEB=${DOCKER_COMPOSE} run --rm ${LOCAL_USER}

default: build

build:
	${DOCKER_COMPOSE} build

stop:
	${DOCKER_COMPOSE} stop

rm:
	${DOCKER_COMPOSE} rm

start:
	${DOCKER_COMPOSE} up web

dev:
	${DOCKER_COMPOSE_RUN_WEB} --service-ports web dev

web:
	${DOCKER_COMPOSE_RUN_WEB} --service-ports web web

test: build
	${DOCKER_COMPOSE_RUN_WEB} web test

shell:
	${DOCKER_COMPOSE_RUN_WEB} web ash

shell_plus:
	${DOCKER_COMPOSE_RUN_WEB} web python manage.py shell_plus

migrate: build
	${DOCKER_COMPOSE_RUN_WEB} web migrate

loaddata: migrate
	${DOCKER_COMPOSE_RUN_WEB} web loaddata
