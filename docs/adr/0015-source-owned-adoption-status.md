# ADR-0015 Preserve the source-provided adoption status during registration

- Status: Accepted
- Date: 2026-10-30
- Tracking: PY-010
- Clarifies: [Domain model](../domain/model.md), ShelterCase field ownership
- Partially supersedes: Registration-time status reconstruction in [ADR-0013](0013-single-stone-ingestion.md) and historical initial-state processing in [ADR-0010](0010-py-009-test-data-preparation.md)

## Context

The external operational system supplies a stone and its case. ShelterCase already includes a current adoption_status in the documented entity model. The input DTO incorrectly omitted it and the application calculated it by replaying history. This added an unintended dependence on event occurrence times and mixed snapshot ingestion with application-owned lifecycle actions.

## Decision

- Require `shelterCase.adoptionStatus` in the registration request, validated as AdoptionStatus: AVAILABLE, RESERVED, ADOPTED, or RETURNED. There is no DTO default.
- Copy its enum value into ShelterCaseModel.adoption_status. Store the supplied events independently as related history in the same transaction.
- Do not compute status by sorting events, selecting the latest event, taking array order, or applying an event-to-status lookup.
- Keep the existing event-list rules: 1 to 100 events and at least one ADMITTED anywhere in the array. ADMITTED does not imply that the incoming current status is AVAILABLE.
- Continue to trust internally consistent source data under the educational happy-path scope. Do not add cross-validation between current status and history in this increment.
- Any future application-owned action or state transition must have explicit accepted rules and a separate contract. Imported facts alone do not authorize inventing those rules.
- Record field origins in the domain documentation and reconcile DTOs, JSON fixtures, services, and endpoint tests when the contract changes. Documentation and accepted contracts are authoritative; superseded decisions are historical context.

## Consequences

The lifecycle calculation function and event-to-status dictionary are removed. No database migration is needed because the status column already exists. Existing local records are preserved; this change neither reloads fixtures nor rewrites stored data. Valid fixture histories still explain their declared statuses, but the ingestion service does not reconstruct or validate that relationship.
