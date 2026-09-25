# Componentes: V4.1 → V5 — EBM2 V5 (6AI 4-20 mA)

Data: 2026-09-23. Estado: esquemático da F2, etapa 2.2b.

Gerado por `ferramentas/gera_lista_componentes.py` a partir das duas netlists exportadas pelo
KiCad: a da V4.1 (`C:\hw\hw-ebm2-v4.1`, só leitura) e a da V5 actual. A correspondência
entre designadores é a da `intencao_EBM2_V5.md` rev. 2, §2; as justificações citam o
`planejamento_pcb_EBM2_V5.md` rev. 3 e a intenção. Os part numbers não foram escritos à mão.

## 1 · Peças que continuam, com o designador novo

| Função | V4.1 | V5 | Muda? | Porquê |
|---|---|---|---|---|
| Conector do barramento | `M20-7822046` P1 | `M20-7822046` P1 | não | Pinagem congelada (RC2). |
| Conector de campo | `M20-7821446` P2 | `M20-7821446` P2 | não | Pinagem congelada (RC2). |
| Isolador digital | `ISO7141CCDBQR` U4 | `ISO7141CCDBQR` U400 | não | Mesma peça. VCC1 passa a 3,3 V pelo U401 novo (fecha G2). Símbolo da EBM7 Legacy. |
| Conversor A/D | `MCP3208T-CI/SL` U5 | `MCP3208T-BI/SL` U500 | **sim** | Grau -CI → -BI: mesmo encapsulamento e pinagem, INL ±1 LSB em vez de ±2 (planejamento 2.1, 2.7b). |
| LDO 3,3 V do ADC | `SPX3819-3.3` U11 | `SPX3819M5-L-3-3/TR` U201 | não | Mesma peça; o MPN completo passa a constar. |
| Ferrite do VCC2 do isolador | `BLM18PG471SN1D` FB2 | `BLM18PG471SN1D` FB400 | não | — |
| Ferrite do VDD do conversor | `BLM18PG471SN1D` FB3 | `BLM18PG471SN1D` FB500 | não | — |
| Desacoplamento VCC1 do isolador | `GRM188R71E104KA01D` C7 | `GRM188R72A104KA35D` C401 | **sim** | — |
| Desacoplamento VCC2 do isolador | `GRM188R71E104KA01D` C8 | `GRM188R72A104KA35D` C403 | **sim** | — |
| Desacoplamento VDD do conversor | `GRM188R71E104KA01D` C10 | `GRM188R72A104KA35D` C502 | **sim** | Mantém-se; acresce o C501 de 1 µF que o datasheet pede (§ 6.4, pág. 23). |
| Termístor de placa | `NTCS0603E3103JLT` R5 | `NTCS0603E3103JLT` R700 | não | Mesma peça. Topo em +2V5_REF em vez de 3V3_REF (planejamento 2.7e); símbolo de NTC. |
| Divisor do termistor | `ERA-3AEB5621V` R8 | `ERA3AEB5621V` R701 | não | — |
| Pull-up do EN do SPX3819 | `CRCW0603100KFKEA` R34 | 100k *(sem MPN)* R203 | MPN por fixar | — |
| Canais 1-6: fusível | `F0603G0R10FNTR` F1, F2, F3, F4, F5, F6 | `3413.0002.22` F601, F602, F603, F604, F605, F606 | **sim** | 100 mA 0603 → 50 mA 1206, a peça da EBM7 Legacy. Rev. 2.1: abre só no curto franco à massa (~2,5 A); o curto do transmissor é do limitador U60x. |
| Canais 1-6: TVS no retorno | `824500301` D4, D7, D13, D22, D2, D12 | `824520361` D601, D602, D603, D604, D605, D606 | **sim** | 30 V SMA → 36 V SMB 600 W (rev. 2.2): envolvente 18–32 V; em curto o retorno sobe ao trilho (31,4 V). |
| Canais 1-6: TVS no trilho | `824500301` D3, D6, D10, D1, D11, D21 | `824520361` D611, D612, D613, D614, D615, D616 | **sim** | Mantidos os seis, num trilho único (+24V_ADC). 30 V → 36 V (rev. 2.2): a 32 V o trilho chega a 31,4 V. É o da EBM7. |
| Canais 1-6: série de protecção | `RC0603FR-07249RL` R6, R11, R18, R15, R1, R4 | `RC1206FR-07100RL` R601, R602, R603, R604, R605, R606 | **sim** | 249 Ω 0603 → 100 Ω 1206 (rev. 2.1/2.2): o curto passa a ser do limitador; 100 Ω para a tensão ao transmissor a 18 V. |
| Canais 1-6: burden | `CRCW0603160RFKEA` R9, R13, R21, R17, R3, R14 | `ERA8AEB111V` R611, R612, R613, R614, R615, R616 | **sim** | 160 Ω 1 % → 110 Ω 0,1 % 25 ppm/°C: com VREF 2,5 V, 20 mA x 110 Ω = 2,2 V (planejamento 2.5). Em 1206 desde a rev. 2.1. |
| Canais 1-6: antialias 3,3 kΩ | `RC0603FR-073K3L` R7, R12, R19, R16, R2, R10 | `RC0603FR-073K3L` R621, R622, R623, R624, R625, R626 | não | — |
| Canais 1-6: condensador do filtro | `GRM188R71E104KA01D` C9, C13, C18, C3, C1, C2 | `GRM188R72A104KA35D` C601, C602, C603, C604, C605, C606 | **sim** | — |
| Canais 1-6: clamp | `BAT54S` D5, D8, D14, D23, D9, D20 | `BAV199LT1G` D621, D622, D623, D624, D625, D626 | **sim** | BAT54S → BAV199 (EBM7): fuga de 5 nA a 25 °C contra µA do Schottky (planejamento 2.1). |
| LED do 5 V | `LG Q396-PS-35` D18 | `KG EELP41.22-PHRH-35-A8J8-20-R18` D204 | **sim** | Passa a indicar +5V_ADC (intenção § 11). |
| LED de trilho de laço | `LG Q396-PS-35` D19 | `KG EELP41.22-PHRH-35-A8J8-20-R18` D630 | **sim** | Passa a indicar +24V_ADC, o F202 inteiro. |
| LED de trilho de laço | `LG Q396-PS-35` D25 | `KG EELP41.22-PHRH-35-A8J8-20-R18` D203 | **sim** | Passa a indicar a entrada de +24V. |
| Resistência do LED do 5 V | `RC0603FR-072K2L` R24 | `RC0603FR-072K2L` R208 | não | — |
| Resistência do LED | `ERJ-3EKF1472V` R25 | `ERJ-3EKF1472V` R630 | não | — |
| Resistência do LED | `ERJ-3EKF1472V` R26 | `ERJ-3EKF1472V` R207 | não | — |

## 2 · Peças da V4.1 que saem

| V4.1 | Porquê |
|---|---|
| `PDM2-S24-S24-S` U1, U8<br>`CRE1S2405SC` U7 | Conversores isolados: a V5 alimenta o campo a partir do 24 V, sem isolamento de potência (folhas 02 e 03). |
| `PMEG6010CEH,115` D15, D16, D24 | PMEG6010CEH de 60 V: curto contra o grampo de 58,1 V do D200; substituídos pelo MBR1H100SF de 100 V. |
| `ZMM5234B` D17 | Sai (lista da intenção § 2). **Motivo individual não escrito.** |
| `BZT52H-B2V4,115` D26 | Zener de 2,45 V em serie na entrada: conduzia ~130 mA de uma peça de classe µA (notas da folha 02). |
| `3413.0008.22` F7, F9 | I²t de fusão 1,5e-3 A²s contra 5,65e-3 A²s de arranque dos 10 µF: avaria medida na V4.1 (notas da folha 02). Substituidos por CC12H (Eaton). |
| `0466.125NR` F8 | Sai com a entrada antiga (lista da intenção § 2). **Motivo individual não escrito.** |
| `ESL107M050AGMAA` C12, C28 | Electrolíticos de 50 V ficavam 8,1 V abaixo do grampo; substituídos pelo cerâmico C201 de 100 V. |
| `BLM18PG471SN1D` FB4 | Sai (lista da intenção § 2). **Motivo individual não escrito.** |
| `C1206C102KGRACTU` C4, C16, C19, C21, C31, C32<br>`C1206C104M5RAC` C5, C22<br>`UMK316BBJ106ML-T` C11, C15, C27, C29, C30<br>`GRM188R71E104KA01D` C20, C53, C54<br>`GRM188R61C106KAALD` C25<br>`GRM32ER61A107ME20K` C26<br>`GRM188R61C225KE15J` C51, C52 | Condensadores sem correspondente na V5: a intenção (§2) di-los ao serviço dos conversores que saem. **Não se conferiu um a um.** |

## 3 · Peças novas na V5

| V5 | Porquê |
|---|---|
| 2u2/100V *(sem MPN)* C200 | Entrada do regulador 2,2 µF/100 V 1206. **MPN por fixar (V6).** |
| `GRM32EC72A106ME05L` C201 | Bulk dos laços 10 µF/100 V, no lugar dos electrolíticos. |
| 10uF/25V *(sem MPN)* C202 | Saída do U200. |
| 100nF *(sem MPN)* C203 | Saída do U200. |
| 2u2 *(sem MPN)* C204 | Saída do SPX3819. |
| 100nF *(sem MPN)* C205 | Saída do SPX3819. |
| 100nF *(sem MPN)* C206 | Entrada do ADR4525. |
| 1uF *(sem MPN)* C207 | Saída do ADR4525. |
| 10nF *(sem MPN)* C208 | BP do SPX3819: baixo ruído. |
| 1uF *(sem MPN)* C400 | Entrada do U401. |
| 1uF *(sem MPN)* C402 | Saída do U401. |
| `GRM188R72A104KA35D` C500 | VREF no pino do ADC. |
| 1uF *(sem MPN)* C501 | 1 µF no VDD, pedido pelo datasheet. |
| `GRM188R72A104KA35D` C700 | 100 nF no canal do NTC (fig. 4-2 do DS21298E). |
| `SMA6J33A-Q` D200 | TVS de entrada 33 V: a V4.1 não tem nenhum (planejamento 2.2). |
| `MBR1H100SFT3G` D201 | Bloqueio 100 V da rama do regulador. |
| `MBR1H100SFT3G` D202 | Bloqueio 100 V da rama dos laços. |
| `BAT46W-7-F` D641 | Schottky antiparalelo ao U601: o AL5809 só aguenta −0,3 V em inversão. |
| `BAT46W-7-F` D642 | Idem, canal 2. |
| `BAT46W-7-F` D643 | Idem, canal 3. |
| `BAT46W-7-F` D644 | Idem, canal 4. |
| `BAT46W-7-F` D645 | Idem, canal 5. |
| `BAT46W-7-F` D646 | Idem, canal 6. |
| `CC12H250MA-TR` F201 | Fusível da rama do regulador, CC12H 250 mA (a série não tem 100 mA). |
| `CC12H750MA-TR` F202 | Fusível da rama dos laços, CC12H 750 mA: margem de arranque 41,7× (planejamento 2.6). |
| `RC0603JR-070RL` R200 | Net-tie 0 Ω, único caminho GND_24V ↔ GND_ADC. |
| 32k4 *(sem MPN)* R201 | Divisor do U200. |
| 10k *(sem MPN)* R202 | Divisor do U200. |
| 4k42 *(sem MPN)* R204 | Divisor do TL431. |
| 10k *(sem MPN)* R205 | Divisor do TL431. |
| 33R *(sem MPN)* R206 | Limitador de arranque 33 Ω (rev. 2.2, margem 12,3× a 32 V): sem ele o F201 não cumpre RA2. **MPN por fixar (V5).** |
| `TPS7A4001DGNR` U200 | Regulador 24 → 4,974 V (EBM7). |
| `ADR4525BRZ` U202 | Referência 2,5 V ±0,02 % (EBM7): VREF deixa de ser o VDD. |
| `TL431BQDBZR` U203 | TL431 a 3,6 V: sumidouro dos clamps; a V4.1 não tem nenhum. |
| `MCP1824ST-3302E/DB` U401 | LDO 3,3 V para o VCC1 do isolador: fecha G2. |
| `AL5809-25P1-7` U601 | Limitador de corrente 23,75-26,25 mA no retorno (rev. 2.1): fecha a V8, herdada da V4.1. |
| `AL5809-25P1-7` U602 | Idem, canal 2. |
| `AL5809-25P1-7` U603 | Idem, canal 3. |
| `AL5809-25P1-7` U604 | Idem, canal 4. |
| `AL5809-25P1-7` U605 | Idem, canal 5. |
| `AL5809-25P1-7` U606 | Idem, canal 6. |
| `T201`, `T202`, `T203`, `T204`, `T205`, `T206`, `T207`, `T400`, `T500` | Pontos de prova: a V4.1 tem zero (RD1). |
| `FID101`, `FID102`, `FID103` | Fiduciais: a V4.1 tem zero (RD2). |

## 4 · Contagem

| | Peças |
|---|---|
| V4.1 | 101 |
| V5 | 120 |
| Continuam (§1) | 67 na V4.1 → 67 na V5, em 27 linhas: 12 iguais, 14 mudam de peça, 1 com MPN por fixar na V5 |
| Peças da V5 ainda sem MPN no esquemático | 17: C200, C202, C203, C204, C205, C206, C207, C208, C400, C402, C501, R201, R202, R203, R204, R205, R206 |
| Saem (§2) | 34 |
| Novas (§3) | 53 |

Em aberto: os MPN em falta (fecham na BOM preliminar da F2; `R206` é a `V5` e `C200` a `V6`
da intenção) e três saídas sem motivo individual escrito (`D17`, `F8`, `FB4`).
