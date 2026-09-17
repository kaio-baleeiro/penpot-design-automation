---
id: build-active-page-serial-mutations
kind: project
status: mitigated
title: Active Penpot page makes MCP mutations serial
integration: penpot-build/SKILL.md; benchmark v4 orchestration
---

## Failure

Workers paralelos abriram páginas diferentes do mesmo arquivo Penpot. Como a
página ativa é compartilhada, mutações e exports passaram a atingir o contexto
do último worker, criando páginas duplicadas e handoffs inconsistentes.

## Rule

Preparação de fontes e scripts pode ocorrer em paralelo, mas abertura de
página, mutação, inventário e export do mesmo arquivo Penpot são uma fila
serial. Cada operação confirma os ids esperados de página e frame.

## Countermeasure

O contrato de build proíbe mutações MCP concorrentes no mesmo arquivo e exige
assert de página/frame antes do efeito. Duplicatas devem ser removidas por ids
resolvidos, preservando as versões históricas aprovadas.

## Verification

A rodada v4 executou Apple, GitHub e Warframe em série e terminou com uma única
página final por benchmark, mantendo as páginas v2 históricas.
