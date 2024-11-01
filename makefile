include .env
export $(shell sed -E '/^\s*#/d;/^\s*$$/d;s/=.*//' .env)

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
