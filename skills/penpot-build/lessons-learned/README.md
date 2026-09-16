# Lições do build

Registre aqui falhas de MCP, componentes provisórios, asset refs, logs ou
truncamento na construção. Regras do projeto ficam em `project/`; limitações
da máquina ficam em `local/` e não são versionadas. Regras que afetem captura
ou validação devem ser linkadas ao [índice compartilhado](../../penpot-design/lessons-learned/README.md).

`kind: machine` fica restrito a esta memória local; `kind: project` exige
integração no build, referência, teste ou gate antes de ser mitigada.

Regra base: plano aprovado primeiro, mutação MCP depois, log append-only sempre.
O build também não pré-popula `cycles/cycle-N`; consulte [o avaliador é dono dos diretórios de ciclo](project/LL%20-%20evaluator%20owns%20cycle%20directories.md).
Boards aninhados usam coordenadas locais; consulte [boards aninhados exigem coordenadas locais](project/LL%20-%20nested%20boards%20require%20local%20coordinates.md).
