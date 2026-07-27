#!/usr/bin/env python3
"""Publica cada versão da LP da Arclimtec em uma branch própria, já como index.html."""
import pathlib, subprocess, sys

ROOT = pathlib.Path("/home/caio/arclimtec-site")
TITLE = "<title>Arclimtec — Soluções em Climatização | Industrial, empresarial e residencial</title>"
VERSIONS = [
    ("v1-engenharia", "v1-engenharia.html", "Engenharia — escuro e técnico"),
    ("v2-editorial",  "v2-editorial.html",  "Editorial clara — arejada e elegante"),
    ("v3-impacto",    "v3-impacto.html",    "Impacto industrial — tipografia gigante"),
]

def git(*a, check=True):
    r = subprocess.run(["git", "-C", str(ROOT), *a], capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"ERRO em `git {' '.join(a)}`:\n{r.stdout}{r.stderr}")
    return r.stdout.strip()

for branch, src, desc in VERSIONS:
    git("checkout", "-q", "main")
    git("checkout", "-q", "-B", branch, "main")

    html = (ROOT / src).read_text(encoding="utf-8")
    # título limpo: na branch a versão É o site, o nome dela já identifica qual é
    before = html
    for marker in ("V1 Engenharia · ", "V2 Editorial · ", "V3 Impacto · "):
        html = html.replace(f"<title>{marker}Arclimtec — Soluções em Climatização</title>", TITLE)
    if html == before:
        sys.exit(f"ERRO: título de {src} não casou com o padrão esperado")

    (ROOT / "index.html").write_text(html, encoding="utf-8")
    for _, other, _ in VERSIONS:
        (ROOT / other).unlink(missing_ok=True)

    git("add", "-A")
    msg = (f"{desc}\n\n"
           f"Versão publicada como index.html nesta branch, pronta para deploy.\n"
           f"As três direções de design convivem em main para comparação.\n\n"
           f"Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>\n"
           f"Claude-Session: https://claude.ai/code/session_01L3Qdfz7JouVviLnrdxphbp\n")
    subprocess.run(["git", "-C", str(ROOT), "commit", "-q", "-F", "-"],
                   input=msg, text=True, check=True)
    print(f"{branch}: {git('log', '--oneline', '-1')}")

git("checkout", "-q", "main")
print("de volta em main:", git("log", "--oneline", "-1"))
