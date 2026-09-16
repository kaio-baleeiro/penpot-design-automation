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

Aggregate score: **87.30/100**
Minimum screen score: **87.30/100**
Coverage: **72.37%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **PASS**

Next state: **REFINEMENT**

## home — 1440×900

- Score: **87.30**; coverage: **72.37%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×5261**; capture: **full_page**
- Similarity evidence: pixel=0.8430, exact=0.5473
- Comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 90.98 | 27.29 | content bbox IoU=0.900, area similarity=0.900, viewport_match=1 |
| Spacing/grid | 20 | 89.97 | 17.99 | row profile MAE=0.130, column profile MAE=0.070 |
| Typography | 15 | 82.23 | 12.33 | dark density similarity=0.784, row similarity=0.869; image-only heuristic |
| Color/border/shadow | 15 | 84.77 | 12.72 | quantized RGB histogram similarity=0.848 |
| Content/density | 10 | 88.77 | 8.88 | mask coverage=0.853, density similarity=0.940 |
| Assets | 10 | 80.86 | 8.09 | component count similarity=0.714, area similarity=0.950; image-only heuristic |

Issues:
- **P1** `home-1440x900-I1` — Visual difference region at `{'x': 0, 'y': 3932, 'width': 1440, 'height': 523}`: 671973 pixels (8.87% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=3932, w=1440, h=523.
- **P1** `home-1440x900-I2` — Visual difference region at `{'x': 726, 'y': 3340, 'width': 702, 'height': 580}`: 399982 pixels (5.28% da tela) ultrapassam o limiar de diferença; ajuste a região x=726, y=3340, w=702, h=580.
- **P1** `home-1440x900-I3` — Visual difference region at `{'x': 418, 'y': 1040, 'width': 603, 'height': 400}`: 176576 pixels (2.33% da tela) ultrapassam o limiar de diferença; ajuste a região x=418, y=1040, w=603, h=400.
- **P1** `home-1440x900-I4` — Visual difference region at `{'x': 232, 'y': 370, 'width': 988, 'height': 291}`: 172188 pixels (2.27% da tela) ultrapassam o limiar de diferença; ajuste a região x=232, y=370, w=988, h=291.
- **P1** `home-1440x900-I5` — Visual difference region at `{'x': 1118, 'y': 2156, 'width': 322, 'height': 580}`: 144703 pixels (1.91% da tela) ultrapassam o limiar de diferença; ajuste a região x=1118, y=2156, w=322, h=580.
- **P1** `home-1440x900-I6` — Visual difference region at `{'x': 449, 'y': 1598, 'width': 269, 'height': 329}`: 58021 pixels (0.77% da tela) ultrapassam o limiar de diferença; ajuste a região x=449, y=1598, w=269, h=329.
- **P1** `home-1440x900-I7` — Visual difference region at `{'x': 796, 'y': 1603, 'width': 196, 'height': 282}`: 39535 pixels (0.52% da tela) ultrapassam o limiar de diferença; ajuste a região x=796, y=1603, w=196, h=282.
- **P1** `home-1440x900-I8` — Visual difference region at `{'x': 726, 'y': 2156, 'width': 121, 'height': 580}`: 35209 pixels (0.46% da tela) ultrapassam o limiar de diferença; ajuste a região x=726, y=2156, w=121, h=580.
- **P1** `home-1440x900-I9` — Visual difference region at `{'x': 0, 'y': 2748, 'width': 356, 'height': 312}`: 32446 pixels (0.43% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=2748, w=356, h=312.
- **P1** `home-1440x900-I10` — Visual difference region at `{'x': 110, 'y': 3586, 'width': 226, 'height': 274}`: 27804 pixels (0.37% da tela) ultrapassam o limiar de diferença; ajuste a região x=110, y=3586, w=226, h=274.
- **P1** `home-1440x900-I11` — Visual difference region at `{'x': 184, 'y': 2394, 'width': 334, 'height': 244}`: 25798 pixels (0.34% da tela) ultrapassam o limiar de diferença; ajuste a região x=184, y=2394, w=334, h=244.
- **P1** `home-1440x900-I12` — Visual difference region at `{'x': 337, 'y': 3578, 'width': 154, 'height': 245}`: 20301 pixels (0.27% da tela) ultrapassam o limiar de diferença; ajuste a região x=337, y=3578, w=154, h=245.
- **P1** `home-1440x900-I13` — Visual difference region at `{'x': 785, 'y': 2156, 'width': 256, 'height': 134}`: 18405 pixels (0.24% da tela) ultrapassam o limiar de diferença; ajuste a região x=785, y=2156, w=256, h=134.
- **P1** `home-1440x900-I14` — Visual difference region at `{'x': 259, 'y': 2960, 'width': 184, 'height': 163}`: 11745 pixels (0.16% da tela) ultrapassam o limiar de diferença; ajuste a região x=259, y=2960, w=184, h=163.
- **P1** `home-1440x900-I15` — Visual difference region at `{'x': 729, 'y': 1611, 'width': 76, 'height': 282}`: 10370 pixels (0.14% da tela) ultrapassam o limiar de diferença; ajuste a região x=729, y=1611, w=76, h=282.
- **P1** `home-1440x900-I16` — Visual difference region at `{'x': 259, 'y': 3127, 'width': 182, 'height': 165}`: 8852 pixels (0.12% da tela) ultrapassam o limiar de diferença; ajuste a região x=259, y=3127, w=182, h=165.
