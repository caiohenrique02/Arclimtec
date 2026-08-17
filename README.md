# Site Arclimtec — Soluções em Climatização

Landing page da **Arclimtec** (climatização industrial, empresarial e residencial). Site estático: só HTML/CSS/JS inline, sem build e sem servidor de aplicação.

## O que está na `main`

A `main` guarda só as duas versões finais, lado a lado, com um `index.html` que serve de página de comparação pro cliente:

| Arquivo | Versão | Linguagem visual |
|---|---|---|
| `v12-continuo-b.html` | V12 B — Escura | Hero com texto e capa (obra+planta) lado a lado já na primeira tela; degradê contínuo do branco até o azul-marinho da marca; foto do galpão fixa e translúcida ao fundo |
| `v12-continuo-c.html` | V12 C — Clara | Mesma estrutura da V12 B, recolorida pra ficar em tons claros do início ao fim — nenhuma seção escurece, nem o rodapé |

Todas as versões anteriores (V1 a V12 A) foram aposentadas pra branches próprias — ver "Direções anteriores" mais abaixo.

### O que a V12 B/C mudam (retificações do cliente por WhatsApp, 13–17/08)

Partem da V12 A (que por sua vez parte da V11 A) e aplicam, nessa ordem:

- **Hero reorganizado**: o texto de apresentação e a capa (foto da obra + planta do projeto) viraram uma única seção de duas colunas — a foto já aparece na primeira tela, sem precisar rolar. No celular a foto vem primeiro, o texto embaixo (`order:-1` no grid).
- **Planta real**: o SVG placeholder da planta foi trocado por `assets/p-planta-projeto.jpg`, um desenho técnico (blueprint) da rede dutada gerado a pedido do cliente.
- **Repaginação "Apple"**: cantos arredondados e sombras suaves em vez de bordas duras (capa, marquee, painel de serviços, cards, carrossel, clientes); botões com hover de elevação suave em vez do efeito "adesivo" deslocado; nav com borda fina em vez de faixa azul grossa.
- **Blocos de serviço (industrial/doméstico) bem mais compactos**: texto de um lado, lista de 2 colunas do outro, em vez de empilhado — ficaram largos e curtos.
- **Carrossel de fotos**: cards menores (3 por vez no desktop), e agora **anda sozinho** automaticamente, pausando quando o usuário interage.
- **Quem somos**: logo grande trocada de branca pra colorida (mesma do topo), sem a caixa/glow que tinha antes.
- **Rodapé**: botão de WhatsApp em verde (diferente do azul usado no resto do site).
- **V12 B** mantém o degradê indo até `--azul-deep`/`--azul-night`, com a foto de fundo (`assets/p-dutos-galpao.jpg`) fixa (`position:fixed`, não rola nem se repete) e um overlay translúcido de transição longa por cima.
- **V12 C** é a V12 B com o mesmo overlay só que preso em tons claros (branco → azul bem claro, nunca passa de `--frio`/`--azul`) — isso obrigou a rever todo texto/ícone que assumia fundo escuro (títulos de seção, números da empresa, legendas do carrossel, rodapé) pra usar tinta escura em vez de branca, e a logo do rodapé/"quem somos" virou a colorida (a branca sumiria num fundo claro).

### O que a V12 A mudou (retificações do cliente por WhatsApp, 13/08)

Parte da V11 A (Capa Editorial) e aplicou:

- **Degradê único na página inteira**: o `body` recebe um só `linear-gradient` vertical — branco até ~12%, azul claro (`--frio-2`) no 1/4 da página, passando por `--azul` e chegando no azul mais escuro da marca (`--azul-deep`) na metade, mantido até o rodapé.
- **Cano/marquee**: o duto em pílula da V11 foi trocado pelo cano azul da V6/V7, no fluxo contrário ao da V6.
- **Carrossel de fotos 2 a 2**: setas e bolinhas, cada clique avança uma "página" de 2 fotos.
- **Serviços em pilha**: industrial em cima (tamanho original), doméstico embaixo, reduzido.
- **Logo em "quem somos"**: logo branca grande sobre um brilho radial sutil (V12 B/C substituíram por logo colorida sem glow).
- **V12 B** (nessa época): camada de foto industrial translúcida acompanhando a altura inteira do documento, repetindo verticalmente.

### O que a V11 mudou (pedido do cliente por WhatsApp, 04/08)

As três variações partiam de bases diferentes (V7 A, V7 B e V8) mas aplicavam a mesma lista de mudanças: capa dividida obra+planta (planta em SVG placeholder), duto de ar animado com fileira de chips de serviço, logo maior, título do hero reduzido pela metade, degradê entre seções e estrutura reduzida a 6 seções (apresentação → serviços → fotos → quem somos → clientes → rodapé).

### Direções anteriores (V1 a V12 A)

Todas aposentadas pra branches próprias, cada uma já como `index.html` pronta pra deploy, fora da `main`:

| Branch | Versão | Linguagem visual |
|---|---|---|
| `v1-engenharia` | Engenharia | Escuro e técnico — Space Grotesk + Inter, cards de vidro fosco, ciano luminoso |
| `v2-editorial` | Editorial clara | Claro e arejado — Fraunces + Manrope, seções numeradas, galeria estilo revista |
| `v3-impacto` | Impacto industrial | Bebas Neue condensada, blocos de cor chapada, letreiro rolante, carrossel de obras |
| `v4-termico` | Térmico | A página esfria conforme rola: laranja no topo, azul embaixo, termômetro fixo de 38° a 22° |
| `v5-duelo` | Duelo | Hero com cortina arrastável quente/frio, cartas que viram problema→solução, contadores |
| `v6-definitiva` | V6 Definitiva | Escura. Mistura aprovada: hero da V3, duto que esquenta na rolagem, termômetro 24° → 38° → 22° |
| `v7-claro-a` | V7 Claro A — Editorial | A V6 recolorida para papel branco puro, texto azul-marinho |
| `v7-claro-b` | V7 Claro B — Técnico | Mesma recoloração em papel azul-gelo, contraste mais marcado |
| `v8-minimal` | V8 Minimalista | Releitura enxuta: sem termômetro, cortina ou efeitos de rolagem; mobile-first |
| `v9-fluxo` | V9 Fluxo | A de mais movimento: uma ideia por tela cheia, papel e cor comandados pela temperatura |
| `v10-prancha` | V10 Prancha | Linguagem de projeto: papel quadriculado, cotas, carimbo, desenho técnico que se traça na rolagem |
| `v11-capa-1` | V11 A — Capa Editorial | Capa dividida obra+planta, duto azul animado, 6 seções |
| `v11-capa-2` | V11 B — Capa Técnico | Planta à esquerda em estilo prancha, duto com flanges/rebites |
| `v11-capa-3` | V11 C — Capa Minimalista | Capa num cartão único arredondado, CTA laranja |
| `v12-continuo-a` | V12 A — Degradê contínuo | Base pra V12 B/C, sem a foto real na planta nem a repaginação "Apple" |

As V7 A/B foram geradas por `tools/gen_claro.py` a partir da V6 — só cores mudam, a estrutura é a mesma.

## Estrutura da página (igual nas duas versões atuais)

Hero (texto + capa obra/planta) → cano/marquee → serviços (bloco industrial + bloco doméstico, cada um com manutenção **preventiva e corretiva**) → grade de 8 serviços → fotos dos equipamentos (carrossel automático) → quem somos → clientes → rodapé.

## Assets

- `assets/logo.png` — logo colorida com fundo transparente
- `assets/logo-branca.png` — versão branca, para fundos escuros (usada na V12 B)
- `assets/bg-industrial.jpg` — foto de fundo das direções antigas (V1–V3)
- `assets/p-dutos-galpao.jpg` — foto de fundo fixa da V12 B/C e uma das fotos do carrossel
- `assets/p-planta-projeto.jpg` — blueprint técnico da rede dutada, usado na capa do hero (V12 B/C)
- `assets/p-*.jpg` — demais fotos de obras, usadas no carrossel de equipamentos

Paleta extraída da própria logo: `#24549C` (azul institucional), `#00A8F0` (ciano), `#48C6FF` (ciano claro).

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
| `arclimtec-comp` (opcional) | `main` — comparação V12 B × V12 C |

As demais versões (`v6-definitiva` … `v12-continuo-a`) também têm branch própria, mesmo padrão, caso seja preciso reativar alguma pra deploy.

Configuração em cada serviço: **Build = Dockerfile**, **Dockerfile Path = `Dockerfile`** (vazio também funciona, o padrão é `./Dockerfile`) e **porta 80**.

## A preencher antes de publicar

Os campos entre colchetes no HTML aguardam informação do cliente:

- `[Razão social / CNPJ]` no rodapé
- Confirmar se o WhatsApp é o **83 3099-8606** (é número fixo) ou um celular
- Conferir as legendas técnicas das fotos de projetos
