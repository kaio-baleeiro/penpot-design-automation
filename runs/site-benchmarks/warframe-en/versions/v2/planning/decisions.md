# Decisões — Warframe EN v2

## Mantidas da execução anterior

- A URL é a fonte de precedência; screenshots são evidência derivada.
- O viewport de observação é `1440×900`; o frame não deve ser fixado em 900px quando a página finita continua abaixo da dobra.
- O overflow horizontal observado é acidental/contido; o frame raiz permanece em 1440px.
- Assets first-party exatos podem ser reutilizados e devem ter proveniência registrada.
- A captura anterior (cycle 2) ficou `NEEDS_REVIEW` sem score por instabilidade.

## Proposta v2 ainda não aprovada

- Limite vertical: `5837px`, reproduzido com `wait_ms=5000` e `scroll_probes=0`.
- Política: `dynamic_bounded`; `stable:false` até confirmação do usuário e recaptura de handoff.
- Não criar ciclos, score, export de validação ou mutação no Penpot antes dessa confirmação.

## Diagnóstico que deve orientar o próximo build

O último ciclo não falhou por falta de um frame editável, mas porque a origem não ofereceu estabilidade determinística: a altura mudou de 5953 para 5837 entre tentativas e a largura variou em cada amostra. O próximo worker deve preservar a altura aprovada, manter 1440px de largura e validar cada seção contra a captura full-page, sem transformar o screenshot em conteúdo visível.
