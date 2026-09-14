---
type: project-infrastructure
status: active
created: 2026-09-14
updated: 2026-09-14
source_agent: codex
agent_context: penpot-design-automation
confidence: high
review: false
---

# Infraestrutura do Penpot

## Objetivo

Manter uma instância Penpot 2.17 local, compartilhada por todos os projetos futuros de design. A superfície HTTP é restrita ao host local:

- `http://localhost:9001` — Penpot
- `http://localhost:1080` — Mailcatcher

A composição contém sete serviços: frontend, backend, MCP, exporter, PostgreSQL, Valkey e Mailcatcher.

## Dados e migração

O compose usa, como volumes externos, os dados que já pertenciam à instalação do KatiauInvest:

- `katiauinvest-penpot_penpot_postgres_data` — banco PostgreSQL
- `katiauinvest-penpot_penpot_assets` — assets do Penpot

Isso evita copiar ou apagar dados na primeira migração. O nome do projeto Compose é genérico (`penpot-design-automation`), portanto a identidade da composição não fica acoplada ao produto KatiauInvest.

Segredos e persistência não são versionados. O arquivo `infra/penpot/.env` deve ser criado localmente a partir de `.env.example`. A URL/token do MCP deve permanecer apenas na configuração local do Codex.

Ao rotacionar a chave MCP pelo Penpot, use o botão de cópia da própria interface
e execute `scripts/update-mcp-key-from-clipboard.sh` na raiz do projeto. O script
valida o conteúdo, atualiza o `.env` com permissão `0600` e recria o registro
local `penpot-design` do Codex sem exibir a chave. Ele depende de `pbpaste` e,
portanto, é destinado à estação macOS onde esta instância está instalada.

## Comandos

Todos os comandos devem ser executados a partir de `infra/penpot` ou usando os scripts:

```sh
./scripts/validate.sh       # valida sintaxe e dependências sem iniciar nada
./scripts/up.sh             # inicia ou atualiza os sete serviços
./scripts/healthcheck.sh    # verifica containers, HTTP, Mailcatcher e volumes
./scripts/logs.sh [serviço] # acompanha logs; Ctrl-C encerra apenas o acompanhamento
./scripts/down.sh           # para a composição sem remover volumes
./scripts/backup.sh [dir]   # backup lógico do banco + arquivo de assets
./scripts/restore.sh DIR    # restore destrutivo, exige confirmação explícita
./scripts/update.sh [versão]# troca a versão após validação e backup
```

Os scripts falham se `.env` não existir. Não preencha segredos no `.env.example`.

## Backup e restore

O backup gera um diretório com `manifest.env`, `database.dump` e `assets.tgz`. O manifesto registra versão, data, projeto e volumes usados. O backup deve ser feito antes de qualquer atualização ou restore.

O restore exige `PENPOT_RESTORE_CONFIRM=YES` e um diretório de backup válido. Ele para os serviços de aplicação, restaura o banco no PostgreSQL e substitui o conteúdo do volume de assets; depois sobe a composição novamente. O restore nunca remove os volumes externos, mas substitui seu conteúdo. Faça uma cópia adicional antes de restaurar se houver dúvida.

## Atualização e rollback

`update.sh` exige uma versão explícita, executa `validate.sh`, cria backup e só então atualiza `PENPOT_VERSION` no `.env`. Em caso de falha, restaure a versão anterior no `.env`, execute `up.sh` e, se necessário, use `restore.sh` com o backup gerado. A alteração de versão e o backup devem ser registrados na revisão do projeto.

## Manutenção posterior

Os volumes ainda têm os nomes históricos do KatiauInvest para viabilizar a migração sem cópia. Depois de validar a operação e uma restauração completa, planejar uma janela de manutenção para:

1. criar volumes com nomes neutros do projeto;
2. copiar os dados com o stack parado e backup verificado;
3. apontar o `.env` para os novos nomes;
4. executar healthcheck e teste de login/arquivo/MCP;
5. manter os volumes históricos em retenção até confirmar rollback.

Não execute essa renomeação automaticamente.

## Validação de segurança

- Portas publicadas apenas em `127.0.0.1`.
- `down.sh` não remove volumes.
- `restore.sh` não aceita execução sem `PENPOT_RESTORE_CONFIRM=YES`.
- Segredos, tokens MCP, cookies, dumps e assets ficam fora do Git.
- A rotação da chave usa a área de transferência e não coloca o token em argumentos documentados ou relatórios.
