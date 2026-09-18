---
id: build-structural-inventory-gate
kind: project
status: mitigated
title: Structural inventory is a build gate
integration: penpot-build/SKILL.md; penpot-validate/SKILL.md; scripts/penpot_validation/structure.py
---

# Inventário estrutural é gate de construção

Uma imagem visualmente próxima não comprova que o frame contém texto, formas,
componentes e instâncias editáveis. Antes do handoff, gere
`design/structure-inventory.json` a partir do frame real e bloqueie a validação
quando o inventário estiver ausente, vazio, image-only ou contiver instâncias
destacadas sem justificativa.

O inventário deve registrar ao menos frames, contagem de descendentes
editáveis, imagens, tokens, componentes, instâncias e detached instances. O
revisor raiz confirma esse gate separadamente do score visual.
