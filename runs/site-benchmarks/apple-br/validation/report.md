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

Aggregate score: **99.30/100**
Minimum screen score: **99.30/100**
Coverage: **98.37%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **FAIL**

Structural blockers:
- missing required component instances: Footer, GlobalNav, PromoSection

Next state: **READY_FOR_USER_REVIEW**

## home — 1440×900

- Score: **99.30**; coverage: **98.37%**; status: **PASS**
- Viewport: **1440×900**; frame: **1440×5261**; capture: **full_page**
- Similarity evidence: pixel=0.9938, exact=0.8110
- Comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 100.00 | 30.00 | content bbox IoU=1.000, area similarity=1.000, viewport_match=1 |
| Spacing/grid | 20 | 98.79 | 19.76 | row profile MAE=0.013, column profile MAE=0.011 |
| Typography | 15 | 99.74 | 14.96 | dark density similarity=0.999, row similarity=0.996; image-only heuristic |
| Color/border/shadow | 15 | 98.37 | 14.76 | quantized RGB histogram similarity=0.984 |
| Content/density | 10 | 98.49 | 9.85 | mask coverage=0.987, density similarity=0.982 |
| Assets | 10 | 99.77 | 9.98 | component count similarity=1.000, area similarity=0.994; image-only heuristic |

- No differences above the configured threshold.
