---
id: build-nested-boards-local-coordinates
kind: project
status: mitigated
title: Nested Penpot boards require local descendant coordinates
integration: penpot-build/SKILL.md; Warframe EN v2 cycle 3 verification
---

## Failure

No ciclo 2 do benchmark Warframe, o inventário registrou 113 shapes e 17
imagens, mas quase todas as seções inferiores ficaram vazias no export. Os
filhos de boards aninhados receberam coordenadas verticais da página inteira e
foram deslocados para fora da área recortada do próprio board.

## Rule

Descendentes de um board usam coordenadas locais. Ao partir de medidas da
página, converta com `local_x = page_x - board_x` e
`local_y = page_y - board_y`, ou mantenha o elemento diretamente no frame raiz
com coordenadas globais. Nunca misture os dois sistemas no mesmo contêiner.

## Countermeasure

O contrato de build agora exige a conversão explícita e uma inspeção do export
full-page que confirme conteúdo visível em cada seção mapeada. Contagens de
shapes, textos e imagens não substituem essa verificação visual.

## Verification

O ciclo 3 do Warframe EN v2 converteu os 104 filhos aninhados e o export
`1440x5837-cycle3.png` passou a exibir Hero, News, Shop, Prime, Guides,
Community, Legal e Footer. A revisão oficial confirmou geometria global 99,41;
o benchmark permaneceu `NEEDS_REVIEW` por outras divergências de fidelidade.
