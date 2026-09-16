---
type: lesson
status: mitigated
kind: project
integration: skills/penpot-validate/SKILL.md; skills/penpot-validate/references/scoring.md; tests/test_workflow_gates.py
scope: penpot-validate
applies_to: [penpot-validate, penpot-build, penpot-delivery]
---

# A linha de base precisa representar o mesmo artefato

## Failure

Um ciclo de reconstrução editável foi comparado com a pontuação de uma versão
anterior baseada em captura. A queda de score gerou regressão, embora a
comparação não medisse duas versões equivalentes do design.

## Rule

Use a linha de base de regressão apenas entre ciclos da mesma versão editável,
com a mesma fonte, viewport e frame-spec. Ao trocar de screenshot de referência
para composição editável, abra uma nova versão/run e compare o primeiro ciclo
diretamente à fonte; nunca herde a pontuação do artefato incompatível.

## Countermeasure

O contrato de validação explicita a identidade da baseline e trata a troca de
representação como novo run. O relatório deve registrar fonte, frame-spec e
artefato comparados antes de interpretar uma queda como regressão.

## Verification

Os novos runs GitHub/Apple em `versions/v2` não herdaram score da representação
antiga: cada ciclo v2 compara a composição editável com a fonte e os ciclos
seguintes usam somente a baseline da própria versão. Os manifestos v2 registram
`prior_version`, referenciam esta lição e preservam o histórico anterior sem
usá-lo como regressão. A regra foi verificada e está mitigada.
