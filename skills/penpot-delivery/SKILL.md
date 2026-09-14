---
name: penpot-delivery
description: Package a completed Penpot run with links, versioned provenance, visual comparisons, scores, issues and a clear delivered or needs-review decision.
metadata:
  short-description: Deliver Penpot files and visual validation evidence
  compatibility: Requires the project checkout and a completed Penpot workflow run directory.
---

# Penpot delivery

Read the current run manifest and all current score/issue records
before packaging.
This skill runs only after design-system revalidation or an explicit
`NEEDS_REVIEW` terminal state.

## Acceptance gate

Declare `DELIVERED` only when every screen/viewport passes score >= 90,
coverage >= 80, zero P0/P1, the structural component/style checks pass, and
the user has provided required formal approval. Otherwise deliver as
`NEEDS_REVIEW`, naming the exact blockers and best available version.

## Package

Create `delivery/report.md` and `delivery/manifest.json` containing:

- Penpot workspace/project/file/page/frame references and version;
- route, source/briefing references, viewport matrix and decisions;
- score and coverage per screen/viewport, with evaluator/config version;
- links to side-by-side, overlay, heatmap and issue evidence;
- issue table with severity, region, expected/actual, cause and fix status;
- validation cycles used and any remaining risks/assumptions;
- design-system inventory and structural verification;
- exact approval or `NEEDS_REVIEW` reason.
- `lesson_refs` for applicable mistakes and countermeasures, without duplicating
  the canonical vault notes.

Do not include secrets or private captures in Git. Keep source and feedback
records linked by stable ids. If a user asks for a visual summary, surface the
parallel comparison and explain each material mismatch in plain language.
Before delivery, run `scripts/check-package.py <run-dir>` from this skill's
physical directory.
