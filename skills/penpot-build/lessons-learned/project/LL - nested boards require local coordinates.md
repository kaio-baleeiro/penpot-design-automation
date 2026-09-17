---
id: build-nested-boards-local-coordinates
kind: project
status: mitigated
title: Nested Penpot boards require one explicit coordinate contract
integration: penpot-build/SKILL.md; Warframe EN v2 cycle 3 verification
---

## Failure

No ciclo 2 do benchmark Warframe, o inventário registrou 113 shapes e 17
imagens, mas quase todas as seções inferiores ficaram vazias no export. Os
filhos de boards aninhados receberam coordenadas verticais da página inteira e
foram deslocados para fora da área recortada do próprio board.

## Rule

`penpotUtils.setParentXY` recebe coordenadas locais ao pai. Cada helper deve
declarar se recebe âncoras globais ou locais. Ao receber medidas da página,
converta uma única vez com `local_x = page_x - board_x` e
`local_y = page_y - board_y`; quando a entrada já for local, passe-a sem
subtrair novamente. Nunca misture os dois contratos no mesmo helper.

## Countermeasure

O contrato de build agora exige o tipo de entrada no helper, a conversão
explícita quando necessária e uma inspeção do export full-page que confirme
conteúdo visível em cada seção mapeada. Contagens de shapes, textos e imagens
não substituem essa verificação visual.

## Verification

O ciclo 3 do Warframe EN v2 converteu os 104 filhos aninhados e o export
`1440x5837-cycle3.png` passou a exibir Hero, News, Shop, Prime, Guides,
Community, Legal e Footer. A revisão oficial confirmou geometria global 99,41;
o benchmark permaneceu `NEEDS_REVIEW` por outras divergências de fidelidade.
No GitHub v4, a navegação de perfil recebeu valores já locais em um helper de
âncoras globais e foi recortada; o ciclo 3 reposicionou 14 descendentes com
`setParentXY` local e elevou o score de 83,92 para 84,10.
