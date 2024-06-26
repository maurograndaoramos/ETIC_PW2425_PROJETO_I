.PHONY: help migrate migration_sync up down superuser flush all

all: migration create_superuser up

help:
	@echo "make all     - Set up the entire project (migration, create superuser, start services)"
	@echo "make up      - Start the Docker Compose services"
	@echo "make down    - Stop and remove Docker Compose services and images"
	@echo "make superuser - Create a superuser"
	@echo "make migration - Run Django migrations"
	@echo "make migration_sync - Run Django migrations and sync database"
	@echo "make flush   - Flush database"

migration:
	(cd EDrive && python3 manage.py makemigrations && python3 manage.py migrate)

migration_sync:
	(cd EDrive && python3 manage.py makemigrations && python3 manage.py migrate --run-syncdb)

superuser:
	(cd EDrive && python3 manage.py createsuperuser)

create_superuser:
	@echo "Creating superuser..."
	@cd EDrive && echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('Admin', 'admin@test.com', 'Admin') if not User.objects.filter(username='Admin').exists() else None" | python3 manage.py shell

flush:
	(cd EDrive && python3 manage.py flush)

up:
	docker compose up

down:
	docker compose dow