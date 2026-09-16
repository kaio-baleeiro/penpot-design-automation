# Decisões — Apple Brasil v2

1. `source/raw/full-page/source.png` é a referência histórica integral; uma
   cópia pública sanitizada é mantida nesta versão como
   `source/reference-full-page.png`.
2. O documento visível mede 1440×5261. A medição bruta reportou largura maior
   por mídia off-canvas; a política aprovada é `horizontal_policy:
   accidental_overflow`, frame de 1440.
3. O ciclo 3 anterior não foi aprovado. Seus dez P1 e métricas são diagnóstico
   de entrada, não devem ser sobrescritos nem convertidos em score v2.
4. A construção deve usar os 12 assets first-party enumerados no manifesto e
   representar as seções completas, incluindo TV gallery e footer.
5. A pontuação oficial será atribuída pelo revisor final, usando o avaliador
   determinístico após cada ciclo Luna. Abaixo de 90 ou com P0/P1, retorna para
   refatoração direcionada; após o terceiro ciclo, `NEEDS_REVIEW`.
