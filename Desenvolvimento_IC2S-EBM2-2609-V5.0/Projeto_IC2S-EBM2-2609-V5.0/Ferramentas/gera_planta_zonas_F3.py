# -*- coding: utf-8 -*-
"""F3 etapa 3.2: planta de zonas da EBM2 V5 (proposta para o projectista, antes do placement fino).

Desenha, a escala sobre o contorno real, as restricoes duras (P1/P2 com o numero e a rede de cada pino, H1/H2,
LED da V11) e as zonas funcionais propostas. Coordenadas KiCad (mm, y para baixo).
Uso: python gera_planta_zonas_F3.py  -> Documentos/F3/planta_zonas_EBM2_V5.svg e .png
"""
import os
import fitz

S = 14.0                      # px por mm
X0, Y0 = 118.5011, 75.0036
OUT = r"C:\hw\hw-ebm2-v5\Documentos\F3\planta_zonas_EBM2_V5"
M = 60                        # margem em px
ML = 150                      # margem esquerda (rotulos do P1)


def px(x, y):
    return ML + (x - X0) * S, M + 40 + (y - Y0) * S


P1 = {1: "nc", 2: "nc", 3: "DGND", 4: "MOSI", 5: "CLK", 6: "MISO", 7: "nc", 8: "nc", 9: "CS_ADC", 10: "nc", 11: "ID1 nc",
      12: "DGND", 13: "ID3 nc", 14: "nc", 15: "nc", 16: "DGND", 17: "+5V", 18: "nc", 19: "GND_24V", 20: "+24V"}
P2 = {1: "nc", 14: "GND_ADC"}
for k in range(1, 7):
    P2[2 * k] = "LOOP%d_V+" % k; P2[2 * k + 1] = "AIN%d-" % k

ZONAS = [  # (x0, y0, x1, y1, cor, titulo, linhas)
    (121.8, 76.0, 129.6, 123.2, "#dbe6f7", "DIGITAL", ["U5 MCP1824ST", "C10 C11", "FB1 C12", "TP8 (DGND)"]),
    (131.2, 77.0, 147.4, 110.0, "#e3f1e7", "CONVERSOR + REFERÊNCIA", ["U7 MCP3208 (posição da V4.1 U5)", "C14 C15 C16 · FB2", "TH1 R40 C35 (V4.1 R5/R8)",
                                                                       "U2 ADR4525 · U3 TL431 · U4", "R8 R9 · C5 C7 C8 C9 · TP5 TP7"]),
    (147.8, 82.3, 175.2, 113.0, "#f6e9d8", "SEIS LAÇOS · GND_ADC", ["uma fila por canal, no par de pinos do P2", "canal 1 em cima (P2.2/3) ... canal 6 (P2.12/13)",
                                                                   "P2 → F / TVS → U8-13 TPS26613 → 0 Ω", "→ burden 1206 → 3k3 → C + BAV199 → 4k7 → U7"]),
    (147.8, 114.0, 175.2, 134.4, "#f2e4f2", "+12V_TPS", ["U14 TPS7A4001 · C29-C34", "R35-R39 (VSNS) · TP10", "LED D24 + R34 (fixo)"]),
    (131.2, 111.0, 147.4, 122.6, "#fbf1d3", "+5V_ADC", ["U1 TPS7A4001 · C3 C4 C6", "R5 R6 · TP6", "LED D5 + R4 (fixo)"]),
    (129.9, 123.4, 147.4, 134.4, "#f7dcdc", "ENTRADA 24 V", ["D2 TVS · F1 F2 · D3 D4", "R3 150 Ω · C1 · C2 1210", "R2 net-tie · TP1-TP4", "(D1 da entrada fixo ao centro, R1 ao lado)"]),
]


def svg():
    w, h = ML + M + 60 * S + 200, 2 * M + 60 * S + 80
    s = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" font-family="Helvetica, Arial" font-size="12">' % (w, h),
         '<rect width="100%" height="100%" fill="white"/>',
         '<text x="%d" y="%d" font-size="20" font-weight="bold">EBM2 V5 — planta de zonas proposta (F3 3.2, vista de cima)</text>' % (ML, 30),
         '<text x="%d" y="%d" fill="#555">Contorno 60 × 60 mm da V4.1 · componentes só na face de cima · P1/P2 pinos a vermelho = face inferior</text>' % (ML, 50)]
    a, b = px(X0, Y0); c, d = px(X0 + 60, Y0 + 60)
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#1f5130" fill-opacity="0.08" stroke="black" stroke-width="2"/>' % (a, b, c - a, d - b))
    for x0, y0, x1, y1, cor, tit, lin in ZONAS:
        a, b = px(x0, y0); c, d = px(x1, y1)
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="6" fill="%s" stroke="#666"/>' % (a, b, c - a, d - b, cor))
        s.append('<text x="%.1f" y="%.1f" font-weight="bold" font-size="13">%s</text>' % (a + 6, b + 17, tit))
        for i, l in enumerate(lin):
            s.append('<text x="%.1f" y="%.1f" font-size="11">%s</text>' % (a + 6, b + 33 + 14 * i, l))
    # barreira: entre x 129,6 e 131,2 ate y 123,3; depois horizontal entre P1.17 e P1.19
    pts = [px(130.4, Y0), px(130.4, 123.3), px(X0, 123.3)]
    s.append('<polyline points="%s" fill="none" stroke="#c00" stroke-width="3" stroke-dasharray="8 5"/>' % " ".join("%.1f,%.1f" % p for p in pts))
    x, y = px(130.4, 76.5); s.append('<text x="%.1f" y="%.1f" fill="#c00" font-weight="bold" transform="rotate(90 %.1f %.1f)">BARREIRA FUNCIONAL — só o U6 ISO7141 a atravessa</text>' % (x + 4, y, x + 4, y))
    # U6
    a, b = px(130.19 - 3.6, 99.84 - 3.0); c, d = px(130.19 + 3.6, 99.84 + 3.0)
    s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#9fb8e8" stroke="black"/>' % (a, b, c - a, d - b))
    s.append('<text x="%.1f" y="%.1f" font-weight="bold">U6</text>' % (a + 2, b + 14))
    # pinos
    for ref, xpin, tab, lado in (("P1", 120.5051, P1, 1), ("P2", 176.5121, P2, -1)):
        for n, net in tab.items():
            y = 80.8788 + 2.54 * (n - 1)
            X, Y = px(xpin, y)
            s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#d33"/>' % (X, Y, 0.75 * S))
            tx = X + 16 if lado == -1 else X - 16
            anc = "start" if lado == -1 else "end"
            if lado == -1:
                tx = c_ = px(X0 + 60, 0)[0] + 10
            else:
                tx = px(X0, 0)[0] - 8
            s.append('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="11">%s.%d %s</text>' % (tx, Y + 4, anc, ref, n, net))
    for nome, (x, y) in (("H1", (126.501, 131.004)), ("H2", (170.501, 79.004))):
        X, Y = px(x, y)
        s.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#e8c95a" stroke="black"/><circle cx="%.1f" cy="%.1f" r="%.1f" fill="white"/>' % (X, Y, 3 * S, X, Y, 1.6 * S))
        s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-weight="bold">%s</text>' % (X, Y + 4, nome))
    for nome, x in (("D5", 140.1647), ("D1", 152.6361), ("D24", 164.4217)):
        X, Y = px(x, 120.8076)
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#f3b233" stroke="black"/>' % (X - 0.8 * S, Y - 1.1 * S, 1.6 * S, 2.2 * S))
        s.append('<text x="%.1f" y="%.1f" font-weight="bold" font-size="11">%s</text>' % (X + 14, Y + 4, nome))
    y = 2 * M + 60 * S + 50
    s.append('<text x="%d" y="%d" fill="#555">Fixos (bloqueados): P1, P2, H1, H2, D1, D5, D24 · Retorno dos laços (V1 &lt; 5 mΩ): burden → GND_ADC → R2 → GND_24V → P1.19, sem passar pelo AGND do U7.</text>' % (ML, y))
    s.append("</svg>")
    return "\n".join(s)


open(OUT + ".svg", "w", encoding="utf-8").write(svg())
d = fitz.open(OUT + ".svg"); d[0].get_pixmap(dpi=96).save(OUT + ".png")
print("escrito", OUT + ".svg/.png")
