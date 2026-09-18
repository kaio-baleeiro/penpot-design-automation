# Apple Brasil benchmark

Fonte pública: <https://www.apple.com/br/>
Viewport observado: 1440×900. A captura registrou conteúdo fora do viewport,
mas o frame aprovado contém a página em 1440×5261 e trata a largura extra como
overflow acidental. [Referência oficial](versions/v4/source/reference.png).

Versão oficial/canônica: [v4](versions/v4/README.md), aceita pelo usuário.
O gate automático permanece **NEEDS_REVIEW** após três ciclos:
`71,38 → 71,08 → 71,04`; cobertura final `75,72%`. Score e cobertura continuam
abaixo da régua automática.

Frame Penpot editável: `Apple BR — Home — 1440x5261 — v4`.
[Render do ciclo 3](versions/v4/exports/cycle-3.png). A captura full-page
original permanece apenas como evidência de comparação.

Análise v4 final: [detail board](analysis/v4-cycle-3-home-detail-board.png) ·
[side-by-side](analysis/v4-cycle-3-home-side-by-side-annotated.png) ·
[overlay](analysis/v4-cycle-3-home-overlay.png) ·
[heatmap](analysis/v4-cycle-3-home-heatmap.png).

O quickstart do Penpot está no índice de [benchmarks](../README.md). Abra o
projeto `Penpot Benchmarks`, arquivo `Site Benchmarks`, página `Benchmark — Apple
BR v4` e frame `Apple BR — Home — 1440x5261 — v4`. Consulte o README da v4 para
os IDs e a descrição dos artefatos.
