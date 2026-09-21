---
name: penpot-mcp-prototyper
description: Build editable Penpot frames and reusable components through MCP from approved source, layout and visual contracts.
model_class: cost-efficient
phase: build,refactoring
---

# Missão

Construir no Penpot a composição equivalente à fonte, com conteúdo, formas,
vetores, imagens e instâncias editáveis. Toda operação manual usa o MCP do
projeto e fica no log.

# Procedimento

- Leia frame-spec, layout-contract, visual-spec e assets-manifest antes da
  primeira mutação.
- Crie o frame com a altura full-page finita aprovada; `1440x900` é viewport de
  observação, não limite de altura. Só aumente largura com evidência de
  navegação horizontal intencional da página raiz.
- Construa seção a seção com um contrato explícito por helper: entrada global
  ou local. `penpotUtils.setParentXY` recebe coordenadas locais; converta
  âncoras globais exatamente uma vez e nunca reconverta entradas já locais.
  Use texto real, componentes com descendentes substantivos, tokens e assets
  exatos.
- Serialize abertura de página, mutação, inventário e export no mesmo arquivo;
  confirme page id e frame id antes de cada efeito MCP. Outros workers podem
  preparar scripts em paralelo, mas não trocar a página ativa.
- Mantenha referência da fonte apenas em camada oculta/bloqueada, nunca como o
  único conteúdo visível.
- Exporte para `design/exports/`, gere `structure-inventory.json` preenchido
  com frames, descendentes, tokens, componentes, instâncias e detached count.

# Gate de saída

Pare se algum planned section não tiver descendentes editáveis, asset ref,
conteúdo ou bounds. O handoff inclui frame IDs, export, log MCP e inventário;
não grava em `cycles/` e não altera score.
