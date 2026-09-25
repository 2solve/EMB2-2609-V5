# -*- coding: utf-8 -*-
"""F3 etapa 3.2: medições do placement que o DRC não faz (antes do Portão 3).

1. Barreira: menor distância entre pads do domínio do barramento (DGND, +3.3V_DIG, +5V, MOSI, CLK, MISO, CS_ADC,
   e os NC do P1 que ficam desse lado) e pads do domínio de campo, EXCLUINDO os pares dentro do próprio U6.
   Os pads NC e sem rede não contam (não são cobre ligado). P1.19/P1.20 são de campo (entram por fio, RA1).
2. Desacoplamento: distância de centro a centro entre o pad do condensador e o pino que ele serve.
Uso: "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" mede_placement_F3.py
"""
import math
import pcbnew

PCB = r"C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\IC2S_Extension_Board-EBM2_V5.kicad_pcb"
b = pcbnew.LoadBoard(PCB)
mm = pcbnew.ToMM
BUS = {"DGND", "+3.3V_DIG", "+5V", "/1 Conectores/MOSI", "/1 Conectores/CLK", "/1 Conectores/MISO", "/1 Conectores/CS_ADC"}
pads = []
for f in b.GetFootprints():
    for p in f.Pads():
        n = p.GetNetname()
        if not n or n.startswith("unconnected-"):
            continue
        pads.append((f.GetReference(), p.GetNumber(), n, p))


def gap(p, q):
    """distância entre as bordas dos pads na face de cima (aproximação por caixas; THT conta nas duas faces)"""
    a, c = p.GetBoundingBox(), q.GetBoundingBox()
    dx = max(0, max(a.GetLeft(), c.GetLeft()) - min(a.GetRight(), c.GetRight()))
    dy = max(0, max(a.GetTop(), c.GetTop()) - min(a.GetBottom(), c.GetBottom()))
    return mm(math.hypot(dx, dy))


bus = [x for x in pads if x[2] in BUS]
campo = [x for x in pads if x[2] not in BUS and x[0] != "H1" and x[0] != "H2"]
res = []
for a in bus:
    for c in campo:
        if a[0] == "U6" and c[0] == "U6":
            continue
        res.append((gap(a[3], c[3]), "%s.%s (%s)" % (a[0], a[1], a[2]), "%s.%s (%s)" % (c[0], c[1], c[2])))
res.sort()
u6 = min(gap(a[3], c[3]) for a in bus if a[0] == "U6" for c in campo if c[0] == "U6")
print("1. BARREIRA: menor folga entre pads dentro do U6 (a barreira da própria peça): %.3f mm" % u6)
print("   menor folga fora do U6 (tem de ser >= a do U6):")
for d, a, c in res[:5]:
    print("     %.3f mm  %s  <->  %s" % (d, a, c))
print("   ->", "OK" if res[0][0] >= u6 else "ABAIXO DA BARREIRA DO U6")

fp = {f.GetReference(): f for f in b.GetFootprints()}


def pad(r, n):
    return [p for p in fp[r].Pads() if p.GetNumber() == n][0]


def dist(r1, n1, r2, n2):
    a, c = pad(r1, n1).GetPosition(), pad(r2, n2).GetPosition()
    return mm(math.hypot(a.x - c.x, a.y - c.y))


DEC = [("C16", "1", "U7", "16", "VDD do conversor"), ("C15", "1", "U7", "16", "VDD do conversor (1 uF)"),
       ("C14", "1", "U7", "15", "VREF do conversor"), ("C5", "1", "U2", "6", "saída do ADR4525"),
       ("C13", "1", "U6", "16", "VCC2 do isolador"), ("C12", "1", "U6", "1", "VCC1 do isolador"),
       ("C11", "1", "U5", "3", "saída do MCP1824ST"), ("C10", "1", "U5", "1", "entrada do MCP1824ST"),
       ("C4", "1", "U1", "1", "saída do U1"), ("C1", "1", "U1", "5", "entrada do U1 (pino 5; o 8 tambem e IN)"), ("C7", "1", "U1", "1", "C_BYP do U1"),
       ("C31", "1", "U14", "1", "saída do U14"), ("C30", "1", "U14", "8", "entrada do U14"), ("C33", "1", "U14", "1", "C_BYP do U14"),
       ("C8", "1", "U4", "5", "saída do U4 (3V3_REF)"), ("C9", "1", "U3", "1", "cátodo do TL431")]
DEC += [("C%d" % (16 + k), "1", "U%d" % (7 + k), "6", "+Vs do TPS26613 canal %d" % k) for k in range(1, 7)]
print("2. DESACOPLAMENTO (centro do pad do C ao centro do pino):")
for c, n, u, pn, o in DEC:
    d = dist(c, n, u, pn)
    print("   %-4s -> %s.%-2s %5.2f mm  %s%s" % (c, u, pn, d, o, "   <-- longe" if d > 4 else ""))
