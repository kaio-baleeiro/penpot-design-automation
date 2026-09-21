# Delegação portável no workflow Penpot

Toda fase operacional é iniciada pelo agente principal com um worker separado.
O host resolve o worker econômico por `agents/runtime-policy.yaml` e usa o
adaptador nativo disponível. A delegação precisa declarar:

- objetivo observável e fase do workflow;
- entradas e diretórios permitidos;
- artefatos esperados;
- gates, limite de ciclos e condição de parada;
- proibição de alterar contratos, scores e evidências históricas.

O worker executa a mão na massa: captura, inspeção, construção no MCP,
exportação, correções direcionadas e coleta de evidências. Ele pode explicar
achados, mas não é o revisor final e não atribui a pontuação oficial nem muda
o estado de aprovação. O orquestrador/revisor executa ou confere o avaliador
determinístico, registra a pontuação sem override e decide a transição do
estado conforme os gates.

O orquestrador verifica o retorno do runtime. Se a criação/execução do worker
exceder a cota ou informar indisponibilidade, registre
`BLOCKED_WORKER_UNAVAILABLE` e pare a fase. A seleção não pode ser silenciosa:
qualquer modelo diferente do mapeamento padrão precisa ser registrado antes da
fase. Scripts locais não escolhem modelo; essa decisão pertence ao runtime de
agentes, não ao Penpot ou ao Playwright.

## Adaptadores oficiais

- Codex: subagente dinâmico com preferência por `gpt-5.6-luna`.
- Claude Code: `.claude/agents/<profile>.md`.
- Devin CLI: `.devin/agents/<profile>.md`.
- Gemini CLI: `.gemini/agents/<profile>.md`.
- Outros hosts: fornecer o `AGENT.md` canônico a um worker separado e registrar
  runtime/modelo no handoff.
