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

Aggregate score: **71.08/100**
Minimum screen score: **71.08/100**
Coverage: **76.83%** (required ≥80%)

Metric table: **penpot-visual-v2**. The detail board presents source, Penpot export and heatmap in readable vertical slices; the full annotated comparison remains available.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **PASS**

Next state: **REFINEMENT**

## home — 1440×900

- Score: **71.08**; coverage: **76.83%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×5261**; capture: **full_page**
- Similarity evidence: pixel=0.8853, exact=0.5912
- Readable detail board: `home-detail-board.png`; full comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 25 | 75.90 | 18.98 | local foreground IoU=0.772, edge IoU=0.190, bbox IoU=0.973 |
| Spacing/grid | 15 | 51.63 | 7.74 | edge IoU=0.190, regional floor=0.479, row/column MAE=0.112/0.057 |
| Typography | 15 | 72.85 | 10.93 | local dark similarity=0.734, edge IoU=0.190; image-only heuristic |
| Color/border/shadow | 15 | 79.64 | 11.95 | local pixel similarity=0.857, regional floor=0.479 |
| Content/density | 15 | 75.45 | 11.32 | local foreground IoU=0.772, regional floor=0.479 |
| Assets | 15 | 67.78 | 10.17 | local pixel similarity=0.857, edge IoU=0.190; image-only heuristic |

Issues:
- **P0** `home-1440x900-I1` — Visual difference region at `{'x': 255, 'y': 3932, 'width': 930, 'height': 523}`: 470758 pixels (6.21% da tela) ultrapassam o limiar; delta médio=172.2, máximo=253.
- **P2** `home-1440x900-I2` — Visual difference region at `{'x': 418, 'y': 1040, 'width': 603, 'height': 400}`: 176576 pixels (2.33% da tela) ultrapassam o limiar; delta médio=134.8, máximo=247.
- **P2** `home-1440x900-I3` — Visual difference region at `{'x': 232, 'y': 370, 'width': 988, 'height': 291}`: 172188 pixels (2.27% da tela) ultrapassam o limiar; delta médio=111.9, máximo=255.
- **P0** `home-1440x900-I4` — Visual difference region at `{'x': 1118, 'y': 2156, 'width': 322, 'height': 580}`: 144703 pixels (1.91% da tela) ultrapassam o limiar; delta médio=210.1, máximo=255.
- **P2** `home-1440x900-I5` — Visual difference region at `{'x': 0, 'y': 3932, 'width': 242, 'height': 523}`: 123875 pixels (1.64% da tela) ultrapassam o limiar; delta médio=139.8, máximo=255.
- **P2** `home-1440x900-I6` — Visual difference region at `{'x': 1198, 'y': 3932, 'width': 242, 'height': 523}`: 100873 pixels (1.33% da tela) ultrapassam o limiar; delta médio=152.9, máximo=254.
- **P2** `home-1440x900-I7` — Visual difference region at `{'x': 470, 'y': 1607, 'width': 240, 'height': 296}`: 50287 pixels (0.66% da tela) ultrapassam o limiar; delta médio=98.8, máximo=255.
- **P3** `home-1440x900-I8` — Visual difference region at `{'x': 796, 'y': 1603, 'width': 196, 'height': 282}`: 39535 pixels (0.52% da tela) ultrapassam o limiar; delta médio=74.2, máximo=244.
- **P0** `home-1440x900-I9` — Visual difference region at `{'x': 726, 'y': 2156, 'width': 121, 'height': 580}`: 35209 pixels (0.46% da tela) ultrapassam o limiar; delta médio=160.4, máximo=247.
- **P3** `home-1440x900-I10` — Visual difference region at `{'x': 0, 'y': 2748, 'width': 356, 'height': 312}`: 32032 pixels (0.42% da tela) ultrapassam o limiar; delta médio=70.9, máximo=247.
- **P2** `home-1440x900-I11` — Visual difference region at `{'x': 922, 'y': 3581, 'width': 182, 'height': 278}`: 28148 pixels (0.37% da tela) ultrapassam o limiar; delta médio=89.1, máximo=227.
- **P2** `home-1440x900-I12` — Visual difference region at `{'x': 110, 'y': 3586, 'width': 226, 'height': 274}`: 27804 pixels (0.37% da tela) ultrapassam o limiar; delta médio=140.6, máximo=255.
- **P2** `home-1440x900-I13` — Visual difference region at `{'x': 184, 'y': 2394, 'width': 334, 'height': 244}`: 25798 pixels (0.34% da tela) ultrapassam o limiar; delta médio=106.2, máximo=255.
- **P2** `home-1440x900-I14` — Visual difference region at `{'x': 337, 'y': 3578, 'width': 154, 'height': 245}`: 20301 pixels (0.27% da tela) ultrapassam o limiar; delta médio=108.2, máximo=255.
- **P2** `home-1440x900-I15` — Visual difference region at `{'x': 785, 'y': 2156, 'width': 256, 'height': 134}`: 18374 pixels (0.24% da tela) ultrapassam o limiar; delta médio=138.0, máximo=183.
- **P0** `home-1440x900-I16` — Visual difference region at `{'x': 259, 'y': 2960, 'width': 184, 'height': 163}`: 11745 pixels (0.16% da tela) ultrapassam o limiar; delta médio=172.7, máximo=247.
- **P3** `home-1440x900-I17` — Visual difference region at `{'x': 731, 'y': 1611, 'width': 74, 'height': 282}`: 10086 pixels (0.13% da tela) ultrapassam o limiar; delta médio=76.9, máximo=208.
- **P2** `home-1440x900-I18` — Visual difference region at `{'x': 259, 'y': 3127, 'width': 182, 'height': 165}`: 8852 pixels (0.12% da tela) ultrapassam o limiar; delta médio=118.3, máximo=244.
- **P2** `home-1440x900-I19` — Visual difference region at `{'x': 1104, 'y': 3578, 'width': 84, 'height': 250}`: 7601 pixels (0.10% da tela) ultrapassam o limiar; delta médio=110.1, máximo=225.
