default: up

up:
	docker-compose up -d --remove-orphans

shell:
	docker exec -ti -e COLUMNS=$(shell tput cols) -e LINES=$(shell tput lines) rextube_wsgi bash

logs:
	docker logs rextube_wsgi -f

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
