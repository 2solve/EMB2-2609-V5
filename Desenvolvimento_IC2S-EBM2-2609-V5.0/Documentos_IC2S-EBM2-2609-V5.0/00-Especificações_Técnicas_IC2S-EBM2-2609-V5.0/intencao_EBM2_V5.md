# Documento de intenção — IC2S Extension Board EBM2 V5 (6AI)

| | |
|---|---|
| Projecto | IC2S Extension Board EBM2, 6 entradas 4-20 mA |
| Revisão do documento | **2** — reescrita em 2026-09-23 depois da F0, da F1 e do datasheet do `MCP3208`. **Rev. 2.4 (2026-09-24): limitador `AL5809` → `TPS26613`, copiado da EBM7 V2.3 Legacy (§9)**. **Rev. 2.5 (2026-09-24): correcções da 2.3b rev. 2.4 (§17)** |
| Fase | F2, etapa 2.2a |
| Autoridade | **Este documento manda até ao primeiro ERC limpo.** A partir daí manda o `.kicad_sch` e este texto congela como registo de intenção. O ERC ainda não está limpo: faltam as folhas 01, 04, 05, 06 e 07 |
| Base | `planejamento_pcb_EBM2_V5.md` rev. 3 e a V4.1 convertida e auditada, copiada antes de inventar |
| Histórico | A revisão 1 está em `intencao_EBM2_V5_rev1_historico.md`. Ficou superada em oito pontos |

> ## ✅ APROVADO pelo projectista em 2026-09-23
>
> Javier Rivadineira aprovou esta revisão 2 em 2026-09-23 («documento aprobado»).
> A aprovação cobre a especificação das folhas 01, 04, 05, 06 e 07, a proposta de
> LED da §11 e o diagrama de blocos da etapa 2.1. **Não cobre**, porque são
> decisões à parte e continuam abertas: a `V8` (transmissor em curto, antes do
> Portão 1) e o critério `RE1` (pior caso ou típico, Portão 0). A 2.2b desenha-se
> com o que está especificado; se a `V8` pedir peças novas, entram depois.

> **Para o projectista rever antes de se desenhar qualquer folha nova.** A
> skill exige esta aprovação entre a 2.2a e a 2.2b. As folhas 02 e 03 já estão
> desenhadas e verificadas; as secções delas descrevem o que está no CAD. As
> folhas 01, 04, 05, 06 e 07 **ainda não existem**, e é sobre elas que esta
> revisão pede aprovação.

---

## 1 · O que este documento decide, em poucas linhas

1. **O mapa de canais do conversor fica congelado como na V4.1**: campo em
   `CH0`-`CH3`, `CH6` e `CH7`; `CH4` é o termístor; `CH5` fica preso ao trilho.
2. **O 5 V do barramento chama-se `+5V` e o 5 V de campo chama-se `+5V_ADC`**,
   como na V4.1. Já se corrigiu a folha 03, que chamava `+5V` ao trilho de
   campo: se a folha 01 tivesse um porto `+5V`, as duas redes fundiam-se e a
   barreira ficava anulada sem mensagem de erro nenhuma.
3. **O isolador passa a ter `VCC1` a 3,3 V** por um `MCP1824S`, que fecha o gap
   `G2`: o pino `MISO` deixa de levar 5 V à Raspberry Pi.
4. **O termístor ganha um condensador de 100 nF no pino**, que a V4.1 não tinha.
   Sem ele, a figura 4-2 do `DS21298E` põe o canal fora de especificação a
   1 MHz de relógio.
5. **Duas verificações novas que não são pormenor**: com os 24 V sem isolamento
   e sem limite de corrente, um transmissor em curto deixa passar ~64 mA
   sustentados, que o fusível de 50 mA não abre e que queimam a resistência
   série de 249 Ω. ~~É uma regressão face à V4.1~~ **Correcção de 2026-09-23: não é
   regressão.** O `PDM2-S24-S24-S` da V4.1 só aguenta curto durante 1 s e não tem
   protecção de sobrecarga (datasheet CUI); a V4.1 fazia passar ~65 mA no mesmo caso.
   O defeito é herdado e precisa de decisão (`V8`); proposta no
   `Relatorio_Melhorias_Isolamento_V8_RE1_2026-09-23.md`.
   E a tensão que sobra ao transmissor a 20 V de entrada é ~11 V (`V9`).

## 2 · Estrutura de folhas e designadores

| Folha | Bloco | Designadores (desde 2026-09-25) |
|---|---|---|
| 01 | Conectores `P1`, `P2`, fiduciais | `P1`, `P2`, `FID1`-`FID3` |
| 02 | Entrada de 24 V e protecção | `R1`-`R3`, `C1`-`C2`, `D1`-`D4`, `F1`-`F2`, `TP1`-`TP4` |
| 03 | Alimentação | `R4`-`R9`, `C3`-`C9`, `D5`, `U1`-`U4`, `TP5`-`TP7` |
| 04 | Barreira: `ISO7141` e o seu LDO | `C10`-`C13`, `U5`-`U6`, `FB1`, `TP8` |
| 05 | Conversor `MCP3208` | `C14`-`C16`, `U7`, `FB2`, `TP9` |
| 06 | Seis laços 4-20 mA | `F3`-`F8`, `D6`-`D24`, `U8`-`U14`, `C17`-`C34`, `R10`-`R39`, `TP10` |
| 07 | Termístor da placa | `TH1`, `R40`, `C35` |

**Regra de designador (renumeração de 2026-09-25, a pedido do projectista)**: prefixo mais número, sem
sufixos de letra, **R1, R2, … por ordem hierárquica** — folhas 01 → 07 e, dentro da folha, da esquerda para a
direita e de cima para baixo. Na folha 06, por função e depois por canal: o canal k de cada função é sempre
base + k (`U(7+k)`, `R(15+k)`, …). `TP` para pontos de prova, `TH` para o termístor. A numeração por
centenas (R2xx, R6xx) que valeu até 2026-09-25 traduz-se por `tabela_correspondencia_refs_EBM2_V5.md`; a
topologia foi conferida nó a nó antes e depois (`confere_renumeracao.py`). **Referências de outras placas
levam sempre o nome da placa colado** (`V4.1 R26`, `Legacy U12`); sem nome de placa, são da EBM2 V5.

### Correspondência V4.1 → V5 das peças herdadas

A comparação final nó a nó contra a V4.1 é por topologia, não por nome. Esta
tabela é o que permite lê-la.

| Função | V4.1 | V5 |
|---|---|---|
| Isolador | `U4` | `U6` |
| Conversor | `U5` | `U7` |
| LDO 3,3 V | `U11` | `U4` |
| Ferrite do `VCC2` do isolador | `FB2` | `FB1` |
| Ferrite do `VDD` do conversor | `FB3` | `FB2` |
| Desacoplamento `VCC1` / `VCC2` | `C7` / `C8` | `C12` / `C13` |
| Desacoplamento `VDD` do conversor | `C10` | `C16`, mais `C15` novo |
| Termístor e o seu divisor | `R5` / `R8` | `TH1` / `R40` |
| Pull-up do `EN` do SPX3819 | `R34` | `R7` |
| Canais 1 a 6: fusível | `F1`-`F6` | `F3`-`F8` |
| Canais 1 a 6: TVS no retorno | `D4`,`D7`,`D13`,`D22`,`D2`,`D12` | `D6`-`D11` |
| Canais 1 a 6: TVS no trilho | `D3`,`D6`,`D10`,`D1`,`D11`,`D21` | `D12`-`D17` |
| Canais 1 a 6: série 249 Ω | `R6`,`R11`,`R18`,`R15`,`R1`,`R4` | `R10`-`R15` |
| Canais 1 a 6: burden | `R9`,`R13`,`R21`,`R17`,`R3`,`R14` | `R16`-`R21` |
| Canais 1 a 6: antialias 3,3 kΩ | `R7`,`R12`,`R19`,`R16`,`R2`,`R10` | `R22`-`R27` |
| Canais 1 a 6: condensador do filtro | `C9`,`C13`,`C18`,`C3`,`C1`,`C2` | `C23`-`C28` |
| Canais 1 a 6: clamp | `D5`,`D8`,`D14`,`D23`,`D9`,`D20` | `D18`-`D23` |
| LED | `D18` / `D19` / `D25` | `D5` / `D24` / `D1` |
| Resistência do LED | `R24` / `R25` / `R26` | `R4` / `R34` / `R1` |

**Saem da V4.1, e é essa a revisão**: os conversores isolados `U1`, `U7`, `U8`;
os díodos `D15`, `D16`, `D24`, `D17` e o zener em série `D26`; os fusíveis `F7`,
`F8`, `F9`; os electrolíticos `C12`, `C28`; a ferrite `FB4`; e os condensadores
que só serviam os conversores. O que os substitui está nas folhas 02 e 03.

## 3 · Trilhos e domínios

| Rede | Domínio | Origem | Quem a usa |
|---|---|---|---|
| `+24V` | campo, sem isolamento | `P1.20` | folha 02 |
| `GND_24V` | campo | `P1.19` | folha 02, unida a `GND_ADC` por `R2` |
| `+24V_ADC` | campo | `F2` → `D4` | folha 06, laços |
| `+24V_REG` | campo | `F1` → `D3` → `R3` | folha 03 |
| `+5V_ADC` | campo | `TPS7A4001` | folha 03 |
| `+12V_TPS` | campo | `U14` `TPS7A4001` a partir de `+24V_ADC` (**rev. 2.4**) | folha 06, `+Vs` dos `U8`-`U13` |
| `3V3_REF` | campo | `SPX3819`, grampo `TL431` | folhas 03, 04 (`VCC2`), 05, 06 (clamps) |
| `+2V5_REF` | campo | `ADR4525` | folhas 05 (`VREF`) e 07 (topo do divisor) |
| `GND_ADC` | campo | — | todas as de campo |
| `+5V` | **barramento** | `P1.17` | folha 04, entrada do `MCP1824S` |
| `+3.3V_DIG` | **barramento** | `MCP1824S` | folha 04, `VCC1` e `EN1` do isolador |
| `DGND` | **barramento** | `P1.3`, `P1.12`, `P1.16` | folha 04 |

**Só o `ISO7141` atravessa a barreira.** Nenhuma rede do barramento pode ter
pinos do lado de campo, nem o contrário. Depois de desenhar as folhas 01 e 04,
isso confere-se na netlist: nenhuma rede pode conter pinos de `DGND` e de
`GND_ADC` ao mesmo tempo, nem os dois lados do isolador.

## 4 · Folha 01 — conectores

### Ligações, como especificação

`P1` é o `Harwin M20-7822046`, 20 pinos, pegada `HDR1X20_FEMALE`. `P2` é o
`M20-7821446`, 14 pinos, `HDR1X14_FEMALE`. **A pinagem das duas está congelada
por `RC2` e copia-se da V4.1 pino a pino.**

| `P1` | Rede | Nota |
|---|---|---|
| 1, 2 | não ligado | `USB1`, `USB2` do barramento: esta placa não os usa |
| 3, 12, 16 | `DGND` | |
| 4 | `MOSI` | para o isolador, folha 04 |
| 5 | `CLK` | idem |
| 6 | `MISO` | do isolador |
| 7, 8 | não ligado | `CS_DAC`, `LDAC_DAC`: não há DAC nesta placa |
| 9 | `CS_ADC` | para o isolador, activo baixo |
| 10 | não ligado | `CS4` |
| 11, 13 | **não ligado, e tem de continuar assim** | `ID1`, `ID3`: ver abaixo |
| 14, 15 | não ligado | `SDA`, `SCL` |
| 17 | `+5V` | barramento, para o `MCP1824S` |
| 18 | não ligado | não existe na V4.1 |
| 19 | `GND_24V` | |
| 20 | `+24V` | |

| `P2` | Rede | Nota |
|---|---|---|
| 1 | não ligado | como na V4.1 |
| 2, 4, 6, 8, 10, 12 | `LOOP1_V+` … `LOOP6_V+` | alimentação de cada laço, saída do seu fusível na folha 06 |
| 3, 5, 7, 9, 11, 13 | `AIN1-` … `AIN6-` | retorno de cada laço, para a folha 06 |
| 14 | `GND_ADC` | |

As redes de sinal saem da folha por rótulo hierárquico. Os trilhos saem por
porto global com o nome exacto da tabela da §3.

### Porquê

- **Os pinos não usados levam no-connect explícito**, com a função do barramento
  escrita numa nota ao lado. Na V4.1 levavam rótulos soltos de um só pino; um
  no-connect diz o mesmo sem deixar ao ERC a dúvida de ser um fio esquecido.
- **`ID1` e `ID3` ficam desligados porque são, muito provavelmente, a identidade
  da placa perante a base board.** Na V4.1 estão desligados; se a V5 os ligasse,
  o firmware poderia deixar de a reconhecer, e isso parte `RC4`. `[EST]`: a
  função dos pinos ID não está documentada nos projectos da base board que se
  estudaram, por isso a regra é a mais segura — copiar o original.
- **`PWR_FLAG` em `+24V` e `GND_24V` é legítimo aqui**: o conector é uma fonte
  real e passiva. É isto que fecha os dois erros estruturais de ERC que ficaram
  pendentes desde a folha 02.

### DFT

Três fiduciais `FID1`-`FID3`, pegada `Fiducial_Point_Top-Bot`, como na
Legacy. São símbolos sem rede; vivem nesta folha porque são mecânicos.

## 5 · Folha 02 — entrada de 24 V *(desenhada)*

Está no CAD e verificada: netlist conferida nó a nó, ERC, zero sobreposições no
PDF. O dimensionamento completo está em `planejamento_pcb_EBM2_V5.md` §2.6 e nas
notas da própria folha. Resumo das ligações:

`+24V` → `TP1` e TVS `D2` a `GND_24V`. Dois ramos: `F2` → `D4` →
`+24V_ADC` com `C2` 10 µF/100 V; e `F1` → `D3` → `+24V_DIO_REG` → `R3`
~~22 Ω~~ ~~33 Ω (rev. 2.2)~~ ~~68 Ω (rev. 2.5)~~ **150 Ω (rev. 2.5c; §17 linhas 1 e 1c)**, KOA `SG73P2ATTD1500F` → `+24V_REG` com `C1` 2,2 µF/100 V (TDK `C3225X7R2A225K230AB`, 1210). `GND_24V` → `R2` 0 Ω → `GND_ADC`.

**Acrescenta-se nesta folha**, por DFT e por LED (§11):

| Peça | Ligação | Porquê |
|---|---|---|
| `TP4` | ponto de prova em `+24V_ADC` | `RD1` pede-o e ainda não existe |
| `TP3` | ponto de prova em `+24V_REG` | idem |
| `D1` + `R1` 14,7 kΩ | LED de `+24V` a `GND_24V` | substitui `D25`; diz que há entrada |

**Desenhado em 2026-09-23** (`ferramentas/aplica_leds_tps_F2.py`): netlist idêntica ao diff
declarado (4 peças, 6 pinos). MPN `R1` = `ERJ-3EKF1472V` e LED `LG Q396-PS-35`, os da V4.1.

## 6 · Folha 03 — alimentação *(desenhada)*

Está no CAD, redesenhada em 2026-09-23 porque a primeira versão tinha dezenas de
textos encimados que nunca se tinham medido no PDF. Netlist conferida idêntica
antes e depois do redesenho. Ligações:

`+24V_REG` → `TPS7A4001` (`IN` e `EN` juntos) → `+5V_ADC` 4,974 V pelo divisor
32k4/10k → `SPX3819` (`EN` por `R7` 100 kΩ, `BP` com `C208` 10 nF) →
`3V3_REF` → `ADR4525` → `+2V5_REF`. `TL431` com `R8`/`R9` grampeia
`3V3_REF` a 3,60 V: é o sumidouro dos clamps de campo.

**Acrescenta-se nesta folha**: `D5` + `R4` 2,2 kΩ, LED de `+5V_ADC` a
`GND_ADC`, que substitui `D18` (§11).

**Desenhado em 2026-09-23**: netlist idêntica ao diff declarado (2 peças, 4 pinos).
MPN `R4` = `RC0603FR-072K2L`, o da V4.1 (`R24`).

## 7 · Folha 04 — barreira

### Ligações, como especificação

**Isolador `U6`, `ISO7141CCDBQR`**, pegada `SSOP16-4.9x3.9mm`. Pinagem
`[HERDADO]` da V4.1 auditada, a conferir contra o datasheet na etapa 2.3:

| Pino | Função | Lado | Rede |
|---|---|---|---|
| 1 | `VCC1` | barramento | `+3.3V_DIG` |
| 2, 8 | `GND1` | barramento | `DGND` |
| 3 | `INA` | barramento | `MOSI` |
| 4 | `INB` | barramento | `CLK` |
| 5 | `INC` | barramento | `CS_ADC` |
| 6 | `OUTD` | barramento | `MISO` |
| 7 | `EN1` | barramento | `+3.3V_DIG` |
| 9, 15 | `GND2` | campo | `GND_ADC` |
| 10 | `EN2` | campo | `VCC2_ISO` |
| 11 | `IND` | campo | `MISO_ADC_ISO` |
| 12 | `OUTC` | campo | `CS_ADC_ISO` |
| 13 | `OUTB` | campo | `CLK_ADC_ISO` |
| 14 | `OUTA` | campo | `MOSI_ADC_ISO` |
| 16 | `VCC2` | campo | `VCC2_ISO` |

`VCC2_ISO` vem de `3V3_REF` pela ferrite `FB1` (`BLM18PG471SN1D`), como na
V4.1, com `C13` 100 nF a `GND_ADC` no pino. `VCC1` leva `C12` 100 nF a `DGND`
no pino.

**LDO `U5`, `MCP1824ST-3302E/DB`**, pegada SOT-223-3 copiada da Legacy.
Pinagem lida na **figura** da pág. 2 do `DS22070A`: 1 `VIN`, 2 `GND`, 3 `VOUT`,
4 (patilha) `GND`. `VIN` em `+5V` com `C10` 1 µF a `DGND`; `VOUT` forma
`+3.3V_DIG` com `C11` 1 µF a `DGND`.

`TP8`, ponto de prova em `DGND`, **deste lado da barreira**.

A barreira desenha-se como linha tracejada vertical que atravessa o `U6`, com
o texto «BARREIRA FUNCIONAL — DGND | GND_ADC». Nenhum fio a cruza.

### Porquê

- **`VCC1` a 3,3 V e não a 5 V fecha o `G2`.** Com `VCC1` a 5 V, o `OUTD` põe
  ~4,9 V no `GPIO9` da Raspberry Pi, e o clamp da base board a +3,3V_IC deixa-o
  em ~4,0 V, acima do máximo da Pi, sem resistência série. A 3,3 V o problema
  desaparece na origem. As entradas continuam a ser atacadas pela Pi a 3,3 V.
- **Não há pino de enable no `MCP1824S`**: o S de SOT-223-3 não tem `SHDN`.
  O «EN1» do planeamento é o pino de enable do isolador, ligado ao seu `VCC1`.
- **`VCC2` fica pela ferrite a partir de `3V3_REF`**, como na V4.1: é a única
  carga digital do lado de campo e a ferrite impede que o seu ruído de comutação
  chegue ao trilho da referência.

### Dimensionamento

- `MCP1824S`: entrada 2,1-6,0 V (pág. 1), portanto os 5 V do barramento cabem
  com folga de 1 V. Estável com 1,0 µF cerâmico à saída (pág. 1). Carga: o lado 1
  do isolador, alguns mA contra 300 mA de capacidade.
- Desacoplamento do isolador: 100 nF por lado, no pino, como na V4.1. A nota de
  layout do datasheet do isolador confere-se na etapa 2.3b.

### Lógica activa

`CS_ADC` activo baixo. `EN1` e `EN2` presos a alto: o isolador está sempre
activo. Modo SPI 0,0 ou 1,1 (`DS21298E` §6.1).

## 8 · Folha 05 — conversor

### Ligações, como especificação

**`U7`, `MCP3208T-BI/SL`**, SOIC-16. Pinagem lida na figura da pág. 1 do
`DS21298E`:

| Pino | Função | Rede |
|---|---|---|
| 1 | `CH0` | `AIN1_ADC` |
| 2 | `CH1` | `AIN2_ADC` |
| 3 | `CH2` | `AIN3_ADC` |
| 4 | `CH3` | `AIN4_ADC` |
| 5 | `CH4` | `NTC_ADC` |
| 6 | `CH5` | `3V3_REF`, antes da ferrite, como na V4.1 |
| 7 | `CH6` | `AIN5_ADC` |
| 8 | `CH7` | `AIN6_ADC` |
| 9 | `DGND` | `GND_ADC` |
| 10 | `CS/SHDN` | `CS_ADC_ISO` |
| 11 | `DIN` | `MOSI_ADC_ISO` |
| 12 | `DOUT` | `MISO_ADC_ISO` |
| 13 | `CLK` | `CLK_ADC_ISO` |
| 14 | `AGND` | `GND_ADC` |
| 15 | `VREF` | `+2V5_REF`, com `C14` 100 nF no pino |
| 16 | `VDD` | `VDD_ADC`, de `3V3_REF` pela ferrite `FB2` |

`VDD_ADC` leva `C15` 1 µF **e** `C16` 100 nF a `GND_ADC`, os dois no pino.
`TP9`, ponto de prova em `GND_ADC`.

### Porquê

- **O mapa de canais não é sequencial e fica congelado** (`RC4`). Pôr os seis
  canais em sequência faria o firmware ler o termístor como canal 5 e um valor
  saturado como canal 6, sem erro nenhum.
- **`CH5` preso a `3V3_REF` lê sempre 4095.** Não traz informação, mas o firmware
  existente pode verificá-lo; mudá-lo arriscaria `RC4`. Fica como está.
- **1 µF no `VDD` e não 100 nF**: é o que a §6.4, pág. 23, recomenda. A V4.1 tinha
  só 100 nF.
- **100 nF no pino de `VREF`** para o desacoplamento de alta frequência junto ao
  conversor. O 1 µF da figura 6-3 já existe como `C5`, à saída do `ADR4525`.
- **`AGND` e `DGND` são pinos distintos e vão os dois a `GND_ADC`**, com
  percursos próprios no layout.

### Restrições que o firmware tem de cumprir

1. Relógio SPI **≤ 1 MHz**: os 2 MHz só estão garantidos a `VDD` = 5 V.
2. Transacção de 24 bits **atómica** por canal: a 85 °C a carga do condensador de
   amostra só se garante 1,2 ms depois da amostragem (§6.2). Partida pelo
   escalonador do Linux, dá erro de linearidade sem aviso.
3. Cadência por canal **abaixo de 4 kHz**, para os 3,3 kΩ custarem menos de 1 LSB.
4. **Estado real (Rodrigo, 2026-09-24):** SPI a **20 kHz**. Os 12-13 bits levam ~0,65 ms, dentro
   dos 1,2 ms da §6.2 (relógio efectivo mínimo de 10 kHz), com margem de ~1,8×: **não baixar mais**.
   A amostragem dura 1,5 ciclos = 75 µs, bem acima do que a fig. 4-2 pede para a fonte de 3,3 kΩ.
5. **O CH4 (NTC) e o CH5 não são lidos pelo software actual.** O divisor do termístor (`TH1`,
   `R40`, `C35`) fica montado: são três peças baratas, mantêm o mapa de canais da V4.1 e deixam a
   compensação de temperatura possível no futuro. **Não se justifica nenhuma decisão de projecto
   com «o firmware lê o NTC».**
6. **Satura em silêncio acima de 20 mA.** ~~Com o limitador (`V8`), um transmissor em curto dá o
   código 4095 (~22,7 mA).~~ **Rev. 2.4 (TPS26613): em curto a leitura alterna** ~100 ms a 4095
   (25-40 mA) e ~800 ms a ~0 mA (FET desligado, novo arranque; SLVSFE3C tabela 8-3). Com a média de
   10 amostras / 500 ms o painel vê sobretudo `"null"`. Pedido ao firmware: tratar 4095 **e** um `"null"`
   intermitente com picos a 4095 como falha (curto ou alarme alto NE43), não como laço aberto. Ver
   `mapa_pinos_EBM2_V5.md`, secção do firmware.

> **Resposta do firmware (Rodrigo, 2026-09-24), tirada do código do DeviceManager.** Na EBM2 não
> há firmware à parte: o backend Node (`extensions/EBM2.js`, `extensions/expander.js`) lê o ADC.
> - **Calibração por canal, no campo, em 6 pontos** (0, 4, 8, 12, 16, 20 mA), pela tela
>   Settings → mapa → Calibrar: 5 trechos lineares, ganho e offset por trecho, guardados no MongoDB
>   **ligados à variável, não à placa**. Sem calibração não há conversão para mA.
> - **Ao trocar a placa a calibração antiga continua aplicada** e nada obriga a recalibrar.
> - SPI a **20 kHz** fixos; média móvel de 10 amostras a cada 500 ms; a captura da calibração usa
>   **uma amostra instantânea**.
> - **CH4 (NTC) e CH5 não são lidos.** AI1-AI6 = CH0, CH1, CH2, CH3, CH6, CH7.
> - Acima de 20 mA não há limite nem aviso (satura em silêncio); abaixo de 3,6 mA a variável vira
>   `"null"` (laço aberto), **só com o canal calibrado**.

## 9 · Folha 06 — seis laços

### Ligações, como especificação

Por canal *k*, de 1 a 6. Exemplo do canal 1:

`+24V_ADC` → fusível `F3` → `LOOP1_V+`, que vai ao pino 2 de `P2` e alimenta o
transmissor. O retorno chega por `AIN1-`, pino 3 de `P2`. Desse nó sai o TVS
`D6` (cátodo no nó, ânodo a `GND_ADC`) e o **protector de laço `U8` `TPS26613DDFR`**
(**rev. 2.4**, como a EBM7 V2.3 Legacy `U8`-`U11`): pino 4 `IN` no nó `AIN1-`, pino 5 `OUT` em
`AIN1_LIM`, pino 6 `+Vs` em `+12V_TPS` com `C17` 100 nF, pino 7 `VSNS` na rede `VSNS`, pinos
1 `GND`, 2 `MODE` e 3 `−Vs` a `GND_ADC`, pino 8 `SGOOD` sem ligação. ~~`AL5809` e `BAT46W`
antiparalelo~~ saem. De `AIN1_LIM` sai `R10`, **0 Ω 0603** (a posição do Legacy `R10`). O
outro terminal de `R10` é o nó de medida: burden `R16` 110 Ω a `GND_ADC` e antialias `R22`
3,3 kΩ. O outro terminal de `R22` forma o nó do filtro `AIN1_FILT`, com `C23` 100 nF a
`GND_ADC` e o clamp `D18` `BAV199`: pino 3 no sinal, pino 1 a `GND_ADC`, pino 2
a `3V3_REF` (figura da pág. 1 do `BAV199LT1/D`). **Rev. 2.5:** de `AIN1_FILT` ao pino do conversor vai a série
`R28` 4k7, e o pino é `AIN1_ADC`: em clamp, limita a corrente ao díodo interno do `MCP3208` a ~30 µA (§17). O TVS `D12` fica entre
~~`+24V_ADC`~~ **`LOOP1_V+`, depois do fusível `F3`, no lado do terminal** (rev. 2.3), e `GND_ADC`.

| Canal | Alimentação | Retorno | Rede no ADC | Canal ADC |
|---|---|---|---|---|
| 1 | `P2.2` | `P2.3` | `AIN1_ADC` | `CH0` |
| 2 | `P2.4` | `P2.5` | `AIN2_ADC` | `CH1` |
| 3 | `P2.6` | `P2.7` | `AIN3_ADC` | `CH2` |
| 4 | `P2.8` | `P2.9` | `AIN4_ADC` | `CH3` |
| 5 | `P2.10` | `P2.11` | `AIN5_ADC` | `CH6` |
| 6 | `P2.12` | `P2.13` | `AIN6_ADC` | `CH7` |

| Peça | Valor | Part number | Pegada | Origem |
|---|---|---|---|---|
| Fusível | 50 mA | `3413.0002.22` | 1206 | Legacy |
| TVS trilho `D12`-`D17` | ~~30 V~~ **36 V** | ~~`824500301`~~ **`824520361`** (SMBJ36A, 600 W) | **DO-214AA** | **rev. 2.2**: a 32 V o trilho chega a 31,4 V, acima dos 30 V de standoff do anterior. É o da EBM7 |
| TVS retorno `D6`-`D11` | ~~36 V~~ **33 V** | **`SMBJ33A-13-F`** (Diodes, a família do `SMBJ36A-13-F` da Legacy) — **datasheet a conferir no pacote da BOM** | DO-214AA | **rev. 2.4**: ver «Porquê» |
| Protector de laço | 25-40 mA, R_ON 4,8-12,5 Ω | ~~`AL5809-25P1-7`~~ **`TPS26613DDFR`** | **SOT-23-8** (md5 igual à Legacy) | **rev. 2.4**, Legacy `U8`-`U11` |
| Desacoplamento `+Vs` | 100 nF 100 V | `GRM188R72A104KA35D` (`C17`-`C22`) | 0603 | Legacy `C26`/`C29`/`C31`/`C32` |
| ~~Schottky antiparalelo~~ | — | ~~`BAT46W-7-F`~~ | — | **sai na rev. 2.4**: o TPS26613 aguenta ±55 V |
| Série | ~~249 Ω~~ ~~150 Ω~~ ~~100 Ω~~ **0 Ω** | `RC0603JR-070RL` | **0603** | **rev. 2.4**: Legacy `R10`; o curto é do `U8-U13` |
| Burden | 110 Ω 0,1 % 25 ppm | ~~`ERA3AEB111V`~~ **`ERA8AEB111V`** | **1206** | F1 §2.5; **rev. 2.1** |
| Antialias | 3,3 kΩ | `RC0603FR-073K3L` | 0603 | V4.1 |
| Filtro | 100 nF | como V4.1 | 0603 | V4.1 |
| Clamp | — | `BAV199LT1G` | SOT23-3 | Legacy |

`D24` + `R34` 14,7 kΩ: LED de `+24V_ADC` a `GND_ADC`, substitui `D19` (§11).

### Porquê

- **Rev. 2.4 (2026-09-24, decidida pelo projectista): o limitador passa a ser o da EBM7 V2.3
  Legacy, `TPS26613DDFR`** («copiemos como está el EBM7»). A 2.3b reprovou o `AL5809` em três
  linhas (F1 térmica em curto, F2 sempre abaixo dos 2,5 V mínimos, F9 −0,40 V contra −0,3 V).
  Citações do `SLVSFE3C` (TI, rev. C, dez. 2021), na pasta de referências da EBM7:
  - *Curto do transmissor (F1).* `MODE` a `GND`: limita a `I(OL)` 25-40 mA (pág. 5) durante
    `tOL_Expiry` 100 ms, corta, e tenta de novo a cada `tRETRY1` 800 ms (tabela 8-3, pág. 23;
    o `26613` é o de «auto-retry», tabela da pág. 3). No pior caso, a 32 V, com `IN` a
    31,0 V e `OUT` a 40 mA × 110 Ω = 4,4 V, **1,06 W durante 100 ms em cada 900 ms: 0,12 W
    de média, +14 °C** (RθJA 117,8 °C/W, pág. 4). A fig. 7-19 (pág. 12, típica, placa da TI)
    dá, a 85 °C e ~1,05 W, **~200 ms até ao corte térmico** (160 °C): o temporizador de
    100 ms corta antes. Não depende de cobre na F3. **Confirmar no T26.**
  - *Tensão mínima (F2).* Não há: dentro do limite é um interruptor de 4,8-12,5 Ω
    (`RON`, pág. 6). A 20 mA cai **≤ 0,25 V**, contra os 1,6-2,5 V do `AL5809`.
  - *Inversão (F9).* `IN` e `OUT` aguentam ±55 V (pág. 4). Com `−Vs` a `GND`, `OUT` abaixo de
    `−Vs` − 0,2 V corta o FET (`VO_UVLO`, pág. 6, só no 26613/14). **O `BAT46W` sai.**
  - *Alimentação.* Precisa de `+Vs` entre 3 e 30 V (pág. 4) e **acima da tensão de `OUT`**, ou
    corta por `VOUT_OVLO` (`+Vs` + 0,05 V, pág. 5). `OUT` chega a 4,4 V no limite. Copia-se a
    Legacy: **`U14` `TPS7A4001` a 12,09 V** (`R35` 93k1 / `R36` 10k: 1,173 × 10,31) a partir de
    `+24V_ADC`. O `+24V_ADC` não serve: a 32 V fica a 31,4 V, acima dos 30 V recomendados.
    Consumo: 6 × 1,65 mA máx. (pág. 6) + divisores ≈ **10,8 mA**; a 32 V são 0,21 W no `U14`,
    +14 °C (RθJA 66,7 °C/W, SBVS162B pág. 4).
  - *Condensadores do `U14`* (SBVS162B pág. 1 e §8.2.2.2: saída **> 4,7 µF sobre temperatura
    e tolerância**, entrada ≥ 1 µF, recomendados 10 µF). Copiam-se os da Legacy: `C31`
    10 µF 50 V 1206 X5R (`C3216X5R1H106K160AB`, Legacy `C38`; a 12 V a curva da TDK tem de
    dar > 4,7 µF — conferir na BOM) e `C30` 10 µF 100 V 1210 + `C29` 100 nF na entrada
    (Legacy `C35`/`C36`). *A EBM7 V2.3 não Legacy tinha 4,7 µF 25 V 0805: não cumpria.*
  - *`VSNS`* (tabela 8-2, pág. 20). A Legacy tem `R22` 11k5 / `R23`‖`R24` 6k65 → limiar
    descendente 4,46 V. A nota (2) pede-o **acima** de `I_LOOP` × `R_burden`: com `I(OL)` máx.
    40 mA × 110 Ω = 4,40 V, a margem é de 1,4 %, e o `V(SNSF)` de 1 V vem sem mínimo nem
    máximo. **Desvio da Legacy: `R37` 13k3** → limiar descendente **5,0 V** (margem 14 %),
    ascendente 1,72 × 5,0 = **8,6 V** contra `+Vs` mín. 11,8 V; `VSNS` = 2,4 V ≤ 5 V; `R1+R2`
    = 16,6 kΩ ≤ `+Vs`/45 µA = 262 kΩ. `R38`/`R39` 6k65 e `C34` 100 nF, como a Legacy.
  - *`SGOOD` sem ligação*, como na Legacy. **Decisão escrita** (a 2.3b da Legacy pedia-a):
    não há GPIO livre do lado de campo; a falha vê-se na leitura.
  - *`R10` a 0 Ω.* A série de 100 Ω só existia para aguentar o curto sem limitador (V4.1);
    com o limite de 40 mA não protege nada. Fica a ilha, como na Legacy (`R10`). Ganho: +2,0 V
    ao transmissor.
  - *TVS do retorno a 33 V.* `IN` do TPS26613 aguenta **55 V**; o SMBJ36A grampeia a
    **58,1 V** (Würth 824520361, pág. 1). A Legacy usa 30 V (grampo 48,4 V), mas com 30 V de
    standoff os 31,4 V do retorno em curto a 32 V ficam acima (a razão da rev. 2.2). **33 V**:
    standoff 33 V > 31,4 V, grampo 53,3 V a 11,3 A (a classe 33 V do `D2`, Bourns
    SMA6J33A pág. 2) < 55 V. Os `D12`-`D17`, no `LOOPk_V+`, não estão no `IN` e ficam a 36 V.
  - *Comportamento que muda para o firmware.* Em curto a leitura **alterna**: 100 ms a 4095
    (25-40 mA) e 800 ms a ~0 mA (FET desligado → `"null"`). Com a média de 10 amostras em 500
    ms o painel verá sobretudo `"null"`. Avisar o Rodrigo: um `"null"` intermitente com picos a
    4095 é curto, não laço aberto.
  - *Sem `+12V_TPS`* (por exemplo `U14` avariado), o TPS26613 passa ao modo de laço (pág. 20):
    conduz com 5-8,5 V de queda e limita a 22-45,5 mA. A medida continua se o transmissor
    tiver tensão.
- **Topologia copiada da V4.1**, com três valores mudados e já justificados na
  F1: burden 110 Ω, clamp `BAV199`, fusível de 50 mA.
- **Rev. 2.3 (2026-09-23): os seis TVS de laço passam para depois do fusível de canal, no
  terminal `LOOPk_V+`** — como na EBM7 Legacy (`D9`/`D10`/`D12`/`D13` em `+24V_AINk`). Um TVS em
  curto abre só o fusível do seu canal, em vez do `F2` e dos seis canais; um surto do campo
  descarrega no terminal sem atravessar o fusível (resta ~2,9 A de pico entre o grampo de
  58 V e o trilho de 31 V: aguenta 8/20 µs, pode abrir em 10/1000 µs); os surtos da fonte
  ficam só com o `D2` (simplifica a `V7`). Custo: uma fonte externa > 36 V ligada a um
  `LOOPk_V+` leva o TVS desse canal, e só desse. Sem efeito na medida.
- ~~**Os seis TVS de trilho ficam, agora num trilho só.**~~ *(texto da rev. 2, ultrapassado)* Na V4.1 havia dois
  trilhos isolados com três TVS cada. Com um trilho, seis é redundante, mas
  mantém um TVS junto de cada par de pinos de `P2`, que é onde a sobretensão
  entra. A interacção com o `D2` analisa-se na 2.3b (`V7`).
- **O fusível de canal passa a 1206**, porque a peça da Legacy é 1206. O da V4.1
  era 0603. O layout desta zona muda de qualquer forma.
- *[Ultrapassado pela rev. 2.4: fica como histórico da escolha do AL5809.]*
  **Rev. 2.1 (2026-09-23, decidida pelo projectista): limitador por canal, fecha a
  `V8`.** Um transmissor em curto fazia passar 74 mA a 28 V e punha 1,4 W na série
  0603 — defeito herdado da V4.1, cujos `PDM2` não limitavam (curto 1 s, sem
  protecção de sobrecarga). O `AL5809-25` garante 23,75-26,25 mA de −40 a +125 °C
  (DS36625 rev. 5, pág. 4): acima dos 22,7 mA de saturação, logo não se perde
  leitura, e o alarme de 21 mA da NE43 lê-se. **No retorno**, em série com o burden,
  não altera a medida; um curto do `+` à massa não passa por ele e continua a abrir
  o fusível de 50 mA (é essa a razão do fusível, que faltava escrever). O `BAT46W`
  (100 V; V_F máx. 0,25 V a 0,1 mA e 0,45 V a 10 mA, Vishay 86406) protege o −0,3 V
  do `AL5809`; a ~3 mA de falha inversa ficam ~0,40 V, **acima dos −0,3 V: resíduo
  a confirmar na 2.3b**. Série a 150 Ω e burden em 1206 para aguentarem os 26 mA.
  Contas em `ferramentas/avalia_opcoes_V8_RE1.py` e no
  `Relatorio_Melhorias_Isolamento_V8_RE1_2026-09-23.md`. **Pegada do AL5809: Type B,
  duas ilhas iguais — não o PowerDI-123 do KiCad.**

  **Estudo completo do datasheet (DS36625 rev. 5-2, 16 págs., md5 7e46a75cc76e), 2026-09-23:**
  - *Queda a 20 mA* — fig. 15 (25 °C): não conduz abaixo de ~1,4 V; a 20 mA fica em
    ~1,6-1,7 V. As contas usam 2,5 V (mínimo recomendado, págs. 4 e 5) porque a fig. 15 é
    só típica e só a 25 °C. A margem real para o transmissor deve ser ~0,8 V melhor.
  - *Corrente em curto* — a tabela garante 23,75-26,25 mA a V_InOut = 3,5 V; a fig. 17
    mostra +1,5 a +2 % a 20 V. Máximo prático em curto ≈ **26,8 mA** (0,08 W no burden e
    0,11 W na série de 150 Ω: dentro de 1206).
  - *Térmica* — o calor sai **pela ilha do pino OUT** (pág. 8: «additional vias between the
    pad of the OUT pin»), e `OUT` é a rede `AINk_LIM`, não a massa. Com a ilha mínima e
    *[2026-09-24: `RB1` passou a 0-70 °C. A 70 °C, 32 V e curto permanente (0,68 W): Tj ≈ 125 °C com
    cobre alargado (nota 5), no limite recomendado; ≈ 171 °C com a ilha mínima (nota 4), em corte térmico.
    O cobre na ilha OUT continua obrigatório. Texto original abaixo:]*
    10 × 10 mm de cobre (nota 4, θJA 148,6 °C/W), o pior caso (85 °C, 28 V, curto
    permanente, ~0,55 W) daria Tj ≈ 167 °C e o **corte térmico (165 °C, histerese 30 °C,
    fig. 18) entraria em ciclo**. Com cobre alargado (nota 5, 81,4 °C/W), Tj ≈ 130 °C. A
    fig. 10 (placa FR4 de 2 camadas) admite ~30 V a 85 °C para a versão de 25 mA, contra
    os ~20,8 V do nosso curto. **Na F3: cobre e vias na ilha OUT de cada U8-U13.** Mesmo com
    cobre insuficiente, a peça protege-se: corta, a leitura cai a 0 mA e recupera.
  - As figuras térmicas do datasheet não são coerentes entre si (a fig. 10 a 25 °C pede
    1,25 W, mais do que a fig. 9 dá para FR4). Usa-se o caso pior e mede-se na bancada.
  - Dois reguladores de corrente em série (o transmissor e o AL5809): abaixo de 23,75 mA
    o AL5809 está fora de regulação e não interage. Perto dos 24 mA os dois tentam
    regular; o ADC já saturou a 22,7 mA. **Ensaio de bancada:** transmissor forçado a
    alarme alto, a ver se há oscilação.

### Prova de uma multiplicação

**Rev. 2.4 (TPS26613, `R10` 0 Ω).** A 18 V, 20 mA, `I_tot` = 6 × 20 mA + 10,8 mA (`U14`)
+ 1,5 mA (LED) = 132 mA:

| Parcela | Conta | Queda |
|---|---|---|
| `F2` | 0,8 Ω × 0,132 A | 0,11 V |
| `D4` | V_F máx. a 0,13 A (fig. 2 do MBR1H100SF) | 0,50 V |
| `F3-F8` | 9,2 Ω × 20 mA | 0,18 V |
| `U8-U13` | `RON` máx. 12,5 Ω × 20 mA | 0,25 V |
| `R10` + burden | (0 + 110 Ω) × 20 mA | 2,20 V |
| **Sobra ao transmissor** | 18 − 3,24 | **≥ 14,76 V** (era ≥ 10,5 V com o AL5809 e 100 Ω) |

Curto a 32 V: `IN` = 31,4 − 9,2 Ω × 40 mA = 31,0 V; `OUT` = 4,4 V; 26,6 V × 40 mA = 1,06 W
durante 100 ms a cada 900 ms. Burden: 40 mA² × 110 Ω = 0,18 W em pico, 0,02 W de média
(`ERA8AEB111V`, 1206, 0,25 W). Pino do ADC: 4,4 V → pelo `R22` 3,3 kΩ e pelo `BAV199` a
`3V3_REF` ≈ 0,15 mA durante 100 ms (a `V10` continua aberta, por construção).

*Texto das revisões anteriores:*

Tensões por canal, rev. 2.1, com 24 V de entrada, `D4` a ~0,5 V `[EST]`, o fusível de
canal a 9,2 Ω (tabela Schurter, «cold resistance typ.»), série 150 Ω e a queda do
limitador tomada por cima em 2,5 V `[EST, mínimo de regulação do AL5809]`:

| Laço | Burden (= pino ADC em DC) | Nó `AINx-` | Sobra para o transmissor |
|---|---|---|---|
| 4 mA | 0,440 V | ≤ 3,54 V | ≥ 19,9 V |
| 20 mA | 2,200 V | ≤ 7,70 V | ≥ 15,6 V |
| 22,7 mA (saturação) | 2,500 V | ≤ 8,41 V | ≥ 14,9 V |
| Transmissor em curto | ≤ 2,89 V (26,25 mA) | — | limitado a 23,75-26,25 mA |

A 20 V de entrada a última coluna cai para **≥ 10,9 V** a 22,7 mA (era ~11,0 V com 249 Ω e
sem limitador).

**Rev. 2.2 — envolvente 18–32 V (`RA1` corrigido em 2026-09-23).** Com a série a 100 Ω, a
**18 V** e 20 mA o transmissor recebe **≥ 10,5 V** no pior caso e ~11,3 V com a queda típica do
limitador (fig. 15 do AL5809). Transmissores que peçam 12 V deixam de medir com a bateria
quase descarregada. É esse o `V9`, e continua a precisar da tensão mínima dos transmissores
instalados, que o escopo não define. A **32 V**, transmissor em curto: 26,8 mA, 25,5 V e
0,68 W no limitador, **Tj ≈ 141 °C** com cobre alargado (nota 5, 81,4 °C/W) e acima do corte
térmico com a ilha mínima (nota 4): **o cobre na ilha OUT de cada U8-U13 passa a obrigatório na
F3.** Contas em `ferramentas/avalia_opcoes_V8_RE1.py`.

## 10 · Folha 07 — termístor

### Ligações, como especificação

`TH1` `NTCS0603E3103JLT` 10 kΩ de **`+2V5_REF`** a `NTC_ADC`; `R40`
`ERA3AEB5621V` 5,62 kΩ de `NTC_ADC` a `GND_ADC`; **`C35` 100 nF de `NTC_ADC` a
`GND_ADC`, novo**. `NTC_ADC` vai ao pino 5 do conversor, `CH4`.

### Porquê

- **Topo em `+2V5_REF` e não em `3V3_REF`**: com a referência nova, o divisor
  pendurado em 3,3 V saturava a 70 °C. Assim fica ratiométrico e o código é o
  mesmo da V4.1: `4096 × ratio` nos dois casos. A tabela do firmware não muda.
- **`C35` é novo e justifica-se pela figura 4-2 do `DS21298E`.** A impedância do
  nó é 10 kΩ ‖ 5,62 kΩ = **3,6 kΩ** a 25 °C e **5,5 kΩ** a −40 °C. A figura, na
  curva de 2,7 V, só garante 1 MHz até ~1,5 kΩ; a 3,6 kΩ cai para ~0,9 MHz e a
  5,5 kΩ para ~0,75 MHz. Com o SPI a 1 MHz o canal saía da especificação no frio.
  Com 100 nF no pino, a carga da amostra vem do condensador e a resistência de
  fonte deixa de contar. Constante de tempo 0,36 ms, irrelevante para uma
  temperatura.

## 11 · LED indicadores — proposta, a confirmar

A V4.1 tem três LED: um no 5 V isolado e dois nos dois trilhos isolados de laço.
Na V5 esses trilhos não existem. Proposta, **mantendo três LED para não mexer nas
janelas do painel**:

| LED | Trilho | Resistência | Corrente | O que diz |
|---|---|---|---|---|
| `D1` | `+24V` | 14,7 kΩ | 1,5 mA | há entrada |
| `D24` | `+24V_ADC` | 14,7 kΩ | 1,5 mA | `F2` está inteiro |
| `D5` | `+5V_ADC` | 2,2 kΩ | 1,4 mA | `F1` e o regulador estão bem |

Diagnóstico que dá: entrada acesa e laço apagado é `F2` aberto. A −40 °C a
queda do LED sobe e a corrente desce ligeiramente, o que só o torna mais
fraco. **A posição física dos três LED tem de ser a da V4.1**, porque pode haver
janelas no painel (`V11`).

## 12 · DFT

| Rede | Ponto | Folha |
|---|---|---|
| `+24V` | `TP1` | 02 |
| `GND_24V` | `TP2` | 02 |
| `+24V_ADC` | `TP4` | 02, novo |
| `+24V_REG` | `TP3` | 02, novo |
| `+5V_ADC` | `TP6` | 03 |
| `3V3_REF` | `TP7` | 03 |
| `+2V5_REF` | `TP5` | 03 |
| `DGND` | `TP8` | 04, do lado do barramento |
| `GND_ADC` | `TP9` | 05 |

Nove, que é o que `RD1` pede. Três fiduciais na folha 01.

## 13 · Orçamento de erro — resumo

Calibração por **constante comum** (confirmado pelo projectista). O pior caso de
`RE1` é **0,237 %** contra 0,2 %, típico 0,139 %; nenhum componente o resolve e
fica uma decisão de escopo para o Portão 0. A deriva, `RE2`/`RB3`, dá 0,165 %
e cumpre. Detalhe em `planejamento_pcb_EBM2_V5.md` §2.7c.

## 14 · Verificações abertas

Numeração única da F2. **As notas da folha 02 chamavam V1 e V2 ao que aqui é V5
e V6**; corrigem-se na mesma passagem.

| # | Verificação | Fecha com |
|---|---|---|
| V1 | Retorno dos seis laços pela massa do ADC: resistência entre as massas dos burden e o `AGND` < 5 mΩ | Layout, F3 |
| V2 | Máximo de entrada do `SPX3819` | Etapa 2.3b |
| V3 | Caminho da corrente de clamp de cada canal até ao sumidouro, com todos os pinos da rede contra os máximos absolutos | Etapa 2.3b |
| V4 | ~~`R34` com pinos trocados no original~~ **Fechada**: a função passou a `R7`, desenhada de novo; a troca não se herda | — |
| V5 | ~~MPN de `R3`, 33 Ω 0805 anti-surto, 1,0 mJ em 80 µs~~ **Fechada (BOM tanda B, 2026-09-25)**: `R3` = 150 Ω KOA `SG73P2ATTD1500F`; curva de impulso SG73P pág. 2: ~26 W a 0,6 ms contra ~6,6 W pedidos (~4×) | — |
| V6 | ~~MPN de `C1`, 2,2 µF ≥ 100 V X7R 1206~~ **Fechada (BOM tanda C, 2026-09-25)**: `C1` = TDK `C3225X7R2A225K230AB` **1210**; curva TDK: 1,54 µF a 30,4 V → 1,18 µF no pior caso (−10 %, −15 %) > 1 µF | — |
| V7 | Seis TVS de 30 V em `+24V_ADC` e o `D2` de 33 V na entrada: quem conduz primeiro e por onde passa a corrente | Etapa 2.3b |
| **V8** | ~~Fechada na rev. 2.1 com o AL5809~~ **Reaberta pela 2.3b e fechada na rev. 2.4 com o `TPS26613` (Legacy): 25-40 mA, corte a 100 ms, novo arranque a 800 ms. Ensaio T26.** Texto original: **Transmissor em curto: ~64 mA sustentados.** O fusível de 50 mA a 1,3× a nominal pode não abrir; `R10` dissipa ~1,0 W e o burden ~0,45 W, em 0603 de 0,1 W. Na V4.1 os conversores isolados de 2 W provavelmente limitavam a corrente `[EST]`; na V5 os 24 V vêm da base board sem limite. **É uma regressão**, e resolvê-la pede peças novas por canal | **Decisão do projectista antes do Portão 1** |
| V9 | **Rev. 2.4: ≥ 14,76 V a 18 V e 20 mA** (§9, prova). Texto original: Tensão que sobra ao transmissor a 20 V de entrada: ~11,0 V a 22,7 mA. Depende do mínimo dos transmissores de campo | Requisito de campo |
| V10 | Máximo absoluto da entrada do conversor, `VDD` + 0,6 V, contra a queda do `BAV199` à corrente real de clamp. A estimativa de 12,5 mA do planeamento ignorava o burden em paralelo; a corrente real é menor | Etapa 2.3b |
| V11 | Posição dos três LED igual à da V4.1, por causa das janelas do painel | F3, contra a placa V4.1 |
| V12 | Pegada SOIC-16 do `MCP3208`: não está na biblioteca do projecto; extrai-se da placa V4.1 auditada | Etapa 2.2b |
| **V13** | **`+5V` do barramento contra o `U5`** (2026-09-23, releitura da netlist da base board V2.3): o `P1.17` recebe o `+5V_IC`, que entra por um borne externo (`P21`) e só tem o TVS `D53` de 5 V (VBR 6,7 V, grampo 9,2 V). O `MCP1824` aguenta **6,5 V** de máximo absoluto (DS22070A). Um transitório entre 6,5 e 9,2 V chega à entrada do LDO. Não é regressão: na V4.1 era o próprio `ISO7141` (máx. 6 V) que estava nesta linha. Avaliar protecção local ou LDO de entrada mais alta | Etapa 2.3b |
| **V14** | **Referências do SPI na base board**: o nosso `DGND` é o `GNDI` (`P19.3/16`, com o `+5V_IC` do `P21`), e o SPI segue para a MainBoard referido a `GNDI_3V3` (`P24.2`). São redes distintas na netlist: a união tem de estar fora da placa (cablagem do painel). Tal como o `CS_ADC` (`P19.9`) e os 24 V (`P19.19/20`), que são ilhas sem cobre e chegam por fio (achado da EBM7). Não verificável pelas netlists: confirmar na cablagem de um painel montado | Antes do Portão 1 |
| **V15** | **LED `LG Q396-PS-35` obsoleto** (DigiKey, última compra 2026-07-02; datasheet v1.9 «Discontinued»). **Substituído (2026-09-24) por `KG EELP41.22-PHRH-35-A8J8-20-R18`**, o mesmo da EBM7 V2.3: mesma pegada e resistências. Com ele saíram também o `GRM188R71E104KA01D` (obsoleto → `GRM188R72A104KA35D`) e o `BAT46W-E3-08` (sem stock até 2027-01 → `BAT46W-7-F`). Ver `Relatorio_Ciclo_Vida_EBM2_V5_2026-09-24.md`. *Nota: a frase anterior citava «−40 °C do RB1»; o projectista corrigiu que não há −40 °C no campo — o `RB1` está a rever (ver escopo)* | Aplicado no gerador; folhas 02/03 à espera do KiCad fechado |

## 15 · O que NÃO muda

Contorno, furação e pinagem de `P1` e `P2`. O mapa de canais do conversor. O
isolador e o conversor, na mesma família e encapsulamento. ~~A série de 249 Ω~~ (0 Ω na rev. 2.4) e a
antialias de 3,3 kΩ. Os 12 TVS de campo (os seis do retorno a 33 V na rev. 2.4). O termístor e a sua resistência.

## 17 · Rev. 2.5 — correcções da 2.3b rev. 2.4 (2026-09-24; **2.5b**: R8 4k12 depois de conferir o TL431BQ)

Origem: `verificacao_2_3b_rev24/verificacao_aplicacao_EBM2_V5_rev24.md` (Fable 5.1, 174 linhas,
16 FAIL) e `recalculo_independente_dimensionamento_EBM2_V5_rev24.md` (Sonnet 5, do zero). Decidido
pelo projectista («adelante, realizalo»). Cada valor com a conta; datasheets na pasta do pacote.

| # | Peça | Antes → depois | Porquê (conta e fonte) |
|---|---|---|---|
| 1 | `R3` | 33 Ω → ~~68 Ω~~ **150 Ω (rev. 2.5c)** 0805 anti-surto (MPN: `V5`, impulso ≤ 4 mJ em ~2 ms) | `RA2` do `F1` a 32 V, mesmo método da 2.3b, com os dados do Eaton 4309 pág. 2 (CC12H250mA: resistência a frio típ. 3,5 Ω, I²t de pré-arco típ. 3,8·10⁻⁴ A²s medido a 10 × In, nota 3; confirmado no texto e na imagem da tabela). A curva I²t-tempo da pág. 4 dá ≈ 6·10⁻⁴ a 1,5·10⁻³ A²s a 0,1-0,5 ms, a duração real do arranque: **a margem abaixo é conservadora**. Conta: `V²·C1/(2R)` + `I_LIM²·t` da carga a jusante (`C4` a 5 V, o trilho `3V3_REF` e `C5`). Com os condensadores novos: 47 Ω → **9,4×** (falha), 56 Ω → 10,3×, **68 Ω → 11,2×**. A 18 V, ~7 mA de carga: 0,48 V em `R3`, o `U1` recebe ~17 V (mín. 7 V). Pico 0,45 A, ~1,1 mJ por arranque |
| 1c | `R3` | **Rev. 2.5c (2026-09-25), decidida pelo projectista** | O recálculo independente da rev. 2.5b achou que o SBVS162B **se contradiz** no I_LIM do TPS7A4001: tabela (pág. 5) máx. **200 mA**; texto (§7.3.1, pág. 8) «**309 mA, typical**». Com 309 mA e 68 Ω o `RA2` cai a **8,6×** (a conta de 11,2× usava 200 mA). Com **150 Ω** a corrente do fusível fica limitada pela própria resistência, I ≤ 32 V / 153,5 Ω = **0,21 A**, qualquer que seja o I_LIM. Limite rigoroso ∫I² ≤ I_max·(Q_C200 + Q_jusante) = 0,208 A × (70 + 92) µC = 3,4·10⁻⁵ A²s → **11,2×**; realista (RC exacto do C1 + jusante a 0,21 A) **14,3×**. A 18 V: 1,05 V em `R3`, `U1` a 16,4 V (mín. 7 V); arranque com ~68 mA, ~1,5 ms. **Interacção a registar:** subir `C8` (TL431) aumenta a carga a jusante e come margem ao `F1` (a 2.3b rev. 2.5b apontou que não estava escrita). **Aberto:** com um curto em `+24V_REG` o `R3` limita a 0,21 A, abaixo da nominal do `F1` (250 mA): o fusível não abre e o `R3` queima como elemento fusível (já acontecia com 33 e 68 Ω, a 0,87 e 0,45 A) |
| 2 | `U4` | `SPX3819M5-L-3-3` → **`MCP1824T-3302E/OT`** (SOT-23-5) | O TL431 precisa de > 6 µF no cátodo (fig. 6-18, SLVS543S pág. 18, curva A: fronteira direita ≈ 4,5-6 µF) e o `SPX3819` só especifica electrolítico/tântalo («bench testing is the best method»). O `MCP1824` é estável com cerâmico ≥ 1 µF e recomenda ≤ 22 µF (DS22070A §4.3, pág. 19); VIN 2,1-6,0 V; VOUT 3,3 V ± 2,5 % (pág. 8). Pinagem SOT-23-5 fixa 1 VIN · 2 GND · 3 SHDN · 4 PWRGD · 5 VOUT (tabela 3-1, pág. 17), a mesma geometria do `SPX3819`: muda só o pino 4 |
| 3 | `C208` | 10 nF → **sai** | Era o `BP` do `SPX3819`. No `MCP1824` o pino 4 é `PWRGD` (dreno aberto): fica sem ligação. `EN_3V3` passa a `SHDN_3V3` (`R7` 100 kΩ a `VIN`; limiar máx. 45 % de VIN, §4.6 pág. 20) |
| 4 | `C8` | 2,2 µF → **10 µF 50 V X5R 1206 `C3216X5R1H106K160AB`** | Curva da TDK (ProductDetailed, pág. 2): ≈ 9,4 µF a 3,3 V. Pior caso −10 % −15 % (X5R) → 7,2 µF + 1,3 µF do resto do trilho = **8,5 µF > 6 µF**. Nominal 11,4 µF ≤ 22 µF do `MCP1824` |
| 5 | `R8` | 4k42 → ~~4k22~~ **4k12** (`RC0603FR-074K12L`, **rev. 2.5b**) | TL431**BQ**, tabela 6.13 do SLVS543S (pág. 14): V_ref 2,483-2,507 V a 25 °C; **V_I(dev) 34 mV** (máx.−mín. em −40…125 °C; a 1.ª conta usou 17 mV de memória, errado); I_ref 4 µA + I_I(dev) 2,5 µA; \|z_KA\| 0,5 Ω; ΔV_ref/ΔV_KA −2,7 mV/V. Conservador (os 34 mV inteiros para cada lado, R a 1 %, 46 mA da falha dupla): 4k22 → 3,451-3,688 V (**12 mV** sob 3,70 V); **4k12 → 3,427-3,662 V: 38 mV sob 3,70 V (`RA4`) e 45 mV sobre os 3,3825 V do `MCP1824` (+2,5 %, pág. 8)**, o TL431 não conduz em regime. Os 3,70 V são critério de aceite (`RA4`), não máximo absoluto de peça (MCP3208 7 V, ISO7141 6 V, ADR4525 15 V). I_min real 0,7 mA (não 1 mA) |
| 6 | `C5` | 1,0 µF → **2,2 µF** | Estava no mínimo da tabela 11 do ADR45xx (pág. 35) |
| 7 | `C11` | 1,0 µF → **2,2 µF** | Estava no mínimo do `MCP1824` (§4.3) |
| 8 | `C7`, `C33` | **novos**, 10 nF entre `OUT` e `FB` do `U1` e do `U14` | `C_BYP` (SBVS162B nota 4 pág. 5, §8.2.2.3 pág. 11: «TI highly recommends»). Zero em 1/(2π·32,4 kΩ·10 nF) = 491 Hz (`U1`) e 171 Hz (`U14`) |
| 9 | `C32` | **novo**, 10 µF 50 V `C3216X5R1H106K160AB` em paralelo com `C31` | Curva TDK a 12,6 V ≈ 5,8 µF; com −10 % e −15 % (X5R garantido) uma peça dá 4,4 µF **< 4,7 µF** (SBVS162B pág. 1). Duas: **8,9 µF** |
| 10 | `R28`-`R33` | **novas**, 4k7 0603 (`RC0603FR-074K7L`) entre o nó do filtro (`AINk_FILT`: `C(22+k)`, `D(17+k)`) e o pino do ADC (`AINk_ADC`) | Em curto (`I(OL)` 40 mA × 110 Ω = 4,4 V) o `BAV199` conduz ~0,15 mA e cai **≈ 0,67 V a 25 °C, ≈ 0,72 V a 0 °C** (fig. 2 do BAV199LT1/D): o nó fica acima de `VDD` + 0,6 V por construção (a `V10`). A série limita a corrente para o díodo interno do MCP3208 (modelado com 0,6 V, fig. 4-1 do DS21298E) a **(0,74 − 0,6)/4,7 kΩ ≈ 30 µA**. Custo: fuga típica ≤ 2 nA (fig. 2-39) × 4,7 kΩ ≈ 9 µV; no máximo da tabela (±1 µA) 4,7 mV = 7,7 LSB de offset, que a calibração de campo remove. A carga do C_sample de 20 pF por 4,7 kΩ + 1 kΩ: τ = 114 ns contra 75 µs de amostragem. **Não prova** o limite absoluto de tensão, que o datasheet só dá em tensão: prova-se no T26 e pede-se à Microchip a corrente de injecção |

| 11 | BOM, tandas A e B (2026-09-25) | MPN e pegada, nenhuma rede | Tanda A: 14 MPN da casa; **`C4` → `C3216X5R1H106K160AB` em 1206** (curva TDK: 7,0 µF a 5 V no pior caso > 4,7 µF; fecha a F8); TP3-TP10 fora da BOM. Tanda B: **`U2` → `ADR4525WBRZ-R7`** (família «Restricted Availability» na Mouser; mesmo grau B, W = automóvel, tabela 14 pág. 40 e nota 2 pág. 41 do ADR45xx; o grau A não serve, 8 ppm/°C bowtie); **`R3` = KOA `SG73P2ATTD1500F`** (curva de impulso SG73P pág. 2: ~26 W a 0,6 ms contra 6,6 W, ~4×); porto DGND do `P1.12` deslocado na folha 01 (o triângulo tapava o `P1.13`). `C5`/`C11` `C1608X5R1E225K080AB` conferidos na curva TDK (≥ 1,26 µF). **Tanda C: `C1` = TDK `C3225X7R2A225K230AB` em 1210** (curva TDK: ~1,54 µF a 30,4 V; pior caso −10 % −15 % = 1,18 µF > 1 µF do TPS7A4001; `RA2` 11,3× com a carga real). O TDK `C3216X7S2A225K160AB` (X7S 1206) foi **descartado**: 0,89 µF no pior caso. Murata GRM31CR72A225KA73L obsoleto e GRM32ER72A225KA35L em fim de vida. Pegada IPC do projecto contra o land pattern TDK (hueco 1,8 contra 2,0-2,4 mm): conferir na F3 |

**Não muda, e porquê:**
- `R10` = 0 Ω. Na falha dupla (`U8-U13` em curto + 30 V injectados) o burden vê 273 mA / 8,2 W. Voltar a
  100 Ω poria `OUT` a 8,4 V no limite de corrente e o `VSNS` deixava de ter solução entre os 4,4 V e o
  `+12V_TPS` mín. 11,58 V. **Aceite como falha dupla**, documentada.
- `V13` (`+5V_IC` com grampo de 9,2 V contra os 6,5 V do `U5`): medir o barramento num painel.
- O «mínimo de 1 mA» do TL431 (recálculo Sonnet): numa falha simples a corrente injectada (≤ 0,15 mA por
  canal) é menor que a carga de `3V3_REF` (~4 mA); o LDO fornece menos e o TL431 nem conduz. Só a falha
  dupla (46 mA) o põe a regular, bem acima de 1 mA.
- A fig. 7-19 do TPS26613 lida pela 2.3b dá ~140 ms até ao corte térmico a 85 °C (a §9 lia ~200 ms):
  continua acima dos 100 ms do temporizador, com menos margem. Confirmar no T26.

## 16 · Porta de verificação da revisão

No fim da F2, a netlist completa da V5 compara-se **nó a nó** com a da V4.1
auditada, pela tabela de correspondência da §2. Qualquer diferença que não esteja
enumerada neste documento é defeito de transcrição, não alteração.
