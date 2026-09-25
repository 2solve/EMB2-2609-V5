# -*- coding: utf-8 -*-
"""Rev. 2.5 (intencao sec. 17) nas folhas desenhadas a mao 02 e 03: enxerto cirurgico, sem regenerar.

Folha 02: R206 33 -> 68 ohm e a nota 11.
Folha 03: U201 SPX3819 -> MCP1824T-3302E/OT (mesma geometria SOT-23-5, pino 4 = PWRGD sem uso),
          C208 sai, EN_3V3 -> SHDN_3V3, C204 10 uF 1206 TDK, R204 4k22, C207 2u2, C209 10 nF (C_BYP do U200)
          e as notas.
Uso: python aplica_rev25_folhas_02_03.py PASTA_DO_PROJECTO   (backup .antes_rev25 de cada folha tocada)
Cada troca tem de aparecer exactamente uma vez; senao aborta sem escrever nada.
"""
import io, os, re, shutil, sys, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from construtor import Folha, blocos_lib_de_folha

P = sys.argv[1]
F02, F03 = os.path.join(P, "02_entrada.kicad_sch"), os.path.join(P, "03_alimentacao.kicad_sch")
UUID03 = "499e7f8e-bd46-4332-a4da-4ccc2afc4430"


def nu():
    return str(uuid.uuid4())


def troca(t, a, b, n=1):
    assert t.count(a) == n, (a[:90], t.count(a))
    return t.replace(a, b)


def bloco(t, inicio):
    """Devolve (i, j) do bloco s-expr que comeca em t[inicio]."""
    d = 0
    for j in range(inicio, len(t)):
        d += (t[j] == "(") - (t[j] == ")")
        if d == 0:
            return inicio, j + 1
    raise ValueError("bloco aberto")


def simbolo_por(t, cond):
    """Bloco '\\n\\t(symbol' de nivel 1 cujo texto satisfaz cond; exige um so."""
    achados = []
    for m in re.finditer(r"\n\t\(symbol\n", t):
        i, j = bloco(t, m.start() + 2)
        if cond(t[i:j]):
            achados.append((m.start(), j))
    assert len(achados) == 1, ("simbolo", len(achados))
    return achados[0]


def poe_mpn(t, ref, valor):
    """Cria o campo MPN (escondido) copiando o campo Footprint, se o simbolo ainda nao o tiver."""
    a, b = simbolo_por(t, lambda s: '(property "Reference" "%s"' % ref in s)
    s = t[a:b]
    assert '(property "MPN"' not in s, ref
    k = s.find('\n\t\t(property "Footprint"')
    i, j = bloco(s, k + 3)
    mp = re.sub(r'\(property "Footprint" "[^"]*"', '(property "MPN" "%s"' % valor, s[k:j], count=1)
    return t[:a] + s[:j] + mp + s[j:] + t[b:]


def prop(t, ref, nome, antigo, novo):
    a, b = simbolo_por(t, lambda s: '(property "Reference" "%s"' % ref in s)
    s = t[a:b]
    s2 = troca(s, '(property "%s" "%s"' % (nome, antigo), '(property "%s" "%s"' % (nome, novo))
    return t[:a] + s2 + t[b:]


# ================================================================ folha 02
t2 = io.open(F02, encoding="utf-8").read()
t2 = prop(t2, "R206", "Value", "33R", "68R")
t2 = prop(t2, "R206", "Description",
          "33 ohm 0805 anti-surto: limita o arranque de C200 a 32 V (nota 11, rev. 2.2). MPN por fixar - V5",
          "68 ohm 0805 anti-surto (rev. 2.5): RA2 do F201 a 32 V com toda a carga a jusante = 11,2x. MPN por fixar - V5")
for a, b in (
    ("11. R206 = 33 ohm limita o arranque de C200 atraves de F201 (a 32 V):",
     "11. R206 = 68 ohm (rev. 2.5) limita o arranque pelo F201 a 32 V, com a carga a jusante:"),
    ("    I2t = 1024 x 2,2e-6 / (2 x 36,5) = 3,09e-5 A2s contra",
     "    I2t = 1024 x 2,2e-6 / (2 x 71,5) + 0,2 A x 91 uC = 3,40e-5 A2s contra"),
    ("    3,8e-4 A2s de fusao: margem 12,3x (RA2 exige 10x). Com 22 ohm: 8,6x.",
     "    3,8e-4 A2s de fusao: margem 11,2x (RA2 exige 10x). Com 47 ohm: 9,4x."),
    ("    Custo a 12 mA: 0,40 V e 4,8 mW. Pico 0,88 A, 80 us, 1,0 mJ.",
     "    Custo a 7 mA: 0,48 V e 3,3 mW. Pico 0,45 A, ~1,1 mJ por arranque."),
    ("    MPN por fixar (V5): 0805 com curva de impulso para 1,0 mJ.",
     "    MPN por fixar (V5): 0805 com curva de impulso para 1,1 mJ."),
):
    t2 = troca(t2, '(text "%s"' % a, '(text "%s"' % b)

# ================================================================ folha 03
t3 = io.open(F03, encoding="utf-8").read()
# --- simbolo de biblioteca: o do SPX3819 renomeado para o MCP1824 (mesma geometria), pinos 3 e 4 trocados
ia = t3.find('\t\t(symbol "Regulator_Linear:SPX3819M5-L-3-3"')
assert ia > 0 and t3.count('(symbol "Regulator_Linear:SPX3819M5-L-3-3"') == 1
i, j = bloco(t3, ia + 2)
lib = t3[i:j]
novo = lib.replace('(symbol "Regulator_Linear:SPX3819M5-L-3-3"', '(symbol "EBM2_V5:MCP1824T-3302E_OT"')
novo = novo.replace('(symbol "SPX3819M5-L-3-3_0_1"', '(symbol "MCP1824T-3302E_OT_0_1"')
novo = novo.replace('(symbol "SPX3819M5-L-3-3_1_1"', '(symbol "MCP1824T-3302E_OT_1_1"')
novo = troca(novo, '(property "Value" "SPX3819M5-L-3-3"', '(property "Value" "MCP1824T-3302E/OT"')
novo = re.sub(r'\(property "Datasheet" "[^"]*"', '(property "Datasheet" "https://ww1.microchip.com/downloads/en/DeviceDoc/22070a.pdf"', novo)
novo = troca(novo, '(property "Description" "500mA Low drop-out regulator, Fixed Output 3.3V, SOT-23-5"',
             '(property "Description" "LDO 300 mA 3,3 V fixo, SOT-23-5: 1 VIN 2 GND 3 SHDN 4 PWRGD 5 VOUT (DS22070A tabela 3-1 pag. 17)"')
novo = troca(novo, '(property "ki_keywords" "REGULATOR LDO 3.3V"', '(property "ki_keywords" "LDO 3.3V MCP1824"')
novo, n = re.subn(r'\(pin input line(\s+)\(at -7\.62 0 0\)(\s+)\(length 2\.54\)(\s+)\(name "EN"',
                  r'(pin input line\1(at -7.62 0 0)\2(length 2.54)\3(name "~{SHDN}"', novo)
assert n == 1, ("pino EN", n)
novo, n = re.subn(r'\(pin input line(\s+)\(at 7\.62 0 180\)(\s+)\(length 2\.54\)(\s+)\(name "BP"',
                  r'(pin open_collector line\1(at 7.62 0 180)\2(length 2.54)\3(name "PG"', novo)   # PWRGD: «PG» cabe no corpo
assert n == 1, ("pino BP", n)
assert "SPX3819" not in novo
t3 = t3[:i] + novo + t3[j:]
# --- instancia U201
a, b = simbolo_por(t3, lambda s: '(property "Reference" "U201"' in s)
s = t3[a:b]
s = troca(s, '(lib_id "Regulator_Linear:SPX3819M5-L-3-3")', '(lib_id "EBM2_V5:MCP1824T-3302E_OT")')
s = troca(s, '(property "Value" "SPX3819M5-L-3-3/TR"', '(property "Value" "MCP1824T-3302E/OT"')
s = troca(s, '(property "MPN" "SPX3819M5-L-3-3/TR"', '(property "MPN" "MCP1824T-3302E/OT"')
s = re.sub(r'\(property "Description" "[^"]*"',
           '(property "Description" "Rev. 2.5: MCP1824 fixo 3,3 V em vez do SPX3819: estavel com ceramico 1-22 uF (DS22070A sec. 4.3), o que o grampo TL431 precisa (> 6 uF, fig. 6-18)"', s, count=1)
s = re.sub(r'\(property "Datasheet" "[^"]*"', '(property "Datasheet" "https://ww1.microchip.com/downloads/en/DeviceDoc/22070a.pdf"', s, count=1)
t3 = t3[:a] + s + t3[b:]
# --- valores
t3 = prop(t3, "C204", "Value", "2u2", "10uF/50V")
t3 = prop(t3, "C204", "Footprint", "EBM2_V5:0603C", "EBM2_V5:C_1206_3216Metric")
t3 = poe_mpn(t3, "C204", "C3216X5R1H106K160AB")
t3 = prop(t3, "R204", "Value", "4k42", "4k22")
t3 = poe_mpn(t3, "R204", "RC0603FR-074K22L")
t3 = prop(t3, "C207", "Value", "1uF", "2u2")
# --- C208 sai com o seu porto de massa, os dois fios e o rotulo; no-connect no pino 4 (PWRGD)
a, b = simbolo_por(t3, lambda s: '(property "Reference" "C208"' in s); t3 = t3[:a] + t3[b:]
a, b = simbolo_por(t3, lambda s: '(at 162.56 76.2 0)' in s and '"power:GND"' in s); t3 = t3[:a] + t3[b:]
for xy in ("(xy 152.4 66.04) (xy 162.56 66.04)", "(xy 162.56 73.66) (xy 162.56 76.2)"):
    k = t3.find(xy); assert t3.count(xy) == 1
    ws = t3.rfind("\n\t(wire\n", 0, k); i, j = bloco(t3, ws + 2); t3 = t3[:ws] + t3[j:]
k = t3.find('\n\t(label "BYP_3V3"'); i, j = bloco(t3, k + 2); t3 = t3[:k] + t3[j:]
t3 = troca(t3, '(label "EN_3V3"', '(label "SHDN_3V3"')
# --- elementos novos: no-connect no PWRGD e C209 (C_BYP do U200) ligado por porto e rotulo
fo = Folha(F03, UUID03, blocos_lib_de_folha(F03))
fo.porto("+5V_ADC", 99.06, 86.36, "power:+5V", base=322)
fo.simbolo("Device:C", "C209", "10nF", 99.06, 90.17, 0, pegada="EBM2_V5:0603C", mpn="",
           descr="Rev. 2.5: C_BYP do U200 entre OUT (+5V_ADC) e FB (FB_5V), SBVS162B nota 4 pag. 5 e sec. 8.2.2.3. Zero a 491 Hz com 32k4. MPN na BOM",
           ref_pos=(101.6, 88.9, 0, "left"), val_pos=(101.6, 91.44, 0, "left"))
novos = list(fo.simbolos)
novos.append('\t(wire\n\t\t(pts\n\t\t\t(xy 99.06 93.98) (xy 99.06 96.52)\n\t\t)\n\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default)\n\t\t)\n\t\t(uuid "%s")\n\t)' % nu())
novos.append('\t(label "FB_5V"\n\t\t(at 99.06 96.52 0)\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify left bottom)\n\t\t)\n\t\t(uuid "%s")\n\t)' % nu())
novos.append('\t(no_connect\n\t\t(at 152.4 66.04)\n\t\t(uuid "%s")\n\t)' % nu())
# Inserir DENTRO da raiz, antes do ')' final. Na 1.a versao procurava-se '\n\t(embedded_fonts', que esta
# folha nao tem: rfind devolvia -1 e os itens caiam depois do ')' da raiz, onde o KiCad os ignora sem aviso.
k = t3.rstrip().rfind(")")
assert k > 0 and t3[k + 1:].strip() == "" and t3[:k].rstrip().endswith(")"), "fim da raiz nao reconhecido"
t3 = t3[:k].rstrip("\n") + "\n" + "\n".join(novos) + "\n" + t3[k:]
# --- notas
for a, b in (
    ("4. Duas etapas: o SPX3819 e de baixo ruido, o TPS7A4001 nao.",
     "4. Duas etapas. Rev. 2.5: U201 = MCP1824 (estavel com ceramico; o SPX3819 nao o garante)."),
    ("8. C208 no pino BP do SPX3819: baixa o ruido do LDO (datasheet MaxLinear, aplicacao).",
     "8. Rev. 2.5: C208 saiu (pino 4 do MCP1824 = PWRGD, sem uso). C209 = C_BYP do U200 (TI 8.2.2.3)."),
    ("   R204/R205 = 4k42/10k -> 2,495 x (1 + 4,42/10) = 3,60 V.",
     "   R204/R205 = 4k22/10k -> 2,495 x 1,422 = 3,55 V; max. 3,65 V a 46 mA (rev. 2.5). C204 10 uF > 6 uF."),
):
    t3 = troca(t3, '(text "%s"' % a, '(text "%s"' % b)

# ================================================================ escrita
for f, t in ((F02, t2), (F03, t3)):
    shutil.copy2(f, f + ".antes_rev25")
    io.open(f, "w", encoding="utf-8", newline="").write(t)
    print("escrito:", os.path.basename(f))
