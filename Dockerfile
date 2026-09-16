FROM nginx:alpine

# Site 100% estático. Funciona igual em qualquer branch:
# nas branches de versão existe só o index.html; em main vem o site inteiro.
COPY *.html /usr/share/nginx/html/
COPY assets/ /usr/share/nginx/html/assets/

# Arquivos de raiz que o Google e o navegador procuram por nome fixo.
COPY robots.txt sitemap.xml site.webmanifest favicon.ico apple-touch-icon.png icon-512.png /usr/share/nginx/html/

# gzip nos textos, cache de 30 dias nas fotos e troca automática por webp
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
