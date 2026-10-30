# ADR-0011 Map validated DTOs directly to ORM entities

- Status: Accepted; application refactoring is pending
- Date: 2026-10-30
- Tracking: [PY-009](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/10)
- Related: [ADR-0001](0001-modular-monolith.md), [ADR-0003](0003-explicit-unit-of-work.md), and [ADR-0010](0010-py-009-test-data-preparation.md)
- Refines: The implementation layering of ADR-0001. Explicit module responsibilities remain; a separate persistence-independent entity class is not required for each ORM entity.

## Context

The current learning increment accepts consistent upstream data and persists related stones, optional profiles, lifetime cases, and life events. Its focus is Pydantic DTOs, SQLAlchemy relationships, Alembic migrations, batch processing, and coordinated transactions.

The existing creation path constructs a domain Stone dataclass and then copies its fields into a SQLAlchemy StoneModel. Expanding this pattern would duplicate each new entity and introduce mappings without a present need for a persistence-independent domain representation.

Neither Python nor SQLAlchemy requires this additional representation. The domain concepts and their ownership remain important, but they do not require two parallel sets of entity classes.

## Decision

Use the following application flow:

1. Validate incoming transport data with Pydantic DTOs.
2. Let application services construct or update SQLAlchemy ORM entities from that data, including related entities.
3. Use repositories for persistence operations and queries where useful.
4. Keep Unit of Work and explicit application-owned transaction boundaries.

Do not introduce or continue expanding separate domain dataclasses that mirror the ORM entities for this increment. Existing domain dataclasses and their consumers will be refactored in a subsequent, explicitly scoped code change; this ADR does not remove or alter them.

### Responsibilities retained

| Responsibility | Location |
| --- | --- |
| Input structure, field types, and request validation | Pydantic DTOs |
| Use-case orchestration and construction of related entities | Application services |
| Tables, columns, foreign keys, and object relationships | SQLAlchemy ORM entities |
| Persistence operations and queries | Repositories or focused query components |
| Commit, rollback, session lifetime, and shared transactions | Application orchestration with Unit of Work |
| Referential integrity, uniqueness, and required columns | Database constraints |

Keep the catalog and adoption capability boundaries and the agreed entity relationships. Preserve the agreed enum vocabularies; enums do not need to be removed merely because the dataclass entity layer is removed. Their exact file placement can be settled during refactoring.

DTOs and ORM entities remain distinct: request shape is not dictated by table layout. One batch item may create a Stone, its ShelterCase, and an optional StoneProfile. Direct mapping means no intermediate duplicate entity representation, not blindly assigning every incoming field to an ORM object. Select the intended fields and relationships explicitly.

Mapping can happen in service code or a small mapping function. A separate mapper class, command DTO, or generic mapping framework is not required without a concrete benefit.

Services and Unit of Work remain. Repositories do not independently commit each item: a creation batch uses one shared transaction, and an event operation persists its events and applicable state changes atomically. The educational happy-path assumptions and deferred hardening in ADR-0010 remain unchanged.

## Consequences

- Fewer parallel models and fewer field-copying steps are required before learning ORM relationships and implementing ingestion.
- Application services may depend on ORM entities. Persistence independence is not an objective of this increment.
- Domain behavior can later be implemented in entity methods or services as appropriate; removing duplicate dataclasses does not remove business rules or module ownership.
- Separate domain models may be reconsidered if a concrete need appears, such as substantially different business and storage structures or persistence-independent behavior with a demonstrated benefit. Complexity alone does not automatically require duplicated entities.
- This decision does not merge API contracts with ORM models, expose ORM entities directly as HTTP responses, remove repositories or Unit of Work, or authorize application edits.

## Alternatives

Retaining separate dataclasses would provide a place for persistence-independent behavior, but currently adds duplicated state and conversions without enough benefit for the agreed ingestion exercise. Revisit the tradeoff when an actual requirement justifies that cost.
