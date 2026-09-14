---
type: workflow-intake
status: complete
created: 2026-09-14
updated: 2026-09-14
source_agent: codex
agent_context: codex-desktop
confidence: high
review: false
---

# Intake — KatiauInvest E2E

## Perguntas iniciais e respostas

- Objetivo: validar de ponta a ponta a rota de reprodução usando o KatiauInvest
  como caso real autorizado pelo usuário.
- Fontes: aplicação local autenticada, código local e arquivo Penpot preservado.
- Escopo: quatro telas desktop já presentes no arquivo Penpot: visão geral,
  investimentos, importação e assistente.
- Viewport: desktop 1440×900. A fonte atual possui outras rotas, mas o protótipo
  disponível não cobre todas elas nem uma variante mobile correspondente.
- Fidelidade: aplicar o gate objetivo por tela; o ensaio não autoriza alterar o
  produto-fonte nem o arquivo histórico apenas para forçar aprovação.
- Saída: relatório sanitizado, score, issues localizadas, lado a lado anotado,
  overlay e heatmap.

## Pergunta obrigatória de adendo/mudança

O usuário respondeu que não havia adendo por ora e autorizou a migração,
construção e validação do workflow, incluindo o uso do KatiauInvest como cobaia.

## Análise de ambiguidades

Não há ambiguidade bloqueante para este ensaio. Telas sem correspondência no
arquivo Penpot e mobile ficam fora da cobertura desta execução, explicitamente
registradas como limitação, sem serem contabilizadas como aprovadas.
