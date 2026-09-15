---
type: lesson
status: mitigated
kind: project
integration: scripts/penpot_mcp.py; tests/test_security_and_sources.py
scope: shared
applies_to: [penpot-build, penpot-validate, penpot-delivery]
---

# Credenciais MCP nunca aparecem no diagnóstico

Logs de request, response, URL e erro devem redigir tokens, cookies, senhas e
endpoints autenticados antes de persistir ou exibir qualquer saída. A chave
local fica apenas no ambiente ignorado.

Verificação: testes de redação, transporte MCP e varredura de segredos do CI.
