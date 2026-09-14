# Penpot Design Automation

Infraestrutura local compartilhada do Penpot e workflow de criação de telas a
partir de URL, screenshot, código ou briefing sem fonte.

O projeto mantém duas rotas:

- `reproduction`: mapeia uma ou mais fontes e reconstrói telas com fidelidade;
- `directed_creation`: refina um briefing com o usuário, cria versões e só
  formaliza o design system depois da aprovação explícita.

Ambas exigem descoberta em duas etapas, rastreabilidade persistente, construção
via Penpot MCP, trabalho operacional com `gpt-5.6-luna` e validação determinística
por tela e viewport.

## Estrutura

```text
infra/penpot/       Compose, backup, restore, healthcheck e atualização
skills/             Skills versionadas do workflow
scripts/            Captura, mapeamento, MCP e comparação visual
tests/              Testes determinísticos
runs/               Metadados sanitizados; material privado fica ignorado
```

Cada pasta em `skills/` é um pacote [Agent Skills](https://agentskills.io/specification):

```text
skills/<skill>/
├── SKILL.md
├── agents/openai.yaml
├── scripts/          # somente quando a skill executa código
├── references/       # somente para documentação carregada sob demanda
└── assets/           # somente para recursos reutilizáveis reais
```

Diretórios opcionais vazios não são criados. Os `SKILL.md` usam apenas
referências diretas a recursos da própria skill; wrappers locais resolvem a
raiz física do checkout antes de chamar o runtime compartilhado do projeto.

## Instalar a skill global

```sh
./install.sh
```

O instalador cria `~/.agents/skills/penpot-design` como vínculo para a skill
canônica deste repositório. Nenhuma cópia divergente é criada.

Depois, uma solicitação pode começar com `$penpot-design` e uma URL, screenshot,
diretório de código ou briefing. A skill sempre fará as perguntas de escopo e a
pergunta final de adendo/mudança antes de construir.

Na rota de reprodução, o site/runtime e o código fornecidos também funcionam
como biblioteca de assets autorizada. O fluxo inventaria e reutiliza SVGs,
imagens, ícones, logos, fontes e demais arquivos úteis da própria origem antes
de procurar qualquer substituto; procedência e exceções ficam registradas em
`source/assets-manifest.json`.

O cliente MCP de terminal usa `scripts/penpot-mcp.sh`, que carrega a URL local
do arquivo ignorado `infra/penpot/.env` sem colocá-la no histórico de comandos.
Depois de regenerar uma chave na interface do Penpot, copie somente a chave e
execute `scripts/update-mcp-key-from-clipboard.sh`. O utilitário atualiza o
`.env` local e o registro `penpot-design` do Codex sem imprimir a credencial.

## Infraestrutura

```sh
infra/penpot/scripts/up.sh
infra/penpot/scripts/healthcheck.sh
infra/penpot/scripts/backup.sh
infra/penpot/scripts/down.sh
```

Interface: <http://localhost:9001>. O ambiente é local e usa volumes externos
preservados da instalação original do KatiauInvest. Consulte
[`infra/penpot/README.md`](infra/penpot/README.md) antes de restore ou atualização.

## Validação

```sh
python3 -m venv .venv
.venv/bin/pip install -r scripts/requirements.txt
.venv/bin/playwright install chromium
python3 -m unittest discover -s tests -v
python3 scripts/validate_skills.py
```

Uma tela passa somente quando alcança score `>= 90`, cobertura `>= 80%`, não
possui P0/P1 e passa pelo gate estrutural. A saída inclui score, issues,
comparação lado a lado anotada, overlay e heatmap. Depois da construção inicial,
cada versão admite até três ciclos internos de correção.

O CLI normal exige um manifesto completo e aplica os estados/aprovações do
contrato. A captura aceita `--storage-state` para fontes privadas sem persistir
cookies ou o caminho do arquivo. O mapa de fontes suporta URL, screenshot,
arquivo ou diretório de código. Após componentização, gere o inventário real:

```sh
scripts/penpot-inventory.sh \
  --output runs/<run-id>/design/structure-inventory.json \
  --log-path runs/<run-id>/design/penpot-mcp-log.jsonl

.venv/bin/python -m scripts.penpot_validation validate \
  --run-dir runs/<run-id> \
  --cycle 1 \
  --inventory design/structure-inventory.json
```

`DS_REVALIDATING` reprova inventários vazios, componentes destacados ou
ausência dos tokens/componentes/instâncias exigidos. Uma aprovação visual
isolada nunca pula a etapa de design system.

## Lições aprendidas

O espaço canônico é
`35-Lessons-Learned/Projects/penpot-design-automation/` no vault. O orquestrador
consulta o índice no início e no fechamento de cada run. Erros reutilizáveis
recebem contexto, evidência, regra futura e `lesson_refs`; uma lição só muda
para `mitigated` após contramedida e verificação. O utilitário fica em
`skills/penpot-design/scripts/record-lesson.py`.

## Segurança dos registros

Manifestos, decisões, mapas e relatórios sanitizados podem ser versionados.
Capturas privadas, cookies, tokens, dumps, exports do Penpot e demais artefatos
sensíveis permanecem em diretórios ignorados. Nunca coloque a URL autenticada do
MCP em commits, relatórios ou comandos registrados.
