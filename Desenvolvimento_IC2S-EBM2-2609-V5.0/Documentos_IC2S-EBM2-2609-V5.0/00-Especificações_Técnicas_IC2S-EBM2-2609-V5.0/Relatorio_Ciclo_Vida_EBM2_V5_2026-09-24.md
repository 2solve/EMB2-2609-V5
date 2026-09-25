# Ciclo de vida dos componentes — EBM2 V5

Data: 2026-09-24 · F2, antes da BOM preliminar · 30 MPN distintos no esquemático (mais 11
posições ainda sem MPN, que se fecham na BOM).

**Fontes, por ordem de uso:**
1. BOM da EBM7 V2.3 de 2026-09-14 (`bom_EBM7_V23_2026-09-14.csv`), com o estado da DigiKey e da
   Mouser: cobre 18 dos 30.
2. Páginas da DigiKey consultadas hoje: cobrem mais 11.
3. Datasheets dos fabricantes, para confirmar que os substitutos são equivalentes.

A ferramenta de stock do servidor KiCad (`jlcsearch`) **não serve para isto**. No controlo
positivo devolveu stock e preço do `LG Q396-PS-35`, que está obsoleto, sem dizer nada do ciclo
de vida.

## 1 · Obsoletos ou sem stock — substituídos

| Peça | Posições | Estado | Substituto | Porque este |
|---|---|---|---|---|
| `LG Q396-PS-35` (LED verde 0603) | `D203`, `D204`, `D630` | **Obsoleto** (DigiKey, última compra 2026-07-02; datasheet ams OSRAM v1.9 «Discontinued») | **`KG EELP41.22-PHRH-35-A8J8-20-R18`** | É o que a EBM7 V2.3 já adoptou (2026-09-15), com o brilho conferido pelo revisor (mínimo +16 % face ao Q396). Datasheet v1.4 de 2026-08-07: 0603, cátodo marcado, −40 a +105 °C, I_F mín. 0,5 mA (usamos ~1,4-1,5 mA). DigiKey «Active», 186 041 em stock. **Mesma pegada `0603LED`, mesmas resistências** |
| `GRM188R71E104KA01D` (100 nF X7R 25 V 0603) | `C401`, `C403`, `C500`, `C502`, `C601`-`C606`, `C700` (11) | **Obsoleto** (DigiKey: «Obsolete and no longer manufactured») | **`GRM188R72A104KA35D`** | Substituto indicado pela DigiKey: 100 nF X7R 0603, 100 V, −55 a +125 °C, «Active», 862 866 em stock. **Atenção:** o `GRM188R71H104KA93D` (50 V), a alternativa óbvia, **também está obsoleto** |
| `BAT46W-E3-08` (Vishay, SOD-123) | `D641`-`D646` | «Active», mas **0 em stock até 2027-01-11** | **`BAT46W-7-F`** (Diodes Inc.) | DS30044 rev. 20 (2023-11): 100 V, V_F máx. 0,25 V a 0,1 mA, 0,45 V a 10 mA e 1,0 V a 250 mA, SOD123 com banda de cátodo. **Os mesmos máximos do Vishay**, que fica como alternativa. DigiKey «Active», em stock |

Nenhuma das três substituições muda pegada, ligação nem valor eléctrico.

## 2 · Activos (verificado)

| MPN | Estado | Stock | Fonte |
|---|---|---|---|
| `TPS7A4001DGNR` | Activo | 1 901 D / 12 228 M | BOM EBM7 2026-09-14 |
| `SPX3819M5-L-3-3/TR` | Activo | — / 258 M | BOM EBM7 |
| `TL431BQDBZR` | Activo | — / 820 M | BOM EBM7 |
| `ISO7141CCDBQR` | Activo | **— / 0 M** | BOM EBM7 · **risco de abastecimento: sem stock na Mouser** |
| `MCP1824ST-3302E/DB` | Activo | 18 061 / 11 937 | BOM EBM7 |
| `MCP3208T-BI/SL` | Activo | 2 748 D | DigiKey 2026-09-24 |
| `AL5809-25P1-7` | Activo | 92 018 D | DigiKey 2026-09-24 |
| `BAV199LT1G` | Activo | 124 710 / 151 885 | BOM EBM7 |
| `MBR1H100SFT3G` | Activo | 453 867 D | DigiKey 2026-09-24 |
| `SMA6J33A-Q` | Activo | 15 395 / 11 149 | BOM EBM7 |
| `824520361` | Activo | **314 / 82** | BOM EBM7 · stock baixo (12 por placa) |
| `CC12H250MA-TR` | Activo | 4 159 D | DigiKey 2026-09-24 |
| `CC12H750MA-TR` | Activo | 6 448 / 5 070 | BOM EBM7 |
| `3413.0002.22` | Activo | 1 492 / 3 536 | BOM EBM7 |
| `BLM18PG471SN1D` | Activo | 575 844 / 164 993 | BOM EBM7 |
| `GRM32EC72A106ME05L` | Activo | 8 929 D | DigiKey 2026-09-24 |
| `ERA8AEB111V` | Activo | 8 398 D | DigiKey 2026-09-24 |
| `ERA3AEB5621V` | Activo | 19 939 D | DigiKey 2026-09-24 (prazo de fábrica 49 semanas) |
| `ERJ-3EKF1472V` | Activo | 49 140 D | DigiKey 2026-09-24 |
| `RC0603FR-072K2L`, `RC0603FR-073K3L`, `RC0603JR-070RL` | Activos | centenas de milhares | BOM EBM7 |
| `RC1206FR-07100RL` | Activo | 400 218 D | DigiKey 2026-09-24 |
| `NTCS0603E3103JLT` | Activo | 26 370 / 11 185 | BOM EBM7 |
| `M20-7822046`, `M20-7821446` | Activos | 2 598 / 1 297 e 815 / 566 | BOM EBM7 |

D = DigiKey, M = Mouser.

## 3 · Não fechado

- **`ADR4525BRZ`** (tubo): a DigiKey só mostrou explicitamente a versão em bobina
  **`ADR4525BRZ-R7`, «Active» e 0 em stock**; a página da Analog Devices deu erro de ligação duas
  vezes. **Estado do `ADR4525BRZ` por confirmar.** É peça única e crítica (a referência do ADC).
- **11 posições sem MPN** (`C200`, `C202`-`C208`, `C400`, `C402`, `C501`, `R201`-`R206`): fecham na
  BOM preliminar.
- Os números de stock são de datas diferentes e mudam: servem para avaliar risco, não como garantia.

## Fontes

- [DigiKey — KG EELP41.22-PHRH-35-A8J8-20-R18](https://www.digikey.com/en/products/detail/ams-osram-ag/KG-EELP41-22-PHRH-35-A8J8-20-R18/24765242)
- [ams OSRAM — KG EELP41.22 datasheet](https://look.ams-osram.com/m/6d0ff21a355ab5c9/original/KG-EELP41-22.pdf)
- [ams OSRAM — LG Q396 datasheet (Discontinued)](https://look.ams-osram.com/m/357e7fcde66d9629/original/LG-Q396.pdf)
- [Diodes Inc. — BAT46W datasheet DS30044](https://www.diodes.com/datasheet/download/BAT46W.pdf)
- [Vishay — BAT46W datasheet 86406](https://www.vishay.com/docs/86406/bat46w.pdf)
- Pesquisas DigiKey (2026-09-24): `GRM188R71E104KA01D`, `GRM188R71H104KA93D`, `GRM188R72A104KA35D`, `BAT46W-E3-08`, `BAT46W-7-F`, `AL5809-25P1-7`, `MCP3208T-BI/SL`, `MBR1H100SFT3G`, `CC12H250MA-TR`, `ERA-8AEB111V`, `ERA-3AEB5621V`, `ERJ-3EKF1472V`, `GRM32EC72A106ME05L`, `RC1206FR-07100RL`, `ADR4525BRZ-R7`.
