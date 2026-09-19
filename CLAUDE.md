# Contexto pro Claude — site da Arclimtec

Cliente: **Arclimtec Soluções em Climatização**, climatização industrial,
empresarial e residencial em Campina Grande/PB. Instagram @arclimtec.
Diretor: **Daniel Souza da Silva**, 15 anos de mercado. Empresa desde 2012,
mais de 50 projetos de médio e grande porte. CNPJ 33.443.579/0001-16.
Telefone 83 3099-8606 (fixo; confirmar se o WhatsApp é outro número).

Site estático: um `index.html` só, com CSS e JS inline. Sem build, sem
framework, sem servidor de aplicação. Deploy em **EasyPanel** por Dockerfile
(nginx alpine, porta 80), feito pelo Caio pelo painel.

## Regras de trabalho neste repo

- **Não existe deploy automático neste projeto.** "Subir pra main" significa
  push no GitHub e nada mais; quem coloca no ar é o Caio, clicando em
  **Redeploy** no EasyPanel depois. Então: empurrar, avisar que está pronto pro
  redeploy e parar por aí. Não ficar esperando a produção mudar sozinha, e não
  concluir que o deploy "falhou" porque o site ainda serve a versão velha.
- **Sempre `git fetch` antes de editar.** O checkout local costuma ficar vários
  commits atrás do `origin/main`.
- **Não rodar `tools/publish_branches.py`**: ele usa `checkout -B` e **recria**
  as branches de versão, apagando o que estiver nelas.
- Servir local com **`python3 tools/servir.py`** (8085), nunca com
  `python3 -m http.server` direto. O módulo padrão não manda `Cache-Control`,
  então o navegador guarda o HTML e as fotos e mostra a versão velha: em
  18/09/2026 isso custou três rodadas de "não vi a mudança" numa alteração que
  já estava no ar. A 8081 e a 8082 costumam estar ocupadas por outros projetos
  do Caio.
- A hero é um carrossel automático e os slides saem de `tools/hero_slides.py`,
  todos em 1600x900. Foto nova na hero passa por lá antes, senão ela é a única
  que não bate com a caixa e a página muda de altura quando ela entra.
- Fotos de obra novas passam por `tools/marca_dagua.py`: o original limpo vai
  pra `tools/fotos-originais/` e o nome entra na lista `FOTOS`. O script
  recarimba tudo a partir dos originais, nunca por cima de foto já carimbada.
  O Dockerfile não copia `tools/`, então o original sem marca não vai ao ar.
- Toda foto nova precisa do `.webp` irmão (`foto.jpg.webp`), senão ela é a
  única do site que não pega a otimização. `python3 tools/webp.py` gera o que
  estiver faltando ou desatualizado. Ver "WebP" abaixo.
- Escrita: PT-BR direto, sem travessão, sem paralelismo de três, sem slogan de
  agência e sem métrica inventada.

## Estado (16/09/2026)

`main` é o site definitivo, a V16. As versões antigas (V1 a V15) estão cada uma
na sua branch, como registro. Detalhe de cada uma no `README.md`.

Feito hoje:

- Galeria de obras com 9 fotos. Cada card mostra a obra e a cidade que o
  cliente informou: Ortobom (Simões Filho/BA), cinema Cinesercla (Campina
  Grande/PB), usina termelétrica (Maracanaú/CE), usina termelétrica Borborema
  Energética, academia Smart Fit e Sam's Club. Os cards 06, 07 e 09 não têm
  obra porque o cliente não informou.
- Cartão do diretor em "Quem somos" e CNPJ no rodapé.
- **Preparo de produção**: WebP, cache, dados estruturados, Open Graph,
  sitemap, robots e favicon. Ver as duas seções seguintes.

Nenhum texto visível da página foi alterado no trabalho de SEO: o pedido do
cliente foi manter as palavras do site. Palavra-chave entrou só em `title`,
`description`, `alt` e dados estruturados.

## WebP e cache (como funciona)

Cada foto tem um irmão `.webp` no mesmo diretório, com o nome completo mais a
extensão: `p-carrier-laje.jpg` → `p-carrier-laje.jpg.webp`. O `default.conf`
tem um `map` que lê o `Accept` do navegador e um `try_files $uri$webp $uri`,
então o WebP é servido no lugar do JPEG sem que HTML e CSS saibam disso.
Navegador velho recebe o JPEG.

No `default.conf`, `Cache-Control` e `Vary` saem de `map`, não de `add_header`
dentro de `location`. **Isso é de propósito**: no nginx, um `add_header` dentro
de um `location` apaga todos os headers herdados do `server`. Se alguém mover
esses headers pra dentro de um location, o cache e os headers de segurança
param de valer sem dar erro nenhum.

O `default.conf` foi testado em container local em 16/09/2026 (`docker build` +
`docker run -p 8099:80`): `nginx -t` ok, troca automática por WebP funcionando
(110 KB -> 62 KB), cache de 30 dias nas fotos, `no-cache` no HTML, headers de
segurança e os seis arquivos de raiz respondendo 200.

## Contato (todos os caminhos caem no WhatsApp)

Regra desde 17/09/2026: **o WhatsApp é o fixo, a ligação é o celular.** Todo
botão de zap abre o WhatsApp com a frase já preenchida; o único `tel:` do site
é o número embaixo do botão de WhatsApp no rodapé, **83 99825-3434**, que é pra
pessoa tocar e ligar na hora. Os dois números estão no JSON-LD.

O número do
atendimento é **83 3099-8606** (trocado a pedido do Caio em 17/09/2026; antes
era o celular 83 99825-3434). Apesar de ser o fixo, ele tem **WhatsApp Business
ativo** — conferido no `wa.me`, que abre o perfil "Arclimtec Soluções Em
Climatização" com a logo da empresa. Ele vai escrito como `558330998606` em
cinco lugares do `index.html`:

- linha ~555, botão "Orçamento" do topo.
- linha ~783, botão WhatsApp do rodapé.
- linha ~787, o número visível do rodapé (era `tel:` com o fixo, virou `wa.me`).
- linha ~801, botão flutuante.
- `const ZAP` no JS, que monta os botões `data-zap` de cada serviço e obra com
  o assunto da caixa que a pessoa abriu.

Trocar o número = trocar `558330998606` nesses cinco pontos, e o texto visível
da linha ~787 junto, senão o rodapé mostra um número e linka outro. O JSON-LD,
em `telephone`, também acompanha.

Conferência rápida depois de trocar, na página servida: todo `a[href*="wa.me"]`
tem que apontar pro mesmo número, e nenhum link pode voltar a usar `tel:`.

## Estado do lançamento (17/09/2026)

**O site está no ar, com HTTPS válido.** `arclimtec.com.br` e
`www.arclimtec.com.br` resolvem 31.97.24.35, respondem 200, o HTTP redireciona
301 pra HTTPS e os dois servem certificado **Let's Encrypt** emitido em
17/09/2026, com validade até 16/12/2026 (renovação automática pelo Traefik do
EasyPanel).

Sobre o SSL, pra não repetir o erro: a primeira tentativa de emitir foi na noite
do dia 16, com o DNS ainda fora do ar, e falhou. **O Traefik não tenta de novo
sozinho**, e um redeploy do app também não forcou: o que resolveu foi desligar e
religar o SSL do domínio no painel, nos dois hostnames, depois do DNS publicado.
Se um dia o certificado voltar a ser `CN=Easypanel`, é esse o caminho.

Continua aberto: redirect 301 do `www` pro apex, Search Console com o
`sitemap.xml`, Perfil da Empresa no Google e o e-mail do domínio (passos 4 a 7
da lista abaixo).

Também em 17/09: as fotos no computador estavam com zoom e a logo do rodapé
esticada. Causa única, e vale pra qualquer `<img>` novo do site: os atributos
`width`/`height` do HTML valem como **altura fixa** quando o CSS só define a
largura, e aí o `aspect-ratio` não tem efeito nenhum. A prévia de obras virava
640x960 com recorte, cada card da galeria ficava mais alto que a tela e a logo
do rodapé ia de 124px para 422px de largura. O `img{...;height:auto}` na regra
global resolve o caso geral; quem define `height` em CSS precisa de `width:auto`
junto.

A foto de fundo chegou a ser mudada pra usar no PC o mesmo `contain` desfocado
do celular, e **o Caio pediu pra voltar**: no PC ela segue `center 18%/cover`,
preenchendo a tela. Não mexer no PC sem ele pedir.

No celular (18/09/2026, a pedido dele) o `contain` saiu: a foto agora tem zoom e
fica presa pelo topo, mostrando o difusor grande inteiro e só a parte de cima da
fileira seguinte, que dissolve no desfoque. O `::after` é uma faixa de `50svh`
com `center top/auto 170%`. **O tamanho é dado pela altura, não pela largura**,
de propósito: assim a fatia visível da foto é sempre o mesmo pedaço de cima em
qualquer tela, e só o corte lateral varia. Mexer no `170%` muda o que aparece;
mexer no `50svh` muda o tamanho da foto na tela sem mudar o enquadramento.

### Como estava em 16/09

### O que já funciona no servidor

O app está rodando no EasyPanel, IP **31.97.24.35** (mesma VPS do
caiohenrique.dev). Testado forjando o `Host`, sem depender de DNS:

    curl -sk --resolve arclimtec.com.br:443:31.97.24.35 https://arclimtec.com.br/

- `arclimtec.com.br` e `www.arclimtec.com.br` respondem **200** com o site certo.
- HTTP redireciona pra HTTPS sozinho.
- Quem publica é o Caio, clicando em **Redeploy** no EasyPanel depois do push.
- Certificado atual: `CN=Easypanel`, o auto-assinado padrão.

### O que trava

O domínio `arclimtec.com.br` é registrado no **Registro.br** (não na Hostinger,
como o arquivo supunha antes), em nome da Arclimtec, titular Daniel Souza da
Silva, conta **DASSI1531**, criado em 18/07/2026 e pago até 2031.

Na noite do dia 16 foi ligado o **modo avançado** do DNS do Registro.br e criados
dois registros:

| Tipo | Nome | Dados |
|---|---|---|
| A | (vazio, o apex) | 31.97.24.35 |
| A | www | 31.97.24.35 |

O painel salvou os dois ("Zona DNS atualizada com sucesso"), mas eles ficaram
com a **bolinha cinza**, que é pendente de publicação, e até 22h04 o DNS público
seguia sem responder. A zona no ar ainda era a de domínio parqueado, com o
`v=spf1 -all` e o MX nulo `0 .` de fábrica. O serial subiu várias vezes
(...9920, ...9950, ...0000, ...0010) republicando sempre a versão antiga.

Causa: o Registro.br segura a publicação enquanto o domínio está na janela de
**transição** aberta pela troca de modo básico para avançado. O contador na tela
marcava 1h7m às 21h33, ou seja, fecharia por volta das **22h40 de 16/09**.

**Lição**: ligar o modo avançado custa uma janela de 2h em que nada publica. Em
domínio novo com pressa de subir, o modo básico resolve o apex na hora. O
avançado só compensa se precisar de `www` separado, MX ou TXT, e é melhor ligar
com antecedência, não no dia do lançamento.

### Amanhã, na ordem

1. **Conferir se o DNS publicou.** Pelo DNS público, que não tem cache local:

       curl -s "https://dns.google/resolve?name=www.arclimtec.com.br&type=A"

   Esperado: `31.97.24.35` nos dois nomes. Se der `Status 3`, ainda é NXDOMAIN.
   O navegador pode insistir no NXDOMAIN por até 15 min depois de publicar (TTL
   negativo do SOA é 900s): limpar em `chrome://net-internals/#dns` ou com
   `ipconfig /flushdns`.

2. **Se publicou**: o Caio clica em emitir o SSL (Let's Encrypt) nos dois
   domínios no EasyPanel. Uma tentativa já falhou no dia 16, com o DNS ainda
   fora. O limite do Let's Encrypt é de **5 validações falhas por hostname por
   hora**, então só clicar com o DNS confirmado.

3. **Se não publicou nem depois da transição fechar**: aí sim apagar as duas
   entradas no painel e recriar, que força uma publicação nova. Durante a
   transição isso não adianta, as entradas voltam pra mesma fila.

4. Depois do SSL, marcar o **`www` como redirect 301 pro apex** no EasyPanel.
   Hoje os dois servem cópias idênticas (mesmo md5), e o `canonical` do site
   aponta pro apex sem www. Fazer isso antes de cadastrar no Search Console.

5. Search Console e envio do `sitemap.xml`.

6. Perfil da Empresa no Google. Pra busca local do tipo "ar condicionado Campina
   Grande", pesa mais que o site.

7. E-mail do domínio — o Caio quer fazer isso **em 19/09/2026**, junto comigo.
   Ver a seção "E-mail do domínio" no fim deste arquivo, que tem o passo a
   passo e as opções de provedor.

### Acesso

O painel do Registro.br é a conta do Daniel (DASSI1531) e a sessão cai rápido.
Quem faz login é o Caio; o Claude só opera a tela depois que ela já está logada.

## Hero: carrossel automático (18/09/2026, pedido do Caio)

O comparador de antes e depois saiu. No lugar entrou um carrossel que **troca
sozinho de 3 em 3 segundos**. São **quatro slides**, nesta ordem (ordem do
cliente, 18/09/2026):

1. `p-hero-5-condensadoras-laje.jpg` — condensadoras Carrier na laje
2. `p-hero-6-condensadoras-aquasnap.jpg` — condensadoras Carrier em bases de concreto
3. `p-hero-7-dutos-teto.jpg` — rede dutada no teto do galpão
4. `p-hero-2-tecnico.jpg` — o desenho técnico do prédio, o traçado transparente

As duas primeiras levam a mesma legenda, "Condensadoras em laje": foi escolha
do Caio em 18/09/2026, depois de eu ter posto "Condensadoras AquaSnap" e
"Condensadoras Carrier" na segunda. Não "consertar" pra diferenciar.

O cliente pediu o **desenho** no fim, não o render realista: são duas artes do
mesmo prédio e é fácil trocar uma pela outra. O render (`p-hero-1`), o duto
vertical (`p-hero-4`) e as condensadoras no piso (`p-hero-3`) ficaram fora da
hero. Os arquivos continuam em `assets/` e o `tools/hero_slides.py` continua
gerando os sete — é só o HTML que serve quatro.

A caixa **sangra até as duas bordas da tela**, agora também no computador
(`width:100vw` com `margin-inline:calc(50% - 50vw)`), e é **16/9 fixa**.

### Quem mexe manda na foto (18/09/2026)

Tem **seta dos dois lados** (`.capa__seta`, mesmo desenho das do trilho de
fotos, com fundo escuro pra não sumir num slide claro) e **arraste pro lado**,
a partir de 40px. Clicar, arrastar ou usar a seta **para o carrossel por 10
segundos** naquele slide; passados os 10s ele volta a passar sozinho. Tocar de
novo dentro desses 10s recomeça a contagem, senão o segundo toque herdaria o
resto da parada do primeiro.

Dois detalhes que não são enfeite:

- a capa é `touch-action:pan-y`. Sem isso o Chrome do celular decide no meio do
  gesto que o arraste horizontal era rolagem, manda `pointercancel` e o swipe
  morre.
- seta e arraste saem os dois do mesmo `pointerup`, e o `pointerup` fica na
  **janela**, não na capa: soltar o dedo fora da caixa não dispararia o da
  capa e o carrossel voltaria a passar no meio do gesto.
- **não usar `setPointerCapture` aqui.** A primeira versão prendia o ponteiro
  na capa e deixava a seta no `click` do botão. No desktop ia; no celular não,
  porque com o ponteiro preso o `click` do toque é entregue à capa e não ao
  botão, e a seta virava enfeite. O Caio pegou isso em produção em 18/09/2026.
- a seta só conta se o dedo **soltar em cima da mesma seta** onde apertou.
- o `click` do botão continua lá, mas só atende teclado (`e.detail === 0`).
  Sem essa guarda o mouse contaria duas vezes, no `pointerup` e no `click`.

Com `prefers-reduced-motion` ele continua não passando sozinho, mas as setas
valem: aí a troca é escolha da pessoa, não animação solta.

O `<h1>` "Climatização industrial e empresarial" **fica por cima das fotos**, no
alto da caixa, e não mais acima dela: no fluxo ele comia uma faixa da primeira
tela e empurrava a foto pra baixo. O véu escuro atrás dele não é enfeite, é o
que segura a leitura — o desenho técnico do prédio é quase branco no topo e o
texto é claro.

O que segura tudo isso é o `tools/hero_slides.py`: ele entrega os slides
já em 1600x900, então o HTML não corta nem estica nada e a página não muda de
altura a cada troca. Cada foto chega nesse formato de um jeito:

- os dois renders do prédio têm fundo liso, então o fundo é **esticado** pros
  lados. Não se perde um pixel do desenho e não dá pra ver a emenda.
- as fotos de obra são **recortadas**, com um foco vertical por foto.
- as fotos de obra levam a marca d'água; os renders não, porque a logo branca
  sumiria no fundo claro deles.

Os arquivos que alimentam o script moram em `tools/fotos-originais/`, inclusive
os dois renders — eles saíram de `assets/` quando deixaram de ser servidos.

O carrossel para quando a aba sai da frente, e com `prefers-reduced-motion` ele
nem começa: fica na primeira foto, parada. A troca também espera a próxima foto
estar carregada, senão entraria um quadro vazio no meio.

## Decisões de layout (17/09/2026, pedidos do cliente)

- **Fotos da galeria**: todo card é 4/3 e a foto preenche ele por inteiro
  (`object-fit:cover`), sem faixa vazia. Como as fotos vão de 16:9 a quase 1:2,
  o recorte é inevitável, então cada foto em pé tem seu `object-position` no
  CSS, apontando pra faixa onde está o equipamento. Foto nova em pé precisa
  ganhar a linha dela, senão o corte cai no centro e pode pegar teto ou chão.
  **O `marca_dagua.py` tem uma cópia desses `object-position` na constante
  `POSICAO`** e é ela que decide onde a marca cabe. Mudou o valor no CSS e
  esqueceu do script, a marca volta a sair cortada no card — foi o que
  aconteceu quando o card virou `cover` e o script ainda calculava por
  `contain` (corrigido em 18/09/2026).
  A margem da marca sai da **menor** dimensão visível. Tirada da largura, como
  era antes, a marca ficava colada na borda de baixo das fotos deitadas e de
  longe parecia cortada.
- **Carrossel**: cada clique anda **uma foto**, e o alvo sai da posição medida do
  card (`getBoundingClientRect`), nunca de múltiplos da largura visível. Era
  isso que desalinhava: o gap fazia o erro crescer a cada clique até os cards
  pararem cortados. As bolinhas são uma por foto.
- **Menu do celular**: os links do topo viram um painel lateral, aberto pelo
  botão de três linhas à direita do orçamento. O painel mora **fora do
  `header`**, de propósito: a barra tem `backdrop-filter`, e um ancestral com
  filtro vira containing block de qualquer `position:fixed` dentro dele — o
  painel ficava com a altura da barra. Por isso os quatro links existem duas
  vezes no HTML, na barra e no painel; mexeu num, mexe no outro.
- **Logo do topo**: 58px no PC, 36px no celular e 32px abaixo de 400px. A altura
  da barra e o `min-height` do hero (`calc(100svh - 93px)`) acompanham.
- **Textos**: o site não fala mais em "desde 2012"; fala em **15 anos de
  experiência no mercado**. E o alcance deixou de ser "Paraíba e região": o selo
  virou **BR / atendemos o Brasil todo**, a seção de clientes acompanha e o
  JSON-LD ganhou o país no `areaServed`. O `foundingDate` de 2012 continua no
  JSON-LD: é dado de cadastro, não texto de página.

## SEO

- `robots.txt`, `sitemap.xml`, `site.webmanifest`, `favicon.ico`,
  `apple-touch-icon.png` e `icon-512.png` ficam na **raiz** e são copiados
  explicitamente pelo Dockerfile. Arquivo novo na raiz precisa entrar lá.
- Dados estruturados `HVACBusiness` em JSON-LD no fim do `<body>`: CNPJ,
  endereço, telefone, fundação, o diretor, cidades atendidas e os 8 serviços.
- Imagem de compartilhamento: `assets/og-arclimtec.jpg`, 1200x630.
- **O domínio está escrito como `arclimtec.com.br`** em `index.html`,
  `robots.txt` e `sitemap.xml`. Era uma suposição. Se o domínio comprado for
  outro, trocar nos três.

## E-mail do domínio (levantado em 18/09/2026, pra fazer em 19/09)

O Caio perguntou quanto custa e como compra o e-mail do domínio. Isto aqui é a
resposta, pra não refazer a pesquisa amanhã.

### O que ele estava confundindo

**Registro.br não vende e-mail.** Ele registra o domínio e dá o painel de DNS,
só. E-mail se compra em outro lugar e se aponta por DNS.

**A VPS da Hostinger não entra nessa.** Site e e-mail são independentes:

- o site vai pelo registro `A`, que aponta pro IP da VPS (`31.97.24.35`)
- o e-mail vai pelos registros `MX`, que apontam pro provedor contratado

Ou seja: não se mexe em nada do EasyPanel pra ter e-mail, e **não se mexe no
registro `A`** na hora de configurar o e-mail, senão o site cai.

### Como a zona está hoje (conferido em 18/09/2026)

Nameservers: `a.sec.dns.br` e `b.sec.dns.br` — o DNS é do próprio Registro.br.
Então dá pra contratar o e-mail em qualquer provedor e só colar os registros
lá, sem trocar nameserver.

**MX: nenhum. TXT: nenhum.** Conferido pelo DNS público:

    curl -s "https://dns.google/resolve?name=arclimtec.com.br&type=MX"
    curl -s "https://dns.google/resolve?name=arclimtec.com.br&type=TXT"

Os dois voltam `Status 0` sem `Answer`, que é NODATA: o registro não existe.
A versão anterior deste arquivo dizia que a zona tinha **MX nulo** e **SPF
`-all`** e que os dois teriam que sair antes — **isso não confere mais**, não
tem nada pra remover. Conferir de novo antes de mexer, porque a zona pode ter
mudado entre 18/09 e o dia de fazer.

### Opções

| Opção | Custo | Pega bem se |
|---|---|---|
| **Zoho Mail grátis** | R$ 0 | 5 contas, 5 GB cada. **Só webmail e app do Zoho**: IMAP/POP virou pago, então não conecta no Outlook nem no app de e-mail do celular |
| **Hostinger (Titan)** | ~US$ 1 a US$ 2,50 por caixa/mês | O Caio já é cliente: cai na mesma fatura e a configuração é mais guiada |
| **Google Workspace / Microsoft 365** | O mais caro | Se o cliente já vive no Gmail ou no Outlook e quer Drive/Teams junto |
| **Servidor na própria VPS** | R$ 0 de licença | **Não fazer.** Porta 25 costuma vir bloqueada, o IP não tem reputação e o e-mail cai no spam |

Os preços são de 18/09/2026 e **não estão cravados**: mudam, e o que aparece
anunciado quase sempre é promoção de primeiro ciclo, com renovação mais cara e
cobrança adiantada de 12 a 48 meses. Conferir no site antes de fechar.

### O passo a passo

1. Contratar o plano no provedor escolhido, informando `arclimtec.com.br`.
2. O provedor entrega uma lista de registros: os **MX**, um **TXT de SPF**, um
   **TXT de DKIM** e às vezes um TXT de verificação do domínio.
3. Entrar no Registro.br e colar esses registros no DNS do domínio.
   **Não encostar no registro `A`.**
4. Esperar propagar (minutos a algumas horas) e criar as caixas.

Os TXT de SPF e DKIM não são opcionais: sem eles o e-mail sai, mas cai no spam
de quem recebe.

### Quem assina

O domínio está na conta do **cliente** no Registro.br (DASSI1531, do Daniel), e
a sessão cai a cada poucos minutos — quem faz login é o Caio, eu só opero a tela
depois de logada.

A assinatura do e-mail deve ficar **no nome do cliente**, não do Caio: se entrar
na conta dele, no dia que o contrato acabar a empresa fica com o e-mail preso em
nome de terceiro. Vale escrever isso no contrato, que era justamente o que o
Caio estava redigindo quando perguntou.

## Pendências

Do Caio, fora do código:

Ver "Onde paramos" acima: o domínio já existe no Registro.br, os registros A
já foram criados e o que falta é a publicação da zona, o SSL, o redirect do
`www`, o Search Console, o Perfil da Empresa e o e-mail do domínio — este
último marcado com o Caio pra **19/09/2026**, ver a seção "E-mail do domínio".

De conteúdo, com o cliente:

- ~~Autorização pra publicar as marcas dos clientes e as obras citadas pelo
  nome~~ — **autorizado** pelo Caio em 16/09/2026.
- Obra e cidade das fotos 06, 07 e 09, que ficaram sem.
- Confirmar se fazem chiller e câmara fria.
- Três dúvidas técnicas nas legendas: `p-carrier-laje` (as seis Carrier são
  condensadoras de expansão direta ou mini-chiller?), `p-vrf-hitachi` (a
  etiqueta diz Hitachi "airCore Σ", mas a linha VRF da Hitachi é SET FREE),
  `p-casa-de-maquinas` ("fancoil" implica água gelada; podem ser evaporadoras
  de expansão direta).
- Não existe foto de ventilação/exaustão nem de higienização, e os dois são
  serviços de destaque na página.
- O `<h1>` é "Climatização industrial e empresarial" e não contém "ar
  condicionado", que é o termo que as pessoas pesquisam. É o maior ganho de
  SEO que sobrou na página, mas mexe em texto visível: só com aval do cliente.
