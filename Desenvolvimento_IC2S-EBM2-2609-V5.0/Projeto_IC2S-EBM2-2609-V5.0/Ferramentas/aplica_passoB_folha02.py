# -*- coding: utf-8 -*-
"""F2 / 2.2b - passo B na folha 02_entrada.

Aplica a lista fechada que a F1 deixou (planejamento_pcb_EBM2_V5.md §8b) e os
defeitos que o render da folha mostrou:
  1. F201 = CC12H250MA-TR (a serie CC12H nao tem 100 mA)
  2. R206 = 22 ohm 0805 entre o catodo de D201 e a derivacao de C200
  3. C200 passa a 1206 (0603 era herdada de uma peca de 25 V)
  4. notas refeitas: unidades em A2s, nota 5 contraditoria, D201/D202 trocados
  5. rotulos +24V_FUS_* deixam de pisar o texto dos diodos (filas alongadas)
  6. bloco de notas desloca-se para x = 152,40 para dar espaco ao circuito
  7. ressalva do bloco de titulo

Sem argumentos: ENSAIO (mostra o estado antes e o que faria, nao escreve).
Com --aplicar: backup .antes_passoB, escreve, copia a pegada 0805R.
"""
import io, os, re, shutil, subprocess, sys, uuid

F   = r"C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\02_entrada.kicad_sch"
LIB = r"C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\footprints\EBM2_V5.pretty"
STD = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Resistor_SMD.pretty\R_0805_2012Metric.kicad_mod"
APLICAR = "--aplicar" in sys.argv

# ---------------------------------------------------------------- guardas
# O KiCad 10 corre os editores dentro de kicad.exe, por isso o nome do processo
# nao diz que projecto esta aberto. Os titulos das janelas dizem.
PS1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), "janelas_kicad.ps1")
tit = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", PS1],
                     capture_output=True, text=True).stdout.splitlines()
tit = [x.strip() for x in tit if x.strip()]
if tit:
    print("janelas KiCad abertas:", tit)
if any(("EBM2_V5" in x) or ("EBM2 V5" in x) for x in tit):
    sys.exit("ABORTA: o projecto EBM2 V5 esta aberto no KiCad - ele nao rele do disco e pisaria a escrita")

t = io.open(F, encoding="utf-8").read()
if '"R206"' in t:
    sys.exit("ABORTA: R206 ja existe. O script nao e idempotente: restaurar o backup antes.")
mtime_antes = os.path.getmtime(F)


def fim(s, i):
    d = 0; dentro = False; n = len(s)
    while i < n:
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
    raise ValueError("parenteses por fechar a partir de %d" % i)


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


def simbolo(s, ref):
    for a, b in topo(s, "symbol"):
        if re.search(r'\(property "Reference" "%s"' % re.escape(ref), s[a:b]):
            return a, b
    raise KeyError(ref)


def fmt(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def pos(blk):
    m = re.search(r"\(at (-?[\d.]+) (-?[\d.]+)", blk)
    return float(m.group(1)), float(m.group(2))


def num(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


def desloca(blk, dx, dy=0.0):
    # conserva a cadeia original no eixo que nao se move: nao arredondar o que nao se pediu
    def f(m):
        x = m.group(1) if dx == 0 else num(float(m.group(1)) + dx)
        y = m.group(2) if dy == 0 else num(float(m.group(2)) + dy)
        return "(at %s %s" % (x, y)
    return re.sub(r"\(at (-?[\d.]+) (-?[\d.]+)", f, blk)


def nu():
    return str(uuid.uuid4())


# ------------------------------------------------ 1. mover simbolos (ensaio verifica o antes)
MOV = {  # ref: (x antes, y antes, dx)
    "D201": (82.55, 63.50, 12.70), "D202": (82.55, 101.60, 12.70),
    "C200": (93.98, 72.39, 38.10), "C201": (93.98, 110.49, 38.10),
    "#PWR201": (93.98, 76.20, 38.10), "#PWR205": (93.98, 114.30, 38.10),
    "#PWR204": (101.60, 63.50, 36.83), "#FLG203": (101.60, 63.50, 36.83),
    "#PWR208": (101.60, 101.60, 36.83), "#FLG202": (101.60, 101.60, 36.83),
}
print("== ENSAIO: estado antes ==")
for ref, (x0, y0, dx) in MOV.items():
    a, b = simbolo(t, ref)
    x, y = pos(t[a:b])
    ok = abs(x - x0) < 0.01 and abs(y - y0) < 0.01
    print("  %-8s em (%.2f, %.2f) -> (%.2f, %.2f)  %s" % (ref, x, y, x + dx, y, "ok" if ok else "*** DIFERENTE DO ESPERADO ***"))
    if not ok:
        sys.exit("ABORTA: a folha nao esta no estado que foi mostrado ao projectista")
for ref, (x0, y0, dx) in MOV.items():
    a, b = simbolo(t, ref)
    t = t[:a] + desloca(t[a:b], dx) + t[b:]

# ------------------------------------------------ 2. apagar fios das duas filas
FIOS = {
    "d2f8661d-f478-4232-8db2-ccfaff3cad11": "(xy 71.12 63.5) (xy 78.74 63.5)",
    "58a9b062-8e9a-4948-928c-f7a5626254b6": "(xy 86.36 63.5) (xy 93.98 63.5)",
    "73b38f92-edcd-4376-9798-23d29f5aaf37": "(xy 93.98 63.5) (xy 101.6 63.5)",
    "df34441a-cc6d-492b-8c3e-eba0dd58a67e": "(xy 93.98 63.5) (xy 93.98 68.58)",
    "138dbbce-d5c4-43ca-aa47-fdab51f9f7fb": "(xy 71.12 101.6) (xy 78.74 101.6)",
    "2008b1ac-75ca-4427-b83b-a5846be21000": "(xy 86.36 101.6) (xy 93.98 101.6)",
    "2d9078d4-d21d-4d67-9c2e-e5a595b20a20": "(xy 93.98 101.6) (xy 101.6 101.6)",
    "b9c632ae-8303-413d-8662-9a40fce13b30": "(xy 93.98 101.6) (xy 93.98 106.68)",
}
for u, pts in FIOS.items():
    k = t.find('(uuid "%s")' % u)
    assert k > 0, "fio %s nao encontrado" % u
    a = t.rfind("\n\t(wire", 0, k) + 1
    b = fim(t, a)
    assert pts in t[a:b], "fio %s nao tem os pontos esperados" % u
    t = t[:a] + t[b + 1:]          # +1 leva o \n que fecha a linha
print("  fios apagados: %d" % len(FIOS))

# ------------------------------------------------ 3. mover as duas juncoes de derivacao
for y in ("63.5", "101.6"):
    velho = "(junction\n\t\t(at 93.98 %s)" % y
    assert t.count(velho) == 1, "juncao em (93.98, %s) nao encontrada ou duplicada" % y
    t = t.replace(velho, "(junction\n\t\t(at 132.08 %s)" % y)
print("  juncoes movidas: 2")

# ------------------------------------------------ 4. apagar o bloco de notas antigo
notas = [(a, b) for a, b in topo(t, "text") if re.search(r"\(at 114\.30? ", t[a:b])]
assert len(notas) == 30, "esperava 30 linhas de nota, ha %d" % len(notas)
for a, b in reversed(notas):
    t = t[:a] + t[b + 1:]
print("  linhas de nota apagadas: %d" % len(notas))

# ------------------------------------------------ 5. F201, C200
a, b = simbolo(t, "F201"); blk = t[a:b]
blk = blk.replace('(property "Value" "100mA T"', '(property "Value" "CC12H250MA-TR"', 1)
blk = blk.replace('(property "MPN" ""', '(property "MPN" "CC12H250MA-TR"', 1)
blk = blk.replace('(property "Description" ""',
                  '(property "Description" "Eaton CC12H 250 mA alto I2t, Technical Data 4309 pag. 2. So cumpre RA2 com R206"', 1)
assert '"CC12H250MA-TR"' in blk
t = t[:a] + blk + t[b:]

a, b = simbolo(t, "C200"); blk = t[a:b]
assert '"EBM2_V5:0603C"' in blk
blk = blk.replace('"EBM2_V5:0603C"', '"EBM2_V5:1206C120"', 1)
blk = blk.replace('(property "Description" ""',
                  '(property "Description" "2,2 uF >= 100 V X7R 1206, >= 1 uF efectivo a 24 V. MPN por fixar - V2"', 1)
t = t[:a] + blk + t[b:]
print("  F201 -> CC12H250MA-TR | C200 -> 1206C120")

# ------------------------------------------------ 6. novos fios, rotulo, notas
def fio(x1, y1, x2, y2):
    return ('\t(wire\n\t\t(pts\n\t\t\t(xy %s %s) (xy %s %s)\n\t\t)\n\t\t(stroke\n\t\t\t(width 0)\n'
            '\t\t\t(type default)\n\t\t)\n\t\t(uuid "%s")\n\t)\n' % (fmt(x1), fmt(y1), fmt(x2), fmt(y2), nu()))

NOVOS_FIOS = [
    (71.12, 63.5, 91.44, 63.5), (99.06, 63.5, 119.38, 63.5), (127.00, 63.5, 132.08, 63.5),
    (132.08, 63.5, 138.43, 63.5), (132.08, 63.5, 132.08, 68.58),
    (71.12, 101.6, 91.44, 101.6), (99.06, 101.6, 132.08, 101.6),
    (132.08, 101.6, 138.43, 101.6), (132.08, 101.6, 132.08, 106.68),
]
novo = "".join(fio(*f) for f in NOVOS_FIOS)
novo += ('\t(label "+24V_DIO_REG"\n\t\t(at 100.33 63.50 0)\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n'
         '\t\t\t)\n\t\t\t(justify left bottom)\n\t\t)\n\t\t(uuid "%s")\n\t)\n' % nu())

NOTAS = [
    "DECISOES DESTA FOLHA (F2 2.2b - fonte: planejamento_pcb_EBM2_V5.md rev.3)",
    "1. D200 = SMA6J33A-Q (Bourns): VRWM 33 V, VBR 36,7-40,6 V,",
    "   clamp 58,1 V @ 11,3 A - tabela de seleccao, linha VRWM=33.",
    "   ATENCAO: a folha equivalente da EBM7 legacy cita 53,3 V:",
    "   esse valor e da linha VRWM=30. Para esta peca sao 58,1 V.",
    "2. F202 (rama dos lacos) = CC12H750MA-TR (Eaton, alto I2t).",
    "   Leva 125 mA (6 x 20 mA + 3 LED). I2t de fusao 0,15 A2s.",
    "   Arranque de C201: 576 x 10e-6 / (2 x 0,8) = 3,6e-3 A2s: 41,7x.",
    "3. F201 (rama do regulador) = CC12H250MA-TR. A serie CC12H NAO",
    "   tem 100 mA: comeca em 250 mA (Technical Data 4309, pag. 2).",
    "4. D201/D202 = MBR1H100SF (100 V), NAO PMEG6010CEH (60 V): com",
    "   o clamp de 58,1 V sobrariam 1,9 V. D201 = regulador, D202 = lacos.",
    "5. C201 = 10 uF 100 V ceramico 1210: os electroliticos de 50 V",
    "   da V4.1 (C12/C28) ficariam 8,1 V abaixo do clamp.",
    "6. R200 = net-tie 0R, UNICA uniao GND_24V <-> GND_ADC.",
    "7. Diodos: pino 1 = CATODO (convencao KiCad = Nexperia).",
    "8. Trilhos como power ports globais: o nome da rede vem do",
    "   campo Value e casa letra por letra com a netlist.",
    "9. SAI da V4.1: o zener D26 de 2,45 V em serie na entrada,",
    "   um zener de classe uA a conduzir ~130 mA da placa.",
    "10. C200 = 2,2 uF, NAO 10 uF: o TPS7A4001 so pede Cin > 1 uF.",
    "    100 V X7R em 1206: a 0603 herdada era de uma peca de 25 V.",
    "    MPN por fixar (V2): >= 1 uF efectivo a 24 V de polarizacao.",
    "11. R206 = 22 ohm limita o arranque de C200 atraves de F201:",
    "    I2t = 576 x 2,2e-6 / (2 x 25,5) = 2,48e-5 A2s contra",
    "    3,8e-4 A2s de fusao: margem 15,3x (RA2 exige 10x).",
    "    Sem R206 seriam 2,1x. Nenhum outro CC12H resolve.",
    "    Fica ANTES da derivacao de C200: depois nao limitaria nada.",
    "    Custo a 12 mA: 0,26 V e 3,2 mW. Pico 0,94 A, 56 us, 0,55 mJ.",
    "    MPN por fixar (V1): 0805 com curva de impulso para 0,55 mJ.",
    "12. Avaria medida na V4.1: F7/F9 = 3413.0008.22, I2t de fusao",
    "    1,5e-3 A2s, contra 10 uF de arranque = 5,65e-3 A2s com",
    "    R=0,51 ohm (1,69e-3 com R=1,7). Acima nos dois casos.",
    "ERC pendente estrutural: +24V e GND_24V sem driver ate existir",
    "a folha 1 (PWR_FLAG pertence ao P1, fonte passiva real).",
]
NX, NY, NDY = 152.40, 27.94, 3.81
for i, L in enumerate(NOTAS):
    assert '"' not in L and "\n" not in L and "\\" not in L
    x, y = NX, NY + i * NDY
    # guarda de moldura A4 e do bloco de titulo, com 1,15 mm por caracter (medido)
    xe = x + len(L) * 1.15
    assert xe <= 287.0, "nota fora da moldura: %r" % L
    assert not (xe > 175.0 and y > 164.0), "nota invade o bloco de titulo: %r" % L
    novo += ('\t(text "%s"\n\t\t(exclude_from_sim no)\n\t\t(at %s %s 0)\n\t\t(effects\n\t\t\t(font\n'
             '\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify left bottom)\n\t\t)\n\t\t(uuid "%s")\n\t)\n'
             % (L, fmt(x), fmt(y), nu()))
print("  notas novas: %d linhas, de y=%.2f a y=%.2f" % (len(NOTAS), NY, NY + (len(NOTAS) - 1) * NDY))

a0 = topo(t, "symbol")[0][0]
t = t[:a0] + novo + t[a0:]

# ------------------------------------------------ 7. R206 a partir de R200
a, b = simbolo(t, "R200")
r = t[a:b]
r = desloca(r, 123.19 - 80.01, 63.50 - 165.10)
r = re.sub(r'\(uuid "[^"]+"\)', lambda m: '(uuid "%s")' % nu(), r)
r = r.replace('"Reference" "R200"', '"Reference" "R206"').replace('(reference "R200")', '(reference "R206")')
r = r.replace('(property "Value" "0R"', '(property "Value" "22R"')
r = r.replace('"EBM2_V5:0603R"', '"EBM2_V5:0805R"')
r = r.replace('(property "MPN" "RC0603JR-070RL"', '(property "MPN" ""')
r = r.replace('(property "Description" ""',
              '(property "Description" "22 ohm 0805 anti-surto: limita o arranque de C200 (nota 11). MPN por fixar - V1"')
assert '"R206"' in r and '"22R"' in r and '"EBM2_V5:0805R"' in r and "R200" not in r
ult = topo(t, "symbol")[-1][1]
t = t[:ult] + "\n" + r + t[ult:]
print("  R206 inserido em (123.19, 63.5) rot 90")

# ------------------------------------------------ 8. ressalva do bloco de titulo
velho = '(comment 3 "RESSALVA: F1 formal saltada. Bloco portado da EBM7 V2.3 legacy; MPN do F201 por confirmar.")'
assert t.count(velho) == 1
t = t.replace(velho, '(comment 3 "F0 e F1 concluidas (planejamento_pcb_EBM2_V5.md rev.3). Abertas: V1 MPN de R206, V2 MPN de C200.")')

# ------------------------------------------------ guardas de escrita
assert not re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", t), "caractere de controlo"
assert not re.search(r"\(at [-\d.]+ [-\d.]+ \)", t), "(at x y) sem angulo"
assert "999999" not in t, "coordenada 999999"
assert "justify center" not in t, "justify center apaga o resto do ficheiro"
d = 0; dentro = False
for i, c in enumerate(t):
    if c == '"' and t[i - 1] != "\\":
        dentro = not dentro
    elif not dentro:
        d += (c == "(") - (c == ")")
        assert d >= 0, "parentese a fechar a mais em %d" % i
assert d == 0 and not dentro, "parenteses desequilibrados (%d) ou cadeia aberta" % d
fora = []
def fora_grelha(s):
    a_, b_ = topo(s, "lib_symbols")[0]      # geometria interna da biblioteca nao e posicao na folha
    c_ = s[:a_] + s[b_:]
    res = {}
    for m in re.finditer(r"\((?:at|xy) (-?[\d.]+) (-?[\d.]+)", c_):
        if any(abs(float(v) / 1.27 - round(float(v) / 1.27)) > 0.004 for v in (m.group(1), m.group(2))):
            ctx = re.findall(r'\(property "Reference" "([^"]+)"', c_[max(0, m.start() - 3000):m.start()])
            res[m.group(0)] = ctx[-1] if ctx else "?"
    return res
T0 = io.open(F, encoding="utf-8").read()
velhos, novos = fora_grelha(T0), fora_grelha(t)
def valores_fora(d):
    out = set()
    for k in d:
        for v in k.split()[1:3]:
            if abs(float(v) / 1.27 - round(float(v) / 1.27)) > 0.004:
                out.add(v)
    return out
vv = valores_fora(velhos)
# um par conta como introduzido so se o seu valor fora da grelha nao existia antes
herdados = {k: v for k, v in novos.items() if valores_fora({k: v}) <= vv}
introduzidos = {k: v for k, v in novos.items() if not valores_fora({k: v}) <= vv}
print("  fora da grelha, herdados e nao tocados: %s" % sorted(herdados.items()))
assert not introduzidos, "coordenadas fora da grelha INTRODUZIDAS por este script: %s" % introduzidos
print("== guardas: controlo, angulo, 999999, justify, parenteses, grelha: OK ==")

if not APLICAR:
    print("\nENSAIO terminado. Nada foi escrito. Correr com --aplicar.")
    sys.exit(0)

assert os.path.getmtime(F) == mtime_antes, "a folha mudou no disco durante o ensaio"
shutil.copy2(F, F + ".antes_passoB")
io.open(F, "w", encoding="utf-8", newline="").write(t)

dst = os.path.join(LIB, "0805R.kicad_mod")
if not os.path.exists(dst):
    fp = io.open(STD, encoding="utf-8").read()
    assert fp.count('(footprint "R_0805_2012Metric"') == 1
    fp = fp.replace('(footprint "R_0805_2012Metric"', '(footprint "0805R"')
    io.open(dst, "w", encoding="utf-8", newline="").write(fp)
    print("pegada copiada:", dst)
print("ESCRITO:", F, "| backup:", F + ".antes_passoB")
