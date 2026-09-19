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

# Penpot validation report — cycle 3

Gate result: **FAIL**

Aggregate score: **64.03/100**
Minimum screen score: **64.03/100**
Coverage: **61.58%** (required ≥80%)

Metric table: **penpot-visual-v2**. The detail board presents source, Penpot export and heatmap in readable vertical slices; the full annotated comparison remains available.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **PASS**

Next state: **NEEDS_REVIEW**

## home — 1440×900

- Score: **64.03**; coverage: **61.58%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×5837**; capture: **frame_bounds**
- Similarity evidence: pixel=0.8665, exact=0.0115
- Readable detail board: `home-detail-board.png`; full comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 25 | 67.85 | 16.96 | local foreground IoU=0.510, edge IoU=0.135, bbox IoU=0.996 |
| Spacing/grid | 15 | 44.04 | 6.61 | edge IoU=0.135, regional floor=0.475, row/column MAE=0.305/0.165 |
| Typography | 15 | 83.47 | 12.52 | local dark similarity=0.959, edge IoU=0.135; image-only heuristic |
| Color/border/shadow | 15 | 72.86 | 10.93 | local pixel similarity=0.843, regional floor=0.475 |
| Content/density | 15 | 56.69 | 8.50 | local foreground IoU=0.510, regional floor=0.475 |
| Assets | 15 | 56.72 | 8.51 | local pixel similarity=0.843, edge IoU=0.135; image-only heuristic |

Issues:
- **P1** `home-1440x900-I1` — Visual difference region at `{'x': 0, 'y': 66, 'width': 1440, 'height': 833}`: 1029166 pixels (12.24% da tela) ultrapassam o limiar; delta médio=95.7, máximo=255.
- **P2** `home-1440x900-I2` — Visual difference region at `{'x': 0, 'y': 1626, 'width': 1440, 'height': 999}`: 424435 pixels (5.05% da tela) ultrapassam o limiar; delta médio=103.8, máximo=255.
- **P2** `home-1440x900-I3` — Visual difference region at `{'x': 0, 'y': 4010, 'width': 1440, 'height': 393}`: 293585 pixels (3.49% da tela) ultrapassam o limiar; delta médio=126.4, máximo=247.
- **P2** `home-1440x900-I4` — Visual difference region at `{'x': 0, 'y': 2977, 'width': 1360, 'height': 908}`: 272232 pixels (3.24% da tela) ultrapassam o limiar; delta médio=92.9, máximo=250.
- **P2** `home-1440x900-I5` — Visual difference region at `{'x': 0, 'y': 900, 'width': 1440, 'height': 511}`: 266030 pixels (3.17% da tela) ultrapassam o limiar; delta médio=89.4, máximo=249.
- **P2** `home-1440x900-I6` — Visual difference region at `{'x': 80, 'y': 3557, 'width': 834, 'height': 323}`: 199752 pixels (2.38% da tela) ultrapassam o limiar; delta médio=107.1, máximo=250.
- **P2** `home-1440x900-I7` — Visual difference region at `{'x': 388, 'y': 4553, 'width': 650, 'height': 238}`: 85929 pixels (1.02% da tela) ultrapassam o limiar; delta médio=105.5, máximo=255.
- **P2** `home-1440x900-I8` — Visual difference region at `{'x': 609, 'y': 2708, 'width': 831, 'height': 195}`: 56871 pixels (0.68% da tela) ultrapassam o limiar; delta médio=82.8, máximo=255.
- **P3** `home-1440x900-I9` — Visual difference region at `{'x': 0, 'y': 2810, 'width': 732, 'height': 308}`: 56552 pixels (0.67% da tela) ultrapassam o limiar; delta médio=63.5, máximo=242.
- **P2** `home-1440x900-I10` — Visual difference region at `{'x': 121, 'y': 2215, 'width': 487, 'height': 289}`: 55895 pixels (0.66% da tela) ultrapassam o limiar; delta médio=121.0, máximo=246.
- **P3** `home-1440x900-I11` — Visual difference region at `{'x': 0, 'y': 1419, 'width': 1440, 'height': 137}`: 48282 pixels (0.57% da tela) ultrapassam o limiar; delta médio=66.2, máximo=199.
- **P2** `home-1440x900-I12` — Visual difference region at `{'x': 82, 'y': 1627, 'width': 624, 'height': 87}`: 10338 pixels (0.12% da tela) ultrapassam o limiar; delta médio=92.7, máximo=199.
- **P0** `home-1440x900-I13` — Visual difference region at `{'x': 104, 'y': 3264, 'width': 152, 'height': 67}`: 9609 pixels (0.11% da tela) ultrapassam o limiar; delta médio=160.8, máximo=238.
- **P2** `home-1440x900-I14` — Visual difference region at `{'x': 476, 'y': 2233, 'width': 138, 'height': 133}`: 9289 pixels (0.11% da tela) ultrapassam o limiar; delta médio=95.6, máximo=243.
- **P2** `home-1440x900-I15` — Visual difference region at `{'x': 1103, 'y': 11, 'width': 321, 'height': 44}`: 8881 pixels (0.11% da tela) ultrapassam o limiar; delta médio=106.1, máximo=255.
- **P0** `home-1440x900-I16` — Visual difference region at `{'x': 650, 'y': 2675, 'width': 140, 'height': 67}`: 8566 pixels (0.10% da tela) ultrapassam o limiar; delta médio=166.8, máximo=255.
