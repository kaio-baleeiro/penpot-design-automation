# Apple Brasil — benchmark v2

Pacote de reconstrução editável preparado para o builder Luna. Esta versão
reinicia o orçamento de validação em `cycle: 0`, sem alterar os ciclos
imutáveis da versão anterior (`80.27/100`, `69.80%` de cobertura).

Fonte prevalente: captura pública full-page de `https://www.apple.com/br/`,
viewport de observação `1440×900` e frame final `1440×5261`. A altura acompanha
o documento finito; a largura permanece em 1440 porque o overflow observado é
acidental/off-canvas. O plano exige reconstruir cada seção com textos, formas,
componentes e assets first-party editáveis — a captura é apenas evidência.

Leia `source/README.md` antes de capturar, `design/README.md` antes de construir
e `manifest.json` como handoff canônico. Os três ciclos desta versão devem ser
gerados pelo avaliador, em ordem, sem pré-criar `cycles/`.
## Status da versão

Os três ciclos foram executados e a versão terminou em NEEDS_REVIEW.
Consulte delivery/ para scores, evidências e plano de remoção das páginas
legadas no arquivo KatiauInvest.
