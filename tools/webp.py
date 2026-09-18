#!/usr/bin/env python3
"""Gera o irmão .webp de cada imagem de assets/.

    python3 tools/webp.py

O nginx serve `foto.jpg.webp` no lugar de `foto.jpg` quando o navegador
aceita WebP (ver o `map` do default.conf), então o nome do irmão é o nome
completo mais `.webp` — e sem ele a foto é a única do site que não pega a
otimização. Só regrava quem está faltando ou mais velho que o original, então
dá pra rodar depois de qualquer mexida em foto.
"""

import subprocess
from pathlib import Path

from PIL import Image

ASSETS = Path(__file__).resolve().parent.parent / "assets"
FORMATOS = (".jpg", ".jpeg", ".png")
QUALIDADE = 80


def ignorado(caminho):
    """True se o git ignora o arquivo: é referência interna, não vai ao ar."""
    return subprocess.run(
        ["git", "check-ignore", "-q", str(caminho)], cwd=ASSETS.parent
    ).returncode == 0


def main():
    for origem in sorted(ASSETS.iterdir()):
        if origem.suffix.lower() not in FORMATOS or ignorado(origem):
            continue
        destino = origem.with_name(origem.name + ".webp")
        if destino.exists() and destino.stat().st_mtime >= origem.stat().st_mtime:
            continue

        imagem = Image.open(origem)
        # PNG pode ter transparência (a logo tem), JPEG nunca
        imagem = imagem.convert("RGBA" if imagem.mode in ("RGBA", "LA", "P") else "RGB")
        imagem.save(destino, "WEBP", quality=QUALIDADE, method=6)
        antes, depois = origem.stat().st_size, destino.stat().st_size
        print(f"{destino.name}: {antes // 1024} KB -> {depois // 1024} KB")


if __name__ == "__main__":
    main()
