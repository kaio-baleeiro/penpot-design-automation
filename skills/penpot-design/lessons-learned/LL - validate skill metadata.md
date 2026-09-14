---
type: lesson
status: mitigated
scope: shared
applies_to: [penpot-design, penpot-intake, penpot-source-map, penpot-build, penpot-validate, penpot-design-system, penpot-delivery]
---

# Metadata precisa passar no spec e no host

Uma skill pode parecer correta no host e ainda quebrar o padrão Agent Skills,
ou o inverso. Valide frontmatter, nome, descrição, recursos referenciados,
scripts executáveis, `agents/openai.yaml` e o validador oficial antes de
publicar.

Verificação: `scripts/validate_skills.py`, `quick_validate.py` e `skills-ref`.
