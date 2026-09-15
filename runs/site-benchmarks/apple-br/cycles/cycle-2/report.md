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

Aggregate score: **79.40/100**
Minimum screen score: **79.40/100**
Coverage: **38.98%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **PASS**

Next state: **REFINEMENT**

## home — 1440×900

- Score: **79.40**; coverage: **38.98%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×5261**; capture: **full_page**
- Similarity evidence: pixel=0.5313, exact=0.1850
- Comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 99.60 | 29.88 | content bbox IoU=0.995, area similarity=0.998, viewport_match=1 |
| Spacing/grid | 20 | 75.49 | 15.10 | row profile MAE=0.421, column profile MAE=0.069 |
| Typography | 15 | 55.75 | 8.36 | dark density similarity=0.601, row similarity=0.504; image-only heuristic |
| Color/border/shadow | 15 | 75.73 | 11.36 | quantized RGB histogram similarity=0.757 |
| Content/density | 10 | 70.50 | 7.05 | mask coverage=0.576, density similarity=0.898 |
| Assets | 10 | 76.51 | 7.65 | component count similarity=0.667, area similarity=0.913; image-only heuristic |

Issues:
- **P1** `home-1440x900-I1` — Visual difference region at `{'x': 0, 'y': 1452, 'width': 1440, 'height': 1442}`: 1918127 pixels (25.32% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=1452, w=1440, h=1442.
- **P1** `home-1440x900-I2` — Visual difference region at `{'x': 0, 'y': 2972, 'width': 1440, 'height': 889}`: 863663 pixels (11.40% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=2972, w=1440, h=889.
- **P1** `home-1440x900-I3` — Visual difference region at `{'x': 255, 'y': 3932, 'width': 930, 'height': 523}`: 477754 pixels (6.31% da tela) ultrapassam o limiar de diferença; ajuste a região x=255, y=3932, w=930, h=523.
- **P1** `home-1440x900-I4` — Visual difference region at `{'x': 0, 'y': 337, 'width': 1440, 'height': 483}`: 326067 pixels (4.30% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=337, w=1440, h=483.
- **P1** `home-1440x900-I5` — Visual difference region at `{'x': 410, 'y': 1040, 'width': 620, 'height': 400}`: 206565 pixels (2.73% da tela) ultrapassam o limiar de diferença; ajuste a região x=410, y=1040, w=620, h=400.
- **P1** `home-1440x900-I6` — Visual difference region at `{'x': 719, 'y': 3578, 'width': 709, 'height': 342}`: 173986 pixels (2.30% da tela) ultrapassam o limiar de diferença; ajuste a região x=719, y=3578, w=709, h=342.
- **P1** `home-1440x900-I7` — Visual difference region at `{'x': 1198, 'y': 3932, 'width': 242, 'height': 523}`: 126566 pixels (1.67% da tela) ultrapassam o limiar de diferença; ajuste a região x=1198, y=3932, w=242, h=523.
- **P1** `home-1440x900-I8` — Visual difference region at `{'x': 0, 'y': 3932, 'width': 242, 'height': 523}`: 125613 pixels (1.66% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=3932, w=242, h=523.
- **P1** `home-1440x900-I9` — Visual difference region at `{'x': 1000, 'y': 4652, 'width': 320, 'height': 250}`: 69513 pixels (0.92% da tela) ultrapassam o limiar de diferença; ajuste a região x=1000, y=4652, w=320, h=250.
- **P1** `home-1440x900-I10` — Visual difference region at `{'x': 80, 'y': 4648, 'width': 320, 'height': 254}`: 69138 pixels (0.91% da tela) ultrapassam o limiar de diferença; ajuste a região x=80, y=4648, w=320, h=254.
- **P1** `home-1440x900-I11` — Visual difference region at `{'x': 400, 'y': 4682, 'width': 284, 'height': 228}`: 60664 pixels (0.80% da tela) ultrapassam o limiar de diferença; ajuste a região x=400, y=4682, w=284, h=228.
- **P1** `home-1440x900-I12` — Visual difference region at `{'x': 715, 'y': 4682, 'width': 285, 'height': 220}`: 60077 pixels (0.79% da tela) ultrapassam o limiar de diferença; ajuste a região x=715, y=4682, w=285, h=220.
- **P1** `home-1440x900-I13` — Visual difference region at `{'x': 0, 'y': 44, 'width': 1440, 'height': 8}`: 11520 pixels (0.15% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=44, w=1440, h=8.
- **P1** `home-1440x900-I14` — Visual difference region at `{'x': 400, 'y': 4648, 'width': 280, 'height': 33}`: 7956 pixels (0.11% da tela) ultrapassam o limiar de diferença; ajuste a região x=400, y=4648, w=280, h=33.
- **P1** `home-1440x900-I15` — Visual difference region at `{'x': 720, 'y': 4648, 'width': 280, 'height': 33}`: 7821 pixels (0.10% da tela) ultrapassam o limiar de diferença; ajuste a região x=720, y=4648, w=280, h=33.
- **P1** `home-1440x900-I16` — Regression against previous cycle: Score caiu de 99.30 para 79.40; revisar antes de aprovar.

## Regression gate

The cycle is not approved because at least one screen regressed against the prior cycle.
