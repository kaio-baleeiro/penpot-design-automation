---
type: lesson
status: mitigated
kind: project
integration: scripts/penpot_validation/frame.py; tests/test_frame_sizing.py
scope: shared
applies_to: [penpot-design, penpot-source-map, penpot-build, penpot-validate]
---

# Viewport não é a extensão final do frame

`1440x900` é a janela desktop de observação e o mínimo do frame, não um corte
obrigatório. Meça documento e viewport separadamente. Conteúdo finito estável
faz o frame crescer verticalmente; largura adicional só é válida com evidência
de navegação horizontal intencional na página raiz. Conteúdo infinito exige um
limite reproduzível aprovado.

Verificação: testes de frame sizing, captura CDP `frame_bounds` e gate que
reprova truncamento ou alargamento injustificado.
