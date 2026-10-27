# PY-002 implementation checklist

Issue: [PY-002](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/2). Branch: `PY-002-db-support`.

This checklist tracks future human implementation. Preparing these documents does not complete any item below.

## 1. Configuration and resource lifecycle
- [ ] 1.1 Define validated database settings and deliberate local environment loading; cover invalid configuration and secret handling.
- [ ] 1.2 Configure the async engine and session factory without opening connections at import or factory-construction time.
- [ ] 1.3 Connect engine lifetime to application lifespan and verify cleanup while retaining the factory-only OpenAPI test.

## 2. Explicit Unit of Work
- [ ] 2.1 Define the transaction contract and SQLAlchemy implementation with explicit commit and rollback on uncommitted exit.
- [ ] 2.2 Assemble UoW and persistence participants around one session per execution; release sessions reliably.
- [ ] 2.3 Verify authenticated PostgreSQL connectivity, commit, normal-exit rollback, exception rollback and commit failure reporting.
- [ ] 2.4 Verify independent sessions and atomic rollback across two participants using isolated test data.

## 3. Migration environment
- [ ] 3.1 Define the shared declarative base and configure Alembic with settings-backed connectivity and metadata.
- [ ] 3.2 Verify revision inspection on the isolated database without creating business tables or enabling automatic startup migrations.

## 4. Review and handoff
- [ ] 4.1 Document the implemented connection, migration and focused test commands without credentials.
- [ ] 4.2 Run Ruff lint/format checks, mypy and the relevant focused tests; record real outcomes.
- [ ] 4.3 Review the implementation against the database-support requirements and update GitHub issue status when appropriate.
