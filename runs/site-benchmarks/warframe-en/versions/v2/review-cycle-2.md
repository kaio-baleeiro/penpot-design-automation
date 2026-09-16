---
type: root-review
status: failed
created: 2026-09-16
source_agent: codex-root
review: true
---

# Revisão oficial — Warframe EN v2 — ciclo 2

## Decisão

**REPROVADO COM REGRESSÃO.** Score **71,94/100**, cobertura **65,6995%**,
dezessete regiões P1 e uma P1 de regressão. O ciclo caiu 7,00 pontos em
relação ao ciclo 1. O gate estrutural do ciclo regular passou, mas a fidelidade
visual e semântica falhou.

## Causa raiz confirmada no export

Os elementos das seções foram criados, porém muitos filhos de boards usam
coordenadas verticais de página como se fossem coordenadas locais. Dentro de
um board em `y=N`, um filho colocado novamente perto de `y=N` é deslocado para
fora da área útil do contêiner e fica recortado. Isso explica a divergência
entre a contagem de 113 shapes/17 imagens e as extensas áreas vazias no export.

## Problemas visuais e semânticos

- O herói melhorou em cor e conteúdo, mas ainda usa escala, crop, hierarquia e
  composição diferentes da fonte; o key art do personagem central continua
  ausente.
- `NEWS & UPDATES`, `SHOP WARFRAME`, `PRIME RESURGENCE`, guias, comunidade e
  rodapé continuam visualmente vazios ou quase vazios no export, apesar de
  existirem como objetos no inventário.
- Conteúdo/densidade caiu para **56,59** e assets para **40,77**, comprovando
  que a simples presença estrutural não se converteu em pixels visíveis.
- Persistem P1 extensos em `y=66..1398`, `y=1706..2625` e `y=4012..4403`.

## Correção obrigatória no ciclo 3

1. Converter as coordenadas de todos os filhos para o sistema local de cada
   board: `local_y = page_y - board_y`, ou mover os elementos para o frame raiz
   mantendo coordenadas globais. Não misturar os dois sistemas.
2. Após cada grupo de seções, exportar e verificar visualmente que News, Shop,
   Prime, Guides, Community, Legal e Footer realmente aparecem.
3. Recuperar o herói central vermelho da fonte e reduzir/remover o logotipo
   gigante que domina a composição atual.
4. Preservar copy, ordem e assets first-party da fonte; nenhum placeholder.
5. Este é o terceiro e último ciclo. Se score <90, cobertura <80%, houver P1
   ou o gate semântico falhar, encerrar como `NEEDS_REVIEW` sem quarto ciclo.

## Evidências

- `cycles/cycle-2/score.json`
- `cycles/cycle-2/issues.json`
- `../../analysis/v2-cycle-2-home-side-by-side-annotated.png`
- `../../analysis/v2-cycle-2-home-overlay.png`
- `../../analysis/v2-cycle-2-home-heatmap.png`
