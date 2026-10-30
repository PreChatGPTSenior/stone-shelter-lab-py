# Stone registration scenarios

## Request files

- `fixtures/stones/<stone.externalId>.json`: valid, reusable single-stone registration requests for tests and the future upstream emulator.
- `tests/fixtures/stone-registration/invalid-validation/`: test-only requests rejected by Pydantic before persistence.
- `tests/fixtures/stone-registration/invalid-persistence/`: test-only requests accepted by the DTO but rejected by PostgreSQL constraints.
- `fixtures/shelters.json`: the two existing shelter records seeded into the disposable test database, or explicitly into the persistent local application database; this is setup data, not a registration request.
- `expected-*-errors.json`: expected validation/database error codes kept separately from request bodies. Successful status assertions compare storage with the source-provided adoptionStatus.

Each stone file is one request, without a batch wrapper. Valid filenames match the stone external UUID. Negative files use descriptive names and must never be included in the emulator input directory.

## Valid scenarios

| Stone | Expected status | Events | Profile | Request file |
| --- | --- | --- | --- | --- |
| Brave Gneiss | AVAILABLE | 5 | Present | [3b41b31d-5a1f-43ef-af77-c107bb7ae382](../../fixtures/stones/3b41b31d-5a1f-43ef-af77-c107bb7ae382.json) |
| Sir Pebble | AVAILABLE | 1 | Absent | [49cf225d-800f-4dce-8eb5-af192d2449d5](../../fixtures/stones/49cf225d-800f-4dce-8eb5-af192d2449d5.json) |
| Mossy Limestone | AVAILABLE | 3 | Absent | [4a7ebdcb-0433-4d59-be40-9040e908ba66](../../fixtures/stones/4a7ebdcb-0433-4d59-be40-9040e908ba66.json) |
| Madame Obsidian | AVAILABLE | 1 | Present | [67269139-e8b8-4c7d-aa58-33b88162ec70](../../fixtures/stones/67269139-e8b8-4c7d-aa58-33b88162ec70.json) |
| Sunny Marble | ADOPTED | 2 | Absent | [83a3033b-807e-439e-86e8-2d94769b21ea](../../fixtures/stones/83a3033b-807e-439e-86e8-2d94769b21ea.json) |
| Wandering Sandstone | RESERVED | 3 | Absent | [9c09973a-5ece-4649-8923-eb210dd023ed](../../fixtures/stones/9c09973a-5ece-4649-8923-eb210dd023ed.json) |
| Professor Quartzless | AVAILABLE | 100 | Absent | [abcbd2b8-234c-4653-a9cf-d3c022073750](../../fixtures/stones/abcbd2b8-234c-4653-a9cf-d3c022073750.json) |
| Velvet Slate | RETURNED | 5 | Present | [af5f85d4-9cc7-48a9-a1e6-aad5d8fec581](../../fixtures/stones/af5f85d4-9cc7-48a9-a1e6-aad5d8fec581.json) |
| Homeward Pumice | AVAILABLE | 4 | Present | [d8d61c1e-2f5d-472b-9c57-3c2f67ea0bbf](../../fixtures/stones/d8d61c1e-2f5d-472b-9c57-3c2f67ea0bbf.json) |
| Captain Basalt | RESERVED | 3 | Present | [dfa0ae9a-f070-495f-a489-cf3ecbc1912b](../../fixtures/stones/dfa0ae9a-f070-495f-a489-cf3ecbc1912b.json) |

The histories cover admission, reservation, reservation ending, direct adoption, adoption after reservation, return, readiness after return, meetings, care, observations, and both transfer directions. Velvet Slate has a coherent history supplied in reverse array order; the supplied adoptionStatus is RETURNED and must be preserved independently of event array order. Event timestamps remain historical facts, not a status calculation input. Professor Quartzless has exactly 100 events, the accepted upper boundary. Captain Basalt has an empty optional profile, representing unknown traits and care needs.

Current shelter IDs reference the supplied shelter setup records. Lifetime case numbers retain their original P1 suffix after a transfer to P2. Current shelter is accepted from the request under the agreed consistent-input policy; these tests do not introduce transfer validation.

## Negative scenarios

| File | Expected error |
| --- | --- |
| `invalid-validation/missing-case.json` | `missing` |
| `invalid-validation/missing-adoption-status.json` | `missing` |
| `invalid-validation/unknown-adoption-status.json` | `enum` |
| `invalid-validation/empty-history.json` | `too_short` |
| `invalid-validation/missing-admission.json` | `CASE_ADMITTED_EVENT_REQUIRED` |
| `invalid-validation/too-many-events.json` | `CASE_EVENT_LIMIT_EXCEEDED` |
| `invalid-validation/unknown-stone-type.json` | `enum` |
| `invalid-validation/blank-name.json` | `string_too_short` |
| `invalid-validation/event-without-timezone.json` | `timezone_aware` |
| `invalid-persistence/unknown-shelter.json` | PostgreSQL SQLSTATE `23503` |
| `invalid-persistence/duplicate-event-id.json` | PostgreSQL SQLSTATE `23505` |

The persistence failures exercise existing foreign-key and uniqueness constraints, not new application-level duplicate or conflict handling. Both carry a profile so rollback checks cover all four newly created entity types. Tests first save an unrelated valid stone, then verify a failed registration leaves all entity counts unchanged and preserves the earlier registration.

## Running the scenarios

```sh
uv run pytest tests/integration/catalog/test_register_stone.py
```

Docker must be running for integration tests. They apply Alembic migrations to a fresh Testcontainers PostgreSQL database, seed the two shelters, and send each valid or structurally invalid JSON request through the real FastAPI POST /api/v1/stones endpoint, service, repository, and Unit of Work. The endpoint returns HTTP 201 with only the internal stone id, or HTTP 422 with validation details and the existing custom error codes. Each successful registration is read in a new session with explicit relationship loading, and the stored case status must equal the adoptionStatus supplied in its JSON request. No separate computed-status expectation file is used. Per-test cleanup affects only this disposable database.

The separate rollback test calls the real service directly to inspect the original database error and confirm transaction atomicity. Duplicate DTO-only checks and tests for the previous flat creation contract have been removed. No custom FastAPI exception handler or new persistence-error HTTP policy is introduced.

## Local application loading

The application may retain data in local Docker Compose PostgreSQL under [ADR-0014](../adr/0014-persistent-local-application-database.md). Follow [setup instructions](../setup.md) to apply migrations, run `python -m stone_shelter.tools.seed_shelters`, and start the application. Then `python -m stone_shelter.tools.load_stones` sends the ten valid files through HTTP. No automatic duplicate skipping, retries, or database resets are performed. Automated tests continue to use Testcontainers exclusively.
