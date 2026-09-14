# Lições aprendidas

O conteúdo durável pertence ao vault compartilhado, nunca a uma pasta paralela
do repositório:

```text
35-Lessons-Learned/Projects/penpot-design-automation/
```

## Quando registrar

Registre ou atualize uma lição quando houver erro reproduzível, suposição
incorreta, regressão, fraqueza de segurança, incompatibilidade de ferramenta,
falha repetida de validação ou correção do usuário que deva alterar execuções
futuras. Um erro transitório sem valor reutilizável pode ficar apenas no log.

## Ciclo de superação

1. Pesquise o índice e as notas existentes antes de criar outra.
2. Registre contexto, evidência identificável e uma regra futura verificável.
3. Adicione a wikilink da lição a `lesson_refs` no manifesto e no relatório do
   run afetado.
4. Implemente a contramedida em instrução, script, teste ou gate.
5. Verifique a contramedida com um caso que teria capturado o erro original.
6. Somente então altere a lição de `active` para `mitigated` e documente a
   verificação. Se a prova falhar, mantenha `active`.

Use `scripts/record-lesson.py record ...` para uma nova nota e
`scripts/record-lesson.py resolve ...` depois da verificação. O utilitário
deduplica por nome, restringe a escrita ao espaço canônico e nunca sobrescreve
uma lição existente durante `record`.

Promova uma lição para `35-Lessons-Learned/Patterns/` apenas quando houver
evidência de que ela se aplica além deste projeto. No run, guarde somente a
referência; não copie o texto da nota.
