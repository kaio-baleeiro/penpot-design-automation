---
type: lesson
status: mitigated
skill: penpot-design
kind: project
integration: skills/penpot-design/SKILL.md; skills/penpot-design/references/delegation.md; agents/runtime-policy.yaml; scripts/sync_agent_adapters.py; tests/test_agent_profiles.py
created: 2026-09-21
updated: 2026-09-21
source_agent: portable-agent
confidence: high
review: false
applies_to:
  - penpot-design, all delegated phases
---

# LL - Vendor model cannot define a portable workflow

## Lesson

Canonical profiles must describe capabilities and gates; runtime adapters select concrete models.

## Context

The workflow claimed support for Codex, Claude, Devin and Gemini while validators and manifests required gpt-5.6-luna.

## Evidence

agents/runtime-policy.yaml; scripts/validate_agent_profiles.py; tests/test_agent_profiles.py

## Future Rule

Keep canonical profiles vendor-neutral, resolve an economical worker per host, and record the concrete runtime/model in each run and handoff.

## Resolution

Resolved: 2026-09-21

### Countermeasure

Canonical profiles now declare a cost-efficient model class; runtime-policy.yaml maps each host; native adapters are generated and strict manifests record execution metadata.

### Verification

scripts/sync_agent_adapters.py --check, validate_agent_profiles.py, validate_skills.py and all 75 unit tests passed on 2026-09-21.
