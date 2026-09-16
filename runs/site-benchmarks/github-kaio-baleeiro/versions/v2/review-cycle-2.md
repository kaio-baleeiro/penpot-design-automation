# Revisão final — GitHub Kaio — ciclo 2

- Revisor: orquestrador principal (Codex)
- Score visual determinístico atribuído: **96,77/100**; cobertura **92,07%**.
- Gate de imagem: PASS; gate de fidelidade e rastreabilidade: **FAIL**; decisão: **uma correção final (ciclo 3), não aprovar**.
- Fonte e bounds: `source/reference.png`, 1440×1807.
- Export: `design/exports/home/1440x1807-cycle2.png`.
- Comparações: `cycles/cycle-2/home-side-by-side-annotated.png`, `home-overlay.png`, `home-heatmap.png`.

## Avanço e problemas restantes

O header e os seis nomes de repositório foram aproximados da fonte. A composição, contudo, ainda se parece com um texto simplificado sobre uma página branca, não com o perfil capturado. O score aumentou porque a imagem-base é majoritariamente branca; isso não é prova de fidelidade.

1. **Sidebar x=100–408, y=112–921:** foto do Kaio, nome, follow, bio, followers, badge e highlights não aparecem no export, embora o inventário declare uma imagem. Investigar se a foto/formas ficaram ocultas, fora do frame ou recortadas por boards; conferir o render, não só a árvore.
2. **README x=432–1328, y=169–636:** falta o contorno do card, o texto real dos bullets, as imagens SVG/snake e a grade de contribuições. O export troca isso por bullets inventados e uma caixa vazia `Contribuições e projetos recentes`. Recriar o conteúdo observável e verificar asset_refs.
3. **Repositórios x=432–1328, y=665–1037:** nomes agora coincidem, mas cards, badges, divisórias e metadata não renderizam; há linguagens e descrições inventadas (por exemplo, `projeto-leitura-de-dados` aparece Python no export e Java na fonte). Usar fonte pixel/section-map para corrigir copy e layouts.
4. **Contribuição x=432–1328, y=1080–1289:** o gráfico da fonte tem meses, dias, escala, contorno e células pequenas; o export tem uma grade grande/randomizada sem o card ou seus rótulos. Corrigir tamanho, posição e cores com dados da captura.
5. **Atividade x=432–1328, y=1313–1693:** timeline, `Created 7 commits in 1 repository`, link `kaio-baleeiro/penpot-design-automation`, `Created 1 repository`, marcador privado, barra e seletor anual faltam. Corrigir esta região sem preencher com texto genérico.
6. **Rodapé y=1730–1807:** falta parte dos links e a marca; alinhar à fonte.

## Gate de rastreabilidade

O `design/penpot-mcp-log.jsonl` contém apenas inicialização/exportação (12 linhas), sem entradas de mutação `execute_code`. Isso impede conferir como os `asset_id` declarados foram aplicados; antes de encerrar o ciclo 3, registrar as mutações pelo wrapper MCP append-only e confirmar a foto no export. Não marcar `embedded_first_party` apenas porque a árvore contém um image fill invisível.

Esta é a última refatoração interna permitida. Se o ciclo 3 ainda falhar em fonte/estrutura apesar de score >=90, terminar `NEEDS_REVIEW` com comparação visual e causas explícitas — nunca alterar a régua para aprovar.
