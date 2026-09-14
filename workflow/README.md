# Penpot Design Automation workflow

Este diretório define o contrato operacional das skills versionadas em `../skills`.
O workflow transforma uma origem (URL, screenshot, código, combinação dessas fontes)
ou um briefing sem origem em telas estáticas no Penpot, com componentes, tokens,
validação visual e entrega rastreável.

## Entradas e rotas

- **Reprodução (`reproduction`)**: uma ou mais fontes visuais/técnicas. A origem é
  registrada antes da construção e divergências entre fontes exigem uma pergunta
  explícita ao usuário.
- **Criação dirigida (`directed_creation`)**: não há fonte. O briefing é refinado
  em diálogo e, depois da aprovação formal do briefing, torna-se a referência da
  primeira versão. Feedback do usuário pode gerar rodadas ilimitadas; cada versão
  ainda passa pelo limite interno de três ciclos de correção.

## Leitura recomendada

1. `CONTRACT.md`: invariantes e critérios de aceite.
2. `STATE-MACHINE.md`: estados, transições e artefatos obrigatórios.
3. `ARTIFACTS.md`: nomes, localizações e campos mínimos dos registros.
4. `SCORING.md`: score determinístico, gates e formato dos achados.
5. `QUESTIONS.md`: questionário mínimo e análise de ambiguidades.
6. `DELEGATION.md`: contrato executável de subagentes Luna e falha segura.

Os scripts referenciados são implementados em `../scripts`. Use o wrapper
`../scripts/penpot-mcp.sh` para carregar a configuração MCP local ignorada e o
pacote `python3 -m scripts.penpot_validation` para captura, mapeamento e score.
