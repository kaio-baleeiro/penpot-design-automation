# Dimensionamento inteligente de viewport e frame

Viewport e frame representam coisas diferentes. O viewport é a janela usada
para observar o comportamento responsivo; o frame do Penpot representa a
extensão estática que deve ser entregue.

## Regra padrão para desktop

- Comece a inspeção com viewport `1440x900`.
- O frame tem largura mínima `1440` e altura mínima `900`.
- Se o documento finito cresce verticalmente, use altura
  `max(900, document_height)` e capture evidência full-page nas mesmas dimensões.
- Não corte a página no primeiro fold e não fixe a altura em `900` quando houver
  conteúdo estável abaixo dele.

## Overflow horizontal

Expanda o frame além de `1440` somente quando houver evidência de que a página
raiz é intencionalmente horizontal, como canvas, board, timeline, mapa ou faixa
de conteúdo cuja navegação horizontal faz parte da experiência. Nesse caso, use
`max(1440, document_width)` e registre a evidência.

Não expanda o frame raiz quando a largura adicional vier de:

- um elemento quebrado, deslocado ou maior por engano;
- sombra, transformação ou decoração fora dos limites;
- carrossel, tabela, editor ou outro container com scroll próprio;
- conteúdo oculto, off-canvas ou estado não visível.

Nesses casos, mantenha o frame em `1440`, preserve o estado visível do container
e registre seu comportamento. Se a intenção não puder ser provada pela execução,
DOM ou código, trate como ambiguidade material e pergunte antes de alargar.

## Conteúdo dinâmico

Compare pelo menos três amostras: inicial, após estabilização e após duas
sondagens limitadas de scroll quando houver lazy loading. Se largura ou altura
continuarem mudando por paginação ou scroll infinito, não tente materializar
conteúdo ilimitado. Registre o estado, rota e último item visível, proponha um
limite reproduzível e obtenha confirmação do usuário.

A captura de URL usa duas sondagens por padrão. Desative-as apenas quando o
scroll puder disparar uma ação destrutiva ou fora de escopo; registre essa
limitação como evidência incompleta.

`stable_after_wait` mede apenas a estabilidade das dimensões. Antes de congelar
uma referência full-page, faça uma auditoria visual/asset por seção: aguarde e
confirme mídia lazy, SVGs, imagens e fontes, compare com o inventário de assets
e registre qualquer lacuna. Uma captura dimensionalmente estável, mas com
blocos vazios, exige recaptura ou aprovação explícita e não deve ser tratada
como referência completa.

## Registro obrigatório

Para cada tela/viewport, grave em `source/frame-spec.json`:

```json
{
  "schema_version": "1.0",
  "screens": [{
    "screen_id": "home",
    "viewport": {"width": 1440, "height": 900},
    "document": {"width": 1440, "height": 2840},
    "frame": {"width": 1440, "height": 2840},
    "vertical_policy": "finite_document",
    "horizontal_policy": "viewport_bounded",
    "capture_mode": "full_page",
    "stable": true,
    "build_ready": true,
    "requires_user_decision": false,
    "evidence": ["capture.json", "source-full-page.png"]
  }]
}
```

Políticas verticais: `viewport_bounded`, `finite_document` e
`dynamic_bounded`. Políticas horizontais: `viewport_bounded`,
`intentional_page`, `container_overflow` e `accidental_overflow`. Largura
isolada nunca é evidência suficiente para `intentional_page`.

Para `intentional_page`, a captura de referência usa `--frame-bounds` e
`capture_mode: frame_bounds`; `full_page` sozinho não comprova nem captura a
largura além do viewport.

Use valores medidos, não estimativas visuais. Para código sem aplicação
executável, registre a inferência e sua evidência; pergunte quando ela puder
alterar materialmente o tamanho entregue.
