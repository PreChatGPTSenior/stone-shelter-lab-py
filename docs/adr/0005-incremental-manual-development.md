# ADR-0005 Incremental human-written backend

- Status: Accepted
- Date: 2026-10-27
- Tracking: [PY-002](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/2)

Update 2026-10-29: [ADR-0006](0006-rag-and-agent-learning-focus.md) supersedes the CRUD-first sequencing and blanket deferral of answer-quality evaluation below. The original decision is retained as history; the manual implementation agreement remains in effect.

## Context

The owner is an experienced Java engineer learning Python and its frameworks by writing the application manually. The historical product specification is broader than the next useful learning increment.

## Decision

The owner chooses the next scope and writes application code and tests. Assistant work is explanation, review and explicitly requested scaffolding, infrastructure or documentation. Installing OpenSpec does not authorize automatic code implementation.

Proceed through database support and simple Stone create/read/delete/update. The initial list endpoint returns all stones without search or pagination. Verify the API and persistence through tests. PostgreSQL is the only required service for this stage; existing Redis and MinIO Compose definitions do not make them application dependencies.

Defer UI integration, authentication, adoption workflows, photos, indexing and Redis integration. Search and LLM search follow CRUD. LangChain and LangGraph are accepted later learning goals. Hypothesis, free-form LLM answer-quality evaluation and true token streaming remain explicit future work; do not install their tooling now.

## Consequences

Do not claim full compatibility with the existing UI or full delivery of the historical product specification. Adopt historical requirements deliberately when relevant. Keep active scope on GitHub, proposed guarantees in OpenSpec and durable rationale in ADRs.
