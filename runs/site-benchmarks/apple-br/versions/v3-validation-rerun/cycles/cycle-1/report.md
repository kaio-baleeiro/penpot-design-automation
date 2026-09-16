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

# Penpot validation report — cycle 1

Gate result: **FAIL**

Aggregate score: **89.57/100**
Minimum screen score: **89.57/100**
Coverage: **71.42%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **FAIL**

Structural blockers:
- strict validation inventory has no reusable components
- strict validation inventory has no component instances

Next state: **REFINEMENT**

## home — 1440×900

- Score: **89.57**; coverage: **71.42%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×5261**; capture: **full_page**
- Similarity evidence: pixel=0.8440, exact=0.5362
- Comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 90.98 | 27.29 | content bbox IoU=0.900, area similarity=0.900, viewport_match=1 |
| Spacing/grid | 20 | 90.51 | 18.10 | row profile MAE=0.123, column profile MAE=0.067 |
| Typography | 15 | 83.03 | 12.45 | dark density similarity=0.796, row similarity=0.872; image-only heuristic |
| Color/border/shadow | 15 | 85.92 | 12.89 | quantized RGB histogram similarity=0.859 |
| Content/density | 10 | 89.74 | 8.97 | mask coverage=0.860, density similarity=0.954 |
| Assets | 10 | 98.58 | 9.86 | component count similarity=1.000, area similarity=0.964; image-only heuristic |

Issues:
- **P1** `home-1440x900-I1` — Visual difference region at `{'x': 0, 'y': 3932, 'width': 1185, 'height': 523}`: 559266 pixels (7.38% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=3932, w=1185, h=523.
- **P1** `home-1440x900-I2` — Visual difference region at `{'x': 726, 'y': 3340, 'width': 702, 'height': 580}`: 399982 pixels (5.28% da tela) ultrapassam o limiar de diferença; ajuste a região x=726, y=3340, w=702, h=580.
- **P1** `home-1440x900-I3` — Visual difference region at `{'x': 232, 'y': 361, 'width': 988, 'height': 375}`: 231915 pixels (3.06% da tela) ultrapassam o limiar de diferença; ajuste a região x=232, y=361, w=988, h=375.
- **P1** `home-1440x900-I4` — Visual difference region at `{'x': 418, 'y': 1040, 'width': 603, 'height': 400}`: 189899 pixels (2.51% da tela) ultrapassam o limiar de diferença; ajuste a região x=418, y=1040, w=603, h=400.
- **P1** `home-1440x900-I5` — Visual difference region at `{'x': 1118, 'y': 2156, 'width': 322, 'height': 580}`: 144703 pixels (1.91% da tela) ultrapassam o limiar de diferença; ajuste a região x=1118, y=2156, w=322, h=580.
- **P1** `home-1440x900-I6` — Visual difference region at `{'x': 1198, 'y': 3932, 'width': 242, 'height': 523}`: 102590 pixels (1.35% da tela) ultrapassam o limiar de diferença; ajuste a região x=1198, y=3932, w=242, h=523.
- **P1** `home-1440x900-I7` — Visual difference region at `{'x': 449, 'y': 1514, 'width': 274, 'height': 434}`: 66779 pixels (0.88% da tela) ultrapassam o limiar de diferença; ajuste a região x=449, y=1514, w=274, h=434.
- **P1** `home-1440x900-I8` — Visual difference region at `{'x': 726, 'y': 1521, 'width': 266, 'height': 413}`: 57626 pixels (0.76% da tela) ultrapassam o limiar de diferença; ajuste a região x=726, y=1521, w=266, h=413.
- **P1** `home-1440x900-I9` — Visual difference region at `{'x': 726, 'y': 2156, 'width': 121, 'height': 580}`: 35209 pixels (0.46% da tela) ultrapassam o limiar de diferença; ajuste a região x=726, y=2156, w=121, h=580.
- **P1** `home-1440x900-I10` — Visual difference region at `{'x': 0, 'y': 2748, 'width': 356, 'height': 312}`: 32446 pixels (0.43% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=2748, w=356, h=312.
- **P1** `home-1440x900-I11` — Visual difference region at `{'x': 110, 'y': 3586, 'width': 226, 'height': 274}`: 27804 pixels (0.37% da tela) ultrapassam o limiar de diferença; ajuste a região x=110, y=3586, w=226, h=274.
- **P1** `home-1440x900-I12` — Visual difference region at `{'x': 184, 'y': 2394, 'width': 334, 'height': 244}`: 25798 pixels (0.34% da tela) ultrapassam o limiar de diferença; ajuste a região x=184, y=2394, w=334, h=244.
- **P1** `home-1440x900-I13` — Visual difference region at `{'x': 337, 'y': 3578, 'width': 154, 'height': 245}`: 20301 pixels (0.27% da tela) ultrapassam o limiar de diferença; ajuste a região x=337, y=3578, w=154, h=245.
- **P1** `home-1440x900-I14` — Visual difference region at `{'x': 785, 'y': 2156, 'width': 256, 'height': 134}`: 18405 pixels (0.24% da tela) ultrapassam o limiar de diferença; ajuste a região x=785, y=2156, w=256, h=134.
- **P1** `home-1440x900-I15` — Visual difference region at `{'x': 259, 'y': 2960, 'width': 184, 'height': 163}`: 11745 pixels (0.16% da tela) ultrapassam o limiar de diferença; ajuste a região x=259, y=2960, w=184, h=163.
- **P1** `home-1440x900-I16` — Visual difference region at `{'x': 259, 'y': 3127, 'width': 182, 'height': 165}`: 8852 pixels (0.12% da tela) ultrapassam o limiar de diferença; ajuste a região x=259, y=3127, w=182, h=165.
