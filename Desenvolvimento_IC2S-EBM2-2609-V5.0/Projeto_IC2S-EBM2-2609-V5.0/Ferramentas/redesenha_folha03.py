# -*- coding: utf-8 -*-
"""F2 / 2.2b - passo C: redesenhar a folha 03_alimentacao.

A folha foi dada por verificada sem medir a sobreposicao no PDF. A medicao deu
dezenas de textos encimados: portos de trilho a 2,54 mm com o nome a direita,
valores de CI dentro do corpo, o divisor do TL431 dentro das notas.

Este script mantem os MESMOS componentes (bloco, uuid, propriedades, instancia)
e a MESMA ligacao; refaz so a geometria: posicoes, fios, juncoes, rotulos,
portos de trilho, no-connects e notas. A netlist tem de sair com topologia
identica - e isso que o prova, nao este script.

Sem argumentos: ENSAIO. Com --aplicar: backup .antes_redesenho e escreve.
"""
import io, os, re, shutil, subprocess, sys, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kicad_pinos import pinos_biblioteca, pos_pino

F = r"C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\03_alimentacao.kicad_sch"
APLICAR = "--aplicar" in sys.argv
MARCA = "10. Um so porto por trilho em cada bloco"

PS1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "janelas_kicad.ps1")
tit = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", PS1],
                     capture_output=True, text=True).stdout
if "EBM2_V5" in tit or "EBM2 V5" in tit:
    sys.exit("ABORTA: o projecto EBM2 V5 esta aberto no KiCad")

T0 = io.open(F, encoding="utf-8").read()
if MARCA in T0:
    sys.exit("ABORTA: a folha ja foi redesenhada. Restaurar o backup antes de repetir.")
LIB = pinos_biblioteca(F)


def fim(s, i):
    d = 0; dentro = False
    while True:
        c = s[i]
        if c == '"' and s[i - 1] != "\\":
            dentro = not dentro
        elif not dentro:
            if c == "(":
                d += 1
            elif c == ")":
                d -= 1
                if d == 0:
                    return i + 1
        i += 1


def topo(s, cab):
    res, k, pat = [], 0, "\n\t(" + cab
    while True:
        k = s.find(pat, k)
        if k < 0:
            return res
        i = k + 1
        if s[i + 2 + len(cab)] in " \n\t\r":
            res.append((i, fim(s, i)))
        k = i + 1


def nu():
    return str(uuid.uuid4())


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


# ---------------------------------------------------------------- 1. recolher blocos
simb = {}
for a, b in topo(T0, "symbol"):
    blk = T0[a:b]
    ref = re.search(r'\(property "Reference" "([^"]+)"', blk).group(1)
    simb[ref] = blk
COMP = ["U200", "U201", "U202", "U203", "R201", "R202", "R203", "R204", "R205",
        "C202", "C203", "C204", "C205", "C206", "C207", "C208", "T203", "T204", "T205"]
assert all(c in simb for c in COMP), [c for c in COMP if c not in simb]
MODELO_TRILHO = {}
for ref, blk in simb.items():
    if ref.startswith("#PWR"):
        v = re.search(r'\(property "Value" "([^"]+)"', blk).group(1)
        MODELO_TRILHO.setdefault(v, blk)
print("componentes: %d | modelos de porto: %s" % (len(COMP), sorted(MODELO_TRILHO)))

# ---------------------------------------------------------------- 2. geometria nova
# ref: (x, y, rot, campos {nome: (x, y, ang, justify)})
def campos_RC(x, y):         # R ou C vertical: texto a direita
    return {"Reference": (x + 2.54, y - 1.27, 0, "left"), "Value": (x + 2.54, y + 1.27, 0, "left")}


def campos_TP(x, y):         # ponto de prova: texto empilhado por cima do circulo
    return {"Reference": (x, y - 7.62, 0, None), "Value": (x, y - 5.08, 0, None)}


POS = {
    "U200": (50.80, 71.12, 0, {"Reference": (50.80, 54.61, 0, None), "Value": (50.80, 57.15, 0, None)}),
    "R201": (68.58, 69.85, 0, campos_RC(68.58, 69.85)),
    "R202": (68.58, 77.47, 0, campos_RC(68.58, 77.47)),
    "C202": (81.28, 69.85, 0, campos_RC(81.28, 69.85)),
    "C203": (96.52, 69.85, 0, campos_RC(96.52, 69.85)),
    "T203": (106.68, 63.50, 0, campos_TP(106.68, 63.50)),
    "R203": (118.11, 73.66, 90, {"Reference": (118.11, 71.12, 90, None), "Value": (118.11, 76.20, 90, None)}),
    "U201": (144.78, 66.04, 0, {"Reference": (144.78, 54.61, 0, None), "Value": (144.78, 57.15, 0, None)}),
    "C208": (162.56, 69.85, 0, campos_RC(162.56, 69.85)),
    "T204": (160.02, 58.42, 0, campos_TP(160.02, 58.42)),
    "C204": (175.26, 64.77, 0, campos_RC(175.26, 64.77)),
    "C205": (190.50, 64.77, 0, campos_RC(190.50, 64.77)),
    "U202": (63.50, 119.38, 0, {"Reference": (63.50, 101.60, 0, None), "Value": (63.50, 104.14, 0, None)}),
    "C206": (38.10, 120.65, 0, campos_RC(38.10, 120.65)),
    "C207": (86.36, 120.65, 0, campos_RC(86.36, 120.65)),
    "T205": (93.98, 114.30, 0, campos_TP(93.98, 114.30)),
    "U203": (139.70, 121.92, 90, {"Reference": (143.51, 120.65, 90, "left"), "Value": (143.51, 123.19, 90, "left")}),
    "R204": (124.46, 118.11, 0, campos_RC(124.46, 118.11)),
    "R205": (124.46, 125.73, 0, campos_RC(124.46, 125.73)),
}

# portos: (valor, x, y). Tensao: corpo para cima, nome centrado por cima. Massa: nome por baixo.
PORTOS = [
    ("+24V_REG", 33.02, 60.96), ("+5V", 88.90, 63.50),
    ("GND_ADC", 50.80, 83.82), ("GND_ADC", 68.58, 83.82), ("GND_ADC", 81.28, 76.20), ("GND_ADC", 96.52, 76.20),
    ("GND_ADC", 144.78, 76.20), ("GND_ADC", 162.56, 76.20), ("GND_ADC", 175.26, 71.12), ("GND_ADC", 190.50, 71.12),
    ("3V3_REF", 205.74, 58.42),
    ("3V3_REF", 30.48, 114.30), ("GND_ADC", 38.10, 127.00), ("GND_ADC", 63.50, 134.62),
    ("+2V5_REF", 114.30, 114.30), ("GND_ADC", 86.36, 127.00),
    ("3V3_REF", 132.08, 111.76), ("GND_ADC", 124.46, 132.08), ("GND_ADC", 139.70, 127.00),
]


def barra(y, xs):
    return [(xs[i], y, xs[i + 1], y) for i in range(len(xs) - 1)]


FIOS = [
    # entrada do TPS7A4001: IN e EN amarrados ao +24V_REG
    (33.02, 60.96, 33.02, 68.58), (33.02, 68.58, 40.64, 68.58), (33.02, 68.58, 33.02, 73.66), (33.02, 73.66, 40.64, 73.66),
    # saida e barra de +5V
    (60.96, 68.58, 63.50, 68.58), (63.50, 68.58, 63.50, 63.50),
] + barra(63.50, [63.50, 68.58, 81.28, 88.90, 96.52, 106.68, 114.30, 137.16]) + [
    (68.58, 63.50, 68.58, 66.04), (81.28, 63.50, 81.28, 66.04), (96.52, 63.50, 96.52, 66.04), (114.30, 63.50, 114.30, 73.66),
    # FB
    (60.96, 73.66, 68.58, 73.66),
    # massas da fila 1
    (50.80, 81.28, 50.80, 83.82), (68.58, 81.28, 68.58, 83.82), (81.28, 73.66, 81.28, 76.20), (96.52, 73.66, 96.52, 76.20),
    # EN do SPX3819 pela R203
    (121.92, 73.66, 134.62, 73.66), (134.62, 73.66, 134.62, 66.04), (134.62, 66.04, 137.16, 66.04),
    (144.78, 73.66, 144.78, 76.20),
    # saida e barra de 3V3_REF
    (152.40, 63.50, 154.94, 63.50), (154.94, 63.50, 154.94, 58.42),
] + barra(58.42, [154.94, 160.02, 175.26, 190.50, 205.74]) + [
    (175.26, 58.42, 175.26, 60.96), (190.50, 58.42, 190.50, 60.96),
    (152.40, 66.04, 162.56, 66.04),
    (162.56, 73.66, 162.56, 76.20), (175.26, 68.58, 175.26, 71.12), (190.50, 68.58, 190.50, 71.12),
    # ADR4525
] + barra(114.30, [30.48, 38.10, 50.80]) + [
    (38.10, 114.30, 38.10, 116.84), (38.10, 124.46, 38.10, 127.00), (63.50, 132.08, 63.50, 134.62),
] + barra(114.30, [76.20, 86.36, 93.98, 114.30]) + [
    (86.36, 114.30, 86.36, 116.84), (86.36, 124.46, 86.36, 127.00),
    # TL431 e o seu divisor
    (124.46, 114.30, 124.46, 111.76), (124.46, 111.76, 132.08, 111.76), (132.08, 111.76, 139.70, 111.76),
    (139.70, 111.76, 139.70, 119.38), (124.46, 121.92, 137.16, 121.92),
    (124.46, 129.54, 124.46, 132.08), (139.70, 124.46, 139.70, 127.00),
]

JUNCOES = [(33.02, 68.58), (68.58, 63.50), (81.28, 63.50), (88.90, 63.50), (96.52, 63.50), (106.68, 63.50),
           (114.30, 63.50), (68.58, 73.66), (160.02, 58.42), (175.26, 58.42), (190.50, 58.42),
           (38.10, 114.30), (86.36, 114.30), (93.98, 114.30), (132.08, 111.76), (124.46, 121.92)]
ROTULOS = [("FB_5V", 62.23, 73.66), ("EN_3V3", 123.19, 73.66), ("BYP_3V3", 153.67, 66.04), ("FB_CLAMP", 125.73, 121.92)]
NC = [(48.26, 60.96), (50.80, 60.96), (53.34, 60.96),
      (50.80, 121.92), (50.80, 124.46), (76.20, 121.92), (76.20, 124.46), (63.50, 106.68)]

NOTAS_D = (160.02, 91.44, [
    "DECISOES DESTA FOLHA (F2 2.2b - planejamento_pcb_EBM2_V5.md rev.3)",
    "1. U200 TPS7A4001: entrada 7-100 V, saida max 50 mA, Iq 25 uA.",
    "   Carga real ~3,7 mA (ADC 0,55 + ISO lado 2 ~2 + ADR 0,95 + NTC 0,21).",
    "   Dissipa (24-5) x 5 mA = 95 mW no HVSSOP com pad termico.",
    "2. VOUT por R201/R202: VREF 1,173 V (datasheet 1,161-1,185).",
    "   R1/R2 = 5/1,173 - 1 = 3,2625 -> 32k4/10k -> VOUT = 4,974 V.",
    "   Divisor = 118 uA, acima dos 10 uA minimos do datasheet.",
    "3. NAO se porta o comutado R-78HB da legacy: exigiria 45 mA de",
    "   pre-carga para 4 mA de carga. Um linear resolve sem pre-carga.",
    "4. Duas etapas: o SPX3819 e de baixo ruido, o TPS7A4001 nao.",
    "   O ultimo trilho alimenta o VDD do ADC e a referencia.",
    "5. U202 ADR4525 alimenta-se de 3V3_REF: VIN 3-15 V, queda max",
    "   500 mV (Tabela 2): com 3,3 V sobram 0,3 V de margem.",
    "   Grau B: erro inicial +-0,02 %, TC 4 ppm/C pelo metodo bowtie.",
    "6. +2V5_REF alimenta o VREF do MCP3208 e o topo do divisor do NTC",
    "   (folha 07). Carga 160-354 uA; o ADR4525 fornece 10 mA e a sua",
    "   regulacao de carga e 80 ppm/mA max: 0,003 %.",
])
NOTAS_E = (25.40, 147.32, [
    "7. U203 TL431 a 3,6 V = SUMIDOURO dos clamps de campo.",
    "   R204/R205 = 4k42/10k -> 2,495 x (1 + 4,42/10) = 3,60 V.",
    "   ACHADO V4.1: 3V3_REF nao tinha sumidouro. Seis clamps despejavam corrente",
    "   num LDO, que nao absorve, e em 2,3 uF: o trilho subia sem limite.",
    "   Uma proteccao e um caminho ate ao sumidouro, nao uma peca. Corrente por canal: na 2.3b.",
    "8. C208 no pino BP do SPX3819: baixa o ruido do LDO (datasheet MaxLinear, aplicacao).",
    "9. Pinos NIC e DNC do ADR4525 e NC do TPS7A4001 com no-connect explicito.",
    MARCA + ": os nomes de rede nao se sobrepoem.",
    "    O trilho corre em fio entre os condensadores.",
])

# ---------------------------------------------------------------- 3. autoverificacao de ligacao
pinos = {}
for ref in COMP:
    blk = simb[ref]
    lib = re.search(r'\(lib_id "([^"]+)"', blk).group(1)
    x, y, rot, _ = POS[ref]
    for n, (px, py, a, nome) in LIB[lib].items():
        pinos["%s.%s" % (ref, n)] = pos_pino(px, py, x, y, rot)
pontos_pino = {}
for k, p in pinos.items():
    pontos_pino.setdefault(p, []).append(k)
for v, x, y in PORTOS:
    pontos_pino.setdefault((x, y), []).append("porto:" + v)


def sobre(p, s):
    (x, y), (x1, y1, x2, y2) = p, s
    if abs(x1 - x2) < 1e-6:
        return abs(x - x1) < 1e-6 and min(y1, y2) + 1e-6 < y < max(y1, y2) - 1e-6
    return abs(y - y1) < 1e-6 and min(x1, x2) + 1e-6 < x < max(x1, x2) - 1e-6


erros = []
pontas = {}
for s in FIOS:
    for p in ((s[0], s[1]), (s[2], s[3])):
        pontas[p] = pontas.get(p, 0) + 1
for p, n in pontas.items():
    if n == 1 and p not in pontos_pino:
        erros.append("ponta de fio solta em %s" % (p,))
    tot = n + len({q.split('.')[0] for q in pontos_pino.get(p, [])})   # pinos empilhados do mesmo CI contam como um
    if tot >= 3 and p not in JUNCOES:
        erros.append("no com %d ligacoes sem juncao em %s" % (tot, p))
for p, quem in pontos_pino.items():
    for s in FIOS:
        if sobre(p, s):
            erros.append("pino %s cai no meio do fio %s" % (quem, s))
for p in JUNCOES:
    if pontas.get(p, 0) + len({q.split('.')[0] for q in pontos_pino.get(p, [])}) < 3:
        erros.append("juncao desnecessaria em %s" % (p,))
nc_pinos = {p: q for p, q in pontos_pino.items() if p in NC}
for p in NC:
    if p not in pontos_pino:
        erros.append("no-connect fora de pino em %s" % (p,))
    elif p in pontas:
        erros.append("no-connect num pino ligado em %s" % (p,))
ligados = set(pontas) | set(JUNCOES)
for k, p in pinos.items():
    if p not in ligados and p not in NC:
        erros.append("pino sem ligacao: %s em %s" % (k, p))
if erros:
    print("AUTOVERIFICACAO FALHOU:")
    for e in erros: print("   ", e)
    sys.exit(1)
print("autoverificacao de ligacao: OK (%d pinos, %d fios, %d juncoes, %d no-connect)"
      % (len(pinos), len(FIOS), len(JUNCOES), len(NC)))


# ---------------------------------------------------------------- 4. construir os blocos
def canon_effects(just):
    j = "\n\t\t\t\t(justify %s)" % just if just else ""
    return "(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)%s\n\t\t\t)" % j


def mexe_prop(blk, nome, x, y, ang, just, esconder):
    k = blk.find('(property "%s" ' % nome)
    if k < 0:
        return blk
    e = fim(blk, k)
    p = blk[k:e]
    p = re.sub(r"\(at [-\d.]+ [-\d.]+ [-\d.]+\)", "(at %s %s %s)" % (f(x), f(y), f(ang)), p, count=1)
    ke = p.find("(effects")
    p = p[:ke] + canon_effects(just) + p[fim(p, ke):]
    if esconder and "(hide yes)" not in p:
        p = re.sub(r"(\(at [-\d.]+ [-\d.]+ [-\d.]+\))", r"\1\n\t\t\t(hide yes)", p, count=1)
    return blk[:k] + p + blk[e:]


def coloca(blk, x, y, rot, campos):
    blk = re.sub(r"\(at [-\d.]+ [-\d.]+ [-\d.]+\)", "(at %s %s %s)" % (f(x), f(y), f(rot)), blk, count=1)
    for nome in re.findall(r'\(property "([^"]+)"', blk):
        if nome in campos:
            cx, cy, ca, cj = campos[nome]
            blk = mexe_prop(blk, nome, cx, cy, ca, cj, False)
        else:
            blk = mexe_prop(blk, nome, x, y, rot, None, True)
    return blk


novos = []
for ref in COMP:
    x, y, rot, campos = POS[ref]
    novos.append(coloca(simb[ref], x, y, rot, campos))

for i, (v, x, y) in enumerate(PORTOS):
    ref = "#PWR%d" % (301 + i)
    blk = MODELO_TRILHO[v]
    velho = re.search(r'\(property "Reference" "([^"]+)"', blk).group(1)
    blk = re.sub(r'\(uuid "[^"]+"\)', lambda m: '(uuid "%s")' % nu(), blk)
    blk = blk.replace('"Reference" "%s"' % velho, '"Reference" "%s"' % ref)
    blk = blk.replace('(reference "%s")' % velho, '(reference "%s")' % ref)
    dy = 3.81 if v == "GND_ADC" else -3.81
    blk = coloca(blk, x, y, 0, {"Value": (x, y + dy, 0, None)})
    novos.append(blk)


def fio(x1, y1, x2, y2):
    return ('\t(wire\n\t\t(pts\n\t\t\t(xy %s %s) (xy %s %s)\n\t\t)\n\t\t(stroke\n\t\t\t(width 0)\n'
            '\t\t\t(type default)\n\t\t)\n\t\t(uuid "%s")\n\t)' % (f(x1), f(y1), f(x2), f(y2), nu()))


itens = [fio(*s) for s in FIOS]
itens += ['\t(junction\n\t\t(at %s %s)\n\t\t(diameter 0)\n\t\t(color 0 0 0 0)\n\t\t(uuid "%s")\n\t)' % (f(x), f(y), nu())
          for x, y in JUNCOES]
itens += ['\t(no_connect\n\t\t(at %s %s)\n\t\t(uuid "%s")\n\t)' % (f(x), f(y), nu()) for x, y in NC]
itens += ['\t(label "%s"\n\t\t(at %s %s 0)\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n'
          '\t\t\t(justify left bottom)\n\t\t)\n\t\t(uuid "%s")\n\t)' % (n, f(x), f(y), nu()) for n, x, y in ROTULOS]
for x0, y0, linhas in (NOTAS_D, NOTAS_E):
    for i, L in enumerate(linhas):
        assert '"' not in L and "\\" not in L
        x, y = x0, y0 + i * 3.81
        xe = x + len(L) * 1.15
        assert xe <= 287.0 and not (xe > 175.0 and y > 164.0) and y <= 195.0, "nota fora do quadro: %r" % L
        itens.append('\t(text "%s"\n\t\t(exclude_from_sim no)\n\t\t(at %s %s 0)\n\t\t(effects\n\t\t\t(font\n'
                     '\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify left bottom)\n\t\t)\n\t\t(uuid "%s")\n\t)'
                     % (L, f(x), f(y), nu()))

# ---------------------------------------------------------------- 5. montar o ficheiro
t = T0
apagar = []
for cab in ("symbol", "wire", "junction", "label", "no_connect", "text"):
    apagar += topo(t, cab)
apagar.sort()
lib_a, lib_b = topo(t, "lib_symbols")[0]
assert all(not (lib_a <= a < lib_b) for a, b in apagar), "tentou apagar dentro de lib_symbols"
for a, b in reversed(apagar):
    t = t[:a] + t[b + 1:]
la, lb = topo(t, "lib_symbols")[0]
t = t[:lb] + "\n" + "\n".join(itens + novos) + t[lb:]
velho = '(comment 3 "RESSALVA: F1 formal saltada. MPN dos passivos por fixar na BOM preliminar.")'
assert t.count(velho) == 1
t = t.replace(velho, '(comment 3 "F0/F1 concluidas (planejamento rev.3). MPN dos passivos na BOM preliminar.")')

# ---------------------------------------------------------------- 6. guardas de escrita
assert not re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", t), "caractere de controlo"
assert not re.search(r"\(at [-\d.]+ [-\d.]+ \)", t), "(at x y) sem angulo"
assert "999999" not in t and "justify center" not in t
d = 0; dentro = False
for i, c in enumerate(t):
    if c == '"' and t[i - 1] != "\\":
        dentro = not dentro
    elif not dentro:
        d += (c == "(") - (c == ")")
        assert d >= 0
assert d == 0 and not dentro, "parenteses desequilibrados"
la, lb = topo(t, "lib_symbols")[0]
fora = sorted({v for m in re.finditer(r"\((?:at|xy) (-?[\d.]+) (-?[\d.]+)", t[:la] + t[lb:])
               for v in m.groups() if abs(float(v) / 1.27 - round(float(v) / 1.27)) > 0.004})
assert not fora, "fora da grelha: %s" % fora
cont = {c: len(topo(t, c)) for c in ("symbol", "wire", "junction", "label", "no_connect", "text")}
print("itens depois:", cont)
print("== guardas: controlo, angulo, 999999, justify, parenteses, grelha: OK ==")

if not APLICAR:
    print("ENSAIO terminado. Nada foi escrito.")
    sys.exit(0)
assert io.open(F, encoding="utf-8").read() == T0, "a folha mudou no disco durante o ensaio"
shutil.copy2(F, F + ".antes_redesenho")
io.open(F, "w", encoding="utf-8", newline="").write(t)
print("ESCRITO:", F)
