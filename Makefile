.PHONY: check

check:
	uv run ruff check --fix .
	uv run ruff format .
	uv run mypy
	uv run pytest
	uv run alembic check
