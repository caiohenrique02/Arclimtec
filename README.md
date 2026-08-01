# Site Arclimtec — Soluções em Climatização

Landing page da **Arclimtec** (climatização industrial, empresarial e residencial). Site estático: só HTML/CSS/JS inline, sem build e sem servidor de aplicação.

## Versões em avaliação (o que está na `main`)

A `main` guarda só a versão escolhida e as posteriores, lado a lado, com um `index.html` que serve de página de comparação:

| Arquivo | Versão | Linguagem visual |
|---|---|---|
| `v6-definitiva.html` | V6 Definitiva | Escura. Mistura aprovada: hero da V3, duto que esquenta na rolagem, termômetro 24° → 38° → 22° |
| `v7-claro-a.html` | V7 Claro A — Editorial | A V6 recolorida para papel branco puro (`#FFFFFF`), texto azul-marinho, sem a foto no fundo fixo |
| `v7-claro-b.html` | V7 Claro B — Técnico | Mesma recoloração em papel azul-gelo (`#F5F9FD`), contraste e linhas mais marcados |
| `v8-minimal.html` | V8 Minimalista | Releitura enxuta: sem termômetro, cortina ou efeitos de rolagem; Bebas Neue + Barlow, mobile-first |
| `v9-fluxo.html` | V9 Fluxo | A de mais movimento. Uma ideia por tela cheia, partículas de ar em canvas, fundo e cor comandados pela temperatura |
| `v10-prancha.html` | V10 Prancha | Linguagem de projeto: papel quadriculado, cotas, carimbo fixo, desenho técnico que se traça na rolagem, IBM Plex Mono |

As V7 A/B são geradas por `tools/gen_claro.py` a partir da V6 — só cores mudam, a estrutura é a mesma.

### Como a V9 e a V10 funcionam

**V9 Fluxo** — cada `<section>` declara `data-temp` (26° no hero, 38° nos problemas, 22° da virada em diante). O JS interpola entre os centros das seções e escreve `--h` (0 frio → 1 quente), que comanda o fundo, a cor de destaque, a direção das partículas e o termômetro lateral. Dois detalhes que custaram render para acertar: o fundo é **uma cor só** interpolada (cruzar um véu azul e um laranja com opacidade complementar dava um marrom morto no meio), e a virada de cor do destaque é **comprimida** numa faixa curta em torno de `--h` 0.5 — interpolar ciano→âmbar devagar passa por um verde feio.

**V10 Prancha** — os desenhos usam `getTotalLength()` para medir cada traço e completá-los com `stroke-dashoffset` quando a prancha entra na tela. O carimbo do rodapé acompanha qual prancha está no meio da tela, e a mira de CAD só aparece em ponteiro fino (`pointer:fine`).

### Direções anteriores (V1 a V5)

Ficaram nas branches próprias, cada uma já como `index.html` pronta para deploy, e saíram da `main`:

| Branch | Versão | Linguagem visual |
|---|---|---|
| `v1-engenharia` | Engenharia | Escuro e técnico — Space Grotesk + Inter, cards de vidro fosco, ciano luminoso |
| `v2-editorial` | Editorial clara | Claro e arejado — Fraunces + Manrope, seções numeradas, galeria estilo revista |
| `v3-impacto` | Impacto industrial | Bebas Neue condensada, blocos de cor chapada, letreiro rolante, carrossel de obras |
| `v4-termico` | Térmico | A página esfria conforme rola: laranja no topo, azul embaixo, termômetro fixo de 38° a 22° |
| `v5-duelo` | Duelo | Hero com cortina arrastável quente/frio, cartas que viram problema→solução, contadores |

## Estrutura da página (igual em todas)

Hero → serviços (bloco industrial/empresarial + bloco doméstico/residencial, cada um com manutenção **preventiva e corretiva**) → capacidades → projetos em destaque → a empresa → onde já prestou serviço → Instagram → contato.

Nas V1–V3 o fundo é fixo (não rola com a página): uma foto das máquinas em monocromia no azul da logo, translúcida, feita com `background-blend-mode: luminosity` — a foto entra por cima de um sólido azul, então a imagem contribui só a luminosidade e a cor vem da marca.

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

## Deploy (EasyPanel)

O `Dockerfile` é o mesmo em todas as branches — nginx alpine servindo os estáticos, com gzip e cache de 30 dias nas imagens (`default.conf`).

Um serviço por versão, todos apontando para este repo:

| Serviço | Branch |
|---|---|
| `arclimtec-v1` | `v1-engenharia` |
| `arclimtec-v2` | `v2-editorial` |
| `arclimtec-v3` | `v3-impacto` |
| `arclimtec-v4` | `v4-termico` |
| `arclimtec-v5` | `v5-duelo` |

Da V6 em diante nenhuma tem branch própria: ficam na `main`, acessíveis pelo `index.html` de comparação (`/v6-definitiva.html`, `/v7-claro-a.html`, `/v7-claro-b.html`, `/v8-minimal.html`, `/v9-fluxo.html`, `/v10-prancha.html`).
| `arclimtec-comp` (opcional) | `main` |

Configuração em cada serviço: **Build = Dockerfile**, **Dockerfile Path = `Dockerfile`** (vazio também funciona, o padrão é `./Dockerfile`) e **porta 80**.

## A preencher antes de publicar

Os campos entre colchetes no HTML aguardam informação do cliente:

- `[Cliente 01]`…`[Cliente 08]` — nomes na seção "onde já prestamos serviço" (confirmar autorização de uso de marca de terceiros)
- `[X] anos` e `[X]+ obras` — tempo de mercado e volume de obras
- `[e-mail comercial]` e `[Razão social / CNPJ]`
- Confirmar se o WhatsApp é o **83 3099-8606** (é número fixo) ou um celular
- Conferir as legendas técnicas das fotos de projetos
