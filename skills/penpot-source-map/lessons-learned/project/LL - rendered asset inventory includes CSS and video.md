---
id: source-rendered-asset-inventory
kind: project
status: mitigated
title: Asset inventory must include rendered CSS and video resources
integration: penpot-source-map/SKILL.md; penpot-build/SKILL.md
---

## Failure

O primeiro inventário do Warframe v4 cobriu imagens HTML, mas omitiu o poster
do hero, imagens de cards carregadas por configuração dinâmica e recursos de
vídeo. A construção usou o logo esticado como fundo e perdeu fidelidade.

## Rule

Inventariar a página renderizada por seção: `<img>`, SVG inline/externo,
background computado, pseudo-elemento, `video` poster/source, fontes, sprites e
URLs de configuração/runtime. Uma lista de `<img>` não prova prontidão.

## Countermeasure

Registrar cada recurso em `source/assets-manifest.json`, ligar o `asset_id` ao
plano e bloquear fallback silencioso. Se o frame congelado de vídeo não puder
ser recuperado, registrar a divergência entre screenshot e poster.

## Verification

O ciclo 2 do Warframe v4 substituiu o logo esticado pelo poster oficial e
incorporou as três imagens exatas dos guias; a limitação do frame de vídeo
permaneceu explícita na validação, sem aprovação falsa.
