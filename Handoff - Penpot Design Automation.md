---
type: handoff
status: complete
created: 2026-09-14
updated: 2026-09-14
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

O repositório privado é
`https://github.com/kaio-baleeiro/penpot-design-automation`. A skill global
`/Users/baleeiro/.agents/skills/penpot-design` é um vínculo para a implementação
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
intake/adendo, escolhe reprodução ou criação dirigida, delega tarefas manuais a
`gpt-5.6-luna`, registra fontes e conduz construção, score, correção, aprovação,
formalização do design system e entrega.

As sete skills estão empacotadas no formato Agent Skills. Contratos extensos,
wrappers e configuração ficam respectivamente em `references/`, `scripts/` e
`assets/` dentro da skill proprietária. O validador rejeita caminhos externos,
recursos quebrados, diretórios opcionais vazios e scripts não executáveis.

## Validação concluída

- 31 testes unitários/integrados aprovados.
- 7 skills aprovadas no validador oficial e no validador local.
- Compose, scripts, instalador, healthcheck, MCP, export e inventário validados.
- Backups pré e pós-migração com checksums válidos.
- Forward test independente Luna aprovado após correções.
- Espaço de lições aprendidas criado e quatro falhas do desenvolvimento convertidas
  em regras mitigadas com evidência.
- KatiauInvest: score agregado 90,31; dashboard 88,42, investimentos 90,70,
  importação 88,15 e assistente 93,99. O limite de três ciclos encerrou em
  `NEEDS_REVIEW`, sem permitir que a média escondesse falhas individuais.

## Manutenção

Os volumes ainda têm nomes `katiauinvest-penpot_*`. A tarefa
[[Task - Renomear volumes legados do Penpot]] registra o procedimento futuro;
não remover os volumes atuais antes de backup, restore isolado e aceite.

## Links

- [[P - Penpot Design Automation]]
- [[Technical Spec - Penpot Design Automation]]
- [[Implementation Plan - Penpot Design Automation]]
- [[35-Lessons-Learned/Projects/penpot-design-automation/README|Lições aprendidas do projeto]]
- [[P - KatiauInvest]]
