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

# Penpot validation report — cycle 3

Gate result: **FAIL**

Aggregate score: **80.27/100**
Minimum screen score: **80.27/100**
Coverage: **69.80%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **PASS**

Next state: **NEEDS_REVIEW**

## home — 1440×900

- Score: **80.27**; coverage: **69.80%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×5261**; capture: **full_page**
- Similarity evidence: pixel=0.8144, exact=0.6079
- Comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 86.87 | 26.06 | content bbox IoU=0.854, area similarity=0.854, viewport_match=1 |
| Spacing/grid | 20 | 80.35 | 16.07 | row profile MAE=0.222, column profile MAE=0.171 |
| Typography | 15 | 77.89 | 11.68 | dark density similarity=0.755, row similarity=0.808; image-only heuristic |
| Color/border/shadow | 15 | 82.83 | 12.42 | quantized RGB histogram similarity=0.828 |
| Content/density | 10 | 75.00 | 7.50 | mask coverage=0.769, density similarity=0.721 |
| Assets | 10 | 65.31 | 6.53 | component count similarity=0.600, area similarity=0.733; image-only heuristic |

Issues:
- **P1** `home-1440x900-I1` — Visual difference region at `{'x': 0, 'y': 3932, 'width': 1440, 'height': 523}`: 709175 pixels (9.36% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=3932, w=1440, h=523.
- **P1** `home-1440x900-I2` — Visual difference region at `{'x': 718, 'y': 3340, 'width': 710, 'height': 580}`: 403072 pixels (5.32% da tela) ultrapassam o limiar de diferença; ajuste a região x=718, y=3340, w=710, h=580.
- **P1** `home-1440x900-I3` — Visual difference region at `{'x': 12, 'y': 3340, 'width': 705, 'height': 537}`: 280815 pixels (3.71% da tela) ultrapassam o limiar de diferença; ajuste a região x=12, y=3340, w=705, h=537.
- **P1** `home-1440x900-I4` — Visual difference region at `{'x': 0, 'y': 1040, 'width': 1440, 'height': 412}`: 228752 pixels (3.02% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=1040, w=1440, h=412.
- **P1** `home-1440x900-I5` — Visual difference region at `{'x': 232, 'y': 370, 'width': 988, 'height': 285}`: 171869 pixels (2.27% da tela) ultrapassam o limiar de diferença; ajuste a região x=232, y=370, w=988, h=285.
- **P1** `home-1440x900-I6` — Visual difference region at `{'x': 449, 'y': 1597, 'width': 543, 'height': 439}`: 124127 pixels (1.64% da tela) ultrapassam o limiar de diferença; ajuste a região x=449, y=1597, w=543, h=439.
- **P1** `home-1440x900-I7` — Visual difference region at `{'x': 80, 'y': 2736, 'width': 623, 'height': 185}`: 94170 pixels (1.24% da tela) ultrapassam o limiar de diferença; ajuste a região x=80, y=2736, w=623, h=185.
- **P1** `home-1440x900-I8` — Visual difference region at `{'x': 726, 'y': 2640, 'width': 702, 'height': 96}`: 60089 pixels (0.79% da tela) ultrapassam o limiar de diferença; ajuste a região x=726, y=2640, w=702, h=96.
- **P1** `home-1440x900-I9` — Visual difference region at `{'x': 0, 'y': 2144, 'width': 1440, 'height': 508}`: 35546 pixels (0.47% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=2144, w=1440, h=508.
- **P1** `home-1440x900-I10` — Visual difference region at `{'x': 0, 'y': 44, 'width': 1440, 'height': 8}`: 11520 pixels (0.15% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=44, w=1440, h=8.
