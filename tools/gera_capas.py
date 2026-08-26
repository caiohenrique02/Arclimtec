#!/usr/bin/env python3
"""Gera a página de escolha de capa da Arclimtec em dois formatos.

  repo     — arquivo pro repositório: caminhos relativos de assets, UTF-8,
             documento completo (doctype/html/head/body).
  artifact — arquivo pro Artifact: todo asset em data URI, ASCII puro (o
             wrapper do Artifact injeta o <head>, então um <meta charset>
             nosso cairia no <body>, tarde demais pra valer) e sem esqueleto.

Uso: gera_capas.py <build_dir> <repo_out.html> <artifact_out.html>
"""
import base64, mimetypes, os, re, sys

BASE, OUT_REPO, OUT_ART = sys.argv[1], sys.argv[2], sys.argv[3]

# ---------------------------------------------------------------- capas ------
CAPAS = [
    {'k': 'a', 'nome': 'Capa A', 'img': 'assets/p-capa-planta-baixa.jpg',
     'linha': 'Planta baixa do pavimento',
     'sub': 'Arrastar o divisor troca a fachada pela planta: as evaporadoras '
            'e o traçado das linhas frigorígenas sala por sala.',
     'alt': 'Planta baixa de pavimento com as evaporadoras e o traçado das '
            'linhas frigorígenas em azul e vermelho'},
    {'k': 'b', 'nome': 'Capa B', 'img': 'assets/p-capa-predio-tecnico.jpg',
     'linha': 'O prédio em desenho técnico',
     'sub': 'É o mesmo prédio dos dois lados. Arrastar o divisor é um raio-X: '
            'sai a fachada, entra a tubulação.',
     'alt': 'Mesmo edifício em desenho técnico isométrico, com as linhas '
            'frigorígenas e a rede dutada em azul e vermelho sobre o traçado '
            'da estrutura'},
]
IMG_ESQ = 'assets/p-capa-predio-render.jpg'   # igual nas duas


def jsstr(t):
    return '"%s"' % t.replace('\\', '\\\\').replace('"', '\\"')


# ------------------------------------------------------------------ css ------
CSS = '''
<style>
  /* ===== tela de escolha da capa — só nesta prévia, não vai pro site ===== */
  .esc{position:fixed;inset:0;z-index:200;display:flex;align-items:flex-start;justify-content:center;
    padding:32px 20px;overflow:auto;background:rgba(255,255,255,.93);
    backdrop-filter:blur(8px);-webkit-backdrop-filter:blur(8px)}
  .esc[hidden]{display:none}
  .esc__in{width:100%;max-width:940px;margin:auto;display:flex;flex-direction:column;align-items:center;gap:6px}
  .esc__logo{width:186px;height:auto;margin-bottom:10px}
  .esc__eyebrow{font-family:"Barlow Condensed",sans-serif;font-weight:600;font-size:13px;
    letter-spacing:.16em;text-transform:uppercase;color:var(--frio)}
  .esc__h{font-family:"Bebas Neue",sans-serif;font-size:clamp(30px,4.4vw,46px);line-height:1.04;
    letter-spacing:.01em;color:var(--ink);text-align:center;text-wrap:balance}
  .esc__lead{font-size:16.5px;font-weight:300;color:var(--ink-soft);text-align:center;
    max-width:56ch;margin-bottom:14px}
  .esc__cards{display:grid;grid-template-columns:1fr 1fr;gap:22px;width:100%}
  .esc__c{appearance:none;cursor:pointer;text-align:left;padding:0;overflow:hidden;
    background:var(--paper);border:1px solid var(--line);border-radius:var(--r-lg);
    box-shadow:var(--shadow-1);transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease}
  .esc__c:hover{transform:translateY(-4px);border-color:var(--frio);box-shadow:var(--shadow-2)}
  .esc__c:focus-visible{outline:2px solid var(--azul);outline-offset:3px}
  .esc__prev{display:flex;height:200px;background:#fff;border-bottom:1px solid var(--line)}
  .esc__prev i{display:block;background:#fff center/contain no-repeat}
  .esc__prev i:first-child{flex:0 0 52%;border-right:1px solid var(--line)}
  .esc__prev i:last-child{flex:1}
  .esc__txt{display:block;padding:18px 22px 22px}
  .esc__n{display:block;font-family:"Bebas Neue",sans-serif;font-size:26px;letter-spacing:.02em;color:var(--ink)}
  .esc__l{display:block;font-family:"Barlow Condensed",sans-serif;font-weight:600;font-size:13px;
    letter-spacing:.12em;text-transform:uppercase;color:var(--frio);margin-top:2px}
  .esc__s{display:block;font-size:14.5px;font-weight:300;line-height:1.5;color:var(--ink-soft);margin-top:9px}
  .esc__pe{font-size:13.5px;color:var(--ink-soft);margin-top:16px}
  html.esc-aberta{overflow:hidden}

  /* ===== barra da capa em uso, com volta pra tela de escolha ===== */
  .ab{position:fixed;left:18px;bottom:18px;z-index:60;display:flex;align-items:center;gap:10px;
    padding:8px 10px 8px 15px;border-radius:999px;background:var(--paper);
    border:1px solid var(--line);box-shadow:var(--shadow-1),0 18px 40px -24px rgba(11,42,82,.45)}
  .ab[hidden]{display:none}
  .ab__q{font-family:"Barlow Condensed",sans-serif;font-weight:600;font-size:14px;
    letter-spacing:.1em;text-transform:uppercase;color:var(--ink);white-space:nowrap}
  .ab__b{appearance:none;border:1px solid var(--line);cursor:pointer;border-radius:999px;
    padding:7px 14px;font-family:"Barlow Condensed",sans-serif;font-weight:600;font-size:13.5px;
    letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);background:var(--paper-2);
    white-space:nowrap;transition:background .18s ease,color .18s ease,border-color .18s ease}
  .ab__b:hover{background:var(--frio);border-color:var(--frio);color:#fff}
  .ab__b:focus-visible{outline:2px solid var(--azul);outline-offset:2px}

  @media (max-width:760px){
    .esc__cards{grid-template-columns:1fr}
    .esc__prev{height:170px}
    .esc__logo{width:150px}
  }
  @media (max-width:640px){
    .ab{left:12px;right:78px;bottom:14px;justify-content:center;padding:7px 10px} /* deixa o botao do WhatsApp livre */
    .ab__q{font-size:13px}
  }
  @media (prefers-reduced-motion:reduce){
    .esc__c,.ab__b{transition:none}
    .esc__c:hover{transform:none}
  }
</style>
'''

# ----------------------------------------------------------------- html ------
cards = '\n'.join('''      <button class="esc__c" type="button" data-capa="%(k)s">
        <span class="esc__prev" aria-hidden="true">
          <i style="background-image:url('%(esq)s')"></i>
          <i style="background-image:url('%(img)s')"></i>
        </span>
        <span class="esc__txt">
          <span class="esc__n">%(nome)s</span>
          <span class="esc__l">%(linha)s</span>
          <span class="esc__s">%(sub)s</span>
        </span>
      </button>''' % dict(c, esq=IMG_ESQ) for c in CAPAS)

HTML = '''
<div class="esc" id="esc" role="dialog" aria-modal="true" aria-labelledby="escH">
  <div class="esc__in">
    <img class="esc__logo" id="escLogo" src="%(logo)s" alt="Arclimtec">
    <span class="esc__eyebrow">Proposta de capa</span>
    <h2 class="esc__h" id="escH">Duas capas pro topo do site.<br>Abra a que quiser ver.</h2>
    <p class="esc__lead">O prédio da esquerda é o mesmo nas duas. O que muda é a imagem que
      aparece quando o divisor da capa é arrastado.</p>
    <div class="esc__cards">
%(cards)s
    </div>
    <p class="esc__pe">Depois de abrir, a barra no canto de baixo troca de capa sem precisar voltar aqui.</p>
  </div>
</div>

<div class="ab" id="ab" role="group" aria-label="Capa em uso" hidden>
  <span class="ab__q" id="abQ">Capa</span>
  <button class="ab__b" type="button" id="abTroca">Ver a outra</button>
  <button class="ab__b" type="button" id="abVolta">As duas</button>
</div>
''' % {'logo': 'assets/logo.png', 'cards': cards}

# ------------------------------------------------------------------- js ------
JS = '''
<script>
(function(){
  var CAPAS = {%(mapa)s};
  var ORDEM = [%(ordem)s];
  var img = document.querySelector('.capa__planta img');
  var esc = document.getElementById('esc');
  var ab  = document.getElementById('ab');
  var q   = document.getElementById('abQ');
  var troca = document.getElementById('abTroca');
  var volta = document.getElementById('abVolta');
  if(!img || !esc || !ab) return;
  var atual = null;

  function poe(k){
    var c = CAPAS[k]; if(!c) return;
    atual = k;
    img.src = c.img; img.alt = c.alt;
    q.textContent = c.nome + ' \\u2014 ' + c.linha;
    troca.textContent = 'Ver a ' + CAPAS[outra()].nome;
  }
  function outra(){
    return ORDEM[(ORDEM.indexOf(atual) + 1) %% ORDEM.length];
  }
  function abre(k){
    poe(k);
    esc.hidden = true; ab.hidden = false;
    document.documentElement.classList.remove('esc-aberta');
    window.scrollTo(0, 0);
    troca.focus();
  }
  function escolhe(){
    esc.hidden = false; ab.hidden = true;
    document.documentElement.classList.add('esc-aberta');
  }

  esc.querySelectorAll('.esc__c').forEach(function(b){
    b.addEventListener('click', function(){ abre(b.getAttribute('data-capa')); });
  });
  troca.addEventListener('click', function(){ abre(outra()); });
  volta.addEventListener('click', escolhe);
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' && !esc.hidden && atual) abre(atual);
  });

  // a logo da tela de escolha e a mesma do topo — evita repetir a imagem
  var topo = document.querySelector('.brand img');
  var escLogo = document.getElementById('escLogo');
  if(topo && escLogo) escLogo.src = topo.src;

  atual = ORDEM[0];
  esc.hidden = false; ab.hidden = true;
  document.documentElement.classList.add('esc-aberta');
})();
</script>
''' % {
    'mapa': ','.join('%s:{img:%s,alt:%s,nome:%s,linha:%s}' % (
        c['k'], jsstr(c['img']), jsstr(c['alt']), jsstr(c['nome']), jsstr(c['linha']))
        for c in CAPAS),
    'ordem': ','.join(jsstr(c['k']) for c in CAPAS),
}


# --------------------------------------------------------------- montagem ----
src = open(os.path.join(BASE, 'index.html'), encoding='utf-8').read()
assert src.count('</title>') == 1 and src.count('</body>') == 1

TITULO_REPO = 'Arclimtec — escolha da capa'
TITULO_ART = 'Capa Arclimtec'


AVISO = ('<!-- GERADO por tools/gera_capas.py a partir do index.html da branch\n     v13-capa-b. Nao edite este arquivo a mao: mexa no site na branch da\n     versao e rode o gerador de novo. -->\n')


def monta(titulo):
    d = re.sub(r'<title>.*?</title>', '<title>%s</title>' % titulo, src, count=1, flags=re.S)
    d = d.replace('</head>', CSS + '</head>', 1)
    return d.replace('</body>', HTML + JS + '</body>', 1)


# --- repo: documento completo, assets relativos ------------------------------
d = monta(TITULO_REPO)
d = re.sub(r'(<!DOCTYPE html>\s*)', r'\1' + AVISO, d, count=1, flags=re.I)
open(OUT_REPO, 'w', encoding='utf-8').write(d)
print('repo     -> %s (%.0f KB)' % (OUT_REPO, os.path.getsize(OUT_REPO) / 1024))

# --- artifact: assets em data URI, sem esqueleto, ASCII puro -----------------
doc = monta(TITULO_ART)


def datauri(rel):
    p = os.path.join(BASE, rel)
    if not os.path.exists(p):
        sys.exit('asset ausente: ' + rel)
    mime = mimetypes.guess_type(p)[0] or 'application/octet-stream'
    with open(p, 'rb') as f:
        return 'data:%s;base64,%s' % (mime, base64.b64encode(f.read()).decode('ascii'))


refs = sorted(set(re.findall(r'assets/[A-Za-z0-9._/-]+', doc)), key=len, reverse=True)
for r in refs:
    doc = doc.replace(r, datauri(r))
print('artifact -> %d assets embutidos' % len(refs))

doc = re.sub(r'^\s*<!DOCTYPE html>\s*', '', doc, flags=re.I)
for t in ('html', 'head', 'body'):
    doc = re.sub(r'</?%s[^>]*>\s*' % t, '', doc, flags=re.I)
doc = re.sub(r'<meta charset[^>]*>\s*', '', doc, flags=re.I)
doc = re.sub(r'<meta name="viewport"[^>]*>\s*', '', doc, flags=re.I)
doc = doc.strip()
assert doc.startswith('<title>'), doc[:120]


def asciify(d):
    def js(m):
        return '<script%s>%s</script>' % (m.group(1), re.sub(
            r'[^\x00-\x7f]', lambda c: '\\u%04x' % ord(c.group()), m.group(2)))

    def css(m):
        return '<style%s>%s</style>' % (m.group(1), re.sub(
            r'[^\x00-\x7f]', lambda c: '\\%06x' % ord(c.group()), m.group(2)))

    d = re.sub(r'<script([^>]*)>(.*?)</script>', js, d, flags=re.S)
    d = re.sub(r'<style([^>]*)>(.*?)</style>', css, d, flags=re.S)
    return d.encode('ascii', 'xmlcharrefreplace').decode('ascii')


doc = asciify(doc)
assert not [c for c in doc if ord(c) > 127]
open(OUT_ART, 'w', encoding='ascii').write(doc)
print('artifact -> %s (%.1f MB)' % (OUT_ART, os.path.getsize(OUT_ART) / 1048576))
