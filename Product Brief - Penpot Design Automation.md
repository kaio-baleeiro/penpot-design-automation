---
type: product-brief
status: approved
created: 2026-09-14
updated: 2026-09-18
source_agent: codex
agent_context: codex-desktop
project: Penpot Design Automation
confidence: high
review: false
---

# Product Brief - Penpot Design Automation

## Opportunity

Transformar referências visuais e briefings em telas editáveis no Penpot sem
perder contexto, decisões ou evidências de fidelidade.

## Target User

O proprietário do vault, em trabalhos pessoais de produto e desenvolvimento.

## Current Pain

A criação manual é lenta; referências vindas de sites, screenshots e código são
fáceis de perder; revisões visuais sem métricas produzem correções vagas.

## Proposed Solution

Um workflow de duas rotas:

- **Reprodução:** mapeia URL, screenshots e/ou código, constrói no Penpot e mede
  fidelidade contra cada fonte e viewport aprovado.
- **Criação dirigida:** transforma prompt em briefing aprovado, itera versões com
  feedback humano e, após aprovação, formaliza o design system sem alterar a
  aparência aceita.

## Scope

- Perguntas obrigatórias e fechamento obrigatório para adendos.
- Registro persistente da fonte, decisões e feedbacks.
- Construção de telas estáticas, componentes, tokens e design system.
- Operações manuais executadas por Luna; métricas calculadas por scripts.
- Comparação lado a lado anotada, overlay, heatmap e relatório de issues.
- Aprovação por tela e viewport, sem médias que escondam falhas.

## Constraints

- Penpot acessível somente no host local.
- Segredos, cookies e material privado não entram no Git.
- Capturas grandes ou privadas permanecem em armazenamento local ignorado.
- Score mínimo de 90%, cobertura mínima de 80% e ausência de P0/P1.
- Até três ciclos internos de correção por versão.

## Next Decision

Manter Apple BR, GitHub Kaio e Warframe EN como benchmarks públicos oficiais.

## Links

- [[P - Penpot Design Automation]]
- [[Technical Spec - Penpot Design Automation]]
