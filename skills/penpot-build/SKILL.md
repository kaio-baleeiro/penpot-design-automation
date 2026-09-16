---
name: penpot-build
description: Build editable static Penpot frames, reusable components and initial styles from an approved source map or briefing through the Penpot MCP, preserving full-page bounds and exact source assets.
metadata:
  short-description: Build static Penpot screens with MCP
  compatibility: Requires the project checkout, local environment file, Python 3, and Penpot MCP.
---

# Penpot MCP build

Use the portable `penpot-mcp-prototyper` profile for all hands-on operations and
require its handoff before validation. Planning inputs may come from the
`ux-ia-responsive-designer` and `visual-ui-designer` profiles.

Read [`lessons-learned/README.md`](lessons-learned/README.md), then require a run manifest whose intake and ambiguity gates are complete, and read the current `source/source-map.json` or
approved `briefing/brief-vNNN.md` before acting.
Only build after intake and material ambiguity gates pass.
For the screenshot-versus-editable-design failure mode, apply
[`LL - screenshot is not editable design.md`](lessons-learned/project/LL%20-%20screenshot%20is%20not%20editable%20design.md).
The structural inventory is a required build output; apply
[`LL - Inventário estrutural vazio invalida o benchmark.md`](lessons-learned/project/LL%20-%20Inventário%20estrutural%20vazio%20invalida%20o%20benchmark.md)
before handing the frame to validation.

## Build contract

Delegate all hands-on MCP operations to `gpt-5.6-luna`; if unavailable stop
with `BLOCKED_MODEL_UNAVAILABLE`. The worker must use the configured Penpot MCP,
not an untracked manual substitute, and append every mutation/result to
`design/penpot-mcp-log.jsonl`.

For reproduction, create static screens from the approved
`source/frame-spec.json`; for directed creation, use the equivalent frame spec
approved in the briefing. For desktop,
`1440x900` is the minimum/default observation viewport, while the Penpot frame
height grows to the measured finite document height and must cover the complete
full-page source capture. Grow width beyond `1440` only when the
source map proves intentional page-level horizontal navigation; keep accidental
overflow and nested scroll containers within the base frame. Never silently
truncate stable content below or beside the fold.

Use semantic
groups, reusable components, variants where justified, shared typography/color/
spacing styles and real text/assets when evidence exists. Read
`source/assets-manifest.json` and reuse the exact mapped SVG, image, icon, logo
or font before considering a substitute. Do not search external catalogs for a
lookalike while an original asset is accessible. If the source asset is absent,
unusable or legally restricted, record the reason and ask before introducing an
externally sourced replacement. Do not claim a design system is complete during
this initial pass; mark provisional styles. Do not add interactions unless
separately authorized.

The full-page source image is not the design. It may be imported only as a
hidden/locked reference layer. Every visible section in the delivered frame
must be reconstructed with editable text, shapes/vectors and source assets, and
each semantic component must have substantive descendants. A one-image frame,
or a component containing only a label that names the section, is an invalid
build even when it looks pixel-perfect.

When a section is a nested Penpot board, position its descendants in that
board's local coordinate system; convert page coordinates with
`local_x = page_x - board_x` and `local_y = page_y - board_y`. Do not mix local
and page coordinates inside the same container. Before handing off any long
page, inspect the exported full-page PNG and verify that every mapped section
contains visible content; shape and image counts alone do not prove visibility.
See [`LL - nested boards require local coordinates.md`](lessons-learned/project/LL%20-%20nested%20boards%20require%20local%20coordinates.md).

Plan first in `design/plan.json`: screen id, route/state, viewport, frame bounds, source
anchors or briefing requirements, content, components, `asset_refs` pointing to
the source manifest and expected responsive behavior. Then call the project Penpot client with
`scripts/penpot-mcp.sh execute --args '<JSON>' --log-path design/penpot-mcp-log.jsonl` (or
`scripts/penpot-mcp.sh call <tool-name> --args '<JSON>' --log-path design/penpot-mcp-log.jsonl`) from this skill's physical directory to apply the
plan and `scripts/penpot-mcp.sh export --args '<JSON>' --save-image <PNG>
--log-path design/penpot-mcp-log.jsonl` for frame PNGs. The client sends the MCP `tools/call` request and must
append request, response and frame identifiers to the MCP log.

Keep all build exports under `design/exports/<screen>/`. The build must never
create or populate `cycles/cycle-N/`; those directories are reserved for the
append-only evaluator, which creates the score, issues, report, side-by-side,
overlay and heatmap artifacts. See [`LL - evaluator owns cycle directories.md`](lessons-learned/project/LL%20-%20evaluator%20owns%20cycle%20directories.md).

## Handoff

Return the Penpot file/project reference, frame ids, export paths and unresolved
implementation questions. Never overwrite an earlier version; use a versioned
file or page name. The next state is `VALIDATING`, not approval.
