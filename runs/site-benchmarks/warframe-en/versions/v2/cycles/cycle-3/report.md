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

# Penpot validation report — cycle 3

Gate result: **FAIL**

Aggregate score: **83.34/100**
Minimum screen score: **83.34/100**
Coverage: **60.72%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **PASS**

Next state: **NEEDS_REVIEW**

## home — 1440×900

- Score: **83.34**; coverage: **60.72%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×5837**; capture: **bounded_state**
- Similarity evidence: pixel=0.8599, exact=0.0001
- Comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 99.41 | 29.82 | content bbox IoU=0.992, area similarity=0.997, viewport_match=1 |
| Spacing/grid | 20 | 75.27 | 15.05 | row profile MAE=0.323, column profile MAE=0.172 |
| Typography | 15 | 94.87 | 14.23 | dark density similarity=0.957, row similarity=0.938; image-only heuristic |
| Color/border/shadow | 15 | 77.06 | 11.56 | quantized RGB histogram similarity=0.771 |
| Content/density | 10 | 66.12 | 6.61 | mask coverage=0.623, density similarity=0.718 |
| Assets | 10 | 60.61 | 6.06 | component count similarity=0.545, area similarity=0.697; image-only heuristic |

Issues:
- **P1** `home-1440x900-I1` — Visual difference region at `{'x': 0, 'y': 66, 'width': 1440, 'height': 1345}`: 1141110 pixels (13.58% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=66, w=1440, h=1345.
- **P1** `home-1440x900-I2` — Visual difference region at `{'x': 0, 'y': 1666, 'width': 1440, 'height': 965}`: 621785 pixels (7.40% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=1666, w=1440, h=965.
- **P1** `home-1440x900-I3` — Visual difference region at `{'x': 0, 'y': 4012, 'width': 1440, 'height': 391}`: 302078 pixels (3.59% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=4012, w=1440, h=391.
- **P1** `home-1440x900-I4` — Visual difference region at `{'x': 19, 'y': 2928, 'width': 1336, 'height': 662}`: 283526 pixels (3.37% da tela) ultrapassam o limiar de diferença; ajuste a região x=19, y=2928, w=1336, h=662.
- **P1** `home-1440x900-I5` — Visual difference region at `{'x': 84, 'y': 2215, 'width': 530, 'height': 332}`: 120648 pixels (1.44% da tela) ultrapassam o limiar de diferença; ajuste a região x=84, y=2215, w=530, h=332.
- **P1** `home-1440x900-I6` — Visual difference region at `{'x': 80, 'y': 4545, 'width': 958, 'height': 200}`: 119591 pixels (1.42% da tela) ultrapassam o limiar de diferença; ajuste a região x=80, y=4545, w=958, h=200.
- **P1** `home-1440x900-I7` — Visual difference region at `{'x': 110, 'y': 3664, 'width': 390, 'height': 217}`: 78518 pixels (0.93% da tela) ultrapassam o limiar de diferença; ajuste a região x=110, y=3664, w=390, h=217.
- **P1** `home-1440x900-I8` — Visual difference region at `{'x': 930, 'y': 3665, 'width': 397, 'height': 221}`: 65604 pixels (0.78% da tela) ultrapassam o limiar de diferença; ajuste a região x=930, y=3665, w=397, h=221.
- **P1** `home-1440x900-I9` — Visual difference region at `{'x': 524, 'y': 3675, 'width': 390, 'height': 204}`: 55798 pixels (0.66% da tela) ultrapassam o limiar de diferença; ajuste a região x=524, y=3675, w=390, h=204.
- **P1** `home-1440x900-I10` — Visual difference region at `{'x': 647, 'y': 2734, 'width': 793, 'height': 169}`: 50865 pixels (0.61% da tela) ultrapassam o limiar de diferença; ajuste a região x=647, y=2734, w=793, h=169.
- **P1** `home-1440x900-I11` — Visual difference region at `{'x': 0, 'y': 1421, 'width': 1440, 'height': 135}`: 49286 pixels (0.59% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=1421, w=1440, h=135.
- **P1** `home-1440x900-I12` — Visual difference region at `{'x': 80, 'y': 3585, 'width': 1280, 'height': 194}`: 47438 pixels (0.56% da tela) ultrapassam o limiar de diferença; ajuste a região x=80, y=3585, w=1280, h=194.
- **P1** `home-1440x900-I13` — Visual difference region at `{'x': 0, 'y': 3093, 'width': 82, 'height': 259}`: 14693 pixels (0.17% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=3093, w=82, h=259.
- **P1** `home-1440x900-I14` — Visual difference region at `{'x': 252, 'y': 323, 'width': 169, 'height': 122}`: 8915 pixels (0.11% da tela) ultrapassam o limiar de diferença; ajuste a região x=252, y=323, w=169, h=122.
- **P1** `home-1440x900-I15` — Visual difference region at `{'x': 650, 'y': 2675, 'width': 140, 'height': 68}`: 8570 pixels (0.10% da tela) ultrapassam o limiar de diferença; ajuste a região x=650, y=2675, w=140, h=68.
