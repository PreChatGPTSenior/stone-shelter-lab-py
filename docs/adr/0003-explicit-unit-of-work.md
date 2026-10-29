# ADR-0003 Explicit Unit of Work and session ownership

- Status: Accepted
- Date: 2026-10-27
- Tracking: [PY-002](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/2)
- Implementation: Planned in [database-support](../../openspec/changes/py-002-db-support/proposal.md)

## Context

Multiple persistence operations may need to succeed or fail together. A central UoW exposing every module's repository would couple transaction management to the entire domain.

## Decision

Define a small application-level UoW contract and implement it using SQLAlchemy in shared database infrastructure. The UoW knows transaction and session lifecycle, not catalog or adoption repositories.

The outer use case owns the explicit commit decision. Composition binds its UoW and participating adapters to the same AsyncSession. Repositories may flush but do not commit. Exiting without a successful commit triggers rollback and cleanup. Each independent execution receives a separate session; concurrent tasks must not share a mutable AsyncSession.

Engine and session factory may have application lifetime. Database connections must not be opened as import side effects. External network work such as model calls or object transfers stays outside long-held database transactions.

## Consequences

Atomicity across modules is possible within the monolith. Shared participation is explicit wiring rather than Spring-style implicit transaction propagation. Tests must verify shared rollback, independent sessions and cleanup. Nested transactions and distributed transactions are not introduced by this decision.

## Alternatives

Repository-level commits break use-case atomicity. A global session breaks concurrent isolation. A repository-owning central UoW accumulates module coupling.
