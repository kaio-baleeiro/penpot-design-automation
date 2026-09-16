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

# Penpot validation report — cycle 1

Gate result: **FAIL**

Aggregate score: **85.93/100**
Minimum screen score: **85.93/100**
Coverage: **71.31%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **PASS**

Next state: **REFINEMENT**

## home — 1440×900

- Score: **85.93**; coverage: **71.31%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×5261**; capture: **full_page**
- Similarity evidence: pixel=0.8386, exact=0.5346
- Comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 90.98 | 27.29 | content bbox IoU=0.900, area similarity=0.900, viewport_match=1 |
| Spacing/grid | 20 | 86.14 | 17.23 | row profile MAE=0.146, column profile MAE=0.132 |
| Typography | 15 | 83.15 | 12.47 | dark density similarity=0.799, row similarity=0.871; image-only heuristic |
| Color/border/shadow | 15 | 80.64 | 12.10 | quantized RGB histogram similarity=0.806 |
| Content/density | 10 | 82.06 | 8.21 | mask coverage=0.841, density similarity=0.790 |
| Assets | 10 | 86.38 | 8.64 | component count similarity=0.909, area similarity=0.796; image-only heuristic |

Issues:
- **P1** `home-1440x900-I1` — Visual difference region at `{'x': 0, 'y': 3932, 'width': 1440, 'height': 523}`: 639014 pixels (8.43% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=3932, w=1440, h=523.
- **P1** `home-1440x900-I2` — Visual difference region at `{'x': 726, 'y': 2156, 'width': 702, 'height': 580}`: 404094 pixels (5.33% da tela) ultrapassam o limiar de diferença; ajuste a região x=726, y=2156, w=702, h=580.
- **P1** `home-1440x900-I3` — Visual difference region at `{'x': 0, 'y': 3340, 'width': 726, 'height': 580}`: 240120 pixels (3.17% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=3340, w=726, h=580.
- **P1** `home-1440x900-I4` — Visual difference region at `{'x': 418, 'y': 1040, 'width': 603, 'height': 400}`: 176576 pixels (2.33% da tela) ultrapassam o limiar de diferença; ajuste a região x=418, y=1040, w=603, h=400.
- **P1** `home-1440x900-I5` — Visual difference region at `{'x': 232, 'y': 370, 'width': 988, 'height': 291}`: 172188 pixels (2.27% da tela) ultrapassam o limiar de diferença; ajuste a região x=232, y=370, w=988, h=291.
- **P1** `home-1440x900-I6` — Visual difference region at `{'x': 355, 'y': 2156, 'width': 359, 'height': 580}`: 151697 pixels (2.00% da tela) ultrapassam o limiar de diferença; ajuste a região x=355, y=2156, w=359, h=580.
- **P1** `home-1440x900-I7` — Visual difference region at `{'x': 449, 'y': 1598, 'width': 269, 'height': 329}`: 58021 pixels (0.77% da tela) ultrapassam o limiar de diferença; ajuste a região x=449, y=1598, w=269, h=329.
- **P1** `home-1440x900-I8` — Visual difference region at `{'x': 796, 'y': 1603, 'width': 196, 'height': 282}`: 39535 pixels (0.52% da tela) ultrapassam o limiar de diferença; ajuste a região x=796, y=1603, w=196, h=282.
- **P1** `home-1440x900-I9` — Visual difference region at `{'x': 0, 'y': 2156, 'width': 109, 'height': 580}`: 33197 pixels (0.44% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=2156, w=109, h=580.
- **P1** `home-1440x900-I10` — Visual difference region at `{'x': 922, 'y': 3578, 'width': 266, 'height': 281}`: 30643 pixels (0.40% da tela) ultrapassam o limiar de diferença; ajuste a região x=922, y=3578, w=266, h=281.
- **P1** `home-1440x900-I11` — Visual difference region at `{'x': 47, 'y': 2156, 'width': 256, 'height': 134}`: 18537 pixels (0.24% da tela) ultrapassam o limiar de diferença; ajuste a região x=47, y=2156, w=256, h=134.
- **P1** `home-1440x900-I12` — Visual difference region at `{'x': 729, 'y': 1611, 'width': 76, 'height': 282}`: 10370 pixels (0.14% da tela) ultrapassam o limiar de diferença; ajuste a região x=729, y=1611, w=76, h=282.
