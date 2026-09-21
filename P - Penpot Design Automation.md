---
type: project
status: active
created: 2026-09-14
updated: 2026-09-21
source_agent: codex
agent_context: codex-desktop
confidence: high
review: false
workspace: .
repository: https://github.com/kaio-baleeiro/penpot-design-automation
next: Usar $penpot-design em um novo pedido e planejar a renomeação futura dos volumes
---

# P - Penpot Design Automation

## Objetivo

Manter uma instância local e compartilhada do Penpot e um workflow versionado
capaz de criar telas a partir de URL, screenshot, código ou briefing sem fonte,
com construção via MCP, rastreabilidade da origem, validação visual determinística
e correções executadas por trabalhadores econômicos selecionados pelo runtime.

## Critério de conclusão

- [x] Infraestrutura do Penpot migrada de uma instalação local sem perda de dados.
- [x] Repositório público criado e publicado no GitHub.
- [x] Skill global instalada a partir da implementação versionada no projeto.
- [x] Rotas de reprodução e criação dirigida implementadas.
- [x] Validação por tela e viewport exige score mínimo de 90%, cobertura de 80%
  e ausência de problemas P0/P1.
- [x] Comparação lado a lado, overlay, heatmap e issues localizadas gerados.
- [x] Ciclo de correção limitado a três tentativas por versão.
- [x] Workflow testado de ponta a ponta com benchmarks públicos.
- [x] As sete skills seguem o formato Agent Skills com recursos locais e
  validação estrutural automatizada.
- [x] Lições aprendidas versionadas dentro de cada skill, com índice transversal,
  registro, contramedida e verificação obrigatórios.
- [x] Dimensionamento inteligente diferencia viewport e frame, mede páginas
  longas e bloqueia overflow horizontal sem intenção comprovada.

## Decisões

- 2026-09-14: o workspace e repositório pertencem ao vault, em `02-Projects`.
- 2026-09-14: a instância permanece local em `localhost` e atende projetos futuros.
- 2026-09-14: os volumes legados serão reutilizados como externos nesta migração.
- 2026-09-14: os times e projetos existentes serão preservados; novos trabalhos
  usarão o time geral `Design Studio`.
- 2026-09-14: skills e scripts canônicos vivem neste repositório; uma skill global
  fina aponta para o orquestrador versionado.
- 2026-09-21: os perfis canônicos são neutros de fornecedor; cada runtime resolve
  seu trabalhador econômico por `agents/runtime-policy.yaml`, registra runtime e
  modelo concretos e interrompe o fluxo se a delegação exigida estiver indisponível.
- 2026-09-14: toda execução começa com perguntas, encerra a descoberta perguntando
  por adendos ou mudanças e reavalia ambiguidades antes de construir.
- 2026-09-14: divergências entre fontes exigem decisão do usuário.
- 2026-09-14: o modo sem fonte usa briefing aprovado como referência objetiva e
  também exige aprovação estética explícita do usuário.
- 2026-09-14: rodadas de feedback do usuário são ilimitadas; cada versão admite
  no máximo três ciclos internos de correção.
- 2026-09-14: a migração preservou 1 perfil, 3 times, 5 projetos, 2 arquivos e
  51 assets; backups anterior e posterior passaram nos checksums.
- 2026-09-17: Apple BR, GitHub Kaio e Warframe EN v4 foram escolhidos pelo
  usuário como baselines canônicas; os gates automáticos permanecem
  `NEEDS_REVIEW` e não foram reescritos.
- 2026-09-14: cada skill referencia somente recursos diretos da própria pasta;
  o runtime compartilhado permanece único e é acessado por wrappers locais.
- 2026-09-14: lições operacionais vivem em `skills/<skill>/lessons-learned/`;
  `penpot-design/lessons-learned/` mantém o índice transversal, runs guardam
  referências relativas em `lesson_refs` e só marcam uma lição como mitigada
  após verificação.
- 2026-09-14: sites/runtimes e repositórios fornecidos são fontes autorizadas de
  SVGs, imagens, ícones, logos, fontes e outros assets úteis; o workflow deve
  inventariar e reutilizar os originais antes de buscar substitutos externos.
- 2026-09-14: o repositório foi tornado público por solicitação explícita do
  usuário.
- 2026-09-14: `1440x900` é o viewport desktop de observação e o mínimo do frame,
  não seu limite final; altura acompanha conteúdo finito e largura só cresce com
  evidência de navegação horizontal intencional na página raiz.

## Links

- [Lições executáveis no repositório](https://github.com/kaio-baleeiro/penpot-design-automation/tree/main/skills)

- [[Product Brief - Penpot Design Automation]]
- [[Technical Spec - Penpot Design Automation]]
- [[Implementation Plan - Penpot Design Automation]]
- [[Task - Renomear volumes legados do Penpot]]
- [[Handoff - Penpot Design Automation]]
- [[35-Lessons-Learned/Projects/penpot-design-automation/README|Lições aprendidas do projeto]]
- [[LL - Penpot viewport is not the final frame extent]]
- [[_Project Index|Índice de projetos]]
