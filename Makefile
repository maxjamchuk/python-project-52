.PHONY: install lint test migrate collectstatic start render-start build

install:
	uv sync

lint:
	uv run ruff check

dev:
	uv run manage.py runserver

start:
	uv run gunicorn task_manager.asgi:application -k uvicorn.workers.UvicornWorker

render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh

migrate:
	uv run manage.py migrate --run-syncdb

migrations:
	uv run manage.py makemigrations

test:
	uv run manage.py test task_manager

coverage:
	uv run coverage run manage.py test task_manager
	uv run coverage xml
	uv run coverage report
