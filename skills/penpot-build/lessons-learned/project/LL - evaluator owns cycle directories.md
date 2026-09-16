---
type: lesson
status: mitigated
kind: project
integration: skills/penpot-build/SKILL.md; skills/penpot-design/references/artifacts.md; tests/test_penpot_validation.py
scope: penpot-build
applies_to: [penpot-build, penpot-validate, penpot-delivery]
---

# O avaliador é dono dos diretórios de ciclo

## Failure

Uma execução colocou export do Penpot e README em `versions/v2/cycles/cycle-1`
antes do score. O avaliador append-only recusou a validação com
`FileExistsError`, pois o diretório já não estava vazio.

## Rule

O build nunca cria, popula ou documenta `cycles/cycle-N`. Exports e planos
ficam em `design/exports/` e `design/`; relatórios, scores, issues e imagens
comparativas entram no ciclo somente quando o avaliador os gerar.

## Countermeasure

O contrato de artefatos declara `cycles/cycle-N/` como diretório exclusivo do
avaliador e o build aponta todos os exports para `design/exports/`. Antes de
validar, o orquestrador só pode selecionar o próximo ciclo vazio.

## Verification

O teste de validação prepara um ciclo não vazio e confirma a recusa imutável.
As execuções `runs/site-benchmarks/apple-br/versions/v2` e
`runs/site-benchmarks/github-kaio-baleeiro/versions/v2` produziram os três
ciclos somente com `score.json`, `issues.json`, `report.md`, side-by-side,
overlay e heatmap; exports permaneceram em `design/exports/`. A regra foi
verificada no fluxo real e está mitigada.
