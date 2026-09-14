---
name: penpot-source-map
description: Capture and map URLs, screenshots, running apps and code repositories into a persistent, auditable source record for Penpot reconstruction.
metadata:
  short-description: Map source evidence for faithful Penpot reconstruction
---

# Penpot source mapping

Use only for the `reproduction` route. Read `../../workflow/CONTRACT.md` and
`ARTIFACTS.md`. Every supplied source remains represented even when inaccessible
or lower confidence.

## Capture and inventory

Delegate hands-on capture/inspection to `gpt-5.6-luna`. For a public URL, use
the project CLI command
`python3 -m scripts.penpot_validation capture --url <URL> --output <dir> --viewport <WxH>`
(add `--full-page` only when the requested evidence is a full page). Use
Playwright through that command and record the exact viewport, route, timestamp,
loading state, fonts and dynamic-content limitations. For repositories, inspect
the checked-out code and runtime directly (there is no separate source-inspect
script); record commit/ref, framework, entry points, route list, responsive
breakpoints, tokens, components and how the app was run. For screenshots, use
`python3 -m scripts.penpot_validation map-screenshot --image <PNG> --output <json>`
and record pixel dimensions, crop, device-pixel-ratio if known, visible states
and what is unknown.

When sources are combined, compile them with `python3 -m
scripts.penpot_validation.source_map --url <URL> --screenshot <PNG> --code
<repo-or-file> --output source/source-map.json`. Code inputs may be files or
directories; secret/env/dependency directories are excluded from their stable
hash.

## Persistent map

Write `source/source-map.json` and `source/source-inventory.md` before building.
Each observation needs a stable id, source id, evidence path/anchor, viewport,
confidence and notes. Include hashes for files/captures and sanitise secrets.
Keep raw captures outside Git when private; refer to their local path without
committing cookies, tokens or authenticated data.

## Conflicts and gaps

Compare URL, screenshot and code evidence. If they disagree on layout,
content, viewport, typography, assets or behavior, set `precedence: unresolved`,
record both observations and ask the user which source prevails. Do not average,
guess or proceed with a silent choice. Non-material assumptions must be
recorded with impact and reversal.

Conclude with a screen/viewport inventory and a build handoff. A missing source,
blocked authentication or unavailable Luna is an explicit blocker, not a
fabricated capture.
