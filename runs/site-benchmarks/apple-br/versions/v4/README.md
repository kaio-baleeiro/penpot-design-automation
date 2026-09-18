# Apple BR v4

Reconstrução editável e versionada da página inicial da Apple Brasil. A fonte
é a captura full-page `1440×5261` registrada no pacote desta versão; a imagem
não foi usada como camada visível da entrega. Esta v4 foi aceita pelo usuário
como a versão oficial/canônica do benchmark.

- página Penpot: `Benchmark — Apple BR v4`
- frame: `Apple BR — Home — 1440x5261 — v4`
- página id: `b9b9f43f-1dd3-801e-8008-a6714b37dc3b`
- frame id: `b9b9f43f-1dd3-801e-8008-a67202c01eef`
- aceitação humana: `CANÔNICA / ACEITA PELO USUÁRIO`
- gate automático: `NEEDS_REVIEW`

## Ciclos

| Ciclo | Score | Cobertura | Resultado | Evidência legível |
|---:|---:|---:|---|---|
| 1 | 71,38 | 75,76% | REFINEMENT | [detail board](cycles/cycle-1/home-detail-board.png) |
| 2 | 71,08 | 76,83% | REFINEMENT | [detail board](cycles/cycle-2/home-detail-board.png) |
| 3 | 71,04 | 75,72% | NEEDS_REVIEW | [detail board](cycles/cycle-3/home-detail-board.png) |

O frame permaneceu abaixo dos gates automáticos de score e cobertura após três
ciclos. A divergência principal está na escala/crop dos assets hero e TV, seguida da
densidade incompleta do rodapé. Consulte o `report.md`, side-by-side, overlay e
heatmap em cada diretório de ciclo.

## Quickstart no Penpot

Abra [http://localhost:9001](http://localhost:9001), selecione o projeto
`Penpot Benchmarks` e o arquivo `Site Benchmarks`. A página é `Benchmark — Apple
BR v4` e o frame é `Apple BR — Home — 1440x5261 — v4`.

- página id: `b9b9f43f-1dd3-801e-8008-a6714b37dc3b`
- frame id: `b9b9f43f-1dd3-801e-8008-a67202c01eef`

`source/` contém a referência e a procedência; `design/` contém plano,
inventários e log MCP; `exports/` contém renders dos frames editáveis; `cycles/` contém
score, issues, relatório, comparação, overlay e heatmap. O estado automático
`NEEDS_REVIEW` não invalida a aceitação humana da v4 como canônica.

Registro da decisão: [aprovação canônica v001](approvals/approval-v001.md).
