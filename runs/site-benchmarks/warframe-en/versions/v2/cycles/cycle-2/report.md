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

# Penpot validation report — cycle 2

Gate result: **FAIL**

Aggregate score: **71.94/100**
Minimum screen score: **71.94/100**
Coverage: **65.70%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **PASS**

Next state: **REFINEMENT**

## home — 1440×900

- Score: **71.94**; coverage: **65.70%**; status: **FAIL**
- Viewport: **1440×900**; frame: **1440×5837**; capture: **bounded_state**
- Similarity evidence: pixel=0.8684, exact=0.0005
- Comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 79.28 | 23.78 | content bbox IoU=0.770, area similarity=0.770, viewport_match=1 |
| Spacing/grid | 20 | 65.53 | 13.11 | row profile MAE=0.387, column profile MAE=0.303 |
| Typography | 15 | 94.32 | 14.15 | dark density similarity=0.959, row similarity=0.925; image-only heuristic |
| Color/border/shadow | 15 | 74.41 | 11.16 | quantized RGB histogram similarity=0.744 |
| Content/density | 10 | 56.59 | 5.66 | mask coverage=0.608, density similarity=0.503 |
| Assets | 10 | 40.77 | 4.08 | component count similarity=0.333, area similarity=0.519; image-only heuristic |

Issues:
- **P1** `home-1440x900-I1` — Visual difference region at `{'x': 0, 'y': 66, 'width': 1440, 'height': 1332}`: 1266957 pixels (15.07% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=66, w=1440, h=1332.
- **P1** `home-1440x900-I2` — Visual difference region at `{'x': 0, 'y': 1706, 'width': 1440, 'height': 919}`: 494213 pixels (5.88% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=1706, w=1440, h=919.
- **P1** `home-1440x900-I3` — Visual difference region at `{'x': 0, 'y': 4012, 'width': 1440, 'height': 391}`: 258877 pixels (3.08% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=4012, w=1440, h=391.
- **P1** `home-1440x900-I4` — Visual difference region at `{'x': 113, 'y': 3664, 'width': 387, 'height': 215}`: 75307 pixels (0.90% da tela) ultrapassam o limiar de diferença; ajuste a região x=113, y=3664, w=387, h=215.
- **P1** `home-1440x900-I5` — Visual difference region at `{'x': 690, 'y': 3073, 'width': 433, 'height': 510}`: 58553 pixels (0.70% da tela) ultrapassam o limiar de diferença; ajuste a região x=690, y=3073, w=433, h=510.
- **P1** `home-1440x900-I6` — Visual difference region at `{'x': 0, 'y': 1421, 'width': 1440, 'height': 135}`: 49286 pixels (0.59% da tela) ultrapassam o limiar de diferença; ajuste a região x=0, y=1421, w=1440, h=135.
- **P1** `home-1440x900-I7` — Visual difference region at `{'x': 526, 'y': 3675, 'width': 388, 'height': 201}`: 48498 pixels (0.58% da tela) ultrapassam o limiar de diferença; ajuste a região x=526, y=3675, w=388, h=201.
- **P1** `home-1440x900-I8` — Visual difference region at `{'x': 80, 'y': 3585, 'width': 1280, 'height': 194}`: 47438 pixels (0.56% da tela) ultrapassam o limiar de diferença; ajuste a região x=80, y=3585, w=1280, h=194.
- **P1** `home-1440x900-I9` — Visual difference region at `{'x': 697, 'y': 2734, 'width': 743, 'height': 169}`: 46890 pixels (0.56% da tela) ultrapassam o limiar de diferença; ajuste a região x=697, y=2734, w=743, h=169.
- **P1** `home-1440x900-I10` — Visual difference region at `{'x': 406, 'y': 4573, 'width': 306, 'height': 172}`: 44709 pixels (0.53% da tela) ultrapassam o limiar de diferença; ajuste a região x=406, y=4573, w=306, h=172.
- **P1** `home-1440x900-I11` — Visual difference region at `{'x': 1063, 'y': 3665, 'width': 264, 'height': 219}`: 38087 pixels (0.45% da tela) ultrapassam o limiar de diferença; ajuste a região x=1063, y=3665, w=264, h=219.
- **P1** `home-1440x900-I12` — Visual difference region at `{'x': 539, 'y': 3336, 'width': 360, 'height': 254}`: 30325 pixels (0.36% da tela) ultrapassam o limiar de diferença; ajuste a região x=539, y=3336, w=360, h=254.
- **P1** `home-1440x900-I13` — Visual difference region at `{'x': 133, 'y': 2215, 'width': 276, 'height': 230}`: 29996 pixels (0.36% da tela) ultrapassam o limiar de diferença; ajuste a região x=133, y=2215, w=276, h=230.
- **P1** `home-1440x900-I14` — Visual difference region at `{'x': 1161, 'y': 705, 'width': 279, 'height': 95}`: 15199 pixels (0.18% da tela) ultrapassam o limiar de diferença; ajuste a região x=1161, y=705, w=279, h=95.
- **P1** `home-1440x900-I15` — Visual difference region at `{'x': 732, 'y': 4573, 'width': 306, 'height': 172}`: 11001 pixels (0.13% da tela) ultrapassam o limiar de diferença; ajuste a região x=732, y=4573, w=306, h=172.
- **P1** `home-1440x900-I16` — Visual difference region at `{'x': 743, 'y': 4587, 'width': 189, 'height': 137}`: 10443 pixels (0.12% da tela) ultrapassam o limiar de diferença; ajuste a região x=743, y=4587, w=189, h=137.
- **P1** `home-1440x900-I17` — Visual difference region at `{'x': 476, 'y': 2233, 'width': 138, 'height': 134}`: 9114 pixels (0.11% da tela) ultrapassam o limiar de diferença; ajuste a região x=476, y=2233, w=138, h=134.
- **P1** `home-1440x900-I18` — Regression against previous cycle: Score caiu de 78.94 para 71.94; revisar antes de aprovar.

## Regression gate

The cycle is not approved because at least one screen regressed against the prior cycle.
