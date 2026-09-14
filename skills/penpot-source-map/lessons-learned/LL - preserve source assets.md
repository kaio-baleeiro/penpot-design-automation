---
type: lesson
status: mitigated
scope: penpot-source-map
---

# Preserve os assets exatos da origem

Quando a origem fornece SVG, imagem, ícone, logo ou fonte utilizável, buscar um
similar externo cria divergência evitável e perde provenance. Inventarie e
reutilize o asset original antes de considerar substituição.

Verificação: `source/assets-manifest.json`, hashes e testes de segurança do
mapa de fontes.
