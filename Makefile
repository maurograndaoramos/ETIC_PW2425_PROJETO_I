.PHONY: help migrate up down

# ALGUÉM ME LIBERTA DESSE MAKEFILE PELO AMOR DE DEUS
help:
	@echo "make migration - Run Django migrations"
	@echo "make migration sync - Run Django migrations and sync database"
	@echo "make up      - Start the Docker Compose services"
	@echo "make down    - Stop and remove Docker Compose services and images"

migration:
	(cd EDrive && python3 manage.py makemigrations && python3 manage.py migrate)

migration sync:
	(cd EDrive && python3 manage.py makemigrations && python3 manage.py migrate --run-syncdb)

superuser:
	(cd EDrive && python3 manage.py createsuperuser)

flush:
	(cd EDrive && python3 manage.py flush)

superuser:
	(cd EDrive && python manage.py createsuperuser)

up:
	docker compose up

down:
	docker compose down --rmi all --volumes --remove-orphans