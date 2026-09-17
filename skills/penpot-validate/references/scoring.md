# Score e gates da validação Penpot

O score oficial é produzido por
`scripts/validate.sh --run-dir <run-dir> --cycle <1..3>`;
não substitua seu resultado por avaliação subjetiva do agente. A tabela
versionada `penpot-visual-v2`, implementada em
pelo runtime versionado do projeto, usa estes pesos:

| Dimensão | Peso |
|---|---:|
| Geometria e alinhamento | 25 |
| Espaçamento e grid | 15 |
| Tipografia | 15 |
| Cor, borda e sombra | 15 |
| Conteúdo e densidade | 15 |
| Imagens, ícones e assets | 15 |
| **Total** | **100** |

Cada dimensão é uma heurística determinística de imagem, limitada a `0..100`.
A v2 divide a página em regiões de 240 px, pondera conteúdo e bordas em cada
região e aplica uma penalidade pelo quintil inferior. Isso impede que grandes
fundos brancos escondam diferenças locais em páginas longas ou esparsas. O
score final soma as contribuições `dimensão_score * peso / 100`, limita o
resultado pelo score regional calibrado e arredonda a duas casas. O relatório preserva a versão da tabela e a
explicação/evidência de cada métrica. As limitações (sem prova de semântica,
família tipográfica, procedência de asset ou editabilidade Penpot) devem ser
mantidas no relatório.

## Revisão semântica e de provenance

As métricas acima são heurísticas de pixels e podem produzir falso positivo em
layouts claros ou repetitivos. Elas não aprovam conteúdo. O revisor deve
executar um gate separado, comparando copy, rota/estado, ordem/hierarquia,
logos, imagens, ícones, fontes e `asset_refs` com a fonte mapeada. Divergências
ou conteúdo inventado mantêm `NEEDS_REVIEW`, mesmo com score e coverage acima
dos limiares. Esse gate não altera a fórmula determinística.

`coverage` é um gate independente: a fração de pixels cujo maior delta de
canal é `<= 32`, emitida no intervalo `0..1`. As similaridades pixel/exata
também são registradas como evidência auxiliar. O avaliador redimensiona o
export para as dimensões da fonte para calcular as métricas; dimensões originais
diferentes ainda produzem issue P0. O gate por tela/viewport é:

```text
PASS = score >= 90 AND coverage >= 0.80 AND count(P0,P1) == 0
```

Os limiares imutáveis no código são `MIN_SCORE = 90.0`,
`MIN_COVERAGE = 0.80` e `MAX_CYCLES = 3`. Severidade determinística: P0 para
dimensões diferentes, área de diferença `>= 40%` ou score `< 60`; P1 para área
`>= 20%` ou score `< 90`; P2 para área `>= 2%`; caso contrário P3. Uma queda
maior que 2 pontos em relação ao ciclo anterior gera P1 de regressão. O
avaliador grava cada ciclo de forma exclusiva em `cycles/cycle-N/`, impedindo
que um agente sobrescreva score ou issues já produzidos.
Quando um ciclo anterior falhou, o próximo ciclo é recusado se o hash do export
Penpot continuar idêntico. Revalidar o mesmo PNG não é refatorar e não consome
uma das três tentativas.

Um agregado geral nunca mascara uma tela que falhou. Se não houver fonte visual
na rota de criação dirigida, o mesmo score mede aderência ao briefing aprovado e
à versão de referência aceita; a aprovação estética continua sendo manual.

## Evidência visual

Para cada tela/viewport aprovado ou reprovado, o CLI gera:

- `<screen>-side-by-side-annotated.png`: fonte à esquerda e render Penpot à
  direita, com regiões de diferença marcadas;
- `<screen>-overlay.png`: sobreposição da fonte e do export;
- `<screen>-heatmap.png`: magnitude espacial das diferenças;
- `<screen>-detail-board.png`: fonte, export e heatmap lado a lado em fatias
  verticais legíveis, inclusive para páginas muito longas;
- `issues.json` e seção no relatório com região, diferença, causa e correção.

Se uma imagem não puder ser comparada com segurança (escala desconhecida,
conteúdo dinâmico ou fonte incompleta), marque a métrica como indisponível,
reduza a confiança e encaminhe uma pergunta; não converta ausência em zero ou
em aprovação.

## Gate estrutural

Na etapa `DS_REVALIDATING`, o CLI também exige `--inventory <json>`. O arquivo
precisa inventariar tokens, componentes, instâncias, estilos, instâncias
requeridas e cópias destacadas. Tokens, componentes, instâncias e estilos
vazios reprovam; qualquer instância destacada reprova. O score visual não pode
compensar falha estrutural e `READY_FOR_DELIVERY` só é derivado depois das
aprovações formais.
