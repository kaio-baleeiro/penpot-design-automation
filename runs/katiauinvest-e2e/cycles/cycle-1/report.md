---
type: validation-report
status: needs-review
created: 2026-09-14
updated: 2026-09-14
source_agent: codex
agent_context: penpot-design-automation
confidence: high
review: true
---

# Penpot validation report — cycle 1

Decision: **NEEDS_REVIEW**

Aggregate score: **90.31/100**
Minimum screen score: **88.15/100**
Coverage: **88.51%** (required ≥80%)

Metric table: **penpot-visual-v1**. The annotated side-by-side artifact shows source on the left and Penpot export on the right. Red boxes identify actionable difference regions.

The six metrics are deterministic image heuristics. They cannot prove font family, semantic copy, asset provenance, or editable Penpot structure without DOM/Penpot metadata.

Next state: **REFINEMENT**

## dashboard — 1440×900

- Score: **88.42**; coverage: **76.91%**; status: **FAIL**
- Similarity evidence: pixel=0.9195, exact=0.0078
- Comparison: `dashboard-side-by-side-annotated.png`; overlay: `dashboard-overlay.png`; heatmap: `dashboard-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 99.80 | 29.94 | content bbox IoU=0.998, area similarity=0.998, viewport_match=1 |
| Spacing/grid | 20 | 78.05 | 15.61 | row profile MAE=0.272, column profile MAE=0.167 |
| Typography | 15 | 98.07 | 14.71 | dark density similarity=0.995, row similarity=0.963; image-only heuristic |
| Color/border/shadow | 15 | 83.89 | 12.58 | quantized RGB histogram similarity=0.839 |
| Content/density | 10 | 69.80 | 6.98 | mask coverage=0.563, density similarity=0.901 |
| Assets | 10 | 85.99 | 8.60 | component count similarity=0.867, area similarity=0.850; image-only heuristic |

Issues:
- **P1** `dashboard-1440x900-I1` — Visual difference region at `{'x': 110, 'y': 572, 'width': 799, 'height': 251}`: 64621 pixels (4.99% da tela) ultrapassam o limiar de diferença; ajuste a região x=110, y=572, w=799, h=251.
- **P1** `dashboard-1440x900-I2` — Visual difference region at `{'x': 84, 'y': 256, 'width': 379, 'height': 198}`: 42110 pixels (3.25% da tela) ultrapassam o limiar de diferença; ajuste a região x=84, y=256, w=379, h=198.
- **P1** `dashboard-1440x900-I3` — Visual difference region at `{'x': 547, 'y': 640, 'width': 168, 'height': 119}`: 15312 pixels (1.18% da tela) ultrapassam o limiar de diferença; ajuste a região x=547, y=640, w=168, h=119.
- **P1** `dashboard-1440x900-I4` — Visual difference region at `{'x': 722, 'y': 641, 'width': 170, 'height': 88}`: 13175 pixels (1.02% da tela) ultrapassam o limiar de diferença; ajuste a região x=722, y=641, w=170, h=88.
- **P1** `dashboard-1440x900-I5` — Visual difference region at `{'x': 550, 'y': 559, 'width': 165, 'height': 84}`: 12529 pixels (0.97% da tela) ultrapassam o limiar de diferença; ajuste a região x=550, y=559, w=165, h=84.
- **P1** `dashboard-1440x900-I6` — Visual difference region at `{'x': 126, 'y': 558, 'width': 244, 'height': 39}`: 9132 pixels (0.70% da tela) ultrapassam o limiar de diferença; ajuste a região x=126, y=558, w=244, h=39.
- **P1** `dashboard-1440x900-I7` — Visual difference region at `{'x': 1159, 'y': 127, 'width': 181, 'height': 44}`: 7428 pixels (0.57% da tela) ultrapassam o limiar de diferença; ajuste a região x=1159, y=127, w=181, h=44.
- **P1** `dashboard-1440x900-I8` — Visual difference region at `{'x': 1167, 'y': 179, 'width': 181, 'height': 44}`: 7221 pixels (0.56% da tela) ultrapassam o limiar de diferença; ajuste a região x=1167, y=179, w=181, h=44.
- **P1** `dashboard-1440x900-I9` — Visual difference region at `{'x': 952, 'y': 131, 'width': 198, 'height': 36}`: 6798 pixels (0.52% da tela) ultrapassam o limiar de diferença; ajuste a região x=952, y=131, w=198, h=36.
- **P1** `dashboard-1440x900-I10` — Visual difference region at `{'x': 723, 'y': 597, 'width': 169, 'height': 49}`: 6740 pixels (0.52% da tela) ultrapassam o limiar de diferença; ajuste a região x=723, y=597, w=169, h=49.
- **P1** `dashboard-1440x900-I11` — Visual difference region at `{'x': 378, 'y': 559, 'width': 164, 'height': 38}`: 6156 pixels (0.47% da tela) ultrapassam o limiar de diferença; ajuste a região x=378, y=559, w=164, h=38.
- **P1** `dashboard-1440x900-I12` — Visual difference region at `{'x': 961, 'y': 187, 'width': 196, 'height': 28}`: 5341 pixels (0.41% da tela) ultrapassam o limiar de diferença; ajuste a região x=961, y=187, w=196, h=28.
- **P1** `dashboard-1440x900-I13` — Visual difference region at `{'x': 117, 'y': 837, 'width': 150, 'height': 37}`: 5246 pixels (0.40% da tela) ultrapassam o limiar de diferença; ajuste a região x=117, y=837, w=150, h=37.
- **P1** `dashboard-1440x900-I14` — Visual difference region at `{'x': 126, 'y': 843, 'width': 774, 'height': 41}`: 4842 pixels (0.37% da tela) ultrapassam o limiar de diferença; ajuste a região x=126, y=843, w=774, h=41.
- **P1** `dashboard-1440x900-I15` — Visual difference region at `{'x': 110, 'y': 442, 'width': 816, 'height': 39}`: 3226 pixels (0.25% da tela) ultrapassam o limiar de diferença; ajuste a região x=110, y=442, w=816, h=39.
- **P1** `dashboard-1440x900-I16` — Visual difference region at `{'x': 183, 'y': 140, 'width': 140, 'height': 39}`: 2733 pixels (0.21% da tela) ultrapassam o limiar de diferença; ajuste a região x=183, y=140, w=140, h=39.
- **P1** `dashboard-1440x900-I17` — Visual difference region at `{'x': 778, 'y': 321, 'width': 118, 'height': 35}`: 2228 pixels (0.17% da tela) ultrapassam o limiar de diferença; ajuste a região x=778, y=321, w=118, h=35.
- **P1** `dashboard-1440x900-I18` — Visual difference region at `{'x': 148, 'y': 190, 'width': 106, 'height': 38}`: 2125 pixels (0.16% da tela) ultrapassam o limiar de diferença; ajuste a região x=148, y=190, w=106, h=38.
- **P1** `dashboard-1440x900-I19` — Visual difference region at `{'x': 540, 'y': 364, 'width': 126, 'height': 30}`: 1947 pixels (0.15% da tela) ultrapassam o limiar de diferença; ajuste a região x=540, y=364, w=126, h=30.
- **P1** `dashboard-1440x900-I20` — Visual difference region at `{'x': 960, 'y': 880, 'width': 369, 'height': 20}`: 1891 pixels (0.15% da tela) ultrapassam o limiar de diferença; ajuste a região x=960, y=880, w=369, h=20.

## investments — 1440×900

- Score: **90.70**; coverage: **91.28%**; status: **PASS**
- Similarity evidence: pixel=0.9546, exact=0.0676
- Comparison: `investments-side-by-side-annotated.png`; overlay: `investments-overlay.png`; heatmap: `investments-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 99.80 | 29.94 | content bbox IoU=0.998, area similarity=0.998, viewport_match=1 |
| Spacing/grid | 20 | 80.13 | 16.03 | row profile MAE=0.250, column profile MAE=0.148 |
| Typography | 15 | 98.94 | 14.84 | dark density similarity=0.992, row similarity=0.986; image-only heuristic |
| Color/border/shadow | 15 | 94.18 | 14.13 | quantized RGB histogram similarity=0.942 |
| Content/density | 10 | 73.78 | 7.38 | mask coverage=0.649, density similarity=0.871 |
| Assets | 10 | 83.89 | 8.39 | component count similarity=0.857, area similarity=0.812; image-only heuristic |

Issues:
- **P3** `investments-1440x900-I1` — Visual difference region at `{'x': 85, 'y': 258, 'width': 1105, 'height': 44}`: 5789 pixels (0.45% da tela) ultrapassam o limiar de diferença; ajuste a região x=85, y=258, w=1105, h=44.
- **P3** `investments-1440x900-I2` — Visual difference region at `{'x': 97, 'y': 265, 'width': 1263, 'height': 41}`: 5249 pixels (0.41% da tela) ultrapassam o limiar de diferença; ajuste a região x=97, y=265, w=1263, h=41.
- **P3** `investments-1440x900-I3` — Visual difference region at `{'x': 87, 'y': 140, 'width': 284, 'height': 38}`: 5156 pixels (0.40% da tela) ultrapassam o limiar de diferença; ajuste a região x=87, y=140, w=284, h=38.
- **P3** `investments-1440x900-I4` — Visual difference region at `{'x': 1058, 'y': 343, 'width': 142, 'height': 96}`: 3232 pixels (0.25% da tela) ultrapassam o limiar de diferença; ajuste a região x=1058, y=343, w=142, h=96.
- **P3** `investments-1440x900-I5` — Visual difference region at `{'x': 463, 'y': 139, 'width': 151, 'height': 39}`: 2935 pixels (0.23% da tela) ultrapassam o limiar de diferença; ajuste a região x=463, y=139, w=151, h=39.
- **P3** `investments-1440x900-I6` — Visual difference region at `{'x': 766, 'y': 375, 'width': 137, 'height': 38}`: 2826 pixels (0.22% da tela) ultrapassam o limiar de diferença; ajuste a região x=766, y=375, w=137, h=38.
- **P3** `investments-1440x900-I7` — Visual difference region at `{'x': 161, 'y': 375, 'width': 131, 'height': 38}`: 2580 pixels (0.20% da tela) ultrapassam o limiar de diferença; ajuste a região x=161, y=375, w=131, h=38.
- **P3** `investments-1440x900-I8` — Visual difference region at `{'x': 525, 'y': 375, 'width': 137, 'height': 38}`: 2546 pixels (0.20% da tela) ultrapassam o limiar de diferença; ajuste a região x=525, y=375, w=137, h=38.
- **P3** `investments-1440x900-I9` — Visual difference region at `{'x': 84, 'y': 323, 'width': 332, 'height': 136}`: 2462 pixels (0.19% da tela) ultrapassam o limiar de diferença; ajuste a região x=84, y=323, w=332, h=136.
- **P3** `investments-1440x900-I10` — Visual difference region at `{'x': 418, 'y': 324, 'width': 32, 'height': 134}`: 2103 pixels (0.16% da tela) ultrapassam o limiar de diferença; ajuste a região x=418, y=324, w=32, h=134.
- **P3** `investments-1440x900-I11` — Visual difference region at `{'x': 602, 'y': 139, 'width': 105, 'height': 39}`: 2096 pixels (0.16% da tela) ultrapassam o limiar de diferença; ajuste a região x=602, y=139, w=105, h=39.
- **P3** `investments-1440x900-I12` — Visual difference region at `{'x': 372, 'y': 142, 'width': 93, 'height': 36}`: 1785 pixels (0.14% da tela) ultrapassam o limiar de diferença; ajuste a região x=372, y=142, w=93, h=36.
- **P3** `investments-1440x900-I13` — Visual difference region at `{'x': 124, 'y': 274, 'width': 160, 'height': 20}`: 1660 pixels (0.13% da tela) ultrapassam o limiar de diferença; ajuste a região x=124, y=274, w=160, h=20.
- **P3** `investments-1440x900-I14` — Visual difference region at `{'x': 748, 'y': 797, 'width': 100, 'height': 19}`: 1328 pixels (0.10% da tela) ultrapassam o limiar de diferença; ajuste a região x=748, y=797, w=100, h=19.

## imports — 1440×900

- Score: **88.15**; coverage: **91.18%**; status: **FAIL**
- Similarity evidence: pixel=0.9574, exact=0.0548
- Comparison: `imports-side-by-side-annotated.png`; overlay: `imports-overlay.png`; heatmap: `imports-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 99.80 | 29.94 | content bbox IoU=0.998, area similarity=0.998, viewport_match=1 |
| Spacing/grid | 20 | 79.33 | 15.87 | row profile MAE=0.215, column profile MAE=0.198 |
| Typography | 15 | 99.17 | 14.88 | dark density similarity=0.995, row similarity=0.988; image-only heuristic |
| Color/border/shadow | 15 | 90.58 | 13.59 | quantized RGB histogram similarity=0.906 |
| Content/density | 10 | 76.96 | 7.70 | mask coverage=0.716, density similarity=0.850 |
| Assets | 10 | 61.90 | 6.19 | component count similarity=0.500, area similarity=0.798; image-only heuristic |

Issues:
- **P1** `imports-1440x900-I1` — Visual difference region at `{'x': 125, 'y': 603, 'width': 762, 'height': 49}`: 8999 pixels (0.69% da tela) ultrapassam o limiar de diferença; ajuste a região x=125, y=603, w=762, h=49.
- **P1** `imports-1440x900-I2` — Visual difference region at `{'x': 425, 'y': 139, 'width': 182, 'height': 50}`: 4009 pixels (0.31% da tela) ultrapassam o limiar de diferença; ajuste a região x=425, y=139, w=182, h=50.
- **P1** `imports-1440x900-I3` — Visual difference region at `{'x': 131, 'y': 198, 'width': 170, 'height': 41}`: 3454 pixels (0.27% da tela) ultrapassam o limiar de diferença; ajuste a região x=131, y=198, w=170, h=41.
- **P1** `imports-1440x900-I4` — Visual difference region at `{'x': 231, 'y': 142, 'width': 128, 'height': 36}`: 2473 pixels (0.19% da tela) ultrapassam o limiar de diferença; ajuste a região x=231, y=142, w=128, h=36.
- **P1** `imports-1440x900-I5` — Visual difference region at `{'x': 141, 'y': 616, 'width': 103, 'height': 25}`: 1870 pixels (0.14% da tela) ultrapassam o limiar de diferença; ajuste a região x=141, y=616, w=103, h=25.
- **P1** `imports-1440x900-I6` — Visual difference region at `{'x': 152, 'y': 251, 'width': 206, 'height': 18}`: 1824 pixels (0.14% da tela) ultrapassam o limiar de diferença; ajuste a região x=152, y=251, w=206, h=18.
- **P1** `imports-1440x900-I7` — Visual difference region at `{'x': 88, 'y': 141, 'width': 86, 'height': 37}`: 1777 pixels (0.14% da tela) ultrapassam o limiar de diferença; ajuste a região x=88, y=141, w=86, h=37.
- **P1** `imports-1440x900-I8` — Visual difference region at `{'x': 180, 'y': 560, 'width': 237, 'height': 14}`: 1737 pixels (0.13% da tela) ultrapassam o limiar de diferença; ajuste a região x=180, y=560, w=237, h=14.
- **P1** `imports-1440x900-I9` — Visual difference region at `{'x': 360, 'y': 139, 'width': 62, 'height': 39}`: 1420 pixels (0.11% da tela) ultrapassam o limiar de diferença; ajuste a região x=360, y=139, w=62, h=39.
- **P1** `imports-1440x900-I10` — Visual difference region at `{'x': 226, 'y': 582, 'width': 212, 'height': 14}`: 1369 pixels (0.11% da tela) ultrapassam o limiar de diferença; ajuste a região x=226, y=582, w=212, h=14.
- **P1** `imports-1440x900-I11` — Visual difference region at `{'x': 969, 'y': 588, 'width': 178, 'height': 17}`: 1321 pixels (0.10% da tela) ultrapassam o limiar de diferença; ajuste a região x=969, y=588, w=178, h=17.

## assistant — 1440×900

- Score: **93.99**; coverage: **94.68%**; status: **PASS**
- Similarity evidence: pixel=0.9758, exact=0.1276
- Comparison: `assistant-side-by-side-annotated.png`; overlay: `assistant-overlay.png`; heatmap: `assistant-heatmap.png`

Metric breakdown:

| Dimension | Weight | Score | Contribution | Explanation |
|---|---:|---:|---:|---|
| Geometry/alignment | 30 | 99.80 | 29.94 | content bbox IoU=0.998, area similarity=0.998, viewport_match=1 |
| Spacing/grid | 20 | 85.36 | 17.07 | row profile MAE=0.131, column profile MAE=0.162 |
| Typography | 15 | 99.39 | 14.91 | dark density similarity=0.994, row similarity=0.993; image-only heuristic |
| Color/border/shadow | 15 | 92.21 | 13.83 | quantized RGB histogram similarity=0.922 |
| Content/density | 10 | 86.85 | 8.69 | mask coverage=0.818, density similarity=0.944 |
| Assets | 10 | 95.55 | 9.55 | component count similarity=1.000, area similarity=0.889; image-only heuristic |

Issues:
- **P3** `assistant-1440x900-I1` — Visual difference region at `{'x': 550, 'y': 711, 'width': 198, 'height': 44}`: 8328 pixels (0.64% da tela) ultrapassam o limiar de diferença; ajuste a região x=550, y=711, w=198, h=44.
- **P3** `assistant-1440x900-I2` — Visual difference region at `{'x': 816, 'y': 314, 'width': 158, 'height': 22}`: 1587 pixels (0.12% da tela) ultrapassam o limiar de diferença; ajuste a região x=816, y=314, w=158, h=22.
- **P3** `assistant-1440x900-I3` — Visual difference region at `{'x': 804, 'y': 621, 'width': 532, 'height': 4}`: 1572 pixels (0.12% da tela) ultrapassam o limiar de diferença; ajuste a região x=804, y=621, w=532, h=4.
