FROM nginx:alpine

# Site 100% estático. Funciona igual em qualquer branch:
# nas branches de versão existe só o index.html; em main vêm também
# os arquivos v1-*/v2-*/v3-* e o index.html de comparação.
COPY *.html /usr/share/nginx/html/
COPY assets/ /usr/share/nginx/html/assets/

# gzip nos textos e cache longo nas fotos (a página é pesada de imagem)
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
