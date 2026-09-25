# -*- coding: utf-8 -*-
"""Rev. 2.5b: R204 4k22 -> 4k12 (folha 03). Recalculo com a tabela 6.13 do TL431BQ (SLVS543S pag. 14):
V_I(dev) 34 mV (nao 17), I_I(dev) 2,5 uA, dVref/dVKA -2,7 mV/V. 4k22 dava 3,451-3,688 V (12 mV sob 3,70 V);
4k12 da 3,427-3,662 V (38 mV sob 3,70 V, 45 mV sobre os 3,3825 V do MCP1824). Decidido pelo projectista.
Uso: python aplica_rev25b_R204.py PASTA_DO_PROJECTO  (backup .antes_rev25b)
"""
import io, os, re, shutil, sys


def troca(t, a, b):
    assert t.count(a) == 1, (a[:90], t.count(a))
    return t.replace(a, b)


def simbolo_por(t, cond):
    """Bloco de simbolo de nivel 1 que satisfaz cond; exige um so. (Copiado de aplica_rev25_folhas_02_03,
    que nao se pode importar: corre tudo ao ser importado.)"""
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


F03 = os.path.join(sys.argv[1], "03_alimentacao.kicad_sch")
t = io.open(F03, encoding="utf-8").read()
a, b = simbolo_por(t, lambda s: '(property "Reference" "R204"' in s)
s = t[a:b]
s = troca(s, '(property "Value" "4k22"', '(property "Value" "4k12"')
s = troca(s, '(property "MPN" "RC0603FR-074K22L"', '(property "MPN" "RC0603FR-074K12L"')
t = t[:a] + s + t[b:]
t = troca(t, '(text "   R204/R205 = 4k22/10k -> 2,495 x 1,422 = 3,55 V; max. 3,65 V a 46 mA (rev. 2.5). C204 10 uF > 6 uF."',
          '(text "   R204/R205 = 4k12/10k -> 2,495 x 1,412 = 3,52 V; 3,43-3,66 V a 46 mA (rev. 2.5b). C204 10 uF > 6 uF."')
shutil.copy2(F03, F03 + ".antes_rev25b")
io.open(F03, "w", encoding="utf-8", newline="").write(t)
print("escrito:", os.path.basename(F03))
