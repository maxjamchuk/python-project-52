.PHONY: install lint test migrate collectstatic start render-start build setup

install:
	uv sync

lint:
	uv run ruff check .

test:
	uv run pytest

migrate:
	uv run python manage.py migrate

collectstatic:
	uv run python manage.py collectstatic --noinput

start:
	uv run python manage.py runserver 0.0.0.0:8000

render-start:
	gunicorn task_manager.wsgi

build:
	./build.sh

setup:
	@echo "Hexlet CI setup: nothing to do here (env will be prepared later)"
