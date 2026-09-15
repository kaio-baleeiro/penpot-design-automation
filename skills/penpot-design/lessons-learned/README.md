# Lições compartilhadas do workflow Penpot

Cada skill mantém suas lições em dois buckets irmãos. `project/` contém regras
do produto/workflow e é versionado; `local/` contém apenas detalhes da máquina
que executa o checkout e é ignorado pelo Git. Este arquivo é o índice transversal
das regras de `project/` que afetam mais de uma fase.

## Classificação

- `kind: machine`: comportamento específico da estação, sistema operacional,
  Docker, navegador, rede, volumes ou credenciais locais. Vai para
  `skills/<skill>/lessons-learned/local/`, permanece fora do Git e não vira
  regra do workflow.
- `kind: project`: comportamento do Penpot Automation. Depois da verificação,
  vai para `skills/<skill>/lessons-learned/project/`, deve ser integrado a
  `SKILL.md`, referência, script, teste ou gate e mantém a lição como
  rastreabilidade.

## Regras

- Registre contexto, evidência, regra futura e contramedida.
- Escreva um teste ou verificação reproduzível antes de marcar `mitigated`.
- Não apague histórico: use novos arquivos/versionamento.
- Mantenha tokens, cookies, capturas autenticadas e exports privados fora do
  Git.

## Índice por skill

- [penpot-design](../../penpot-design/lessons-learned/README.md)
- [penpot-intake](../../penpot-intake/lessons-learned/README.md)
- [penpot-source-map](../../penpot-source-map/lessons-learned/README.md)
- [penpot-build](../../penpot-build/lessons-learned/README.md)
- [penpot-validate](../../penpot-validate/lessons-learned/README.md)
- [penpot-design-system](../../penpot-design-system/lessons-learned/README.md)
- [penpot-delivery](../../penpot-delivery/lessons-learned/README.md)

## Lições transversais

- [Viewport não é a extensão final do frame](project/LL - viewport is not the final frame extent.md)
- [Recursos da skill devem resolver a partir da raiz do checkout](project/LL - resolve resources from skill root.md)
- [Estado terminal precisa estar persistido no manifesto](project/LL - persist terminal state.md)
- [Metadata precisa passar no spec e no host](project/LL - validate skill metadata.md)
- [Credenciais MCP nunca aparecem no diagnóstico](../../penpot-build/lessons-learned/project/LL - redact MCP credentials.md)
