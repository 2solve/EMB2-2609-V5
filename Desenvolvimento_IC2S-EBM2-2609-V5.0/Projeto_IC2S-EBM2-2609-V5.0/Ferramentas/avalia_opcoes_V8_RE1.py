# -*- coding: utf-8 -*-
"""Avalia as opcoes para V8 (transmissor em curto) e RE1 (exactidao) lado a lado.

Cada numero tem procedencia; o que e estimativa esta marcado como tal.

Fontes:
  MCP3208 DS21298E pag. 2: offset +-3 LSB, ganho +-5 LSB, INL -B +-1 / -C +-2 LSB, todos a VREF 5 V;
    VREF de 0,25 V a VDD. Fig. 2-18/2-2: offset e INL sao tensoes fixas; fig. 2-15: ganho e fraccao.
  ADR4525/ADR4540 grau B: erro inicial +-0,02 % (planejamento 2.1; ADR4540 da mesma familia, a confirmar).
  ERA3AEB/ERA6AEB/ERA8AEB (Panasonic AOA0000C307 pag. 2): +-0,1 %, 25 ppm, 47 ohm a 330 kohm.
  Fusivel de canal Schurter 3413.0002.22: 9,2 ohm a frio (planejamento).
  AL5809-30P1-7 / -25P1-7 (Diodes DS36625 rev. 5): 28,5-31,5 / 23,75-26,25 mA de -40 a +125 C; 2,5-60 V; abs max 80 V e -0,3 V;
    PowerDI123 thetaJA 81,4 C/W (nota 5, cobre alargado); Tj recomendada <= 125 C.
  NSI45030AZ (onsemi rev. 3): 27-33 mA a 25 C e Vak 7,5 V; Voverhead 1,8 V; 45 V; -0,5 V;
    SOT-223 thetaJA 96-131 C/W conforme o cobre; Tj max 150 C; coeficiente negativo (nao tabelado).
  RA1: 18 a 32 V (corrigido em 2026-09-23; antes 20-28 V). V4.1: burden CRCW0603160RFKEA (1 %), referencia = saida do LDO (+-1 %, defeito D7).
ESTIMATIVAS (marcadas "est."): queda do D202 0,6 V; queda do limitador a 20 mA tomada pelo limite
  conservador (AL5809 2,5 V = minimo de regulacao; NSI 1,8 V = Voverhead) ate se ler a curva.
"""
import math

LSB5 = 5.0 / 4096            # LSB a VREF = 5 V, onde o datasheet especifica
OFFSET_V = 3 * LSB5           # tensao fixa
INL_V = {"B": 1 * LSB5, "C": 2 * LSB5}
GANHO = 5 / 4096 * 100        # %, fraccao

def re1(vref_err, burden_tol, fs_v, grau):
    termos = {"referencia": vref_err, "burden": burden_tol, "ganho ADC": GANHO,
              "offset ADC": OFFSET_V / fs_v * 100, "INL ADC": INL_V[grau] / fs_v * 100}
    return math.sqrt(sum(v * v for v in termos.values())), termos

V_D202, R_FUS = 0.6, 9.2      # est. / datasheet
LIM = {
    None: dict(nome="sem limitador", queda=0.0, imax=None),
    "AL5809": dict(nome="AL5809-30P1-7", queda=2.5, imax=31.5e-3, theta=81.4, tj_rec=125, tj_abs=175),
    "AL5809-25": dict(nome="AL5809-25P1-7", queda=2.5, imax=26.25e-3, theta=81.4, tj_rec=125, tj_abs=175),
    "NSI": dict(nome="NSI45030AZ", queda=1.8, imax=33e-3, theta=109.0, tj_rec=150, tj_abs=150),
}

CONFIGS = [
    # nome, vref, err_ref, burden, tol_burden, grau, serie, limitador
    ("V4.1 (base de comparacao)", 3.3, 1.0, 160, 1.0, "C", 249, None),
    ("V5 actual", 2.5, 0.02, 110, 0.1, "B", 249, None),
    ("A: limitador + serie 150 ohm 1206", 2.5, 0.02, 110, 0.1, "B", 150, "AL5809"),
    ("A25: limitador AL5809-25 + serie 150 ohm 1206", 2.5, 0.02, 110, 0.1, "B", 150, "AL5809-25"),
    ("B25: B com AL5809-25", 4.096, 0.02, 180, 0.1, "B", 100, "AL5809-25"),
    ("V5 rev. 2.2 (AL5809-25, serie 100 ohm)", 2.5, 0.02, 110, 0.1, "B", 100, "AL5809-25"),
    ("A': idem com NSI45030AZ", 2.5, 0.02, 110, 0.1, "B", 150, "NSI"),
    ("B: A + VDD 5 V, ADR4540 4,096 V, burden 180 ohm, serie 100 ohm", 4.096, 0.02, 180, 0.1, "B", 100, "AL5809"),
    ("B': B com serie 150 ohm", 4.096, 0.02, 180, 0.1, "B", 150, "AL5809"),
    ("(erro do planejamento) 4,096 V/180 ohm com INL do grau -C", 4.096, 0.02, 180, 0.1, "C", 100, "AL5809"),
]

print("%-62s %7s %8s %8s %9s %9s %9s %8s %8s" % ("configuracao", "RE1 %", "sat mA", "Vtx 18V", "Icc mA", "P_lim W", "P_serie W", "P_burd W", "Tj lim"))
for nome, vref, erf, rb, tol, grau, rs, lk in CONFIGS:
    fs20 = 0.020 * rb
    tot, termos = re1(erf, tol, fs20, grau)
    sat = vref / rb * 1000
    lim = LIM[lk]
    # tensao que sobra para o transmissor, alimentacao minima de 20 V, laco a 20 mA
    vtx = 18 - V_D202 - 0.020 * (R_FUS + rs + rb) - lim["queda"]
    # curto do transmissor, alimentacao maxima de 28 V
    vcc = 32 - V_D202
    if lim["imax"] is None:
        icc = vcc / (R_FUS + rs + rb); plim = 0.0; tj = "-"
    else:
        icc = lim["imax"]; plim = (vcc - icc * (R_FUS + rs + rb)) * icc
        tj = "%.0f C" % (70 + plim * lim["theta"])   # RB1: 0 a 70 C (2026-09-24)
    print("%-62s %7.3f %8.1f %8.2f %9.1f %9.2f %9.3f %8.3f %8s" % (
        nome[:62], tot, sat, vtx, icc * 1000, plim, icc ** 2 * rs, icc ** 2 * rb, tj))
print()
print("Vtx 18V = tensao disponivel para o transmissor com a alimentacao no minimo do RA1 (18 V) e 20 mA.")
print("Icc/P_* = transmissor em curto com 32 V (maximo do RA1). Tj lim = 70 C ambiente (RB1 corrigido) + P x thetaJA.")
print("Resistencias 0603 = 0,1 W; 0805 = 0,125 W; 1206 = 0,25 W (a 70 C, com reducao acima).")
for nome, vref, erf, rb, tol, grau, rs, lk in CONFIGS[1:2] + CONFIGS[4:5]:
    tot, termos = re1(erf, tol, 0.020 * rb, grau)
    print("\n%s: RSS %.3f %%" % (nome, tot))
    for k, v in termos.items():
        print("   %-12s %.3f %%" % (k, v))
    print("   resolucao: %.2f uA por LSB" % (vref / 4096 / rb * 1e6))
