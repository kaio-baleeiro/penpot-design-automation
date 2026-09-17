---
type: lesson
status: mitigated
kind: project
integration: skills/penpot-validate/SKILL.md; scripts/penpot_validation/validator.py; tests/test_penpot_validation.py
scope: penpot-validate
---

# Unchanged export is not a refinement cycle

## Failure

Three cycle directories were produced from the same Penpot PNG, so the reports
looked like iterative validation although no design mutation occurred.

## Rule

After a failed cycle, require a different Penpot export hash and an MCP mutation
record before starting the next cycle. A validation-only rerun is diagnostic and
must not consume or be presented as one of the three refactor cycles.

## Integration

This rule is enforced by the validator and described directly in
`skills/penpot-validate/SKILL.md`.
