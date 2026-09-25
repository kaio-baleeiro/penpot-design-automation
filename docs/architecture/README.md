# Arquitetura versionada

- `penpot-workflow.json` é a fonte estruturada destinada a agentes: entradas,
  rotas, fases, artefatos, perfis, transições e invariantes.
- `penpot-workflow-architecture.svg` é o diagrama visual de ponta a ponta.

O JSON referencia os contratos executáveis no repositório. Se o controller,
os estados ou os gates mudarem, atualize a arquitetura junto e mantenha
`tests/test_architecture.py` passando.
