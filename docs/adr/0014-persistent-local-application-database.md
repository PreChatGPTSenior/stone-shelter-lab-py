# ADR-0014 Separate persistent application data from disposable test databases

- Status: Accepted
- Date: 2026-10-30
- Tracking: PY-010
- Partially supersedes: [ADR-0012](0012-clean-testcontainers-only-development.md)
- Related: [ADR-0013](0013-single-stone-ingestion.md)

## Decision

Use persistent local PostgreSQL from the existing Docker Compose configuration for the application. The application reads the local connection settings from `.env`; the named PostgreSQL volume retains records across restarts.

Continue using clean Testcontainers databases for every database-backed automated test and for migration generation and verification. Supply their settings explicitly and never run test cleanup against the application database.

Local setup consists of starting PostgreSQL, applying Alembic migrations, and seeding the two reference shelters with the UUIDs referenced by authored requests. Shelter seeding creates missing records, skips identical existing records, and rejects conflicting existing reference data without overwriting it. It does not delete data or create stones.

The upstream emulator reads `fixtures/stones/*.json` and sends one complete request per file to `POST /api/v1/stones`. It uses HTTPX, already installed, and does not import the application service, validate requests through server DTOs, or insert stones through SQL. It reports each response and a final success/failure summary; a failed request does not roll back previously successful requests. There are no automatic retries, updates, duplicate suppression, or multi-stone transactions. A timeout is reported as a failure with an uncertain server outcome, not proof of rollback.

Repeated imports are not idempotent: UUID uniqueness constraints remain in force. The current happy-path scope does not add a duplicate-handling HTTP contract. Do not rerun successful files expecting updates or automatic skips. Keep already loaded files separate when submitting further data.

No change to the persistent application database, schema, or volume is performed merely by running tests. Ordinary shutdown and restart preserve records. Local migration conflicts must be reported rather than resolved through automatic deletion or invented compatibility migrations.

## Consequences

- Fictional pet histories can accumulate across local application sessions.
- Test isolation remains independent of locally authored and loaded data.
- Reference shelters are shared fixture data, not test-only payloads.
- Database setup and HTTP loading are explicit commands; neither runs automatically at application startup.
- The project remains a local learning application; production compatibility and backfill work remain outside scope.
