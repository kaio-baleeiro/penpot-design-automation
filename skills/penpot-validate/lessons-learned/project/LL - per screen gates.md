---
type: lesson
status: mitigated
kind: project
integration: scripts/penpot_validation/validator.py; tests/test_workflow_gates.py
scope: penpot-validate
---

# O gate é por tela e viewport

Uma média agregada não pode esconder dashboard ou estado que falhou. Score,
cobertura, P0/P1, dimensões e estrutura devem passar individualmente para cada
viewport solicitado.

Verificação: fixture terminal em `NEEDS_REVIEW` e testes de gates.
