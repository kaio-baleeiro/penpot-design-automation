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

Aggregate score: **71.04/100**
Minimum screen score: **71.04/100**
Coverage: **75.72%** (required ≥80%)

Metric table: **penpot-visual-v2**. The detail board presents source, Penpot export and heatmap in readable vertical slices; the full annotated comparison remains available.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **PASS**

Next state: **NEEDS_REVIEW**

## home — 1440×900

- Score: **71.04**; coverage: **75.72%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×5261**; capture: **full_page**
- Similarity evidence: pixel=0.8825, exact=0.5799
- Readable detail board: `home-detail-board.png`; full comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 25 | 75.87 | 18.97 | local foreground IoU=0.773, edge IoU=0.188, bbox IoU=0.973 |
| Spacing/grid | 15 | 51.61 | 7.74 | edge IoU=0.188, regional floor=0.479, row/column MAE=0.110/0.055 |
| Typography | 15 | 72.85 | 10.93 | local dark similarity=0.734, edge IoU=0.188; image-only heuristic |
| Color/border/shadow | 15 | 79.53 | 11.93 | local pixel similarity=0.854, regional floor=0.479 |
| Content/density | 15 | 75.57 | 11.34 | local foreground IoU=0.773, regional floor=0.479 |
| Assets | 15 | 67.59 | 10.14 | local pixel similarity=0.854, edge IoU=0.188; image-only heuristic |

Issues:
- **P0** `home-1440x900-I1` — Visual difference region at `{'x': 255, 'y': 3932, 'width': 930, 'height': 523}`: 470758 pixels (6.21% da tela) ultrapassam o limiar; delta médio=172.2, máximo=253.
- **P2** `home-1440x900-I2` — Visual difference region at `{'x': 232, 'y': 361, 'width': 988, 'height': 375}`: 231915 pixels (3.06% da tela) ultrapassam o limiar; delta médio=104.0, máximo=255.
- **P2** `home-1440x900-I3` — Visual difference region at `{'x': 418, 'y': 1040, 'width': 603, 'height': 400}`: 189899 pixels (2.51% da tela) ultrapassam o limiar; delta médio=132.5, máximo=247.
- **P0** `home-1440x900-I4` — Visual difference region at `{'x': 1118, 'y': 2156, 'width': 322, 'height': 580}`: 144703 pixels (1.91% da tela) ultrapassam o limiar; delta médio=210.1, máximo=255.
- **P2** `home-1440x900-I5` — Visual difference region at `{'x': 0, 'y': 3932, 'width': 242, 'height': 523}`: 123875 pixels (1.64% da tela) ultrapassam o limiar; delta médio=139.8, máximo=255.
- **P2** `home-1440x900-I6` — Visual difference region at `{'x': 1198, 'y': 3932, 'width': 242, 'height': 523}`: 100873 pixels (1.33% da tela) ultrapassam o limiar; delta médio=152.9, máximo=254.
- **P2** `home-1440x900-I7` — Visual difference region at `{'x': 449, 'y': 1522, 'width': 264, 'height': 426}`: 64049 pixels (0.85% da tela) ultrapassam o limiar; delta médio=100.8, máximo=255.
- **P3** `home-1440x900-I8` — Visual difference region at `{'x': 729, 'y': 1524, 'width': 263, 'height': 410}`: 55292 pixels (0.73% da tela) ultrapassam o limiar; delta médio=79.3, máximo=255.
- **P0** `home-1440x900-I9` — Visual difference region at `{'x': 726, 'y': 2156, 'width': 121, 'height': 580}`: 35209 pixels (0.46% da tela) ultrapassam o limiar; delta médio=160.4, máximo=247.
- **P3** `home-1440x900-I10` — Visual difference region at `{'x': 0, 'y': 2748, 'width': 356, 'height': 312}`: 32032 pixels (0.42% da tela) ultrapassam o limiar; delta médio=70.9, máximo=247.
- **P2** `home-1440x900-I11` — Visual difference region at `{'x': 922, 'y': 3581, 'width': 182, 'height': 278}`: 28148 pixels (0.37% da tela) ultrapassam o limiar; delta médio=89.1, máximo=227.
- **P2** `home-1440x900-I12` — Visual difference region at `{'x': 110, 'y': 3586, 'width': 226, 'height': 274}`: 27804 pixels (0.37% da tela) ultrapassam o limiar; delta médio=140.6, máximo=255.
- **P2** `home-1440x900-I13` — Visual difference region at `{'x': 184, 'y': 2394, 'width': 334, 'height': 244}`: 25798 pixels (0.34% da tela) ultrapassam o limiar; delta médio=106.2, máximo=255.
- **P2** `home-1440x900-I14` — Visual difference region at `{'x': 337, 'y': 3578, 'width': 154, 'height': 245}`: 20301 pixels (0.27% da tela) ultrapassam o limiar; delta médio=108.2, máximo=255.
- **P2** `home-1440x900-I15` — Visual difference region at `{'x': 785, 'y': 2156, 'width': 256, 'height': 134}`: 18374 pixels (0.24% da tela) ultrapassam o limiar; delta médio=138.0, máximo=183.
- **P0** `home-1440x900-I16` — Visual difference region at `{'x': 259, 'y': 2960, 'width': 184, 'height': 163}`: 11745 pixels (0.16% da tela) ultrapassam o limiar; delta médio=172.7, máximo=247.
- **P2** `home-1440x900-I17` — Visual difference region at `{'x': 259, 'y': 3127, 'width': 182, 'height': 165}`: 8852 pixels (0.12% da tela) ultrapassam o limiar; delta médio=118.3, máximo=244.
- **P2** `home-1440x900-I18` — Visual difference region at `{'x': 1104, 'y': 3578, 'width': 84, 'height': 250}`: 7601 pixels (0.10% da tela) ultrapassam o limiar; delta médio=110.1, máximo=225.
