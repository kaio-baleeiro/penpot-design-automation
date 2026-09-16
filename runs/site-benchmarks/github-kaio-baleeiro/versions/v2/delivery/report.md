---
type: delivery-report
status: needs-review
created: 2026-09-15
updated: 2026-09-15
source_agent: codex
agent_context: penpot-design-automation
confidence: high
review: true
---

# GitHub Kaio benchmark — v2 delivery report

## Decision

**NEEDS_REVIEW.** This is the terminal package after the permitted three
validation cycles. The deterministic image gate passes in cycle 3, but the
orchestrator's final fidelity review rejects the design because important
content, asset and component details still differ from the source. It is not
an approved reproduction and must not be marked `DELIVERED`.

## Penpot artifact

- File: `Site Benchmarks` (`cf04346a-b044-818b-8008-a4ed84a51a17`)
- Project: `Penpot Benchmarks`
- Page: `Benchmark — GitHub Kaio`
- Frame: `GitHub Kaio — Home — 1440x1807`
- Frame ID: `9a19287b-6930-802f-8008-a4ee0b57f233`
- Type: editable composition; the source screenshot is not visible content.

The desktop observation viewport is 1440×900. The source is a finite full-page
document of 1440×1807, so the delivered frame grows vertically and keeps the
root width bounded at 1440.

## Validation history

| Cycle | Score | Coverage | Image/structure gate | Reviewer decision |
|---:|---:|---:|---|---|
| 1 | 93.96 | 88.15% | Pass | Refactor: header, sidebar, README, repos and activity were materially wrong. |
| 2 | 96.77 | 92.07% | Pass | Refactor: asset rendering, README/card fidelity and MCP mutation trace still incomplete. |
| 3 | 98.52 | 92.79% | Pass | `NEEDS_REVIEW`: source-content fidelity still fails; no fourth cycle allowed. |

The score is `penpot-visual-v1`. Its own report states that the image heuristics
cannot prove semantic copy, font family, asset provenance or editability. The
final review therefore remains authoritative for acceptance.

## Final-cycle blockers

1. Avatar crop/scale and Pull Shark badge differ from the captured profile, and
   the followers count is `12` instead of the visible `3`.
2. README border, layout, exact copy, links and contribution SVG are simplified
   or placed at the wrong scale.
3. Repository cards omit source borders, badges and metadata; descriptions and
   language labels diverge in multiple cards.
4. Contribution calendar, labels, activity timeline, controls and footer are
   incomplete compared with the source.

These regions are visible in the final comparison:

- [side-by-side annotated](../../../analysis/v2-cycle-3-home-side-by-side-annotated.png)
- [overlay](../../../analysis/v2-cycle-3-home-overlay.png)
- [heatmap](../../../analysis/v2-cycle-3-home-heatmap.png)
- [issue record](../cycles/cycle-3/issues.json)

Cycle 1 and cycle 2 comparisons are retained for audit:

- [cycle 1 side-by-side](../../../analysis/v2-cycle-1-home-side-by-side-annotated.png)
- [cycle 2 side-by-side](../../../analysis/v2-cycle-2-home-side-by-side-annotated.png)

## Structural and provenance checks

The final structure gate passes: the frame is not screenshot-only, with 280
descendants, 279 editable shapes and two image shapes. The design plan,
structure inventory, MCP log, source map, frame specification and asset
manifest are linked in `manifest.json`. The full-size profile avatar is
embedded; the badge and contribution SVG are source-mapped but not verified as
rendered originals. Private captures and secrets are excluded.

## Lessons applied

This run references the executable project lessons for editable composition,
full-page evidence, heuristic-score limits and immutable cycle ownership. The
remaining semantic-fidelity gap is intentionally left visible as a lesson for
the next version: a high visual score cannot override the orchestrator's
content/source review.

## Next action

Do not modify these cycle directories or open a hidden fourth cycle. Start a new
version/run using the final-cycle issues as its initial correction brief, then
repeat intake, source mapping, editable construction and the three-cycle gate.
