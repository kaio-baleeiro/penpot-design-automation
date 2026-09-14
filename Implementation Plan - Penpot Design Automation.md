---
type: implementation-plan
status: complete
created: 2026-09-14
updated: 2026-09-14
source_agent: codex
agent_context: codex-desktop
project: Penpot Design Automation
confidence: high
review: false
---

# Implementation Plan - Penpot Design Automation

## Target Outcome

Entregar infraestrutura migrada, skills instaláveis, scripts validados, teste com
KatiauInvest e repositório público publicado.

## Files Or Systems Affected

- Novo workspace no vault.
- Infraestrutura Docker anteriormente mantida no KatiauInvest.
- Perfil global de skills em `/Users/baleeiro/.agents/skills`.
- Perfil MCP local do Codex.
- Repositório GitHub `kaio-baleeiro/penpot-design-automation`.

## Plan

1. [x] Fechar escopo e decisões com o usuário.
2. [x] Criar backup consistente de banco, assets e configuração local.
3. [x] Implementar infraestrutura portátil usando volumes externos.
4. [x] Implementar skills, contratos e política de trabalhadores Luna.
5. [x] Implementar e testar captura, mapeamento e validação visual.
6. [x] Migrar a composição e confirmar preservação dos dados.
7. [x] Instalar a skill global e registrar o MCP sem expor o token.
8. [x] Executar validação ponta a ponta com KatiauInvest.
9. [x] Remover o acoplamento antigo do KatiauInvest e atualizar suas notas.
10. [x] Criar, publicar e verificar o repositório, posteriormente tornado público
    por decisão do usuário.
11. [x] Adequar as sete skills ao formato Agent Skills com recursos locais.
12. [x] Criar e integrar o ciclo de lições aprendidas do projeto.
13. [x] Formalizar a política source-first para inventário e reutilização de
    assets do site/runtime ou código fornecido.

## Validation

- Backups com checksums válidos.
- Containers saudáveis e endpoints locais respondendo.
- Skills sem erros de estrutura ou placeholders.
- Testes automatizados aprovados.
- Run do KatiauInvest com artefatos rastreáveis e comparação visual.
- Coerência automática entre estado terminal, score final e entrega.
- Lição só pode ser marcada como mitigada depois de registrar verificação.

## Rollback

Reutilizar a composição antiga com os volumes preservados ou restaurar o dump do
PostgreSQL e o arquivo dos assets guardados em `state/backups`.

## Links

- [[P - Penpot Design Automation]]
- [[Technical Spec - Penpot Design Automation]]
