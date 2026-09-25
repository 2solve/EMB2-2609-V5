# -*- coding: utf-8 -*-
"""BOM preliminar, tanda C (2026-09-25): C200 = TDK C3225X7R2A225K230AB, pegada 1206 -> 1210. Nenhuma rede muda.

Ficha TDK «ProductDetailed» de 2026-09-25 (fornecida pelo projectista), pag. 1: 2,2 uF +-10 %, 100 V, X7R +-15 %,
1210 (3,2 x 2,5 x 2,3 mm). Curva DC bias (pag. 2): ~1,54 uF a 30,4 V (trabalho a 32 V de entrada) e ~1,48 uF a 32 V.
Pior caso com o criterio do projecto (tolerancia -10 % e classe X7R -15 %): 1,18 uF e 1,13 uF > 1 uF, o minimo de
entrada do TPS7A4001 «over temperature and tolerance» (SBVS162B pag. 1). RA2 do F201: carga real ate 32 V ~63 uC
(+10 %: 69 uC) -> 0,208 A x (69 + 92) uC = 3,35e-5 A2s -> 11,3x.
Descartados: TDK C3216X7S2A225K160AB (X7S 1206: 0,89 uF no pior caso) e Murata GRM32ER72A225KA35L (fim de vida).
Uso: python aplica_bom_tandaC_C200.py PASTA_DO_PROJECTO   (backup .antes_tandaC)
"""
import io, os, re, shutil, sys

P = sys.argv[1]
F = os.path.join(P, "02_entrada.kicad_sch")
t = io.open(F, encoding="utf-8", newline="").read()


def bloco(t, i):
    d = 0
    for j in range(i, len(t)):
        d += (t[j] == "(") - (t[j] == ")")
        if d == 0:
            return j + 1


def um(s, a, b):
    assert s.count(a) == 1, (a[:70], s.count(a))
    return s.replace(a, b)


ach = [(m.start(), bloco(t, m.start() + 2)) for m in re.finditer(r"\n\t\(symbol\n", t)
       if '(property "Reference" "C200"' in t[m.start():bloco(t, m.start() + 2)]]
assert len(ach) == 1
a, b = ach[0]
s = t[a:b]
s = um(s, '(property "Footprint" "EBM2_V5:1206C120"', '(property "Footprint" "EBM2_V5:C_1210_3225Metric"')
s = um(s, '(property "MPN" ""', '(property "MPN" "C3225X7R2A225K230AB"')
s = um(s, '(property "Description" "2,2 uF >= 100 V X7R 1206, >= 1 uF efectivo a 24 V. MPN por fixar - V6"',
          '(property "Description" "2,2 uF 100 V X7R 1210 TDK: 1,18 uF a 30,4 V no pior caso (curva TDK, -10 %, -15 %) > 1 uF do TPS7A4001; RA2 11,3x"')
t = t[:a] + s + t[b:]
for x, y in (("    100 V X7R em 1206: a 0603 herdada era de uma peca de 25 V.",
              "    100 V X7R em 1210 (tanda C): o 1206 X7S so dava 0,89 uF no pior caso."),
             ("    MPN por fixar (V6): >= 1 uF efectivo a 32 V de polarizacao.",
              "    TDK C3225X7R2A225K230AB: 1,18 uF a 30,4 V no pior caso (curva TDK).")):
    t = um(t, '(text "%s"' % x, '(text "%s"' % y)
shutil.copy2(F, F + ".antes_tandaC")
io.open(F, "w", encoding="utf-8", newline="").write(t)
print("tanda C: C200 = C3225X7R2A225K230AB, pegada 1210, notas 10 da folha 02")
