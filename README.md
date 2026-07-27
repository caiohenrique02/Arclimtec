# Site Arclimtec — Soluções em Climatização

Landing page da **Arclimtec** (climatização industrial, empresarial e residencial). Site estático: só HTML/CSS/JS inline, sem build e sem servidor de aplicação.

## Cinco direções de design

O cliente pediu três versões bem diferentes entre si e, depois, mais duas em cima da V3 com a leitura térmica (laranja = o problema do ar quente, azul = a Arclimtec) e mais movimento. Cada uma vive numa branch própria, já como `index.html`, pronta para deploy:

| Branch | Versão | Linguagem visual |
|---|---|---|
| `v1-engenharia` | Engenharia | Escuro e técnico — Space Grotesk + Inter, cards de vidro fosco, ciano luminoso |
| `v2-editorial` | Editorial clara | Claro e arejado — Fraunces + Manrope, seções numeradas, galeria estilo revista |
| `v3-impacto` | Impacto industrial | Bebas Neue condensada, blocos de cor chapada, letreiro rolante, carrossel de obras |
| `v4-termico` | Térmico | A página esfria conforme rola: laranja no topo, azul embaixo, termômetro fixo de 38° a 22° |
| `v5-duelo` | Duelo | Hero com cortina arrastável quente/frio, cartas que viram problema→solução, contadores |

A branch **`main`** guarda todas lado a lado (`v1-engenharia.html` … `v5-duelo.html`) e um `index.html` que serve de página de comparação.

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
| `arclimtec-comp` (opcional) | `main` |

Configuração em cada serviço: **Build = Dockerfile**, **Dockerfile Path = `Dockerfile`** (vazio também funciona, o padrão é `./Dockerfile`) e **porta 80**.

## A preencher antes de publicar

Os campos entre colchetes no HTML aguardam informação do cliente:

- `[Cliente 01]`…`[Cliente 08]` — nomes na seção "onde já prestamos serviço" (confirmar autorização de uso de marca de terceiros)
- `[X] anos` e `[X]+ obras` — tempo de mercado e volume de obras
- `[e-mail comercial]` e `[Razão social / CNPJ]`
- Confirmar se o WhatsApp é o **83 3099-8606** (é número fixo) ou um celular
- Conferir as legendas técnicas das fotos de projetos
