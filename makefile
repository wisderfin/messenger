include .env
export $(shell sed -E '/^\s*#/d;/^\s*$$/d;s/=.*//' .env)

# standart commands
up:
	docker-compose up
upd:
	docker-compose up -d
upb:
	docker-compose up --build
upbd:
	docker-compose up --build -d
stop:
	docker-compose stop
down:
	docker-compose down
logs:
	docker-compose logs -f

# commands for api-container
api-sh:
	docker-compose exec api sh
