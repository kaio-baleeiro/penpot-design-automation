---
name: penpot-source-map
description: Capture and map URLs, screenshots, running apps and code repositories into a persistent, auditable source record for Penpot reconstruction.
metadata:
  short-description: Map source evidence for faithful Penpot reconstruction
  compatibility: Requires the project checkout and Python 3; URL capture uses Playwright Chromium.
---

# Penpot source mapping

Use only for the `reproduction` route. Every supplied source remains represented
even when inaccessible or lower confidence. Resolve this skill's physical
directory before invoking its bundled wrapper.

## Capture and inventory

Delegate hands-on capture/inspection to `gpt-5.6-luna`. For a public URL, use
the project CLI command
`scripts/source-map.sh capture --url <URL> --output <dir> --viewport <WxH>`
(add `--full-page` only when the requested evidence is a full page). Use
Playwright through that command and record the exact viewport, route, timestamp,
loading state, fonts and dynamic-content limitations. For repositories, inspect
the checked-out code and runtime directly (there is no separate source-inspect
script); record commit/ref, framework, entry points, route list, responsive
breakpoints, tokens, components and how the app was run. For screenshots, use
`scripts/source-map.sh map-screenshot --image <PNG> --output <json>`
and record pixel dimensions, crop, device-pixel-ratio if known, visible states
and what is unknown.

When sources are combined, compile them with `scripts/source-map.sh compile
--url <URL> --screenshot <PNG> --code
<repo-or-file> --output source/source-map.json`. Code inputs may be files or
directories; secret/env/dependency directories are excluded from their stable
hash.

## Source asset inventory

The user grants standing permission to inspect and retrieve useful assets from
the supplied site/runtime and codebase for the requested reconstruction. Before
planning the build, inspect image/SVG elements, inline SVG, CSS backgrounds,
font declarations and loaded first-party or source-referenced resources. In
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

## Persistent map

Write `source/source-map.json`, `source/source-inventory.md` and
`source/assets-manifest.json` before building.
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
