# Base de conhecimento pesquisada

Pesquisa realizada em 16/09/2026. As referências abaixo foram escolhidas por
serem documentação primária, padrão normativo ou material do próprio Penpot.
Cada item vira uma regra operacional nos perfis; a execução não deve fazer
busca web não relacionada à origem fornecida pelo usuário.

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

## Como isso muda o benchmark

Os ciclos anteriores evidenciaram três falhas: densidade/cores e tipografia
subestimadas na Apple; assets e espaçamento ausentes no Warframe; e score alto
no GitHub sem inventário estrutural preenchido. Os perfis agora exigem:

1. inventário de assets antes do plano;
2. contrato de layout medido a partir de DOM/CSS quando houver código;
3. mapa de conteúdo e seções com cobertura full-page;
4. reconstrução editável com inventário estrutural obrigatório;
5. QA separado em pixel, conteúdo/proveniência, acessibilidade e estrutura.
