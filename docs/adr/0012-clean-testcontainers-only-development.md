# ADR-0012 Use only clean Testcontainers databases during local development

- Status: Partially superseded by [ADR-0014](0014-persistent-local-application-database.md); Testcontainers isolation remains required for tests and schema verification
- Date: 2026-10-30
- Tracking: [PY-009](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/10)
- Related: [ADR-0010](0010-py-009-test-data-preparation.md) and [ADR-0011](0011-dto-to-orm-without-domain-dataclasses.md)
- Scope: Database-backed development, schema generation, migration verification, and tests

## Policy update

The owner now permits a persistent local application database and explicitly requested retaining data between application restarts. ADR-0014 governs application setup and fixture loading. The original decision below is retained as historical context; it no longer prohibits the application from using local PostgreSQL.

## Context

Stone Shelter is a single-developer learning project used and checked locally on the owner's machine. Git commits preserve development work; they do not represent deployed installations or compatibility promises to external consumers. The features currently being developed are not integrated with other systems.

The current goal is to understand DTOs, ORM relationships, migrations, and transactions using coherent happy-path data. Designing migration paths for previously populated installations would add unrelated work.

## Decision

Until the owner explicitly requests a different policy:

- Use clean, disposable PostgreSQL databases created through Testcontainers for database-backed work.
- Start schema verification from an empty database and reload representative data as needed. Preserve the source JSON fixtures and code, not the contents of a previous temporary database.
- Prefer recreating the temporary database over migrating old application data.
- Do not implement data transfer, backfills, compatibility adapters, transitional schemas, staged production upgrades, or rollback procedures intended to preserve an existing installation.
- Do not infer such requirements from the presence of earlier migrations, local database containers, Git history, or old test records.
- Use Alembic to create and verify the current schema on an empty database. Revisions must form a valid schema-building sequence, but no production data-preserving upgrade path is required.

### Connection targets and existing tooling

Provide the Testcontainers connection settings explicitly for generation and verification. Do not assume that the default settings loaded from `.env` point to an authorized disposable database.

The current Alembic environment still reads application database settings. Any tooling needed to direct migration generation to a temporary container is separate implementation work; this ADR does not claim that the flow has already been adapted.

Do not run database commands against a persistent local development instance as a substitute for the container flow. Existing persistent databases and volumes are not deletion targets under this policy.

### Learning quality

This decision limits deployment and compatibility scope. It does not remove structural validation, database constraints, transaction boundaries, or explicitly selected learning exercises such as optimistic locking.

Tests should verify the agreed behavior on fresh databases. Creating valid foreign keys, preserving atomic writes, and ensuring that the schema matches ORM declarations remain part of the work.

## Consequences

- Schema and fixture iteration can remain focused on the current model without invented legacy-data scenarios.
- Migration generation and verification must use container-specific settings rather than an implicit development database target.
- No old-data mapping is needed merely to add a required field to a table that will be created empty for verification.
- Existing code, migration files, test fixtures, and documentation may need explicit follow-up adjustments. Recording this policy does not authorize or perform those changes.
- If persistent deployments or integrations become relevant later, the owner must explicitly change the policy before compatibility and data-preserving migration requirements are introduced.
