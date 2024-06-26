FROM python:latest
RUN pip install poetry
WORKDIR /app
COPY . .
WORKDIR /app/EDrive
EXPOSE 8000
RUN poetry install
CMD poetry run python manage.py runserver 0.0.0.0:8000