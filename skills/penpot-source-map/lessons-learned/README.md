# Lições do source map

Registre aqui erros de captura, medição, provenance, assets, hashes ou
precedência entre URL, screenshot e código. Regras do projeto ficam em
`project/`; problemas da máquina ficam em `local/` e são ignorados pelo Git.
Compartilhe regras transversais no
[índice do orquestrador](../../penpot-design/lessons-learned/README.md).

Use `kind: machine` para problemas da estação e `kind: project` quando a regra
deve entrar no contrato ou nos scripts do source map.

Regra base: nenhuma tela vai para construção sem `source-map.json`,
`source-inventory.md`, `assets-manifest.json` e `frame-spec.json` sanitizados.

Fonte dinâmica sem estado finito reproduzível não entra em pontuação. Consulte
[estado dinâmico precisa de limite antes de pontuar](project/LL%20-%20bounded%20state%20before%20scoring.md).

Estabilidade dimensional não garante mídia pronta; consulte [dimensões não provam asset readiness](project/LL%20-%20dimensions%20do%20not%20prove%20asset%20readiness.md).
