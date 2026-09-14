# Penpot local

Esta composição mantém uma instância Penpot local e compartilhada para os projetos de design automatizado. Ela publica somente:

- Penpot: <http://localhost:9001>
- Mailcatcher: <http://localhost:1080>

Os sete serviços são `penpot-frontend`, `penpot-backend`, `penpot-mcp`, `penpot-exporter`, `penpot-postgres`, `penpot-valkey` e `penpot-mailcatch`.

## Preparação

1. Copie `.env.example` para `.env` dentro deste diretório.
2. Gere valores locais para `PENPOT_SECRET_KEY` e `PENPOT_POSTGRES_PASSWORD`.
3. Confirme que os volumes externos `katiauinvest-penpot_penpot_postgres_data` e `katiauinvest-penpot_penpot_assets` existem, ou restaure-os antes de subir a composição.

O `.env`, os backups e os dados persistentes ficam fora do Git. Os volumes externos são deliberados: a migração troca a composição sem copiar nem apagar os dados existentes.

## Operação segura

Os scripts em `scripts/` são o contrato operacional:

```sh
./scripts/up.sh
./scripts/healthcheck.sh
./scripts/logs.sh
./scripts/down.sh
```

`down.sh` nunca usa `--volumes`. Backup e restore exigem a confirmação explícita documentada no próprio script. Para revisar a configuração renderizada sem iniciar serviços:

```sh
./scripts/validate.sh
```

Consulte [docs/infra.md](../../docs/infra.md) para migração, backup, restore, atualização e rollback.

## MCP

A composição habilita o MCP oficial do Penpot com `enable-mcp`. Depois de criar ou acessar a conta local e abrir um arquivo, use **Your account → Integrations → MCP Server**, habilite o servidor e gere uma URL/token. O token é pessoal e não deve entrar no repositório.

Registre a URL somente na configuração local do Codex, por exemplo:

```sh
codex mcp add penpot-design --url '<URL_COPIADA_DO_PENPOT>'
```

Não coloque cookies, tokens, credenciais ou URLs autenticadas em issues, commits ou manifestos de origem.
