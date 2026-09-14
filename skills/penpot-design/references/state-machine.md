# Máquina de estados do workflow Penpot

Estados persistidos no manifesto da execução:

| Estado | Entrada | Saída mínima | Próximos estados |
|---|---|---|---|
| `INTAKE_PENDING` | pedido do usuário | perguntas, rota candidata | `INTAKE_REVIEW` |
| `INTAKE_REVIEW` | respostas iniciais | segunda pergunta obrigatória | `AMBIGUITY_ANALYSIS` |
| `AMBIGUITY_ANALYSIS` | adendo/mudança | decisões ou perguntas materiais | `SOURCE_CAPTURED` / `BRIEF_REFINEMENT` |
| `SOURCE_CAPTURED` | reprodução sem conflito | `source-map.json`, capturas, inventário | `BUILD_PLANNED` |
| `BRIEF_REFINEMENT` | criação dirigida | briefing versionado e aprovado | `BUILD_PLANNED` |
| `BUILD_PLANNED` | escopo resolvido | plano de telas/viewports | `BUILDING` |
| `BUILDING` | plano aprovado | arquivo/frames Penpot e log MCP | `VALIDATING` |
| `VALIDATING` | render exportado | score, coverage, diff e issues | `REFINEMENT` / `READY_FOR_USER_REVIEW` / `NEEDS_REVIEW` |
| `REFACTORING` | issues P0/P1 ou score < 90 | patch de correção | `VALIDATING` (até ciclo 3) |
| `REFINEMENT` | gate visual falhou antes do ciclo 3 | handoff de correção preciso | `BUILDING` / `VALIDATING` |
| `READY_FOR_USER_REVIEW` | gate visual passou | versão e evidências | `USER_REVIEW` |
| `USER_REVIEW` | criação dirigida | feedback versionado ou aprovação | `BUILDING` / `DS_FORMALIZATION` |
| `DS_FORMALIZATION` | aprovação formal | tokens/componentes e reconstrução | `DS_REVALIDATING` |
| `DS_REVALIDATING` | protótipo componentizado | score final, comparação e inventário estrutural | `REFINEMENT` / `READY_FOR_DELIVERY` / `NEEDS_REVIEW` |
| `READY_FOR_DELIVERY` | gates e aprovações passaram | pacote final | `DELIVERED` |
| `DELIVERED` | gates finais passados | pacote de entrega + relatório | terminal |
| `NEEDS_REVIEW` | ciclo 3 falhou ou gate final falhou | melhor versão + bloqueios explícitos | terminal |
| `BLOCKED_MODEL_UNAVAILABLE` | Luna indisponível | erro e retomada segura | terminal |

Regras de transição:

- `REFACTORING -> VALIDATING` incrementa `validation_cycle`; não exceder 3.
- `USER_REVIEW` pode repetir sem limite no modo `directed_creation`, mas uma
  construção nova inicia novamente sua validação interna em ciclo 1.
- `DELIVERED` só é permitido quando todos os viewports passam individualmente,
  design system estrutural está íntegro, o usuário aprovou e o relatório foi gerado.
- Falha de entrada, fonte inacessível ou MCP indisponível deve ser registrada
  como bloqueio, sem fabricar evidência.
