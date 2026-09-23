---
type: lesson
status: mitigated
skill: penpot-design
kind: project
integration: scripts/workflow_guard.py; agent; penpot-workflow; AGENTS.md; tests/test_workflow_controller.py
created: 2026-09-23
updated: 2026-09-23
source_agent: portable-agent
confidence: high
review: false
applies_to:
  - penpot-design
---

# LL - Repository rules need executable gates

## Lesson

Agent instructions alone cannot guarantee sequence adherence. Make the supported launcher ask the first route question and enforce route/state/artifact prerequisites in the commands that mutate workflow state; state explicitly that a raw client can still bypass the repository and invoke external tools.

## Context

Workflow portability review for clients that may start in the repository and have access to Penpot MCP.

## Evidence

tests/test_workflow_controller.py; tests/test_workflow_gates.py; scripts/workflow_guard.py; AGENTS.md

## Future Rule

When adding an operational path, test that it fails before the required user choice or state, and make sure it uses the shared controller. Never claim that repository files can constrain a client that deliberately ignores them.

## Resolution

Resolved: 2026-09-23

### Countermeasure

Added a fresh-session launcher, explicit route selection, guards at mutating wrappers and internal CLI entrypoints, artifact audits on state transitions, and documented the residual bypass boundary.

### Verification

python3 -m unittest discover -s tests -v; python3 scripts/validate_skills.py; python3 scripts/validate_agent_profiles.py; git diff --check
