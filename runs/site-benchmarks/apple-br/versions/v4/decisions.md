# Decisões — Apple BR v4

1. Criar uma página nova `Benchmark — Apple BR v4`; não limpar nem sobrescrever v2/v3.
2. Reutilizar os assets first-party observados no DOM e mantidos no manifesto v2, importando-os por URL exata.
3. Manter frame 1440×5261 e 12 regiões visíveis: navegação, 3 heroes, 6 promos, TV+ gallery e footer.
4. O screenshot full-page permanece evidência, não conteúdo visível do frame.
5. Tokens/componentes/instâncias devem ser formalizados pelo root na janela serial do MCP; esta execução construiu a composição editável e importou os assets.
6. Limitação registrada: o export imediato desta sessão renderizou os fills de imagem, mas não os textos; root deve corrigir a causa no MCP antes da revisão.
