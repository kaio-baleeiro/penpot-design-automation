---
type: lesson
status: active
skill: penpot-validate
kind: project
integration: scripts/penpot_validation/validator.py; skills/penpot-validate/SKILL.md; tests/test_penpot_validation.py
created: 2026-09-16
updated: 2026-09-16
source_agent: portable-agent
confidence: high
review: false
applies_to:
  - penpot-build,penpot-validate,penpot-delivery
---

# LL - Inventário estrutural vazio invalida o benchmark

## Lesson

Uma reconstrução pode parecer visualmente próxima, mas sem inventário de frames, descendentes, componentes, instâncias e estilos não há prova de que o Penpot contém um design editável.

## Context

Um run legado registrou `structure-inventory.json` vazio e obteve score visual
alto sem evidência estrutural.

## Evidence

scripts/penpot_validation/validator.py; tests/test_penpot_validation.py; agents/profiles/visual-qa-auditor/AGENT.md

## Future Rule

Em toda validação de schema estrito, exigir structure-inventory.json não vazio e bloquear a aprovação quando ele faltar, estiver vazio ou não provar descendentes editáveis.
