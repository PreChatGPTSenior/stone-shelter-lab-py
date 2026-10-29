# ADR-0001 Modular monolith with explicit module contracts

- Status: Accepted
- Date: 2026-10-27
- Tracking: [PY-002](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/2)

## Context

Stone Shelter is one Python backend maintained as a learning project. It needs clear ownership without separate deployments, packages or infrastructure for every business capability.

## Decision

Use one uv-managed project with a `src/stone_shelter` import package. Group business code by capability, initially catalog and later adoption. Keep domain, application, persistence and HTTP responsibilities identifiable inside each module. Expose intentional module contracts rather than importing another module's private ORM implementation.

Place cross-module orchestration in the shared application layer and dependency assembly in bootstrap. Shared database plumbing does not own business repositories. Avoid cyclic module dependencies. Introduce deeper package structure only when actual responsibilities require it.

## Consequences

Modules can participate in one PostgreSQL transaction without being separate services. Python imports do not enforce architectural boundaries; review and focused checks must preserve them. A package scaffold is not evidence that its business capability exists.

## Alternatives

Global technical-layer folders would scatter each business capability across the project. Separate distributions or microservices would add lifecycle and deployment costs without a present requirement.
