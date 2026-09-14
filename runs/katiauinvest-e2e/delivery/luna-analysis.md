---
type: penpot-refactoring-handoff
status: NEEDS_REVIEW
created: 2026-09-14
updated: 2026-09-14
source_agent: codex
agent_context: katiauinvest-e2e cycle 1 strict deterministic validation
confidence: high
review: true
---

# KatiauInvest — handoff de correções Luna

## Decisão

O ciclo 1 foi executado pelo avaliador estrito com os quatro exports existentes. O resultado permanece **NEEDS_REVIEW**: score agregado 90,31/100 e cobertura 88,51%, mas dashboard e imports falham o gate por tela e existem issues P1. Não há aprovação de design ou de design system; não declarar `DELIVERED`.

Evidência máquina: `cycles/cycle-1/score.json`, `cycles/cycle-1/issues.json`, `cycles/cycle-1/report.md` e os artefatos side-by-side/overlay/heatmap correspondentes. Os scores são heurísticas de imagem e não provam texto, fonte, origem de assets ou editabilidade estrutural.

## Correções por tela

### dashboard — FAIL

Score 88,42; cobertura 76,91%; 20 issues P1. Os sinais dominantes são spacing/grid 78,05, content/density 69,80, color/border/shadow 83,89 e assets 85,99, com geometria (99,80) e tipografia (98,07) preservadas.

Causa provável: composição da faixa principal e dos cards inferiores está mais densa/deslocada que a referência; há diferenças de preenchimento/cor e de componentes agrupadas no miolo inferior. A barra superior também tem desalinhamentos locais.

Correções precisas:

- Reconstituir primeiro o bloco inferior grande em `(x=110,y=572,w=799,h=251)` e o bloco esquerdo em `(84,256,379,198)`, usando os mesmos limites, gaps e altura da captura-fonte; esses são os maiores deltas.
- Ajustar os cards/valores em `(547,640,168,119)`, `(722,641,170,88)`, `(550,559,165,84)`, `(126,558,244,39)`, `(723,597,169,49)` e `(378,559,164,38)` sem alterar a grade global.
- Corrigir os controles do cabeçalho em `(1159,127,181,44)`, `(1167,179,181,44)`, `(952,131,198,36)`, `(961,187,196,28)`, `(183,140,140,39)` e `(148,190,106,38)`: mesma posição, padding, raio e cor da fonte/controle da referência.
- Corrigir a linha/rodapé em `(117,837,150,37)`, `(126,843,774,41)` e `(960,880,369,20)`; conferir clipping no limite inferior.
- Verificar os deltas residuais em `(110,442,816,39)`, `(778,321,118,35)` e `(540,364,126,30)`. Preservar componentes e tokens existentes; não redesenhar a tela inteira.

### investments — PASS visual, manter sob observação

Score 90,70; cobertura 91,28%; 14 issues P3; nenhum P0/P1. Os menores sinais são content/density 73,78, assets 83,89 e spacing/grid 80,13.

Causa provável: diferenças pequenas de densidade/ocupação nos cabeçalhos, tabela e ilustração/área direita; a grade e as cores já estão próximas.

Correções precisas, somente se houver nova rodada: conferir o alinhamento dos títulos e filtros em `(87,140,284,38)`, `(463,139,151,39)`, `(602,139,105,39)`, `(372,142,93,36)`; ajustar as linhas/tabela em `(85,258,1105,44)`, `(97,265,1263,41)`, `(84,323,332,136)`, `(418,324,32,134)`, `(161,375,131,38)`, `(525,375,137,38)`, `(766,375,137,38)`; e validar o painel direito `(1058,343,142,96)` e rodapé `(748,797,100,19)`. Não alterar componentes compartilhados sem confirmar impacto no dashboard/imports.

### imports — FAIL

Score 88,15; cobertura 91,18%; 11 issues P1. O maior sinal é assets 61,90, seguido de content/density 76,96 e spacing/grid 79,33; geometry 99,80, typography 99,17 e color 90,58 estão adequados.

Causa provável: o dropzone/área de importação e seus elementos auxiliares não reproduzem a mesma quantidade/área de componentes da fonte; há também desalinhamento no cabeçalho e no bloco de ajuda/ações.

Correções precisas:

- Recriar o bloco de ação/rodapé em `(x=125,y=603,w=762,h=49)` e `(141,616,103,25)`, preservando altura, borda, raio, ícone e espaçamento interno.
- Ajustar cabeçalho/controles em `(425,139,182,50)`, `(231,142,128,36)`, `(360,139,62,39)` e `(88,141,86,37)` para coincidir com a posição e os pesos visuais da fonte.
- Corrigir o texto/bloco explicativo em `(131,198,170,41)` e `(152,251,206,18)`; conferir line-height, largura de coluna e margem superior.
- Ajustar as linhas auxiliares em `(180,560,237,14)`, `(226,582,212,14)` e `(969,588,178,17)`. Reutilizar assets/componentes reais (não placeholders) e verificar que todos os elementos do dropzone estão presentes.

### assistant — PASS visual, manter sob observação

Score 93,99; cobertura 94,68%; 3 issues P3. O score é estável; assets 95,55, typography 99,39 e geometry 99,80 estão fortes.

Causa provável: diferenças locais de mensagem/controle e uma linha fina no painel, sem evidência de problema estrutural amplo.

Correções precisas, opcionais após resolver as telas FAIL: conferir o componente em `(550,711,198,44)`, o controle em `(816,314,158,22)` e a linha em `(804,621,532,4)`; ajustar apenas padding, cor/espessura e baseline conforme o side-by-side. Não fazer refatoração ampla.

## Próximo passo

Aplicar exclusivamente as correções acima em uma rodada Luna, preservar `score.json`/`issues.json` já gravados e executar novamente o avaliador completo como cycle 2. O gate só pode mudar após score ≥90, cobertura ≥80% e zero P0/P1 por tela; se o orçamento terminar sem isso, manter `NEEDS_REVIEW` e registrar os deltas restantes.
