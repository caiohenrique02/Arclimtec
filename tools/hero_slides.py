#!/usr/bin/env python3
"""Prepara os slides do carrossel da hero, todos no mesmo formato.

    python3 tools/hero_slides.py

O carrossel troca de foto sozinho e mostra cada uma inteira, na largura toda
da tela. Como as fotos originais vão de 0.64 (em pé) a 1.77 (deitada), se
cada slide entrasse com a proporção dela a página inteira pularia de altura a
cada troca. Então todo slide sai daqui em 1600x900 (16/9), e o HTML não
precisa saber de nada: é sempre a mesma caixa.

Cada foto chega nesse formato de um jeito, escolhido pelo que ela é:

- os dois renders do prédio têm fundo liso, então o fundo é *esticado* pros
  lados até fechar 16/9. Não se perde um pixel do desenho e não aparece
  emenda, porque o que se repete é a cor chapada da borda.
- as fotos de obra são recortadas, com o foco dizendo que faixa não pode
  sumir. Foto real não dá pra esticar sem aparecer o rastro.
- a foto em pé (`p-hero-4-duto-vertical`) entra no modo `blur`, escolhido pelo
  Caio em 18/09/2026: ela aparece inteira no meio e o que sobra dos lados é ela
  mesma ampliada e desfocada. Recortar pra deitada também funcionava, mas
  jogava fora quase toda a descida do duto, que é o assunto da foto.

As fotos de obra levam a mesma marca d'água da galeria, do mesmo jeito: logo
branca no canto inferior direito, com sombra. Os renders não levam: são
desenho, não foto de obra, e a logo branca sumiria no fundo claro.
"""

from pathlib import Path

from PIL import Image, ImageFilter

from marca_dagua import QUALIDADE, carimba

RAIZ = Path(__file__).resolve().parent.parent
ORIGINAIS = RAIZ / "tools" / "fotos-originais"
ASSETS = RAIZ / "assets"
LOGO = ASSETS / "logo-branca.png"

LARGURA, ALTURA = 1600, 900      # 16/9, a caixa única do carrossel
PROPORCAO = LARGURA / ALTURA

# A hero ocupa a tela toda, então a marca entra menor em fração do que nos
# cards da galeria: com os 0.26 de lá ela sairia do tamanho de um cartaz.
MARCA_HERO = 0.15
MARGEM_HERO = 0.06

# origem, destino, modo, foco vertical do recorte (0 = topo, 1 = base)
SLIDES = [
    (ORIGINAIS / "p-capa-predio-render.jpg", "p-hero-1-render.jpg", "estica", 0.5),
    (ORIGINAIS / "p-capa-predio-tecnico-alinhado.jpg", "p-hero-2-tecnico.jpg", "estica", 0.5),
    (ORIGINAIS / "p-hero-3-condensadoras-piso.jpg", "p-hero-3-condensadoras-piso.jpg", "corta", 0.45),
    (ORIGINAIS / "p-hero-4-duto-vertical.jpg", "p-hero-4-duto-vertical.jpg", "blur", 0.5),
    (ORIGINAIS / "p-hero-5-condensadoras-laje.jpg", "p-hero-5-condensadoras-laje.jpg", "corta", 0.5),
    (ORIGINAIS / "p-hero-6-condensadoras-aquasnap.jpg", "p-hero-6-condensadoras-aquasnap.jpg", "corta", 0.5),
    # quase quadrada e com o assunto no teto: o foco alto joga fora o piso vazio
    (ORIGINAIS / "p-hero-7-dutos-teto.jpg", "p-hero-7-dutos-teto.jpg", "corta", 0.18),
]


def apara_bordas(foto, limite=24):
    """Tira a tarja preta que algumas fotos trazem no topo ou na base.

    Vídeo e print de celular costumam vir com essas bordas. No recorte elas
    somem sozinhas, mas na versão com fundo desfocado a foto aparece inteira
    e a tarja fica à vista no meio da tela.
    """
    largura, altura = foto.size
    cinza = foto.convert("L")

    def clara(linha):
        return max(cinza.getpixel((x, linha)) for x in range(0, largura, 8)) > limite

    topo, base = 0, altura - 1
    while topo < base and not clara(topo):
        topo += 1
    while base > topo and not clara(base):
        base -= 1
    return foto.crop((0, topo, largura, base + 1)) if (topo or base < altura - 1) else foto


def corta(foto, foco):
    """Recorta a maior região 16/9 da foto, na faixa apontada pelo foco."""
    largura, altura = foto.size
    if largura / altura > PROPORCAO:          # sobra largura: tira das laterais
        corte_l, corte_a = round(altura * PROPORCAO), altura
    else:                                     # sobra altura: tira de cima e de baixo
        corte_l, corte_a = largura, round(largura / PROPORCAO)
    x = round((largura - corte_l) * 0.5)
    y = round((altura - corte_a) * foco)
    return foto.crop((x, y, x + corte_l, y + corte_a))


def estica(foto):
    """Fecha 16/9 esticando a cor da borda pros lados, sem cortar a arte."""
    largura, altura = foto.size
    alvo_l = round(altura * PROPORCAO)
    if alvo_l <= largura:
        return corta(foto, 0.5)

    tela = Image.new("RGB", (alvo_l, altura))
    sobra = (alvo_l - largura) // 2
    # a coluna de 1px de cada borda, repetida até preencher a faixa que falta
    tela.paste(foto.crop((0, 0, 1, altura)).resize((sobra, altura)), (0, 0))
    tela.paste(
        foto.crop((largura - 1, 0, largura, altura)).resize((alvo_l - largura - sobra, altura)),
        (sobra + largura, 0),
    )
    tela.paste(foto, (sobra, 0))
    return tela


def com_blur(foto):
    """Foto inteira no meio, o que sobra é ela mesma ampliada e desfocada.

    Devolve junto a caixa da parte nítida: é lá dentro que a marca tem que
    ficar, senão ela cai na faixa desfocada e parece colada por engano.
    """
    foto = apara_bordas(foto)
    fundo = corta(foto, 0.5).resize((LARGURA, ALTURA), Image.LANCZOS)
    fundo = fundo.filter(ImageFilter.GaussianBlur(28))

    escala = min(LARGURA / foto.width, ALTURA / foto.height)
    frente = foto.resize((round(foto.width * escala), round(foto.height * escala)), Image.LANCZOS)
    caixa = ((LARGURA - frente.width) // 2, (ALTURA - frente.height) // 2)
    fundo.paste(frente, caixa)
    return fundo, (*caixa, frente.width, frente.height)


def grava(imagem, nome, logo, marcar, visivel=None):
    imagem = imagem.resize((LARGURA, ALTURA), Image.LANCZOS)
    if marcar:
        imagem = carimba(imagem, logo, visivel, MARCA_HERO, MARGEM_HERO)
    imagem.save(ASSETS / nome, quality=QUALIDADE, optimize=True, progressive=True)
    print(f"{nome}: {LARGURA}x{ALTURA}{' + marca' if marcar else ''}")


def main():
    logo = Image.open(LOGO).convert("RGBA")
    for origem, nome, modo, foco in SLIDES:
        if not origem.exists():
            raise SystemExit(f"falta o original {origem}")
        foto = Image.open(origem).convert("RGB")
        marcar = modo != "estica"                    # só as fotos de obra
        visivel = None
        if modo == "estica":
            imagem = estica(foto)
        elif modo == "blur":
            imagem, visivel = com_blur(foto)
        else:
            imagem = corta(foto, foco)
        grava(imagem, nome, logo, marcar, visivel)


if __name__ == "__main__":
    main()
