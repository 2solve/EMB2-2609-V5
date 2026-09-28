---
projeto: IC2S Extension Board EBM2 V5 (6AI 4-20 mA)
etapa: BOM preliminar (2shw-pcb:bom, modo preliminar)
netlist: EBM2_V5_2026-09-28.net
fonte_dados: Mouser Search API, consulta de 2026-09-25T06:09 + reconsulta 2026-09-25T06:10 + reconsulta 2026-09-25T06:38 + reconsulta 2026-09-25T07:09
moeda: USD
---

# BOM preliminar — EBM2 V5

**Só se liberta a Suprimentos com o Portão 1 assinado. Hardware não compra.**

Fonte dos dados comerciais: Mouser Search API, consulta de 2026-09-25T06:09 + reconsulta 2026-09-25T06:10 + reconsulta 2026-09-25T06:38 + reconsulta 2026-09-25T07:09. Ciclo de vida só com fonte e data; sem fonte é `N/D`, nunca «activo» por omissão.

## 1 · Alertas

- **Ciclo de vida fora de «activo»:** ADR4525WBRZ-R7 — Restricted Availability (Mouser 2026-09-25)
- **Sem dado Mouser:** 2 MPN.
- **Stock Mouser abaixo de 10 placas:**
  - KG EELP41.22-PHRH-35-A8J8-20-R18 (D1, D5, D24): 0 em stock para 3 por placa; alternativa verificada Q65113A7469: 15898 em stock
  - 3413.0002.22 (F3, F4, F5, F6, F7, F8): 0 em stock para 6 por placa; alternativa verificada 3413.0002.11: 8838 em stock
  - ISO7141CCDBQR (U6): 0 em stock para 1 por placa; alternativa verificada ISO7141CCDBQ: 0 em stock

### Alternativas verificadas (mesma peça eléctrica, conferida no datasheet)

| Principal | Alternativa | Stock Mouser | Evidência |
|---|---|---:|---|
| `ADR4525WBRZ-R7` | `ADR4525BRZ` | N/D | O MPN original: mesmo grau B em tubo de 98; na Mouser sem preço nem stock e «Restricted Availability» (2026-09-25). A WBRZ-R7 entrou na tanda B por isso (ADR45xx Rev. G, tabela 14 pág. 40, nota 2 pág. 41) |
| `3413.0002.22` | `3413.0002.11` | 8838 | Mesma linha eléctrica (50 mA, 63 VDC, 9200 mΩ, 0,0002 A²s); só muda a embalagem: 100 un. em fita (Schurter USFF, págs. 3-4) |
| `KG EELP41.22-PHRH-35-A8J8-20-R18` | `Q65113A7469` | 15898 | Código de encomenda OSRAM do mesmo tipo e bin, KG EELP41.22-PHRH-35-A8J8 (datasheet v1.4 pág. 3) |
| `ISO7141CCDBQR` | `ISO7141CCDBQ` | 0 | Mesma peça, tubo de 75 em vez de bobina de 2500 (TI, package option addendum pág. 27) |

## 2 · Linhas (41, 123 componentes montados)

| Refs | Qtd | Valor | Pegada | Fabricante | MPN | Mouser | Stock | Unit. lote 1 | Unit. lote 10 | Unit. lote 100 | Ciclo de vida | Origem | Notas |
|---|---:|---|---|---|---|---|---|---:|---:|---:|---|---|---|
| C1 | 1 | 2u2/100V | C_1210_3225Metric | N/D | `C3225X7R2A225K230AB` | 810-C3225X7R2A225K | 30005 | 0.7800 | 0.4880 | 0.3380 | Production (ficha TDK 2026-09-25) | NOVO | C1: curva TDK ~1,54 uF a 30,4 V; pior caso 1,18 uF > 1 uF (TPS7A4001); RA2 11,3x. X7S 1206 descartado (0,89 uF) |
| C2, C30 | 2 | 10uF/100V | C_1210_3225Metric | Murata | `GRM32EC72A106ME05L` | 81-GRM32EC72A106ME5L | 35196 | 1.1800 | 0.7580 | 0.5420 | Activo (DigiKey 2026-09-24) | biblioteca 2Solve |  |
| C3, C6, C9, C12, C13, C14, C16, C17, C18, C19, C20, C21, C22, C23, C24, C25, C26, C27, C28, C34, C35 | 21 | 100nF/50V | 0603C | TDK | `C1608X7R1H104K080AA` | N/D | N/D | N/D | N/D | N/D | N/D | biblioteca 2Solve |  |
| C4, C8, C10, C31, C32 | 5 | 10uF/50V | C_1206_3216Metric | TDK | `C3216X5R1H106K160AB` | 810-C3216X5R1H106K | 124920 | 1.8500 | 0.9910 | 0.7820 | Production (ficha TDK 2026-09-24) | biblioteca 2Solve | Curva TDK conferida: C4 7,0 µF a 5 V, C8 7,2 µF a 3,3 V, C31+C32 8,9 µF a 12,6 V (pior caso) |
| C5, C11 | 2 | 2u2 | 0603C | TDK | `C1608X5R1E225K080AB` | 810-C1608X5R1E225K | 15300 | 0.2700 | 0.1610 | 0.0980 | Production (ficha TDK 2026-09-24) | biblioteca 2Solve | Curva TDK conferida (ficha 2026-09-24): pior caso 1,44 µF a 2,5 V (C5) e 1,26 µF a 3,3 V (C11), ≥ 1 µF |
| C7, C33 | 2 | 10nF | 0603C | Murata | `GCM188R71H103KA37J` | 81-GCM188R71H103KA7J | 3509127 | 0.1200 | 0.0680 | 0.0410 | N/D | biblioteca 2Solve |  |
| C15 | 1 | 1uF/50V | 0603C | TDK | `C1608X7R1H105K080AB` | N/D | N/D | N/D | N/D | N/D | N/D | biblioteca 2Solve |  |
| C29 | 1 | 100nF/100V | 0603C | Murata | `GRM188R72A104KA35D` | 81-GRM188R72A104KA35 | 1344731 | 0.1600 | 0.0870 | 0.0540 | Activo (substituto do GRM188R71E104KA01D obsoleto, relatório 2026-09-24) | biblioteca 2Solve |  |
| D1, D5, D24 | 3 | KG EELP41.22 | 0603LED | ams OSRAM | `KG EELP41.22-PHRH-35-A8J8-20-R18` | 720-P4122PHRH35A8J82 | 0 | 0.1600 | 0.1090 | 0.0760 | Activo (substituto do LG Q396 obsoleto, relatório 2026-09-24) | biblioteca 2Solve |  |
| D2 | 1 | SMA6J33A-Q | DO-214 | Bourns | `SMA6J33A-Q` | 652-SMA6J33A-Q | 11149 | 0.5800 | 0.2760 | 0.2270 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve |  |
| D4 | 1 | MBR1H100SF | SOD123 | onsemi | `MBR1H100SFT3G` | 863-MBR1H100SFT3G | 106816 | 0.6600 | 0.2970 | 0.2610 | Activo (DigiKey 2026-09-24) | biblioteca 2Solve |  |
| D6, D7, D8, D9, D10, D11 | 6 | SMBJ33A | DO-214AA | Diodes Inc. | `SMBJ33A-13-F` | 621-SMBJ33A-13-F | 89868 | 0.5700 | 0.2710 | 0.1900 | N/D | NOVO | Novo na rev. 2.4 (DS19002 conferido) |
| D12, D13, D14, D15, D16, D17 | 6 | 824520361 | DO-214AA | Würth Elektronik | `824520361` | 710-824520361 | 82 | 0.3500 | 0.3200 | 0.2370 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve | Stock baixo (314 D / 82 M) para 6 por placa |
| D18, D19, D20, D21, D22, D23 | 6 | BAV199 | SOT23-3 | onsemi | `BAV199LT1G` | 863-BAV199LT1G | 136104 | 0.1600 | 0.0720 | 0.0450 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve |  |
| F2 | 1 | CC12H750MA-TR | 1206F | Eaton | `CC12H750MA-TR` | 504-CC12H750MA-TR | 5070 | 1.1600 | 1.0700 | 0.8160 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve |  |
| F3, F4, F5, F6, F7, F8 | 6 | 50mA | 1206F | Schurter | `3413.0002.22` | 693-3413.0002.22 | 0 | 2.4100 | 1.8200 | 1.3700 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve |  |
| FB1, FB2 | 2 | BLM18PG471SN1D | 0603FB | Murata | `BLM18PG471SN1D` | 81-BLM18PG471SN1D | 443559 | 0.1000 | 0.0620 | 0.0440 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve |  |
| P1 | 1 | M20-7822046 | HDR1X20_FEMALE | Harwin | `M20-7822046` | 855-M20-7822046 | 1287 | 2.2400 | 2.2400 | 1.8600 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve |  |
| P2 | 1 | M20-7821446 | HDR1X14_FEMALE | Harwin | `M20-7821446` | 855-M20-7821446 | 562 | 1.7500 | 1.4400 | 1.4300 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve |  |
| R1, R34 | 2 | 14k7 | 0603R | Panasonic | `ERJ-3EKF1472V` | 667-ERJ-3EKF1472V | 66735 | 0.1000 | 0.0240 | 0.0200 | Activo (DigiKey 2026-09-24) | NOVO |  |
| R2, R10, R11, R12, R13, R14, R15 | 7 | 0R | 0603R | Yageo | `RC0603JR-070RL` | 603-RC0603JR-070RL | 5980483 | 0.1000 | 0.0080 | 0.0050 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve |  |
| R4 | 1 | 2k2 | 0603R | Yageo | `RC0603FR-072K2L` | 603-RC0603FR-072K2L | 557666 | 0.1000 | 0.0140 | 0.0080 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve |  |
| R5 | 1 | 32k4 | 0603R | Yageo | `RC0603FR-0732K4L` | 603-RC0603FR-0732K4L | 221 | 0.1100 | 0.0140 | 0.0090 | N/D | NOVO |  |
| R6, R9, R36 | 3 | 10k | 0603R | Yageo | `RC0603FR-0710KL` | 603-RC0603FR-0710KL | 2811281 | 0.1000 | 0.0140 | 0.0080 | N/D | biblioteca 2Solve |  |
| R7 | 1 | 100k | 0603R | Yageo | `RC0603FR-07100KL` | 603-RC0603FR-07100KL | 5080704 | 0.1000 | 0.0140 | 0.0080 | N/D | biblioteca 2Solve |  |
| R8 | 1 | 4k12 | 0603R | Yageo | `RC0603FR-074K12L` | 603-RC0603FR-074K12L | 16714 | 0.1000 | 0.0140 | 0.0080 | N/D | NOVO |  |
| R16, R17, R18, R19, R20, R21 | 6 | 110R 0,1% | 1206R | Panasonic | `ERA8AEB111V` | 667-ERA-8AEB111V | 7280 | 0.2700 | 0.1970 | 0.1640 | Activo (DigiKey 2026-09-24) | NOVO |  |
| R22, R23, R24, R25, R26, R27 | 6 | 3k3 | 0603R | Yageo | `RC0603FR-073K3L` | 603-RC0603FR-073K3L | 588651 | 0.1200 | 0.0140 | 0.0100 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve |  |
| R28, R29, R30, R31, R32, R33 | 6 | 4k7 | 0603R | Yageo | `RC0603FR-074K7L` | 603-RC0603FR-074K7L | 2124140 | 0.1000 | 0.0140 | 0.0080 | N/D | NOVO |  |
| R35 | 1 | 93k1 | 0603R | Stackpole | `RMCF0603FT93K1` | 708-RMCF0603FT93K1 | 87588 | 0.1000 | 0.0120 | 0.0100 | N/D | biblioteca 2Solve |  |
| R37 | 1 | 13k3 | 0603R | Yageo | `RC0603FR-0713K3L` | 603-RC0603FR-0713K3L | 420840 | 0.1000 | 0.0140 | 0.0080 | N/D | NOVO |  |
| R38, R39 | 2 | 6k65 | 0603R | Yageo | `RC0603FR-076K65L` | 603-RC0603FR-076K65L | 879514 | 0.1000 | 0.0140 | 0.0080 | N/D | biblioteca 2Solve |  |
| R40 | 1 | 5k62 0,1% | 0603R | Panasonic | `ERA3AEB5621V` | 667-ERA-3AEB5621V | 8540 | 0.1000 | 0.0640 | 0.0610 | Activo (DigiKey 2026-09-24) | NOVO | Prazo de fábrica 49 semanas (DigiKey 2026-09-24) |
| TH1 | 1 | 10k NTC | 0603R | Vishay | `NTCS0603E3103JLT` | 594-NTCS0603E3103JLT | 11185 | 0.2300 | 0.2140 | 0.1750 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve |  |
| U1, U14 | 2 | TPS7A4001DGN | HVSSOP-8-1EP | Texas Instruments | `TPS7A4001DGNR` | 595-TPS7A4001DGNR | 11204 | 3.5300 | 2.6500 | 2.1800 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve |  |
| U2 | 1 | ADR4525WBRZ-R7 | SOIC8 | Analog Devices | `ADR4525WBRZ-R7` | 584-ADR4525WBRZ-R7 | 2147 | 14.8000 | 11.5900 | 9.9100 | Restricted Availability (Mouser 2026-09-25) | NOVO | Família «Restricted Availability» na Mouser: comprar cedo |
| U3 | 1 | TL431B | SOT23-3 | Texas Instruments | `TL431BQDBZR` | 595-TL431BQDBZR | 820 | 0.4400 | 0.3060 | 0.2360 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve |  |
| U4, U5 | 2 | MCP1824T-3302E/OT | SOT-23-5 | Microchip | `MCP1824T-3302E/OT` | 579-MCP1824T-3302EOT | 14500 | 0.5600 | 0.5600 | 0.4750 | N/D | NOVO | Novo na rev. 2.5 (U4) |
| U6 | 1 | ISO7141CCDBQR | SSOP16-4.9x3.9mm | Texas Instruments | `ISO7141CCDBQR` | 595-ISO7141CCDBQR | 0 | 10.9400 | 8.5600 | 7.3000 | Activo (BOM EBM7 2026-09-14) | biblioteca 2Solve | **0 em stock na Mouser** (BOM EBM7 2026-09-14): risco de abastecimento |
| U7 | 1 | MCP3208T-BI/SL | SOIC16 | Microchip | `MCP3208T-BI/SL` | 579-MCP3208T-BI/SL | 3893 | 5.7600 | 5.7600 | 4.6400 | Activo (DigiKey 2026-09-24) | NOVO |  |
| U8, U9, U10, U11, U12, U13 | 6 | TPS26613DDFR | SOT-23-8 | Texas Instruments | `TPS26613DDFR` | 595-TPS26613DDFR | 3238 | 1.8000 | 1.2100 | 0.9720 | N/D | biblioteca 2Solve | Novo na rev. 2.4 (protector de laço) |

## 3 · Totais da placa (USD)

| Lote | Total | Por placa |
|---:|---:|---:|
| 1 | parcial 97.54 (faltam 2 linhas) | parcial 97.54 |
| 10 | parcial 699.56 (faltam 2 linhas) | parcial 69.96 |
| 100 | parcial 5634.80 (faltam 2 linhas) | parcial 56.35 |

Linhas sem preço (fora do parcial): C3, C6, C9, C12, C13, C14, C16, C17, C18, C19, C20, C21, C22, C23, C24, C25, C26, C27, C28, C34, C35; C15.

Preço no escalão que a quantidade do lote atinge (qtd por placa × placas); mínimos e múltiplos de embalagem não somados — Suprimentos confirma no carrinho.

### Cenário comprável hoje na Mouser

Principal quando há stock para o lote; senão a alternativa verificada com stock. As linhas em «sem stock» entram a preço de lista mas **não se compram hoje** na Mouser.

| Lote | Total | Por placa | Sem stock para o lote |
|---:|---:|---:|---|
| 1 | 102.13 | 102.13 | `C1608X7R1H104K080AA`, `C1608X7R1H105K080AB`, `ISO7141CCDBQR` |
| 10 | 732.08 | 73.21 | `C1608X7R1H104K080AA`, `C1608X7R1H105K080AB`, `ISO7141CCDBQR` |
| 100 | 5823.80 | 58.24 | `824520361`, `C1608X7R1H104K080AA`, `C1608X7R1H105K080AB`, `ISO7141CCDBQR` |

## 4 · Compra antecipada (críticos / long-lead) e acções

| Peça | Porquê | Acção sugerida |
|---|---|---|
| `ISO7141CCDBQR` (U6) | **0 em stock na Mouser em todas as variantes** (DBQR, DBQ, DBQRG4; 2026-09-25); prazo 112 dias (DBQR) / 63 dias (DBQ, tubo). Única peça que atravessa a barreira; a versão F (saída por defeito baixa) **não serve**: deixava o ADC seleccionado com o barramento desligado | Encomendar `ISO7141CCDBQ` à fábrica logo após o Portão 1, ou outro distribuidor autorizado |
| `3413.0002.22` (F3-F8, 6 por placa) | 0 em stock, **prazo 269 dias** | Protótipo com `3413.0002.11` (mesma peça, 100 un. em fita; 8838 em stock) |
| `ADR4525WBRZ-R7` (U2) | Família inteira **«Restricted Availability»** na Mouser (a BRZ original sem preço nem stock; trocada na tanda B) | Comprar com o protótipo (2147 em stock). Grau A **não** serve: 8 ppm/°C bowtie contra 4 |
| `ADR4525WBRZ-R7` (U2): grau W | A pág. 41 do ADR45xx Rev. G avisa que o modelo automóvel «may have specifications that differ from the commercial models». Conferido (2026-09-25): as tabelas 1-2 (págs. 3-5) só têm os graus A, B, C e D, **sem coluna W**; a guia de encomenda (pág. 40) dá o WBRZ-R7 como grau B, −40…+125 °C, SOIC-8. O datasheet **não publica** nenhuma especificação própria do W; se existir, só a ADI a dá | Decisão mantida (U2 = WBRZ-R7, fechada pelo projectista). Pedir à ADI, com a compra, a confirmação de que o WBRZ cumpre a tabela 2 do grau B (ou o relatório Automotive Reliability) |
| LED `KG EELP41.22` (3) | 0 em stock pelo código comprido | Pedir por `Q65113A7469` (mesmo tipo e bin; 15898 em stock) |
| `824520361` (D12-D17, 6 por placa) | 82 em stock: chega para 13 placas; prazo 154 dias | Reservar para o protótipo |
| `ERA3AEB5621V`, `ERA8AEB111V` | Prazo de fábrica 343 dias (Mouser); stock 8540 / 7280 | Comprar com o protótipo |
| `C1` | **Fechado na tanda C:** TDK `C3225X7R2A225K230AB` em 1210 (pior caso 1,18 µF a 30,4 V). Descartados: TDK X7S 1206 (0,89 µF) e Murata GRM31CR72A225KA73L / GRM32ER72A225KA35L (obsoleto / fim de vida) | Land pattern TDK (PA 2,0-2,4 mm) contra a pegada IPC do projecto (1,8 mm): conferir na F3 |
| `R3` | **Fechado na tanda B:** KOA `SG73P2ATTD1500F`, pulso conferido (~4x) | — |
| `C5`, `C11` | **Conferido:** curva TDK dá ≥ 1,26 µF no pior caso | — |

```yaml
evidencia:
  skill: 2shw-pcb:bom
  modo: preliminar
  artefatos: [bom_preliminar_EBM2_V5.md, bom_preliminar_EBM2_V5.csv]
  itens: 41
  alertas_ciclo_vida: 1
  itens_nd: 2
  total_1un: N/D
  total_100un: N/D
  fonte_dados: wrapper(2026-09-25T06:09 + reconsulta 2026-09-25T06:10 + reconsulta 2026-09-25T06:38 + reconsulta 2026-09-25T07:09)
```
