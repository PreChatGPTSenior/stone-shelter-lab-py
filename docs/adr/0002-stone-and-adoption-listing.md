# ADR-0002 Separate Stone from adoption availability

- Status: Accepted
- Date: 2026-10-27
- Tracking: [PY-002 architecture context](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/2)
- Implementation: Deferred; not part of PY-002 through PY-006

Update 2026-10-29: [ADR-0007](0007-lifetime-shelter-case-identity.md) replaces the proposed AdoptionListing with a lifetime ShelterCase and settles case identity across returns and transfers. The separation of Stone properties from adoption/accounting state remains accepted. The original proposal below is retained as history.

## Context

A stone is a specimen with its own properties. Availability for adoption belongs to a shelter process, and a reservation application has its own lifecycle.

## Decision

Catalog owns Stone and its specimen properties. Adoption will own AdoptionListing, referencing a stone and carrying adoption availability, and AdoptionApplication, representing an individual request. Stone does not contain adoption status. Current HTTP CRUD will not add a synthetic status field.

When adoption enters scope, a shared registration use case may create Stone and AdoptionListing in one transaction if the selected business rule requires immediate listing. Adoption reservations will change listing and application state without changing Stone properties. Public read DTOs may combine data from both modules.

## Consequences

The current CRUD can be implemented without adoption tables. The wire representation need not mirror domain entities. Whether stones may exist without listings, and whether a future relisting creates a new listing, must be settled when adoption is implemented. Cross-module creation is not authorized by this ADR alone.

## Alternatives

Keeping adoption status directly on Stone mixes specimen and shelter-process responsibilities. Deriving all current state from a full event history would add an unrequested event-sourcing model.
