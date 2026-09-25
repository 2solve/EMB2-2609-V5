# -*- coding: utf-8 -*-
"""BOM preliminar (2shw-pcb:bom), tanda A de 2026-09-25: MPN das linhas que o nao tinham, C202 em 1206 e os
pontos de prova fora da BOM. Nenhuma ligacao muda (a netlist tem de ter as mesmas redes).

MPN escolhidos por reutilizacao (copiar o original): pecas ja usadas na V5 ou na EBM7 V2.3 Legacy.
  C203 C205 C206  100 nF   GRM188R72A104KA35D   (ja na V5)
  R202 R205       10k      RC0603FR-0710KL      (ja na V5, R642)
  R203            100k     RC0603FR-07100KL     (EBM7)
  R201            32k4     RC0603FR-0732K4L     (serie Yageo RC da casa)
  C400 C501       1 uF     C0603C105K4RACTU     (EBM7; KEMET 16 V X7R)
  C209 C645       10 nF    GCM188R71H103KA37J   (EBM7; 50 V X7R)
  C207 C402       2,2 uF   C1608X5R1E225K080AB  (EBM7; TDK 25 V X5R) - curva DC bias por conferir
  C202            10 uF    C3216X5R1H106K160AB  (ja na V5) e pegada 0603 -> 1206: curva TDK a 5 V ~9,2 uF,
                  pior caso 9,2 x 0,9 x 0,85 = 7,0 uF > 4,7 uF (TPS7A4001, SBVS162B pag. 1). Fecha a F8.
Pontos de prova T203-T640: in_bom no, como T201/T202 (sao ilhas/vias, nao se compram).
Ficam por fixar (precisam de curva do fabricante): C200 (>= 1 uF a 32 V) e R206 (impulso ~4 mJ em ~2 ms).
Uso: python aplica_mpn_bom_prelim.py PASTA_DO_PROJECTO  (backup .antes_mpn_bom de cada folha tocada)
"""
import io, os, re, shutil, sys

P = sys.argv[1]
MPN = {
    "03_alimentacao.kicad_sch": {"C203": "GRM188R72A104KA35D", "C205": "GRM188R72A104KA35D", "C206": "GRM188R72A104KA35D",
                                 "R202": "RC0603FR-0710KL", "R205": "RC0603FR-0710KL", "R203": "RC0603FR-07100KL",
                                 "R201": "RC0603FR-0732K4L", "C209": "GCM188R71H103KA37J", "C207": "C1608X5R1E225K080AB",
                                 "C202": "C3216X5R1H106K160AB"},
    "04_barreira.kicad_sch": {"C400": "C0603C105K4RACTU", "C402": "C1608X5R1E225K080AB"},
    "05_adc.kicad_sch": {"C501": "C0603C105K4RACTU"},
    "06_lacos.kicad_sch": {"C645": "GCM188R71H103KA37J"},
}
EXTRA = {"03_alimentacao.kicad_sch": {"C202": [("Value", "10uF/25V", "10uF/50V"), ("Footprint", "EBM2_V5:0603C", "EBM2_V5:C_1206_3216Metric")]}}
TP_FORA = {"02_entrada.kicad_sch": ["T206", "T207"], "03_alimentacao.kicad_sch": ["T203", "T204", "T205"],
           "04_barreira.kicad_sch": ["T400"], "05_adc.kicad_sch": ["T500"], "06_lacos.kicad_sch": ["T640"]}


def bloco(t, i):
    d = 0
    for j in range(i, len(t)):
        d += (t[j] == "(") - (t[j] == ")")
        if d == 0:
            return j + 1
    raise ValueError("bloco aberto")


def simbolo(t, ref):
    ach = [(m.start(), bloco(t, m.start() + 2)) for m in re.finditer(r"\n\t\(symbol\n", t)
           if '(property "Reference" "%s"' % ref in t[m.start():bloco(t, m.start() + 2)]]
    assert len(ach) == 1, (ref, len(ach))
    return ach[0]


def troca1(s, a, b, ctx):
    assert s.count(a) == 1, (ctx, a[:70], s.count(a))
    return s.replace(a, b)


novos = {}
for f in sorted(set(MPN) | set(TP_FORA)):
    t = io.open(os.path.join(P, f), encoding="utf-8", newline="").read()
    for ref, mpn in MPN.get(f, {}).items():
        a, b = simbolo(t, ref)
        s = t[a:b]
        m = re.search(r'\(property "MPN" "([^"]*)"', s)
        if m:
            assert m.group(1) in ("", "-"), (ref, "ja tem MPN", m.group(1))
            s = s[:m.start()] + '(property "MPN" "%s"' % mpn + s[m.end():]
        else:                                        # cria o campo copiando o Footprint (escondido)
            k = s.find('\n\t\t(property "Footprint"')
            j = bloco(s, k + 3)
            s = s[:j] + re.sub(r'\(property "Footprint" "[^"]*"', '(property "MPN" "%s"' % mpn, s[k:j], count=1) + s[j:]
        for campo, velho, novo in EXTRA.get(f, {}).get(ref, []):
            s = troca1(s, '(property "%s" "%s"' % (campo, velho), '(property "%s" "%s"' % (campo, novo), ref)
        t = t[:a] + s + t[b:]
    for ref in TP_FORA.get(f, []):
        a, b = simbolo(t, ref)
        t = t[:a] + troca1(t[a:b], "(in_bom yes)", "(in_bom no)", ref) + t[b:]
    novos[f] = t
for f, t in novos.items():
    c = os.path.join(P, f)
    shutil.copy2(c, c + ".antes_mpn_bom")
    io.open(c, "w", encoding="utf-8", newline="").write(t)
print("escritas %d folhas: %d MPN, 1 pegada (C202), %d pontos de prova fora da BOM"
      % (len(novos), sum(len(v) for v in MPN.values()), sum(len(v) for v in TP_FORA.values())))
