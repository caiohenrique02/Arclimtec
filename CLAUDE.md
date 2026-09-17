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
- Servir local com `python3 -m http.server 8085` na raiz do repo. A 8081 e a
  8082 costumam estar ocupadas por outros projetos do Caio.
- Fotos de obra novas passam por `tools/marca_dagua.py`: o original limpo vai
  pra `tools/fotos-originais/` e o nome entra na lista `FOTOS`. O script
  recarimba tudo a partir dos originais, nunca por cima de foto já carimbada.
  O Dockerfile não copia `tools/`, então o original sem marca não vai ao ar.
- Toda foto nova precisa do `.webp` irmão (`foto.jpg.webp`), senão ela é a
  única do site que não pega a otimização. Ver "WebP" abaixo.
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
preenchendo a tela, e o `contain` continua só no celular. Não mexer nisso de
novo sem ele pedir.

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

7. E-mail do domínio quando o cliente quiser. A zona hoje tem **MX nulo** e
   **SPF `-all`**, que bloqueiam e-mail: os dois precisam sair na hora de
   apontar o provedor. Como o DNS é do Registro.br, dá pra contratar em
   qualquer lugar e só trocar os registros, sem mexer em nameserver.

### Acesso

O painel do Registro.br é a conta do Daniel (DASSI1531) e a sessão cai rápido.
Quem faz login é o Caio; o Claude só opera a tela depois que ela já está logada.

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

## Pendências

Do Caio, fora do código:

Ver "Onde paramos" acima: o domínio já existe no Registro.br, os registros A
já foram criados e o que falta é a publicação da zona, o SSL, o redirect do
`www`, o Search Console, o Perfil da Empresa e o e-mail do domínio.

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
