# Revisão final — Apple BR — ciclo 2

- Revisor: orquestrador principal (Codex)
- Score visual determinístico atribuído: **87,30/100**; cobertura **72,37%**.
- Gates: score FAIL, cobertura FAIL, múltiplos P1; estrutura editável PASS.
- Decisão: **última refatoração interna no ciclo 3**, sem aprovar.
- Comparações: `cycles/cycle-2/home-side-by-side-annotated.png`, `home-overlay.png`, `home-heatmap.png` (cópias públicas em `../../analysis/v2-cycle-2-*`).

## Melhorias verificadas

O grid promocional passou a ter duas colunas e seis tiles; os seis assets da galeria TV foram adquiridos. A pontuação subiu 1,37 ponto e a cobertura 1,06 ponto percentual. Os exports e mutações foram registrados pelo wrapper MCP sem sobrescrever o ciclo 1.

## Handoff certeiro para o ciclo 3

1. **TV y=3932–4455, P1 largura total:** a fonte mostra um carousel com um card principal largo (`Mayday`) e previews laterais, controles/dots e texto sobre imagem. O export tem seis posters iguais e estreitos em uma linha. Reposicionar/recortar os assets existentes para a hierarquia e proporções da captura; manter overlay text/control editável.
2. **Heróis, P1:** iPhone 18 Pro artwork x=232–1220/y=370–661, Duo x=418–1021/y=1040–1440, Watch Series 12 nos dois relógios y=1598–1927. Os image fills originais ainda aparecem aproximadamente 2–3× menores/mais estreitos. Investigar `fillImage` contain/cover ou usar retângulos de imagem maiores, centralizados e clipados pelo board de seção; ajustar por bounds da fonte, sem deformar produto.
3. **Promoções P1 y=2156–3920:** as tiles agora têm posições plausíveis mas o conteúdo da captura não coincide. Há diferenças significativas x=726–1428/y=3340–3920 e y=2156–2736. Reconciliar cada quadrante com a referência fixa; não presumir que `stable:true` dimensional signifique que os lazy assets estavam visualmente prontos no snapshot. Registrar tiles da origem que ainda estavam em branco como limitação, não preencher um benchmark diferente sem decisão.
4. **Typography/nav/CTAs:** glifo Apple aparece quadrado; os CTAs estão como links azuis, sem botões azul sólido/contornado. Textos em certas tiles ficam ilegíveis sobre imagem escura. Usar logo SVG/wordmark exato quando acessível e formas/botões editáveis nas posições da fonte.
5. **Footer y=4503–5261:** ainda restam centenas de pixels vazios onde a origem tem notas legais, cinco colunas e rodapé Brasil. Reconstruir todo o texto/hierarquia visíveis, sem substituir por uma única nota e 13 palavras.

Não mudar score, referência ou políticas de frame durante o ciclo 3. Se a última tentativa não atingir score ≥90, coverage ≥80 e zero P0/P1 — ou se a fonte fixa continuar visualmente incompleta — entregar `NEEDS_REVIEW` com causas, nunca um quarto ciclo oculto.
