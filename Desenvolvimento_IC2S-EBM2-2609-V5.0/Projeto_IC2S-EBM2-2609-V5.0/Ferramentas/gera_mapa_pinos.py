# -*- coding: utf-8 -*-
"""F2 etapa 2.4 - mapa de pinos da EBM2 V5 (skill 2shw-pcb:esquematico).

A rede de cada pino LE-SE DA NETLIST exportada pelo kicad-cli; a funcao, a direccao, o nivel activo e o
timing vem dos datasheets (pagina citada). A rede esperada vem da intencao (sec. 4 e 8): se a netlist
discordar, o script recusa escrever - o mapa e tambem uma verificacao cruzada da 2.3.
Uso: python gera_mapa_pinos.py netlist.net saida.md
"""
import io, re, sys
from netlist_diff import ler

NET, OUT = sys.argv[1], sys.argv[2]
c, redes, pino = ler(NET)
t = io.open(NET, encoding="utf-8").read()
ptype = {}
for m in re.finditer(r'\(node\s+\(ref "([^"]+)"\)\s+\(pin "([^"]+)"\)(?:\s+\(pinfunction "([^"]*)"\))?(?:\s+\(pintype "([^"]*)"\))?', t):
    ptype["%s.%s" % (m.group(1), m.group(2))] = (m.group(3) or "", m.group(4) or "")


def curta(r):
    return r.split("/")[-1] if r else "—"


# ref -> pino -> (rede esperada, funcao, direccao, nivel activo, timing/observacoes)
# direccao vista da PLACA (entrada = entra no pino).  NC = sem ligacao.
MCP = "DS21298E"
ISO = "SLLSE83F"
MAPA = {
 "U7": ("MCP3208T-BI/SL — conversor 12 bits, SPI", {
   1: ("AIN1_ADC", "CH0 — laço 1 (`P2.2`/`P2.3`)", "entrada analógica", "—", "0 a VREF = 2,5 V; 4 mA = 721, 20 mA = 3604, 22,7 mA = 4095 (110 Ω). Série `R28` 4k7 (rev. 2.5)"),
   2: ("AIN2_ADC", "CH1 — laço 2", "entrada analógica", "—", "idem, `R29`"),
   3: ("AIN3_ADC", "CH2 — laço 3", "entrada analógica", "—", "idem, `R30`"),
   4: ("AIN4_ADC", "CH3 — laço 4", "entrada analógica", "—", "idem, `R31`"),
   5: ("NTC_ADC", "CH4 — termístor da placa", "entrada analógica", "—", "**Não lido pelo software actual** (Rodrigo 2026-09-24). Divisor de `+2V5_REF`, `C35` 100 nF no pino"),
   6: ("3V3_REF", "CH5 — preso ao trilho", "entrada analógica", "—", "Lê sempre 4095 (3,3 V > VREF). Mapa congelado (`RC4`); não lido"),
   7: ("AIN5_ADC", "CH6 — laço 5", "entrada analógica", "—", "idem, `R32`. **O mapa não é sequencial**: laço 5 = CH6"),
   8: ("AIN6_ADC", "CH7 — laço 6", "entrada analógica", "—", "idem, `R33`"),
   9: ("GND_ADC", "DGND", "massa", "—", "Massa de campo"),
   10: ("CS_ADC_ISO", "~CS/SHDN", "entrada digital", "**baixo**", "Descida → 1.º flanco de subida de CLK ≥ 100 ns (t_SUCS); alto entre conversões ≥ 500 ns (t_CSH). Com CS alto, DOUT em alta impedância (" + MCP + " pág. 3)"),
   11: ("MOSI_ADC_ISO", "DIN", "entrada digital", "—", "Bit de início (1.º «1» com CS baixo), SGL/DIFF, D2 D1 D0 (§5, pág. 19). Setup/hold ≥ 50 ns"),
   12: ("MISO_ADC_ISO", "DOUT", "saída digital", "—", "Válido ≤ 200 ns após a descida de CLK (t_DO); bit nulo e depois B11…B0, MSB primeiro (pág. 20)"),
   13: ("CLK_ADC_ISO", "CLK", "entrada digital", "—", "**≤ 1 MHz** (garantido a 2,7 V; 2 MHz só a 5 V, pág. 3). **≥ 10 kHz efectivos** (nota 3 pág. 3, §6.2). Real: 20 kHz. Modo SPI 0,0 ou 1,1 (§6.1, pág. 21). Amostra 1,5 ciclos a partir do 4.º flanco após o início (pág. 17)"),
   14: ("GND_ADC", "AGND", "massa", "—", "Percurso próprio no layout, junto ao `DGND`"),
   15: ("+2V5_REF", "VREF", "alimentação (referência)", "—", "ADR4525 2,5 V; `C14` 100 nF no pino, `C5` 2,2 µF na saída do ADR"),
   16: ("VDD_ADC", "VDD", "alimentação", "—", "3,3 V de `3V3_REF` pela ferrite `FB2`; `C15` 1 µF + `C16` 100 nF"),
 }),
 "U6": ("ISO7141CCDBQR — isolador digital 4 canais (3 → campo, 1 → barramento)", {
   1: ("+3.3V_DIG", "VCC1", "alimentação", "—", "Lado do barramento, 3,3 V do `U5` MCP1824S (fecha o gap G2: MISO a 3,3 V para a Pi)"),
   2: ("DGND", "GND1", "massa", "—", "Massa do barramento"),
   3: ("MOSI", "INA → OUTA (pino 14)", "entrada digital", "—", "Entradas TTL, toleram 5 V a VCC 3,3 V (" + ISO + " pág. 1). Atraso 15-45 ns a 3,3 V (§6.10, pág. 8)"),
   4: ("CLK", "INB → OUTB (pino 13)", "entrada digital", "—", "idem"),
   5: ("CS_ADC", "INC → OUTC (pino 12)", "entrada digital", "**baixo** (atravessa sem inversão)", "Entrada aberta ou lado 1 sem alimentação → OUTC **alto** (versão CC, tabela 3, pág. 19): o ADC fica desseleccionado"),
   6: ("MISO", "OUTD ← IND (pino 11)", "saída digital", "—", "**Sempre activa** (EN1 fixo em VCC1, como na V4.1 e na EBM7 Legacy). Com o ADC desseleccionado, IND fica em alta impedância e OUTD vai a **alto** (tabela 3). Se o MISO da base board for partilhado com outro escravo SPI, há contenção: confirmar na cablagem (`V14`)"),
   7: ("+3.3V_DIG", "EN1", "entrada (fixa)", "alto = activo", "Fixo: OUTD nunca vai a alta impedância"),
   8: ("DGND", "GND1", "massa", "—", ""),
   9: ("GND_ADC", "GND2", "massa", "—", "Massa de campo"),
   10: ("VCC2_ISO", "EN2", "entrada (fixa)", "alto = activo", "Fixo em VCC2: OUTA/B/C sempre activas"),
   11: ("MISO_ADC_ISO", "IND", "entrada digital", "—", "De DOUT do `U7`"),
   12: ("CS_ADC_ISO", "OUTC", "saída digital", "baixo = ADC seleccionado", "Para ~CS do `U7`"),
   13: ("CLK_ADC_ISO", "OUTB", "saída digital", "—", "Para CLK do `U7`"),
   14: ("MOSI_ADC_ISO", "OUTA", "saída digital", "—", "Para DIN do `U7`"),
   15: ("GND_ADC", "GND2", "massa", "—", ""),
   16: ("VCC2_ISO", "VCC2", "alimentação", "—", "3,3 V de `3V3_REF` pela ferrite `FB1`, `C13` 100 nF"),
 }),
 "P1": ("Harwin M20-7822046 — barramento para a base board (pinagem congelada, `RC2`)", {
   1: (None, "USB1 do barramento", "NC", "—", "Não usado"),
   2: (None, "USB2 do barramento", "NC", "—", "Não usado"),
   3: ("DGND", "GND do barramento (GNDI na base board V2.3)", "massa", "—", "O SPI na MainBoard vai referido a GNDI_3V3: união fora da placa (`V14`)"),
   4: ("MOSI", "MOSI", "entrada digital", "—", "Da Raspberry Pi (mestre), 3,3 V"),
   5: ("CLK", "SCLK", "entrada digital", "—", "20 kHz no software actual"),
   6: ("MISO", "MISO", "saída digital", "—", "3,3 V; sempre accionada pelo isolador (ver `U6.6`)"),
   7: (None, "CS_DAC", "NC", "—", "Não há DAC nesta placa"),
   8: (None, "LDAC_DAC", "NC", "—", ""),
   9: ("CS_ADC", "CS_ADC", "entrada digital", "**baixo**", "Na base board V2.3 o P19.9 não tem cobre: chega por fio no painel (achado da EBM7)"),
   10: (None, "CS4", "NC", "—", ""),
   11: (None, "ID1", "NC — **tem de continuar assim**", "—", "Provável identidade da placa perante a base board [EST]: copiado da V4.1"),
   12: ("DGND", "GND", "massa", "—", ""),
   13: (None, "ID3", "NC — **tem de continuar assim**", "—", "idem"),
   14: (None, "SDA", "NC", "—", ""),
   15: (None, "SCL", "NC", "—", ""),
   16: ("DGND", "GND", "massa", "—", ""),
   17: ("+5V", "+5V do barramento (+5V_IC)", "alimentação", "—", "Para o `U5`. Na base board: borne P21 com TVS D53 (grampo 9,2 V) contra 6,5 V abs. max do MCP1824: **`V13` aberta**"),
   18: (None, "—", "NC", "—", "Não existe na V4.1"),
   19: ("GND_24V", "0 V do painel", "massa", "—", "Unido a `GND_ADC` só por `R2` (net-tie). Sem cobre na base board: por fio"),
   20: ("+24V", "18-32 V do painel", "alimentação", "—", "Rede, bateria ou solar (`RA1`). D2 SMA6J33A-Q na entrada. Por fio"),
 }),
 "P2": ("Harwin M20-7821446 — campo, 6 laços 4-20 mA (pinagem congelada, `RC2`)", {
   1: (None, "—", "NC", "—", "Como na V4.1"),
   14: ("GND_ADC", "0 V de campo", "massa", "—", "Para transmissores de 4 fios / blindagem"),
 }),
}
for k in range(1, 7):
    MAPA["P2"][1][2 * k] = ("LOOP%d_V+" % k, "Alimentação do laço %d" % k, "saída (alimentação)", "—",
                            "`+24V_ADC` → `F%d` 50 mA → pino; TVS `D%d` 36 V no pino" % (2 + k, 11 + k))
    MAPA["P2"][1][2 * k + 1] = ("AIN%d-" % k, "Retorno do laço %d" % k, "entrada (corrente)", "—",
                                "→ `U%d` TPS26613 (IN) → burden 110 Ω. TVS `D%d` 33 V. Em curto: 25-40 mA 100 ms, corta 800 ms (leitura alterna 4095 / ~0)" % (7 + k, 5 + k))

falhas, linhas = [], []
for ref, (titulo, pinos) in MAPA.items():
    todos = sorted((int(p.split(".")[1]) for p in pino if p.split(".")[0] == ref))
    if sorted(pinos) != todos:
        falhas.append("%s: pinos no mapa %s, na netlist %s" % (ref, sorted(pinos), todos))
    linhas += ["", "## `%s` — %s" % (ref, titulo), "",
               "| Pino | Rede (netlist) | Função | Direcção | Nível activo | Timing / observações |",
               "|---|---|---|---|---|---|"]
    for n in todos:
        esp, fun, dire, niv, obs = pinos.get(n, (None, "?", "?", "?", "?"))
        real = pino.get("%s.%d" % (ref, n))
        nc = real is None or real.startswith("unconnected-")
        if esp is None:
            if not nc:
                falhas.append("%s.%d devia estar sem ligação e está em %s" % (ref, n, real))
        elif curta(real) != esp:
            falhas.append("%s.%d: intenção %s, netlist %s" % (ref, n, esp, real))
        linhas.append("| %d | %s | %s | %s | %s | %s |" % (n, "sem ligação" if nc else "`%s`" % curta(real), fun, dire, niv, obs))
if falhas:
    print("*** MAPA RECUSADO: %d divergências com a netlist ***" % len(falhas))
    for f in falhas:
        print("   ", f)
    sys.exit(1)

cab = """# Mapa de pinos — EBM2 V5 (F2, etapa 2.4)

| | |
|---|---|
| Esquemático | intenção **rev. 2.5c**, netlist `%s` |
| Gerado por | `ferramentas/gera_mapa_pinos.py` — a rede de cada pino **lê-se da netlist**; se discordar da intenção (§4, §8) o script recusa escrever |
| Datasheets | MCP3208 `%s` (Microchip 2008); ISO7141CC `%s` rev. F (TI 2015); pastas `Documentos/verificacao_2_3b_rev25/datasheets/` |
| Cruzamento com a 2.3 | Os pinos coincidem com `verificacao_2_3/verificacao_pinagem_EBM2_V5.md` (revisão humana, 16 grupos, sem divergências) |

Âmbito: os componentes de alta pinagem e as interfaces — conversor, isolador e os dois conectores. É também a
base do handoff de firmware (secção final).
""" % (NET.replace("\\", "/").split("/")[-1], MCP, ISO)

fw = """
## Para o firmware (DeviceManager, `extensions/EBM2.js`)

| Tema | Regra | Fonte |
|---|---|---|
| Mapa de canais | Laço 1-4 = CH0-CH3; **laço 5 = CH6, laço 6 = CH7**; CH4 = NTC; CH5 = 4095 fixo | `U7` pinos 1-8; `RC4` |
| Escala | 12 bits sobre VREF 2,5 V e burden 110 Ω: **1 LSB = 5,55 µA**; 4 mA = 721; 20 mA = 3604; satura a 22,7 mA | intenção §8-§9 |
| Relógio SPI | **10 kHz ≤ f ≤ 1 MHz** (real: 20 kHz). Pela barreira: 45 ns por sentido (`U6`), 90 ns ida e volta mais t_DO 200 ns; folgado até 1 MHz | DS21298E pág. 3; SLLSE83F pág. 8 |
| Trama | 24 bits **atómicos** por canal (bit de início, SGL/DIFF, D2 D1 D0, bit nulo, B11…B0); CS alto ≥ 500 ns entre tramas | DS21298E págs. 19-20 |
| Curto do transmissor | A leitura **alterna** ~100 ms a 4095 e ~800 ms a ~0 mA (`"null"`). Com a média de 10 amostras / 500 ms vê-se sobretudo `"null"`: **`"null"` intermitente com picos a 4095 = curto, não laço aberto** | TPS26613 SLVSFE3C tabela 8-3 |
| Alarme NAMUR | ≥ 21 mA lê-se (código ≥ 3784) antes da saturação | NE43 |
| Troca de placa | **Recalibrar os seis canais ao instalar** (a V4.1 lia com outra escala: −9,3 %) | escopo `RC4` |
| MISO | Sempre accionado pelo isolador, nunca em alta impedância: não partilhar a linha com outro escravo SPI sem confirmar a cablagem | `U6.6`; `V14` |
"""
io.open(OUT, "w", encoding="utf-8").write(cab + "\n".join(linhas) + "\n" + fw)
print("mapa escrito:", OUT, "|", sum(len(p) for _, p in MAPA.values()), "pinos, 0 divergências com a netlist")
