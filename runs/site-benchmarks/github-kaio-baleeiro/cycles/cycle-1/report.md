---
type: validation-report
status: complete
created: 2026-09-15
updated: 2026-09-15
source_agent: codex
agent_context: penpot-design-automation
confidence: high
review: false
---

# Penpot validation report — cycle 1

Gate result: **PASS**

Aggregate score: **100.00/100**
Minimum screen score: **100.00/100**
Coverage: **100.00%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **FAIL**

Structural blockers:
- missing required component instances: GitHubHeader, ProfileHeader, ProfileTabs, RepositoryList

Next state: **READY_FOR_USER_REVIEW**

## home — 1440×900

- Score: **100.00**; coverage: **100.00%**; status: **PASS**
- Viewport: **1440×900**; frame: **1440×1807**; capture: **full_page**
- Similarity evidence: pixel=1.0000, exact=1.0000
- Comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 100.00 | 30.00 | content bbox IoU=1.000, area similarity=1.000, viewport_match=1 |
| Spacing/grid | 20 | 100.00 | 20.00 | row profile MAE=0.000, column profile MAE=0.000 |
| Typography | 15 | 100.00 | 15.00 | dark density similarity=1.000, row similarity=1.000; image-only heuristic |
| Color/border/shadow | 15 | 100.00 | 15.00 | quantized RGB histogram similarity=1.000 |
| Content/density | 10 | 100.00 | 10.00 | mask coverage=1.000, density similarity=1.000 |
| Assets | 10 | 100.00 | 10.00 | component count similarity=1.000, area similarity=1.000; image-only heuristic |

- No differences above the configured threshold.
