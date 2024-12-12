include .env

PROJECT=smtp-project

default:
	@echo --- Выберете подходящую команду ---
	@awk -F ":" '/^[^#[:space:]].*:/ {print " •", $$1}' Makefile | sort

install:
	@$(MAKE) -s docker-build

restart: \
	down \
	up

docker-build: \
	docker-build-app

docker-build-app:
	@docker build --progress=plain --target=python \
         -t ${REGISTRY}/${SERVICE_SMTP}/python:${IMAGE_TAG} -f ./docker/Dockerfile .

docker-logs:
	@docker compose -p ${PROJECT} logs -f

up:
	@docker compose -p ${PROJECT} -f docker-compose.yml up -d

down:
	@docker compose -p ${PROJECT} -f docker-compose.yml down

builder-exec:
	@docker container run --rm -v $(PWD):/app \
		 ${REGISTRY}/${SERVICE_SMTP}/python:${IMAGE_TAG} \
		 $(cmd)

ps:
	@docker compose -p ${PROJECT} -f docker-compose.yml ps

app-py-cli-exec:
	@docker compose -p ${PROJECT} \
		 -f docker-compose.yml run --rm ${PROJECT} $(cmd)

shell:
	$(MAKE) app-py-cli-exec cmd="/bin/bash"