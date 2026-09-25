# Correspondência de referências · EBM2 V5 (renumeração de 2026-09-25)

A partir de 2026-09-25 as referências da EBM2 V5 são **R1, R2, … por ordem hierárquica**, em vez da numeração por
folha (R2xx, R6xx). Nenhuma ligação mudou: `confere_renumeracao.py` compara a netlist de antes e a de depois
(139 componentes, 99 redes, topologia idêntica; valor, pegada e os 126 MPN iguais letra a letra).

## Regra

1. Folhas pela ordem da hierarquia (01 → 07); numeração contínua por prefixo, a começar em 1.
2. Dentro da folha, da esquerda para a direita e, na mesma coluna, de cima para baixo (o sentido do sinal).
3. Folha 06 (seis laços iguais): por função e depois por canal, para que o **canal k seja sempre base + k**:
   `F(2+k)` fusível · `D(11+k)` TVS do terminal · `D(5+k)` TVS do retorno · `U(7+k)` TPS26613 · `C(16+k)` +Vs ·
   `R(9+k)` 0 Ω · `R(15+k)` burden · `R(21+k)` 3k3 · `C(22+k)` filtro · `D(17+k)` BAV199 · `R(27+k)` 4k7.
4. Prefixos: `T` → **`TP`** (T é transformador; TP é o padrão da biblioteca KiCad); NTC → **`TH`** (padrão do
   símbolo `Device:Thermistor_NTC`); `FID101-103` → `FID1-3`. **`P1` e `P2` não mudam** (pinagem congelada da V4.1,
   citada pelo firmware e pela base board).

## Como ler documentos antigos

- A nova numeração nunca passa de dois dígitos (R40 é a maior). **Uma referência de três dígitos (R206, U601) é
  sempre da numeração antiga**: traduzir por esta tabela.
- Relatórios datados, verificações anteriores (`verificacao_2_3*`, `revisao_F2`) e os três relatórios da verificação
  cruzada do Portão 1 ficam **como foram escritos** (registo histórico), com a numeração antiga.
- Referências de outras placas levam sempre o nome da placa colado: `V4.1 R26`, `Legacy U12`, `EBM7 U8`. Sem
  nome de placa, a referência é da EBM2 V5.
- Peças que já saíram do projecto mantêm o nome antigo nos textos (ex.: `C208`, retirado na rev. 2.5).

## Tabela

### 01_conectores

| Antiga | Nova | Símbolo |
|---|---|---|
| `P1` | **`P1`** | `Connector_Generic:Conn_01x20` |
| `P2` | **`P2`** | `Connector_Generic:Conn_01x14` |
| `FID101` | **`FID1`** | `Mechanical:Fiducial` |
| `FID102` | **`FID2`** | `Mechanical:Fiducial` |
| `FID103` | **`FID3`** | `Mechanical:Fiducial` |

### 02_entrada

| Antiga | Nova | Símbolo |
|---|---|---|
| `R207` | **`R1`** | `Device:R` |
| `D203` | **`D1`** | `Device:LED` |
| `D200` | **`D2`** | `Device:D_Zener` |
| `T201` | **`TP1`** | `Connector:TestPoint` |
| `F201` | **`F1`** | `Device:Fuse` |
| `F202` | **`F2`** | `Device:Fuse` |
| `T202` | **`TP2`** | `Connector:TestPoint` |
| `R200` | **`R2`** | `Device:R` |
| `D201` | **`D3`** | `Device:D_Schottky` |
| `D202` | **`D4`** | `Device:D_Schottky` |
| `R206` | **`R3`** | `Device:R` |
| `C200` | **`C1`** | `Device:C` |
| `C201` | **`C2`** | `Device:C` |
| `T207` | **`TP3`** | `Connector:TestPoint` |
| `T206` | **`TP4`** | `Connector:TestPoint` |

### 03_alimentacao

| Antiga | Nova | Símbolo |
|---|---|---|
| `R208` | **`R4`** | `Device:R` |
| `D204` | **`D5`** | `Device:LED` |
| `C206` | **`C3`** | `Device:C` |
| `U200` | **`U1`** | `EBM7_V23_proyecto9:TPS7A4001DGN` |
| `U202` | **`U2`** | `EBM7_V23_proyecto10:ADR4525BRZ` |
| `R201` | **`R5`** | `Device:R` |
| `R202` | **`R6`** | `Device:R` |
| `C202` | **`C4`** | `Device:C` |
| `C207` | **`C5`** | `Device:C` |
| `T205` | **`TP5`** | `Connector:TestPoint` |
| `C203` | **`C6`** | `Device:C` |
| `C209` | **`C7`** | `Device:C` |
| `T203` | **`TP6`** | `Connector:TestPoint` |
| `R203` | **`R7`** | `Device:R` |
| `R204` | **`R8`** | `Device:R` |
| `R205` | **`R9`** | `Device:R` |
| `U203` | **`U3`** | `Reference_Voltage:TL431DBZ` |
| `U201` | **`U4`** | `EBM2_V5:MCP1824T-3302E_OT` |
| `T204` | **`TP7`** | `Connector:TestPoint` |
| `C204` | **`C8`** | `Device:C` |
| `C205` | **`C9`** | `Device:C` |

### 04_barreira

| Antiga | Nova | Símbolo |
|---|---|---|
| `C400` | **`C10`** | `Device:C` |
| `T400` | **`TP8`** | `Connector:TestPoint` |
| `U401` | **`U5`** | `EBM2_V5:MCP1824ST-3302E` |
| `C402` | **`C11`** | `Device:C` |
| `C401` | **`C12`** | `Device:C` |
| `U400` | **`U6`** | `EBM7_V23_proyecto4:ISO7141CC` |
| `C403` | **`C13`** | `Device:C` |
| `FB400` | **`FB1`** | `Device:L_Ferrite` |

### 05_adc

| Antiga | Nova | Símbolo |
|---|---|---|
| `C500` | **`C14`** | `Device:C` |
| `U500` | **`U7`** | `Analog_ADC:MCP3208` |
| `C501` | **`C15`** | `Device:C` |
| `FB500` | **`FB2`** | `Device:L_Ferrite` |
| `C502` | **`C16`** | `Device:C` |
| `T500` | **`TP9`** | `Connector:TestPoint` |

### 06_lacos

| Antiga | Nova | Símbolo |
|---|---|---|
| `D601` | **`D6`** | `Device:D_Zener` |
| `D602` | **`D7`** | `Device:D_Zener` |
| `D603` | **`D8`** | `Device:D_Zener` |
| `D604` | **`D9`** | `Device:D_Zener` |
| `D605` | **`D10`** | `Device:D_Zener` |
| `D606` | **`D11`** | `Device:D_Zener` |
| `F601` | **`F3`** | `Device:Fuse` |
| `F602` | **`F4`** | `Device:Fuse` |
| `F603` | **`F5`** | `Device:Fuse` |
| `F604` | **`F6`** | `Device:Fuse` |
| `F605` | **`F7`** | `Device:Fuse` |
| `F606` | **`F8`** | `Device:Fuse` |
| `D611` | **`D12`** | `Device:D_Zener` |
| `D612` | **`D13`** | `Device:D_Zener` |
| `D613` | **`D14`** | `Device:D_Zener` |
| `D614` | **`D15`** | `Device:D_Zener` |
| `D615` | **`D16`** | `Device:D_Zener` |
| `D616` | **`D17`** | `Device:D_Zener` |
| `U601` | **`U8`** | `EBM7_V23_proyecto7:TPS26613DDFR` |
| `U602` | **`U9`** | `EBM7_V23_proyecto7:TPS26613DDFR` |
| `U603` | **`U10`** | `EBM7_V23_proyecto7:TPS26613DDFR` |
| `U604` | **`U11`** | `EBM7_V23_proyecto7:TPS26613DDFR` |
| `U605` | **`U12`** | `EBM7_V23_proyecto7:TPS26613DDFR` |
| `U606` | **`U13`** | `EBM7_V23_proyecto7:TPS26613DDFR` |
| `C611` | **`C17`** | `Device:C` |
| `C612` | **`C18`** | `Device:C` |
| `C613` | **`C19`** | `Device:C` |
| `C614` | **`C20`** | `Device:C` |
| `C615` | **`C21`** | `Device:C` |
| `C616` | **`C22`** | `Device:C` |
| `R601` | **`R10`** | `Device:R` |
| `R602` | **`R11`** | `Device:R` |
| `R603` | **`R12`** | `Device:R` |
| `R604` | **`R13`** | `Device:R` |
| `R605` | **`R14`** | `Device:R` |
| `R606` | **`R15`** | `Device:R` |
| `R611` | **`R16`** | `Device:R` |
| `R612` | **`R17`** | `Device:R` |
| `R613` | **`R18`** | `Device:R` |
| `R614` | **`R19`** | `Device:R` |
| `R615` | **`R20`** | `Device:R` |
| `R616` | **`R21`** | `Device:R` |
| `R621` | **`R22`** | `Device:R` |
| `R622` | **`R23`** | `Device:R` |
| `R623` | **`R24`** | `Device:R` |
| `R624` | **`R25`** | `Device:R` |
| `R625` | **`R26`** | `Device:R` |
| `R626` | **`R27`** | `Device:R` |
| `C601` | **`C23`** | `Device:C` |
| `C602` | **`C24`** | `Device:C` |
| `C603` | **`C25`** | `Device:C` |
| `C604` | **`C26`** | `Device:C` |
| `C605` | **`C27`** | `Device:C` |
| `C606` | **`C28`** | `Device:C` |
| `D621` | **`D18`** | `EBM7_V23_proyecto3:BAV199` |
| `D622` | **`D19`** | `EBM7_V23_proyecto3:BAV199` |
| `D623` | **`D20`** | `EBM7_V23_proyecto3:BAV199` |
| `D624` | **`D21`** | `EBM7_V23_proyecto3:BAV199` |
| `D625` | **`D22`** | `EBM7_V23_proyecto3:BAV199` |
| `D626` | **`D23`** | `EBM7_V23_proyecto3:BAV199` |
| `R661` | **`R28`** | `Device:R` |
| `R662` | **`R29`** | `Device:R` |
| `R663` | **`R30`** | `Device:R` |
| `R664` | **`R31`** | `Device:R` |
| `R665` | **`R32`** | `Device:R` |
| `R666` | **`R33`** | `Device:R` |
| `R630` | **`R34`** | `Device:R` |
| `D630` | **`D24`** | `Device:LED` |
| `C641` | **`C29`** | `Device:C` |
| `C640` | **`C30`** | `Device:C` |
| `U640` | **`U14`** | `EBM7_V23_proyecto9:TPS7A4001DGN` |
| `R641` | **`R35`** | `Device:R` |
| `R642` | **`R36`** | `Device:R` |
| `C642` | **`C31`** | `Device:C` |
| `C644` | **`C32`** | `Device:C` |
| `T640` | **`TP10`** | `Connector:TestPoint` |
| `C645` | **`C33`** | `Device:C` |
| `R643` | **`R37`** | `Device:R` |
| `R644` | **`R38`** | `Device:R` |
| `R645` | **`R39`** | `Device:R` |
| `C643` | **`C34`** | `Device:C` |

### 07_ntc

| Antiga | Nova | Símbolo |
|---|---|---|
| `R700` | **`TH1`** | `Device:Thermistor_NTC` |
| `R701` | **`R40`** | `Device:R` |
| `C700` | **`C35`** | `Device:C` |

Gerada por `ferramentas/renumera_referencias.py`; CSV para máquina: `tabela_correspondencia_refs_EBM2_V5.csv`.
