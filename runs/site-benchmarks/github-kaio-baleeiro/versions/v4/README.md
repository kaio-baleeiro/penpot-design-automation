# GitHub Kaio — v4

Reconstrução editável versionada do perfil público `kaio-baleeiro`, baseada na
fonte full-page em `../v2/source/reference.png` e no frame finito
1440×1807.

- página Penpot: `Benchmark — GitHub Kaio v4`
- frame: `GitHub Kaio — Home — 1440x1807 — v4`
- página id: `b9b9f43f-1dd3-801e-8008-a6725d4e8fbd`
- frame id: `b9b9f43f-1dd3-801e-8008-a6741a129cb3`
- export atual: `exports/cycle-3.png`
- estado final: `NEEDS_REVIEW`

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

`v2` e `v3-validation-rerun` permanecem intactos. O log MCP append-only está
em `design/penpot-mcp-log.jsonl`.
