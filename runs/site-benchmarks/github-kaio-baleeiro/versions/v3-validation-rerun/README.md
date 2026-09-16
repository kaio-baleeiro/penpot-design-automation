# GitHub kaio-baleeiro — revalidação v3

Reexecução determinística dos três ciclos sobre o export editável Penpot
registrado na v2. A fonte e o frame têm 1440×1807 px, preservando a captura
full-page.

Resultados: ciclo 1 **98,52**, ciclo 2 **98,52**, ciclo 3 **98,52**;
cobertura **92,79%** em todos. O score visual passa, porém os três ciclos
terminaram em `NEEDS_REVIEW` por fidelidade semântica/conteúdo e porque o
inventário estrutural não comprova componentes nem instâncias reutilizáveis.

Cada `cycles/cycle-N/` contém `score.json`, `issues.json`, `report.md` e os
artefatos PNG side-by-side, overlay e heatmap.
