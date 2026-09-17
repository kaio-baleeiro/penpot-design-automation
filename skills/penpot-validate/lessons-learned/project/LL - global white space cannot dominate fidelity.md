---
type: lesson
status: mitigated
kind: project
integration: skills/penpot-validate/references/scoring.md; scripts/penpot_validation/metrics.py; tests/test_penpot_validation.py
scope: penpot-validate
---

# Global white space cannot dominate fidelity

## Failure

A sparse but semantically wrong GitHub layout scored above 98 because global
background, bounding-box and histogram similarity overwhelmed local UI errors.

## Rule

Score long and sparse pages by local regions, weight foreground and edges, and
apply a lower-region penalty. Numeric similarity remains separate from semantic,
asset-provenance and structural gates.

## Integration

The v2 evaluator and `references/scoring.md` implement this regional rule.
