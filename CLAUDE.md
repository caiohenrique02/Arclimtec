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

Desde 16/09/2026 **nenhum link de contato usa `tel:`**: o pedido do Caio foi que
todo número clicável abra o WhatsApp, com a frase já preenchida. São cinco
lugares com o número, todos com `558330998606` literal:

- `index.html` linha ~555, botão "Orçamento" do topo.
- linha ~783, botão WhatsApp do rodapé.
- linha ~787, o número visível do rodapé (era `tel:`, virou `wa.me`).
- linha ~801, botão flutuante.
- `const ZAP` no JS, que monta os botões `data-zap` de cada serviço e obra com
  o assunto da caixa que a pessoa abriu.

Trocar o número = trocar `558330998606` nesses cinco pontos. O JSON-LD guarda
`+55-83-3099-8606` em `telephone` de propósito: lá é o telefone da empresa, não
um botão.

⚠️ **Não está confirmado que 83 3099-8606 tem WhatsApp** — é o fixo. Se não
tiver, os cinco caminhos de contato do site não levam a lugar nenhum. O cadastro
do domínio no Registro.br traz 83 99825-3434 como celular do Daniel.

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

1. Apontar o domínio da Hostinger pro EasyPanel (registro A do `@`, CNAME do
   `www`), escolher a versão oficial e ligar o HTTPS. **Não trocar os
   nameservers da Hostinger**, senão o e-mail do domínio para junto.
2. Comprar o e-mail do domínio (recomendado: Titan da Hostinger). Depois que
   existir, o endereço entra no rodapé e no contato, que hoje só têm WhatsApp
   e telefone.
3. Cadastrar o site no Google Search Console e enviar o sitemap.
4. Criar e verificar o Perfil da Empresa no Google. Pra busca local do tipo
   "ar condicionado Campina Grande", isso pesa mais que o site.

De conteúdo, com o cliente:

- Autorização pra publicar as marcas dos clientes (Borborema, Axia,
  Pernambuco III, Thermomatic, Imago, Smart Fit) e as obras citadas pelo nome
  (Ortobom, Cinesercla, Sam's Club).
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
