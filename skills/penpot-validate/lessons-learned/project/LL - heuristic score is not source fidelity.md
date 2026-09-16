---
type: lesson
status: active
kind: project
integration: skills/penpot-validate/SKILL.md; skills/penpot-validate/references/scoring.md; tests/test_workflow_gates.py
scope: penpot-validate
applies_to: [penpot-source-map, penpot-build, penpot-validate, penpot-delivery]
---

# Score heurístico alto não prova fidelidade da fonte

## Failure

O benchmark GitHub obteve score heurístico de 93,96 e coverage de 88,15% em
uma tela de fundo claro, mas o perfil reconstruído tinha nomes de repositório,
avatar, README, cabeçalho e atividade fictícios. O gate visual não detectou a
divergência semântica.

## Rule

O score determinístico de imagem é imutável e continua sendo necessário, mas
não basta para aprovação. O revisor deve executar um gate independente de
fidelidade semântica e de provenance: textos, rotas/estado, hierarquia,
logos/ícones/imagens, fontes e `asset_refs` precisam corresponder à fonte ou
estar explicitamente marcados como desconhecidos/pendentes.

## Countermeasure

Antes de aprovar ou entregar, comparar o conteúdo observável com
`source-inventory.md`, `assets-manifest.json`, `frame-spec.json` e o plano;
registrar cada divergência no relatório. Uma tela que passa numericamente, mas
falha esse checklist, fica `NEEDS_REVIEW` sem alterar a fórmula ou o limiar.

## Verification

O contrato de validação e o checklist de revisão documentam o gate separado;
esta lição permanece ativa até uma execução de benchmark comprovar a inspeção
semântica e de assets com evidência persistida.
