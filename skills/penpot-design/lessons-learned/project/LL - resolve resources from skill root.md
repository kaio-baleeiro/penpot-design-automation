---
type: lesson
status: mitigated
kind: project
integration: scripts/penpot_validation; tests/test_frame_sizing.py
scope: shared
applies_to: [penpot-design, penpot-intake, penpot-source-map, penpot-build, penpot-validate, penpot-design-system, penpot-delivery]
---

# Recursos devem resolver a partir da raiz do checkout

Wrappers chamados a partir de `/`, de um terminal do agente ou de outro
diretório precisam localizar o checkout físico antes de importar scripts ou
referências. Caminhos relativos ao diretório atual quebram execuções válidas.

Verificação: testes de wrappers executados com `cwd=/`.
