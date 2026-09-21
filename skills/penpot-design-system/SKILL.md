---
name: penpot-design-system
description: Formalize an approved Penpot prototype into reusable tokens, styles, components and responsive rules, then rebuild and revalidate the screens against the approved version.
metadata:
  short-description: Extract and verify a Penpot design system
  compatibility: Requires the project checkout, local environment file, Python 3, and Penpot MCP.
---

# Penpot design system

Use the portable `design-system-architect` profile for extraction and MCP
refactoring; its token/component handoff is required before DS revalidation.

Read [`lessons-learned/README.md`](lessons-learned/README.md). Run only after formal approval of the constructed version (and approved
briefing/version in directed creation). Use append-only run artifacts and never
replace the approved reference version.

Delegate extraction and MCP refactoring to the configured cost-efficient
worker; stop with `BLOCKED_WORKER_UNAVAILABLE` if delegation is unavailable.
Extract the inventory from the approved frames/code and apply
the changes through `scripts/penpot-mcp.sh execute --args '<JSON>' --log-path design/penpot-mcp-log.jsonl` from this skill's physical directory (or
`scripts/penpot-mcp.sh call <tool-name> --args '<JSON>' --log-path design/penpot-mcp-log.jsonl`). Record the inventory, MCP requests and
responses; do not assume a separate token-extraction script exists.

## Required output

Create a versioned design-system inventory covering color, typography, spacing,
radius, borders, elevation, breakpoints, icon/image treatment, component names,
variants, states and usage rules. In Penpot, create shared styles and
components with meaningful names and replace duplicated provisional shapes with
instances. Preserve visual values from the approved prototype unless a user
decision authorizes change.

Use the source asset manifest as the canonical registry for icons, logos,
illustrations, images and fonts. Preserve `asset_id`/provenance in the inventory,
promote repeated vectors or image treatments to named reusable components when
appropriate, and do not replace originals with visually similar library assets.

Re-export every approved screen/viewport after componentization. `penpot-validate`
must compare those renders to the approved prototype with the same immutable
gates (`>=90`, coverage `>=80`, no P0/P1) and provide side-by-side, overlay,
heatmap and issues. A design system that looks right but is structurally made
of detached copies fails. A componentization that changes layout fails until
corrected or marked `NEEDS_REVIEW`.

Persist token/component inventory, reconstruction log and revalidation evidence;
never replace the original approved prototype or its records.

Before delivery, run `scripts/inventory.sh --output
design/structure-inventory.json --log-path design/penpot-mcp-log.jsonl`. It
exports `tokens`, `components`, `component_instances`, `detached_instances`,
`styles` and `required_component_instances`; add the planned required instances
to the manifest before validating. Empty design-system inventories and detached
instances fail `DS_REVALIDATING`.
