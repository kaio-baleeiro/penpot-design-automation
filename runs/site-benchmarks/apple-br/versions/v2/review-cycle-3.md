# Revisão final — Apple BR — ciclo 3

- Revisor: orquestrador principal (Codex)
- Score visual determinístico atribuído: **89,57/100**; cobertura **71,42%**.
- Gate final: **FAIL** (score <90, cobertura <80 e múltiplos P1).
- Decisão terminal: **NEEDS_REVIEW**; não haverá quarto ciclo interno.
- Fonte/export: `source/reference-full-page.png` / `design/exports/home/1440x5261-cycle3.png`, ambos 1440×5261.
- Evidência final: `cycles/cycle-3/home-side-by-side-annotated.png`, `home-overlay.png`, `home-heatmap.png`; cópias públicas em `../../analysis/v2-cycle-3-*`.

## Melhorias verificadas

Os três heróis ganharam escala em relação aos ciclos anteriores; a galeria TV virou um carrossel de 930px com previews. O score subiu de 85,93 → 87,30 → 89,57. A estrutura permanece editável, com imagem first-party para artwork e textos/formas em seções semanticamente separadas.

## Diferenças que impedem aprovação

1. **TV y=3932–4455, P1:** a hierarquia está próxima, mas o card principal usa `Matéria Escura` enquanto a captura mostra `Mayday`; imagens e previews têm recortes/ordem diferentes, e faltam texto/controles na posição correta.
2. **Promoções y=2156–3920, P1:** várias tiles ainda divergem da referência fixa em imagem, ordem, posição e texto. A captura original parece conter lazy media incompleta em alguns quadrantes, apesar de estabilidade dimensional; o benchmark não pode presumir que a fonte visual estava completa.
3. **Heróis y=361–736, 1040–1440, 1514–1948, P1:** produto iPhone 18 Pro, Duo e os dois relógios ainda não coincidem em escala/recorte/posições. Títulos, subtítulos e CTAs são textos simples, não os botões da fonte; há colisão de texto sobre os relógios.
4. **Rodapé y=4503–5261:** falta a densidade de notas, cinco colunas de navegação, dados legais e links finais do site. O export deixa grande área vazia.
5. **Fonte tipográfica/nav:** o logo Apple é um glifo quadrado no render; fontes e pesos não seguem a pilha observada SF Pro. O fallback precisa ser registrado e a marca reconstruída como SVG/asset exato.

O frame full-page está correto, mas score, cobertura, achados P1 e revisão da fonte reprovam esta versão. Uma próxima versão exigiria novo run e decisão do usuário. Preservar os três ciclos, issues, exports e comparações; nunca mudar score histórico, adicionar um quarto ciclo oculto ou dizer que o design foi aprovado.
