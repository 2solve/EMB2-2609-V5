# -*- coding: utf-8 -*-
"""Tanda P1-R (2026-09-25), itens 2 e 5: biblioteca de simbolos propria do projecto.

A sym-lib-table apontava para dez ficheiros ${KIPRJMOD}/symbols/EBM7_V23_proyectoN.kicad_sym que NAO existem
neste projecto (restos da EBM7), e os dois simbolos EBM2_V5:MCP1824* nao tinham entrada nenhuma. O projecto so
abria porque os simbolos estao embebidos nas folhas (verificacao cruzada P1, bloco 2, achado 1).
Correccao: symbols/EBM2_V5.kicad_sym com os 7 simbolos proprios USADOS, copiados letra a letra das copias
embebidas (mesmos pinos; as duas copias do TPS7A4001, folhas 03 e 06, sao identicas), lib_id -> EBM2_V5:<nome>,
e a sym-lib-table so com essa entrada. Item 5: a descricao do TPS26613 dizia "o D2 grampeia a 48,4 V" (valor da
EBM7 Legacy, TVS de 30 V); na EBM2 V5 o D2 e o SMA6J33A: 53,3 V a 11,3 A (Bourns SMA6J, pag. 2).
Nenhuma rede muda. Uso: python aplica_P1R_biblioteca.py   (backups .antes_P1R)
"""
import io, os, re, shutil

K = r"C:\hw\hw-ebm2-v5\KiCad_EBM2_V5"
FOLHAS = ["01_conectores", "02_entrada", "03_alimentacao", "04_barreira", "05_adc", "06_lacos", "07_ntc"]
PREF = r"(?:EBM7_V23_proyecto\d+|EBM2_V5)"
VELHO = "NAO ligar aos +24V_ADC, que o D2 grampeia a 48,4 V."
NOVO = "NAO ligar aos +24V_ADC, que o D2 (SMA6J33A) grampeia a 53,3 V (Bourns pag. 2)."


def bloco(t, i):
    d = 0
    for j in range(i, len(t)):
        d += (t[j] == "(") - (t[j] == ")")
        if d == 0:
            return j + 1


simbolos, novos = {}, {}
for f in FOLHAS:
    p = os.path.join(K, f + ".kicad_sch")
    t = io.open(p, encoding="utf-8", newline="").read()
    a = t.find("(lib_symbols"); b = bloco(t, a)
    for m in re.finditer(r'\n\t\t\(symbol "(%s):([^"]+)"' % PREF, t[a:b]):
        i = a + m.start() + 3
        s = t[i:bloco(t, i)].replace(VELHO, NOVO)
        s = s.replace('(symbol "%s:%s"' % (m.group(1), m.group(2)), '(symbol "%s"' % m.group(2), 1)
        if m.group(2) in simbolos:
            assert simbolos[m.group(2)] == s, "copias diferentes de " + m.group(2)
        simbolos[m.group(2)] = s
    n = re.sub(r'"%s:' % PREF, '"EBM2_V5:', t)   # lib_id das instancias e nomes em lib_symbols
    n = n.replace(VELHO, NOVO)
    novos[p] = (t, n)
assert len(simbolos) == 7, sorted(simbolos)
assert sum(VELHO in t for t, _ in novos.values()) == 1

lib = ["(kicad_symbol_lib", "\t(version 20251024)", '\t(generator "kicad_symbol_editor")', '\t(generator_version "10.0")']
for nome in sorted(simbolos):
    # as copias embebidas estao dois tabs dentro (kicad_sch > lib_symbols); na biblioteca ficam a um tab
    lib.append("\t" + "\n".join(l[1:] if l.startswith("\t") else l for l in simbolos[nome].split("\n")))
lib.append(")")
os.makedirs(os.path.join(K, "symbols"), exist_ok=True)
io.open(os.path.join(K, "symbols", "EBM2_V5.kicad_sym"), "w", encoding="utf-8", newline="\n").write("\n".join(lib) + "\n")

TAB = os.path.join(K, "sym-lib-table")
shutil.copy2(TAB, TAB + ".antes_P1R")
io.open(TAB, "w", encoding="utf-8", newline="\n").write(
    '(sym_lib_table\n\t(version 7)\n\t(lib (name "EBM2_V5")(type "KiCad")(uri "${KIPRJMOD}/symbols/EBM2_V5.kicad_sym")(options "")'
    '(descr "Simbolos proprios da EBM2 V5 (7): copiados das folhas em 2026-09-25; pinagem conferida contra datasheet na 2.3"))\n)\n')
for p, (t, n) in novos.items():
    if t != n:
        shutil.copy2(p, p + ".antes_P1R")
        io.open(p, "w", encoding="utf-8", newline="").write(n)
        print("folha:", os.path.basename(p), n.count('"EBM2_V5:') - t.count('"EBM2_V5:'), "lib_id/nomes trocados")
print("biblioteca:", sorted(simbolos))
