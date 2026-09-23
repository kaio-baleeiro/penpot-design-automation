# Agent instructions for Penpot Design Automation

This file is the portable entrypoint for Codex, Devin CLI, Claude Code,
Gemini, Cursor and other repository-aware agents. Read it before modifying or
running the project. The repository is the source of truth for the executable
workflow; the shared vault stores project context and human-review notes.

## Mandatory first turn

Every client session must begin with `./penpot-workflow begin`. Ask the exact
question it prints and wait for the user's choice before inspecting a source,
editing files, starting containers, or resuming a design run. Record the
verbatim answer with `./penpot-workflow select <mode> --user-answer "..."`.

For `infrastructure`, execute `./penpot-workflow bootstrap-infra`; this creates
the ignored root `.env`, starts Penpot, provisions the local automation account
and MCP, returns account email/password, and stores the MCP token only in `.env`.
For `design`, use the controller and guarded wrappers. Never bypass them by
calling underlying capture, MCP, inventory, validation or delivery scripts.

Launch supported CLIs through `./agent codex|claude|devin|gemini`. A raw
third-party CLI that intentionally ignores repository instructions cannot be
forced to comply; the launcher and internal gates define the supported flow.
The gates block repository-provided mutation commands when the route/state is
wrong, but cannot prevent a client from bypassing the repository and invoking
an external MCP/server directly. Treat such direct calls as unsupported.

## What this repository does

- Runs one shared local Penpot instance for future projects.
- Provides seven Agent Skills under `skills/` for intake, source mapping,
  building, validation, design-system formalization and delivery.
- Provides specialized portable profiles under `agents/`; each operational
  phase receives the profile named by `agents/manifest.yaml`.
- Accepts a URL, screenshot, running app, code repository or a prompt without a
  source.
- Records source provenance and reuses exact source assets when available.
- Uses deterministic visual gates: score `>= 90`, coverage `>= 80%`, no P0/P1,
  and at most three internal correction cycles per version.

The public benchmark tree is canonical at v4. Apple BR, Warframe EN and GitHub
Kaio v4 were accepted by the user as the official reference versions. This
human acceptance is separate from the automated visual gate: a benchmark may
remain `NEEDS_REVIEW` when score, coverage or issue thresholds fail. Never
rewrite a score or call a failed automated gate a pass.

## Required operating contract

1. Pass the mandatory first-turn gate above. Start from
   `skills/penpot-design/SKILL.md` and read only the phase skill and
   references needed for the current request.
2. In every run, ask the mandatory intake questions, ask the final
   adendo/mudança question, then analyze unresolved decisions before building.
3. In reproduction, map every supplied source before changing Penpot. Inspect
   the supplied site/runtime/repository for SVGs, images, icons, logos, fonts
   and other useful assets; prefer those exact files and record provenance.
4. Treat desktop `1440x900` as the observation viewport and minimum frame, not
   the final capture height. Every finite page must be captured and designed
   end-to-end; a longer page gets a taller frame and a full-page reference
   image. Expand horizontally only with evidence of intentional page-level
   navigation. Require an approved bounded state for dynamic or infinite
   content.
5. Delegate hands-on capture, inspection, MCP construction, rendering,
   correction and scoring to the runtime's cost-efficient worker selected by
   `agents/runtime-policy.yaml`. Codex prefers `gpt-5.6-luna`; other hosts use
   their native worker mapping. Record the resolved runtime and model in every
   handoff. If no delegated worker is available, stop with
   `BLOCKED_WORKER_UNAVAILABLE`.
   For visual phases, the worker must open a representative image and record a
   hashed visual observation. A model alias alone is not evidence.
   Use the selected profile's `AGENT.md` and write its required handoff before
   advancing to the next phase. Source/script preparation may be parallel, but
   mutations, inventory and exports of one Penpot file are serial because the
   active page is shared.
6. Never edit scores, thresholds, immutable cycle artifacts or source evidence
   to make a run pass. A failed gate returns to targeted refactoring; cycle 3
   ends in `NEEDS_REVIEW`.
7. After formal user approval, build and revalidate the design system. Do not
   mark delivery complete while the structural gate is failing.

The portable profile contract is in `agents/contracts/handoff.md`. It is
host-neutral: Codex CLI, Devin CLI, Claude Code and similar tools preserve the
same inputs, outputs, gates and stop conditions.

## Skills and shared lessons

Every skill is a self-contained Agent Skills package with `SKILL.md`, optional
`agents/`, `scripts/`, `references/`, `assets/` and a required
`lessons-learned/` directory. Read the local lessons README at the start and
end of work. Add new lessons to the skill that exposed the failure; mark a
lesson `mitigated` only after a regression test or equivalent verification.

Classify the lesson before recording it. Use `kind: machine` for a local
station/OS/Docker/browser/network/credential issue; the recorder stores it in
`lessons-learned/local/`, ignored by Git. Use `kind: project` for a rule about
this workflow; it is stored in `lessons-learned/project/` and requires
`--integration` pointing to the skill, reference, script, test or gate that now
enforces it.

`skills/penpot-design/lessons-learned/README.md` is the cross-skill index. A
lesson that changes behavior in more than one phase must be linked there and
referenced from the affected skill READMEs. Use the recorder from the
repository root:

```sh
python3 skills/penpot-design/scripts/record-lesson.py \
  --skill-dir skills/penpot-validate record \
  --title "Short repeatable failure" \
  --lesson "What must be remembered." \
  --context "Where it happened." \
  --evidence "tests/test_..." \
  --future-rule "The rule to apply next time." \
  --kind project \
  --integration "skills/penpot-validate/SKILL.md; tests/test_..."
```

The recorder writes only inside the selected skill package. Do not commit
cookies, tokens, authenticated captures, `.env` files, Penpot exports or other
private payloads.

## Portable commands

Prerequisites for a fresh clone are Git, Python 3, Docker with Compose and
OpenSSL. Network access is needed once to download Python/Playwright packages
and Penpot images.

Run commands from the repository root, or use absolute paths when a CLI starts
in another directory:

```sh
# Recommended: launcher asks the first question in a fresh CLI session.
./agent codex

# Or initialize the controller manually, then choose exactly one route:
./penpot-workflow begin
./penpot-workflow select infrastructure --user-answer "quero preparar a infraestrutura"
./penpot-workflow bootstrap-infra

# For a design session, select design instead; do not run setup/bootstrap.
./penpot-workflow begin
./penpot-workflow select design --user-answer "quero trabalhar nos designs"

# Automated checks:
python3 -m unittest discover -s tests -v
python3 scripts/validate_skills.py
./install.sh
```

`bootstrap-infra` invokes `setup.sh` for prerequisites, then starts Penpot and
provisions account/MCP. `setup.sh` is idempotent: it never overwrites an
existing `.env`, skill link or volume. On a fresh clone it generates local
secrets and creates neutral Docker volumes; a migrated workstation keeps any
legacy volume names only in its ignored `.env` and local lessons.

The installer creates a single global symlink to
`skills/penpot-design`; it does not copy or fork the skill. Use the wrappers
inside the selected skill for capture, source mapping, MCP and validation so
they resolve the repository even when launched from `/` or another checkout.

## Runtime adapters

- Codex: invoke `$penpot-design` after `./install.sh`; the preferred worker is
  `gpt-5.6-luna`.
- Claude Code: `CLAUDE.md` loads this contract and `.claude/agents/` exposes
  the phase profiles.
- Devin CLI: this `AGENTS.md` is loaded directly and `.devin/agents/` exposes
  the phase profiles.
- Gemini CLI: `GEMINI.md` imports this contract and `.gemini/agents/` exposes
  the phase profiles.
- Other agents: read this file, `skills/penpot-design/SKILL.md`, and the
  canonical profile under `agents/profiles/`; use a separate cost-efficient
  worker when the host supports delegation. Unknown workers must pass the
  visual probe before a visual phase.

Run `python3 scripts/sync_agent_adapters.py --check` after changing a canonical
profile. Generated adapters must stay synchronized with `agents/profiles/`.
Any agent may run tests and read sanitized manifests. A delegated worker may
mutate Penpot only after its runtime and concrete model are recorded.
