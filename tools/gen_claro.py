#!/usr/bin/env python3
# Recolore a V6 Definitiva (produção, escura) para 2 variantes claras — SEM
# mudar estrutura/HTML/JS, só cores. Gera v7-claro-a.html e v7-claro-b.html
# na raiz do repo, a partir do index.html atual (fonte = V6 publicada).
import pathlib, sys

ROOT = pathlib.Path(__file__).parent.parent
SRC = ROOT / "v6-definitiva.html"
src = SRC.read_text(encoding="utf-8")

def sub(s, old, new, expect=1):
    n = s.count(old)
    if n != expect:
        sys.exit(f"ERRO: trecho encontrado {n}x (esperado {expect}):\n{old[:120]}")
    return s.replace(old, new)

# ---------------------------------------------------------------- comum às 2 variantes
common = src

common = sub(common,
    '''  :root{
    --azul:#24549C; --azul-deep:#0B2A52; --azul-night:#061B36;
    --frio:#00A8F0; --frio-2:#48C6FF;
    --quente:#FF6B1A; --quente-2:#FFA23A; --brasa:#D93A0B;
    --line:rgba(255,255,255,.16);
''',
    '''  :root{
    --azul:#24549C; --azul-deep:#0B2A52; --azul-night:#061B36;
    --frio:#00A8F0; --frio-2:#48C6FF;
    --quente:#FF6B1A; --quente-2:#FFA23A; --brasa:#D93A0B;
    /* == paletas por variante (injetadas abaixo) == */
    __PALETTE__
    --line:var(--line-cor);
''')

common = sub(common,
    '''  body{font-family:Barlow,system-ui,sans-serif;background:var(--azul-night);color:#fff;
    font-size:17.5px;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}''',
    '''  body{font-family:Barlow,system-ui,sans-serif;background:var(--paper);color:var(--ink);
    font-size:17.5px;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}''')

# fundo fixo: apaga a foto industrial (ficava escura), mantém só o véu de temperatura,
# agora em tons claros de papel — mesmo mecanismo (--h cruza os dois), sem a foto.
common = sub(common,
    '''  .bg{position:fixed;inset:0;pointer-events:none;background-size:cover;background-position:center;
    background-blend-mode:luminosity;background-repeat:no-repeat;filter:contrast(1.2) saturate(1.5)}
  .bg-frio{z-index:-4;background-image:url("assets/bg-industrial.jpg"),linear-gradient(#1478C8,#1478C8);
    opacity:calc(.32 * (1 - var(--h)))}
  .bg-quente{z-index:-3;background-image:url("assets/bg-industrial.jpg"),linear-gradient(#FF6B1A,#FF6B1A);
    opacity:calc(.42 * var(--h))}
  .veu-frio{position:fixed;inset:0;z-index:-2;pointer-events:none;opacity:calc(1 - var(--h));
    background:linear-gradient(180deg,rgba(6,27,54,.78),rgba(6,27,54,.9))}
  .veu-quente{position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:var(--h);
    background:linear-gradient(180deg,rgba(30,11,4,.72),rgba(30,11,4,.88))}''',
    '''  .bg{position:fixed;inset:0;pointer-events:none}
  .bg-frio{z-index:-4;opacity:0}
  .bg-quente{z-index:-3;opacity:0}
  .veu-frio{position:fixed;inset:0;z-index:-2;pointer-events:none;opacity:calc(1 - var(--h));
    background:linear-gradient(180deg,var(--paper),var(--paper-2))}
  .veu-quente{position:fixed;inset:0;z-index:-1;pointer-events:none;opacity:var(--h);
    background:linear-gradient(180deg,#FFF4EC,#FFE3CE)}''')

common = sub(common,
    '''  .thermo__val{font-family:"Bebas Neue",sans-serif;font-size:23px;letter-spacing:.04em;
    color:#fff;text-shadow:0 2px 10px rgba(0,0,0,.6)}
  .thermo__lab{font-family:"Barlow Condensed",sans-serif;font-size:11px;letter-spacing:.2em;
    text-transform:uppercase;color:rgba(255,255,255,.55);writing-mode:vertical-rl}''',
    '''  .thermo__val{font-family:"Bebas Neue",sans-serif;font-size:23px;letter-spacing:.04em;
    color:var(--ink);text-shadow:0 2px 8px rgba(11,42,82,.15)}
  .thermo__lab{font-family:"Barlow Condensed",sans-serif;font-size:11px;letter-spacing:.2em;
    text-transform:uppercase;color:var(--ink-soft);writing-mode:vertical-rl}''')
common = sub(common,
    '''  .thermo__dot{position:absolute;left:50%;width:16px;height:16px;border-radius:50%;
    transform:translate(-50%,-50%);background:#fff;top:calc(var(--tp) * 100%);
    box-shadow:0 0 0 4px rgba(255,255,255,.18),0 0 18px 2px rgba(255,255,255,.5);
    transition:top .12s linear}''',
    '''  .thermo__dot{position:absolute;left:50%;width:16px;height:16px;border-radius:50%;
    transform:translate(-50%,-50%);background:#fff;top:calc(var(--tp) * 100%);
    box-shadow:0 0 0 4px rgba(11,42,82,.12),0 0 14px 2px rgba(11,42,82,.28);
    transition:top .12s linear}''')

common = sub(common,
    '''  .btn--frio:hover{background:#fff;transform:translate(-3px,-3px);box-shadow:6px 6px 0 var(--frio)}''',
    '''  .btn--frio:hover{background:var(--ink);color:#fff;transform:translate(-3px,-3px);box-shadow:6px 6px 0 var(--frio)}''')
common = sub(common,
    '''  .btn--quente:hover{background:#fff;transform:translate(-3px,-3px);box-shadow:6px 6px 0 var(--quente)}''',
    '''  .btn--quente:hover{background:var(--ink);color:#fff;transform:translate(-3px,-3px);box-shadow:6px 6px 0 var(--quente)}''')
common = sub(common,
    '''  .btn--out{border-color:#fff;color:#fff}
  .btn--out:hover{background:#fff;color:var(--azul-deep);transform:translate(-3px,-3px);
    box-shadow:6px 6px 0 rgba(255,255,255,.35)}''',
    '''  .btn--out{border-color:var(--ink);color:var(--ink)}
  .btn--out:hover{background:var(--ink);color:#fff;transform:translate(-3px,-3px);
    box-shadow:6px 6px 0 rgba(11,42,82,.18)}''')

common = sub(common,
    '''    background-image:linear-gradient(rgba(20,8,3,var(--h)),rgba(20,8,3,var(--h)));''',
    '''    background-image:linear-gradient(rgba(255,232,214,var(--h)),rgba(255,232,214,var(--h)));''')

common = sub(common,
    '''  .hero__lead{font-size:20px;color:#C6DAEE;font-weight:300;max-width:46ch}
  .hero__lead b{color:#fff;font-weight:600}''',
    '''  .hero__lead{font-size:20px;color:var(--ink-soft);font-weight:300;max-width:46ch}
  .hero__lead b{color:var(--ink);font-weight:600}''')
common = sub(common,
    '''  .hero__side span{font-size:14.5px;color:#A9C2DA;line-height:1.4;display:block}''',
    '''  .hero__side span{font-size:14.5px;color:var(--ink-soft);line-height:1.4;display:block}''')

common = sub(common,
    '''  .sec__head p{margin-left:auto;color:#A9C2DA;max-width:34ch;font-size:16px;font-weight:300;
    text-align:right;flex:none}''',
    '''  .sec__head p{margin-left:auto;color:var(--ink-soft);max-width:34ch;font-size:16px;font-weight:300;
    text-align:right;flex:none}''')

common = sub(common,
    '''  .prob{background:rgba(30,11,4,.86);padding:34px 28px;position:relative;overflow:hidden;
    transition:background .3s, transform .3s}''',
    '''  .prob{background:#fff;padding:34px 28px;position:relative;overflow:hidden;
    transition:background .3s, transform .3s}''')
common = sub(common,
    '''  .prob p{font-size:15.5px;color:#D5BCAE;font-weight:300;line-height:1.55}''',
    '''  .prob p{font-size:15.5px;color:var(--ink-soft);font-weight:300;line-height:1.55}''')
common = sub(common,
    '''  .probs-head p{color:#D9C2B4}''',
    '''  .probs-head p{color:var(--ink-soft)}''')

common = sub(common,
    '''  .virada{position:relative;padding:120px 0;text-align:center;overflow:hidden;
    background:linear-gradient(180deg,rgba(30,11,4,0),rgba(30,11,4,.3) 26%,rgba(6,27,54,.62))}''',
    '''  .virada{position:relative;padding:120px 0;text-align:center;overflow:hidden;
    background:linear-gradient(180deg,rgba(255,244,236,0),rgba(255,244,236,.6) 26%,var(--paper-2))}''')
common = sub(common,
    '''  .virada p{position:relative;z-index:2;color:#CFE0F0;max-width:52ch;margin:16px auto 0;
    font-weight:300;font-size:18px}''',
    '''  .virada p{position:relative;z-index:2;color:var(--ink-soft);max-width:52ch;margin:16px auto 0;
    font-weight:300;font-size:18px}''')

common = sub(common,
    '''  .flake{position:absolute;top:-20px;color:rgba(140,215,255,.55);font-size:13px;
    animation:fall linear infinite}''',
    '''  .flake{position:absolute;top:-20px;color:rgba(36,84,156,.4);font-size:13px;
    animation:fall linear infinite}''')

common = sub(common,
    '''  .blk li{padding:13px 0 13px 34px;position:relative;border-top:1px solid var(--line);font-size:16.5px}
  .blk li::before{content:"";position:absolute;left:0;top:19px;width:16px;height:3px;background:var(--frio)}
  .blk--cyan li::before{background:#04121F}''',
    '''  .blk li{padding:13px 0 13px 34px;position:relative;border-top:1px solid var(--line);font-size:16.5px}
  .blk li::before{content:"";position:absolute;left:0;top:19px;width:16px;height:3px;background:var(--frio)}
  .blk--cyan li::before{background:#04121F}
  .blk--dark li,.blk--cyan li{border-top-color:rgba(255,255,255,.2)}''')

common = sub(common,
    '''  .gc{background:rgba(6,27,54,.86);padding:32px 26px;position:relative;
    transition:background .25s, transform .25s}''',
    '''  .gc{background:#fff;padding:32px 26px;position:relative;
    transition:background .25s, transform .25s}''')
common = sub(common,
    '''  .gc p{font-size:14.5px;color:rgba(255,255,255,.72);line-height:1.5}''',
    '''  .gc p{font-size:14.5px;color:var(--ink-soft);line-height:1.5}''')

common = sub(common,
    '''  .rail::-webkit-scrollbar-track{background:rgba(255,255,255,.08)}''',
    '''  .rail::-webkit-scrollbar-track{background:rgba(11,42,82,.08)}''')
common = sub(common,
    '''  .rail__hint{font-family:"Barlow Condensed",sans-serif;letter-spacing:.16em;text-transform:uppercase;
    font-size:13.5px;color:#7C96B0;margin-top:8px}''',
    '''  .rail__hint{font-family:"Barlow Condensed",sans-serif;letter-spacing:.16em;text-transform:uppercase;
    font-size:13.5px;color:var(--ink-soft);margin-top:8px}''')

common = sub(common,
    '''  .about p{color:#B9CEE2;margin-bottom:16px;max-width:56ch;font-weight:300}
  .about p b{color:#fff;font-weight:600}''',
    '''  .about p{color:var(--ink-soft);margin-bottom:16px;max-width:56ch;font-weight:300}
  .about p b{color:var(--ink);font-weight:600}''')
common = sub(common,
    '''  .about__nums div{background:rgba(6,27,54,.86);padding:24px 20px}''',
    '''  .about__nums div{background:#fff;padding:24px 20px}''')
common = sub(common,
    '''  .about__nums span{font-size:13.5px;color:#9FB8D0}''',
    '''  .about__nums span{font-size:13.5px;color:var(--ink-soft)}''')

common = sub(common,
    '''  .cli__item{background:rgba(6,27,54,.86);padding:26px 24px;display:flex;flex-direction:column;
    align-items:center;justify-content:center;gap:16px;transition:background .25s}''',
    '''  .cli__item{background:#fff;padding:26px 24px;display:flex;flex-direction:column;
    align-items:center;justify-content:center;gap:16px;transition:background .25s}''')
common = sub(common,
    '''  .cli__nota{margin-top:26px;font-size:14.5px;color:#7C96B0;font-weight:300}''',
    '''  .cli__nota{margin-top:26px;font-size:14.5px;color:var(--ink-soft);font-weight:300}''')

common = sub(common,
    '''  .contato p{color:#B4CBE1;max-width:56ch;margin:0 auto 34px;font-weight:300;font-size:18.5px}''',
    '''  .contato p{color:var(--ink-soft);max-width:56ch;margin:0 auto 34px;font-weight:300;font-size:18.5px}''')
common = sub(common,
    '''  .contato__info{display:flex;gap:36px;justify-content:center;flex-wrap:wrap;margin-top:44px;
    padding-top:30px;border-top:1px solid var(--line);font-size:16px;color:#A9C2DA}''',
    '''  .contato__info{display:flex;gap:36px;justify-content:center;flex-wrap:wrap;margin-top:44px;
    padding-top:30px;border-top:1px solid var(--line);font-size:16px;color:var(--ink-soft)}''')

# ---------------------------------------------------------------- variante A: Claro Editorial
A_PALETTE = '''--paper:#FFFFFF; --paper-2:#F3F8FD; --ink:#0B2A52; --ink-soft:#4A6A8F; --line-cor:rgba(11,42,82,.12);'''
a = common.replace('__PALETTE__', A_PALETTE)

a = sub(a, '<title>V6 Definitiva · Arclimtec — Soluções em Climatização</title>',
    '<title>V7 Claro A · Editorial · Arclimtec</title>')

a = sub(a,
    '''  header.nav{position:sticky;top:0;z-index:40;backdrop-filter:blur(10px);
    background-color:rgba(6,27,54,.86);''',
    '''  header.nav{position:sticky;top:0;z-index:40;backdrop-filter:blur(10px);
    background-color:rgba(255,255,255,.86);''')
a = sub(a,
    '''  footer{background:#04121F;padding:40px 0;border-top:3px solid var(--frio)}
  .foot{display:flex;gap:20px;align-items:center;flex-wrap:wrap;font-size:14px;color:#7C96B0}''',
    '''  footer{background:var(--paper-2);padding:40px 0;border-top:3px solid var(--frio)}
  .foot{display:flex;gap:20px;align-items:center;flex-wrap:wrap;font-size:14px;color:var(--ink-soft)}''', expect=1)
a = sub(a,
    '''  .card__b{background:rgba(11,42,82,.92);border-left:3px solid var(--frio);padding:20px 22px}
  .card__b i{font-style:normal;font-family:"Barlow Condensed",sans-serif;font-weight:700;font-size:13.5px;
    letter-spacing:.2em;text-transform:uppercase;color:var(--frio);display:block;margin-bottom:5px}
  .card__b b{font-family:"Bebas Neue",sans-serif;font-size:27px;display:block;line-height:1;margin-bottom:8px}
  .card__b p{font-size:14.5px;color:#B4CBE1;font-weight:300;line-height:1.5}''',
    '''  .card__b{background:var(--azul-deep);border-left:3px solid var(--frio);padding:20px 22px}
  .card__b i{font-style:normal;font-family:"Barlow Condensed",sans-serif;font-weight:700;font-size:13.5px;
    letter-spacing:.2em;text-transform:uppercase;color:var(--frio);display:block;margin-bottom:5px}
  .card__b b{font-family:"Bebas Neue",sans-serif;font-size:27px;display:block;line-height:1;margin-bottom:8px}
  .card__b p{font-size:14.5px;color:#C6DAEE;font-weight:300;line-height:1.5}''')
# nav/rodapé claros -> logo colorida (não a branca, feita p/ fundo escuro)
a = a.replace('assets/logo-branca.png', 'assets/logo.png')

(ROOT / "v7-claro-a.html").write_text(a, encoding="utf-8")

# ---------------------------------------------------------------- variante B: Claro Técnico
B_PALETTE = '''--paper:#F5F9FD; --paper-2:#E3EFFB; --ink:#0B2740; --ink-soft:#3E6690; --line-cor:rgba(11,42,82,.14);'''
b = common.replace('__PALETTE__', B_PALETTE)

b = sub(b, '<title>V6 Definitiva · Arclimtec — Soluções em Climatização</title>',
    '<title>V7 Claro B · Técnico · Arclimtec</title>')

# nav e rodapé em azul sólido da marca (fundo continua claro no resto da página)
b = sub(b,
    '''  header.nav{position:sticky;top:0;z-index:40;backdrop-filter:blur(10px);
    background-color:rgba(6,27,54,.86);''',
    '''  header.nav{position:sticky;top:0;z-index:40;backdrop-filter:blur(10px);
    background-color:rgba(11,42,82,.94);''')
b = sub(b,
    '''  footer{background:#04121F;padding:40px 0;border-top:3px solid var(--frio)}
  .foot{display:flex;gap:20px;align-items:center;flex-wrap:wrap;font-size:14px;color:#7C96B0}''',
    '''  footer{background:var(--azul-deep);padding:40px 0;border-top:3px solid var(--frio)}
  .foot{display:flex;gap:20px;align-items:center;flex-wrap:wrap;font-size:14px;color:rgba(255,255,255,.65)}''', expect=1)
# projetos: legenda clara (com contorno) em vez de barra azul sólida — mais leve que a A
b = sub(b,
    '''  .card__b{background:rgba(11,42,82,.92);border-left:3px solid var(--frio);padding:20px 22px}
  .card__b i{font-style:normal;font-family:"Barlow Condensed",sans-serif;font-weight:700;font-size:13.5px;
    letter-spacing:.2em;text-transform:uppercase;color:var(--frio);display:block;margin-bottom:5px}
  .card__b b{font-family:"Bebas Neue",sans-serif;font-size:27px;display:block;line-height:1;margin-bottom:8px}
  .card__b p{font-size:14.5px;color:#B4CBE1;font-weight:300;line-height:1.5}''',
    '''  .card__b{background:#fff;border-left:3px solid var(--frio);padding:20px 22px;
    box-shadow:inset 0 0 0 1px rgba(11,42,82,.1)}
  .card__b i{font-style:normal;font-family:"Barlow Condensed",sans-serif;font-weight:700;font-size:13.5px;
    letter-spacing:.2em;text-transform:uppercase;color:var(--azul);display:block;margin-bottom:5px}
  .card__b b{font-family:"Bebas Neue",sans-serif;font-size:27px;display:block;line-height:1;margin-bottom:8px;color:var(--ink)}
  .card__b p{font-size:14.5px;color:var(--ink-soft);font-weight:300;line-height:1.5}''')
# ritmo de seções alternando papel/papel-2 (só cor de fundo, mesma estrutura)
b = sub(b,
    '''  @media (max-width:980px){''',
    '''  #problemas,#empresa{background:var(--paper-2)}

  @media (max-width:980px){''', expect=1)
# nav/rodapé escuros nesta variante -> logo branca (feita p/ fundo escuro)
# (o resto do body já usa a logo branca originalmente só nesses 2 lugares, então não mexe)

(ROOT / "v7-claro-b.html").write_text(b, encoding="utf-8")

print("ok: v7-claro-a.html, v7-claro-b.html")
