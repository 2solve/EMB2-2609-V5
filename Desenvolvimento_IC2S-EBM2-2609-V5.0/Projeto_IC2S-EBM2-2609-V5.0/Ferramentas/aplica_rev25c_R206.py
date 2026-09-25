# -*- coding: utf-8 -*-
"""Rev. 2.5c: R206 68 -> 150 ohm (folha 02). Decidido pelo projectista em 2026-09-25.

Porque: o SBVS162B contradiz-se no I_LIM do TPS7A4001 (tabela pag. 5: max. 200 mA; texto sec. 7.3.1 pag. 8:
«309 mA, typical»). Com 309 mA e 68 ohm o RA2 do F201 cai a 8,6x. Com 150 ohm a corrente do fusivel fica
limitada pela propria resistencia, <= 32 V / 153,5 ohm = 0,21 A, qualquer que seja o I_LIM:
limite rigoroso I_max x (Q_C200 + Q_jusante) = 0,208 x 162 uC -> 11,2x; realista 14,3x.
Uso: python aplica_rev25c_R206.py PASTA_DO_PROJECTO  (backup .antes_rev25c)
"""
import io, os, re, shutil, sys


def troca(t, a, b):
    assert t.count(a) == 1, (a[:90], t.count(a))
    return t.replace(a, b)


def simbolo_por(t, cond):
    """Bloco de simbolo de nivel 1 que satisfaz cond; exige um so."""
    achados = []
    for m in re.finditer(r"\n\t\(symbol\n", t):
        i, d = m.start() + 2, 0
        for j in range(i, len(t)):
            d += (t[j] == "(") - (t[j] == ")")
            if d == 0:
                break
        if cond(t[i:j + 1]):
            achados.append((m.start(), j + 1))
    assert len(achados) == 1, ("simbolo", len(achados))
    return achados[0]


F02 = os.path.join(sys.argv[1], "02_entrada.kicad_sch")
t = io.open(F02, encoding="utf-8").read()
a, b = simbolo_por(t, lambda s: '(property "Reference" "R206"' in s)
s = t[a:b]
s = troca(s, '(property "Value" "68R"', '(property "Value" "150R"')
s = re.sub(r'\(property "Description" "[^"]*"',
           '(property "Description" "150 ohm 0805 anti-surto (rev. 2.5c): limita o F201 a 0,21 A, RA2 >= 11,2x sem depender do I_LIM do U200. MPN por fixar - V5"',
           s, count=1)
t = t[:a] + s + t[b:]
for x, y in (
    ("11. R206 = 68 ohm (rev. 2.5) limita o arranque pelo F201 a 32 V, com a carga a jusante:",
     "11. R206 = 150 ohm (rev. 2.5c) limita a corrente do F201 a 32 V / 153,5 ohm = 0,21 A:"),
    ("    I2t = 1024 x 2,2e-6 / (2 x 71,5) + 0,2 A x 91 uC = 3,40e-5 A2s contra",
     "    I2t <= 0,21 A x (70 uC do C200 + 92 uC a jusante) = 3,4e-5 A2s contra"),
    ("    3,8e-4 A2s de fusao: margem 11,2x (RA2 exige 10x). Com 47 ohm: 9,4x.",
     "    3,8e-4 A2s de fusao: >= 11,2x sem depender do I_LIM do U200 (TI: 200 ou 309 mA)."),
    ("    Custo a 7 mA: 0,48 V e 3,3 mW. Pico 0,45 A, ~1,1 mJ por arranque.",
     "    Custo a 7 mA: 1,05 V e 7 mW (U200 a 16,4 V com 18 V). Pico 0,21 A, <= 4 mJ."),
    ("    MPN por fixar (V5): 0805 com curva de impulso para 1,1 mJ.",
     "    MPN por fixar (V5): 0805 com curva de impulso para 4 mJ em ~2 ms."),
):
    t = troca(t, '(text "%s"' % x, '(text "%s"' % y)
shutil.copy2(F02, F02 + ".antes_rev25c")
io.open(F02, "w", encoding="utf-8", newline="").write(t)
print("escrito:", os.path.basename(F02))
