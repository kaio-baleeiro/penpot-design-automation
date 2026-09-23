# Penpot local

Esta composição mantém uma instância Penpot local e compartilhada para os projetos de design automatizado. Ela publica somente:

- Penpot: <http://localhost:9001>
- Mailcatcher: <http://localhost:1080>

Os sete serviços são `penpot-frontend`, `penpot-backend`, `penpot-mcp`, `penpot-exporter`, `penpot-postgres`, `penpot-valkey` e `penpot-mailcatch`.

A instância foi configurada para HTTP em loopback. Não a exponha por domínio,
IP ou proxy sem ativar HTTPS e restaurar cookies seguros. O servidor PREPL de
desenvolvimento está desabilitado.

## Preparação

### Clone novo

Na raiz do repositório, execute:

```sh
./penpot-workflow begin
./penpot-workflow select infrastructure --user-answer "quero preparar a infraestrutura"
./penpot-workflow bootstrap-infra
```

O bootstrap cria `.env` na raiz com segredos aleatórios, provisiona uma conta local e habilita o MCP. Usa os volumes neutros
`penpot-design-automation_postgres_data` e `penpot-design-automation_assets` e
permite que o `up.sh` os crie na primeira execução. O terminal mostra o email e
a senha da conta; o token MCP fica somente no `.env`. Nada sobrescreve um `.env`
existente.

### Instalação migrada

Nesta máquina, o `.env` ignorado pode manter volumes históricos. Os nomes
concretos pertencem à configuração local e não devem ser copiados para um clone
novo; use o bootstrap ou um restore documentado.

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

A composição habilita o MCP oficial do Penpot com `enable-mcp`. O bootstrap
provisiona o usuário e a chave pela API local; use **Your account → Integrations
→ MCP Server** como fallback manual.

Para qualquer agente, registre a URL e o token somente no `.env` local como
`PENPOT_MCP_URL` e `PENPOT_MCP_TOKEN`, ou injete essas variáveis no ambiente.
O wrapper `scripts/penpot-mcp.sh` lê ambos sem imprimi-los. No Codex, também é
possível registrar a URL com:

```sh
codex mcp add penpot-design --url '<URL_COPIADA_DO_PENPOT>'
```

Não coloque cookies, tokens, credenciais ou URLs autenticadas em issues, commits ou manifestos de origem.
