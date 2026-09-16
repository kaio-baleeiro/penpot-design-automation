---
type: lesson
status: active
kind: project
integration: skills/penpot-source-map/SKILL.md; skills/penpot-source-map/references/frame-sizing.md; tests/test_frame_sizing.py
scope: penpot-source-map
applies_to: [penpot-source-map, penpot-build, penpot-validate, penpot-delivery]
---

# Estabilidade dimensional não prova completude visual

## Failure

Uma captura full-page da Apple parou de crescer e foi marcada `stable: true`,
mas tiles promocionais ainda estavam sem mídia por causa de lazy loading. O
frame tinha dimensões corretas, porém a referência usada no score não
representava a página renderizada completa.

## Rule

Antes de congelar a referência, verifique prontidão visual e de assets além da
estabilidade dimensional: percorra as seções, aguarde mídia lazy, confira
imagens/SVGs/fontes carregados e compare o inventário de assets com a captura.
Se houver lacuna, registre a limitação e peça recaptura ou aprovação explícita;
não trate `stable: true` como prova de fidelidade.

## Countermeasure

O source map e o frame-sizing exigem sondagens de scroll, auditoria de seções e
asset readiness antes do handoff. Uma referência incompleta permanece marcada
com baixa confiança/pendência e não deve ser usada para declarar fidelidade.

## Verification

O contrato e o teste documental exigem a auditoria visual/asset separada da
medição de altura; a lição permanece ativa até um benchmark comprovar essa
checagem com evidência persistida.
