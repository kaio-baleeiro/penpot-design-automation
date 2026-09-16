# Inventário de origem

| source_id | tipo | localização | evidência | confiança |
|---|---|---|---|---:|
| `src-url-apple-br` | URL pública | `https://www.apple.com/br/` | captura full-page e âncoras DOM históricas | 0.90 |
| `src-full-page-apple-br-v2` | screenshot full-page | `source/reference-full-page.png` | 1440×5261, viewport 1440×900 | 0.98 |

## Seções medidas

Nav `0–44`; iPhone 18 Pro `44–736`; iPhone Duo `748–1440`; Apple Watch
Series 12 `1452–2144`; promo row 1 `2156–2736`; promo row 2 `2748–3328`;
promo row 3 `3340–3920`; TV gallery `3932–4503`; footer `4503–5261`.

Oito pixels de gutter entre blocos e 12px entre tiles são intencionais. A
largura raiz permanece 1440: os 5748px medidos anteriormente são overflow de
mídia fora do canvas, não navegação horizontal do site.

## Diagnóstico usado como insumo

O ciclo 3 marcou P1 em y=370, 1040, 1597, 2144, 2640, 2736, 3340, 3932 e
footer, com score 80.27 e cobertura 69.80%. O plano v2 endereça essas regiões
por seção, conteúdo real e assets first-party; nenhum score histórico é editado.
