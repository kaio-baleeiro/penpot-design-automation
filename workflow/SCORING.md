# Score e gates

O score oficial é produzido por
`python3 -m scripts.penpot_validation validate --run-dir <run-dir> --cycle <1..3>`;
não substitua seu resultado por avaliação subjetiva do agente. A tabela
versionada `penpot-visual-v1`, implementada em
`scripts/penpot_validation/metrics.py`, usa estes pesos:

| Dimensão | Peso |
|---|---:|
| Geometria e alinhamento | 30 |
| Espaçamento e grid | 20 |
| Tipografia | 15 |
| Cor, borda e sombra | 15 |
| Conteúdo e densidade | 10 |
| Imagens, ícones e assets | 10 |
| **Total** | **100** |

Cada dimensão é uma heurística determinística de imagem, limitada a `0..100`;
o score final é a soma das contribuições `dimensão_score * peso / 100`,
arredondada a duas casas. O relatório preserva a versão da tabela e a
explicação/evidência de cada métrica. As limitações (sem prova de semântica,
família tipográfica, procedência de asset ou editabilidade Penpot) devem ser
mantidas no relatório.

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

Um agregado geral nunca mascara uma tela que falhou. Se não houver fonte visual
na rota de criação dirigida, o mesmo score mede aderência ao briefing aprovado e
à versão de referência aceita; a aprovação estética continua sendo manual.

## Evidência visual

Para cada tela/viewport aprovado ou reprovado, o CLI gera:

- `<screen>-side-by-side-annotated.png`: fonte à esquerda e render Penpot à
  direita, com regiões de diferença marcadas;
- `<screen>-overlay.png`: sobreposição da fonte e do export;
- `<screen>-heatmap.png`: magnitude espacial das diferenças;
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
