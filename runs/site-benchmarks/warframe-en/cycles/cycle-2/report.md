---
type: validation-report
status: needs-review
created: 2026-09-17
updated: 2026-09-17
source_agent: codex
agent_context: penpot-design-automation
confidence: high
review: true
---

# Penpot validation report — cycle 2

Gate result: **FAIL**

Aggregate score: **65.38/100**
Minimum screen score: **65.38/100**
Coverage: **56.65%** (required ≥80%)

Metric table: **penpot-visual-v2**. The detail board presents source, Penpot export and heatmap in readable vertical slices; the full annotated comparison remains available.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **PASS**

Next state: **REFINEMENT**

## home — 1440×900

- Score: **65.38**; coverage: **56.65%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×5837**; capture: **frame_bounds**
- Similarity evidence: pixel=0.8602, exact=0.0113
- Readable detail board: `home-detail-board.png`; full comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 25 | 69.69 | 17.42 | local foreground IoU=0.576, edge IoU=0.128, bbox IoU=0.996 |
| Spacing/grid | 15 | 46.59 | 6.99 | edge IoU=0.128, regional floor=0.490, row/column MAE=0.255/0.076 |
| Typography | 15 | 83.29 | 12.49 | local dark similarity=0.957, edge IoU=0.128; image-only heuristic |
| Color/border/shadow | 15 | 69.80 | 10.47 | local pixel similarity=0.838, regional floor=0.490 |
| Content/density | 15 | 63.13 | 9.47 | local foreground IoU=0.576, regional floor=0.490 |
| Assets | 15 | 56.93 | 8.54 | local pixel similarity=0.838, edge IoU=0.128; image-only heuristic |

Issues:
- **P1** `home-1440x900-I1` — Visual difference region at `{'x': 0, 'y': 66, 'width': 1440, 'height': 833}`: 1029166 pixels (12.24% da tela) ultrapassam o limiar; delta médio=95.7, máximo=255.
- **P2** `home-1440x900-I2` — Visual difference region at `{'x': 0, 'y': 1599, 'width': 1440, 'height': 1050}`: 633814 pixels (7.54% da tela) ultrapassam o limiar; delta médio=94.1, máximo=255.
- **P2** `home-1440x900-I3` — Visual difference region at `{'x': 0, 'y': 2977, 'width': 1360, 'height': 908}`: 488271 pixels (5.81% da tela) ultrapassam o limiar; delta médio=90.4, máximo=250.
- **P2** `home-1440x900-I4` — Visual difference region at `{'x': 0, 'y': 4010, 'width': 1440, 'height': 393}`: 293585 pixels (3.49% da tela) ultrapassam o limiar; delta médio=126.4, máximo=247.
- **P2** `home-1440x900-I5` — Visual difference region at `{'x': 0, 'y': 900, 'width': 1440, 'height': 511}`: 266030 pixels (3.17% da tela) ultrapassam o limiar; delta médio=89.4, máximo=249.
- **P2** `home-1440x900-I6` — Visual difference region at `{'x': 80, 'y': 4460, 'width': 1170, 'height': 484}`: 266027 pixels (3.16% da tela) ultrapassam o limiar; delta médio=95.5, máximo=255.
- **P2** `home-1440x900-I7` — Visual difference region at `{'x': 82, 'y': 1597, 'width': 625, 'height': 446}`: 168013 pixels (2.00% da tela) ultrapassam o limiar; delta médio=86.0, máximo=248.
- **P3** `home-1440x900-I8` — Visual difference region at `{'x': 0, 'y': 2810, 'width': 732, 'height': 308}`: 56552 pixels (0.67% da tela) ultrapassam o limiar; delta médio=63.5, máximo=242.
- **P3** `home-1440x900-I9` — Visual difference region at `{'x': 609, 'y': 2728, 'width': 831, 'height': 175}`: 54121 pixels (0.64% da tela) ultrapassam o limiar; delta médio=77.6, máximo=242.
- **P3** `home-1440x900-I10` — Visual difference region at `{'x': 0, 'y': 1419, 'width': 1440, 'height': 137}`: 48282 pixels (0.57% da tela) ultrapassam o limiar; delta médio=66.2, máximo=199.
- **P0** `home-1440x900-I11` — Visual difference region at `{'x': 104, 'y': 3264, 'width': 152, 'height': 67}`: 9609 pixels (0.11% da tela) ultrapassam o limiar; delta médio=160.8, máximo=238.
- **P2** `home-1440x900-I12` — Visual difference region at `{'x': 1103, 'y': 11, 'width': 321, 'height': 44}`: 8881 pixels (0.11% da tela) ultrapassam o limiar; delta médio=106.1, máximo=255.
