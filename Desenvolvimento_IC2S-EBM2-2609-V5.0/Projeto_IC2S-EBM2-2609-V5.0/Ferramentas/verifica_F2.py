# -*- coding: utf-8 -*-
"""Porta (a) para as folhas novas: a netlist exportada contra a intencao rev. 2.

As expectativas escrevem-se aqui a partir das TABELAS do documento de intencao
aprovado (sec. 4, 7, 8, 9, 10), nao a partir do gerador. Se o gerador errou, esta
verificacao tem de o apanhar; se lesse do gerador, confirmaria o erro.

Uso: python verifica_F2.py netlist.net
"""
import sys
from netlist_diff import ler

c, redes, pino = ler(sys.argv[1])
falhas = []

def rede_de(p):
    return pino.get(p)

# ---------------------------------------------------------------- A. redes exactas
EXACTAS = {
    "MOSI (P1.4 -> U6 INA)": {"P1.4", "U6.3"},
    "CLK (P1.5 -> U6 INB)": {"P1.5", "U6.4"},
    "CS_ADC (P1.9 -> U6 INC)": {"P1.9", "U6.5"},
    "MISO (U6 OUTD -> P1.6)": {"P1.6", "U6.6"},
    "MOSI_ADC_ISO (OUTA -> DIN)": {"U6.14", "U7.11"},
    "CLK_ADC_ISO (OUTB -> CLK)": {"U6.13", "U7.13"},
    "CS_ADC_ISO (OUTC -> CS)": {"U6.12", "U7.10"},
    "MISO_ADC_ISO (DOUT -> IND)": {"U6.11", "U7.12"},
    "VCC2_ISO": {"FB1.1", "C13.1", "U6.16", "U6.10"},
    "VDD_ADC": {"FB2.1", "C15.1", "C16.1", "U7.16"},
    "+3.3V_DIG": {"U5.3", "C11.1", "C12.1", "U6.1", "U6.7"},
    "+5V do barramento": {"P1.17", "U5.1", "C10.1"},
    "DGND": {"P1.3", "P1.12", "P1.16", "U5.2", "U5.4", "C10.2", "C12.2", "C11.2", "U6.2", "U6.8", "TP8.1"},
    "NTC_ADC": {"TH1.2", "R40.1", "C35.1", "U7.5"},
    "LED do trilho dos lacos": {"R34.2", "D24.2"},
}
CANAL_ADC = {1: "1", 2: "2", 3: "3", 4: "4", 5: "7", 6: "8"}          # CH0-3, CH6, CH7 (sec. 8)
P2_ALIM = {k: str(2 * k) for k in range(1, 7)}                         # P2.2, 4, ... 12 (sec. 4)
P2_RET = {k: str(2 * k + 1) for k in range(1, 7)}                      # P2.3, 5, ... 13
for k in range(1, 7):
    # rev. 2.3: o TVS D(11+k) passa para o lado do terminal, depois do fusivel
    EXACTAS["canal %d: alimentacao do laco" % k] = {"F%d.2" % (2 + k), "P2.%s" % P2_ALIM[k], "D%d.1" % (11 + k)}
    # rev. 2.4: o retorno termina no IN (4) do TPS26613 U(7+k); o OUT (5) e o R(9+k) (0 ohm) formam AINk_LIM.
    # O Schottky D64k saiu.
    EXACTAS["canal %d: retorno" % k] = {"P2.%s" % P2_RET[k], "D%d.1" % (5 + k), "U%d.4" % (7 + k)}
    EXACTAS["canal %d: saida do protector" % k] = {"U%d.5" % (7 + k), "R%d.1" % (9 + k)}
    EXACTAS["canal %d: no de medida" % k] = {"R%d.2" % (9 + k), "R%d.1" % (15 + k), "R%d.1" % (21 + k)}
    # rev. 2.5: o no do filtro (C, clamp) e o pino do ADC ficam separados pela serie R(27+k) 4k7
    EXACTAS["canal %d: no do filtro" % k] = {"R%d.2" % (21 + k), "C%d.1" % (22 + k), "D%d.3" % (17 + k), "R%d.1" % (27 + k)}
    EXACTAS["canal %d: entrada do ADC" % k] = {"R%d.2" % (27 + k), "U7.%s" % CANAL_ADC[k]}
# rev. 2.4: trilho do +Vs dos protectores e o divisor do VSNS (intencao sec. 9, Legacy U12)
EXACTAS["VSNS"] = {"R37.2", "R38.1", "R39.1", "C34.1"} | {"U%d.7" % (7 + k) for k in range(1, 7)}
EXACTAS["FB do U14"] = {"U14.2", "R35.2", "R36.1", "C33.2"}                  # rev. 2.5: C_BYP
EXACTAS["FB do U1"] = {"U1.2", "R5.2", "R6.1", "C7.2"}                  # rev. 2.5: C_BYP
EXACTAS["+12V_TPS"] = ({"U14.1", "R35.1", "C31.1", "C32.1", "C33.1", "TP10.1", "R37.1"}
                       | {"U%d.6" % (7 + k) for k in range(1, 7)} | {"C%d.1" % (16 + k) for k in range(1, 7)})
for nome, esp in EXACTAS.items():
    rs = {rede_de(p) for p in esp}
    if len(rs) != 1 or None in rs:
        falhas.append("A %s: os pinos estao em redes diferentes %s" % (nome, rs)); continue
    r = rs.pop()
    if redes[r] != esp:
        falhas.append("A %s: rede %s tem %s, esperado exactamente %s" % (nome, r, sorted(redes[r]), sorted(esp)))

# ---------------------------------------------------------------- B. trilhos globais
GLOBAIS = {
    "+24V": {"P1.20"},
    "GND_24V": {"P1.19"},
    "+24V_ADC": {"F%d.1" % (2 + k) for k in range(1, 7)} | {"R34.1", "U14.8", "U14.5", "C30.1", "C29.1"},
    "3V3_REF": {"U7.6", "FB1.2", "FB2.2"} | {"D%d.2" % (17 + k) for k in range(1, 7)},
    "+2V5_REF": {"U7.15", "C14.1", "TH1.1"},
    "GND_ADC": {"P2.14", "U6.9", "U6.15", "U7.9", "U7.14", "C13.2", "C14.2", "C15.2", "C16.2",
                "R40.2", "C35.2", "D24.1", "TP9.1"}
               | {"D%d.2" % (5 + k) for k in range(1, 7)} | {"D%d.2" % (11 + k) for k in range(1, 7)}
               | {"R%d.2" % (15 + k) for k in range(1, 7)} | {"C%d.2" % (22 + k) for k in range(1, 7)}
               | {"D%d.1" % (17 + k) for k in range(1, 7)}
               # rev. 2.4: GND, MODE e -Vs de cada TPS26613; U14 com o PAD; condensadores e divisores
               | {"U%d.%d" % (7 + k, n) for k in range(1, 7) for n in (1, 2, 3)} | {"C%d.2" % (16 + k) for k in range(1, 7)}
               | {"U14.4", "U14.9", "C30.2", "C29.2", "C31.2", "R36.2", "R38.2", "R39.2", "C34.2"}
               | {"C32.2", "U4.2", "C8.2"},                                  # rev. 2.5
}
for nome, esp in GLOBAIS.items():
    if nome not in redes:
        falhas.append("B trilho %s nao existe" % nome); continue
    falta = esp - redes[nome]
    if falta:
        falhas.append("B %s: faltam %s" % (nome, sorted(falta)))

# ---------------------------------------------------------------- C. barreira
BARRAMENTO = set().union(EXACTAS["MOSI (P1.4 -> U6 INA)"], EXACTAS["CLK (P1.5 -> U6 INB)"],
                         EXACTAS["CS_ADC (P1.9 -> U6 INC)"], EXACTAS["MISO (U6 OUTD -> P1.6)"],
                         EXACTAS["+3.3V_DIG"], EXACTAS["+5V do barramento"], EXACTAS["DGND"])
redes_bar = {rede_de(p) for p in BARRAMENTO} - {None}
for r in redes_bar:
    intrusos = {p for p in redes[r] if p not in BARRAMENTO}
    if intrusos:
        falhas.append("C BARREIRA ATRAVESSADA: a rede %s do barramento tem pinos de campo %s" % (r, sorted(intrusos)))
for lado1 in ("U6.%d" % n for n in range(1, 9)):
    if rede_de(lado1) not in redes_bar:
        falhas.append("C pino do lado 1 %s fora das redes do barramento" % lado1)
for lado2 in ("U6.%d" % n for n in range(9, 17)):
    if rede_de(lado2) in redes_bar:
        falhas.append("C pino do lado 2 %s numa rede do barramento" % lado2)

# ---------------------------------------------------------------- D. nomes e pinos sem rede
gerados = [n for n in redes if n.startswith("Net-")]
if gerados:
    falhas.append("D nomes de rede gerados: %s" % gerados)
NC_ESPERADOS = {"P1.%d" % n for n in (1, 2, 7, 8, 10, 11, 13, 14, 15, 18)} | {"P2.1"}
nc_reais = {p for n, ps in redes.items() if n.startswith("unconnected-") for p in ps}
nc_novos = {p for p in nc_reais if p.split(".")[0] in ("P1", "P2")}
if nc_novos != NC_ESPERADOS:
    falhas.append("D no-connect de P1/P2: esperado %s, real %s" % (sorted(NC_ESPERADOS), sorted(nc_novos)))

# rev. 2.4: SGOOD sem uso (decisao escrita) e os NC do U14; nada da V8 antiga pode sobrar
nc_tps = {p for p in nc_reais if p.split(".")[0] in {"U%d" % (7 + k) for k in range(1, 7)} | {"U14"}}
NC_TPS = {"U%d.8" % (7 + k) for k in range(1, 7)} | {"U14.3", "U14.6", "U14.7"}
if nc_tps != NC_TPS:
    falhas.append("D no-connect dos TPS: esperado %s, real %s" % (sorted(NC_TPS), sorted(nc_tps)))
sobra = sorted(r for r in c if r.startswith("D64"))
if sobra:
    falhas.append("D o Schottky da rev. 2.1 continua: %s" % sobra)
for k in range(1, 7):
    for ref, esperado in (("U%d" % (7 + k), "TPS26613DDFR"), ("D%d" % (5 + k), "SMBJ33A"), ("R%d" % (9 + k), "0R")):
        if ref in c and c[ref]["value"] != esperado:
            falhas.append("D valor de %s: %s, esperado %s" % (ref, c[ref]["value"], esperado))

# rev. 2.5 (intencao sec. 17): U4 MCP1824 com PWRGD sem uso e SHDN pelo R7; C208 saiu; valores novos
r = rede_de("U4.3")
if r is None or len(redes[r]) != 2 or not any(p.startswith("R7.") for p in redes[r]):
    falhas.append("D SHDN do U4: esperado so U4.3 + R7, real %s" % (sorted(redes.get(r, ())),))
if not any(n.startswith("unconnected-") and "U4.4" in ps for n, ps in redes.items()):
    falhas.append("D U4.4 (PWRGD) devia estar sem ligacao")
if "C208" in c:
    falhas.append("D C208 (BP do SPX3819) continua na netlist")
if rede_de("U4.5") != "3V3_REF" or "C8.1" not in redes.get("3V3_REF", ()):
    falhas.append("D U4.5/C8.1 fora de 3V3_REF")
VALORES_25 = ((("R3", "150R"), ("R8", "4k12"), ("C8", "10uF/50V"), ("C5", "2u2"), ("C11", "2u2"),
               ("U4", "MCP1824T-3302E/OT"), ("C32", "10uF/50V"), ("C33", "10nF"), ("C7", "10nF"))
              + tuple(("R%d" % (27 + k), "4k7") for k in range(1, 7)))
for ref, esperado in VALORES_25:
    if ref not in c:
        falhas.append("D falta %s" % ref)
    elif c[ref]["value"] != esperado:
        falhas.append("D valor de %s: %s, esperado %s" % (ref, c[ref]["value"], esperado))

print("componentes: %d | redes: %d" % (len(c), len(redes)))
print("A redes exactas conferidas: %d | B trilhos: %d | C barreira: %d redes do barramento"
      % (len(EXACTAS), len(GLOBAIS), len(redes_bar)))
if falhas:
    print("\n*** %d FALHAS ***" % len(falhas))
    for x in falhas: print("   ", x)
    sys.exit(1)
print("TUDO CONFERE com a intencao rev. 2.5: redes exactas, trilhos, barreira, nomes e no-connects.")
