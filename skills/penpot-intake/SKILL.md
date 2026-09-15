---
name: penpot-intake
description: Gather and normalize the mandatory questions, route, scope, viewport and approval decisions before a Penpot design run starts.
metadata:
  short-description: Ask, scope and prepare a Penpot design run
  compatibility: Requires the project checkout and Python 3; URL capture uses Playwright Chromium.
---

# Penpot intake

Read [the mandatory questionnaire](references/questions.md) and the local
[`lessons-learned/README.md`](lessons-learned/README.md) first.
This skill owns `INTAKE_PENDING`, `INTAKE_REVIEW`, `AMBIGUITY_ANALYSIS` and the
directed-creation briefing gate.

## Required behavior

- Ask the initial questions before any build or source mutation.
- After the answers, ask the mandatory second question about adendo/mudança and
  persist its response, including “não”.
- Analyze unresolved decisions and ask additional questions when they could
  change scope, source precedence, desktop/mobile delivery, content, brand,
  security or approval. Do not hide material assumptions.
- For URLs/repositories, investigate whether responsive layouts exist for
  desktop, mobile or both. Report evidence and ask which viewports to deliver.
  For a URL, capture a temporary desktop reconnaissance at `1440x900` and mobile
  reconnaissance at `390x844`, compare reflow, clipping, navigation and content
  order, and record the two capture manifests. For code, also inspect media
  queries/breakpoints. `1440x900` and `390x844` are observation viewports, not
  fixed final frame bounds: report measured page extents and any horizontal or
  dynamic overflow. This reconnaissance informs the question; it does not
  silently add both viewports to delivery scope.
- For `directed_creation`, confirm there is no source, draft a structured
  briefing, show it to the user, and wait for formal approval before building.
  Include viewport and intended frame extent in that briefing; default desktop
  starts at `1440x900`, while content below the fold may produce a taller frame.
  For every finite URL/repository screen, require a full-page capture and use
  its measured height for the design frame; never design only the first 900
  pixels.
  User feedback rounds later are unlimited; each accepted revision is a new
  version with its own internal three-cycle validation budget.
- For reproduction, pass all source handles to `penpot-source-map`; never
  discard a supplied source silently.
- Do not ask again for permission to inspect or reuse assets from a supplied
  site/runtime or codebase: that permission is a standing workflow decision.
  Ask only about material licensing, privacy or source-precedence restrictions.

Write `questions.md`, `decisions.md` and `manifest.json` with the required
schema. Set `worker_model` to `gpt-5.6-luna` for any delegated acquisition or
inspection. If unavailable, return `BLOCKED_MODEL_UNAVAILABLE`.

## CLI handoff

For URL capture, hand the worker the command
`scripts/capture.sh --url <URL> --output <dir> --viewport <WxH>` from this
skill's physical directory.
For authenticated sources, add `--storage-state <ignored-private-json>`; the
capture manifest records only `authenticated: true`, a sanitized URL and its
hash, never cookies or the private path.
For a supplied screenshot, hand it to `$penpot-source-map`.
Repository inspection is performed by the Luna worker against the checked-out
code and recorded in the source inventory; no unimplemented helper is assumed.
