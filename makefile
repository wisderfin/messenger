include .env
export $(shell sed -E '/^\s*#/d;/^\s*$$/d;s/=.*//' .env)

# standart commands
up:
	docker-compose up --remove-orphans
upd:
	docker-compose up --remove-orphans -d
upb:
	docker-compose up --remove-orphans --build
upbd:
	docker-compose up --remove-orphans --build -d
stop:
	docker-compose stop --remove-orphans
down:
	docker-compose down --remove-orphans -v
logs:
	docker-compose logs -f

# commands for api-container
api-sh:
	docker-compose exec api sh

# commands for database-container
db-sh:
	docker-compose exec database sh
psql:
	docker-compose exec database sh -c "psql -U $(DATABASE_USER) -d $(DATABASE_NAME)"

# comands for migration-container
msg?=
mgr:
	docker-compose run migration sh -c "alembic revision --autogenerate -m '$(msg)'"
	docker-compose run migration sh -c "alembic upgreade head"
	docker-compose stop migration
