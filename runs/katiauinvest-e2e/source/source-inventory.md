---
type: source-inventory
status: complete
created: 2026-09-14
updated: 2026-09-14
source_agent: codex
agent_context: codex-desktop
confidence: high
review: false
---

# Inventário de fontes — KatiauInvest E2E

| ID | Tipo | Localização sanitizada | Papel | Cobertura |
|---|---|---|---|---|
| `katiau-app-local` | URL autenticada local | `http://127.0.0.1:3100` | referência visual primária | quatro rotas desktop |
| `katiau-code` | diretório de código | repositório local externo `KatiauInvest` | estrutura e evidência complementar | aplicação atual |
| `katiau-penpot` | arquivo Penpot local | arquivo `Novo arquivo 1`, ID registrado no manifesto | candidato avaliado | quatro boards 1440×900 |

## Rotas e correspondência

| Tela | Rota fonte | Página/board Penpot |
|---|---|---|
| `dashboard` | `/` | `Page 1` / `74a25ccb-fd56-8020-8008-9b84a334d936` |
| `investments` | `/investments` | `D0 — Investimentos` / `74a25ccb-fd56-8020-8008-9b866c03c249` |
| `imports` | `/imports` | `D0 — Importação` / `5f6b4633-d59e-807c-8008-9c218ed4bc28` |
| `assistant` | `/assistant` | `D0 — Assistente IA` / `5f6b4633-d59e-807c-8008-9c21eadf671d` |

## Limitações

- O ensaio cobre somente desktop 1440×900 porque o arquivo Penpot preservado
  não contém boards mobile equivalentes.
- Estado de dados e textos dinâmicos pode variar; isso é evidência real de
  divergência e não é removido do score.
- Credenciais e materiais brutos não são versionados.
