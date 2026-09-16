# Contrato de handoff entre perfis

Todo handoff é um arquivo versionado dentro do run (por exemplo,
`design/handoffs/v001-visual-ui.json`). Nunca sobrescreva um handoff anterior.

## Campos obrigatórios

```json
{
  "schema_version": "1.0",
  "profile": "penpot-mcp-prototyper",
  "worker_model": "gpt-5.6-luna",
  "run_id": "...",
  "phase": "build",
  "inputs": ["..."],
  "outputs": ["..."],
  "decisions": [{"id": "...", "decision": "...", "evidence": "..."}],
  "open_issues": [],
  "checks": [{"name": "asset-provenance", "status": "pass", "evidence": "..."}],
  "next_profile": "visual-qa-auditor",
  "stop_condition": "..."
}
```

`inputs` e `outputs` são caminhos relativos ao run; não coloque cookies, tokens,
URLs autenticadas ou caminhos absolutos. `open_issues` precisa incluir região,
causa provável e correção sugerida quando houver falha. `checks` só pode dizer
`pass` com evidência verificável.

## Gatilhos de bloqueio

O perfil deve parar e devolver `BLOCKED_INPUT` quando faltar fonte, asset
essencial, frame-spec, estado dinâmico aprovado ou acesso ao MCP/Luna. Não
preencha lacunas com um screenshot colado, texto inventado ou ícone genérico.

O perfil de QA devolve `NEEDS_REVIEW` se score < 90, coverage < 80%, houver P0/P1,
conteúdo/fonte divergente, asset sem procedência ou inventário estrutural
ausente. O perfil não altera os arquivos de ciclo nem o resultado do avaliador.
