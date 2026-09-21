---
type: handoff
status: complete
created: 2026-09-14
updated: 2026-09-21
source_agent: codex
agent_context: codex-desktop
project: Penpot Design Automation
from: Codex
to: proprietário do workspace
confidence: high
review: false
---

# Handoff - Penpot Design Automation

## Estado atual

O Penpot compartilhado está saudável em `http://localhost:9001`, com
Mailcatcher em `http://localhost:1080`. A composição `penpot-design-automation`
possui sete serviços e reutiliza os volumes históricos externos. A migração
preservou 1 perfil, 3 times, 5 projetos, 2 arquivos e 51 assets.

O repositório público é
`https://github.com/kaio-baleeiro/penpot-design-automation`. A skill global
`~/.agents/skills/penpot-design` é um vínculo para a implementação
canônica deste projeto. O MCP local está registrado como `penpot-design`; sua
URL autenticada permanece somente na configuração local ignorada.

## Operação

```sh
infra/penpot/scripts/up.sh
infra/penpot/scripts/healthcheck.sh
infra/penpot/scripts/backup.sh
infra/penpot/scripts/down.sh
```

Novos pedidos começam com `$penpot-design`. A skill resolve as perguntas de
intake/adendo, escolhe reprodução ou criação dirigida, delega tarefas manuais ao
worker econômico configurado para o runtime, registra fontes e conduz construção,
score, correção, aprovação, formalização do design system e entrega. Os perfis
canônicos são compartilhados; Codex, Claude Code, Devin CLI e Gemini CLI usam
adaptadores nativos sincronizados a partir deles.

As sete skills estão empacotadas no formato Agent Skills. Contratos extensos,
wrappers e configuração ficam respectivamente em `references/`, `scripts/` e
`assets/` dentro da skill proprietária. O validador rejeita caminhos externos,
recursos quebrados, diretórios opcionais vazios e scripts não executáveis.

Na reprodução, a origem é também a biblioteca prioritária de assets: site,
runtime e código podem ser inspecionados para reutilizar SVGs, imagens, ícones,
logos e fontes exatos. O inventário registra procedência e substituições
externas só entram após uma decisão explícita.

O dimensionamento também distingue viewport e frame. Desktop parte de
`1440x900`, mas o frame acompanha a altura finita medida. Largura adicional só
é usada quando a página raiz possui experiência horizontal intencional;
overflow acidental ou de containers não alarga o frame. Conteúdo instável ou
infinito exige um limite reproduzível confirmado pelo usuário.

## Validação concluída

- 75 testes unitários/integrados aprovados.
- 7 skills aprovadas no validador oficial e no validador local.
- Compose, scripts, instalador, healthcheck, MCP, export e inventário validados.
- Backups pré e pós-migração com checksums válidos.
- Adaptadores nativos dos sete perfis validados para Codex, Claude Code, Devin
  CLI e Gemini CLI; o worker concreto continua sendo registrado por execução.
- Cada skill possui `lessons-learned/`; o índice transversal do orquestrador
  compartilha regras entre fases e cinco falhas do desenvolvimento foram
  convertidas em regras mitigadas com evidência.
- Auditoria Luna específica de dimensionamento incorporada ao gate executável.
- Os benchmarks públicos oficiais são Apple BR, GitHub Kaio e Warframe EN v4.
  Todos preservam três ciclos e artefatos visuais; a escolha canônica do usuário
  não altera o gate automático `NEEDS_REVIEW`.

## Manutenção

Uma instalação migrada pode manter nomes locais de volumes. A tarefa
[[Task - Renomear volumes legados do Penpot]] registra o procedimento futuro;
não remover os volumes atuais antes de backup, restore isolado e aceite.

## Links

- [Lições executáveis no repositório](https://github.com/kaio-baleeiro/penpot-design-automation/tree/main/skills)

- [[P - Penpot Design Automation]]
- [[Technical Spec - Penpot Design Automation]]
- [[Implementation Plan - Penpot Design Automation]]
- [[35-Lessons-Learned/Projects/penpot-design-automation/README|Lições aprendidas do projeto]]
