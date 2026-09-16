# Lições da validação

Registre aqui falhas de score, cobertura, severidade, comparação visual,
frame-spec ou correção. Regras do projeto ficam em `project/`; incidentes da
máquina ficam em `local/` e são ignorados pelo Git. Nunca ajuste fórmula, limiar ou evidência para aprovar
uma tela. Compartilhe regras no [índice transversal](../../penpot-design/lessons-learned/README.md).

Lições `machine` não alteram o avaliador; lições `project` só podem ser
mitigadas após integração e teste do comportamento corrigido.

Quando a representação muda, inicie uma nova versão/run e não herde score de
uma captura incompatível; consulte [baseline precisa representar o mesmo artefato](project/LL%20-%20baseline%20must%20match%20representation.md).
