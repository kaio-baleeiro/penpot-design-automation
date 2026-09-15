# Lições do build

Registre aqui falhas de MCP, componentes provisórios, asset refs, logs ou
truncamento na construção. Regras do projeto ficam em `project/`; limitações
da máquina ficam em `local/` e não são versionadas. Regras que afetem captura
ou validação devem ser linkadas ao [índice compartilhado](../../penpot-design/lessons-learned/README.md).

`kind: machine` fica restrito a esta memória local; `kind: project` exige
integração no build, referência, teste ou gate antes de ser mitigada.

Regra base: plano aprovado primeiro, mutação MCP depois, log append-only sempre.
