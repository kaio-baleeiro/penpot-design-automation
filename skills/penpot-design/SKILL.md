---
name: penpot-design
description: Orchestrate creation or faithful reconstruction of static Penpot screens from URLs, screenshots, code repositories, or a refined prompt, including source traceability, delegated execution, deterministic validation, design-system formalization, and delivery.
metadata:
  short-description: Build and validate Penpot designs from sources or prompts
  compatibility: Requires the project checkout, Python 3, Penpot MCP, and a host capable of delegated workers.
---

# Penpot Design Orchestrator

Use this as the entrypoint for a request to create screens in the shared Penpot
instance. This skill may be installed through a symbolic link. Resolve its
physical directory first (`pwd -P` or equivalent) and derive the repository
root as two parents above that directory. Read
[the workflow contract](references/workflow-contract.md),
[the state machine](references/state-machine.md),
[the artifact schema](references/artifacts.md) and
[the delegation contract](references/delegation.md) and [the agent profile
mapping](references/agent-profiles.md) before acting. Read
[the lessons protocol](references/lessons-learned.md) and the local
[`lessons-learned/README.md`](lessons-learned/README.md) at the beginning and
end of every run. The machine-readable defaults are in
`assets/workflow-config.yaml`.

At the beginning of every new agent session run `<repo>/penpot-workflow begin`
and ask its exact infrastructure-or-design question. Record the user's answer
with `select <mode> --user-answer "<verbatim answer>"`. Infrastructure uses
`bootstrap-infra`; design runs use `new-run` and guarded state transitions.
Before visual delegation, the worker must open an image and record its hash and
what it observed. This is auditable evidence of capability, not proof of inner
model cognition.

The sibling skills `penpot-intake`, `penpot-source-map`,
`penpot-build`, `penpot-validate`, `penpot-design-system` and `penpot-delivery`
are the authoritative phase instructions. Read their `SKILL.md` from the
physical repository before each phase; they do not need separate global copies.

## Route selection

- Choose `reproduction` when any URL, screenshot, running application, or code
  repository is supplied. Sources can be combined.
- Choose `directed_creation` only when the user explicitly wants creation from
  a prompt with no source.

Run the mandatory interaction defined by `penpot-intake`: ask the initial
questions, ask the second adendo/mudança question, then analyze ambiguities.
Do not construct before material decisions are resolved. Persist every answer,
decision, source, feedback and applicable `lesson_refs` in the run directory
described by `references/artifacts.md`. Initialize a new run with the project
controller; the older `scripts/start-run.sh` only imports controller-owned
manifests.

For reproduction, treat the supplied site/runtime and codebase as the primary
asset library. The user grants standing permission to inspect and retrieve
SVGs, raster images, icons, logos, fonts and other useful files referenced by
those sources when needed for the requested screens. Inventory their provenance
before construction and prefer the exact source asset over searching for a
similar replacement elsewhere. Keep private payloads out of Git and do not
expand this permission into unrelated web browsing.

The source screenshot is evidence and visual reference only. It is never an
acceptable substitute for the Penpot composition: each delivered frame must
contain editable text, vector/rectangle/image shapes and meaningful component
descendants. A visible frame whose only substantive child is a full-page
screenshot/image fill fails the structural gate even if its pixel score is high.
Reference captures may remain on a hidden or locked evidence layer, but they
must not be the only visible content. Record descendant counts by type and
component-instance counts in `design/structure-inventory.json`.

## Delegation policy

All hands-on work uses the cost-efficient worker selected for the current host
by `agents/runtime-policy.yaml`: source capture, inspection, MCP construction,
correction, token extraction, rendering and scoring. Codex prefers
`gpt-5.6-luna`; other runtimes use their declared native mapping. Record the
resolved runtime and model in the run manifest and every handoff. If no
delegated worker is available, stop with `BLOCKED_WORKER_UNAVAILABLE`. Keep the
orchestrator focused on routing, user questions, gate decisions and records.

Use the specialized portable profiles in `agents/` for each phase: source
analyst, frontend forensics, UX/IA, visual UI, Penpot MCP prototyper, visual QA
and design-system architect. Every handoff must follow
`agents/contracts/handoff.md`; a missing handoff, empty structure inventory,
unmapped asset or unresolved layout contract blocks the next phase. The profile
does not replace the orchestrator's final score or semantic review.

Follow `references/delegation.md`: invoke the native adapter for the current
host, or pass the canonical profile to an equivalent delegated worker. Treat
quota/model/delegation errors as `BLOCKED_WORKER_UNAVAILABLE`.

## Pipeline

1. `penpot-intake`: collect answers, route, scope and target viewports.
2. `penpot-source-map` for reproduction, including the source asset inventory,
   measured document bounds and `frame-spec.json`, or the briefing branch in
   intake for directed creation, including an approved frame spec derived from
   the planned content.
3. Plan screens and hand the plan to `penpot-build` for static frames and
   reusable components through Penpot MCP. The build must reconstruct the
   visible sections as editable shapes/text/assets; semantic labels without
   substantive descendants do not satisfy this phase.
4. `penpot-validate`: render every requested screen/viewport, run the immutable
   deterministic score, and produce side-by-side, overlay, heatmap and issues.
5. If any screen fails `score >= 90`, `coverage >= 80`, or has P0/P1, delegate
   targeted fixes to the configured worker and repeat validation. Allow at most three internal
   cycles after initial construction; otherwise end `NEEDS_REVIEW`.
6. Obtain formal user approval. In directed creation, user feedback rounds are
   unlimited and each new build starts a fresh three-cycle validation budget.
7. `penpot-design-system`: extract and formalize tokens/styles/components,
   rebuild screens with instances, then revalidate against the approved
   prototype.
8. `penpot-delivery`: package the Penpot link/file, records and visual report.

Whenever a mistake, failed assumption, regression, security weakness or user
correction changes future behavior, create or update a lesson in the affected
skill's `lessons-learned/` directory before delivery. Promote cross-phase rules
to the shared index at `penpot-design/lessons-learned/`. A lesson is only
overcome after its countermeasure is verified and its status becomes
`mitigated`; link it through `lesson_refs` instead of copying the lesson into
the run. The vault may retain a project reference, but the versioned skill
lesson is the executable source of future behavior.

Use the state names in `references/state-machine.md`. Never mark
`DELIVERED` while a viewport or structural design-system gate is failing.
