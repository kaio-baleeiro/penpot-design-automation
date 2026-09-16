# GitHub Kaio benchmark — v2

Fresh benchmark version built in the general Penpot Site Benchmarks file. This
version owns its source evidence, editable Penpot export and three immutable
validation cycles. It is intentionally separate from the KatiauInvest file.

## Current result

`NEEDS_REVIEW` after the maximum three-cycle budget. The deterministic image
score reached 98.52/100 with 92.79% coverage, but the final reviewer rejected
the result because source-content fidelity is still incomplete. A high pixel
score is not treated as approval: the remaining differences are listed in
[`review-cycle-3.md`](review-cycle-3.md).

## Inspect the evidence

- [`source/reference.png`](source/reference.png) — full-page source capture
  at 1440×1807.
- [`design/exports/home/1440x1807-cycle3.png`](design/exports/home/1440x1807-cycle3.png)
  — final editable-composition export.
- [`cycles/cycle-1/`](cycles/cycle-1/) — score, issues and visual comparisons
  for the first build.
- [`cycles/cycle-2/`](cycles/cycle-2/) — targeted correction cycle.
- [`cycles/cycle-3/`](cycles/cycle-3/) — final correction cycle.
- [`delivery/`](delivery/) — terminal package and exact blockers.

Each cycle includes side-by-side, overlay and heatmap images. The Penpot frame
is editable (`image_only: false`) and is tracked in the manifest; the source
capture remains evidence, never the delivered composition.

## Penpot reference

- File: `Site Benchmarks` (`cf04346a-b044-818b-8008-a4ed84a51a17`)
- Page: `Benchmark — GitHub Kaio`
- Frame: `GitHub Kaio — Home — 1440x1807`

The frame is available for inspection, but it is not presented as an approved
faithful reproduction. A future improvement must start a new version/run,
not reopen a fourth cycle or rewrite the immutable evidence here.
