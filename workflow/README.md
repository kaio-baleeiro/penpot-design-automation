# Workflow controller

The machine-readable contract is enforced by `./penpot-workflow`. Start clients
with `./agent codex|claude|devin|gemini`. Each launch creates a fresh pending
session and asks the user whether to prepare infrastructure or work on designs.

After the answer, record the exact response:

```sh
./penpot-workflow select design --user-answer "<verbatim answer>"
```

The infrastructure choice instead uses `select infrastructure` and
`./penpot-workflow bootstrap-infra`, which starts Penpot, provisions a local
account and MCP key, and saves secrets in the ignored root `.env`.

Design runs are created through `new-run` and state transitions pass only when
required artifacts validate. A worker must open a representative image, record
what it saw and its SHA-256. This is an auditable attestation, not proof of the
model's internal perception. A raw arbitrary CLI that ignores project rules
cannot be forced to comply; the supported entrypoint is `./agent`.
