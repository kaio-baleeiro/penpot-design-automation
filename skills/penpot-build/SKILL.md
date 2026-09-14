---
name: penpot-build
description: Build static Penpot frames, reusable components and initial styles from an approved source map or directed-creation briefing through the Penpot MCP.
metadata:
  short-description: Build static Penpot screens with MCP
  compatibility: Requires the project checkout, local environment file, Python 3, and Penpot MCP.
---

# Penpot MCP build

Require a run manifest whose intake and ambiguity gates are complete, then read the current `source/source-map.json` or
approved `briefing/brief-vNNN.md` before acting.
Only build after intake and material ambiguity gates pass.

## Build contract

Delegate all hands-on MCP operations to `gpt-5.6-luna`; if unavailable stop
with `BLOCKED_MODEL_UNAVAILABLE`. The worker must use the configured Penpot MCP,
not an untracked manual substitute, and append every mutation/result to
`design/penpot-mcp-log.jsonl`.

Create static screens at the explicitly approved viewports. Use semantic
groups, reusable components, variants where justified, shared typography/color/
spacing styles and real text/assets when evidence exists. Do not claim a
design system is complete during this initial pass; mark provisional styles.
Do not add interactions unless separately authorized.

Plan first in `design/plan.json`: screen id, route/state, viewport, source
anchors or briefing requirements, content, components, assets and expected
responsive behavior. Then call the project Penpot client with
`scripts/penpot-mcp.sh execute --args '<JSON>' --log-path design/penpot-mcp-log.jsonl` (or
`scripts/penpot-mcp.sh call <tool-name> --args '<JSON>' --log-path design/penpot-mcp-log.jsonl`) from this skill's physical directory to apply the
plan and `scripts/penpot-mcp.sh export --args '<JSON>' --save-image <PNG>
--log-path design/penpot-mcp-log.jsonl` for frame PNGs. The client sends the MCP `tools/call` request and must
append request, response and frame identifiers to the MCP log.

## Handoff

Return the Penpot file/project reference, frame ids, export paths and unresolved
implementation questions. Never overwrite an earlier version; use a versioned
file or page name. The next state is `VALIDATING`, not approval.
