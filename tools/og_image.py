#!/usr/bin/env python3
"""Gera a imagem de compartilhamento (Open Graph) do site.

    python3 tools/og_image.py

É a foto que aparece quando alguém cola o link do site no WhatsApp, no
Instagram, no Facebook ou no compartilhamento do Google. O `og:image` do
`index.html` aponta pra `assets/og-arclimtec-condensadoras.jpg`, em 1200x630.

Ela era o render do prédio, a mesma arte que o cliente tirou da hero em
18/09/2026. Em 20/09/2026 ele viu o render na prévia do link e pediu a
**primeira foto do carrossel** no lugar: as condensadoras Carrier na laje.

O recorte sai do original limpo, não do slide de 1600x900 já pronto: o slide
levaria a marca d'água dele junto e ela ficaria fora de posição depois de
cortar mais 60px de altura. Aqui a foto é cortada primeiro e carimbada
depois, então a marca cai no canto certo da imagem final.

A marca entra maior que na hero (0.22 contra 0.15): a prévia do WhatsApp é um
cartão pequeno e, no tamanho da hero, a logo não se lia.
"""

from pathlib import Path

from PIL import Image

from marca_dagua import QUALIDADE, carimba

RAIZ = Path(__file__).resolve().parent.parent
ORIGINAIS = RAIZ / "tools" / "fotos-originais"
ASSETS = RAIZ / "assets"
LOGO = ASSETS / "logo-branca.png"

LARGURA, ALTURA = 1200, 630       # o formato que as redes pedem
PROPORCAO = LARGURA / ALTURA

ORIGEM = ORIGINAIS / "p-hero-5-condensadoras-laje.jpg"
DESTINO = ASSETS / "og-arclimtec-condensadoras.jpg"

# 0 = topo, 1 = base. A foto é mais deitada que 1200x630, então o corte sai de
# cima e de baixo; 0.45 segura o céu e o topo das condensadoras e tira mais da
# telha vazia do primeiro plano.
FOCO = 0.45

MARCA_OG = 0.22
MARGEM_OG = 0.06


def corta(foto, foco):
    """Recorta a maior região 1200x630 da foto, na faixa apontada pelo foco."""
    largura, altura = foto.size
    if largura / altura > PROPORCAO:          # sobra largura: tira das laterais
        corte_l, corte_a = round(altura * PROPORCAO), altura
    else:                                     # sobra altura: tira de cima e de baixo
        corte_l, corte_a = largura, round(largura / PROPORCAO)
    x = round((largura - corte_l) * 0.5)
    y = round((altura - corte_a) * foco)
    return foto.crop((x, y, x + corte_l, y + corte_a))


def main():
    if not ORIGEM.exists():
        raise SystemExit(f"falta o original {ORIGEM}")
    logo = Image.open(LOGO).convert("RGBA")
    foto = corta(Image.open(ORIGEM).convert("RGB"), FOCO)
    foto = foto.resize((LARGURA, ALTURA), Image.LANCZOS)
    foto = carimba(foto, logo, None, MARCA_OG, MARGEM_OG)
    foto.save(DESTINO, quality=QUALIDADE, optimize=True, progressive=True)
    print(f"{DESTINO.name}: {LARGURA}x{ALTURA} + marca")


if __name__ == "__main__":
    main()
