---
type: lesson
status: mitigated
scope: shared
applies_to: [penpot-design, penpot-intake, penpot-validate, penpot-delivery]
---

# O estado terminal precisa estar persistido

Scores e logs não bastam para inferir conclusão. O manifesto precisa registrar
estado, aprovação, ciclo, `lesson_refs` e motivos de `NEEDS_REVIEW` ou
`BLOCKED_MODEL_UNAVAILABLE`, permitindo retomada por outro agente.

Verificação: gates de manifesto, transições e fixture terminal KatiauInvest.
