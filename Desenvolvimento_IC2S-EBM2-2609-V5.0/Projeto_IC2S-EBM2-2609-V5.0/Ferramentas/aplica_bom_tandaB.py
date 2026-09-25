# -*- coding: utf-8 -*-
"""BOM preliminar, tanda B (2026-09-25), pedida pelo projectista antes do Portao 1. Nenhuma rede muda.

1. U202 ADR4525BRZ -> ADR4525WBRZ-R7. A familia esta «Restricted Availability» na Mouser e a BRZ sem preco
   nem stock. A WBRZ-R7 e o MESMO grau B (TC 2 ppm/C box, 4 ppm/C bowtie, -40..125 C, SOIC-8), W = qualificado
   para automovel, bobina de 1000 (ADR45xx Rev. G, tabela 14 pag. 40, nota 2 pag. 41). 2147 em stock.
2. R206 recebe o MPN KOA SG73P2ATTD1500F (0805, 150 ohm 1 %, anti-surto, AEC-Q200; familia da EBM7).
   Curva «One-Pulse Limiting Electric Power» (SG73P, pag. 2), linha 2A: ~26 W a 0,6 ms; o arranque equivale,
   no pior caso, a 6,6 W durante 0,6 ms (4 mJ): margem ~4x.
3. Folha 01: o porto DGND do P1.12 passa de x 48,26 para 78,74 (fio prolongado na mesma linha): o triangulo
   deixa de tapar o no-connect do P1.13 e o texto «ID3». A ligacao nao muda.
Uso: python aplica_bom_tandaB.py PASTA_DO_PROJECTO   (backup .antes_tandaB)
"""
import io, os, re, shutil, sys

P = sys.argv[1]


def bloco(t, i):
    d = 0
    for j in range(i, len(t)):
        d += (t[j] == "(") - (t[j] == ")")
        if d == 0:
            return j + 1
    raise ValueError


def simbolo(t, cond):
    ach = [(m.start(), bloco(t, m.start() + 2)) for m in re.finditer(r"\n\t\(symbol\n", t)
           if cond(t[m.start():bloco(t, m.start() + 2)])]
    assert len(ach) == 1, len(ach)
    return ach[0]


def um(s, a, b):
    assert s.count(a) == 1, (a[:70], s.count(a))
    return s.replace(a, b)


def ler(f):
    return io.open(os.path.join(P, f), encoding="utf-8", newline="").read()


novos = {}
# 1 ---- U202
t = ler("03_alimentacao.kicad_sch")
a, b = simbolo(t, lambda s: '(property "Reference" "U202"' in s)
s = um(t[a:b], '(property "Value" "ADR4525BRZ"', '(property "Value" "ADR4525WBRZ-R7"')
s = um(s, '(property "MPN" "ADR4525BRZ"', '(property "MPN" "ADR4525WBRZ-R7"')
novos["03_alimentacao.kicad_sch"] = t[:a] + s + t[b:]
# 2 ---- R206
t = ler("02_entrada.kicad_sch")
a, b = simbolo(t, lambda s: '(property "Reference" "R206"' in s)
s = um(t[a:b], '(property "MPN" ""', '(property "MPN" "SG73P2ATTD1500F"')
s = re.sub(r'\(property "Description" "[^"]*"',
           '(property "Description" "150 ohm 0805 anti-surto KOA SG73P2A: pulso ~4 mJ em ~2 ms com margem ~4x (SG73P pag. 2); RA2 >= 11,2x sem depender do I_LIM do U200"',
           s, count=1)
t = t[:a] + s + t[b:]
t = um(t, '(text "    MPN por fixar (V5): 0805 com curva de impulso para 4 mJ em ~2 ms."',
          '(text "    MPN KOA SG73P2ATTD1500F: 26 W a 0,6 ms (SG73P pag. 2) contra 6,6 W: ~4x."')
novos["02_entrada.kicad_sch"] = t
# 3 ---- folha 01: porto DGND do P1.12
t = ler("01_conectores.kicad_sch")
t = um(t, "(xy 45.72 73.66) (xy 48.26 73.66)", "(xy 45.72 73.66) (xy 78.74 73.66)")
a, b = simbolo(t, lambda s: '(lib_id "power:GND")' in s and "(at 48.26 73.66 0)" in s)
s = t[a:b]
s = re.sub(r"\(at ([-\d.]+) ([-\d.]+)", lambda m: "(at %s %s" % (("%.4f" % (float(m.group(1)) + 30.48)).rstrip("0").rstrip("."), m.group(2)), s)
assert "(at 78.74 73.66 0)" in s, s[:300]
t = t[:a] + s + t[b:]
# o texto do ID3 tinha sido deslocado a mao para fugir do triangulo; volta ao padrao das outras linhas
# (x 48,26; y = pino + 0,635)
k = t.find('(text "ID3 - manter desligado"')
assert k > 0 and t.count('(text "ID3 - manter desligado"') == 1
j = bloco(t, k)
t = t[:k] + um(t[k:j], "(at 49.276 76.962 0)", "(at 48.26 76.835 0)") + t[j:]
novos["01_conectores.kicad_sch"] = t

for f, t in novos.items():
    c = os.path.join(P, f)
    shutil.copy2(c, c + ".antes_tandaB")
    io.open(c, "w", encoding="utf-8", newline="").write(t)
print("tanda B: U202 -> ADR4525WBRZ-R7, R206 = SG73P2ATTD1500F, porto DGND do P1.12 deslocado")
