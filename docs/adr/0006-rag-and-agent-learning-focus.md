# ADR-0006 Prioritize retrieval, RAG, tools, and agent workflows

- Status: Accepted direction; implementation is incremental
- Date: 2026-10-29
- Supersedes: the CRUD-first sequencing and deferred answer-evaluation scope in [ADR-0005](0005-incremental-manual-development.md)
- Preserves: manual learning, explicit authorization for assistant code changes, modular boundaries, and transaction ownership
- Requirements and learning backlog: [RAG learning requirements](../requirements/rag-learning.md)

## Retrieval backend refinement

[ADR-0016](0016-typesense-lexical-qdrant-vector-experiments.md) selects Typesense for lexical retrieval and Qdrant for vectors, with Python fusion and an incremental experiment plan. This is accepted direction only; no search or provider integration is installed by that documentation change.

## Context

The owner has approximately fifteen years of Java and enterprise engineering experience. Database configuration, async sessions, transaction ownership, migrations, repository wiring, HTTP contracts, and scenario tests have now been explored in Python. Continuing through a complete CRUD interface or another object-storage photo upload would largely repeat familiar engineering tasks with different syntax.

The learning objective is shifting toward unfamiliar capabilities: retrieval, embeddings, RAG, tool calling, LangChain, LangGraph, evaluation, and a reproducible experiment harness. A later implementation of the same RAG behavior using Spring AI will support a meaningful comparison between the Python and Java ecosystems.

## Implemented baseline

- PY-001: application scaffold, uv, development tooling, and local infrastructure.
- PY-002: validated database settings, async SQLAlchemy engine and sessions, explicit UoW, application lifespan, and Alembic. Merged into master in `fcc427d`.
- PY-003: stone creation through HTTP, a UUID domain model, SQLAlchemy persistence in `stone_shelter.stones`, explicit commit, and an ID-only HTTP 201 response. Merged into master in `1d21252`.
- Verification at the end of PY-003: 24 tests passed, Ruff and mypy passed, and Alembic reported no schema differences. This is recorded evidence from that verification, not a perpetual guarantee.
- The English stone encyclopedia was imported unchanged from the Java repository, with provenance, in `67758a2`.
- Read, Delete, Update, supplier ingestion, trigger data, retrieval, embeddings, and agent workflows are not implemented at this decision point.

Deferred verification remains deferred: the creation endpoint's failure after insertion but before commit, migration execution against a fresh isolated database, and the earlier multi-participant/two-UoW isolation scenarios are not claimed as covered.

## Decision

### Learning scope

Retrieval and assistant behavior become the main learning track. Completing CRUD, photo storage, adoption, and a full UI is no longer a prerequisite. [ADR-0008](0008-external-batch-ingestion-and-partial-updates.md) supersedes the earlier independent Delete plan: retain stones and update state instead. Other catalog operations are introduced when needed by the assistant and its tools. A plain catalog view may exist without user-facing search controls; the assistant is the primary interface for expressing search and filtering intent.

### Data ownership

Stones and accounting data arrive from a simulated external integration service in batches. JSON fixtures and a sending script will call our ingestion API rather than populate tables directly. Users are not expected to create specimens manually through a product form. The existing creation implementation remains a reusable persistence foundation, not a commitment to a manual-entry UI.

[ADR-0007](0007-lifetime-shelter-case-identity.md) refines this direction into a staff-facing hub for two shelters, with shelter addresses and a single globally identified lifetime case per stone. Case UUID and searchable case number come from an external identity service; returns and transfers preserve them. The accepted lifecycle uses UNDER_REVIEW, AVAILABLE, RESERVED and ADOPTED: a return requires review, and direct adoption from AVAILABLE is allowed. Implementation and remaining transfer/import rules are future work.

Keep two information sources distinct: individual catalog specimens in PostgreSQL and curated type-level knowledge in the encyclopedia. ADR-0008 accepts external Stone UUIDs, batch creation, single-stone partial updates ordered by source time, local change history, and simple database-backed shelters. Batch atomicity, timestamp edge cases and exact DTOs remain open. Establish entities and basic population before discussing search behavior.

### Constraints and playful properties

The domain is a fictional world in which stones are pets, not a scientifically realistic rock-care system. [ADR-0009](0009-fictional-pet-stone-profiles.md) accepts staff-assigned socialization traits as an enum set, a care category with a separate health description, free-text triggers/experiences, free-text wishes for the future family, and a separate authored fictional compatibility document.

Keep geological source material, individual fictional profile facts, and shared game/world rules distinguishable. A fear of water can be valid fictional profile data without a geological explanation. Missing knowledge does not imply suitability, and the assistant must not invent individual characteristics or present game rules as scientific facts. Exact vocabulary and storage remain unimplemented.

### Retrieval and orchestration

Use precise database filtering for structured constraints and retrieval for textual knowledge. Embeddings are not a replacement for exact filters or a source of truth. LangChain and LangGraph are both intended learning targets: integrations, retrieval and tools for the former, and explicit state, branching, clarification, bounded retries and resumption for the latter.

The assistant will combine knowledge lookup and catalog tools to select real specimens and explain recommendations with sources. The graph, tool schemas, ranking rules, models, and endpoints will be selected incrementally from concrete scenarios.

### Model providers

Use both local Ollama and OpenRouter for model experiments. The owner has OpenRouter credentials and intends to compare multiple models; experiments are not limited to local inference. Specific OpenRouter models and the LangChain integration package remain implementation-time choices after checking compatibility with the actual project stack.

Read credentials from environment configuration, using `OPENROUTER_API_KEY` for OpenRouter. Do not commit credentials or include authorization headers in traces. This decision does not configure credentials, install integrations, or authorize a paid experiment without a concrete run configuration and budget.

### Observability and selection traces

Select **Langfuse Cloud, Hobby plan** as the initial hosted observability platform. Use one primary LLM tracing destination rather than configuring LangSmith alongside it. Langfuse is selected because it supports the planned LangChain/LangGraph instrumentation and a later Spring AI comparison through OpenTelemetry.

One assistant turn or evaluation case has a root trace with child observations for interpretation, retrieval, catalog tools, candidate checks, generation, and evaluation. Associate related turns with a session/conversation identifier. Record explicit selection decisions, exclusion reason codes and supporting evidence, not just prompts and model responses. Automatic framework callbacks must be supplemented by application observations for deterministic filters and business decisions.

The trace is evidence of observable execution, not access to the model's private reasoning. Model-authored explanations remain outputs to evaluate against tool results, constraints and sources.

Retain experiment configurations, case results, usage summaries and trace references locally as well, so long-term comparisons do not depend on the hosted plan's history window. Cloud tracing sends captured content to Langfuse; enable content capture deliberately, omit credentials, and apply masking where appropriate. No account, SDK, exporter or integration is provisioned by this ADR update.

### Usage accounting and experiment budgets

Record provider-reported input/output usage for every model invocation, including routing, query rewriting, answer generation, retries and LLM judges. Account for corpus embedding and query embedding separately from generation. If provider usage or cost is unavailable, record it as unknown or explicitly estimated rather than zero. Ollama has no per-token API bill, but its tokens, calls and elapsed time still consume experiment resources.

Set limits at case and experiment level: calls, tool calls, retries, output size, elapsed time, token usage and, for paid providers, money. Keep judge/evaluation expenditure visible as a separate budget category. The runner enforces limits before starting further work and bounds provider calls; Langfuse dashboards and alerts are observability, not the spending control mechanism. Estimates require a reserve for outstanding requests and are not a guarantee of exact provider billing.

Keep regular `make check` independent of live model calls. Run live smoke checks and full experiments explicitly with a selected dataset, models, repetitions and budget. Budget exhaustion is a separate outcome from a wrong answer. Start with a simple measured call and local usage records before adding a large harness.

### Evaluation and comparison

Evaluation of free-form answers is now an intended part of the learning track, replacing its earlier blanket deferral. Begin with a small question set and expected evidence, then separately evaluate retrieval, candidate selection, tool use, and generated explanations. Evaluation tools are not installed merely by accepting this direction.

Compare the same corpus, questions, models, chunking, retrieval settings, and behavioral criteria when implementing the later Spring AI version. A full-context baseline and general-versus-domain-model comparisons are proposed experiments, not claims that a specialized model will perform better.

## Consequences

- Existing UI contracts are references rather than acceptance gates. Numeric IDs and full creation responses are already intentionally superseded by UUID and ID-only creation output.
- Keep Stone properties separate from adoption/accounting state. ADR-0007 replaces AdoptionListing with ShelterCase; lifecycle data is now planned for staff recommendations. Implementing statuses and allowing chatbot-driven lifecycle writes are separate future decisions.
- Redis, photos, Kafka, authentication, token streaming, and a full UI are not required for the first RAG increment.
- Retain the PostgreSQL durable-task direction in ADR-0004 for future indexing. Its worker and queue design is still deferred until indexing is implemented.
- Prefer a few informative scenario tests and evaluation datasets to tests of each intermediate implementation step. Existing deferred tests are not silently marked complete.
- The owner continues to write application code manually unless explicitly delegating a change. Later assistant implementation of deferred tests is authorized for later work, not for this documentation update.
- Acceptance of a learning backlog does not authorize installing every library, creating every table, changing board status, or implementing every proposed exercise immediately.
- Langfuse Cloud Hobby is selected but not connected; OpenRouter and Ollama remain planned experiment providers. No live LLM calls, tracing exports, accounts or paid services are activated by the documentation change.

## Alternatives considered

- Complete CRUD, photo upload, and the original UI first: postpones the capabilities that now motivate the project.
- Replace exact filtering with vector search everywhere: obscures deterministic constraints and makes selection harder to verify.
- Introduce a full agent stack before a baseline: makes it difficult to attribute improvements or failures to retrieval, generation, tools, or orchestration.
- LangSmith was considered for native LangGraph tracing; Langfuse is selected as the initial shared destination for the planned Python and Spring AI experiments.
- Self-host Langfuse immediately: deferred in favor of the Hobby cloud plan to avoid adding infrastructure before the first model integration.

## References

- [Langfuse pricing](https://langfuse.com/pricing): checked on 2026-10-29; Hobby was free without a credit card, with 50,000 units/month, 30 days of data access, and two users. These are dated plan details, not permanent limits or model-token allowances; recheck before onboarding or upgrading.
- [LangChain and LangGraph tracing](https://langfuse.com/integrations/frameworks/langchain).
- [Spring AI integration through OpenTelemetry](https://langfuse.com/integrations/frameworks/spring-ai).
- [Langfuse usage and cost tracking](https://langfuse.com/docs/observability/features/token-and-cost-tracking).
