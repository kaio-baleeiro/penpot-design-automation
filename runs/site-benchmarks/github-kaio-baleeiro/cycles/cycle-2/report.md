---
type: validation-report
status: needs-review
created: 2026-09-15
updated: 2026-09-15
source_agent: codex
agent_context: penpot-design-automation
confidence: high
review: true
---

# Penpot validation report — cycle 2

Gate result: **FAIL**

Aggregate score: **93.96/100**
Minimum screen score: **93.96/100**
Coverage: **88.14%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **PASS**

Next state: **REFINEMENT**

## home — 1440×900

- Score: **93.96**; coverage: **88.14%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×1807**; capture: **full_page**
- Similarity evidence: pixel=0.9433, exact=0.3779
- Comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 99.80 | 29.94 | content bbox IoU=0.998, area similarity=0.998, viewport_match=1 |
| Spacing/grid | 20 | 99.34 | 19.87 | row profile MAE=0.006, column profile MAE=0.007 |
| Typography | 15 | 89.71 | 13.46 | dark density similarity=0.845, row similarity=0.961; image-only heuristic |
| Color/border/shadow | 15 | 91.83 | 13.77 | quantized RGB histogram similarity=0.918 |
| Content/density | 10 | 99.33 | 9.93 | mask coverage=0.990, density similarity=0.999 |
| Assets | 10 | 69.88 | 6.99 | component count similarity=0.500, area similarity=0.997; image-only heuristic |

Issues:
- **P2** `home-1440x900-I1` — Visual difference region at `{'x': 0, 'y': 0, 'width': 1440, 'height': 73}`: 100096 pixels (3.85% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=0, w=1440, h=73.
- **P2** `home-1440x900-I2` — Visual difference region at `{'x': 100, 'y': 112, 'width': 266, 'height': 297}`: 61595 pixels (2.37% da tela) ultrapassam o limiar de diferença; ajuste a região x=100, y=112, w=266, h=297.
- **P3** `home-1440x900-I3` — Visual difference region at `{'x': 468, 'y': 1427, 'width': 268, 'height': 31}`: 4840 pixels (0.19% da tela) ultrapassam o limiar de diferença; ajuste a região x=468, y=1427, w=268, h=31.
- **P3** `home-1440x900-I4` — Visual difference region at `{'x': 1211, 'y': 1313, 'width': 117, 'height': 34}`: 3853 pixels (0.15% da tela) ultrapassam o limiar de diferença; ajuste a região x=1211, y=1313, w=117, h=34.
- **P3** `home-1440x900-I5` — Visual difference region at `{'x': 114, 'y': 717, 'width': 62, 'height': 75}`: 3121 pixels (0.12% da tela) ultrapassam o limiar de diferença; ajuste a região x=114, y=717, w=62, h=75.
- **P3** `home-1440x900-I6` — Visual difference region at `{'x': 990, 'y': 1427, 'width': 189, 'height': 31}`: 2770 pixels (0.11% da tela) ultrapassam o limiar de diferença; ajuste a região x=990, y=1427, w=189, h=31.
- **P1** `home-1440x900-I7` — Regression against previous cycle: Score caiu de 100.00 para 93.96; revisar antes de aprovar.

## Regression gate

The cycle is not approved because at least one screen regressed against the prior cycle.
