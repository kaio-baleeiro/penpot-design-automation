# Perfis de agentes do workflow Penpot

Este diretório contém os perfis portáveis que executam o workflow de
prototipação. Eles são instruções em Markdown, acompanhadas por um manifesto
pequeno e contratos de handoff; por isso podem ser usados por Codex CLI, Devin
CLI, Claude Code, Gemini, Cursor ou outro agente que leia `AGENTS.md`.

## Perfis disponíveis

| Perfil | Fase | Responsabilidade principal |
|---|---|---|
| `intake-source-analyst` | intake/source-map | Capturar a origem inteira, estados, viewports e procedência |
| `frontend-forensics-engineer` | source-map/build-plan | Ler DOM/CSS/código, medir geometria e descobrir responsividade |
| `ux-ia-responsive-designer` | build-plan | Transformar evidência em hierarquia, fluxo estático e matriz responsiva |
| `visual-ui-designer` | build-plan/build | Extrair linguagem visual, conteúdo, tipografia, assets e regras de composição |
| `penpot-mcp-prototyper` | build/refinement | Construir frames editáveis e componentes no Penpot via MCP |
| `design-system-architect` | design-system | Formalizar tokens, estilos, variantes e instâncias reutilizáveis |
| `visual-qa-auditor` | validate/delivery | Coletar diffs, verificar estrutura e apontar correções por região |

Os perfis declaram `model_class: cost-efficient` e não fixam fornecedor. O
arquivo `runtime-policy.yaml` resolve esse papel para cada host: Luna no Codex,
Haiku no Claude Code, o router econômico no Devin CLI e Flash no Gemini CLI.
O agente principal continua sendo o revisor final: executa/confere o avaliador
determinístico, aplica os gates 90/80/P0-P1 e decide o estado. Um perfil não
pode alterar score, limiares ou evidência imutável.

## Como invocar em qualquer CLI

1. Leia `AGENTS.md` na raiz e `skills/penpot-design/SKILL.md`.
2. Escolha o perfil pelo manifesto `manifest.yaml`. Use o adaptador nativo em
   `.claude/agents/`, `.devin/agents/` ou `.gemini/agents/`; em outro host,
   leia o `AGENT.md` canônico.
3. Passe ao perfil os caminhos do run e o contrato
   [`contracts/handoff.md`](contracts/handoff.md).
4. O perfil grava apenas os artefatos da sua fase e devolve um handoff
   versionado. O próximo perfil só inicia quando os campos obrigatórios estão
   presentes.

Não é necessário instalar um runtime proprietário: o host deve fornecer
Playwright quando houver URL/app, o cliente MCP configurado quando houver
construção no Penpot e Python 3 para os scripts do repositório.

Os adaptadores são gerados por `scripts/sync_agent_adapters.py`. Edite apenas o
perfil canônico e rode o gerador; `--check` valida que os 21 wrappers estão em
sincronia.

## Pipeline

```text
intake-source-analyst
        ↓
frontend-forensics-engineer ──┐
        ↓                      ├─ ux-ia-responsive-designer
visual-ui-designer ───────────┘
        ↓
penpot-mcp-prototyper → visual-qa-auditor ──(até 3 ciclos)──┐
        ↓                                                     │
design-system-architect → visual-qa-auditor → entrega        │
        └────────────────────── correção precisa ─────────────┘
```

O perfil de QA nunca “aprova por aparência”. Ele combina comparação visual,
conteúdo/proveniência, estrutura editável e acessibilidade; um score alto não
compensa uma falha estrutural.

## Base de conhecimento

As fontes pesquisadas, a data da pesquisa e a regra que cada uma adiciona ao
workflow estão em [`research/README.md`](research/README.md). O material é
curado para este projeto, não um convite a buscar referências externas durante
uma execução.
