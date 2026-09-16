---
type: validation-report
status: complete
created: 2026-09-15
updated: 2026-09-15
source_agent: codex
agent_context: penpot-design-automation
confidence: high
review: false
---

# Penpot validation report — cycle 2

Gate result: **PASS**

Aggregate score: **96.77/100**
Minimum screen score: **96.77/100**
Coverage: **92.07%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Structural gate: **PASS**

Next state: **READY_FOR_USER_REVIEW**

## home — 1440×900

- Score: **96.77**; coverage: **92.07%**; status: **PASS**
- Viewport: **1440×900**; frame: **1440×1807**; capture: **full_page**
- Similarity evidence: pixel=0.9607, exact=0.8107
- Comparison: `home-side-by-side-annotated.png`; overlay: `home-overlay.png`; heatmap: `home-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 99.85 | 29.95 | content bbox IoU=0.998, area similarity=0.998, viewport_match=1 |
| Spacing/grid | 20 | 99.55 | 19.91 | row profile MAE=0.003, column profile MAE=0.005 |
| Typography | 15 | 85.00 | 12.75 | dark density similarity=0.755, row similarity=0.966; image-only heuristic |
| Color/border/shadow | 15 | 94.70 | 14.21 | quantized RGB histogram similarity=0.947 |
| Content/density | 10 | 99.53 | 9.95 | mask coverage=0.994, density similarity=0.998 |
| Assets | 10 | 99.98 | 10.00 | component count similarity=1.000, area similarity=0.999; image-only heuristic |

Issues:
- **P2** `home-1440x900-I1` — Visual difference region at `{'x': 112, 'y': 112, 'width': 250, 'height': 297}`: 61054 pixels (2.35% da tela) ultrapassam o limiar de diferença; ajuste a região x=112, y=112, w=250, h=297.
- **P3** `home-1440x900-I2` — Visual difference region at `{'x': 890, 'y': 17, 'width': 204, 'height': 38}`: 4830 pixels (0.19% da tela) ultrapassam o limiar de diferença; ajuste a região x=890, y=17, w=204, h=38.
- **P3** `home-1440x900-I3` — Visual difference region at `{'x': 1211, 'y': 1313, 'width': 117, 'height': 34}`: 3882 pixels (0.15% da tela) ultrapassam o limiar de diferença; ajuste a região x=1211, y=1313, w=117, h=34.
- **P3** `home-1440x900-I4` — Visual difference region at `{'x': 1224, 'y': 17, 'width': 109, 'height': 38}`: 3607 pixels (0.14% da tela) ultrapassam o limiar de diferença; ajuste a região x=1224, y=17, w=109, h=38.
- **P3** `home-1440x900-I5` — Visual difference region at `{'x': 114, 'y': 717, 'width': 62, 'height': 64}`: 3128 pixels (0.12% da tela) ultrapassam o limiar de diferença; ajuste a região x=114, y=717, w=62, h=64.
- **P3** `home-1440x900-I6` — Visual difference region at `{'x': 1004, 'y': 21, 'width': 91, 'height': 30}`: 2684 pixels (0.10% da tela) ultrapassam o limiar de diferença; ajuste a região x=1004, y=21, w=91, h=30.
