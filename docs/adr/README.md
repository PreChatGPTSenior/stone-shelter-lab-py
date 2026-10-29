# Architecture decision records

ADRs record why an architectural choice was accepted, including consequences and implementation scope. **Accepted does not mean implemented.** Supersede decisions explicitly rather than silently rewriting their history.

| Record | Decision | Implementation scope |
| --- | --- | --- |
| [ADR-0001](0001-modular-monolith.md) | Modular monolith and explicit module contracts | Scaffold exists; behavior is incremental |
| [ADR-0002](0002-stone-and-adoption-listing.md) | Separate specimen properties from adoption availability | Separation retained; AdoptionListing design superseded by ADR-0007 |
| [ADR-0003](0003-explicit-unit-of-work.md) | Explicit UoW and per-execution session ownership | Implemented in PY-002; deferred verification is tracked separately |
| [ADR-0004](0004-postgresql-task-queue.md) | PostgreSQL-backed durable tasks instead of Kafka | Deferred until background indexing is in scope |
| [ADR-0005](0005-incremental-manual-development.md) | Incremental, human-written backend with test-based verification | Manual working agreement retained; sequencing partly superseded by ADR-0006 |
| [ADR-0006](0006-rag-and-agent-learning-focus.md) | Prioritize retrieval, RAG, tools, agents, and evaluation; compare later with Spring AI | Accepted direction; detailed future capabilities are not implemented |
| [ADR-0007](0007-lifetime-shelter-case-identity.md) | One lifetime ShelterCase per stone, stable global identity, and explicit adoption states/transitions | Accepted design; return requires review and direct adoption is allowed; persistence and ingestion are not implemented |
| [ADR-0008](0008-external-batch-ingestion-and-partial-updates.md) | External batch creation, timestamp-aware single-stone partial updates, observed history, and no physical deletion | Accepted design; entities and payload details precede search; implementation is pending |
| [ADR-0009](0009-fictional-pet-stone-profiles.md) | Fictional pet-stone profiles, staff-assigned social traits, care/health notes, triggers, wishes and separate compatibility knowledge | Accepted conceptual fields; vocabulary, storage and compatibility content are not implemented |

Tracking: [PY-002](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/2), [OpenSpec proposal](../../openspec/changes/py-002-db-support/proposal.md), [project board](https://github.com/users/PreChatGPTSenior/projects/1/views/1).

Current learning scope and proposed experiments: [RAG learning requirements](../requirements/rag-learning.md).
