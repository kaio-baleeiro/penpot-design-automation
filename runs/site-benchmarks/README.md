# Benchmark de sites

Runs de reprodução pública em viewport base 1440×900.

Cada run preserva a fonte, decisões, frame-spec e o paralelo visual gerado
pela análise. As imagens abaixo são evidências públicas sanitizadas; o score
fica ausente quando o gate não pôde comparar um export do Penpot.

| Site | Run | Estado |
|---|---|---|
| Apple Brasil | [apple-br](apple-br/README.md) | v2 · NEEDS_REVIEW · 89,57 · 3 ciclos |
| Warframe English | [warframe-en](warframe-en/README.md) | v2 planejado · limite dinâmico aguardando aprovação |
| GitHub kaio-baleeiro | [github-kaio-baleeiro](github-kaio-baleeiro/README.md) | v2 · NEEDS_REVIEW · 98,52 · 3 ciclos |

## Galeria de análise

| Site | Referência | Side-by-side | Overlay | Heatmap |
|---|---|---|---|---|
| Apple Brasil | ![referência Apple](apple-br/source/reference.png) | ![Apple side-by-side](apple-br/analysis/side-by-side-annotated.png) | [overlay](apple-br/analysis/overlay.png) | [heatmap](apple-br/analysis/heatmap.png) |
| Warframe English | ![referência Warframe](warframe-en/source/reference.png) | ![Warframe side-by-side](warframe-en/analysis/side-by-side-annotated.png) | [overlay](warframe-en/analysis/overlay.png) | [heatmap](warframe-en/analysis/heatmap.png) |
| GitHub kaio-baleeiro | ![referência GitHub](github-kaio-baleeiro/source/reference.png) | ![GitHub side-by-side](github-kaio-baleeiro/analysis/side-by-side-annotated.png) | [overlay](github-kaio-baleeiro/analysis/overlay.png) | [heatmap](github-kaio-baleeiro/analysis/heatmap.png) |

## Reconstruções v2 e histórico de ciclos

As versões v2 ficam no arquivo Penpot `Site Benchmarks`, projeto `Penpot
Benchmarks`, fora do arquivo do KatiauInvest. O orquestrador principal pontuou
cada ciclo; Luna executou captura, construção, exportação e correções.

- Apple: [pacote v2](apple-br/versions/v2/README.md), com
  [referência full-page 1440×5261](apple-br/versions/v2/source/reference-full-page.png)
  e comparações públicas dos ciclos [1](apple-br/analysis/v2-cycle-1-home-side-by-side-annotated.png),
  [2](apple-br/analysis/v2-cycle-2-home-side-by-side-annotated.png) e
  [3](apple-br/analysis/v2-cycle-3-home-side-by-side-annotated.png). Evolução:
  `85,93 → 87,30 → 89,57`; terminou `NEEDS_REVIEW`.
- GitHub: [pacote v2](github-kaio-baleeiro/versions/v2/README.md), com
  [referência full-page 1440×1807](github-kaio-baleeiro/versions/v2/source/reference.png)
  e comparações públicas dos ciclos
  [1](github-kaio-baleeiro/analysis/v2-cycle-1-home-side-by-side-annotated.png),
  [2](github-kaio-baleeiro/analysis/v2-cycle-2-home-side-by-side-annotated.png)
  e [3](github-kaio-baleeiro/analysis/v2-cycle-3-home-side-by-side-annotated.png).
  Evolução: `93,96 → 96,77 → 98,52`; o score visual passou, mas a revisão de
  conteúdo/fonte reprovou e o estado final é `NEEDS_REVIEW`.
- Warframe: [planejamento v2](warframe-en/versions/v2/README.md). A origem é
  dinâmica; o limite reproduzível proposto é `1440×5837` e não será pontuado
  antes de aprovação explícita.

Cada `analysis/v2-cycle-N-*` contém side-by-side, overlay e heatmap públicos.
Os diretórios `cycles/cycle-N/` são evidência imutável do avaliador e não devem
ser editados nem usados como destino de exportações do Penpot.
