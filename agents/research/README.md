# Base de conhecimento pesquisada

Pesquisa realizada em 16/09/2026. As referências abaixo foram escolhidas por
serem documentação primária, padrão normativo ou material do próprio Penpot.
Cada item vira uma regra operacional nos perfis; a execução não deve fazer
busca web não relacionada à origem fornecida pelo usuário.

## Portabilidade entre agentes — revisão de 21/09/2026

- [Agent Skills specification](https://agentskills.io/specification): o núcleo
  portável é `SKILL.md` com recursos relativos; `agents/openai.yaml` é metadata
  opcional de um cliente. Regra: o validador não pode exigir metadata OpenAI.
- [Claude Code custom subagents](https://code.claude.com/docs/en/sub-agents):
  perfis de projeto vivem em `.claude/agents/` e podem escolher um modelo
  econômico. Regra: gerar wrappers finos que apontam ao perfil canônico.
- [Gemini CLI project context](https://geminicli.com/docs/cli/gemini-md/) e
  [subagents](https://geminicli.com/docs/core/subagents/): `GEMINI.md` carrega
  o contrato e `.gemini/agents/` registra workers. Regra: manter o mesmo nome e
  descrição dos perfis canônicos.
- [Devin CLI rules and AGENTS.md](https://docs.devin.ai/cli/extensibility/rules)
  e [subagents](https://docs.devin.ai/cli/subagents): Devin lê `AGENTS.md` e
  perfis em `.devin/agents/`; o router padrão de subagentes é econômico. Regra:
  não exigir um modelo de outro fornecedor.

Essas fontes sustentam a separação entre contrato funcional, perfil canônico e
adaptador do runtime. O manifesto registra o runtime e o modelo resolvidos para
que economia, auditoria e reprodução não dependam de inferência posterior.

## Penpot e design systems

- [Components — Penpot User Guide](https://help.penpot.app/user-guide/design-systems/components/): componente principal é a fonte de verdade e instâncias herdam mudanças. Regra: prototipar componentes reais e verificar instâncias, não apenas nomes de camadas.
- [Design Systems — Penpot User Guide](https://help.penpot.app/user-guide/design-systems/): bibliotecas, assets, variantes e tokens formam o sistema. Regra: a tela passa por uma fase explícita de componentização após aprovação.
- [Design Tokens — Penpot User Guide](https://help.penpot.app/user-guide/design-systems/design-tokens/): tokens cobrem cor, tipografia, espaçamento, sombra e aderem ao formato W3C DTCG. Regra: separar tokens base, semânticos e de componente e exportar JSON.
- [Developer’s guide to design tokens and CSS variables — Penpot](https://penpot.app/blog/the-developers-guide-to-design-tokens-and-css-variables/): conjuntos têm cascata/prioridade e aliases permitem temas. Regra: o perfil de DS registra sets, aliases e modo, em vez de repetir valores hexadecimais.

## Responsividade e implementação

- [Responsive web design — MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/CSS_layout/Responsive_Design): grids fluidos, imagens limitadas ao container e breakpoints orientados ao conteúdo. Regra: mapear comportamento por breakpoint, sem presumir que 1440×900 seja a altura final.
- [CSS container queries — MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries): componentes podem responder ao tamanho do container, não só ao viewport. Regra: o forense de frontend procura queries de container e registra o contexto de cada componente.
- [HTML: a good basis for accessibility — MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML): semântica, ordem de fonte, labels e controles nativos melhoram acessibilidade e responsividade. Regra: extrair semântica do código e preservar hierarquia no plano Penpot.

## Acessibilidade e UX

- [WCAG 2.2 — W3C Recommendation](https://www.w3.org/TR/WCAG22/): critérios testáveis organizados nos princípios perceivable, operable, understandable e robust. Regra: revisar contraste, foco, tamanho de alvo, reflow, texto alternativo e ordem de leitura no handoff.
- [10 Usability Heuristics — Nielsen Norman Group](https://www.nngroup.com/articles/ten-usability-heuristics/): avaliação heurística de visibilidade do estado, consistência, prevenção de erros e reconhecimento. Regra: o perfil UX registra riscos de compreensão mesmo em telas estáticas.

## Captura e validação

- [Full-page screenshots — Playwright MCP](https://playwright.dev/mcp/tools/screenshots): `fullPage: true` captura conteúdo abaixo da dobra; screenshot e accessibility snapshot respondem a perguntas diferentes. Regra: guardar viewport e full-page separados e mapear seções inteiras.
- [Visual comparisons — Playwright](https://playwright.dev/docs/next/test-snapshots): screenshots precisam de ambiente determinístico, esperam dois frames estáveis e produzem diff revisável. Regra: congelar estado dinâmico e não comparar capturas de ambientes diferentes.
- [Accessibility testing — Playwright](https://playwright.dev/docs/accessibility-testing): axe encontra problemas comuns, mas não substitui avaliação manual. Regra: QA combina teste automatizado com revisão de conteúdo, semântica e uso.
- [Image quality assessment: from error visibility to structural similarity — Wang et al.](https://ece.uwaterloo.ca/~z70wang/publications/ssim.pdf): erro médio por pixel não representa sozinho a estrutura percebida. Regra: combinar evidência de pixels, bordas, ocupação e regiões; nunca deixar o fundo global compensar uma seção incorreta.
- [Penpot Plugin API](https://doc.plugins.penpot.app/interfaces/Penpot): a API oficial expõe upload de mídia, criação de shapes e bibliotecas/componentes. Regra: registrar upload e identidade do asset, e construir componentes reais em vez de simular reutilização pelo nome da camada.

## Como isso muda o benchmark

Os ciclos anteriores evidenciaram três falhas: densidade/cores e tipografia
subestimadas na Apple; assets e espaçamento ausentes no Warframe; e score alto
no GitHub sem inventário estrutural preenchido. Os perfis agora exigem:

1. inventário de assets antes do plano;
2. contrato de layout medido a partir de DOM/CSS quando houver código;
3. mapa de conteúdo e seções com cobertura full-page;
4. reconstrução editável com inventário estrutural obrigatório;
5. QA separado em pixel, conteúdo/proveniência, acessibilidade e estrutura.

A auditoria seguinte acrescentou duas proteções: score regional com penalidade
para o quintil mais fraco e rejeição de um novo ciclo quando o export reprovado
não mudou. Os relatórios full-page também incluem um painel de detalhes em
fatias, porque uma imagem de 2880×5000 reduzida no README não é evidência útil.
