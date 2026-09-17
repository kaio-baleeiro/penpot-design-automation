# Apple BR v4

Reconstrução editável e versionada da página inicial da Apple Brasil. A fonte
é a captura full-page `1440×5261` em
`../v2/source/reference-full-page.png`; a imagem não foi usada como camada
visível da entrega.

- página Penpot: `Benchmark — Apple BR v4`
- frame: `Apple BR — Home — 1440x5261 — v4`
- página id: `b9b9f43f-1dd3-801e-8008-a6714b37dc3b`
- frame id: `b9b9f43f-1dd3-801e-8008-a67202c01eef`
- estado final: `NEEDS_REVIEW`

## Ciclos

| Ciclo | Score | Cobertura | Resultado | Evidência legível |
|---:|---:|---:|---|---|
| 1 | 71,38 | 75,76% | REFINEMENT | [detail board](cycles/cycle-1/home-detail-board.png) |
| 2 | 71,08 | 76,83% | REFINEMENT | [detail board](cycles/cycle-2/home-detail-board.png) |
| 3 | 71,04 | 75,72% | NEEDS_REVIEW | [detail board](cycles/cycle-3/home-detail-board.png) |

O frame permaneceu abaixo dos gates de score e cobertura após três ciclos. A
divergência principal está na escala/crop dos assets hero e TV, seguida da
densidade incompleta do rodapé. Consulte o `report.md`, side-by-side, overlay e
heatmap em cada diretório de ciclo.

Plano, inventários e log MCP sanitizado ficam em `design/`; exports do Penpot
ficam em `exports/`. `v2` e `v3-validation-rerun` permanecem como histórico.
