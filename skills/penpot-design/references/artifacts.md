# Artefatos e convenções do workflow

Cada execução deve viver em `runs/<run-id>/` (ou no diretório equivalente que o
projeto configurar) e usar estes nomes estáveis:

```text
runs/<run-id>/
  manifest.json
  questions.md
  decisions.md
  source/source-map.json
  source/source-inventory.md
  source/raw/                 # capturas privadas, sempre ignoradas
  source/sanitized/           # mapas/recortes revisados que podem ser versionados
  briefing/brief-v001.md      # somente directed_creation
  design/plan.json
  design/penpot-mcp-log.jsonl
  design/structure-inventory.json
  design/exports/<screen>/<viewport>.png
  cycles/cycle-1/score.json
  cycles/cycle-1/issues.json
  cycles/cycle-1/<screen>-side-by-side-annotated.png
  cycles/cycle-1/<screen>-overlay.png
  cycles/cycle-1/<screen>-heatmap.png
  feedback/feedback-v001.md
  approvals/approval-v001.md
  delivery/report.md
  delivery/manifest.json
```

## Campos mínimos do manifesto

```json
{
  "schema_version": "1.0",
  "run_id": "stable-id",
  "route": "reproduction|directed_creation",
  "state": "INTAKE_PENDING",
  "worker_model": "gpt-5.6-luna",
  "source_refs": [],
  "target_viewports": [],
  "screens": [],
  "validation_cycle": 0,
  "max_validation_cycles": 3,
  "user_review_round": 0,
  "lesson_refs": [],
  "approval": {"briefing": false, "design": false, "design_system": false},
  "intake": {
    "initial_questions_completed": true,
    "addendum_question_completed": true,
    "ambiguity_analysis_completed": true,
    "evidence": ["questions.md", "decisions.md"]
  },
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601"
}
```

O CLI é estrito: além dos campos acima, `target_viewports` e `screens` devem ser
não vazios, `worker_model` deve ser exatamente `gpt-5.6-luna`, e a evidência das
duas perguntas mais a análise de ambiguidades deve existir. Exemplo executável:

```json
{
  "schema_version": "1.0",
  "run_id": "stable-id",
  "route": "reproduction",
  "mode": "source",
  "state": "VALIDATING",
  "worker_model": "gpt-5.6-luna",
  "source_refs": [{"source_id": "src-1", "type": "screenshot"}],
  "target_viewports": [{"width": 1440, "height": 900}],
  "screens": [
    {
      "id": "home",
      "viewport": {"width": 1440, "height": 900},
      "source": "source/raw/home-1440x900.png",
      "penpot_export": "design/exports/home/1440x900.png"
    }
  ],
  "validation_cycle": 0,
  "max_validation_cycles": 3,
  "user_review_round": 0,
  "lesson_refs": [],
  "approval": {"briefing": true, "design": false, "design_system": false},
  "intake": {
    "initial_questions_completed": true,
    "addendum_question_completed": true,
    "ambiguity_analysis_completed": true
  }
}
```

Inicialize o run com `scripts/start-run.sh --run-dir <run-dir> --manifest
<manifest.json>` e valide com o wrapper da skill `$penpot-validate`. O arquivo
de cada ciclo é imutável; use o
próximo número de ciclo para uma nova tentativa.

`source-map.json` deve guardar, por fonte, tipo, localização, timestamp,
hash, viewport, páginas/rotas, evidências observadas, limitações, nível de
confiança, relação com outras fontes e decisões de precedência. Cada item
observado precisa apontar para um arquivo ou âncora (URL, seletor, linha,
coordenada ou recorte).

O CLI escreve `issues.json` como `{run_id, cycle, issues}`. Cada issue
determinístico possui `id`, `screen`, `viewport`, `severity` (`P0`..`P3`),
`title`, `detail`, `bounds`, `status` e `source`; a interpretação Luna deve
registrar `root_cause` e `fix` no handoff/relatório sem editar a evidência
imutável.

`feedback/` é append-only. Cada feedback inclui a versão a que se refere, texto
do usuário, interpretação, alterações solicitadas, ambiguidades abertas e
confirmação de encerramento.

`approvals/` também é append-only. Cada nota registra etapa (`briefing`,
`design` ou `design_system`), versão aprovada, decisão, declaração do usuário,
timestamp e referência à mensagem/decisão. Atualize os flags do próximo
manifesto versionado somente quando existir esse registro; score não cria
aprovação automaticamente.

`lesson_refs` é sempre uma lista. Começa vazia e recebe wikilinks para lições
canônicas em `35-Lessons-Learned/Projects/penpot-design-automation/` quando um
erro ou correção produzir uma regra futura. O run nunca duplica o corpo da nota.

Em `DS_REVALIDATING`, o inventário estrutural é obrigatório e precisa conter
tokens, componentes, instâncias e estilos não vazios, além de zero instâncias
destacadas. Passe-o ao CLI com `--inventory`.
