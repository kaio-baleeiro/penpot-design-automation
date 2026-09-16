---
type: lesson
status: active
kind: project
integration: skills/penpot-source-map/SKILL.md; skills/penpot-source-map/references/frame-sizing.md; tests/test_security_and_sources.py; tests/test_frame_sizing.py
scope: penpot-source-map
applies_to: [penpot-source-map, penpot-validate, penpot-delivery]
---

# Estado dinâmico precisa de limite antes de pontuar

## Failure

Uma página dinâmica manteve `stable: false` em tentativas de captura full-page.
Sem um limite reproduzível, não era possível saber se a altura e o conteúdo
comparados pertenciam à mesma tela; o score foi corretamente bloqueado.

## Rule

Não pontue nem entregue uma fonte instável. Defina e registre um estado finito
aprovado (rota, filtros, scroll e limite de conteúdo) ou peça decisão ao
usuário. Recapture a referência e derive o frame-spec desse mesmo estado antes
de construir e validar.

## Countermeasure

O mapa de fonte registra estabilidade, métricas, probes e a decisão de limite.
O validador rejeita full-page instável e exige `bounded_state`/`frame_bounds`
quando o conteúdo dinâmico não pode ser tratado como página finita.

## Verification

Os testes de captura e frame sizing cobrem estados estáveis e instáveis; o
benchmark Warframe permanece `NEEDS_REVIEW` enquanto não houver um limite
reprodutível.
