# Stone Shelter Python Backend

This branch contains a documentation-only Python project scaffold.
No application behavior, domain entities, dependencies or tools are implemented or configured yet.

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

## Future setup

Populate `pyproject.toml` when configuring the project. Generate `uv.lock` with uv after dependencies are selected and resolved; a fabricated lockfile is intentionally not included. Add runnable setup and test instructions here when implementation begins.
