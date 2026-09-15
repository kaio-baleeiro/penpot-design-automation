# Decisões — Warframe English

- URL é a fonte de precedência; screenshot Playwright é evidência derivada.
- Reutilizar assets first-party; registrar qualquer asset dinâmico e não persistir cookies/tokens/DOM bruto.
- Devido à instabilidade, manter `stable:false`, `vertical_policy: dynamic_bounded` e `NEEDS_REVIEW`; o board 1440×5953 e export são uma representação visual baseada na captura trial, não uma aprovação da origem.
- Validação: score ≥90, cobertura ≥80, zero P0/P1, até 3 ciclos. Sem aprovação inventada.
- Tentativa de estabilização adicional em 2026-09-15 com `wait_ms=5000` e `scroll_probes=0` também falhou: amostras de largura 1895→1959→2028 px e altura 5837 px. O design foi criado a partir da captura full-page trial para avaliação visual, mas score/aprovação seguem bloqueados até existir captura finita estável e aprovada.
