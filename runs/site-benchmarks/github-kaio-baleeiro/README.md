# GitHub Kaio — v4

Reconstrução editável canônica do perfil público `kaio-baleeiro`, baseada na
fonte full-page do pacote e no frame finito 1440×1807. Este pacote único contém
a v4 aceita pelo usuário como baseline oficial/canônico do benchmark.

- página Penpot: `Benchmark — GitHub Kaio v4`
- frame: `GitHub Kaio — Home — 1440x1807 — v4`
- página id: `b9b9f43f-1dd3-801e-8008-a6725d4e8fbd`
- frame id: `b9b9f43f-1dd3-801e-8008-a6741a129cb3`
- export atual: `exports/cycle-3.png`
- aceitação humana: `CANÔNICA / ACEITA PELO USUÁRIO`
- gate automático: `NEEDS_REVIEW`

## Ciclos

| Ciclo | Score | Cobertura | Resultado | Evidência legível |
|---:|---:|---:|---|---|
| 1 | 83,79 | 93,46% | REFINEMENT | [detail board](cycles/cycle-1/home-detail-board.png) |
| 2 | 83,92 | 93,42% | REFINEMENT | [detail board](cycles/cycle-2/home-detail-board.png) |
| 3 | 84,10 | 93,32% | NEEDS_REVIEW | [detail board](cycles/cycle-3/home-detail-board.png) |

O ciclo 2 restaurou pills editáveis e o asset exato do Pull Shark. O ciclo 3
corrigiu a navegação de perfil recortada por mistura de coordenadas locais e
globais. A cobertura passou, mas o score permaneceu abaixo de 90, sobretudo por
tipografia, bordas/spacing e diferenças finas de assets.

## Quickstart no Penpot

Abra [http://localhost:9001](http://localhost:9001), selecione o projeto
`Penpot Benchmarks` e o arquivo `Site Benchmarks`. A página é `Benchmark —
GitHub Kaio v4` e o frame é `GitHub Kaio — Home — 1440x1807 — v4`.

- página id: `b9b9f43f-1dd3-801e-8008-a6725d4e8fbd`
- frame id: `b9b9f43f-1dd3-801e-8008-a6741a129cb3`

`source/` contém a referência e a procedência; `design/` contém plano,
inventários e log MCP; `exports/` contém renders dos frames editáveis; `cycles/` contém
score, issues, relatório, comparação, overlay e heatmap. O estado automático
`NEEDS_REVIEW` não invalida a aceitação humana da v4 como canônica.

Registro da decisão: [aprovação canônica v001](approvals/approval-v001.md).
