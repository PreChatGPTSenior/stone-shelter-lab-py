# ADR-0013 Register one stone and its complete case per request

- Status: Accepted; DTOs updated, application processing pending
- Date: 2026-10-30
- Tracking: [PY-009](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/10)
- Supersedes: The multi-stone API batch and batch-wide transaction decisions in [ADR-0010](0010-py-009-test-data-preparation.md)
- Preserves: The educational happy-path assumptions, [direct DTO-to-ORM mapping](0011-dto-to-orm-without-domain-dataclasses.md), and [clean Testcontainers policy](0012-clean-testcontainers-only-development.md)

## Context

One pet with its accompanying lifetime case is the business unit delivered by the simulated upstream system. Independent pets do not need to share a request or transaction. The owner prefers individual submissions over a potentially large multi-stone payload, including for synchronization scenarios.

The case can contain accumulated history, not only its admission event. Bound that collection explicitly rather than introducing a multi-stone batch.

## Decision

- Use `StoneRegistrationRequest` as the creation input. Its root contains required `stone` and `shelterCase` objects and an optional `profile`.
- Remove `StoneBatchItemRequest`, `StoneBatchCreateRequest`, and the `items` wrapper. Multi-stone API creation batches are not supported.
- Require `shelterCase.events` to contain between 1 and 100 events inclusive. At least one must be ADMITTED, in any position in the submitted array.
- The upper bound of 100 is a business acceptance rule implemented by a DTO field validator using `PydanticCustomError`, not a generic Pydantic `max_length` constraint. It depends only on the input document and does not require database access or service-layer processing.
- Exceeding the limit produces error type `CASE_EVENT_LIMIT_EXCEEDED`, with structured context `limit` and `actual`.
- Absence of ADMITTED in a nonempty list produces the separate error type `CASE_ADMITTED_EVENT_REQUIRED`, with context `required_event_type: "ADMITTED"`. Position is not checked.
- A missing or empty list remains a normal structural validation failure. For valid event objects, the size validator runs before the admission-presence validator; an oversized list reports the limit error first.
- Pydantic includes these codes and contexts in its validation errors. A future FastAPI `RequestValidationError` handler can translate them into the agreed API error representation. No custom handler is added in this increment; HTTP status and the final response envelope remain separate decisions. The sender can distinguish the two conditions without interpreting message text. Repeating an unchanged oversized request is not a remedy.
- A creation request may carry the case's accumulated coherent history. The existing event types encode status operations and the two shelter-transfer directions; no separate transition or transfer-route fields are added.
- Keep adoption status application-owned. Processing starts from AVAILABLE and uses the supplied history to establish the resulting state; clients do not supply a separate current-status field in the creation DTO. Chronological processing belongs to the future application logic, not array-position validation in the DTO.
- Persist one stone, its case, optional profile, and all supplied case events atomically in one Unit of Work.
- To register multiple stones, the emulator reads separate per-stone fixture files and sends separate requests. Iterating a fixture directory does not create an API batch contract.
- Keep a separate single-case event operation as a future capability for adding later history. Its DTO, name, and limits are not implemented in this creation-only increment; the previously introduced `CaseEventsCreateRequest` has been removed.
- Do not require ADMITTED to be the first array element. Do not add extra lifecycle, ordering, duplicate, or conflict checks beyond the previously agreed happy-path scope.

## Processing boundaries

### Authored stone fixtures

- Store reusable English-language registration data under `fixtures/stones/` at the repository root. These inputs support the upstream emulator and future retrieval experiments, not only automated tests.
- Use one JSON file per stone. Name it `<stone.externalId>.json`; the filename stem must match the UUID inside `stone.externalId`.
- Each file is one complete `StoneRegistrationRequest` with required `stone` and `shelterCase` objects and an optional `profile`. Do not wrap it in an array or an `items` object.
- Include the case's event history in `shelterCase.events`. It must be nonempty, contain ADMITTED in any position, and respect the 100-event business limit.
- Keep case and event UUIDs stable and distinct from the stone UUID. Reference the agreed seeded shelter UUIDs; fixture files do not create shelters implicitly.
- Author coherent fictional-world facts. Admission dates and event times must agree with the described scenario, and any state beyond AVAILABLE must be supported by the corresponding lifecycle history.
- The initial examples are Sir Pebble without a profile and Madame Obsidian with a profile. Both include a case and an ADMITTED event.
- Validate each file against the current DTO and check filename-to-external-ID consistency before using it. Exercise business-rule limits through the custom validation codes agreed above.
- The future emulator reads the directory and sends each file as a separate API request. It must not merge the files into a multi-stone API batch or insert their contents directly through SQL.
- Keep authored fixture files independent of temporary database contents. Reload them into clean Testcontainers databases when persistence scenarios are implemented; no legacy-data migration or preservation is required.
- Creating or validating fixture files does not load them into a database. This ADR does not implement the emulator or reception services.

### Application processing

This decision selects the unit of input and transaction, not a queueing architecture. It does not add a durable queue, workers, an asynchronous acceptance protocol, or receipt/status tracking.

The creation route can use the stone collection without a batch suffix; endpoint wiring and response shape remain separate work. The existing single-case event route remains `POST /api/v1/shelter-cases/{external_case_id}/events`. The earlier proposal for a multi-case event-batch route is not part of the current scope.

For reproducible examples, final states other than AVAILABLE still require coherent event histories explaining them. That history can now accompany creation or be completed through later event requests.

## Consequences

- Payload and transaction boundaries follow one pet and its documents.
- History size has an explicit contract limit. The event-count limit does not by itself define HTTP body-size or text-length limits; those can be agreed separately when needed.
- An error in one request does not roll back unrelated pet registrations.
- Emulator data files remain separate from the shape of an individual API request.
- DTO validation implements the event-count and admission-presence checks with custom codes. It does not implement an HTTP error handler, reception services, ORM mapping, event application, persistence, or an endpoint.
