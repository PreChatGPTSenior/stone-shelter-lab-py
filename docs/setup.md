# Local development setup

Run all commands from the repository root. These instructions cover the database infrastructure, PY-003 stone creation endpoint, and PY-007 Testcontainers-based integration tests. Creation returns HTTP 201 with only the generated UUID; other CRUD operations are not implemented yet.

## Prerequisites

- uv available on your PATH.
- Python 3.13, which uv can provision when synchronizing the project.
- Docker with the daemon running for integration tests. Docker Compose is used for the development application, not for test database startup.
- Make for the combined development check command.

## Install dependencies

```sh
uv sync --locked
```

This creates or updates the project-local `.venv` and installs the locked application and development dependencies. Run project commands through `uv run` to use this environment.

## Configure the local environment

This section configures the development application and manual Alembic commands. Integration tests use explicit Testcontainers settings and do not require this `.env` file.

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

This Compose service is for the development application. Integration tests start their own PostgreSQL container and do not require the Compose PostgreSQL service. Redis, MinIO, and Ollama are not required for the current tests or application bootstrap. Additional infrastructure details are in [infra/README.md](../infra/README.md).

The application runs on the host and connects through the published port. PostgreSQL data is stored in the Compose project's named volume.

To stop PostgreSQL while retaining its data:

```sh
docker compose stop postgres
```

## Manage migrations

The manual commands in this section target the database selected by development configuration. Test migrations are applied automatically to the disposable Testcontainers database instead.

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

This runs Ruff autofix, Ruff formatting, mypy, and pytest, in that order, stopping at the first failing command. Ruff intentionally updates source files. Docker must be available; a development PostgreSQL instance and local `.env` are not required by the integration fixtures. There is no separate development-database `alembic check` command in this target: the migration fixture runs `upgrade head` and then `check` against the fresh container database. `check` detects pending autogenerated schema operations; `upgrade head` applies the migrations.

Read-only lint, formatting, and type checks:

```sh
uv run ruff check --no-fix .
uv run ruff format --check .
uv run mypy
```

`--no-fix` overrides the project's default Ruff autofix setting. Mypy checks application code, tests, and migration scripts.

Run unit tests without PostgreSQL or Docker; they do not request the integration container fixtures:

```sh
uv run pytest tests/unit
```

Run PostgreSQL integration tests, or the complete suite, with the Docker daemon available:

```sh
uv run pytest tests/integration
uv run pytest
```

### Integration database lifecycle

Shared fixtures live in `tests/integration/conftest.py`:

1. `postgres_container` starts one new PostgreSQL/pgvector container per pytest session when first requested, using the same pinned image as development. Docker assigns a host port dynamically. No development volumes are attached.
2. `database_settings` supplies all connection fields explicitly from the container and disables dotenv loading. Tests do not use the development port or credentials.
3. `migrated_database` invokes Alembic through the pytest interpreter in a child process. The child receives container-only PostgreSQL settings and runs from a temporary directory without the development `.env`. It applies the complete migration chain and checks schema drift before database-backed tests run.
4. The shared `app` fixture substitutes those settings into the application lifespan. HTTP requests and independent verification sessions use the same disposable database.
5. Each test releases its own async engines/sessions and cleans up its records or technical tables. Session teardown stops and removes the test container. Downloaded Docker images may remain cached.

The schema starts empty for each pytest session, not each individual test. Existing per-test cleanup is therefore still required. Container startup or migration errors fail setup; there is no fallback to development PostgreSQL and no silent skip when Docker is unavailable. The existing OpenAPI-only test does not require a database connection.

Focused lifecycle and transaction tests:

```sh
uv run pytest tests/unit/application/test_lifespan.py
uv run pytest tests/unit/application/test_unit_of_work.py
uv run pytest tests/integration/test_database_engine.py
uv run pytest tests/integration/test_unit_of_work.py
uv run pytest tests/integration/catalog/test_create_stone.py -v
```

Transaction integration tests create uniquely named technical tables in the disposable container database and remove them during fixture cleanup. Business tables are created by migrations, not `create_all()`. The tests cover explicit commit, uncommitted exit, and exception rollback. Multi-participant atomicity testing remains deferred.

Stone creation tests use the container's migrated `stone_shelter.stones` table and clean up their uniquely identified records. They cover successful creation and five parameterized invalid-input cases. The creation endpoint's failure after insertion but before commit remains deferred. Fresh-database migration application and schema-drift checking are now exercised by the shared container fixtures.

### PY-007 verification evidence

On 2026-10-29, the full suite passed: **24 tests**. Runtime inspection observed a single PostgreSQL target, `localhost:51548/stone_shelter_test`, distinct from the development port `55432`. A temporary in-memory connection guard rejected non-test targets during that verification; it is not a permanent repository feature. The container was removed afterwards. Alembic upgrade and check passed, and mypy passed for 63 source files.

After formatting cleanup, the owner reported that the complete `make check` target passed. The owner then chose to complete PY-007 without further verification runs. A separate run with `.env` absent and development PostgreSQL stopped was not performed and is not claimed as verified. Unit tests separately passed (12 tests) with `DOCKER_HOST` pointing to a nonexistent socket. Fixed example ports in this evidence describe that run only; future test-container ports are dynamic.
