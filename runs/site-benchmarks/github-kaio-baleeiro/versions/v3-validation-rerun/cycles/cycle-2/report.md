---
type: validation-report
status: needs-review
created: 2026-09-16
updated: 2026-09-16
source_agent: codex
agent_context: penpot-design-automation
confidence: high
review: true
---

# Penpot validation report — cycle 2

Gate result: **FAIL**

Aggregate score: **98.52/100**
Minimum screen score: **98.52/100**
Coverage: **92.79%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **FAIL**

Structural blockers:
- strict validation inventory has no reusable components
- strict validation inventory has no component instances

Next state: **REFINEMENT**

## home — 1440×900

- Score: **98.52**; coverage: **92.79%**; status: **PASS**
- Viewport: **1440×900**; frame: **1440×1807**; capture: **full_page**
- Similarity evidence: pixel=0.9659, exact=0.8178
- Comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 99.85 | 29.95 | content bbox IoU=0.998, area similarity=0.998, viewport_match=1 |
| Spacing/grid | 20 | 99.55 | 19.91 | row profile MAE=0.003, column profile MAE=0.005 |
| Typography | 15 | 94.59 | 14.19 | dark density similarity=0.923, row similarity=0.974; image-only heuristic |
| Color/border/shadow | 15 | 96.74 | 14.51 | quantized RGB histogram similarity=0.967 |
| Content/density | 10 | 99.53 | 9.95 | mask coverage=0.994, density similarity=0.998 |
| Assets | 10 | 99.98 | 10.00 | component count similarity=1.000, area similarity=0.999; image-only heuristic |

Issues:
- **P3** `home-1440x900-I1` — Visual difference region at `{'x': 203, 'y': 162, 'width': 158, 'height': 247}`: 17742 pixels (0.68% da tela) ultrapassam o limiar de diferença; ajuste a região x=203, y=162, w=158, h=247.
- **P3** `home-1440x900-I2` — Visual difference region at `{'x': 112, 'y': 112, 'width': 250, 'height': 172}`: 9569 pixels (0.37% da tela) ultrapassam o limiar de diferença; ajuste a região x=112, y=112, w=250, h=172.
- **P3** `home-1440x900-I3` — Visual difference region at `{'x': 890, 'y': 17, 'width': 204, 'height': 38}`: 4830 pixels (0.19% da tela) ultrapassam o limiar de diferença; ajuste a região x=890, y=17, w=204, h=38.
- **P3** `home-1440x900-I4` — Visual difference region at `{'x': 115, 'y': 208, 'width': 119, 'height': 196}`: 4205 pixels (0.16% da tela) ultrapassam o limiar de diferença; ajuste a região x=115, y=208, w=119, h=196.
- **P3** `home-1440x900-I5` — Visual difference region at `{'x': 1211, 'y': 1313, 'width': 117, 'height': 34}`: 3882 pixels (0.15% da tela) ultrapassam o limiar de diferença; ajuste a região x=1211, y=1313, w=117, h=34.
- **P3** `home-1440x900-I6` — Visual difference region at `{'x': 1224, 'y': 17, 'width': 109, 'height': 38}`: 3607 pixels (0.14% da tela) ultrapassam o limiar de diferença; ajuste a região x=1224, y=17, w=109, h=38.
- **P3** `home-1440x900-I7` — Visual difference region at `{'x': 114, 'y': 717, 'width': 62, 'height': 63}`: 3071 pixels (0.12% da tela) ultrapassam o limiar de diferença; ajuste a região x=114, y=717, w=62, h=63.
- **P3** `home-1440x900-I8` — Visual difference region at `{'x': 1004, 'y': 21, 'width': 91, 'height': 30}`: 2684 pixels (0.10% da tela) ultrapassam o limiar de diferença; ajuste a região x=1004, y=21, w=91, h=30.
