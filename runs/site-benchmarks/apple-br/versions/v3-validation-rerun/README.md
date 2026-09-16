# Apple Brasil — revalidação v3

Reexecução determinística dos três ciclos sobre o export editável Penpot
registrado na v2. A fonte full-page tem 1440×5261 px e o frame mantém toda a
altura do documento.

Resultados: ciclo 1 **89,57**, ciclo 2 **89,57**, ciclo 3 **89,57**;
cobertura **71,42%** em todos. Os três ciclos terminaram em `NEEDS_REVIEW`:
score/cobertura ficaram abaixo de 90/80 e o inventário estrutural não comprova
componentes nem instâncias reutilizáveis.

Cada `cycles/cycle-N/` contém `score.json`, `issues.json`, `report.md` e os
artefatos PNG side-by-side, overlay e heatmap. Esta pasta registra a
revalidação; ela não substitui a necessidade de uma nova composição MCP.
