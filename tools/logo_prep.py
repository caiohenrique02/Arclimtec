#!/usr/bin/env python3
"""Extrai a paleta da logo da Arclimtec e gera versões com fundo transparente."""
from PIL import Image
import colorsys, collections, pathlib

A = pathlib.Path("/home/caio/arclimtec-site/assets")
img = Image.open(A / "logo.jpg").convert("RGB")

# --- paleta: cores saturadas mais frequentes ---
small = img.resize((img.width // 2, img.height // 2))
buckets = collections.Counter()
for r, g, b in small.getdata():
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    if s < .35 or v < .12:          # ignora branco/cinza/preto
        continue
    buckets[(r // 12 * 12, g // 12 * 12, b // 12 * 12)] += 1

print("cores dominantes da logo:")
for (r, g, b), n in buckets.most_common(8):
    h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    print(f"  #{r:02X}{g:02X}{b:02X}  px={n:>6}  h={h*360:5.1f} s={s:.2f} v={v:.2f}")

# --- logo com fundo transparente (branco -> alpha) ---
rgba = img.convert("RGBA")
px = rgba.load()
w, h = rgba.size
for y in range(h):
    for x in range(w):
        r, g, b, _ = px[x, y]
        mn, mx = min(r, g, b), max(r, g, b)
        if mn > 236 and mx - mn < 14:            # branco puro do fundo
            px[x, y] = (r, g, b, 0)
        elif mn > 205 and mx - mn < 22:          # antialias claro -> alpha parcial
            px[x, y] = (r, g, b, int((255 - mn) * 255 / 50))
rgba = rgba.crop(rgba.getbbox())
rgba.save(A / "logo.png")
print("logo.png", rgba.size)

# --- versão branca (para fundos escuros) ---
mono = Image.new("RGBA", rgba.size, (255, 255, 255, 0))
mp, sp = mono.load(), rgba.load()
for y in range(rgba.height):
    for x in range(rgba.width):
        *_, a = sp[x, y]
        if a:
            mp[x, y] = (255, 255, 255, a)
mono.save(A / "logo-branca.png")
print("logo-branca.png", mono.size)
