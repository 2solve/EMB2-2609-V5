# Regulador de 3,3 V do lado PLC — U5: MCP1824ST-3302E/DB → MCP1824T-3302E/OT (2026-09-28)

Da reunião de 25-09: «esse chip é mais caro… existe regulador menores». O U5 alimenta só o lado 1 do ISO7141 (+5V do P1 → 3,3 V, massa DGND).

## Comparação que decidiu (datasheets locais; preços da API Mouser gravados nos repositórios)

| | MCP1824ST-3302E/DB (saiu) | SPX3819M5-L-3-3/TR | MCP1824T-3302E/OT |
|---|---|---|---|
| Encapsulamento | SOT-223-3 | SOT-23-5 | SOT-23-5 |
| Entrada (operação / máx. absoluto) | 2,1-6,0 V / 6,5 V | 2,5-16 V / 20 V | 2,1-6,0 V / 6,5 V |
| Precisão em temperatura | ±2,5 % | ±2 % | ±2,5 % |
| Estável com cerâmico | sim, «Stable with 1.0 µF Ceramic» (DS22070A p.1) | **não especificado** («bench testing», SPX3819 rev. 2.0.5 p.7); provado em campo na V2.2 | sim (mesmo datasheet) |
| ESD HBM | ≥ 4 kV | 1 kV | ≥ 4 kV |
| Mouser 1 un. | 0,64 USD (25-09) | 0,51 USD (16-09) | 0,56 USD (25-09) |
| Stock Mouser | 11 898 (25-09) | **99** (16-09) | 14 500 (25-09) |

Carga real: só o lado 1 do ISO7141, ≤ 8 mA a 40 Mbps (TI SLLSE83F p.10). O ISO7141 pede VCC1 de 2,7 a 5,5 V
(p.5) e 0,1 µF a ≤ 2 mm do pino (p.22 e p.25): cumprido com qualquer um dos três (C a 1,9 mm).

**Critério da equipa (28-09-2026): menos MPN, mais peças do mesmo tipo.** Na EBM7 o SPX3819 já é o U3/U4 do
+3.3V_ANA; na EBM2 o MCP1824T já é o U4 do 3V3_REF. O MCP1824ST sai das três placas.

## O que mudou

- **U5 = MCP1824T-3302E/OT**, SOT-23-5. Ligações: 1 IN e 3 SHDN a +5V (SHDN alto ≥ 45 % VIN, DS22070A p.9), 2 GND a DGND, 4 PG aberto (dreno aberto), 5 OUT a +3.3V_DIG.
- Condensadores mantidos (os que já estavam na entrada e na saída).
- PCB: pegada EBM2_V5:SOT-23-5 no mesmo sitio (placa ainda sem pistas). Nota 3 da folha 4 actualizada.

## Verificação

- ERC 0 erros; DRC 0 erros, paridade 0; netlist: só mudam os pinos do U5.

## Riscos em aberto

- Nenhum eléctrico novo: mesmo datasheet e comportamento do MCP1824ST; só muda o encapsulamento.
- Preços e stock são das consultas gravadas (16 e 25-09), não de hoje: a web da Mouser bloqueia leitura automática.

## Complemento: circuito típico do datasheet (MCP1824, DS22070A, «Typical Applications — Fixed Output», p.3)

| Elemento | Datasheet | Na placa |
|---|---|---|
| Entrada C1 | 4,7 µF na figura; «1 µF to 10 µF should be sufficient» (p.17) | **C10 era 1 µF/50 V = 0,80 µF efectivos a 5 V (pior caso) ❌ → agora 10 µF/50 V** |
| Saída C2 | 1 µF («Stable with 1.0 µF Ceramic», p.1) | C11 2,2 µF ✅ |
| SHDN | On/Off; alto ≥ 45 % de VIN (p.9) | directo a +5V ✅ |
| PWRGD + R1 100 kΩ | só se o sinal for usado | aberto (dreno aberto) ✅ |

**C10 = C3216X5R1H106K160AB** (10 µF/50 V 1206, o mesmo MPN de C4/C8/C31/C32; curva TDK: 7,0 µF a 5 V no pior caso). PCB: clone da pegada do C4, a 3,5 mm do U5 (o 1206 não cabia no sítio do 0603). ERC 0; DRC 0 erros, paridade 0.
