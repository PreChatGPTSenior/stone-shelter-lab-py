# Stone Shelter Python Backend

The project has a running FastAPI application, validated PostgreSQL settings, an async engine and session factory, an explicit Unit of Work, and an Alembic migration environment. Stone creation is implemented through `POST /api/v1/stones`, returning HTTP 201 with only the generated UUID. Unit and PostgreSQL integration tests cover infrastructure, successful creation, and invalid-input scenarios. Read, update, delete, and adoption workflows are not implemented yet.

Current work: [PY-003 Create stone](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/3), on branch `PY-003-create-stone`. The issue records completed criteria and explicitly deferred verification.

Planning and rationale: [OpenSpec workflow](openspec/README.md), [PY-002 proposal](openspec/changes/py-002-db-support/proposal.md), [architecture decisions](docs/adr/README.md), and [GitHub board](https://github.com/users/PreChatGPTSenior/projects/1/views/1).

## Layout

- `src/stone_shelter/catalog`: specimen properties and catalog operations.
- `src/stone_shelter/adoption`: listings, applications and adoption lifecycle.
- `src/stone_shelter/application`: cross-module use cases and the transaction contract.
- `src/stone_shelter/bootstrap`: application assembly and dependency wiring.
- `src/stone_shelter/api`: cross-module HTTP entry points and error translation.
- `src/stone_shelter/infrastructure/database`: shared database plumbing and Unit of Work implementation.
- `migrations`: Alembic migration environment and revisions.
- `tests`: unit, integration and browser end-to-end tests.
- `docs`: accepted project documents.

## Transaction boundary

The composition root will bind participating adapters and the Unit of Work to one session per use-case execution. The coordinating use case owns commit. Module operations and repositories do not commit independently. Stone properties and adoption listing availability remain separate.

## Local development

See the [local setup instructions](docs/setup.md) for environment configuration, infrastructure startup, migrations, application startup, and development checks.

The owner writes application code and tests manually; OpenSpec is used to record and validate plans, not to authorize automatic implementation.
