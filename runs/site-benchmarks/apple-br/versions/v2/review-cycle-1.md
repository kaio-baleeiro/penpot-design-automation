# Revisão final — Apple BR — ciclo 1

- Revisor: orquestrador principal (Codex)
- Score visual determinístico atribuído: **85,93/100**; cobertura **71,31%**.
- Gates: score FAIL, cobertura FAIL, múltiplos P1; estrutura editável PASS.
- Decisão: **refatorar no ciclo 2**, sem tocar na fonte/score anteriores.
- Fonte: `source/reference-full-page.png` e frame 1440×5261.
- Export: `design/exports/home/1440x5261.png`.
- Comparações: `cycles/cycle-1/home-side-by-side-annotated.png`, `home-overlay.png`, `home-heatmap.png`.

## Handoff de correção direcionada

1. **Galeria TV y=3932–4455 (P1, largura total):** seis blocos de cor no Penpot substituem os fotogramas reais e o carousel da fonte. Usar os seis URLs `mzstatic` registrados em `source/proposals/rebuild-v2/assets-inventory.json`, com recorte/posicionamento dos cards e textos/controles editáveis.
2. **Grade de promoções y=2156–3920 (P1):** as tiles estão vazias, trocadas ou com produto fora de escala. Reconstruir o grid 2×3 de 702px com gutter de 12px conforme captura. Priorizar x=726–1428/y=2156–2736, x=0–726/y=3340–3920 e as diferenças dos demais quadrantes. Não preencher conteúdo que a referência capturou em branco sem registrar a limitação da origem.
3. **iPhone 18 Pro y=370–661 (P1 x=232–1220):** a arte first-party aparece pequena no export (~470px de produto) contra ~1000px na fonte. Aumentar/recortar image fill dentro da seção clipada para alinhar silhouette e manter título/CTAs nas coordenadas da captura.
4. **iPhone Duo y=1040–1440 (P1 x=418–1021):** a imagem aparece extremamente estreita; usar escala/crop de fundo ou layer de imagem com proporções e posição da fonte, sem distorcer horizontalmente o produto.
5. **Watch Series 12 y=1598–1927 (P1 nos dois relógios):** ampliar artwork para a escala dos dois relógios da fonte e afastar texto/CTAs das imagens; evitar colisão visível.
6. **Footer y=4503–5261:** faltam notas legais e colunas completas; preencher o conteúdo que consta na captura e medir densidade/alinhamento.
7. **Navegação e botões:** substituir glifo quadrado no logo Apple e links de texto simples por formas/asset e botões azul/contornado do estado capturado.

As seções podem usar imagens originais para artwork, mas títulos, CTAs, grupos de navegação, cards e rodapé devem seguir editáveis. O ciclo 2 deve usar este score como baseline de regressão, não o ciclo 3 da versão anterior.
