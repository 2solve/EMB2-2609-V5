# Recálculo independente do dimensionamento — EBM2 V5 rev. 2.4 (2.3b)

**Revisor:** modelo independente (Claude Sonnet 5), sem histórico da conversa de autoria (o autor foi outro modelo).
**Método:** Fase 1 — recalculei do zero a partir só de `EBM2_V5.net`, `esquematico_EBM2_V5.pdf` e dos datasheets em `datasheets/`, com pior caso (mín/máx de tolerâncias, 70 °C, 18 e 32 V). **Só depois** abri `intencao_EBM2_V5.md` e `planejamento_pcb_EBM2_V5.md` (Fase 2).
**Ferramentas:** `grep_datasheet.py` (texto e render de página) e leitura directa da netlist com um script de topologia (`bom_values.py`), citando página de cada datasheet.

---

## 0 · Topologia confirmada na netlist (base de todos os cálculos)

Por canal *k* (exemplo canal 1): `+24V_ADC → F60k (50 mA) → LOOPk_V+ → [transmissor externo] → AINk- → U60k(TPS26613DDFR) IN(4)→OUT(5) → R60k (0 Ω) → nó de medida → burden R61k (110 Ω) a GND_ADC, em paralelo com antialias R62k (3,3 kΩ) → C60k (100 nF) → clamp D62k (BAV199) → MCP3208`.

Pontos que a netlist obrigou a corrigir face à leitura ingénua do esquemático:

- **`U640` (TPS7A4001) alimenta só o `+Vs`/divisores dos seis `U601`-`U606`** (pino 6, rede `+12V_TPS`) — **não** carrega a corrente de laço, que vai directa de `+24V_ADC` pelos `F60x`.
- **O nó `VSNS` é um só, partilhado pelos seis `U60x`** (`R643`/`R644`/`R645` existem uma única vez, não seis). Um erro fácil de cometer (cometi-o na primeira passagem) é multiplicar por 6 a corrente deste divisor.
- **`TL431` `U203`**: confirmei a pinagem do encapsulamento **DBZ (SOT-23-3)** na pág. 4 do `TL431__TI_TL431.pdf` — `1 CATHODE, 2 REF, 3 ANODE` (a tabela de texto extraída tinha as colunas do `TL431` e do `TL432` trocadas; só a imagem desambiguou). Logo: **cátodo em `3V3_REF` (directo), REF em `FB_CLAMP`** (divisor `R204` 4k42/`R205` 10k), ânodo em `GND_ADC` — é um regulador shunt clássico, não um sumidouro sempre saturado como a primeira leitura (só de texto) sugeria.
- **`R206` (33 Ω) está na rama do `+24V_REG`**, entre `D201` e `C200`/`U200` — não existe resistor equivalente na rama `+24V_ADC`/`U640`.
- **`D601`-`D606` (retorno, `SMBJ33A-13-F`) não têm datasheet na pasta.** `D611`-`D616` (terminal, `824520361`/Würth SMBJ36A) têm.

---

## Fase 1 — recálculo independente

### 1 · Queda por canal e tensão ao transmissor, a 18 V

| Termo | Fórmula | Valores | Fonte | Resultado |
|---|---|---|---|---|
| Corrente total em `+24V_ADC` | `6×I_ch + I(U640) + I(D630 LED)` | 6×20 mA + 10,8 mA + ~1 mA | netlist | **≈132 mA** |
| `F202` (0,8 Ω) | `I_tot×R` | 0,132×0,8 | Eaton 4309 p.2, «Typical DC cold resistance» | 0,11 V |
| `D202` (MBR1H100SF) | `V_F` máx. a 0,13 A | fig. 2 (Max Forward Voltage), 25 °C | onsemi p.3 | ≈0,50-0,55 V (leitura gráfica; ver nota) |
| `F60k` (9,2 Ω) | `I_ch×R` | 0,020×9,2 | Schurter 3413, p.4, cold resistance típ. | 0,184 V |
| `U60k` (`R_ON` máx.) | `I_ch×R_ON` | 0,020×12,5 | SLVSFE3C p.6, Elec. Char. | 0,25 V |
| `R60k` (0 Ω) + burden | `I_ch×(0+110)` | 0,020×110 | netlist + BOM | 2,20 V |
| **Sobra ao transmissor, 20 mA** | `18 − ΣV` | 18 − (0,11+0,52+0,184+0,25+2,20) | | **≥ 14,7 V** |
| **Sobra ao transmissor, 22,7 mA (saturação)** | idem, `I_ch`=22,7 mA | | | **≥ 14,3 V** |

**Veredito: cumpre** — mesmo no pior caso (`R_ON` máx., resistências a frio) sobram ≥14,3 V ao transmissor a 18 V. **Nota:** o requisito de campo (tensão mínima de conformidade dos transmissores instalados) não está definido em nenhum documento da pasta — não há como confirmar que 14,3 V chega para *todo* transmissor de campo; é o mesmo gap que a própria intenção já regista (`V9`).

### 2 · Transmissor em curto a 32 V

| Item | Fórmula/fonte | Valores | Resultado | Veredito |
|---|---|---|---|---|
| `I(OL)` unipolar (`MODE`=GND, `-Vs`=GND) | Elec. Char. p.5 | mín/típ/máx 25/32/40 mA | pior caso **40 mA** | — |
| `+24V_ADC` a 32 V, 6 curtos | `32 − I_tot×R_F202 − V_D202` | `I_tot`=6×40+10,8+1≈252 mA; `R_F202`=0,8 Ω; `V_D202`≈0,55 V a 0,25 A | **31,15 V** (por canal, ignorando os outros 5 em curto simultâneo dá 31,4 V como no §9 da intenção) | — |
| `IN` do `U60k` | `+24V_ADC − I×R_F60k` | 31,4 − 0,040×9,2 | **31,03 V** | — |
| `OUT` (burden) | `I_OL×R_burden` | 0,040×110 | **4,40 V** | dentro de `IN,OUT` abs máx ±55 V (p.4) — cumpre |
| Tensão sobre o `U60k` | `IN−OUT` | 31,0−4,4 | 26,6 V | — |
| Potência de pico | `V×I` | 26,6×0,040 | **1,06 W** | — |
| Temporizador `MODE`=GND | Tabela 8-3, p.23 | `I(OL)` por `tOL_Expiry`=100 ms, depois FET desliga, `tRETRY1`=800 ms, repete | ciclo 100 ms ON / 800 ms OFF (11,1 % duty) | — |
| Potência média | `P_pico×duty` | 1,06×0,111 | **0,118 W** | — |
| `ΔT` (RθJA 117,8 °C/W, p.4) | `P_méd×RθJA` | 0,118×117,8 | **+14 °C** | — |
| Corte térmico, fig. 7-19 (p.12) | leitura gráfica a `TA`≈85 °C (não há curva a 70 °C; uso a de 85 °C, mais pessimista, como pior caso) | a ~1,05 W, corte térmico em **~150-250 ms** | o temporizador de 100 ms corta **antes** do corte térmico (160 °C) | **cumpre** — o corte por corrente antecede o corte térmico |
| Potência no burden (`ERA8AEB111V`, 1206) | `I²×R` | 0,04²×110 pico; 0,111×0,04²×110 média | 0,18 W pico / 0,02 W média | dentro de qualquer 1206 usual — cumpre |
| Nó do ADC durante o pulso | `OUT` (4,4 V) por `R621` (3,3 kΩ) até ao clamp `BAV199` | `(4,4−V_clamp)/3300` | ≈0,15-0,2 mA durante 100 ms | ver item 8 |
| Pino do ADC (`MCP3208`) vs abs. máx. | `VDD+0,6 V` (p.2) | `VDD`(=`3V3_REF`)≈3,3 V → abs. máx. ≈3,9 V; clamp = `3V3_REF`+`V_F`(BAV199 a poucas centenas de µA, fig.2 do BAV199) ≈3,6+0,5≈**4,1 V** | **excede o abs. máx. em ~0,2 V** | **FALHA marginal — ver nota** |

**Nota sobre o pino do ADC:** com corrente de clamp baixa (~0,15-0,2 mA, no cotovelo da fig. 2 do `BAV199LT1-D.PDF`, p.3), `V_F`≈0,5-0,6 V. Isso põe o nó a ≈4,1-4,2 V contra um abs. máx. de `VDD+0,6 V`≈3,9 V (com `VDD`=3,3 V nominal) a **3,97-4,26 V se `3V3_REF` já estiver no tecto do grampo do `TL431` (3,615 V)**. É uma margem negativa pequena (dezenas a poucas centenas de mV) e depende de duas leituras gráficas (o `V_F` do `BAV199` a essa corrente exacta e a tolerância de `3V3_REF`); **não é um FALHA robusto, é um aviso quantificado** — o próprio planeamento já tinha aberto este ponto como `V10` sem o fechar. Recomendo medição de bancada (injectar o curto e medir o pino `CH0` do `MCP3208` directamente) antes de assinar.

**Corrente nos clamps `BAV199`:** ≈0,15-0,2 mA durante 100 ms a cada 900 ms — desprezável termicamente (`BAV199` aguenta 215 mA contínuos) e dentro da fuga reversa esperada (nA a µA quando não conduz).

### 3 · Ligação invertida / tensão externa no retorno

| Peça | O que acontece | Fonte | Veredito |
|---|---|---|---|
| `U60k` (`TPS26613`) | **Tabela 8-1 (p.17): "Input Undervoltage: N"** para `TPS26613`/`14` — não bloqueia corrente inversa, mas **limita-a**: linha "Unipolar current limit with `VIN<-Vs`" dá **−40/−32/−25 mA** (mín/típ/máx, p.5) | SLVSFE3C p.5,17 | cumpre — corrente inversa fica limitada à mesma ordem de grandeza que o curto directo, sem dano |
| `OUT` do `U60k` (nó de medida) | `VO_UVLO`=(−Vs)−0,2 a −0,4 V; com `−Vs`=`GND`(0 V), corta o FET se `OUT`<−0,2 a −0,4 V, em `tO_UV_CUT`=1-5 µs | SLVSFE3C p.6,8 | protecção coerente com o burden a jusante — cumpre |
| `IN`/`OUT` abs. máx. | −55 a +55 V (p.4) | SLVSFE3C p.4 | folga grande contra qualquer tensão de campo plausível — cumpre |
| `D601`-`D606` (retorno) | Protegeriam `IN` contra a tensão externa — **datasheet ausente (`SMBJ33A-13-F`, ver `LISTA.md`)** | — | **falta dado** |
| `MCP3208` a jusante | Isolado do evento por `U60k` já cortado (`OUT` grampeado perto de 0 V) antes de chegar ao burden/antialias | — | cumpre, condicionado ao acima |

### 4 · TVS do retorno (`D60x`) e do terminal (`D61x`)

| TVS | Standoff | Clamp | Contra o quê | Veredito |
|---|---|---|---|---|
| `D601`-`D606` (retorno, `SMBJ33A-13-F`) | 33 V (nominal) | **sem datasheet na pasta** — a intenção usa por analogia o `D200` (`SMA6J33A-Q`, Bourns, mesma classe 33 V, clamp 53,3 V @ 11,3 A, p.2) | `IN` do `U60k`, abs. máx. 55 V | **falta dado** (parte real não verificada; a analogia de classe é razoável mas é de outro fabricante — a Diodes Inc. pode ter `V_C` diferente a igual corrente) |
| `D611`-`D616` (terminal, `824520361`) | **36 V DC** (p.1) > 32 V máx. de operação — margem 12,5 % | **58,1 V** @ `I_PEAK` (p.1) | Não está ligado a nenhum pino do `U60k` directamente (fica em `LOOPk_V+`, antes do transmissor externo) — o abs. máx. de 55 V de `IN`/`OUT` só é exposto por acoplamento comum com `D601` através do laço externo | **cumpre no standoff**; **o clamp (58,1 V) excede os 55 V abs. máx. de `IN`/`OUT` do `TPS26613`** — mas o caminho de exposição é indirecto (via o transmissor e o segundo fio do laço), como o próprio autor já regista. Risco residual, não uma exposição directa |
| `D611` vs. retorno em curto (standoff) | a 32 V, `LOOP1_V+`≈`+24V_ADC`−`I×R_F601`≈31,4 V | 36 V > 31,4 V | margem 4,6 V (13 %) | cumpre |

### 5 · Trilho `+12V_TPS` (`U640`, TPS7A4001)

| Item | Fórmula | Valores | Fonte | Resultado |
|---|---|---|---|---|
| `VOUT` nominal | `VREF×(R641+R642)/R642` | `VREF`=1,161/1,173/1,185 (mín/típ/máx); `R641`=93,1 k, `R642`=10 k | SBVS162B p.5 (Elec. Char.) | típ **12,09 V** |
| `VOUT` pior caso (`VREF`+resistores 1 %) | idem, extremos combinados | `R641`×1,01/`R642`×0,99 com `VREF`máx.; e o oposto com `VREF`mín. | | **11,76 V a 12,44 V** |
| `+Vs` do `U60x` vs abs. máx. (−0,3 a 32 V) e rec. operating (0-30 V) | — | 12,44 V máx. | SLVSFE3C p.4 | cumpre com folga larga |
| Consumo total (`IOUT` do `U640`) | `6×I(+Vs) + I(VSNS_div) + I(FB_div)` | 6×1,65 mA(máx, SLVSFE3C p.6) + **0,727 mA (um só divisor `VSNS`, partilhado)** + 0,117 mA | netlist (nó `VSNS` único!) | **≈10,8 mA** |
| `+24V_ADC` a 32 V, 6 canais a 20 mA | `32 − I_tot×R_F202 − V_D202` | `I_tot`≈132 mA | Eaton 4309, onsemi fig.2 | **≈31,4 V** |
| Dissipação `U640` | `(VIN−VOUT)×IOUT` | (31,4−12,09)×0,0108 | SBVS162B eq. 2, p.14 | **0,21 W** |
| `ΔT` (RθJA 66,7 °C/W, p.4) | `P×RθJA` | 0,21×66,7 | | **+14 °C** |
| `Tj` a 70 °C ambiente | `70+14` | | | **84 °C**, bem abaixo do `Tj` máx. 125 °C (p.4) — **cumpre** |
| Condensador de saída (`C642`, 10 µF/50 V X5R, `C3216X5R1H106K160AB`) | mínimo do datasheet: **≥4,7 µF sobre temperatura e tolerância** (p.1, §8.2.2.2) | valor nominal 10 µF a 12 V, mas a curva de polarização DC/temperatura do próprio condensador **não está na pasta** | LISTA.md: ausente | **falta dado** — não posso confirmar que os 10 µF nominais ficam acima de 4,7 µF efectivos a 12 V/70 °C |
| Condensador de entrada (`C640`+`C641`, 10 µF+100 nF/100 V) | mínimo ≥1 µF (recomendado 10 µF, p.11) | `C640` é `GRM32EC72A106ME05L` (Murata, presente na BOM mas datasheet de derating não confirmado nesta pasta) | | **cumpre no valor nominal**; derating a 32 V/70 °C não verificado (mesmo problema que `C642`, mas o valor nominal já é 2× o mínimo recomendado, dando folga) |
| `EN` (pino 5, junto com `IN` em `+24V_ADC`) | `VEN_HI`=1,5 a `VIN` (p.6) | `+24V_ADC`≫1,5 V | | cumpre |

### 6 · Divisor `VSNS` do `U60x`

| Item | Fórmula (Tabela 8-2, p.20) | Valores | Resultado | Veredito |
|---|---|---|---|---|
| Limiar de subida (±Vs supplies) | `+Vs ≥ V(SNSR)×(R1+R2)/R2` | `V(SNSR)`=1,72 V típ. (só típ. no datasheet); `R1`=`R643`=13,3 k; `R2`=`R644‖R645`=3,325 k | limiar = 1,72×16625/3325 = **8,60 V** | `+Vs` mín. 11,76 V > 8,60 V — **cumpre**, fica em modo `±Vs` |
| Limiar de descida (loop power) | `+Vs ≤ V(SNSF)×(R1+R2)/R2` | `V(SNSF)`=1,0 V típ. | limiar = **5,00 V** | `+Vs` nunca se aproxima disto em operação normal — cumpre |
| Nota (1): `(R1+R2)≤(+Vs)/45µA` | | 16 625 ≤ 11,76/45e-6 = 261 333 | cumpre com folga ampla |
| Nota (2): `V(SNSF)×(R1+R2)/R2 > I_LOOP×R_burden` | | 5,00 V > 0,040×110=4,40 V | cumpre (margem 14 %) — o limiar de transição para modo laço fica acima do pior burden em curto |
| `+Vs` vs `VOUT_OVLO` | `VOUT_OVLO`=(+Vs)+0,05 a +0,30 V (p.5) | é relativo a `+Vs`, não um valor fixo | `OUT` nunca chega perto de `+Vs` (máx. 4,4 V em curto vs. `+Vs`≈12 V) — a protecção nunca actua por acidente | cumpre |

### 7 · `F202` e `F201`: I²t de arranque a 32 V

**Fórmula (RC clássica, energia dissipada no fusível ao carregar um bulk através de uma resistência série):**
`I²t = V²·C / (2R)`

| Rama | `C` total | `R` total | `I²t` | I²t de fusão | Margem | Veredito |
|---|---|---|---|---|---|---|
| `F202` (750 mA, `RA2`) | `C201`(10 µF)+`C640`(10 µF)+`C641`(0,1 µF) = **20,1 µF** — todo o bulk *directo*; **`C642`(10 µF)+`C611`-`C616`(0,6 µF) carregam-se pelo limite de corrente do `U640` (200 mA abs. máx., p.5), não como capacidade directa** | `R_F202`=0,8 Ω (Eaton 4309 p.2) | 32²×20,1e-6/(2×0,8) = **0,01286 A²s**, + carga do `U640` (0,2²×`t_carga`; `t_carga`=10,6 µF×12,09 V/0,2 A≈0,64 ms → +2,6e-5) ≈ **0,01289 A²s** | 0,15 A²s (Eaton 4309 p.2) | **11,6×** | **cumpre (>10×), mas com margem apertada** — ver nota |
| `F201` (250 mA) | `C200`=2,2 µF (directo); `C202`(10 µF)+`C203` carregam-se pelo limite do `U200` (200 mA abs. máx.) | `R_F201`(3,5 Ω)+`R206`(**33 Ω**, netlist actual) = 36,5 Ω | 32²×2,2e-6/(2×36,5) = **3,09e-5 A²s**, + carga do `U200` (0,2²×0,25 ms) ≈ **4,09e-5 A²s** | 0,00038 A²s | **9,3× incluindo a carga do `U200`; 12,3× só com `C200`** | **cumpre por pouco (base 12,3×); com a carga do `U200` incluída cai a 9,3×, abaixo dos 10× exigidos por `RA2`** |
| Corrente em regime, 6 curtos simultâneos | `6×I(OL)máx + I(U640)` | 6×40+10,8 = **250,8 mA** | — | `F202` 750 mA nominal | folga 3×, não abre | cumpre |

**Nota sobre `F202` (11,6×):** o datasheet Eaton só publica **resistência típica** (sem mín./máx.). Se a peça real vier ~15-20 % abaixo do típico (variação peça-a-peça plausível, sem dado de tolerância), a margem cai para **≈9,3-9,9×**, ficando **abaixo do critério `RA2` (≥10×)**. Não é uma FALHA que eu possa afirmar — é uma margem **frágil**, sensível a uma tolerância que o fabricante não declara. Recomendo medir a resistência a frio de uma amostra de `F202` antes de fechar `RA2`.

**Nota sobre `F201`:** o valor de 33 Ω (netlist actual) já não é o de 22 Ω usado no `planejamento_pcb_EBM2_V5.md` §2.6 (que também não incluía `C640`/`C641`/`C642`, que ainda não existiam nessa revisão). Recalculado com os valores actuais, a margem-base (só `C200`) é 12,3×; contando a corrente de arranque do `U200` (o mesmo mecanismo que a intenção aplica ao `U640` na rama do `F202`, aqui aplicado à rama do `F201`) a margem cai a **9,3×** — **FALHA marginal contra `RA2`**, mas dependente de uma soma de dois fenómenos (RC directo + corrente limitada do regulador) que provavelmente não são simultâneos no pico, pelo que o número real fica algures entre 9,3× e 12,3×. Ensaio de bancada resolve isto em minutos.

### 8 · Cadeia de referência/clamp (`U200`→`SPX3819`→`3V3_REF` com `TL431`→`ADR4525`)

| Item | Fórmula | Valores | Fonte | Resultado |
|---|---|---|---|---|
| `+5V_ADC` (`U200`) | `VREF×(R201+R202)/R202` | `VREF`=1,161/1,173/1,185; `R201`=32,4 k, `R202`=10 k | SBVS162B p.5 | típ. **4,974 V** (confere exactamente com a intenção); pior caso ≈4,85-5,10 V |
| `3V3_REF` (`SPX3819M5-L-3-3`) | tolerância declarada | ±1 % (fixo 3,3 V), dropout 125-350 mV a 10-50 mA (p.2) | SPX3819 p.2 | `3V3_REF`≈3,267-3,333 V em operação normal |
| Grampo do `TL431` (`U203`) | `V_clamp = Vref×(R204+R205)/R205` | `Vref`(grade B, Q-temp, DBZ)=2,483/2,495/2,507 mV (p.14); `R204`=4,42 k, `R205`=10 k | TL431 SLVS543S p.14 | **3,581 a 3,615 V** (típ. **3,598 V**, confere com os «3,60 V» da intenção) |
| `TL431` em operação normal | `V(REF)`=`3V3_REF`≈3,3 V < `V_clamp`(3,581-3,615 V) | o `TL431` fica **desligado** (`Ioff`≤1 µA, p.6) até `3V3_REF` se aproximar de ~3,6 V | TL431 p.6 | consistente com «sumidouro só quando preciso», e não «sempre saturado» (correcção da 1.ª leitura, feita só de texto extraído) |
| Corrente de cátodo disponível num evento de grampo | `I_clamp`≈0,15-0,2 mA (item 2) | contra `Imin`=1 mA máx. exigido para regulação apertada (p.6, «Minimum cathode current for regulation») | TL431 p.6 | **abaixo de `Imin`** — o grampo pode ficar **mais suave** (nível efectivo acima dos 3,60-3,615 V nominais) do que o valor calculado, porque o `TL431` não está garantidamente na sua região de regulação apertada com tão pouca corrente. **Não é FALHA comprovada, é incerteza a favor da segurança que convém medir** |
| Contra `RA4` (30 V no campo, `3V3_REF`≤3,7 V) | `V_clamp` máx. 3,615 V + a incerteza acima | | | **cumpre no valor nominal (3,615<3,7 V)**, com a reserva da linha anterior |
| Estabilidade (fig. 6-18, p.18) | `C_L` no cátodo = `C204`(2,2 µF)+`C205`+`C206`(0,1 µF cada) = **2,4 µF**; `I_KA`≈0 (repouso) a ≈0,2 mA (grampo) | curva A (`VKA`=`Vref`, a mais próxima do nosso caso) mostra uma região instável entre aprox. 0,01 e poucos µF, estreita perto de `IKA`→0 | TL431 p.18 | **leitura gráfica no limite da resolução do render — não consigo afirmar com confiança que 2,4 µF fica fora da faixa instável a `IKA` tão baixo.** Recomendo ensaio de bancada (procurar oscilação em `3V3_REF` ao forçar um evento de grampo) antes de fechar |
| `ADR4525BRZ` | inicial ±0,02 % (500 µV), 2500 mV nominal, `TC`: 2 ppm/°C (box) / **4 ppm/°C (bowtie, o que conta a partir do ponto de calibração)** | Table 2, p.4 | ADR4525 p.4 | confere com a intenção (§4 do escopo) |

---

### Resumo Fase 1

| # | Item | Veredito |
|---|---|---|
| 1 | Queda por canal / sobra ao transmissor, 18 V | **cumpre** (≥14,3 V) |
| 2 | Curto a 32 V — corrente/potência/`Tj` do `U60x` | **cumpre**; pino do ADC com **margem negativa pequena** contra o abs. máx. (aviso) |
| 3 | Inversão / tensão externa no retorno | **cumpre** no `U60x`; **falta dado** no `D60x` (retorno) |
| 4 | TVS retorno/terminal vs. abs. máx. | `D601`-`606`: **falta dado**; `D611`-`616`: clamp 58,1 V > 55 V abs. máx., exposição **indirecta** |
| 5 | `+12V_TPS` (`U640`) | **cumpre** em tensão/potência/`Tj`; condensadores **falta dado** (sem curva de polarização) |
| 6 | Divisor `VSNS` | **cumpre**, todos os itens |
| 7 | `F202`/`F201` I²t de arranque | `F202` **cumpre com margem frágil** (11,6×, sensível a tolerância não publicada); `F201` **cumpre marginalmente / FALHA marginal** (9,3-12,3× consoante o que se conta) |
| 8 | Cadeia de referência/clamp | **cumpre** nos valores nominais; **estabilidade e nível efectivo do grampo têm incerteza** que recomendo fechar em bancada |

---

## Fase 2 — comparação com as contas do autor

Abri agora `intencao_EBM2_V5.md` e `planejamento_pcb_EBM2_V5.md`.

### Confirmações (sem divergência >5 %)

| Item | Meu número | Número do autor | Nota |
|---|---|---|---|
| Sobra ao transmissor, 18 V/20 mA | ≥14,64-14,76 V | **≥14,76 V** (intenção §9) | confere; a única sub-parcela que difere é a leitura gráfica do `V_F` do `D202` (0,50-0,55 V vs. os 0,50 V do autor — dentro da incerteza de leitura de gráfico) |
| Curto a 32 V: `IN`, `OUT`, potência, `ΔT` | `IN`=31,0 V, `OUT`=4,4 V, 1,06 W pico, 0,12 W média, +14 °C | **idêntico**, item a item (intenção, folha 06 «Porquê» e §9) | confirmação forte — a mesma física, dois caminhos de cálculo independentes |
| `+12V_TPS` consumo/dissipação | 10,8 mA, 0,21 W, +14 °C | **idêntico** (intenção, folha 06 «Porquê») | confirma, **depois de eu próprio corrigir um erro inicial** (tinha multiplicado por 6 a corrente do divisor `VSNS`, que é partilhado — ver §0) |
| `+5V_ADC` (`U200`) | 4,974 V típ. | **4,974 V** (planejamento §2.3, intenção §6) | idêntico |
| Grampo `TL431` | 3,598 V típ. (3,581-3,615 V pior caso) | **3,60 V** (intenção §6, planejamento §3) | idêntico, **depois de corrigir a pinagem do `TL431`** (a extracção de texto tinha trocado cátodo↔REF entre `TL431` e `TL432`; confirmado com a imagem da pág. 4) |
| `RE1`/`RE2` (orçamento de erro) | não recalculado nesta tarefa (fora dos 8 itens pedidos) | 0,237 %/0,165 % (planejamento §2.7c) | sem comparação — não estava no âmbito desta verificação |
| `VSNS` (limiares) | 8,60 V subida / 5,00 V descida, `R1+R2`=16,6 kΩ | **8,6 V / 5,0 V / 16,6 kΩ** (intenção, folha 06 «Porquê») | idêntico |
| TVS terminal (36 V) vs. `IN` do `U60x` (55 V) | clamp 58,1 V > 55 V, exposição indirecta | o autor regista o mesmo facto («Os `D611`-`D616`... ficam a 36 V», sem alegar conformidade contra o abs. máx. de `IN`) | concordância, não é uma correcção |

### Divergências e premissas a rever

| Item | Número do autor | O meu número | Divergência |
|---|---|---|---|
| **`F202`, margem de `RA2`** | **41,7×** (`planejamento_pcb_EBM2_V5.md` §2.6, com `C201`=10 µF só) | **11,6×** (20,1 µF: `C201`+`C640`+`C641`, mais a carga do `U640`) | **Divergência de premissa, não de conta.** O número de 41,7× é da F1 (rev. 3 do planeamento), **antes** de a rev. 2.4 acrescentar `C640` (10 µF), `C641` (100 nF) e o próprio `U640`/`C642` à rede `+24V_ADC`. Nenhum documento que li republica a margem de `F202` depois dessa mudança. A conta correcta, com a netlist actual, dá **11,6×** — ainda cumpre `RA2` (≥10×), mas com muito menos folga do que o texto em vigor sugere, e sensível a uma tolerância de fusível que o fabricante não publica (só «típico»). **Recomendo actualizar esta secção antes do Portão 1.** |
| **`F201`, margem de `RA2`** | **15,3×** (`planejamento_pcb_EBM2_V5.md` §2.6, com `R206`=22 Ω e alimentação a 24 V) | **9,3-12,3×** (com `R206`=**33 Ω** — valor **actual** da netlist — e 32 V, que é o envelope congelado depois de `RA1` ter sido corrigido para 18-32 V) | **Divergência de premissa.** O `planejamento_pcb_EBM2_V5.md` nunca foi actualizado depois de duas mudanças que o afectam directamente: (a) `R206` passou de 22 Ω para 33 Ω (rev. 2.2, «margem de arranque a 32 V», registada só na `intencao_EBM2_V5.md`); (b) o envelope de alimentação passou de 20-28 V para 18-32 V (`RA1`). Refazendo com os valores actuais, a margem-base é 12,3× (cumpre), mas cai a 9,3× se se contar a corrente de arranque do `U200` (o mesmo tipo de termo que a intenção já aplica ao `U640`/`C642` na rama do `F202` — aqui nunca foi aplicado à rama do `F201`). **Este é o achado mais concreto desta revisão**: nenhum documento fecha explicitamente `RA2` para `F201` com os valores hoje em vigor. |
| **Pino do ADC vs. abs. máx. (`V10` da intenção)** | planeamento (§2.7f): «ultrapassa o máximo absoluto em cerca de 0,4 V», depois corrigido para «por confirmar» porque a estimativa de 12,5 mA de corrente de clamp ignorava o burden em paralelo | recalculado para o cenário de curto do `U60x` (não o cenário original de TVS de 30 V que a intenção usava): corrente de clamp ≈0,15-0,2 mA, `3V3_REF`+`V_F(BAV199)`≈4,1-4,2 V contra abs. máx. ≈3,9-3,97 V | **Mesma direcção (excede ligeiramente), cenário diferente.** A intenção nunca fechou este ponto (`V10` continua aberto nos dois documentos); o meu cálculo chega à mesma conclusão qualitativa (margem negativa pequena) por um caminho diferente (o curto do `U60x`, não uma sobretensão de 30 V no TVS de entrada). **Não é uma correcção ao autor — é uma segunda confirmação, por outra via, de que `V10` continua por fechar** e precisa de medição directa. |
| **Estabilidade do `TL431` com a capacitância no cátodo** | não avaliada em nenhum dos dois documentos (nem a fig. 6-18, nem `Imin`) | `Imin`=1 mA (máx.) não garantidamente atingido durante um evento de grampo (~0,15-0,2 mA disponíveis); leitura da fig. 6-18 no limite da minha resolução gráfica para `C_L`=2,4 µF a `IKA` muito baixo | **Item novo, não coberto pelo autor.** Nem a intenção nem o planeamento mencionam a corrente mínima de regulação do `TL431` nem a carta de estabilidade — ambos tratam o `TL431` só pelo valor de grampo (3,60 V). Fica registado como abertura nova para a 2.3b. |
| **Tolerância de `+12V_TPS` (`U640`)** | a intenção só usa o valor típico (12,09 V) | pior caso **11,76-12,44 V** | **Extensão, não correcção.** O autor não computou banda de tolerância para este trilho; a minha banda não muda nenhum veredito (fica sempre dentro de `+Vs` operacional do `U60x`), mas é um número que faltava e que os itens 6 (VSNS) e 5 (dissipação) usam implicitamente. |
| **`D601`-`D606` (retorno) por analogia com `D200`** | a intenção usa o clamp do `D200` (Bourns `SMA6J33A-Q`, 53,3 V) como *proxy* para o `SMBJ33A-13-F` (Diodes Inc., sem datasheet) e conclui «<55 V» | mesma leitura, mas destaco que é uma analogia entre fabricantes diferentes, não uma verificação directa | **Concordância com reserva.** Não é um erro do autor — é uma aproximação razoável dada a ausência do datasheet — mas continua a ser `falta dado` na acepção estrita pedida por este exercício, e a margem (53,3 vs. 55 V, 3 %) é apertada para se apoiar só numa analogia. |

---

## Resumo executivo

**FALHAS / margens que não fecham com confiança:**
1. **`F201` (`RA2`, I²t de arranque a 32 V):** margem entre 9,3× e 12,3× consoante se conta ou não a corrente de arranque do `U200` — **abaixo dos 10× exigidos** num dos dois cenários razoáveis. Nenhum documento da pasta fecha isto com os valores actuais (`R206`=33 Ω, envelope 18-32 V).
2. **Pino do ADC (`MCP3208`, `CH0`-`CH3/6/7`) durante o curto do `U60x` a 32 V:** ligeiramente acima do abs. máx. `VDD+0,6 V` (margem negativa de dezenas a poucas centenas de mV) — coincide com o `V10` já aberto pelo autor, agora confirmado por um segundo caminho de cálculo.

**Margem frágil, mas cumpre:**
3. `F202`: 11,6× (não os 41,7× que o texto em vigor ainda cita) — cumpre `RA2`, mas sensível a uma tolerância de fusível não publicada.

**Falta dado (datasheet ausente na pasta):**
4. `D601`-`D606` (SMBJ33A-13-F, retorno) — clamp real desconhecido; usa-se por analogia o `D200`.
5. `C642` (`C3216X5R1H106K160AB`) e, por extensão, `C640`/`C200` — sem curva de capacidade-vs-polarização-DC/temperatura para confirmar o mínimo de 4,7 µF efectivos do `TPS7A4001` a 12 V/70 °C.

**Divergências com o autor (o dele vs. o meu):**
- `F202`: 41,7× (autor, pré-rev.2.4) vs. **11,6×** (meu, netlist actual) — premissa desactualizada, não erro de conta.
- `F201`: 15,3× a 22 Ω/24 V (autor, F1) vs. **9,3-12,3×** a 33 Ω/32 V (meu, netlist actual) — idem.
- Todo o resto que comparei (headroom a 18 V, curto a 32 V, `U640`, `+5V_ADC`, grampo `TL431`) **confirma** o autor, número a número, depois de eu próprio corrigir dois erros meus a meio do processo (divisor `VSNS` partilhado, e a pinagem do `TL431` DBZ — ambos verificados directamente na netlist e na imagem do datasheet antes de fechar).

**Limite desta revisão:** não recalculei `RE1`/`RE2` (orçamento de erro do ADC), que estava fora dos 8 pontos pedidos e já tem conta própria, extensa, no `planejamento_pcb_EBM2_V5.md` §2.7c.
