# Revisão final — GitHub Kaio — ciclo 1

- Revisor: orquestrador principal (Codex)
- Score visual determinístico atribuído: **93,96/100**; cobertura **88,15%**.
- Gate de imagem: PASS; gate de fidelidade da fonte: **FAIL**; decisão: **refatorar, não aprovar**.
- Fonte: `source/reference.png` (captura completa 1440×1807).
- Export: `design/exports/home/1440x1807-cycle1.png` (composição editável).
- Comparações: `cycles/cycle-1/home-side-by-side-annotated.png`, `home-overlay.png`, `home-heatmap.png`.

## Problemas certeiros para o ciclo 2

1. **Header, y=0–73, largura total:** o export usa navegação antiga `Search or jump / Pull requests / Issues`, enquanto a fonte mostra header preto com GitHub mark, `Platform / Solutions / Resources / Open Source / Enterprise / Pricing`, busca e `Sign in / Sign up`. Recriar texto/ícones/posições reais.
2. **Identidade e sidebar, x=100–408, y=112–921:** o export usa fluidicon e nome/bio inventados. Usar a foto do Kaio e o conteúdo visível da fonte: `Kaio Silva Baleeiro de Jesus`, `kaio-baleeiro`, `Estudante de Tecnologia`, followers, achievement e highlights. Manter essa coluna até a região de repos.
3. **Abas e README, x=432–1328, y=73–635:** faltam a navegação de perfil acima do conteúdo e o card `kaio-baleeiro / README.md` com título `Oláá!! Eu sou o Kaio 😁`, bullets, links e grade de contribuições. O export só mostra perfil horizontal vazio nesse espaço. Recriar elementos editáveis e usar assets exatos onde houver.
4. **Repositórios, x=432–1328, y=665–1037:** os seis cards do export têm nomes/descrições inventados. Usar os seis cards reais da captura (`projeto-leitura-de-dados`, `projeto-estoque`, `bootcamp-react`, `pipeline-spring-boot-azure`, `kaio-baleeiro`, `code-grafos`) com suas linguagens, badges e descrição quando observada.
5. **Contribuições e atividade, x=432–1328, y=1080–1695:** a fonte contém card mensal com 50 contribuições, timeline de setembro/2026 e seletor de anos; o export reduz isso a uma grade colorida repetitiva e uma área vazia. Reconstruir densidade, copy e calendário da captura sem preencher todas as células de verde.
6. **Rodapé, y=1730–1807:** usar links e alinhamento do GitHub real; remover a frase meta `Designed as an editable reconstruction...`, que não existe na fonte.

O score heurístico alto é falso positivo causado por grandes áreas brancas e geometria global parecida. Ele não comprova texto correto, assets reais nem correspondência de componentes. A baseline do ciclo 2 é apenas este ciclo 1 da nova versão; não usar score/PNG do benchmark anterior.
