# Inventário de pinagem — EBM2 V5 (entrada da etapa 2.3)

Gerado por `ferramentas/prepara_pacote_2_3.py` a partir da netlist exportada agora (`EBM2_V5.net`),
das pegadas do projecto e dos datasheets desta pasta. **Não contém conclusões da sessão que desenhou.**

Colunas por pino: número no símbolo → nome do pino no símbolo → tipo → rede. A verificação é conferir
cada linha contra o datasheet (número, nome, função, direcção, nível) e a pegada contra o desenho do
encapsulamento (ilha 1, marca de polaridade).

## D200 — `SMA6J33A-Q` (SMA6J33A-Q)

- Símbolo: `Device:D_Zener` · Pegada: `EBM2_V5:DO-214` · Folha: `/2 Entrada/`
- Datasheet: `datasheets/SMA6J33A__Bourns_SMA6J33A-Q.pdf` (md5 f4ac07fa3bb0, 6 págs.)
- Ilhas da pegada: 1 @(2.042, 0) 1.77x1.8; 2 @(-2.042, 0) 1.77x1.8
- Nota da pegada: 2Solve PCB Library 'DO-214', recuperado da PCB V2.2 (fabricada) em 2026-09-04. Barra de catodo (F.SilkS) junto ao pad 1 acrescentada em 2026-09-04: na V2.3 o pino 1 e o CATODO (convencao KiCad = fabricante); a V2.2 nao tinha marca de polaridade.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| D200 | 1 | K_1 | passive | `+24V` |
| D200 | 2 | A_2 | passive | `GND_24V` |

## D201, D202 — `MBR1H100SFT3G` (MBR1H100SF)

- Símbolo: `Device:D_Schottky` · Pegada: `EBM2_V5:SOD123` · Folha: `/2 Entrada/`
- Datasheet: `datasheets/MBR1H100SF__fetch-1790203902626-3ncrcx.pdf` (md5 71e7d9a6cc96, 6 págs.)
- Ilhas da pegada: 1 @(1.45, 0) 1.2x1.4; 2 @(-1.45, 0) 1.2x1.4
- Nota da pegada: 2Solve PCB Library 'SOD123', recuperado da PCB V2.2 (fabricada) em 2026-09-04. Barra de catodo (F.SilkS) junto ao pad 1 acrescentada em 2026-09-04: na V2.3 o pino 1 e o CATODO (convencao KiCad = fabricante); a V2.2 nao tinha marca de polaridade.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| D201 | 1 | K_1 | passive | `/2 Entrada/+24V_DIO_REG` |
| D201 | 2 | A_2 | passive | `/2 Entrada/+24V_FUS_REG` |
| D202 | 1 | K_1 | passive | `+24V_ADC` |
| D202 | 2 | A_2 | passive | `/2 Entrada/+24V_FUS_ADC` |

## D203, D204, D630 — `KG EELP41.22-PHRH-35-A8J8-20-R18` (KG EELP41.22)

- Símbolo: `Device:LED` · Pegada: `EBM2_V5:0603LED` · Folha: `/2 Entrada/`
- Datasheet: `datasheets/KG_EELP41.22__KG-EELP41-22.pdf` (md5 6de13e051c1c, 22 págs.)
- Ilhas da pegada: 1 @(-0.7, 0) 0.7x0.8; 2 @(0.7, 0) 0.7x0.8
- Nota da pegada: 2Solve PCB Library '0603LED', recuperado da PCB V2.2 (fabricada) em 2026-09-04. Barra de catodo (F.SilkS) junto ao pad 1 acrescentada em 2026-09-04: na V2.3 o pino 1 e o CATODO (convencao KiCad = fabricante); a V2.2 nao tinha marca de polaridade.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| D203 | 1 | K_1 | passive | `GND_24V` |
| D203 | 2 | A_2 | passive | `/2 Entrada/LED_24V` |
| D204 | 1 | K_1 | passive | `GND_ADC` |
| D204 | 2 | A_2 | passive | `/3 Alimentacao/LED_5V_ADC` |
| D630 | 1 | K_1 | passive | `GND_ADC` |
| D630 | 2 | A_2 | passive | `/6 Lacos/LED_24V_ADC` |

## D601, D602, D603, D604, D605, D606, D611, D612, D613, D614, D615, D616 — `824520361` (824520361)

- Símbolo: `Device:D_Zener` · Pegada: `EBM2_V5:DO-214AA` · Folha: `/6 Lacos/`
- Datasheet: `datasheets/824520361__Wurth_824520361_SMBJ36A_DO-214AA.pdf` (md5 713e179e22a5, 9 págs.)
- Ilhas da pegada: 1 @(-2.15, 0) 2.5x2.3; 2 @(2.15, 0) 2.5x2.3
- Nota da pegada: courtyard 6,7 x 4,2 (EBM7: entre os TPS e os fusiveis so ha 7,2 mm); Diode SMB (DO-214AA)

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| D601 | 1 | K_1 | passive | `/1 Conectores/AIN1-` |
| D601 | 2 | A_2 | passive | `GND_ADC` |
| D602 | 1 | K_1 | passive | `/1 Conectores/AIN2-` |
| D602 | 2 | A_2 | passive | `GND_ADC` |
| D603 | 1 | K_1 | passive | `/1 Conectores/AIN3-` |
| D603 | 2 | A_2 | passive | `GND_ADC` |
| D604 | 1 | K_1 | passive | `/1 Conectores/AIN4-` |
| D604 | 2 | A_2 | passive | `GND_ADC` |
| D605 | 1 | K_1 | passive | `/1 Conectores/AIN5-` |
| D605 | 2 | A_2 | passive | `GND_ADC` |
| D606 | 1 | K_1 | passive | `/1 Conectores/AIN6-` |
| D606 | 2 | A_2 | passive | `GND_ADC` |
| D611 | 1 | K_1 | passive | `/1 Conectores/LOOP1_V+` |
| D611 | 2 | A_2 | passive | `GND_ADC` |
| D612 | 1 | K_1 | passive | `/1 Conectores/LOOP2_V+` |
| D612 | 2 | A_2 | passive | `GND_ADC` |
| D613 | 1 | K_1 | passive | `/1 Conectores/LOOP3_V+` |
| D613 | 2 | A_2 | passive | `GND_ADC` |
| D614 | 1 | K_1 | passive | `/1 Conectores/LOOP4_V+` |
| D614 | 2 | A_2 | passive | `GND_ADC` |
| D615 | 1 | K_1 | passive | `/1 Conectores/LOOP5_V+` |
| D615 | 2 | A_2 | passive | `GND_ADC` |
| D616 | 1 | K_1 | passive | `/1 Conectores/LOOP6_V+` |
| D616 | 2 | A_2 | passive | `GND_ADC` |

## D621, D622, D623, D624, D625, D626 — `BAV199LT1G` (BAV199)

- Símbolo: `EBM7_V23_proyecto3:BAV199` · Pegada: `EBM2_V5:SOT23-3` · Folha: `/6 Lacos/`
- Datasheet: `datasheets/BAV199__BAV199LT1-D.PDF` (md5 10d83f61d74f, 6 págs.)
- Ilhas da pegada: 1 @(-1.1, -0.95) 0.6x0.75; 2 @(-1.1, 0.95) 0.6x0.75; 3 @(1.1, 0) 0.6x0.75
- Nota da pegada: 2Solve PCB Library 'SOT23-3', recuperado da PCB V2.2 (fabricada) em 2026-09-04.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| D621 | 1 | A1_1 | passive | `GND_ADC` |
| D621 | 2 | K2_2 | passive | `3V3_REF` |
| D621 | 3 | COM_3 | passive | `/5 ADC/AIN1_ADC` |
| D622 | 1 | A1_1 | passive | `GND_ADC` |
| D622 | 2 | K2_2 | passive | `3V3_REF` |
| D622 | 3 | COM_3 | passive | `/5 ADC/AIN2_ADC` |
| D623 | 1 | A1_1 | passive | `GND_ADC` |
| D623 | 2 | K2_2 | passive | `3V3_REF` |
| D623 | 3 | COM_3 | passive | `/5 ADC/AIN3_ADC` |
| D624 | 1 | A1_1 | passive | `GND_ADC` |
| D624 | 2 | K2_2 | passive | `3V3_REF` |
| D624 | 3 | COM_3 | passive | `/5 ADC/AIN4_ADC` |
| D625 | 1 | A1_1 | passive | `GND_ADC` |
| D625 | 2 | K2_2 | passive | `3V3_REF` |
| D625 | 3 | COM_3 | passive | `/5 ADC/AIN5_ADC` |
| D626 | 1 | A1_1 | passive | `GND_ADC` |
| D626 | 2 | K2_2 | passive | `3V3_REF` |
| D626 | 3 | COM_3 | passive | `/5 ADC/AIN6_ADC` |

## D641, D642, D643, D644, D645, D646 — `BAT46W-7-F` (BAT46W)

- Símbolo: `Device:D_Schottky` · Pegada: `EBM2_V5:SOD123` · Folha: `/6 Lacos/`
- Datasheet: `datasheets/BAT46W__fetch-1790247975568-happxg.pdf` (md5 aacb3b04b04e, 5 págs.)
- Ilhas da pegada: 1 @(1.45, 0) 1.2x1.4; 2 @(-1.45, 0) 1.2x1.4
- Nota da pegada: 2Solve PCB Library 'SOD123', recuperado da PCB V2.2 (fabricada) em 2026-09-04. Barra de catodo (F.SilkS) junto ao pad 1 acrescentada em 2026-09-04: na V2.3 o pino 1 e o CATODO (convencao KiCad = fabricante); a V2.2 nao tinha marca de polaridade.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| D641 | 1 | K_1 | passive | `/1 Conectores/AIN1-` |
| D641 | 2 | A_2 | passive | `/6 Lacos/AIN1_LIM` |
| D642 | 1 | K_1 | passive | `/1 Conectores/AIN2-` |
| D642 | 2 | A_2 | passive | `/6 Lacos/AIN2_LIM` |
| D643 | 1 | K_1 | passive | `/1 Conectores/AIN3-` |
| D643 | 2 | A_2 | passive | `/6 Lacos/AIN3_LIM` |
| D644 | 1 | K_1 | passive | `/1 Conectores/AIN4-` |
| D644 | 2 | A_2 | passive | `/6 Lacos/AIN4_LIM` |
| D645 | 1 | K_1 | passive | `/1 Conectores/AIN5-` |
| D645 | 2 | A_2 | passive | `/6 Lacos/AIN5_LIM` |
| D646 | 1 | K_1 | passive | `/1 Conectores/AIN6-` |
| D646 | 2 | A_2 | passive | `/6 Lacos/AIN6_LIM` |

## P1 — `M20-7822046` (M20-7822046)

- Símbolo: `Connector_Generic:Conn_01x20` · Pegada: `EBM2_V5:HDR1X20_FEMALE` · Folha: `/1 Conectores/`
- Datasheet: `datasheets/Harwin_M20-782__Harwin_M20-782_plano.pdf` (md5 9423011844a3, 1 págs.)
- Ilhas da pegada: 1 @(0, 0) 1.5x1.5; 2 @(2.54, 0) 1.5x1.5; 3 @(5.08, 0) 1.5x1.5; 4 @(7.62, 0) 1.5x1.5; 5 @(10.16, 0) 1.5x1.5; 6 @(12.7, 0) 1.5x1.5; 7 @(15.24, 0) 1.5x1.5; 8 @(17.78, 0) 1.5x1.5; 9 @(20.32, 0) 1.5x1.5; 10 @(22.86, 0) 1.5x1.5; 11 @(25.4, 0) 1.5x1.5; 12 @(27.94, 0) 1.5x1.5; 13 @(30.48, 0) 1.5x1.5; 14 @(33.02, 0) 1.5x1.5; 15 @(35.56, 0) 1.5x1.5; 16 @(38.1, 0) 1.5x1.5; 17 @(40.64, 0) 1.5x1.5; 18 @(43.18, 0) 1.5x1.5; 19 @(45.72, 0) 1.5x1.5; 20 @(48.26, 0) 1.5x1.5
- Nota da pegada: 2Solve PCB Library 'HDR1X20 FEMALE', recuperado da PCB V2.2 (fabricada) em 2026-09-04.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| P1 | 1 | Pin_1_1 | passive+no_connect | `unconnected-(P1-Pin_1-Pad1)` |
| P1 | 2 | Pin_2_2 | passive+no_connect | `unconnected-(P1-Pin_2-Pad2)` |
| P1 | 3 | Pin_3_3 | passive | `DGND` |
| P1 | 4 | Pin_4_4 | passive | `/1 Conectores/MOSI` |
| P1 | 5 | Pin_5_5 | passive | `/1 Conectores/CLK` |
| P1 | 6 | Pin_6_6 | passive | `/1 Conectores/MISO` |
| P1 | 7 | Pin_7_7 | passive+no_connect | `unconnected-(P1-Pin_7-Pad7)` |
| P1 | 8 | Pin_8_8 | passive+no_connect | `unconnected-(P1-Pin_8-Pad8)` |
| P1 | 9 | Pin_9_9 | passive | `/1 Conectores/CS_ADC` |
| P1 | 10 | Pin_10_10 | passive+no_connect | `unconnected-(P1-Pin_10-Pad10)` |
| P1 | 11 | Pin_11_11 | passive+no_connect | `unconnected-(P1-Pin_11-Pad11)` |
| P1 | 12 | Pin_12_12 | passive | `DGND` |
| P1 | 13 | Pin_13_13 | passive+no_connect | `unconnected-(P1-Pin_13-Pad13)` |
| P1 | 14 | Pin_14_14 | passive+no_connect | `unconnected-(P1-Pin_14-Pad14)` |
| P1 | 15 | Pin_15_15 | passive+no_connect | `unconnected-(P1-Pin_15-Pad15)` |
| P1 | 16 | Pin_16_16 | passive | `DGND` |
| P1 | 17 | Pin_17_17 | passive | `+5V` |
| P1 | 18 | Pin_18_18 | passive+no_connect | `unconnected-(P1-Pin_18-Pad18)` |
| P1 | 19 | Pin_19_19 | passive | `GND_24V` |
| P1 | 20 | Pin_20_20 | passive | `+24V` |

## P2 — `M20-7821446` (M20-7821446)

- Símbolo: `Connector_Generic:Conn_01x14` · Pegada: `EBM2_V5:HDR1X14_FEMALE` · Folha: `/1 Conectores/`
- Datasheet: `datasheets/Harwin_M20-782__Harwin_M20-782_plano.pdf` (md5 9423011844a3, 1 págs.)
- Ilhas da pegada: 1 @(0, 0) 1.5x1.5; 2 @(2.54, 0) 1.5x1.5; 3 @(5.08, 0) 1.5x1.5; 4 @(7.62, 0) 1.5x1.5; 5 @(10.16, 0) 1.5x1.5; 6 @(12.7, 0) 1.5x1.5; 7 @(15.24, 0) 1.5x1.5; 8 @(17.78, 0) 1.5x1.5; 9 @(20.32, 0) 1.5x1.5; 10 @(22.86, 0) 1.5x1.5; 11 @(25.4, 0) 1.5x1.5; 12 @(27.94, 0) 1.5x1.5; 13 @(30.48, 0) 1.5x1.5; 14 @(33.02, 0) 1.5x1.5
- Nota da pegada: 2Solve PCB Library 'HDR1X14 FEMALE', recuperado da PCB V2.2 (fabricada) em 2026-09-04.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| P2 | 1 | Pin_1_1 | passive+no_connect | `unconnected-(P2-Pin_1-Pad1)` |
| P2 | 2 | Pin_2_2 | passive | `/1 Conectores/LOOP1_V+` |
| P2 | 3 | Pin_3_3 | passive | `/1 Conectores/AIN1-` |
| P2 | 4 | Pin_4_4 | passive | `/1 Conectores/LOOP2_V+` |
| P2 | 5 | Pin_5_5 | passive | `/1 Conectores/AIN2-` |
| P2 | 6 | Pin_6_6 | passive | `/1 Conectores/LOOP3_V+` |
| P2 | 7 | Pin_7_7 | passive | `/1 Conectores/AIN3-` |
| P2 | 8 | Pin_8_8 | passive | `/1 Conectores/LOOP4_V+` |
| P2 | 9 | Pin_9_9 | passive | `/1 Conectores/AIN4-` |
| P2 | 10 | Pin_10_10 | passive | `/1 Conectores/LOOP5_V+` |
| P2 | 11 | Pin_11_11 | passive | `/1 Conectores/AIN5-` |
| P2 | 12 | Pin_12_12 | passive | `/1 Conectores/LOOP6_V+` |
| P2 | 13 | Pin_13_13 | passive | `/1 Conectores/AIN6-` |
| P2 | 14 | Pin_14_14 | passive | `GND_ADC` |

## U200 — `TPS7A4001DGNR` (TPS7A4001DGN)

- Símbolo: `EBM7_V23_proyecto9:TPS7A4001DGN` · Pegada: `EBM2_V5:HVSSOP-8-1EP` · Folha: `/3 Alimentacao/`
- Datasheet: `datasheets/TPS7A4001__TI_TPS7A4001.pdf` (md5 8905213d1392, 24 págs.)
- Ilhas da pegada: 1 @(-2.15, -0.975) 1.45x0.5; 2 @(-2.15, -0.325) 1.45x0.5; 3 @(-2.15, 0.325) 1.45x0.5; 4 @(-2.15, 0.975) 1.45x0.5; 5 @(2.15, 0.975) 1.45x0.5; 6 @(2.15, 0.325) 1.45x0.5; 7 @(2.15, -0.325) 1.45x0.5; 8 @(2.15, -0.975) 1.45x0.5; 9 @(-0.485, -0.645) 0.6x0.6; 9 @(-0.485, 0.645) 0.6x0.6; 9 @(0, 0) 1.57x1.89; 9 @(0, 0) 1.57x1.89; 9 @(0.485, -0.645) 0.6x0.6; 9 @(0.485, 0.645) 0.6x0.6
- Nota da pegada: HVSSOP, 8 Pin (https://www.ti.com/lit/ds/symlink/tpa6110a2.pdf)

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| U200 | 1 | OUT_1 | power_out | `+5V_ADC` |
| U200 | 2 | FB_2 | input | `/3 Alimentacao/FB_5V` |
| U200 | 3 | NC_3 | no_connect | `unconnected-(U200-NC-Pad3)` |
| U200 | 4 | GND_4 | power_in | `GND_ADC` |
| U200 | 5 | EN_5 | input | `+24V_REG` |
| U200 | 6 | NC_6 | no_connect | `unconnected-(U200-NC-Pad6)` |
| U200 | 7 | NC_7 | no_connect | `unconnected-(U200-NC-Pad7)` |
| U200 | 8 | IN_8 | power_in | `+24V_REG` |
| U200 | 9 | PAD_9 | passive | `GND_ADC` |

## U201 — `SPX3819M5-L-3-3/TR` (SPX3819M5-L-3-3/TR)

- Símbolo: `Regulator_Linear:SPX3819M5-L-3-3` · Pegada: `EBM2_V5:SOT-23-5` · Folha: `/3 Alimentacao/`
- Datasheet: `datasheets/SPX3819__1016_SPX3819.pdf` (md5 52d5c537f3af, 13 págs.)
- Ilhas da pegada: 1 @(-1.3, -0.95) 1.1x0.6; 2 @(-1.3, 0) 1.1x0.6; 3 @(-1.3, 0.95) 1.1x0.6; 4 @(1.3, 0.95) 1.1x0.6; 5 @(1.3, -0.95) 1.1x0.6
- Nota da pegada: 2Solve PCB Library 'SOT-23-5', recuperado da PCB V2.2 (fabricada) em 2026-09-04.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| U201 | 1 | IN_1 | power_in | `+5V_ADC` |
| U201 | 2 | GND_2 | power_in | `GND_ADC` |
| U201 | 3 | EN_3 | input | `/3 Alimentacao/EN_3V3` |
| U201 | 4 | BP_4 | input | `/3 Alimentacao/BYP_3V3` |
| U201 | 5 | OUT_5 | power_out | `3V3_REF` |

## U202 — `ADR4525BRZ` (ADR4525BRZ)

- Símbolo: `EBM7_V23_proyecto10:ADR4525BRZ` · Pegada: `EBM2_V5:SOIC8` · Folha: `/3 Alimentacao/`
- Datasheet: `datasheets/ADR4525__adr4520_4525_4530_4533_4540_4550.pdf` (md5 51ffc461e5b2, 41 págs.)
- Ilhas da pegada: 1 @(-2.6, -1.905) 0.6x1.6; 2 @(-2.6, -0.635) 0.6x1.6; 3 @(-2.6, 0.635) 0.6x1.6; 4 @(-2.6, 1.905) 0.6x1.6; 5 @(2.6, 1.905) 0.6x1.6; 6 @(2.6, 0.635) 0.6x1.6; 7 @(2.6, -0.635) 0.6x1.6; 8 @(2.6, -1.905) 0.6x1.6
- Nota da pegada: 2Solve PCB Library 'SOIC8', recuperado da PCB V2.2 (fabricada) em 2026-09-04.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| U202 | 1 | NIC_1_1 | passive+no_connect | `unconnected-(U202-NIC_1-Pad1)` |
| U202 | 2 | VIN_2 | power_in | `3V3_REF` |
| U202 | 3 | NIC_3_3 | passive+no_connect | `unconnected-(U202-NIC_3-Pad3)` |
| U202 | 4 | GND_4 | power_in | `GND_ADC` |
| U202 | 5 | NIC_5_5 | passive+no_connect | `unconnected-(U202-NIC_5-Pad5)` |
| U202 | 6 | VOUT_6 | power_out | `+2V5_REF` |
| U202 | 7 | NIC_7_7 | passive+no_connect | `unconnected-(U202-NIC_7-Pad7)` |
| U202 | 8 | DNC_8 | no_connect | `unconnected-(U202-DNC-Pad8)` |

## U203 — `TL431BQDBZR` (TL431B)

- Símbolo: `Reference_Voltage:TL431DBZ` · Pegada: `EBM2_V5:SOT23-3` · Folha: `/3 Alimentacao/`
- Datasheet: `datasheets/TL431__TI_TL431.pdf` (md5 6418a55a9ed0, 85 págs.)
- Ilhas da pegada: 1 @(-1.1, -0.95) 0.6x0.75; 2 @(-1.1, 0.95) 0.6x0.75; 3 @(1.1, 0) 0.6x0.75
- Nota da pegada: 2Solve PCB Library 'SOT23-3', recuperado da PCB V2.2 (fabricada) em 2026-09-04.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| U203 | 1 | K_1 | passive | `3V3_REF` |
| U203 | 2 | REF_2 | passive | `/3 Alimentacao/FB_CLAMP` |
| U203 | 3 | A_3 | passive | `GND_ADC` |

## U400 — `ISO7141CCDBQR` (ISO7141CCDBQR)

- Símbolo: `EBM7_V23_proyecto4:ISO7141CC` · Pegada: `EBM2_V5:SSOP16-4.9x3.9mm` · Folha: `/4 Barreira digital/`
- Datasheet: `datasheets/ISO7141__TI_ISO7141CC.pdf` (md5 8528188a89b0, 36 págs.)
- Ilhas da pegada: 1 @(-2.75, -2.222) 0.45x1.8; 2 @(-2.75, -1.587) 0.45x1.8; 3 @(-2.75, -0.953) 0.45x1.8; 4 @(-2.75, -0.3175) 0.45x1.8; 5 @(-2.75, 0.318) 0.45x1.8; 6 @(-2.75, 0.953) 0.45x1.8; 7 @(-2.75, 1.588) 0.45x1.8; 8 @(-2.75, 2.222) 0.45x1.8; 9 @(2.75, 2.222) 0.45x1.8; 10 @(2.75, 1.588) 0.45x1.8; 11 @(2.75, 0.953) 0.45x1.8; 12 @(2.75, 0.318) 0.45x1.8; 13 @(2.75, -0.3175) 0.45x1.8; 14 @(2.75, -0.953) 0.45x1.8; 15 @(2.75, -1.587) 0.45x1.8; 16 @(2.75, -2.222) 0.45x1.8
- Nota da pegada: 2Solve PCB Library 'SSOP16 - 4.9x3.9mm', recuperado da PCB V2.2 (fabricada) em 2026-09-04.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| U400 | 1 | VCC1_1 | power_in | `+3.3V_DIG` |
| U400 | 2 | GND1_2 | power_in | `DGND` |
| U400 | 3 | INA_3 | input | `/1 Conectores/MOSI` |
| U400 | 4 | INB_4 | input | `/1 Conectores/CLK` |
| U400 | 5 | INC_5 | input | `/1 Conectores/CS_ADC` |
| U400 | 6 | OUTD_6 | output | `/1 Conectores/MISO` |
| U400 | 7 | EN1_7 | input | `+3.3V_DIG` |
| U400 | 8 | GND1_8 | power_in | `DGND` |
| U400 | 9 | GND2_9 | power_in | `GND_ADC` |
| U400 | 10 | EN2_10 | input | `/4 Barreira digital/VCC2_ISO` |
| U400 | 11 | IND_11 | input | `/4 Barreira digital/MISO_ADC_ISO` |
| U400 | 12 | OUTC_12 | output | `/4 Barreira digital/CS_ADC_ISO` |
| U400 | 13 | OUTB_13 | output | `/4 Barreira digital/CLK_ADC_ISO` |
| U400 | 14 | OUTA_14 | output | `/4 Barreira digital/MOSI_ADC_ISO` |
| U400 | 15 | GND2_15 | power_in | `GND_ADC` |
| U400 | 16 | VCC2_16 | power_in | `/4 Barreira digital/VCC2_ISO` |

## U401 — `MCP1824ST-3302E/DB` (MCP1824ST-3302E/DB)

- Símbolo: `EBM2_V5:MCP1824ST-3302E` · Pegada: `EBM2_V5:SOT-223-3` · Folha: `/4 Barreira digital/`
- Datasheet: `datasheets/MCP1824__22070a.pdf` (md5 e1c514c6fc42, 34 págs.)
- Ilhas da pegada: 1 @(-2.3, 3.05) 1.9x0.95; 2 @(0, 3.05) 1.9x0.95; 3 @(2.3, 3.05) 1.9x0.95; 4 @(0, -3.05) 1.9x3.25
- Nota da pegada: 2Solve PCB Library 'SOT-223-3', recuperado da PCB V2.2 (fabricada) em 2026-09-04.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| U401 | 1 | VIN_1 | power_in | `+5V` |
| U401 | 2 | GND_2 | power_in | `DGND` |
| U401 | 3 | VOUT_3 | power_out | `+3.3V_DIG` |
| U401 | 4 | TAB_4 | passive | `DGND` |

## U500 — `MCP3208T-BI/SL` (MCP3208T-BI/SL)

- Símbolo: `Analog_ADC:MCP3208` · Pegada: `EBM2_V5:SOIC16` · Folha: `/5 ADC/`
- Datasheet: `datasheets/MCP3208__21298e.pdf` (md5 c133dbad49dc, 40 págs.)
- Ilhas da pegada: 1 @(-2.35, -4.445) 0.6x1.9; 2 @(-2.35, -3.175) 0.6x1.9; 3 @(-2.35, -1.905) 0.6x1.9; 4 @(-2.35, -0.635) 0.6x1.9; 5 @(-2.35, 0.635) 0.6x1.9; 6 @(-2.35, 1.905) 0.6x1.9; 7 @(-2.35, 3.175) 0.6x1.9; 8 @(-2.35, 4.445) 0.6x1.9; 9 @(2.35, 4.445) 0.6x1.9; 10 @(2.35, 3.175) 0.6x1.9; 11 @(2.35, 1.905) 0.6x1.9; 12 @(2.35, 0.635) 0.6x1.9; 13 @(2.35, -0.635) 0.6x1.9; 14 @(2.35, -1.905) 0.6x1.9; 15 @(2.35, -3.175) 0.6x1.9; 16 @(2.35, -4.445) 0.6x1.9
- Nota da pegada: 2Solve PCB Library 'SOIC16', extraida da PCB V4.1 da EBM2 (fabricada) em 2026-09-23. Pads rodados 90 no referencial da biblioteca: na placa a pegada estava a -90 e o angulo do pad e absoluto.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| U500 | 1 | CH0_1 | input | `/5 ADC/AIN1_ADC` |
| U500 | 2 | CH1_2 | input | `/5 ADC/AIN2_ADC` |
| U500 | 3 | CH2_3 | input | `/5 ADC/AIN3_ADC` |
| U500 | 4 | CH3_4 | input | `/5 ADC/AIN4_ADC` |
| U500 | 5 | CH4_5 | input | `/5 ADC/NTC_ADC` |
| U500 | 6 | CH5_6 | input | `3V3_REF` |
| U500 | 7 | CH6_7 | input | `/5 ADC/AIN5_ADC` |
| U500 | 8 | CH7_8 | input | `/5 ADC/AIN6_ADC` |
| U500 | 9 | DGND_9 | power_in | `GND_ADC` |
| U500 | 10 | ~{CS}/SHDN_10 | input | `/4 Barreira digital/CS_ADC_ISO` |
| U500 | 11 | Din_11 | input | `/4 Barreira digital/MOSI_ADC_ISO` |
| U500 | 12 | Dout_12 | output | `/4 Barreira digital/MISO_ADC_ISO` |
| U500 | 13 | CLK_13 | input | `/4 Barreira digital/CLK_ADC_ISO` |
| U500 | 14 | AGND_14 | power_in | `GND_ADC` |
| U500 | 15 | Vref_15 | power_in | `+2V5_REF` |
| U500 | 16 | Vdd_16 | power_in | `/5 ADC/VDD_ADC` |

## U601, U602, U603, U604, U605, U606 — `AL5809-25P1-7` (AL5809-25)

- Símbolo: `EBM2_V5:AL5809` · Pegada: `EBM2_V5:PowerDI123_TypeB` · Folha: `/6 Lacos/`
- Datasheet: `datasheets/AL5809__AL5809.pdf` (md5 7e46a75cc76e, 16 págs.)
- Ilhas da pegada: 1 @(-1.525, 0) 1.05x1.5; 2 @(1.525, 0) 1.05x1.5
- Nota da pegada: PowerDI123 Type B, AL5809 (Diodes DS36625 rev. 5, pag. 13-14). Suggested Pad Layout: X 1,050 x Y 1,500, G 2,000, X1 4,100. Pad 1 = IN, pad 2 = OUT (a barra do encapsulamento fica do lado OUT, pag. 1 e 13). NAO confundir com o PowerDI-123 do KiCad (Type A, pad grande de 2,4 mm). O calor sai pela ilha do pino OUT (pad 2, pag. 8): na F3, cobre e vias nessa ilha.

| Ref | Pino | Nome no símbolo | Tipo | Rede |
|---|---|---|---|---|
| U601 | 1 | In_1 | passive | `/1 Conectores/AIN1-` |
| U601 | 2 | Out_2 | passive | `/6 Lacos/AIN1_LIM` |
| U602 | 1 | In_1 | passive | `/1 Conectores/AIN2-` |
| U602 | 2 | Out_2 | passive | `/6 Lacos/AIN2_LIM` |
| U603 | 1 | In_1 | passive | `/1 Conectores/AIN3-` |
| U603 | 2 | Out_2 | passive | `/6 Lacos/AIN3_LIM` |
| U604 | 1 | In_1 | passive | `/1 Conectores/AIN4-` |
| U604 | 2 | Out_2 | passive | `/6 Lacos/AIN4_LIM` |
| U605 | 1 | In_1 | passive | `/1 Conectores/AIN5-` |
| U605 | 2 | Out_2 | passive | `/6 Lacos/AIN5_LIM` |
| U606 | 1 | In_1 | passive | `/1 Conectores/AIN6-` |
| U606 | 2 | Out_2 | passive | `/6 Lacos/AIN6_LIM` |

