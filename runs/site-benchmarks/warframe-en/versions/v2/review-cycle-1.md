---
type: root-review
status: failed
created: 2026-09-16
source_agent: codex-root
review: true
---

# Revisão oficial — Warframe EN v2 — ciclo 1

## Decisão

**REPROVADO.** Score determinístico **78,94/100**, cobertura **66,1622%**,
vinte regiões P1 e gate estrutural incompleto. O próximo estado é
`REFINEMENT`.

## Revisão visual e semântica do revisor principal

- `y=0..78`: navegação usa ordem, espaçamento, ações e tipografia diferentes
  da fonte; falta reproduzir o menu completo, `PLAY FREE NOW` e `LOG IN`.
- `y=78..1614`: o herói foi substituído por uma composição diferente. A fonte
  usa o key art vermelho, o personagem central, CTAs e dois cards editoriais;
  o export usa logotipo gigante e apenas um card deslocado.
- `y=1614..2799`: `NEWS & UPDATES` está praticamente vazio. Faltam o fundo
  decorativo, título, quatro cards, textos e CTA.
- `y=2799..3984`: `SHOP WARFRAME` conserva somente placeholders e alguns
  retângulos. Faltam imagem principal, painel de produto, faixa de coleção e
  cards com os assets first-party corretos.
- `y=3984..4400`: `PRIME RESURGENCE` está vazio e deve reproduzir banner,
  personagens, copy e CTAs.
- `y=4400..5052`: `PLAYER GUIDES & TOOLS` contém apenas um placeholder; faltam
  três cards completos, imagens, descrições e ações.
- `y=5052..5837`: comunidade, links legais, plataformas, copyright e
  classificação estão vazios.

## Correção exigida no ciclo 2

1. Preencher todas as nove seções, usando os assets first-party já
   catalogados e mantendo cada bloco editável.
2. Priorizar os P1 de página inteira em `y=80..1398`, `y=1613..2625` e
   `y=4009..4403`, depois corrigir os cards e banners localizados.
3. Fazer a hierarquia, a ordem e a copy seguirem a captura aprovada; não usar
   conteúdo genérico como substituto.
4. Completar o inventário estrutural com `component_instances`,
   `detached_instances`, `styles` e `required_component_instances`.
5. Preservar o frame 1440×5837 e o overflow horizontal acidental documentado.

## Evidências

- `cycles/cycle-1/score.json`
- `cycles/cycle-1/issues.json`
- `../../analysis/v2-cycle-1-home-side-by-side-annotated.png`
- `../../analysis/v2-cycle-1-home-overlay.png`
- `../../analysis/v2-cycle-1-home-heatmap.png`
