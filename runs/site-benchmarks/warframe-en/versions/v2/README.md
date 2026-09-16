# Warframe EN — benchmark version 2

Esta versão prepara a reconstrução editável da home de `https://www.warframe.com/en` a partir da captura bounded v2. Ela ainda não está liberada para construção: a origem reportou `stable_after_wait: false` por overflow horizontal incidental e precisa de confirmação humana do limite vertical.

## Estado

- boundary proposta: `1440×5837`, viewport de observação `1440×900`;
- política vertical: `dynamic_bounded`;
- política horizontal: `accidental_overflow` (o frame permanece em 1440px);
- `stable: false`, `build_ready: false`, `requires_user_decision: true`;
- nenhum score, ciclo de validação ou aprovação foi criado nesta versão.

O diagnóstico da execução anterior (`cycle 2`) foi preservado: a origem permaneceu instável, portanto o score ficou bloqueado. A decisão pendente e a recaptura necessária estão em `planning/questions.md` e `planning/decisions.md`.

## Conteúdo

- `source/`: mapa sanitizado e evidências da captura bounded v2;
- `assets/`: inventário de assets first-party, sem cookies, tokens ou payloads privados;
- `planning/`: plano de seções, perguntas e decisões;
- `../source/proposals/bounded-v2/`: proposta original e evidência bruta referenciada.

Após confirmação do limite, o worker Luna deve atualizar o handoff canônico, construir a tela editável no Penpot e então iniciar até três ciclos append-only de validação. O revisor final é responsável pelo score e pelo gate.
