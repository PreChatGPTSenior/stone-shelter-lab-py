# Requirements and change workflow

OpenSpec CLI: **1.15.0**. Node.js **20.19.0 or later** is required for the npm installation used here. OpenSpec is a development documentation tool, not a Python runtime dependency.

```sh
npm install --global --prefix "$HOME/.local" @fission-ai/openspec@1.15.0
export PATH="$HOME/.local/bin:$PATH"
openspec --version
```

The current machine uses a dedicated npm cache after encountering permissions in the existing shared cache. If needed, add `--cache "$HOME/.cache/stone-shelter-openspec-npm"` to the installation command; no privileged cache changes are required.

## Sources of truth

- [GitHub board](https://github.com/users/PreChatGPTSenior/projects/1/views/1): delivery status.
- GitHub Issues: feature scope, acceptance summary and discussion.
- `specs/`: accepted behavior of implemented capabilities.
- `changes/`: proposed behavior and implementation checklists for active work.
- [ADRs](../docs/adr/README.md): durable architecture decisions and their consequences.
- FastAPI-generated OpenAPI: implemented HTTP schemas, not a separately maintained handwritten contract.

This setup was initialized with `openspec init --tools none --language en`. No agent skills or automatic implementation commands were installed. The owner continues writing code and tests manually.

## Current change

[PY-002: Database support](https://github.com/PreChatGPTSenior/stone-shelter-lab-py/issues/2) is described in [changes/py-002-db-support](changes/py-002-db-support/proposal.md).

```sh
openspec status --change py-002-db-support
openspec validate py-002-db-support --strict
openspec validate --all --strict
```

OpenSpec artifact status reports whether planning documents exist. It does not prove that a database capability is implemented or tested. Every PY-002 implementation task starts unchecked. The board remains In progress.

Do not archive PY-002 or promote its delta into `specs/` until implementation and focused verification are complete and the owner requests archiving. Link future changes to their corresponding issue in both directions. Keep delivery status on GitHub rather than maintaining a second board in Markdown.
