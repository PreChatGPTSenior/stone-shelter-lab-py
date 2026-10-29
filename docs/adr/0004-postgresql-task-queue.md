# ADR-0004 PostgreSQL-backed tasks instead of Kafka

- Status: Accepted
- Date: 2026-10-27
- Tracking: [PY-002 architecture context](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/2)
- Implementation: Deferred; no queue or embeddings in current CRUD scope

## Context

Future indexing must not lose the intent to generate an embedding after a successful stone write. The current project does not need Kafka's independent subscribers or replayable distributed event log.

## Decision

When indexing is introduced, persist a durable task in the same PostgreSQL transaction as the relevant business mutation. A separate Python worker will claim work, call the model outside the transaction, and persist the result safely. Use at-least-once processing with idempotency and source-version checks.

Detailed lease, retry, scheduling and failure-state design remains deferred. Kafka is excluded from the selected stack and Compose. Do not implement an in-memory background task as a substitute for durable intent.

## Consequences

No additional broker is required. The future queue must still address crash recovery and duplicate execution. Current Stone creation has no embedding atomicity guarantee because indexing is not yet part of its behavior. Revisit this decision if independent consumers or event replay become real requirements.
