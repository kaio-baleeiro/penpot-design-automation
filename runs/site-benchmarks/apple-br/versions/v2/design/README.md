# Handoff de construção — Apple Brasil v2

O builder deve seguir `plan.json` e construir o frame
`Apple BR — Home — 1440x5261` como composição editável no novo arquivo geral
de benchmarks do Penpot. Não importar a referência como conteúdo visível.

O export em `exports/home/1440x5261.png` é deliberadamente um caminho
planejado; será preenchido pelo worker após a mutação MCP. O worker deve manter
`penpot-mcp-log.jsonl` append-only e entregar o frame para o revisor executar
os ciclos 1–3.
