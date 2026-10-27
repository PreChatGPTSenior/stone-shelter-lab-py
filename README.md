# Stone Shelter Python Backend

The project has a running FastAPI bootstrap, a generated OpenAPI endpoint and its first integration test. Python dependencies and development checks are managed through uv. Business CRUD and application database wiring are not implemented yet.

Current work: [PY-002 Database support](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/2), on branch `PY-002-db-support`.

Planning and rationale: [OpenSpec workflow](openspec/README.md), [PY-002 proposal](openspec/changes/py-002-db-support/proposal.md), [architecture decisions](docs/adr/README.md), and [GitHub board](https://github.com/users/PreChatGPTSenior/projects/1/views/1).

## Layout

- `src/stone_shelter/catalog`: specimen properties and catalog operations.
- `src/stone_shelter/adoption`: listings, applications and adoption lifecycle.
- `src/stone_shelter/application`: cross-module use cases and the transaction contract.
- `src/stone_shelter/bootstrap`: application assembly and dependency wiring.
- `src/stone_shelter/api`: cross-module HTTP entry points and error translation.
- `src/stone_shelter/infrastructure/database`: shared database plumbing and Unit of Work implementation.
- `migrations`: future Alembic migration environment and revisions.
- `tests`: unit, integration and browser end-to-end tests.
- `docs`: accepted project documents.

## Transaction boundary

The composition root will bind participating adapters and the Unit of Work to one session per use-case execution. The coordinating use case owns commit. Module operations and repositories do not commit independently. Stone properties and adoption listing availability remain separate.

## Local development

```sh
uv sync --locked
uv run uvicorn stone_shelter.main:app --reload --host 127.0.0.1 --port 8000
```

The bootstrap serves `/docs` and `/openapi.json`. It does not yet connect to PostgreSQL. Infrastructure setup is documented in [infra/README.md](infra/README.md).

```sh
uv run ruff check .
uv run ruff format --check .
uv run mypy
uv run pytest tests/integration/test_application.py
```

The existing formatter findings remain separate from this documentation change. The owner writes application code and tests manually; OpenSpec is used to record and validate plans, not to authorize automatic implementation.
