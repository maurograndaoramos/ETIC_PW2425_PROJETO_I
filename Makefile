.PHONY: help migrate migration_sync up down
# ALGUÉM ME LIBERTA DESSE MAKEFILE PELO AMOR DE DEUS
help:
	@echo "make up      - Start the Docker Compose services"
	@echo "make down    - Stop and remove Docker Compose services and images"
	@echo "make superuser - Create a superuser"
	@echo "make migration - Run Django migrations"
	@echo "make migration_sync - Run Django migrations and sync database"
	@echo "make flush - Flush database"


migration:
	(cd EDrive && python3 manage.py makemigrations && python3 manage.py migrate)

migration_sync:
	(cd EDrive && python3 manage.py makemigrations && python3 manage.py migrate --run-syncdb)

superuser:
	(cd EDrive && python3 manage.py createsuperuser)

flush:
	(cd EDrive && python3 manage.py flush)

up:
	docker compose up

down:
	docker compose down --rmi all --volumes --remove-orphans

