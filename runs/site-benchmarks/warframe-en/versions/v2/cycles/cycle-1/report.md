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

# Penpot validation report — cycle 1

Gate result: **FAIL**

Aggregate score: **78.94/100**
Minimum screen score: **78.94/100**
Coverage: **66.16%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **FAIL**

Structural blockers:
- inventory missing required keys: component_instances, detached_instances, styles, required_component_instances

Next state: **REFINEMENT**

## home — 1440×900

- Score: **78.94**; coverage: **66.16%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×5837**; capture: **bounded_state**
- Similarity evidence: pixel=0.8563, exact=0.0014
- Comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 89.48 | 26.84 | content bbox IoU=0.883, area similarity=0.883, viewport_match=1 |
| Spacing/grid | 20 | 73.93 | 14.79 | row profile MAE=0.444, column profile MAE=0.077 |
| Typography | 15 | 94.26 | 14.14 | dark density similarity=0.956, row similarity=0.926; image-only heuristic |
| Color/border/shadow | 15 | 60.75 | 9.11 | quantized RGB histogram similarity=0.608 |
| Content/density | 10 | 71.27 | 7.13 | mask coverage=0.555, density similarity=0.950 |
| Assets | 10 | 69.36 | 6.94 | component count similarity=0.500, area similarity=0.984; image-only heuristic |

Issues:
- **P1** `home-1440x900-I1` — Visual difference region at `{'x': 0, 'y': 80, 'width': 1440, 'height': 1318}`: 1085000 pixels (12.91% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=80, w=1440, h=1318.
- **P1** `home-1440x900-I2` — Visual difference region at `{'x': 0, 'y': 1613, 'width': 1440, 'height': 1012}`: 508690 pixels (6.05% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=1613, w=1440, h=1012.
- **P1** `home-1440x900-I3` — Visual difference region at `{'x': 0, 'y': 4009, 'width': 1440, 'height': 394}`: 287229 pixels (3.42% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=4009, w=1440, h=394.
- **P1** `home-1440x900-I4` — Visual difference region at `{'x': 112, 'y': 3665, 'width': 389, 'height': 213}`: 74707 pixels (0.89% da tela) ultrapassam o limiar de diferença; ajuste a região x=112, y=3665, w=389, h=213.
- **P1** `home-1440x900-I5` — Visual difference region at `{'x': 692, 'y': 3073, 'width': 403, 'height': 505}`: 52682 pixels (0.63% da tela) ultrapassam o limiar de diferença; ajuste a região x=692, y=3073, w=403, h=505.
- **P1** `home-1440x900-I6` — Visual difference region at `{'x': 526, 'y': 3675, 'width': 388, 'height': 200}`: 45523 pixels (0.54% da tela) ultrapassam o limiar de diferença; ajuste a região x=526, y=3675, w=388, h=200.
- **P1** `home-1440x900-I7` — Visual difference region at `{'x': 321, 'y': 0, 'width': 1119, 'height': 68}`: 44894 pixels (0.53% da tela) ultrapassam o limiar de diferença; ajuste a região x=321, y=0, w=1119, h=68.
- **P1** `home-1440x900-I8` — Visual difference region at `{'x': 797, 'y': 2712, 'width': 643, 'height': 191}`: 43079 pixels (0.51% da tela) ultrapassam o limiar de diferença; ajuste a região x=797, y=2712, w=643, h=191.
- **P1** `home-1440x900-I9` — Visual difference region at `{'x': 406, 'y': 4573, 'width': 306, 'height': 172}`: 42924 pixels (0.51% da tela) ultrapassam o limiar de diferença; ajuste a região x=406, y=4573, w=306, h=172.
- **P1** `home-1440x900-I10` — Visual difference region at `{'x': 0, 'y': 1420, 'width': 1440, 'height': 136}`: 38492 pixels (0.46% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=1420, w=1440, h=136.
- **P1** `home-1440x900-I11` — Visual difference region at `{'x': 525, 'y': 3888, 'width': 390, 'height': 96}`: 36100 pixels (0.43% da tela) ultrapassam o limiar de diferença; ajuste a região x=525, y=3888, w=390, h=96.
- **P1** `home-1440x900-I12` — Visual difference region at `{'x': 939, 'y': 3888, 'width': 389, 'height': 96}`: 35510 pixels (0.42% da tela) ultrapassam o limiar de diferença; ajuste a região x=939, y=3888, w=389, h=96.
- **P1** `home-1440x900-I13` — Visual difference region at `{'x': 112, 'y': 3890, 'width': 389, 'height': 94}`: 35431 pixels (0.42% da tela) ultrapassam o limiar de diferença; ajuste a região x=112, y=3890, w=389, h=94.
- **P1** `home-1440x900-I14` — Visual difference region at `{'x': 1057, 'y': 3665, 'width': 271, 'height': 219}`: 35101 pixels (0.42% da tela) ultrapassam o limiar de diferença; ajuste a região x=1057, y=3665, w=271, h=219.
- **P1** `home-1440x900-I15` — Visual difference region at `{'x': 1176, 'y': 78, 'width': 264, 'height': 300}`: 33041 pixels (0.39% da tela) ultrapassam o limiar de diferença; ajuste a região x=1176, y=78, w=264, h=300.
- **P1** `home-1440x900-I16` — Visual difference region at `{'x': 149, 'y': 2215, 'width': 260, 'height': 256}`: 29576 pixels (0.35% da tela) ultrapassam o limiar de diferença; ajuste a região x=149, y=2215, w=260, h=256.
- **P1** `home-1440x900-I17` — Visual difference region at `{'x': 0, 'y': 78, 'width': 240, 'height': 300}`: 26980 pixels (0.32% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=78, w=240, h=300.
- **P1** `home-1440x900-I18` — Visual difference region at `{'x': 80, 'y': 3585, 'width': 1280, 'height': 168}`: 21374 pixels (0.25% da tela) ultrapassam o limiar de diferença; ajuste a região x=80, y=3585, w=1280, h=168.
- **P1** `home-1440x900-I19` — Visual difference region at `{'x': 676, 'y': 3378, 'width': 222, 'height': 210}`: 19624 pixels (0.23% da tela) ultrapassam o limiar de diferença; ajuste a região x=676, y=3378, w=222, h=210.
- **P1** `home-1440x900-I20` — Visual difference region at `{'x': 757, 'y': 1321, 'width': 231, 'height': 44}`: 10060 pixels (0.12% da tela) ultrapassam o limiar de diferença; ajuste a região x=757, y=1321, w=231, h=44.
