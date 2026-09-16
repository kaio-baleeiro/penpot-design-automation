# Contrato do workflow Penpot

## Princípios obrigatórios

1. A execução começa identificando a rota: `reproduction` ou
   `directed_creation`. Nunca invente uma fonte para a segunda rota.
2. Antes de construir, faça as perguntas mínimas da etapa 1 de
   `$penpot-intake`. Depois de responder, faça obrigatoriamente a pergunta de
   adendo/mudança da etapa 2. Só então analise ambiguidades e faça perguntas
   adicionais quando existir uma decisão material sem resposta.
3. Em `reproduction`, registre e preserve a origem antes da primeira alteração
   no Penpot. URL, screenshot e código podem coexistir. Se discordarem em
   conteúdo, viewport, layout ou comportamento, pare e pergunte qual fonte
   prevalece; não faça escolha silenciosa.
4. Investigue se a origem tem desktop, mobile ou ambos. Pergunte quais
   viewports devem ser entregues. Nunca inferir o segundo viewport sem informar
   a inferência e obter confirmação quando isso mudar o escopo.
5. O usuário autoriza previamente inspecionar e obter SVGs, imagens, ícones,
   logos, fontes e arquivos úteis do site/runtime ou código fornecido. Registre
   a procedência e reutilize o asset exato antes de procurar similares fora da
   origem. Links de recurso referenciados pela própria origem podem ser
   seguidos quando necessários à tela; não amplie isso para busca web alheia ao
   escopo. Assets privados não entram no Git.
6. Em desktop, `1440x900` é o viewport padrão de observação e o tamanho mínimo
   do frame, não um corte obrigatório. A altura acompanha o conteúdo finito e
   estável. A largura só ultrapassa `1440` quando houver evidência de scroll
   horizontal intencional da página raiz; overflow acidental ou de container
   permanece dentro do viewport. Conteúdo infinito/dinâmico exige um limite
   reproduzível aprovado pelo usuário.
7. O escopo inicial é estático: telas, componentes, estilos/tokens e design
   system. Interações/protótipos ficam fora, salvo pedido posterior explícito.
8. Toda tarefa manual de aquisição, análise, construção no MCP, correção,
   extração e validação deve ser delegada com o perfil `gpt-5.6-luna`. Se esse
   modelo não estiver disponível, interrompa com `BLOCKED_MODEL_UNAVAILABLE`;
   não faça fallback para outro modelo.
9. Luna faz a operação e coleta evidências, mas o orquestrador/revisor final
   executa ou confere o avaliador determinístico invocado por `scripts/start-run.sh`
   e pelo wrapper de validação da skill `$penpot-validate`, atribui a pontuação
   oficial e decide a transição. Nenhum agente pode editar fórmula, limiares,
   cobertura ou severidades para aprovar uma tela.
10. Cada tela e viewport precisa atingir score visual **>= 90/100**, cobertura
   mensurável **>= 80%**, e zero achados P0/P1. Uma falha retorna à correção.
11. Após a construção inicial, há no máximo três ciclos internos de
   validação/refatoração (`cycle: 1..3`). Cada ciclo deve produzir achados
   acionáveis por região, causa provável e correção sugerida. Se falhar após o
   terceiro ciclo, estado final `NEEDS_REVIEW`; nunca declarar aprovado.
12. Em `directed_creation`, as rodadas de feedback com o usuário são ilimitadas
    e não contam como ciclos internos até que uma nova versão seja construída.
    A aprovação estética/produto é sempre do usuário; score automático não a
    substitui.
13. Após aprovação formal em qualquer rota, formalize tokens, estilos,
    componentes e regras no design system. Refaça as telas usando instâncias do
    design system e revalide contra a versão aprovada, novamente com os mesmos
    gates. Se a componentização alterar a aparência, corrija até passar ou
    marque `NEEDS_REVIEW`.
14. A entrega deve conter comparação lado a lado, overlay, heatmap e lista de
    issues vinculada à tela/viewport/região. O relatório precisa explicar
    visualmente o que diverge da fonte (ou do protótipo aprovado, na criação
    dirigida).
15. Consulte o índice compartilhado e a pasta de lições da skill antes da
    execução. Quando um erro ou correção produzir uma regra reutilizável,
    registre a lição, adicione seu caminho a `lesson_refs`, implemente a
    contramedida e só marque a lição como `mitigated` depois de uma verificação
    que cubra o caso original.

## Delegação Luna

Cada delegação deve incluir: `worker_model: gpt-5.6-luna`, objetivo observável,
arquivos de entrada, artefatos de saída, restrições desta contract e condição de
parada. O worker não pode alterar o contrato, pesos de score, limiar de 90,
limite de três ciclos ou registros históricos.

O procedimento de criação e verificação do subagente está em
`references/delegation.md`.
Erro de cota ou indisponibilidade do modelo é indisponibilidade real e aciona o
estado bloqueado; o orquestrador não executa a tarefa manualmente como fallback.

## Segurança e rastreabilidade

- Não versionar cookies, tokens, credenciais, dados privados ou capturas
  autenticadas; guardar somente referência sanitizada e apontar o arquivo
  ignorado.
- Não sobrescrever registros de uma rodada. Use identificadores de versão e
  mantenha feedback, score e decisões anteriores.
- Toda mudança que afete escopo, fonte prevalente, viewport ou aprovação deve
  virar uma decisão registrada pelo workflow.
