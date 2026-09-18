#!/usr/bin/env python3
"""Servidor local do site, na 8085 e sem cache nenhum.

    python3 tools/servir.py

Usar `python3 -m http.server` direto custou caro em 18/09/2026: ele não manda
`Cache-Control`, o navegador guarda o HTML e as fotos por conta própria e o
Caio passou três rodadas revendo a versão antiga e dizendo que a mudança não
tinha aparecido. Com `no-store` o que está na tela é sempre o arquivo que está
no disco agora."""
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer


class SemCache(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def log_message(self, *a):
        pass


ThreadingHTTPServer(("127.0.0.1", 8085), SemCache).serve_forever()
