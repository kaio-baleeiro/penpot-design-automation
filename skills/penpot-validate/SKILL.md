---
name: penpot-validate
description: Rigorously compare Penpot renders against source evidence or an approved directed-creation prototype using immutable deterministic scoring, visual diffs and targeted Luna refactoring.
metadata:
  short-description: Score, compare and correct Penpot screens
---

# Penpot validation and refinement

Read `../../workflow/CONTRACT.md`, `STATE-MACHINE.md` and `SCORING.md`. This
skill owns `VALIDATING`, `REFACTORING` and `DS_REVALIDATING`.

## Validation pass

For every requested screen and viewport, delegate render/capture work to
`gpt-5.6-luna` and run the deterministic evaluator with
`python3 -m scripts.penpot_validation validate --run-dir <run-dir> --cycle <1..3>`.
Never change its formula, threshold, coverage rule or severity mapping during a
run. A human or language model may
explain a finding but may not override the evaluator.

The CLI writes immutable `cycles/cycle-N/score.json`, `issues.json`, report,
side-by-side, overlay and heatmap artifacts. Check the gate separately per viewport:
`score >= 90`, `coverage >= 80`, no P0/P1. Structural checks must also confirm
components/styles/tokens are actually reusable, not only visually similar.

Each deterministic issue identifies a region/coordinates where available,
expected vs actual, magnitude and evidence. The Luna worker must add likely root
cause and a precise fix in the refactoring handoff without altering the
machine-written score/issues files. Penpot exports are produced through
`scripts/penpot-mcp.sh export --args '<JSON>' --save-image <PNG> --log-path design/penpot-mcp-log.jsonl` (or the
configured `call <tool-name>` operation) before validation.

## Refinement loop

If any gate fails after initial build, delegate targeted fixes to Luna using the
issues as the only change list, then rerun the full evaluator. Increment
`validation_cycle`; maximum is three. Avoid broad redesign when the issue calls
for a local correction. Preserve all score files and reports. After cycle 3,
set `NEEDS_REVIEW` with the best version and explicit remaining issues.

In `directed_creation`, user review rounds are unlimited. Record each feedback
message in `feedback/` and build a new version only after interpreting it;
internal validation still starts at cycle 1 for that version.

If the source is incomplete or comparison is unsafe, request clarification;
do not turn missing evidence into a pass. If Luna is unavailable, stop with
`BLOCKED_MODEL_UNAVAILABLE`.

For the post-componentization pass, provide `--inventory
design/structure-inventory.json`. A visual pass alone cannot enter delivery.
