default: up

up:
	docker-compose up -d --remove-orphans

shell:
	docker exec -ti -e COLUMNS=$(shell tput cols) -e LINES=$(shell tput lines) searchtube_wsgi bash

logs:
	docker logs searchtube_wsgi -f

stop:
	docker-compose stop

down:
	docker-compose down

build:
	docker-compose up -d --build

ps:
	docker-compose ps

restart:
	docker-compose restart
