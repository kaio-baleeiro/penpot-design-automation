# Lições aprendidas

O conteúdo operacional durável pertence ao bucket `project/` em
`lessons-learned/` da skill que exibiu o problema. O bucket irmão `local/`
guarda apenas memória da máquina e é ignorado pelo Git. O índice transversal fica em
`skills/penpot-design/lessons-learned/`; o vault pode manter uma referência de
projeto, mas não é necessário para que outro agente execute a regra a partir do
Git.

## Quando registrar

Registre ou atualize uma lição quando houver erro reproduzível, suposição
incorreta, regressão, fraqueza de segurança, incompatibilidade de ferramenta,
falha repetida de validação ou correção do usuário que deva alterar execuções
futuras. Um erro transitório sem valor reutilizável pode ficar apenas no log.

## Ciclo de superação

1. Pesquise o índice compartilhado e as notas da skill antes de criar outra.
2. Registre contexto, evidência identificável e uma regra futura verificável.
3. Classifique como `kind: machine` (grave em `lessons-learned/local/`, fora do
   Git) ou `kind: project` (grave em `lessons-learned/project/`, integrado ao
   workflow). Lições `project` exigem uma referência explícita de integração.
4. Adicione uma referência relativa da lição a `lesson_refs` no manifesto e no
   relatório do run afetado.
5. Implemente a contramedida em instrução, script, teste ou gate quando for
   `kind: project`.
6. Verifique a contramedida com um caso que teria capturado o erro original.
7. Somente então altere a lição de `active` para `mitigated` e documente a
   verificação. Se a prova falhar, mantenha `active`.

Use `scripts/record-lesson.py --skill-dir skills/<skill> record ... --kind
project|machine` para uma nova nota e `... resolve ... --kind project|machine`
depois da verificação. O utilitário deduplica por nome, restringe a escrita ao
pacote da skill e nunca sobrescreve uma lição existente durante `record`.

Promova uma lição para `35-Lessons-Learned/Patterns/` apenas quando houver
evidência de que ela se aplica além deste projeto. No run, guarde somente a
referência; não copie o texto da nota.
