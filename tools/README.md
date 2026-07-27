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

Cuidado: ele usa `git checkout -B`, ou seja, **recria** as branches a partir de `main`. Serviu para o primeiro empurrão das V1–V3. Para atualizar uma branch que já existe sem reescrever histórico, o caminho é outro:

```sh
git checkout v3-impacto
git checkout main -- v3-impacto.html        # traz a versão nova de main
# renomear para index.html, ajustar o <title>, commitar
```

## De onde vieram os assets

Fotos e logo são do próprio cliente, enviadas por WhatsApp. `bg-industrial.jpg` e `p-condensadoras-telhado.jpg` tiveram os 10% de baixo cortados para remover a marca d'água "tirada no moto g⁶ plus" da câmera.
