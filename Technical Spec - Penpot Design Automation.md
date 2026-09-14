---
type: technical-spec
status: complete
created: 2026-09-14
updated: 2026-09-14
source_agent: codex
agent_context: codex-desktop
project: Penpot Design Automation
confidence: high
review: false
---

# Technical Spec - Penpot Design Automation

## Objective

Definir a infraestrutura compartilhada, os contratos das skills e a validação
reproduzível do workflow de design no Penpot.

## Requirements

- Preservar banco, assets, conta, times, projetos e arquivos existentes.
- Operar Penpot 2.17 em `127.0.0.1:9001` e Mailcatcher em `127.0.0.1:1080`.
- Manter PostgreSQL, Valkey, assets, exporter e MCP isolados.
- Versionar skills e scripts no repositório público do GitHub.
- Instalar `penpot-design` globalmente sem duplicar a fonte canônica.
- Produzir manifests, mapas, decisões, scores, issues e evidências por execução.
- Tornar o score determinístico e não editável por agentes.
- Separar viewport de observação dos limites finais do frame e impedir
  truncamento ou expansão horizontal sem evidência.

## Proposed Approach

O repositório combina três camadas: `infra/penpot`, skills modulares sob `skills/`
e scripts determinísticos sob `scripts/`. O orquestrador mantém uma máquina de
estados; trabalhadores Luna recebem pacotes pequenos e acionáveis. A aprovação é
calculada pelos scripts e exige também a passagem do gate estrutural.

Os volumes Docker atuais permanecem externos na primeira migração. Backups locais,
segredos e capturas privadas ficam em diretórios ignorados pelo Git.

## Testing

- Validar a configuração Docker e healthchecks.
- Verificar checksums e legibilidade do backup.
- Confirmar login e contagens persistidas após a migração.
- Validar todas as skills com o validador oficial da `skill-creator`.
- Testar imagens idênticas, divergentes e regressões na suíte visual.
- Executar um run rastreável usando telas do KatiauInvest.

## Migration Or Rollback

Parar a composição antiga sem remover volumes, subir a nova configuração usando
os mesmos volumes externos e validar dados. Para rollback, parar a nova composição
e restaurar a anterior ou os backups consistentes.

## Risks

- Um `down -v` ou remoção manual dos volumes destruiria dados persistidos.
- A URL MCP contém um token pessoal e não pode aparecer em Git, notas ou logs.
- Comparação raster isolada pode gerar falsos positivos; o score deve combinar
  geometria, tipografia, cor, assets e similaridade visual.

## Resultado

A implementação possui 7 skills, cliente MCP com handshake real e log redigido,
captura Playwright autenticada, mapa multi-fonte, score visual versionado,
máquina de estados estrita, inventário MCP, dimensionamento inteligente e gate
estrutural. A suíte local possui 45 testes; forward tests Luna confirmaram
caminhos, contratos e os casos de página longa/overflow.

## Links

- [[P - Penpot Design Automation]]
- [[Implementation Plan - Penpot Design Automation]]
- [[Task - Renomear volumes legados do Penpot]]
- [[Handoff - Penpot Design Automation]]
- [[Technical Spec - Penpot MCP Local - KatiauInvest]]
