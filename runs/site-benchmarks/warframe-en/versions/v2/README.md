# Warframe EN — benchmark version 2

Reconstrução editável da home de `https://www.warframe.com/en` no projeto
Penpot **Penpot Benchmarks**, arquivo **Site Benchmarks**, página
`Benchmark — Warframe EN v2`.

## Estado terminal

**NEEDS_REVIEW.** O usuário aprovou explicitamente o limite dinâmico
`1440×5837`, mantendo a largura excedente como overflow horizontal acidental.
O revisor principal pontuou os três ciclos permitidos:

| Ciclo | Score | Cobertura | Resultado |
|---|---:|---:|---|
| 1 | 78,94 | 66,1622% | Reprovado |
| 2 | 71,94 | 65,6995% | Reprovado com regressão |
| 3 | 83,34 | 60,7192% | Reprovado; terminal |

O ciclo 3 corrigiu o posicionamento local de filhos em boards aninhados e fez
todas as seções aparecerem no export full-page. Ainda assim, cobertura,
espaçamento, densidade, assets e fidelidade semântica ficaram abaixo dos gates.
Não existe quarto ciclo.

## Conteúdo

- `source/`: mapa sanitizado, frame-spec aprovado e evidências da captura;
- `assets/`: inventário de assets first-party;
- `planning/`: plano de seções, perguntas e decisões;
- `design/`: exports editáveis, inventário estrutural e logs MCP;
- `cycles/`: evidência imutável do avaliador para os três ciclos;
- `review-cycle-N.md`: revisão e decisão do agente principal;
- `delivery/`: pacote terminal e referências Penpot.

As imagens públicas de side-by-side, overlay e heatmap ficam em
`../../analysis/v2-cycle-N-*`.
