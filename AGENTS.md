# Agent instructions for Penpot Design Automation

This file is the portable entrypoint for Codex, Devin CLI, Claude Code,
Gemini, Cursor and other repository-aware agents. Read it before modifying or
running the project. The repository is the source of truth for the executable
workflow; the shared vault stores project context and human-review notes.

## What this repository does

- Runs one shared local Penpot instance for future projects.
- Provides seven Agent Skills under `skills/` for intake, source mapping,
  building, validation, design-system formalization and delivery.
- Accepts a URL, screenshot, running app, code repository or a prompt without a
  source.
- Records source provenance and reuses exact source assets when available.
- Uses deterministic visual gates: score `>= 90`, coverage `>= 80%`, no P0/P1,
  and at most three internal correction cycles per version.

## Required operating contract

1. Start from `skills/penpot-design/SKILL.md` and read only the phase skill and
   references needed for the current request.
2. In every run, ask the mandatory intake questions, ask the final
   adendo/mudança question, then analyze unresolved decisions before building.
3. In reproduction, map every supplied source before changing Penpot. Inspect
   the supplied site/runtime/repository for SVGs, images, icons, logos, fonts
   and other useful assets; prefer those exact files and record provenance.
4. Treat desktop `1440x900` as the observation viewport and minimum frame. Let
   finite pages grow vertically; expand horizontally only with evidence of
   intentional page-level navigation. Require an approved bounded state for
   dynamic or infinite content.
5. Delegate hands-on capture, inspection, MCP construction, rendering,
   correction and scoring to `gpt-5.6-luna`. If that worker is unavailable,
   stop with `BLOCKED_MODEL_UNAVAILABLE` instead of falling back silently.
6. Never edit scores, thresholds, immutable cycle artifacts or source evidence
   to make a run pass. A failed gate returns to targeted refactoring; cycle 3
   ends in `NEEDS_REVIEW`.
7. After formal user approval, build and revalidate the design system. Do not
   mark delivery complete while the structural gate is failing.

## Skills and shared lessons

Every skill is a self-contained Agent Skills package with `SKILL.md`, optional
`agents/`, `scripts/`, `references/`, `assets/` and a required
`lessons-learned/` directory. Read the local lessons README at the start and
end of work. Add new lessons to the skill that exposed the failure; mark a
lesson `mitigated` only after a regression test or equivalent verification.

Classify the lesson before recording it. Use `kind: machine` for a local
station/OS/Docker/browser/network/credential issue; keep it in lessons only.
Use `kind: project` for a rule about this workflow and provide `--integration`
pointing to the skill, reference, script, test or gate that now enforces it.

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
./setup.sh
infra/penpot/scripts/up.sh
infra/penpot/scripts/healthcheck.sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_skills.py
./install.sh
```

`setup.sh` is idempotent: it never overwrites an existing `.env`, skill link or
volume. On a fresh clone it generates local secrets and creates neutral Docker
volumes; the migrated KatiauInvest machine keeps its legacy volume names only
in its ignored `.env`.

The installer creates a single global symlink to
`skills/penpot-design`; it does not copy or fork the skill. Use the wrappers
inside the selected skill for capture, source mapping, MCP and validation so
they resolve the repository even when launched from `/` or another checkout.

## Adapter guidance

- Codex: invoke `$penpot-design` after installing with `./install.sh`.
- Devin CLI, Claude Code, Gemini and Cursor: read this file, then invoke the
  relevant `skills/<name>/SKILL.md` directly and preserve the same artifacts,
  gates and lesson protocol.
- Any agent may run tests and read sanitized manifests. Only an explicitly
  delegated Luna worker may perform hands-on Penpot mutations for a run.
