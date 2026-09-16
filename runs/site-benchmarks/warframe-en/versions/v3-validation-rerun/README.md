# Warframe EN — revalidação v3

Reexecução determinística dos três ciclos sobre o export editável Penpot da
v2, usando a referência dinâmica aprovada de 1440×5837 px. O overflow
horizontal acidental continua registrado no `source/frame-spec.json`.

Resultados: ciclo 1 **83,34**, ciclo 2 **83,34**, ciclo 3 **83,34**;
cobertura **60,72%** em todos. Os três ciclos terminaram em `NEEDS_REVIEW`
por score/cobertura abaixo de 90/80, regiões P1 e inventário estrutural sem
frame summary/componentes/instâncias reutilizáveis.

Cada `cycles/cycle-N/` contém `score.json`, `issues.json`, `report.md` e os
artefatos PNG side-by-side, overlay e heatmap.
