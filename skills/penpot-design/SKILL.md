---
name: penpot-design
description: Orchestrate creation or faithful reconstruction of static Penpot screens from URLs, screenshots, code repositories, or a refined prompt, including source traceability, Luna execution, deterministic validation, design-system formalization, and delivery.
metadata:
  short-description: Build and validate Penpot designs from sources or prompts
---

# Penpot Design Orchestrator

Use this as the entrypoint for a request to create screens in the shared Penpot
instance. This skill may be installed through a symbolic link. Resolve its
physical directory first (`pwd -P` or equivalent), derive the repository root
as two parents above that directory, and read the applicable contracts from the
physical `<repository-root>/workflow/` path before acting. Never resolve
`../../workflow/` relative to the logical global symlink.

The skills in `<repository-root>/skills/penpot-intake`, `penpot-source-map`,
`penpot-build`, `penpot-validate`, `penpot-design-system` and `penpot-delivery`
are the authoritative phase instructions. Read the relevant `SKILL.md` directly
from the repository before each phase; they do not need separate global copies.

## Route selection

- Choose `reproduction` when any URL, screenshot, running application, or code
  repository is supplied. Sources can be combined.
- Choose `directed_creation` only when the user explicitly wants creation from
  a prompt with no source.

Run the mandatory interaction in `<repository-root>/workflow/QUESTIONS.md`: ask the initial
questions, ask the second adendo/mudança question, then analyze ambiguities.
Do not construct before material decisions are resolved. Persist every answer,
decision, source, and feedback in the run directory described by
`<repository-root>/workflow/ARTIFACTS.md`.

## Delegation policy

All hands-on work must use `worker_model: gpt-5.6-luna`: source capture,
inspection, MCP construction, correction, token extraction, rendering and
scoring. If Luna is unavailable, stop with `BLOCKED_MODEL_UNAVAILABLE`; do not
silently fall back. Keep the orchestrator focused on routing, user questions,
gate decisions and records.

Follow `<repository-root>/workflow/DELEGATION.md`: create a Codex subagent with
the Luna model for each operational phase and treat quota/model errors as
`BLOCKED_MODEL_UNAVAILABLE`.

## Pipeline

1. `penpot-intake`: collect answers, route, scope and target viewports.
2. `penpot-source-map` for reproduction, or the briefing branch in intake for
   directed creation.
3. Plan screens and hand the plan to `penpot-build` for static frames and
   reusable components through Penpot MCP.
4. `penpot-validate`: render every requested screen/viewport, run the immutable
   deterministic score, and produce side-by-side, overlay, heatmap and issues.
5. If any screen fails `score >= 90`, `coverage >= 80`, or has P0/P1, delegate
   targeted fixes to Luna and repeat validation. Allow at most three internal
   cycles after initial construction; otherwise end `NEEDS_REVIEW`.
6. Obtain formal user approval. In directed creation, user feedback rounds are
   unlimited and each new build starts a fresh three-cycle validation budget.
7. `penpot-design-system`: extract and formalize tokens/styles/components,
   rebuild screens with instances, then revalidate against the approved
   prototype.
8. `penpot-delivery`: package the Penpot link/file, records and visual report.

Use the state names in `<repository-root>/workflow/STATE-MACHINE.md`. Never mark
`DELIVERED` while a viewport or structural design-system gate is failing.
