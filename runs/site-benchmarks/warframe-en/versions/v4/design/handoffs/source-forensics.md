# Handoff — frontend-forensics-engineer / source-forensics

- Worker model: `gpt-5.6-luna` (required by contract).
- Source: bounded Warframe EN capture, DOM and raw styles under
  `../v2/source/`.
- Approved geometry: 1440×5837 frame, 1440×900 observation viewport.
- Root horizontal overflow is accidental; keep the frame at 1440px.
- Section bounds and anchors are in `../plan.json` and `../source/source-map.json`.
- Exact first-party asset URLs are in `../source/assets-manifest.json` and the
  full 41-URL inventory at `../../source/proposals/bounded-v2/assets-inventory.json`.

Open issue: source dimensions report `stable_after_wait: false` because width
changes off-canvas; the user-approved bounded state makes the vertical boundary
reproducible. Cookie consent is incidental and excluded.
