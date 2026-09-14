# Lições compartilhadas do workflow Penpot

Este é o índice transversal das lições que afetam mais de uma fase. As lições
específicas ficam dentro do `lessons-learned/` da skill que expôs o problema;
adicione aqui um link quando a regra também orientar outra skill.

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

- [Viewport não é a extensão final do frame](LL - viewport is not the final frame extent.md)
- [Recursos da skill devem resolver a partir da raiz do checkout](LL - resolve resources from skill root.md)
- [Estado terminal precisa estar persistido no manifesto](LL - persist terminal state.md)
- [Metadata precisa passar no spec e no host](LL - validate skill metadata.md)
- [Credenciais MCP nunca aparecem no diagnóstico](../../penpot-build/lessons-learned/LL - redact MCP credentials.md)
