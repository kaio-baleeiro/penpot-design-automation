---
type: lesson
status: mitigated
kind: project
integration: skills/penpot-build/SKILL.md; scripts/validate_asset_readiness.py; tests/test_asset_readiness.py
scope: penpot-build
---

# Silent asset fallback corrupts fidelity

## Failure

When an upload failed, benchmark builders silently retained a colored rectangle.
The frame remained technically editable but no longer represented the source.

## Rule

Every planned image must resolve through an `asset_ref`, pass the readiness gate
and record its upload result. Upload failure blocks the build; it never degrades
silently to a generic rectangle in a fidelity benchmark.

## Integration

`penpot-build/SKILL.md` and `scripts/validate_asset_readiness.py` enforce the rule.
