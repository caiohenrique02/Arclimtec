#!/usr/bin/env python3
"""Carimba a logo como marca d'água nas fotos do carrossel de equipamentos.

Lê os arquivos limpos de tools/fotos-originais/ e grava a versão carimbada
por cima do mesmo nome em assets/. Sempre parte do original, então dá pra
rodar de novo à vontade pra ajustar tamanho ou opacidade sem carimbar duas
vezes. Os originais ficam em tools/ de propósito: o Dockerfile copia só
*.html e assets/, então a foto sem marca não vai parar no ar.

    python3 tools/marca_dagua.py

O carrossel mostra a foto num card 4/3 com object-fit:cover, ou seja, boa
parte da foto original nunca aparece: as deitadas perdem as laterais, as em
pé perdem o topo e a base, e o quanto perde de cada lado sai do
object-position. A marca é posicionada dentro do que sobra, senão ela cai
justo no pedaço cortado.
"""

from pathlib import Path

from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
ORIGINAIS = RAIZ / "tools" / "fotos-originais"
DESTINO = RAIZ / "assets"
LOGO = RAIZ / "assets" / "logo-branca.png"

CARD = 4 / 3              # .card img { aspect-ratio:4/3 }
# Fotos que não vão pro card 4/3 da galeria: a mosaico de "Manutenção com
# medição" é 3/4 (.manut__fotos img { aspect-ratio:3/4 }). Sem isto o script
# calcularia a área visível como se fosse cortada em 4/3, e a marca cairia no
# lugar errado numa foto que na verdade aparece quase inteira.
CARD_POR_FOTO = {
    "p-manutencao-pressao-eletrica.jpg": 3 / 4,
    "p-manutencao-compressores.jpg": 3 / 4,
    "p-manutencao-temperatura-duto.jpg": 3 / 4,
    "p-manutencao-superaquecimento.jpg": 3 / 4,
}
ZOOM_HOVER = 1.02         # .card:hover img { transform: scale(1.02) }
LARGURA_MARCA = 0.22      # largura da logo, em fração da largura visível
# O respiro sai da MENOR dimensão visível, não da largura: numa foto deitada a
# largura é bem maior que a altura, e uma margem tirada dela deixava a marca
# colada na borda de baixo do card — de longe parecia cortada.
MARGEM = 0.09
OPACIDADE = 0.6
SOMBRA = 0.5              # sombra escura atrás, pra logo branca aguentar foto clara
QUALIDADE = 88

# Espelho do object-position de cada foto no CSS (as regras
# `.card img[src*="..."]` do index.html). Quem não está aqui é `center center`.
# Mudou lá, muda aqui: é esse valor que diz onde a marca não vai ser cortada.
POSICAO = {
    "p-dutos-galpao-2.jpg": (0.5, 0.30),
    "p-vrf-hitachi.jpg": (0.5, 0.45),
    "p-cassete-apartamento.jpg": (0.5, 0.30),
    "p-virotubo-loja.jpg": (0.5, 0.33),
    "p-dutos-isolamento.jpg": (0.60, 0.5),
    "p-cinesercla-plenum.jpg": (0.5, 0.35),
}

# Rodar o script recarimba todas de uma vez, sempre a partir do original limpo
# em tools/fotos-originais/ — nunca por cima de uma foto já carimbada.
FOTOS = [
    "p-dutos-galpao-2.jpg",
    "p-carrier-laje.jpg",
    "p-vrf-hitachi.jpg",
    "p-selfcontained.jpg",
    "p-casa-de-maquinas.jpg",
    "p-condensadoras-laje.jpg",
    "p-cassete-apartamento.jpg",
    "p-virotubo-loja.jpg",
    "p-dutos-isolamento.jpg",
    "p-cinesercla-plenum.jpg",
    "p-thermomatic-climatizadores.jpg",
    "p-manutencao-pressao-eletrica.jpg",
    "p-manutencao-compressores.jpg",
    "p-manutencao-temperatura-duto.jpg",
    "p-manutencao-superaquecimento.jpg",
]


def area_visivel(largura, altura, posicao=(0.5, 0.5), card=CARD):
    """Retângulo da foto que de fato aparece no card.

    O card é 4/3 com object-fit:cover (ou 3/4 na mosaico de manutenção,
    via `card=`): a foto cobre o card inteiro e o que não couber é cortado.
    Foto mais larga que o alvo perde as laterais, foto mais alta perde topo
    e base, e o object-position decide de que lado sai o corte. Desconta
    também a folga do zoom do hover, senão a marca encosta na borda quando o
    card cresce.
    """
    if largura / altura > card:       # deitada demais: corta as laterais
        vis_l, vis_a = altura * card, altura
    else:                             # em pé demais: corta topo e base
        vis_l, vis_a = largura, largura / card

    vis_l /= ZOOM_HOVER
    vis_a /= ZOOM_HOVER
    fx, fy = posicao
    return (
        round((largura - vis_l) * fx),
        round((altura - vis_a) * fy),
        round(vis_l),
        round(vis_a),
    )


def carimba(foto, logo, visivel=None, largura_marca=LARGURA_MARCA, margem_rel=MARGEM):
    """Grava a logo no canto inferior direito da área visível da foto."""
    x, y, vis_l, vis_a = visivel or (0, 0, foto.width, foto.height)

    marca_l = round(vis_l * largura_marca)
    marca_a = round(marca_l * logo.height / logo.width)
    marca = logo.resize((marca_l, marca_a), Image.LANCZOS)

    margem = round(min(vis_l, vis_a) * margem_rel)
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
        visivel = area_visivel(
            *foto.size, POSICAO.get(nome, (0.5, 0.5)), card=CARD_POR_FOTO.get(nome, CARD)
        )
        carimba(foto, logo, visivel).save(
            DESTINO / nome, quality=QUALIDADE, optimize=True, progressive=True
        )
        print(f"{nome}: {foto.width}x{foto.height} -> visivel {visivel}")


if __name__ == "__main__":
    main()
