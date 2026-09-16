# Benchmark de sites

Runs de reprodução pública em viewport base 1440×900.

Cada run preserva a fonte, decisões, frame-spec e o paralelo visual gerado
pela análise. As imagens abaixo são evidências públicas sanitizadas; o score
fica ausente quando o gate não pôde comparar um export do Penpot.

| Site | Run | Estado |
|---|---|---|
| Apple Brasil | [apple-br](apple-br/README.md) | v3 revalidação · NEEDS_REVIEW · 89,57 · 3 ciclos |
| Warframe English | [warframe-en](warframe-en/README.md) | v3 revalidação · NEEDS_REVIEW · 83,34 · 3 ciclos |
| GitHub kaio-baleeiro | [github-kaio-baleeiro](github-kaio-baleeiro/README.md) | v3 revalidação · NEEDS_REVIEW · 98,52 · 3 ciclos |

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
- Warframe: [pacote v2](warframe-en/versions/v2/README.md), com
  [referência dinâmica aprovada 1440×5837](warframe-en/versions/v2/source/reference-full-page.png)
  e comparações públicas dos ciclos
  [1](warframe-en/analysis/v2-cycle-1-home-side-by-side-annotated.png),
  [2](warframe-en/analysis/v2-cycle-2-home-side-by-side-annotated.png) e
  [3](warframe-en/analysis/v2-cycle-3-home-side-by-side-annotated.png).
  Evolução: `78,94 → 71,94 → 83,34`; o terceiro ciclo corrigiu seções
  invisíveis, mas score, cobertura e fidelidade de fonte permaneceram abaixo
  dos gates, encerrando em `NEEDS_REVIEW`.

Cada `analysis/v2-cycle-N-*` contém imagens públicas de side-by-side, overlay e
heatmap para uma galeria rápida. Os diretórios `cycles/cycle-N/` também publicam
as imagens PNG geradas pelo avaliador (incluindo score, side-by-side anotado,
overlay e heatmap de cada iteração), para que alguém que clone o repositório
consiga entender o processo sem abrir o Penpot. Esses diretórios são evidência
imutável: não devem ser editados nem usados como destino de exportações do
Penpot. Capturas brutas, dumps de DOM/estilos, cookies e estado de sessão
continuam locais e ignorados.

## Revalidação v3

Os diretórios `*/versions/v3-validation-rerun/` são uma execução nova e
reprodutível do avaliador sobre os exports editáveis registrados na v2. Cada
um contém os três ciclos completos e os PNGs gerados em cada ciclo:

- [Apple — v3](apple-br/versions/v3-validation-rerun/README.md): [ciclo 1](apple-br/versions/v3-validation-rerun/cycles/cycle-1/home-side-by-side-annotated.png), [ciclo 2](apple-br/versions/v3-validation-rerun/cycles/cycle-2/home-side-by-side-annotated.png), [ciclo 3](apple-br/versions/v3-validation-rerun/cycles/cycle-3/home-side-by-side-annotated.png).
- [GitHub — v3](github-kaio-baleeiro/versions/v3-validation-rerun/README.md): [ciclo 1](github-kaio-baleeiro/versions/v3-validation-rerun/cycles/cycle-1/home-side-by-side-annotated.png), [ciclo 2](github-kaio-baleeiro/versions/v3-validation-rerun/cycles/cycle-2/home-side-by-side-annotated.png), [ciclo 3](github-kaio-baleeiro/versions/v3-validation-rerun/cycles/cycle-3/home-side-by-side-annotated.png).
- [Warframe — v3](warframe-en/versions/v3-validation-rerun/README.md): [ciclo 1](warframe-en/versions/v3-validation-rerun/cycles/cycle-1/home-side-by-side-annotated.png), [ciclo 2](warframe-en/versions/v3-validation-rerun/cycles/cycle-2/home-side-by-side-annotated.png), [ciclo 3](warframe-en/versions/v3-validation-rerun/cycles/cycle-3/home-side-by-side-annotated.png).

O avaliador foi executado novamente, sem copiar os scores. A aprovação
continua bloqueada quando score, cobertura, fidelidade semântica ou o gate
estrutural falham; consulte `score.json` e `report.md` de cada ciclo.
