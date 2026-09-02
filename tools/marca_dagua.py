#!/usr/bin/env python3
"""Carimba a logo como marca d'água nas fotos do carrossel de equipamentos.

Lê os arquivos limpos de tools/fotos-originais/ e grava a versão carimbada
por cima do mesmo nome em assets/. Sempre parte do original, então dá pra
rodar de novo à vontade pra ajustar tamanho ou opacidade sem carimbar duas
vezes. Os originais ficam em tools/ de propósito: o Dockerfile copia só
*.html e assets/, então a foto sem marca não vai parar no ar.

    python3 tools/marca_dagua.py

O carrossel mostra a foto em 4/3 com object-fit:cover e dá um scale(1.02)
no hover, ou seja, boa parte da foto original nunca aparece. A marca é
posicionada dentro do que sobra, senão ela cai justo no pedaço cortado.
"""

from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
ORIGINAIS = RAIZ / "tools" / "fotos-originais"
DESTINO = RAIZ / "assets"
LOGO = RAIZ / "assets" / "logo-branca.png"

FOTOS = [
    "p-dutos-galpao-2.jpg",
    "p-carrier-laje.jpg",
    "p-vrf-hitachi.jpg",
    "p-selfcontained.jpg",
    "p-casa-de-maquinas.jpg",
    "p-condensadoras-laje.jpg",
    "p-cassete-apartamento.jpg",
    "p-aerea-casa-maquinas.jpg",
]

PROPORCAO_CARD = 4 / 3   # .card img { aspect-ratio: 4/3; object-fit: cover }
ZOOM_HOVER = 1.02        # .card:hover img { transform: scale(1.02) }
LARGURA_MARCA = 0.26     # largura da logo, em fração da área visível
MARGEM = 0.045           # respiro até o canto, na mesma fração
OPACIDADE = 0.6
SOMBRA = 0.5             # sombra escura atrás, pra logo branca aguentar foto clara
QUALIDADE = 88


def area_visivel(largura, altura):
    """Retângulo da foto que sobra depois do corte do card e do zoom do hover."""
    proporcao = largura / altura
    if proporcao > PROPORCAO_CARD:
        vis_a = altura
        vis_l = altura * PROPORCAO_CARD
    else:
        vis_l = largura
        vis_a = largura / PROPORCAO_CARD
    vis_l /= ZOOM_HOVER
    vis_a /= ZOOM_HOVER
    return (
        round((largura - vis_l) / 2),
        round((altura - vis_a) / 2),
        round(vis_l),
        round(vis_a),
    )


def carimba(foto, logo):
    x, y, vis_l, vis_a = area_visivel(*foto.size)

    marca_l = round(vis_l * LARGURA_MARCA)
    marca_a = round(marca_l * logo.height / logo.width)
    marca = logo.resize((marca_l, marca_a), Image.LANCZOS)

    margem = round(vis_l * MARGEM)
    pos = (x + vis_l - marca_l - margem, y + vis_a - marca_a - margem)

    alfa = marca.getchannel("A")
    camada = Image.new("RGBA", foto.size, (0, 0, 0, 0))

    # sombra: a mesma silhueta em preto, deslocada 2px, pra marca não sumir
    # quando a foto atrás é clara (forro branco, laje ao sol)
    sombra = Image.new("RGBA", marca.size, (0, 0, 0, 0))
    sombra.putalpha(alfa.point(lambda p: round(p * SOMBRA)))
    camada.paste(sombra, (pos[0] + 2, pos[1] + 2), sombra)

    marca = marca.copy()
    marca.putalpha(alfa.point(lambda p: round(p * OPACIDADE)))
    camada.alpha_composite(marca, pos)

    saida = foto.convert("RGBA")
    saida.alpha_composite(camada)
    return saida.convert("RGB")


def main():
    logo = Image.open(LOGO).convert("RGBA")
    for nome in FOTOS:
        origem = ORIGINAIS / nome
        if not origem.exists():
            raise SystemExit(f"falta o original {origem}")
        foto = Image.open(origem).convert("RGB")
        carimba(foto, logo).save(
            DESTINO / nome, quality=QUALIDADE, optimize=True, progressive=True
        )
        print(f"{nome}: {foto.width}x{foto.height} -> visivel {area_visivel(*foto.size)}")


if __name__ == "__main__":
    main()
