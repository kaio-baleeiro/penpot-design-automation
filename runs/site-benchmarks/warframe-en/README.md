# Warframe EN v4

Reconstrução editável canônica do estado dinâmico aprovado em `1440×5837`.
O documento medido tem largura `1983`, registrada como overflow acidental; o
frame permanece com `1440` de largura conforme aprovação do usuário. Este pacote
único contém a v4 aceita pelo usuário como baseline oficial/canônico do benchmark.

- página Penpot: `Benchmark — Warframe EN v4`
- frame: `Warframe EN — Home — 1440x5837 — v4`
- página id: `b9b9f43f-1dd3-801e-8008-a67636574e02`
- frame id: `b9b9f43f-1dd3-801e-8008-a67636745b0f`
- aceitação humana: `CANÔNICA / ACEITA PELO USUÁRIO`
- gate automático: `NEEDS_REVIEW`

## Ciclos

| Ciclo | Score | Cobertura | Resultado | Evidência legível |
|---:|---:|---:|---|---|
| 1 | 64,23 | 56,98% | REFINEMENT | [detail board](cycles/cycle-1/home-detail-board.png) |
| 2 | 65,38 | 56,65% | REFINEMENT | [detail board](cycles/cycle-2/home-detail-board.png) |
| 3 | 64,03 | 61,58% | NEEDS_REVIEW | [detail board](cycles/cycle-3/home-detail-board.png) |

O segundo ciclo trocou o logo esticado pelo poster oficial, reutilizou as três
imagens exatas dos guias e melhorou a fidelidade. O terceiro ampliou cobertura
de conteúdo/social, mas regrediu em cor e composição da seção de notícias. O
hero da fonte é um frame de vídeo que não coincide com o poster disponível;
essa diferença permanece explícita e impede aprovação falsa.

Plano, inventários e log MCP sanitizado ficam em `design/`; exports do Penpot
ficam em `exports/`.

## Quickstart no Penpot

Abra [http://localhost:9001](http://localhost:9001), selecione o projeto
`Penpot Benchmarks` e o arquivo `Site Benchmarks`. A página é `Benchmark —
Warframe EN v4` e o frame é `Warframe EN — Home — 1440x5837 — v4`.

- página id: `b9b9f43f-1dd3-801e-8008-a67636574e02`
- frame id: `b9b9f43f-1dd3-801e-8008-a67636745b0f`

`source/` contém a referência e a procedência; `design/` contém plano,
inventários e log MCP; `exports/` contém renders dos frames editáveis; `cycles/` contém
score, issues, relatório, comparação, overlay e heatmap. O estado automático
`NEEDS_REVIEW` não invalida a aceitação humana da v4 como canônica.

Registro da decisão: [aprovação canônica v001](approvals/approval-v001.md).
