# Site Arclimtec — Soluções em Climatização

Landing page da **Arclimtec** (climatização industrial, empresarial e residencial). Site estático: só HTML/CSS/JS inline, sem build e sem servidor de aplicação.

## Três direções de design

O cliente pediu três versões bem diferentes entre si. Cada uma vive numa branch própria, já como `index.html`, pronta para deploy:

| Branch | Versão | Linguagem visual |
|---|---|---|
| `v1-engenharia` | Engenharia | Escuro e técnico — Space Grotesk + Inter, cards de vidro fosco, ciano luminoso |
| `v2-editorial` | Editorial clara | Claro e arejado — Fraunces + Manrope, seções numeradas, galeria estilo revista |
| `v3-impacto` | Impacto industrial | Bebas Neue condensada, blocos de cor chapada, letreiro rolante, carrossel de obras |

A branch **`main`** guarda as três lado a lado (`v1-engenharia.html`, `v2-editorial.html`, `v3-impacto.html`) e um `index.html` que serve de página de comparação.

## Estrutura da página (igual nas três)

Hero → serviços (bloco industrial/empresarial + bloco doméstico/residencial, cada um com manutenção **preventiva e corretiva**) → capacidades → projetos em destaque → a empresa → onde já prestou serviço → Instagram → contato.

Em todas elas o fundo é fixo (não rola com a página): uma foto das máquinas em monocromia no azul da logo, translúcida, feita com `background-blend-mode: luminosity` — a foto entra por cima de um sólido azul, então a imagem contribui só a luminosidade e a cor vem da marca.

## Assets

- `assets/logo.png` — logo com fundo transparente (gerada a partir do JPG original)
- `assets/logo-branca.png` — versão branca, para fundos escuros
- `assets/bg-industrial.jpg` — foto usada no fundo fixo
- `assets/p-*.jpg` — fotos de obras, usadas em projetos em destaque

Paleta extraída da própria logo: `#24549C` (azul institucional), `#00A8F0` (ciano), `#006CB4`.

## Rodar localmente

```sh
python3 -m http.server 8081
```

## A preencher antes de publicar

Os campos entre colchetes no HTML aguardam informação do cliente:

- `[Cliente 01]`…`[Cliente 08]` — nomes na seção "onde já prestamos serviço" (confirmar autorização de uso de marca de terceiros)
- `[X] anos` e `[X]+ obras` — tempo de mercado e volume de obras
- `[e-mail comercial]` e `[Razão social / CNPJ]`
- Confirmar se o WhatsApp é o **83 3099-8606** (é número fixo) ou um celular
- Conferir as legendas técnicas das fotos de projetos
