# tools/

Scripts de apoio. Não entram na imagem — o `Dockerfile` copia só os `.html` da raiz e a pasta `assets/`.

## `logo_prep.py`

Lê `assets/logo.jpg` (a logo original, com fundo branco), imprime as cores dominantes e gera:

- `assets/logo.png` — fundo branco removido, cores originais
- `assets/logo-branca.png` — mesma silhueta em branco, para fundos escuros

Foi de onde saiu a paleta usada no site: **#24549C** (azul institucional), **#00A8F0** (ciano) e **#006CB4**.

```sh
python3 tools/logo_prep.py
```

## `publish_branches.py`

Publica uma versão em cada branch, já renomeada para `index.html` e com o `<title>` limpo (sem o marcador "V1 ·/V2 ·…" que serve só para diferenciar as abas na comparação local).

```sh
python3 tools/publish_branches.py
```

Cuidado: ele usa `git checkout -B`, ou seja, **recria** as branches a partir de `main`. Serviu para o primeiro empurrão das V1–V3.

**Histórico, não roda mais como está**: os arquivos `v1-*` … `v5-*` saíram da `main` (vivem só nas branches de mesmo nome), então o script não acha mais o fonte. Para mexer numa dessas branches antigas, trabalhe direto nela:

```sh
git checkout v3-impacto     # a versão já é o index.html da branch
```

## `gen_claro.py`

Gera `v7-claro-a.html` e `v7-claro-b.html` recolorindo a `v6-definitiva.html`. Só troca cores — estrutura, HTML e JS ficam idênticos, e o script aborta se algum trecho de CSS esperado não casar (proteção contra rodar em cima de uma V6 alterada).

```sh
python3 tools/gen_claro.py
```

## De onde vieram os assets

Fotos e logo são do próprio cliente, enviadas por WhatsApp. `bg-industrial.jpg` e `p-condensadoras-telhado.jpg` tiveram os 10% de baixo cortados para remover a marca d'água "tirada no moto g⁶ plus" da câmera.
