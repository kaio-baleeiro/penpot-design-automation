---
id: build-screenshot-is-not-editable-design
kind: project
status: mitigated
title: Full-page reference images cannot masquerade as the delivered design
integration: penpot-build/SKILL.md; penpot-validate/SKILL.md; scripts/penpot_validation/structure.py
---

## Failure

Um benchmark recebeu uma captura `full_page` dentro do Penpot e recebeu nomes
de componentes sem descendentes substanciais. A aparência ficou próxima da
origem, mas o artefato não era editável como as telas D0 do projeto.

## Rule

A imagem de referência pode existir apenas em camada de evidência oculta ou
bloqueada. O frame entregue precisa reconstruir cada seção com textos, formas,
vetores e assets reais; componentes precisam ter descendentes substantivos e
instâncias no frame visível.

## Countermeasure

O build agora rejeita explicitamente um frame de uma imagem ou de labels
semânticos vazios. O inventário registra contagens por tipo e instâncias, e a
validação aplica um gate estrutural independente do score visual.

## Verification

O contrato de `penpot-build`, `penpot-validate` e `penpot-design` foi atualizado;
o próximo rebuild dos benchmarks é obrigado a produzir a árvore editável antes
de ser considerado pronto para revisão.
