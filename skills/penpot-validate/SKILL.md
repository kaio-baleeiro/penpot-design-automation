---
name: penpot-validate
description: Rigorously compare editable Penpot renders against source evidence or an approved prototype with immutable per-viewport scoring (>=90/80), semantic/source-fidelity review, visual diffs, and targeted Luna refactoring capped at three cycles.
metadata:
  short-description: Score, compare and correct Penpot screens
  compatibility: Requires the project checkout and Python 3; Penpot export uses the local MCP connection.
---

# Penpot validation and refinement

Use the portable `visual-qa-auditor` profile for render collection and issue
triage. The orchestrator remains the final reviewer and owns the official score
and state transition.

Read [the immutable scoring contract](references/scoring.md) and the local
[`lessons-learned/README.md`](lessons-learned/README.md). This
skill owns `VALIDATING`, `REFACTORING` and `DS_REVALIDATING`.

## Validation pass

For every requested screen and viewport, delegate render/capture work to
`gpt-5.6-luna`. Luna may render, collect evidence and perform the targeted
refactor, but the orchestrator/reviewer is responsible for the official score,
gate decision and approval transition. Run the deterministic evaluator with
`scripts/validate.sh --run-dir <run-dir> --cycle <1..3>` from this skill's
physical directory.
Never change its formula, threshold, coverage rule or severity mapping during a
run. A human or language model may
explain a finding but may not override the evaluator.

The CLI writes immutable `cycles/cycle-N/score.json`, `issues.json`, report,
side-by-side, detail-board, overlay and heatmap artifacts. The detail board is
the primary human-review artifact for long pages because it keeps source,
export and difference readable by vertical region. Check the gate separately per viewport:
`score >= 90`, `coverage >= 80`, no P0/P1. Structural checks must also confirm
components/styles/tokens are actually reusable, not only visually similar.
Cross-check every planned `asset_ref` against the source asset manifest and the
Penpot build log. A lookalike or unrecorded substitute is an asset-provenance
issue even when its pixel similarity is high.

The numeric image score is not a semantic approval. Before delivery, the
reviewer must separately verify visible copy, route/state, hierarchy and exact
source assets and fonts against `source-inventory.md`, `assets-manifest.json`,
`frame-spec.json` and the build plan. Record mismatches as issues and keep the
run `NEEDS_REVIEW` even when the deterministic score passes; never change the
formula or thresholds to encode this review. See [`LL - heuristic score is not source fidelity.md`](lessons-learned/project/LL%20-%20heuristic%20score%20is%20not%20source%20fidelity.md).

Use a regression baseline only when it represents the same editable version,
source, viewport and frame-spec. Replacing a screenshot-only artifact with an
editable reconstruction starts a new version/run; do not inherit the old score.
See [`LL - baseline must match representation.md`](lessons-learned/project/LL%20-%20baseline%20must%20match%20representation.md).

The structural gate must inspect the delivered frame tree, not only the PNG.
Record descendant counts by type and component-instance counts in
`design/structure-inventory.json`. Fail the gate when the visible frame is
substantively a single screenshot/image fill, when a section contains only a
semantic label with no editable descendants, or when planned components are
not instantiated in the delivered frame. A hidden/locked source-reference
image is allowed as evidence, but it cannot be the only visible content.
In strict schema runs, the inventory is mandatory even when the pixel score
passes; an absent or empty inventory is a blocking structural failure, not an
invitation to infer structure from the PNG.

Before scoring, compare the export dimensions with `source/frame-spec.json`.
The Penpot frame and reference capture must represent the same full finite
content bounds; a `1440x900` export of a longer page is a blocking truncation,
not a valid desktop result. Likewise, an unnecessarily widened frame fails when
the source evidence shows accidental overflow or a nested scroll container.
For unstable/infinite content, validate only the explicitly approved finite
state and name that boundary in the report.

Each deterministic issue identifies a region/coordinates where available,
expected vs actual, magnitude and evidence. The Luna worker must add likely root
cause and a precise fix in the refactoring handoff without altering the
machine-written score/issues files. Penpot exports are produced through
the `$penpot-build` MCP wrapper before validation.

## Refinement loop

If any gate fails after initial build, delegate targeted fixes to Luna using the
issues as the only change list, then rerun the full evaluator. Increment
`validation_cycle`; maximum is three. Avoid broad redesign when the issue calls
for a local correction. Preserve all score files and reports. After cycle 3,
set `NEEDS_REVIEW` with the best version and explicit remaining issues.
Every failed-cycle refactor must produce a new Penpot export hash and a mutation
record in the MCP log. The evaluator rejects an unchanged export before creating
the next immutable cycle directory; a validation-only rerun must be recorded as
such and never presented as a refinement cycle.

In `directed_creation`, user review rounds are unlimited. Record each feedback
message in `feedback/` and build a new version only after interpreting it;
internal validation still starts at cycle 1 for that version.

If the source is incomplete or comparison is unsafe, request clarification;
do not turn missing evidence into a pass. If Luna is unavailable, stop with
`BLOCKED_MODEL_UNAVAILABLE`.

For the post-componentization pass, provide `--inventory
design/structure-inventory.json`. A visual pass alone cannot enter delivery.
