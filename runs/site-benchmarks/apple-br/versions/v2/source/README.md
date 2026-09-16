# Evidência de origem — Apple Brasil v2

Esta pasta contém apenas referências públicas sanitizadas. A captura integral
tem 1440×5261 pixels e representa todo o documento finito, não apenas o
primeiro viewport. DOM, estilos brutos, cookies e payloads do navegador
permanecem no armazenamento ignorado da versão histórica.

`source-map.json`, `source-inventory.md`, `assets-manifest.json` e
`frame-spec.json` são a entrada obrigatória do build. Os caminhos dos assets
são first-party observados na própria página; o builder deve tentar reutilizar
os arquivos exatos e registrar qualquer indisponibilidade no log MCP.
