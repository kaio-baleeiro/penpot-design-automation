# Warframe EN — bounded capture proposal v2

Status: **proposed, awaiting user boundary decision**. This proposal does not
replace the immutable `warframe-en` run or claim a deterministic score.

## Capture

- Source: `https://www.warframe.com/en`
- Observation viewport: `1440×900`
- Proposed vertical boundary: `5837px`
- Proposed Penpot frame: `1440×5837`
- Capture mode: `frame_bounds` (CDP clip, full visible page height)
- Capture timestamp: `2026-09-15T19:58:14.842020+00:00`
- Reference evidence: `source/raw/bounded-1440x5837-v2/source.png`
- Reference SHA-256: `4afdc1028090817543c468b75345539f13d6daa6e8d40b0b3aa186297f0639a7`

The capture reports `stable_after_wait: false`: width samples were
`1923 → 1914 → 1983`, while height stayed `5837` for all samples. The extra
width comes from absolutely positioned images and a child container with
`overflow-x: hidden`; it is not evidence of intentional root horizontal
navigation. Keep the design frame at `1440px` wide.

## Reproducibility protocol

The proposed boundary is derived from the last stable height observed in the
trial-2 capture and reproduced by a fresh run with `wait_ms=5000` and
`scroll_probes=0`. Before this proposal can enter `source/frame-spec.json`, the
user must confirm that the Warframe benchmark should use this bounded page state
through the footer at `5837px`. If not confirmed, keep the benchmark in
`NEEDS_REVIEW` and do not score it.

## Section inventory observed in the bounded state

1. `y=0–66`: fixed global navigation and account actions.
2. `y=66–1614`: hero (Jade Shadows / Constellations) plus trailer/learn-more actions and two feature cards.
3. `y=1469–2799`: News & Updates, four editorial cards and See All (section overlaps the hero's lower boundary by design).
4. `y=2799–4048`: Shop Warframe, Mesa Heirloom collection and New & Notable product row.
5. `y=4000–4400`: Prime Resurgence feature banner.
6. `y=4400–5052`: Player Guides & Tools, with Player Guides, Community and Referral Program.
7. `y=5132–5296`: community/social connection strip.
8. `y=5296–5437`: support, legal and language footer navigation.
9. `y=5437–5837`: platform availability, copyright and rating marks.

Cookie consent is an incidental source overlay in this capture and should be
recorded as source state, not treated as a page section to reproduce unless the
benchmark's existing intake explicitly requires it.

## Asset inventory highlights

The DOM exposed 74 image/video references, including the first-party Warframe
logo, Lotus mark, navigation SVG icons, homepage hero/media WebP files,
editorial uploads, social icons, platform logos, rating mark and cookie
provider assets. The exact sanitized URLs and usage anchors are listed in
`assets-inventory.json`; the source permission allows these first-party files
to be reused in the editable Penpot reconstruction.
