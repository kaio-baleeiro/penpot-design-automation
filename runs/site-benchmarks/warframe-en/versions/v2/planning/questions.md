# Perguntas pendentes — Warframe EN v2

1. Você aprova o estado bounded reproduzido até `5837px` (incluindo footer e marcas de plataforma) como limite finito deste benchmark?
2. A faixa de consentimento de cookies deve ficar somente na evidência de origem ou também ser reconstruída como overlay opcional?

Sem a resposta à primeira pergunta, a origem permanece `stable:false`, `build_ready:false` e não pode entrar no frame-spec canônico, no Penpot ou em pontuação. A segunda pergunta não bloqueia a tela principal, mas altera o escopo visual da validação.

Depois da aprovação, o fluxo deve recapturar o estado aprovado, registrar hashes e iniciar a reconstrução editável. O revisor final deverá pontuar cada ciclo; score menor que 90% retorna para correção direcionada, no máximo três vezes.
