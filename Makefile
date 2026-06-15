.PHONY: install dev build test lint format typecheck migrate seed eval worker clean

install:
	cd backend && python -m pip install -e ".[dev]"
	cd frontend && npm install

dev:
	docker compose -f infra/docker-compose.yml up --build

build:
	cd frontend && npm run build

test:
	cd backend && pytest
	cd frontend && npm test

lint:
	cd backend && ruff check .
	cd frontend && npm run lint

format:
	cd backend && black . && ruff check . --fix
	cd frontend && npm run format

typecheck:
	cd backend && mypy app
	cd frontend && npm run typecheck

migrate:
	cd backend && alembic upgrade head

seed:
	python scripts/seed.py

eval:
	cd backend && python -m app.eval_runner

worker:
	cd backend && python -m app.worker

clean:
	git clean -Xdf
