# Site Arclimtec — Soluções em Climatização

Landing page da **Arclimtec** (climatização industrial, empresarial e residencial). Site estático: só HTML/CSS/JS inline, sem build e sem servidor de aplicação.

## O que está na `main`

A `main` é o site definitivo: um `index.html` só, sem tela de escolha e sem barra
pra alternar entre propostas. É a **V15 C** — a V13 Capa B (hero com divisor
arrastável entre o render isométrico do prédio e o mesmo prédio em desenho
técnico) com a foto aérea da cobertura ocupando, em "Quem somos", o lugar que
era da logo grande.

As outras duas propostas pra foto aérea (V15 A, faixa entre seções; V15 B, foto
08 do carrossel), a tentativa de hero em foto (V14) e a página de comparação
das cinco continuam na branch `v15-aerea`, como registro do que não foi
escolhido. A capa A da V13 segue em `v13-capa-a`, e as versões anteriores
(V1 a V12) em branches próprias — ver "Direções anteriores" mais abaixo.

### O que a V15 mudou

A arte que veio pra hero (`hero-vista-aerea.jpg`, hoje só na branch `v15-aerea`) não é foto e sim um
banner fechado 1280x720: já traz logo, headline e os três serviços embutidos em
pixel, que o site repete em volta. Cortando, comia o texto da arte; sem cortar,
sobrava faixa — por isso a V14 (hero em foto) foi descartada.

A foto de drone limpa saiu da metade direita dessa arte, foi carimbada pelo
`tools/marca_dagua.py` como as outras sete (`assets/p-aerea-casa-maquinas.jpg`,
original em `tools/fotos-originais/`) e entrou em "Quem somos": mais prova de
obra, menos marca repetida — a logo colorida já aparece no topo e no rodapé. A
legenda fica numa barra de degradê no rodapé da foto, parando antes da marca
d'água do canto.

### O que a V13 mudou

Parte da V12 B e mexe só na capa do hero:

- **Divisor arrastável** entre as duas imagens da capa, em vez de mostrar as duas fixas. As duas imagens são registradas uma sobre a outra (mesmo tamanho, mesma posição e escala do prédio) e recebem o mesmo degradê e o mesmo filtro, então o divisor não marca nem degrau de tom nem salto de posição.
- **Prédio inteiro no lugar da foto de obra**: o render isométrico mostra o sistema completo — condensadoras na cobertura, prumadas e rede dutada nos pavimentos.
- Duas propostas pro que o divisor revela: a **planta baixa do pavimento** (Capa A, na branch `v13-capa-a`) ou o **mesmo prédio em desenho técnico** (Capa B, escolhida — é o que está na `main`).

### O que a V12 B/C mudam (retificações do cliente por WhatsApp, 13–17/08)

Partem da V12 A (que por sua vez parte da V11 A) e aplicam, nessa ordem:

- **Hero reorganizado**: o texto de apresentação e a capa (foto da obra + planta do projeto) viraram uma única seção de duas colunas — a foto já aparece na primeira tela, sem precisar rolar. No celular a foto vem primeiro, o texto embaixo (`order:-1` no grid).
- **Planta real**: o SVG placeholder da planta foi trocado por `p-planta-projeto.jpg`, um desenho técnico (blueprint) da rede dutada gerado a pedido do cliente (o arquivo saiu da `main` na limpeza da V15 C; segue nas branches da V12 em diante).
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

### Direções anteriores (V1 a V13 A)

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
| `v12-continuo-b` (na `main` até a V13) | V12 B — Escura | Degradê contínuo do branco ao azul-marinho, foto do galpão fixa ao fundo; base da V13 |
| `v13-capa-a` | V13 A — Capa com planta baixa | Igual à `main`, só que o divisor da capa revela a planta baixa do pavimento |

As V7 A/B foram geradas por `tools/gen_claro.py` a partir da V6 — só cores mudam, a estrutura é a mesma.

## Estrutura da página

Hero (texto + capa obra/planta) → cano/marquee → serviços (bloco industrial + bloco doméstico, cada um com manutenção **preventiva e corretiva**) → grade de 8 serviços → fotos dos equipamentos (carrossel automático) → quem somos → clientes → rodapé.

## Assets

- `assets/logo.png` — logo colorida com fundo transparente
- `assets/logo-branca.png` — versão branca, para fundos escuros (usada na V12 B)
- `assets/bg-industrial.jpg` — foto de fundo das direções antigas (V1–V3); nenhuma página da `main`
  usa, mas o `tools/gen_claro.py` referencia, então fica
- `assets/logo.jpg` — logo original do cliente, com fundo branco; é a entrada do `tools/logo_prep.py`,
  que gera a `logo.png` e a `logo-branca.png`. Também não vai pra página nenhuma
- `assets/p-dutos-galpao.jpg` — foto de fundo fixa da V12 B/C e uma das fotos do carrossel
- `assets/p-capa-predio-render.jpg` — render isométrico do prédio com o sistema por inteiro; é a primeira imagem da capa do hero
- `assets/p-capa-predio-tecnico.jpg` — o mesmo prédio em desenho técnico, revelado pelo divisor da capa.
  Está no mesmo tamanho (1329×904) e com o prédio na mesma posição e escala do render, pra o divisor
  funcionar como raio-X: a linha do desenho cai exatamente em cima da aresta da foto. A planta baixa
  que vinha no canto superior direito foi apagada — só existia deste lado e aparecia do nada ao arrastar.
- `assets/p-aerea-casa-maquinas.jpg` — vista aérea da cobertura, em "Quem somos" desde a V15 C
- `assets/p-*.jpg` — demais fotos de obras, usadas no carrossel de equipamentos. As 7 do carrossel
  saem carimbadas com a marca d'água da logo por `tools/marca_dagua.py`; os arquivos limpos ficam
  em `tools/fotos-originais/`, que o `Dockerfile` não copia

Fotos que só as versões antigas usavam saíram da `main` na V15 C — `hero-vista-aerea.jpg`,
`p-planta-projeto.jpg`, `p-capa-planta-baixa.jpg`, `p-rede-dutada-obra.jpg` e
`p-condensadoras-telhado.jpg` (812 KB no total, que o `Dockerfile` copiava pra imagem à toa).
Cada uma continua nas branches das versões que a usam, e no histórico.

Paleta extraída da própria logo: `#24549C` (azul institucional), `#00A8F0` (ciano), `#48C6FF` (ciano claro).

## Rodar localmente

```sh
python3 -m http.server 8081
```

## Deploy (EasyPanel)

O `Dockerfile` é o mesmo em todas as branches — nginx alpine servindo os estáticos, com gzip e (no `default.conf` da `main`) `no-cache`, pra proposta em revisão nunca abrir com imagem velha. Virando produção pra valer, dá pra voltar o cache longo nas imagens — tem a nota no próprio `default.conf`.

Um serviço por versão, todos apontando para este repo:

| Serviço | Branch |
|---|---|
| `arclimtec-v1` | `v1-engenharia` |
| `arclimtec-v2` | `v2-editorial` |
| `arclimtec-v3` | `v3-impacto` |
| `arclimtec-v4` | `v4-termico` |
| `arclimtec-v5` | `v5-duelo` |
| `arclimtec` | `main` — site definitivo (V15 C) |

As demais versões (`v6-definitiva` … `v13-capa-a`, `v14-hero-foto`, `v15-aerea`) também têm branch própria, mesmo padrão, caso seja preciso reativar alguma pra deploy.

Configuração em cada serviço: **Build = Dockerfile**, **Dockerfile Path = `Dockerfile`** (vazio também funciona, o padrão é `./Dockerfile`) e **porta 80**.

## A preencher antes de publicar

Os campos entre colchetes no HTML aguardam informação do cliente:

- `[Razão social / CNPJ]` no rodapé
- Confirmar se o WhatsApp é o **83 3099-8606** (é número fixo) ou um celular
- Conferir as legendas técnicas das fotos de projetos
