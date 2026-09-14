---
type: task
status: backlog
created: 2026-09-14
updated: 2026-09-14
source_agent: codex
agent_context: codex-desktop
project: Penpot Design Automation
priority: low
due:
confidence: high
review: false
---

# Task - Renomear volumes legados do Penpot

## Outcome

Substituir os nomes `katiauinvest-penpot_*` por nomes neutros do projeto sem
perder banco ou assets.

## Checklist

- [ ] Criar novo backup consistente e verificar checksums.
- [ ] Criar volumes neutros de destino.
- [ ] Restaurar banco e assets em ambiente isolado.
- [ ] Validar conta, times, projetos, arquivos, assets, exportação e MCP.
- [ ] Trocar os nomes externos no Compose.
- [ ] Remover volumes antigos somente após aceite explícito e novo backup.

## Context

A migração inicial reutiliza os volumes existentes para minimizar risco e evitar
cópia durante a mudança de ownership da infraestrutura.

## Done When

- [ ] A composição usa somente volumes com nomes neutros.
- [ ] O rollback foi testado e os dados foram conferidos.

## Links

- [[P - Penpot Design Automation]]
- [[Technical Spec - Penpot Design Automation]]
