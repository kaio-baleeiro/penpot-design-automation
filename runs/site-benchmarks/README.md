# Benchmark de sites

Runs de reprodução pública em viewport base 1440×900.

Cada run preserva a fonte, decisões, frame-spec e o paralelo visual gerado
pela análise. A rodada v4 é a reconstrução atual, executada com o avaliador
regional `penpot-visual-v2`; os resultados anteriores permanecem como histórico.

| Site | Run | Estado |
|---|---|---|
| Apple Brasil | [Apple v4](apple-br/versions/v4/README.md) | NEEDS_REVIEW · `71,38 → 71,08 → 71,04` |
| Warframe English | [Warframe v4](warframe-en/versions/v4/README.md) | NEEDS_REVIEW · `64,23 → 65,38 → 64,03` |
| GitHub kaio-baleeiro | [GitHub v4](github-kaio-baleeiro/versions/v4/README.md) | NEEDS_REVIEW · `83,79 → 83,92 → 84,10` |

## Galeria v4 — ciclo final

O detail board mostra fonte, export do Penpot e heatmap em faixas verticais
legíveis. Os links laterais dão acesso às imagens completas.

| Site | Detail board | Comparações completas |
|---|---|---|
| Apple Brasil | ![Apple v4 detail board](apple-br/analysis/v4-cycle-3-home-detail-board.png) | [side-by-side](apple-br/analysis/v4-cycle-3-home-side-by-side-annotated.png) · [overlay](apple-br/analysis/v4-cycle-3-home-overlay.png) · [heatmap](apple-br/analysis/v4-cycle-3-home-heatmap.png) |
| Warframe English | ![Warframe v4 detail board](warframe-en/analysis/v4-cycle-3-home-detail-board.png) | [side-by-side](warframe-en/analysis/v4-cycle-3-home-side-by-side-annotated.png) · [overlay](warframe-en/analysis/v4-cycle-3-home-overlay.png) · [heatmap](warframe-en/analysis/v4-cycle-3-home-heatmap.png) |
| GitHub kaio-baleeiro | ![GitHub v4 detail board](github-kaio-baleeiro/analysis/v4-cycle-3-home-detail-board.png) | [side-by-side](github-kaio-baleeiro/analysis/v4-cycle-3-home-side-by-side-annotated.png) · [overlay](github-kaio-baleeiro/analysis/v4-cycle-3-home-overlay.png) · [heatmap](github-kaio-baleeiro/analysis/v4-cycle-3-home-heatmap.png) |

Os quatro artefatos também estão publicados para os ciclos 1 e 2 com o prefixo
`v4-cycle-N-` em cada pasta `analysis/`. Nenhum benchmark foi aprovado: Apple e
Warframe falharam score e cobertura; GitHub passou cobertura, mas não o score.

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
