# Architecture decision records

ADRs record why an architectural choice was accepted, including consequences and implementation scope. **Accepted does not mean implemented.** Supersede decisions explicitly rather than silently rewriting their history.

| Record | Decision | Implementation scope |
| --- | --- | --- |
| [ADR-0001](0001-modular-monolith.md) | Modular monolith and explicit module contracts | Scaffold exists; behavior is incremental |
| [ADR-0002](0002-stone-and-adoption-listing.md) | Separate specimen properties from adoption availability | Future adoption design; not part of current CRUD |
| [ADR-0003](0003-explicit-unit-of-work.md) | Explicit UoW and per-execution session ownership | To be implemented in PY-002 |
| [ADR-0004](0004-postgresql-task-queue.md) | PostgreSQL-backed durable tasks instead of Kafka | Deferred until background indexing is in scope |
| [ADR-0005](0005-incremental-manual-development.md) | Incremental, human-written backend with test-based verification | Current working agreement |

Tracking: [PY-002](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/2), [OpenSpec proposal](../../openspec/changes/py-002-db-support/proposal.md), [project board](https://github.com/users/PreChatGPTSenior/projects/1/views/1).
