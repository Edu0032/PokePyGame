.PHONY: install install-dev run-game run-api docker-up test coverage lint typecheck format quality migrate pre-commit

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

run-game:
	python -m PokePY.main

run-api:
	uvicorn PokePY.api.main:app --reload

docker-up:
	docker compose up --build

test:
	pytest

coverage:
	pytest --cov=PokePY --cov-report=term-missing

lint:
	ruff check PokePY tests

typecheck:
	mypy PokePY

format:
	black PokePY tests
	ruff check PokePY tests --fix

quality: lint typecheck test

migrate:
	alembic upgrade head

pre-commit:
	pre-commit run --all-files
