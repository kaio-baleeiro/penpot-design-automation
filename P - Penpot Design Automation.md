---
type: project
status: active
created: 2026-09-14
updated: 2026-09-14
source_agent: codex
agent_context: codex-desktop
confidence: high
review: false
workspace: /Users/baleeiro/AI-Second-Brain/02-Projects/P - Penpot Design Automation
repository: https://github.com/kaio-baleeiro/penpot-design-automation
next: Usar $penpot-design em um novo pedido e planejar a renomeação futura dos volumes
---

# P - Penpot Design Automation

## Objetivo

Manter uma instância local e compartilhada do Penpot e um workflow versionado
capaz de criar telas a partir de URL, screenshot, código ou briefing sem fonte,
com construção via MCP, rastreabilidade da origem, validação visual determinística
e correções executadas por trabalhadores `gpt-5.6-luna`.

## Critério de conclusão

- [x] Infraestrutura do Penpot migrada do KatiauInvest sem perda de dados.
- [x] Repositório privado criado e publicado no GitHub.
- [x] Skill global instalada a partir da implementação versionada no projeto.
- [x] Rotas de reprodução e criação dirigida implementadas.
- [x] Validação por tela e viewport exige score mínimo de 90%, cobertura de 80%
  e ausência de problemas P0/P1.
- [x] Comparação lado a lado, overlay, heatmap e issues localizadas gerados.
- [x] Ciclo de correção limitado a três tentativas por versão.
- [x] Workflow testado de ponta a ponta com o KatiauInvest.

## Decisões

- 2026-09-14: o workspace e repositório pertencem ao vault, em `02-Projects`.
- 2026-09-14: a instância permanece local em `localhost` e atende projetos futuros.
- 2026-09-14: os volumes legados serão reutilizados como externos nesta migração.
- 2026-09-14: os times e projetos existentes serão preservados; novos trabalhos
  usarão o time geral `Design Studio`.
- 2026-09-14: skills e scripts canônicos vivem neste repositório; uma skill global
  fina aponta para o orquestrador versionado.
- 2026-09-14: trabalho operacional delegado usa `gpt-5.6-luna`; indisponibilidade
  do modelo interrompe o fluxo em vez de escolher silenciosamente outro modelo.
- 2026-09-14: toda execução começa com perguntas, encerra a descoberta perguntando
  por adendos ou mudanças e reavalia ambiguidades antes de construir.
- 2026-09-14: divergências entre fontes exigem decisão do usuário.
- 2026-09-14: o modo sem fonte usa briefing aprovado como referência objetiva e
  também exige aprovação estética explícita do usuário.
- 2026-09-14: rodadas de feedback do usuário são ilimitadas; cada versão admite
  no máximo três ciclos internos de correção.
- 2026-09-14: a migração preservou 1 perfil, 3 times, 5 projetos, 2 arquivos e
  51 assets; backups anterior e posterior passaram nos checksums.
- 2026-09-14: o benchmark KatiauInvest encerrou corretamente em `NEEDS_REVIEW`
  após três ciclos porque dashboard e imports ficaram abaixo do gate por tela,
  mesmo com score agregado 90,31.

## Links

- [[Product Brief - Penpot Design Automation]]
- [[Technical Spec - Penpot Design Automation]]
- [[Implementation Plan - Penpot Design Automation]]
- [[Task - Renomear volumes legados do Penpot]]
- [[Handoff - Penpot Design Automation]]
- [[P - KatiauInvest]]
- [[_Project Index|Índice de projetos]]
