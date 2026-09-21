# Perfis especializados e integração

Os perfis portáveis vivem em [`agents/`](../../../agents/). Esta referência é o
contrato da skill: hosts diferentes podem ler os mesmos `AGENT.md`, mas não
podem pular as fases nem trocar o revisor final por um worker.

## Seleção por fase

| Fase | Perfil de worker | Handoff mínimo | Gate do orquestrador |
|---|---|---|---|
| Intake/captura | `intake-source-analyst` | perguntas, mapa, inventário, full-page e frame-spec | fonte preservada, limites e viewports resolvidos |
| Código/runtime | `frontend-forensics-engineer` | contrato DOM/CSS, semântica, breakpoints e assets | conflitos registrados e medidas ancoradas |
| Planejamento | `ux-ia-responsive-designer` + `visual-ui-designer` | IA, matriz responsiva, conteúdo e visual spec | cada seção tem evidência e regra de construção |
| Construção/correção | `penpot-mcp-prototyper` | log MCP, export full-page e inventário estrutural | composição editável; zero screenshot-only |
| Validação | `visual-qa-auditor` | score, coverage, issues, diffs e revisão semântica | score ≥90, coverage ≥80, zero P0/P1 e estrutura válida |
| Pós-aprovação | `design-system-architect` | tokens, estilos, componentes, instâncias e revalidação | aparência preservada e detached count zero |

Todos recebem `model_class: cost-efficient`. O host resolve o modelo em
`agents/runtime-policy.yaml` e deve interromper com
`BLOCKED_WORKER_UNAVAILABLE` se o worker não puder ser criado. O orquestrador é o
único responsável por chamar o avaliador, conferir a estrutura e decidir
`REFINEMENT`, `READY_FOR_USER_REVIEW`, `NEEDS_REVIEW` ou `DELIVERED`.

## Handoff como barreira de qualidade

Cada perfil escreve um handoff em `design/handoffs/` (ou `source/handoffs/` na
captura) seguindo [`agents/contracts/handoff.md`](../../../agents/contracts/handoff.md).
O próximo perfil não começa se houver `BLOCKED_INPUT`, output ausente,
`open_issues` sem causa/correção ou check sem evidência.

## Correções para os benchmarks

- **Apple BR oficial (71,04 / 75,72%):** o forense mede a tipografia real e o visual
  designer compara densidade e imagens por seção; o prototyper não encerra com
  footer/TV/promo incompletos.
- **Warframe EN oficial (64,03 / 61,58%):** o inventário de assets e a matriz de seções
  bloqueiam placeholders; o QA agrupa as regiões grandes de hero, cards e
  fundos antes de consumir um ciclo.
- **GitHub oficial (84,10 / 93,32%):** o gate estrutural e semântico é
  obrigatório mesmo com cobertura alta; inventário vazio não pode resultar em
  aprovação.

Essas três versões foram escolhidas pelo usuário como baselines canônicas. A
aceitação humana não altera o estado automático `NEEDS_REVIEW` nem converte um
score abaixo de 90 em aprovação do gate.

O score determinístico continua imutável. A melhoria vem de entradas melhores,
de uma composição editável verificável e de uma revisão em camadas, não de
baixar limiares ou ajustar a fórmula.
