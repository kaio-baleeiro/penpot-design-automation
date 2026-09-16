# Penpot Design Automation

Infraestrutura local compartilhada do Penpot e workflow de criação de telas a
partir de URL, screenshot, código ou briefing sem fonte. Este repositório é
executável por Codex, Devin CLI e outros agentes que consigam ler
`AGENTS.md`/`SKILL.md`; não depende de uma cópia proprietária do Codex.

O projeto mantém duas rotas:

- `reproduction`: mapeia uma ou mais fontes e reconstrói telas com fidelidade;
- `directed_creation`: refina um briefing com o usuário, cria versões e só
  formaliza o design system depois da aprovação explícita.

Ambas exigem descoberta em duas etapas, rastreabilidade persistente, construção
via Penpot MCP, trabalho operacional com `gpt-5.6-luna` e validação determinística
por tela e viewport.

## Estrutura

```text
AGENTS.md           Instruções portáteis para Codex, Devin CLI e outros agentes
docs/               Documentação transversal da infraestrutura
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
└── lessons-learned/
    ├── project/      # regras do workflow, versionadas
    └── local/        # memória da máquina, ignorada pelo Git
```

Diretórios opcionais vazios não são criados. Os `SKILL.md` usam apenas
referências diretas a recursos da própria skill; wrappers locais resolvem a
raiz física do checkout antes de chamar o runtime compartilhado do projeto.
Cada pasta de trabalho possui um README próprio. O índice em
`skills/penpot-design/lessons-learned/README.md` conecta aprendizados que
atravessam mais de uma fase.

## Instalar a skill global

Para um clone novo, o caminho recomendado é o bootstrap completo:

```sh
./setup.sh
```

Ele cria o ambiente Python, instala Playwright/Chromium, instala o vínculo da
skill global, gera `.env` local com segredos aleatórios, prepara volumes neutros
e valida o Compose. Depois, suba os serviços com os comandos da seção de
infraestrutura.

Se o Penpot já estiver configurado e você só quiser instalar a skill global:

```sh
./install.sh
```

O instalador cria `~/.agents/skills/penpot-design` como vínculo para a skill
canônica deste repositório. Nenhuma cópia divergente é criada.

Depois, uma solicitação pode começar com `$penpot-design` e uma URL, screenshot,
diretório de código ou briefing. A skill sempre fará as perguntas de escopo e a
pergunta final de adendo/mudança antes de construir.

Entradas aceitas:

- URL pública ou aplicação local em execução;
- print PNG/JPEG de desktop ou mobile;
- diretório ou repositório Git do site/app;
- prompt de criação do zero, sem fonte.

As entradas podem ser combinadas. O fluxo pergunta quais fontes prevalecem,
investiga desktop/mobile e não começa a construir antes da aprovação do escopo.

## Como usar o workflow

1. Leia [`AGENTS.md`](AGENTS.md) e escolha a skill de entrada
   [`penpot-design`](skills/penpot-design/SKILL.md).
2. Suba o Penpot local e confirme o healthcheck:

   ```sh
   infra/penpot/scripts/up.sh
   infra/penpot/scripts/healthcheck.sh
   ```

3. Envie uma URL, screenshot, diretório/repositório do código ou um briefing
   sem fonte. O intake pergunta escopo, precedência, viewports e aprovação; a
   resposta de adendo/mudança é obrigatória.
4. O fluxo cria `runs/<run-id>/`, mapeia a origem, inventaria assets, mede
   viewport/documento/frame e entrega um plano para o worker Luna construir no
   Penpot via MCP.
5. A validação exporta a tela, calcula score por viewport e produz comparação
   lado a lado, overlay, heatmap e issues. Falhas retornam para correção precisa
   por até três ciclos; sem aprovação após o terceiro, o estado é
   `NEEDS_REVIEW`.
6. Depois da sua aprovação formal, a skill de design system cria tokens,
   estilos, componentes e instâncias, revalida as telas e só então empacota a
   entrega.

Para executar fora da raiz, use caminhos absolutos ou os wrappers locais das
skills. O contrato continua o mesmo em qualquer agente:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/validate_skills.py
python3 skills/penpot-design/scripts/record-lesson.py \
  --skill-dir skills/penpot-validate record \
  --title "Falha reproduzível" \
  --lesson "Regra aprendida." \
  --context "Contexto." \
  --evidence "tests/test_..." \
  --future-rule "Como evitar na próxima execução." \
  --kind project \
  --integration "skills/penpot-validate/SKILL.md; tests/test_..."
```

Na rota de reprodução, o site/runtime e o código fornecidos também funcionam
como biblioteca de assets autorizada. O fluxo inventaria e reutiliza SVGs,
imagens, ícones, logos, fontes e demais arquivos úteis da própria origem antes
de procurar qualquer substituto; procedência e exceções ficam registradas em
`source/assets-manifest.json`.

Para desktop, `1440x900` é o viewport padrão de observação e o tamanho mínimo
do frame, não um limite fixo. A captura sempre inclui a página finita inteira:
o screenshot de `1440x900` observa o primeiro viewport, enquanto a imagem
`full_page` mede e preserva todo o conteúdo abaixo da dobra. O design usa essa
altura completa; a largura só cresce quando a origem demonstra
scroll horizontal intencional da página. Overflow acidental ou interno continua
contido, e conteúdo infinito exige um limite reproduzível aprovado.

O cliente MCP de terminal usa `scripts/penpot-mcp.sh`, que carrega a URL local
do arquivo ignorado `infra/penpot/.env` sem colocá-la no histórico de comandos.
Depois de regenerar uma chave na interface do Penpot, copie somente a chave e
execute `scripts/update-mcp-key-from-clipboard.sh`. O utilitário atualiza o
`.env` local e o registro `penpot-design` do Codex sem imprimir a credencial.

## Benchmark público

O diretório [`runs/site-benchmarks/`](runs/site-benchmarks/README.md) contém o
teste reproduzível das fontes Apple Brasil, Warframe English e do perfil GitHub
`kaio-baleeiro`. Cada run inclui perguntas, decisões, frame-spec, mapa de
proveniência, inventário de assets e as imagens públicas de referência,
side-by-side, overlay, heatmap e exports das composições editáveis do Penpot.
Os benchmarks v2 são reconstruções com boards, textos, formas e assets
editáveis no projeto Penpot `Penpot Benchmarks`, arquivo `Site Benchmarks`; a
captura full-page é mantida apenas como referência. O GitHub percorreu três
ciclos (`93,96 → 96,77 → 98,52`): o score visual passou, mas a revisão final de
conteúdo/fonte reprovou. A Apple também percorreu os três ciclos
(`85,93 → 87,30 → 89,57`) e não atingiu score, cobertura nem ausência de P1.
Ambos estão corretamente em `NEEDS_REVIEW`, com side-by-side, overlay e
heatmap de cada ciclo publicados. O Warframe recebeu aprovação explícita para
o limite dinâmico `1440×5837` e também percorreu três ciclos
(`78,94 → 71,94 → 83,34`). Todas as seções ficaram editáveis e visíveis no
ciclo final, mas score, cobertura e fidelidade de fonte reprovaram; o estado
terminal é `NEEDS_REVIEW`, sem quarto ciclo.

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

Cada skill separa suas lições em `lessons-learned/project/` (regras do projeto,
versionadas) e `lessons-learned/local/` (detalhes da máquina, ignorados pelo
Git). O orquestrador consulta o índice compartilhado, registra referências em
`lesson_refs` e só permite que uma lição saia de `active` para `mitigated`
quando a contramedida e sua verificação forem documentadas. O vault mantém as
notas de projeto e referências históricas; a regra executável deve estar no
pacote da skill para viajar junto com o Git. O utilitário fica em
`skills/penpot-design/scripts/record-lesson.py`.

Leia o README da skill antes de cada fase para ver suas lições locais e use o
índice compartilhado quando o erro afetar mais de uma fase. O README de cada
bucket explica seu escopo.

## Segurança dos registros

Manifestos, decisões, mapas, relatórios sanitizados, exports editáveis e imagens
de comparação dos ciclos podem ser versionados. Capturas privadas, cookies,
tokens, dumps, exports operacionais e demais artefatos sensíveis permanecem em
diretórios ignorados. Nunca coloque a URL autenticada do MCP em commits,
relatórios ou comandos registrados.
