# Lições do source map

Registre aqui erros de captura, medição, provenance, assets, hashes ou
precedência entre URL, screenshot e código. Compartilhe regras transversais no
[índice do orquestrador](../../penpot-design/lessons-learned/README.md).

Use `kind: machine` para problemas da estação e `kind: project` quando a regra
deve entrar no contrato ou nos scripts do source map.

Regra base: nenhuma tela vai para construção sem `source-map.json`,
`source-inventory.md`, `assets-manifest.json` e `frame-spec.json` sanitizados.
