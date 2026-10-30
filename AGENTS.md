# Agent instructions

## README ownership

- Never create, edit, overwrite, move, rename, or delete a `README` file, including `README.md`, anywhere in this repository. README content is maintained exclusively by the project owner.
- Do not modify README files through formatters, generators, automated fixes, or other indirect operations.
- Put agent-authored documentation in a separate, appropriately named file under `docs/`. Do not add links or summaries to README files.

## Check the project before proposing changes

- Before recommending technologies or implementation approaches, inspect the current dependencies in `pyproject.toml`, the relevant source files, and accepted project decisions.
- Base advice on what is actually installed and implemented. Do not assume that a planned dependency or documented capability already exists.
- Prefer idiomatic Python and established practices for the libraries used in this project. Use Java comparisons to explain concepts, not as a reason to reproduce Java architecture automatically.

## Learning and collaboration

- The owner writes application code and tests to learn Python hands-on. Explain, provide examples, and review the owner's work; edit application code or tests only when explicitly requested.
- Treat the owner as an experienced Java senior engineer and architect with 15 years of experience. Explain unfamiliar Python syntax carefully without repeating basic software engineering concepts unnecessarily.
- Work in small, coherent steps. Provide the next actionable step and explain unfamiliar syntax in examples rather than overwhelming the owner with an entire implementation.
- Before introducing a layer, interface, DTO, abstraction, or dependency, explain its concrete value for the current task or an explicitly agreed learning objective.

## Repository language and decisions

- Write repository documentation, code comments, example data, issue descriptions, and commit messages in English.
- Distinguish accepted decisions from proposals, open questions, and deferred work. Do not turn a discussed option into a requirement without agreement.
- Preserve the agreed scope. Add technologies and infrastructure when their corresponding task is in scope; documenting a future capability does not authorize implementing it.

## Testing

- Prefer meaningful scenario and integration coverage over tests for every field, framework setting, or intermediate implementation step.
- Run database integration tests through Testcontainers. Do not point them at the local development database.

## Temporary database-only development policy

- Until the owner explicitly changes this policy, use only clean, disposable databases provisioned through Testcontainers for database-backed development, schema generation, migration verification, and tests.
- Do not run these operations against an existing local development database or assume that a database selected by `.env` is an authorized target. Supply the container connection settings explicitly.
- Treat the project as a local, single-developer learning application with no deployed installations or external consumers requiring compatibility.
- Prefer recreating the disposable database and reloading prepared data. Do not introduce legacy-data transfer, backfills, transitional schemas, production rollout procedures, or backward-compatibility flows.
- Use Alembic to build and verify the current schema from an empty database. Do not add data-preserving upgrade scenarios merely because older migrations or Git commits exist.
- This policy does not authorize deleting persistent databases or volumes. It applies to disposable Testcontainers resources and does not authorize unrelated code or migration edits.
- See [ADR-0012](docs/adr/0012-clean-testcontainers-only-development.md). Existing tooling may still need adjustment; documentation of this policy does not mean that adjustment is implemented.

## Domain premise

- This is a fictional world where stones are pets. Their personalities, traumatic experiences, health needs, and preferences are legitimate domain data.
- Do not reject agreed fictional properties merely because real stones do not have them. Preserve the distinction between authored world facts and geological reference material.

## Git operations

- Do not commit, push, or merge without an explicit request. Permission to edit a file does not itself authorize these Git operations.
