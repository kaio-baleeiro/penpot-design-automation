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

# Penpot validation report — cycle 1

Gate result: **FAIL**

Aggregate score: **83.79/100**
Minimum screen score: **83.79/100**
Coverage: **93.46%** (required ≥80%)

Metric table: **penpot-visual-v2**. The detail board presents source, Penpot export and heatmap in readable vertical slices; the full annotated comparison remains available.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **PASS**

Next state: **REFINEMENT**

## home — 1440×900

- Score: **83.79**; coverage: **93.46%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×1807**; capture: **full_page**
- Similarity evidence: pixel=0.9720, exact=0.8654
- Readable detail board: `home-detail-board.png`; full comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 25 | 85.64 | 21.41 | local foreground IoU=0.997, edge IoU=0.286, bbox IoU=1.000 |
| Spacing/grid | 15 | 66.31 | 9.95 | edge IoU=0.286, regional floor=0.797, row/column MAE=0.001/0.002 |
| Typography | 15 | 83.26 | 12.49 | local dark similarity=0.893, edge IoU=0.286; image-only heuristic |
| Color/border/shadow | 15 | 94.05 | 14.11 | local pixel similarity=0.975, regional floor=0.797 |
| Content/density | 15 | 94.76 | 14.21 | local foreground IoU=0.997, regional floor=0.797 |
| Assets | 15 | 77.47 | 11.62 | local pixel similarity=0.975, edge IoU=0.286; image-only heuristic |

Issues:
- **P0** `home-1440x900-I1` — Visual difference region at `{'x': 436, 'y': 1283, 'width': 892, 'height': 64}`: 7854 pixels (0.30% da tela) ultrapassam o limiar; delta médio=195.9, máximo=246.
- **P3** `home-1440x900-I2` — Visual difference region at `{'x': 126, 'y': 263, 'width': 235, 'height': 146}`: 5024 pixels (0.19% da tela) ultrapassam o limiar; delta médio=78.1, máximo=237.
- **P3** `home-1440x900-I3` — Visual difference region at `{'x': 118, 'y': 158, 'width': 180, 'height': 176}`: 4659 pixels (0.18% da tela) ultrapassam o limiar; delta médio=59.0, máximo=182.
- **P2** `home-1440x900-I4` — Visual difference region at `{'x': 110, 'y': 678, 'width': 69, 'height': 103}`: 3780 pixels (0.15% da tela) ultrapassam o limiar; delta médio=111.0, máximo=224.
- **P2** `home-1440x900-I5` — Visual difference region at `{'x': 0, 'y': 71, 'width': 1440, 'height': 2}`: 2880 pixels (0.11% da tela) ultrapassam o limiar; delta médio=135.0, máximo=230.
