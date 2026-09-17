---
name: penpot-source-map
description: Capture and map URLs, screenshots, running apps and code repositories into auditable source records with full-page bounds, exact asset provenance, and reproducible dynamic-state limits.
metadata:
  short-description: Map source evidence for faithful Penpot reconstruction
  compatibility: Requires the project checkout and Python 3; URL capture uses Playwright Chromium.
---

# Penpot source mapping

Operational work is delegated to the portable profiles
`intake-source-analyst` and `frontend-forensics-engineer` described in
`agents/profiles/`; their handoffs are required before build planning.

Use only for the `reproduction` route. Read the local
[`lessons-learned/README.md`](lessons-learned/README.md) before capture. Every supplied source remains represented
even when inaccessible or lower confidence. Resolve this skill's physical
directory before invoking its bundled wrapper. For a URL, running application
or runnable codebase, read [the frame-sizing policy](references/frame-sizing.md)
before capture and persist its decision per screen.

## Capture and inventory

Delegate hands-on capture/inspection to `gpt-5.6-luna`. For a public URL, use
the project CLI command
`scripts/source-map.sh capture --url <URL> --output <dir> --viewport <WxH>`
(add `--full-page` only when the requested evidence is a full page). Use
Playwright through that command and record the exact viewport, route, timestamp,
loading state, fonts, `document_metrics` and dynamic-content limitations. Treat
`1440x900` as the default desktop observation viewport, not an automatic final
frame size. Every finite source must also receive a complete `full_page`
capture in a separate output directory; the viewport screenshot is only
above-the-fold evidence. Use the full-page image as the reference for design
and validation. When lazy loading or infinite content
is plausible, keep the default two bounded scroll probes; pass
`--scroll-probes 0` only when scrolling would be unsafe or outside scope and
record that limitation. Continued growth is unstable and needs a finite
user-approved boundary. For repositories, inspect
the checked-out code and runtime directly (there is no separate source-inspect
script); record commit/ref, framework, entry points, route list, responsive
breakpoints, tokens, components and how the app was run. For screenshots, use
`scripts/source-map.sh map-screenshot --image <PNG> --output <json>`
and record pixel dimensions, crop, device-pixel-ratio if known, visible states
and what is unknown. For a known full-page screenshot, also pass
`--capture-mode full_page --viewport <WxH>` so its image height is not mistaken
for the observation viewport. A finite page captured only as `1440x900` is
incomplete and cannot enter the build handoff. If that distinction is unknown
and material, ask.
Do not score or deliver an unstable full-page capture: obtain approval for a
finite bounded state and recapture it before deriving `frame-spec.json`.
Dimensional stability alone is insufficient: before freezing a reference,
audit every full-page section and confirm lazy media, SVGs, images and fonts
are ready and represented in `assets-manifest.json`; record gaps and seek
recapture/approval rather than silently treating `stable: true` as complete.

When sources are combined, compile them with `scripts/source-map.sh compile
--url <URL> --screenshot <PNG> --code
<repo-or-file> --output source/source-map.json`. Code inputs may be files or
directories; secret/env/dependency directories are excluded from their stable
hash.

## Source asset inventory

The user grants standing permission to inspect and retrieve useful assets from
the supplied site/runtime and codebase for the requested reconstruction. Before
planning the build, inspect image/SVG elements, inline SVG, computed CSS
backgrounds, pseudo-elements, `video` poster/source URLs, runtime/dynamic
configuration, font declarations and loaded first-party or source-referenced
resources. Inventory assets section by section from the rendered page; an
HTML-only `<img>` list is incomplete and cannot enter build planning. In
code, inspect the relevant `public`, `static`, `assets`, `src` and component
paths, including icon sets, sprites, illustrations, logos and fonts. Follow a
CDN/resource URL when the supplied source itself references it and the asset is
needed for an in-scope screen; this is not permission for unrelated web search.

Write `source/assets-manifest.json`. Give each candidate a stable `asset_id` and
record kind, sanitized URL or repository-relative path, source id, hash when
available, MIME type, intrinsic dimensions when applicable, screen/component
usage, acquisition status and any known licensing/attribution note. Preserve
the exact source asset whenever usable. Keep authenticated/private payloads in
ignored storage and expose only sanitized provenance in versioned records.
`deferred`, `observed_not_embedded` and equivalent statuses are discovery states,
not build-ready states. Before handoff, each planned asset must have a resolvable
URL or local path and the build plan must name its `asset_id`; unresolved assets
block faithful reconstruction instead of silently becoming placeholders. When
a frozen screenshot shows a video frame that differs from the available
poster, record that mismatch explicitly; do not claim the poster is the
captured frame.

## Persistent map

Write `source/source-map.json`, `source/source-inventory.md`,
`source/assets-manifest.json` and `source/frame-spec.json` before building.
Each observation needs a stable id, source id, evidence path/anchor, viewport,
confidence and notes. Include hashes for files/captures and sanitise secrets.
Keep raw captures outside Git when private; refer to their local path without
committing cookies, tokens or authenticated data.

Derive each screen entry with `scripts/source-map.sh frame-spec --capture
<capture.json> --screen-id <id> --output <screen-frame-spec.json>`. A wider
page requires an explicit `--horizontal-policy` decision; use
`intentional_page` only together with `--horizontal-evidence`. Combine the
screen entries into the run's `source/frame-spec.json` and mirror the matching
entry in `manifest.json` for the validation gate.

After approving a frame wider than the observation viewport, recapture its
reference with `scripts/source-map.sh capture --url <URL> --viewport 1440x900
--frame-bounds <frame-width>x<frame-height> --output <dir>`. This preserves the
responsive viewport while Chromium captures the approved horizontal/vertical
bounds. Never validate a wide frame against a viewport-width PNG.

## Conflicts and gaps

Compare URL, screenshot and code evidence. If they disagree on layout,
content, viewport, typography, assets or behavior, set `precedence: unresolved`,
record both observations and ask the user which source prevails. Do not average,
guess or proceed with a silent choice. Non-material assumptions must be
recorded with impact and reversal.

Conclude with a screen/viewport inventory and a build handoff. A missing source,
blocked authentication or unavailable Luna is an explicit blocker, not a
fabricated capture.
