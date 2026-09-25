# -*- coding: utf-8 -*-
"""Folha 02: tirar os restos da EBM7 Legacy que o editor grafico rejeita.

1. As rotas de instancia dos simbolos apontam para a raiz e a folha da Legacy.
   Passam a apontar para a raiz desta placa e para o simbolo de folha da 02.
2. A subfolha traz um bloco (sheet_instances), que so pode existir na raiz.

kicad-cli tolera as duas coisas; o editor corrige-as ao abrir e avisa. Sem
argumentos: ENSAIO. Com --aplicar: backup .antes_instancias e escreve.
"""
import io, os, re, shutil, subprocess, sys
P = r"C:\hw\hw-ebm2-v5\KiCad_EBM2_V5"
F = os.path.join(P, "02_entrada.kicad_sch")
RAIZ = os.path.join(P, "IC2S_Extension_Board-EBM2_V5.kicad_sch")
APLICAR = "--aplicar" in sys.argv

tit = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                      os.path.join(os.path.dirname(os.path.abspath(__file__)), "janelas_kicad.ps1")],
                     capture_output=True, text=True).stdout
aberto = "EBM2_V5" in tit or "EBM2 V5" in tit

r = io.open(RAIZ, encoding="utf-8").read()
ru = re.search(r'\n\t\(uuid "([^"]+)"\)', r).group(1)
bloco = None
for m in re.finditer(r"\n\t\(sheet\n", r):
    b = r[m.start() + 1:r.find("\n\t)\n", m.start() + 1)]
    if '"Sheetfile" "02_entrada.kicad_sch"' in b:
        bloco = b
su = re.search(r'\n\t\t\(uuid "([^"]+)"\)', bloco).group(1)
certo = "/%s/%s" % (ru, su)

t = io.open(F, encoding="utf-8").read()
errado = "/ea39faa7-2c85-4731-99b5-dc619370fd78/dc966404-66d2-45f9-bab0-0c169c132973"
n = t.count('(path "%s"' % errado)
print("rota certa:  ", certo)
print("rota errada: ", errado, "x", n)
assert n == 22, "esperava 22 instancias com a rota da Legacy"
t2 = t.replace('(path "%s"' % errado, '(path "%s"' % certo)

si = "\n\t(sheet_instances\n\t\t(path \"/\"\n\t\t\t(page \"3\")\n\t\t)\n\t)"
assert t2.count(si) == 1, "bloco sheet_instances nao encontrado na forma esperada"
t2 = t2.replace(si, "")

outras = set(re.findall(r'\(path "([^"]+)"', t2))
assert outras == {certo}, "ficaram rotas estranhas: %s" % outras
assert "(sheet_instances" not in t2
print("depois: todas as rotas = rota certa; sem sheet_instances na subfolha")

if not APLICAR:
    print("ENSAIO terminado. Nada escrito.", "(EBM2 V5 ABERTO no KiCad: fechar SEM guardar antes de aplicar)" if aberto else "")
    sys.exit(0)
if aberto:
    sys.exit("ABORTA: o projecto EBM2 V5 esta aberto no KiCad")
shutil.copy2(F, F + ".antes_instancias")
io.open(F, "w", encoding="utf-8", newline="").write(t2)
print("ESCRITO:", F)
