# -*- coding: utf-8 -*-
"""F3 etapa 3.2 (skill 2shw-pcb:layout): placement inicial da EBM2 V5 sobre a planta de zonas aprovada
(Documentos/F3/planta_zonas_EBM2_V5.png, projectista 2026-09-25). Só face de cima (resposta do projectista).

Não toca no que está bloqueado (P1, P2, H1, H2, D1, D5, D24). Coordenadas absolutas em mm, rotação em graus.
Canais: uma fila por canal, y_k = 85,45 + 5,9 (k - 1); da direita (P2) para a esquerda:
  TVS do terminal D(11+k) · TVS do retorno D(5+k) · [fusível F(2+k) / burden R(15+k)] · TPS26613 U(7+k) com
  C(16+k) em cima · [0 ohm R(9+k) / 3k3 R(21+k)] · BAV199 D(17+k) · [C do filtro C(22+k) / 4k7 R(27+k)] -> U7.
O U7 (SOIC16) ganha na placa o pátio F.CrtYd de ±3,4 x ±5,1 mm que a biblioteca tinha só no User.15.
Uso: "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" coloca_F3.py      (backup .antes_placement)
"""
import os, shutil, sys
import pcbnew

PCB = r"C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\IC2S_Extension_Board-EBM2_V5.kicad_pcb"
MM = pcbnew.FromMM

P = {
    # --- digital (DGND), à esquerda da barreira
    "U5": (125.8, 113.0, 0), "C10": (124.0, 119.3, 0), "C11": (127.6, 119.3, 0), "C12": (124.3, 99.2, 90),
    "TP8": (124.5, 106.0, 0),
    # --- isolador: a posicao e a rotacao do U4 da V4.1 (atravessa a barreira)
    "U6": (130.19, 99.84, 0),
    # --- isolador: lado de campo
    "FB1": (132.5, 93.0, 0), "C13": (133.0, 95.0, 0),
    # --- conversor e referência
    "U7": (137.9, 96.0, 180),
    "C14": (135.5, 102.9, 0), "C16": (138.3, 102.9, 0), "C15": (136.9, 104.9, 0), "FB2": (140.2, 104.9, 0),
    "U2": (135.5, 82.4, 0), "C5": (140.5, 84.8, 90), "TP5": (136.4, 87.0, 0),
    "TH1": (133.5, 89.3, 0), "R40": (136.5, 89.3, 0), "C35": (139.6, 89.3, 0),
    # --- 3V3_REF (faixa de cima): U4, grampo U3, condensadores
    "R7": (142.0, 78.9, 90), "U4": (145.0, 79.0, 0), "C8": (150.4, 78.2, 0), "C9": (153.6, 80.9, 0),
    "C3": (150.4, 80.9, 0), "U3": (156.8, 79.0, 0), "R8": (160.4, 78.0, 0), "R9": (160.4, 80.3, 0),
    "TP7": (163.5, 78.5, 0),
    # --- +5V_ADC (U1) por baixo do conversor; U1 a 90 graus: OUT/FB para baixo, junto de C7/R5/R6
    "U1": (135.4, 109.6, 90), "C1": (139.8, 109.0, -90), "C4": (135.3, 114.05, 0), "C6": (139.6, 114.3, 0),
    "R5": (134.8, 117.9, 0), "R6": (137.6, 117.9, 0), "C7": (134.8, 116.1, 0),
    "TP6": (140.4, 117.3, 0), "R4": (142.4, 120.8, 90),
    # --- entrada de 24 V
    "D2": (126.8, 126.0, 0), "F1": (133.0, 125.0, 0), "D3": (138.6, 125.0, 0), "R3": (143.4, 125.0, 0),
    "TP3": (146.5, 125.0, 0), "F2": (133.0, 128.4, 0), "D4": (138.6, 128.4, 0), "C2": (143.6, 128.8, 0),
    "TP4": (147.0, 128.8, 0), "R2": (133.5, 132.4, 0), "TP2": (130.9, 132.6, 0), "TP1": (136.8, 132.4, 0),
    # --- +12V_TPS (U14) e LED
    "U14": (157.5, 127.5, 0), "C30": (162.4, 127.5, -90), "C29": (165.6, 127.5, -90),
    "C31": (150.2, 124.8, 180), "C32": (150.2, 128.0, 180), "R35": (150.2, 131.3, 0), "R36": (153.1, 131.3, 0),
    "C33": (153.5, 126.9, -90), "TP10": (159.2, 131.5, 0),
    "R37": (170.8, 124.0, 0), "R38": (170.8, 126.0, 0), "R39": (170.8, 128.0, 0), "C34": (170.8, 130.0, 0),
    "R34": (166.8, 120.8, 90), "R1": (155.0, 120.8, 90), "TP9": (148.8, 120.8, 0),
}
for k in range(1, 7):
    y = 85.45 + 5.9 * (k - 1)
    P["D%d" % (11 + k)] = (171.3, y, 180)          # TVS 36 V no terminal (LOOPk_V+), cátodo para o P2
    P["D%d" % (5 + k)] = (164.3, y, 180)           # TVS 33 V no retorno (AINk-)
    P["F%d" % (2 + k)] = (158.5, y - 1.35, 0)      # fusível 50 mA: +24V_ADC -> LOOPk_V+
    P["R%d" % (15 + k)] = (158.5, y + 1.35, 0)     # burden 110 ohm a GND_ADC
    P["U%d" % (7 + k)] = (153.9, y + 0.75, 180)    # TPS26613: IN do lado do P2, OUT para a esquerda
    P["C%d" % (16 + k)] = (153.9, y - 2.0, 0)      # +Vs 100 nF
    P["R%d" % (9 + k)] = (150.1, y - 1.4, 0)       # 0 ohm
    P["R%d" % (21 + k)] = (150.1, y + 1.4, 0)      # 3k3
    P["D%d" % (17 + k)] = (146.6, y, 0)            # BAV199, pino 3 (sinal) para a direita
    P["C%d" % (22 + k)] = (143.1, y - 1.4, 0)      # 100 nF do filtro
    P["R%d" % (27 + k)] = (143.1, y + 1.4, 0)      # 4k7 para o pino do U7

FIXOS = {"P1", "P2", "H1", "H2", "D1", "D5", "D24"}
b = pcbnew.LoadBoard(PCB)
refs = {f.GetReference(): f for f in b.GetFootprints()}
faltam = sorted(set(refs) - set(P) - FIXOS - {"FID1", "FID2", "FID3"})
assert not faltam, "sem posicao: %s" % faltam
assert not (set(P) - set(refs)), sorted(set(P) - set(refs))
for r in FIXOS:
    assert refs[r].IsLocked(), r
shutil.copy2(PCB, PCB + ".antes_placement")

u7 = refs["U7"]
if not any(it.GetLayer() == pcbnew.F_CrtYd for it in u7.GraphicalItems()):
    u7.SetOrientationDegrees(0)
    c = u7.GetPosition()
    sh = pcbnew.PCB_SHAPE(u7); sh.SetShape(pcbnew.SHAPE_T_RECT)
    sh.SetStart(pcbnew.VECTOR2I(c.x - MM(3.4), c.y - MM(5.1))); sh.SetEnd(pcbnew.VECTOR2I(c.x + MM(3.4), c.y + MM(5.1)))
    sh.SetLayer(pcbnew.F_CrtYd); sh.SetWidth(MM(0.05)); u7.Add(sh)

for r, (x, y, rot) in P.items():
    f = refs[r]
    assert not f.IsFlipped(), r
    f.SetOrientationDegrees(rot)
    f.SetPosition(pcbnew.VECTOR2I(MM(x), MM(y)))
    f.Value().SetVisible(False)          # o valor (MPN longo) não vai para a serigrafia
# na serigrafia só a referência: valor, MPN, descrição e datasheet ficam invisíveis em todas as pegadas
for f in refs.values():
    for campo in f.GetFields():
        if not campo.IsReference():
            campo.SetVisible(False)
pcbnew.SaveBoard(PCB, b)
print("colocadas:", len(P), "| fixas intocadas:", sorted(FIXOS))
