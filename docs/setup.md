# Local development setup

Run all commands from the repository root. These instructions cover the database infrastructure and PY-003 stone creation endpoint. Creation returns HTTP 201 with only the generated UUID; other CRUD operations are not implemented yet.

## Prerequisites

- uv available on your PATH.
- Python 3.13, which uv can provision when synchronizing the project.
- Docker with Docker Compose support, with the Docker daemon running.
- Make for the combined development check command.

## Install dependencies

```sh
uv sync --locked
```

This creates or updates the project-local `.venv` and installs the locked application and development dependencies. Run project commands through `uv run` to use this environment.

## Configure the local environment

If `.env` does not already exist, copy the template:

```sh
cp .env.example .env
```

Keep an existing `.env` rather than overwriting it. Replace the password placeholders with local values before the first infrastructure startup. Do not commit `.env` or credentials.

The application consumes these PostgreSQL settings:

| Variable | Purpose | Local template value |
| --- | --- | --- |
| `POSTGRES_HOST` | Host reachable by the application | `127.0.0.1` |
| `POSTGRES_PORT` | Published PostgreSQL port | `55432` |
| `POSTGRES_DB` | Database name | `stone_shelter_py` |
| `POSTGRES_USER` | Database user | `stone_shelter_py` |
| `POSTGRES_PASSWORD` | Database password | Set locally; no credential is documented here |

`DatabaseSettings` reads `.env` relative to the working directory. Existing environment variables take precedence over values in `.env`. The same PostgreSQL values configure Docker Compose and the application.

The template also contains Redis, MinIO, and Ollama settings for later features. They are not required by the current database implementation. Some template comments still describe future wiring; PostgreSQL settings are already wired into the application.

## Start PostgreSQL

```sh
docker compose up -d --wait postgres
docker compose ps postgres
```

Only PostgreSQL is needed for the implemented database and stone creation features. Redis, MinIO, and Ollama do not need to run for the current tests or application bootstrap. Additional infrastructure details are in [infra/README.md](../infra/README.md).

The application runs on the host and connects through the published port. PostgreSQL data is stored in the Compose project's named volume.

To stop PostgreSQL while retaining its data:

```sh
docker compose stop postgres
```

## Manage migrations

Apply all available revisions:

```sh
uv run alembic upgrade head
uv run alembic current
```

Inspect revision files and their history:

```sh
uv run alembic heads
uv run alembic history
```

`heads` describes the available revision graph; `current` reports the revision applied to the configured database. Alembic stores the applied revision in `alembic_version`.

To check a single-step rollback on the local development database, then return to the latest revision:

```sh
uv run alembic downgrade -1
uv run alembic current
uv run alembic upgrade head
uv run alembic current
```

The initial revision has empty `upgrade` and `downgrade` functions. It verifies migration version tracking without introducing business tables. After rolling back this first revision, `current` produces no revision output.

For future schema changes, after defining and importing the relevant ORM models into the migration environment:

```sh
uv run alembic revision --autogenerate -m "Describe the schema change"
```

Review generated upgrade and downgrade operations before applying them. Alembic uses `Base.metadata`, populated by the model imports in `infrastructure/database/models.py`. Catalog tables use the `stone_shelter` schema; the migration version table remains in `public`. Migration execution is a separate CLI operation and does not run automatically at application startup. The current environment supports database-connected commands; offline SQL generation with `--sql` is not implemented.

## Run the application

```sh
uv run uvicorn stone_shelter.main:app --reload --host 127.0.0.1 --port 8000
```

Open [Swagger UI](http://127.0.0.1:8000/docs) or the [OpenAPI document](http://127.0.0.1:8000/openapi.json).

The application lifespan creates the engine and stores the session factory on application state. Shutdown disposes the engine. Creating the engine does not itself establish a database connection or perform a readiness check. Each Unit of Work creates its own session when entered; writes require an explicit commit.

Stop the server with `Ctrl+C`.

## Run checks and tests

Run the full local development check sequence with one command:

```sh
make check
```

This runs Ruff autofix, Ruff formatting, mypy, pytest, and `alembic check`, in that order. It stops at the first failing command. Ruff intentionally updates source files. PostgreSQL must be running and migrations must be applied before running this target. `alembic check` checks for pending autogenerated schema operations; it does not apply migrations.

Read-only lint, formatting, and type checks:

```sh
uv run ruff check --no-fix .
uv run ruff format --check .
uv run mypy
```

`--no-fix` overrides the project's default Ruff autofix setting. Mypy checks application code, tests, and migration scripts.

Run unit tests without PostgreSQL:

```sh
uv run pytest tests/unit
```

Run PostgreSQL integration tests, or the complete suite, with PostgreSQL available and `.env` configured:

```sh
uv run pytest tests/integration
uv run pytest
```

Focused lifecycle and transaction tests:

```sh
uv run pytest tests/unit/application/test_lifespan.py
uv run pytest tests/unit/application/test_unit_of_work.py
uv run pytest tests/integration/test_database_engine.py
uv run pytest tests/integration/test_unit_of_work.py
uv run pytest tests/integration/catalog/test_create_stone.py -v
```

Transaction integration tests create uniquely named technical tables in the configured database and remove them during fixture cleanup. Use the isolated local development database, not a production database. The tests cover explicit commit, uncommitted exit, and exception rollback. Multi-participant atomicity testing is deferred until real persistence operations exist.

Stone creation tests use the migrated `stone_shelter.stones` table and clean up their uniquely identified test records. They cover successful creation and five parameterized invalid-input cases. An endpoint failure after insertion but before commit, and migration verification against a fresh isolated database, are deferred by the owner and are not claimed as verified by `make check`.
