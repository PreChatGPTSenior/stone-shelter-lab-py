# PY-002 implementation checklist

Issue: [PY-002](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/2). Branch: `PY-002-db-support`.

This checklist records the manually implemented database infrastructure and remaining work. Checked items reflect reviewed files and the owner's reported verification results. Deferred work remains unchecked.

## 1. Configuration and resource lifecycle
- [x] 1.1 Define validated database settings and deliberate local environment loading; cover invalid configuration and secret handling.
- [x] 1.2 Configure the async engine and session factory without opening connections at import or factory-construction time.
- [x] 1.3 Connect engine lifetime to application lifespan and verify cleanup while retaining the factory-only OpenAPI test.

## 2. Explicit Unit of Work
- [x] 2.1 Define the transaction contract and SQLAlchemy implementation with explicit commit and rollback on uncommitted exit.
- [ ] 2.2 Assemble UoW and persistence participants around one session per execution; release sessions reliably. **Partially implemented:** UoW session ownership, active-session access, and cleanup are implemented and tested. Wiring real persistence participants is deferred until their operations exist.
- [x] 2.3 Verify authenticated PostgreSQL connectivity, commit, normal-exit rollback, exception rollback and commit failure reporting.
- [ ] 2.4 Verify independent sessions and atomic rollback across two participants using isolated test data. **Deferred:** by the owner's decision, test multi-participant atomicity using real persistence operations when they exist. The separate independence scenario for two UoW executions has not been verified; reading committed data through a verification session does not complete that scenario.

## 3. Migration environment
- [x] 3.1 Define the shared declarative base and configure Alembic with settings-backed connectivity and metadata.
- [x] 3.2 Verify revision inspection on the isolated database without creating business tables or enabling automatic startup migrations.

## 4. Review and handoff
- [x] 4.1 Document the implemented connection, migration and focused test commands without credentials. See [local setup instructions](../../../docs/setup.md).
- [x] 4.2 Run Ruff lint/format checks, mypy and the relevant focused tests; record real outcomes. The owner reported successful Ruff lint and format checks, mypy, and the full pytest suite. The owner also verified Alembic upgrade, downgrade, and re-upgrade against local PostgreSQL. Exact test counts were not recorded.
- [ ] 4.3 Review the implementation against the database-support requirements and update GitHub issue status when appropriate.

## Handoff notes

- Explicit commit, normal-exit rollback, and exception rollback are covered by PostgreSQL integration tests with disposable technical tables.
- Commit failure propagation and cleanup are covered by a mock-based unit test, not a real database commit failure test.
- Multi-participant atomicity remains deferred as described above; PY-002 is not marked fully complete by this documentation update.
- GitHub issue status is unchanged. No commit or merge is included in this documentation update.
