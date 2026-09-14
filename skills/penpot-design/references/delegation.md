# Delegação de trabalhadores Luna no workflow Penpot

Toda fase operacional é iniciada pelo orquestrador do Codex com um subagente
explicitamente configurado como `gpt-5.6-luna`. A delegação precisa declarar:

- objetivo observável e fase do workflow;
- entradas e diretórios permitidos;
- artefatos esperados;
- gates, limite de ciclos e condição de parada;
- proibição de alterar contratos, scores e evidências históricas.

O orquestrador verifica o retorno do runtime. Se a criação/execução do
subagente rejeitar `gpt-5.6-luna`, exceder a cota ou informar indisponibilidade,
registre `BLOCKED_MODEL_UNAVAILABLE` e pare a fase; não repita com outro modelo.
Scripts locais não tentam escolher modelo porque essa decisão pertence ao
runtime de agentes, não ao Penpot ou ao Playwright.
