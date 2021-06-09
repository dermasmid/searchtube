include .env

default: up

up:
	docker-compose up -d --remove-orphans

shell:
	docker exec -ti -e COLUMNS=$(shell tput cols) -e LINES=$(shell tput lines) ${PROJECT_NAME}_wsgi bash

logs:
	docker logs ${PROJECT_NAME}_wsgi -f

stop:
	docker-compose stop

down:
	docker-compose down

build:
	docker-compose up -d --build

ps:
	docker-compose ps
