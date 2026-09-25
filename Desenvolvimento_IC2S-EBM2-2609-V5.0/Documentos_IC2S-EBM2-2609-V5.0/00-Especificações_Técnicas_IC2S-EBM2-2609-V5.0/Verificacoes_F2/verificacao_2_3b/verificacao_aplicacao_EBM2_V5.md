# Verificação de aplicação dos datasheets — EBM2 V5 (6AI 4-20 mA) · etapa 2.3b

| | |
|---|---|
| Projecto | IC2S Extension Board EBM2 V5, seis entradas 4-20 mA |
| Etapa | F2 · 2.3b — secção de aplicação de cada CI crítico avaliada com os valores da BOM |
| Data | 2026-09-24 |
| Esquemático avaliado | `KiCad_EBM2_V5\IC2S_Extension_Board-EBM2_V5.kicad_sch` (Eeschema 10.0.5), netlist `EBM2_V5.net` exportada 2026-09-24 09:06 (md5 `29a8e75fb2e3`) — **só leitura** |
| Intenção de referência | `intencao_EBM2_V5.md` rev. 2 com correcções 2.1/2.2/2.3 (as contas lá escritas foram tratadas como afirmações a conferir) |
| Envelope | 18–32 V (`RA1`); 0–70 °C de dimensionamento (`RB1`); arranque e dissipação a 32 V, tensão ao transmissor a 18 V |
| Revisor | Sessão nova, **Claude Fable 5.1** (autor do esquemático: Claude Opus 5.5), sem o histórico de autoria. Cumpre a regra «quem desenhou não valida» |
| Método | Skill `2shw-pcb:verificar-aplicacao-datasheet`: cada fórmula e cada nota da secção de aplicação vira uma linha; a tabela é **gerada por avaliação** (`tabela.py` sobre `verificacao_aplicacao_EBM2_V5_rows.json`), nunca escrita à mão; citações por pesquisa no PDF (`grep_datasheet.py`), texto **e** figura renderizada |

> **Veredito da tabela: 132 linhas · 103 cumprem · 17 falham · 12 sem dado.** O `tabela.py` termina com código 1: a etapa **não está fechada**. As 17 falhas estão agrupadas na §0; nenhuma foi encontrada pelo ERC, pelo analisador ou pela verificação de pinagem da 2.3, porque nenhuma é um erro de ligação — são valores da BOM contra limites do datasheet.

---

## 0 · O que não cumpre, por ordem de consequência

### 0.1 Falhas que pedem decisão antes do Portão 1

| # | Onde | O que o datasheet diz | O que a BOM dá | Consequência | Caminhos possíveis (decisão do projectista) |
|---|---|---|---|---|---|
| **F1** | `U601`-`U606` AL5809-25, transmissor em curto | DS36625 pág. 8: «junction temperature must be kept ≤ +125 °C»; θJA 148,6 °C/W com a ilha mínima (nota 4), 81,4 °C/W com 25,4 × 25,4 mm de cobre em GETEK (nota 5) | A 32 V e 70 °C: V_InOut 25,5 V × 26,9 mA = **0,69 W** → Tj **172 °C** (nota 4) ou **126 °C** (nota 5). A 24 V: **140 °C** (nota 4), 108 °C (nota 5). A fig. 9 (placa de aplicação FR4) só admite 0,50 W a 70 °C, e isso já com Tj = 145 °C | O corte térmico (165 °C, histerese 30 °C) entra em ciclo: a corrente do laço alterna 0 ↔ 27 mA e a leitura 0 ↔ 4095 enquanto o curto durar. A peça protege-se; o critério do datasheet não se cumpre com nenhuma ilha realizável a 32 V | (a) aceitar o ciclo térmico como comportamento de falha, documentá-lo e ensaiar em bancada a 32 V/70 °C; (b) repartir a dissipação com uma resistência em série de potência antes do limitador (custa tensão ao transmissor a 18 V — `V9`); (c) outra topologia de limitação. A intenção já registou «Tj ≈ 141 °C … cobre obrigatório»; **a conta com a envolvente corrigida dá pior** |
| **F2** | `U601`-`U606` AL5809-25, operação normal 4–20 mA | DS36625 pág. 4: condições recomendadas V_InOut **2,5 a 60 V**; fig. 15 (25 mA): corrente nula abaixo de ~1,35 V, 20 mA a ≈1,6 V, típico a 25 °C | O laço trabalha com 1,45–1,6 V no limitador **o tempo todo** | O comportamento abaixo de 2,5 V não tem mín./máx. nem temperatura no datasheet: a queda que sobra ao transmissor (`V9`) só se fecha por cota (2,5 V) ou por bancada. A regulação nunca actua abaixo de 23,75 mA, logo a medida não é afectada, mas ruído/estabilidade nesta região não estão caracterizados | caracterizar em bancada a queda a 4 e 20 mA a 0/25/70 °C nas seis peças (ou aceitar a cota de 2,5 V no `V9`) |
| **F3** | `U203` TL431B como grampo de `3V3_REF` | SLVS543S §9.4 pág. 31: «be sure that the capacitance is within the stability criteria shown in Figure 6-16 and 6-18»; fig. 6-18 pág. 18 (TL431B/SOT-23/Q): curva A (V_KA = V_ref) instável entre ~0,02 µF e ~6 µF; a 3,6 µF a fronteira está em ≈25 mA; curva B (5 V) estável acima de ~1,5 µF | C_L no cátodo = C204 2,2 + C205 0,1 + C206 0,1 + C403 0,1 + C501 1,0 + C502 0,1 = **3,6 µF** cerâmico; V_KA = 3,6 V (entre A e B); I_K de 3 a 21 mA | Só actua em falha (grampo), mas quando actua pode oscilar: `3V3_REF` (e com ele `VDD` do ADC e `VCC2` do isolador) a oscilar durante a falha | (a) subir a capacidade de `3V3_REF` para ≥ 10 µF (zona estável à direita da curva A) — obriga a confirmar em bancada a estabilidade do SPX3819 com 10 µF cerâmico (`F8`); (b) ensaio de bancada do grampo com 1 e 6 canais em falha; (c) SLVA482 |
| **F4** | `U203` TL431B, nível do grampo (`RA4` ≤ 3,7 V) | SLVS543S §6.13 pág. 14 (TL431BQ): V_ref 2,483–2,507 V, VI(dev) 34 mV, I_ref 4 µA, \|Z_KA\| 0,5 Ω; §9.2.2.2.1 pág. 26: V_o = (1 + R1/R2)·V_ref ± I_ref·R1 | R204 4k42, R205 10k **sem MPN** (tolerância assumida 1 %): V_o nominal 3,616 V; **máximo 3,715 V** > 3,70 V; mínimo 3,510 V (> 3,366 V de `3V3_REF` máximo: o grampo está desligado em operação normal, cumpre) | `RA4` falha por 15 mV no pior caso | R204/R205 a **0,1 %** (máximo 3,694 V) ou recentrar (R204 4k32 → nominal 3,56 V, mínimo 3,46 V) |
| **F5** | `U401` MCP1824S, entrada `+5V` do barramento (`V13`) | DS22070A pág. 7: máximo absoluto V_IN **6,5 V**; operação 2,1–6,0 V | O único tecto garantido no `+5V_IC` da base board é o grampo do TVS `D53`: V_BR 6,7 V, grampo **9,2 V** (leitura da netlist da base board V2.3, herdado da intenção) | Um transitório entre 6,5 e 9,2 V chega ao pino. Falha **condicionada à existência do transitório**; não há medição do barramento | (a) medir o `+5V_IC` com transitórios de carga/ligação no painel; (b) LDO com máximo absoluto ≥ 10 V; (c) resistência série + grampo local a ≤ 6 V. Na V4.1 era o próprio ISO7141 (6 V) que estava nesta linha |
| **F6** | `C207` (saída do ADR4525) e `C402` (saída do MCP1824) | ADR45xx Rev. G Tabela 11 pág. 35: C_OUT **mínimo 1,0 µF**; Tabela 2: load capacitance 1–100 µF. DS22070A §4.3 pág. 19: C_OUT **mínimo 1 µF** | 1,0 µF nominal em ambos, **sem MPN**. Com −10 % de tolerância: 0,99 µF (C207 + C500) e 0,90 µF (C402) — antes de descontar polarização DC e temperatura | Nominal igual ao mínimo não é margem: qualquer peça real fica abaixo do que o datasheet exige para estabilidade | 2,2 a 4,7 µF em ambos (a aplicação típica do MCP1824, pág. 3 e 21, usa 4,7 µF; o ADR4525 aceita até 100 µF, à custa de tempo de arranque) |
| **F7** | `F201` CC12H250mA, `RA2` (I²t ≥ 10×) a 32 V | Eaton 4309 pág. 2: I²t pré-arco típico 0,00038 A²s. SBVS162B pág. 5: I_LIM do TPS7A4001 51–200 mA; **não existe arranque suave** (pesquisa «soft»: 0 ocorrências) — o planejamento §5 afirma «arranque suave próprio», e isso não consta | Arranque = C200 2,2 µF por R206 33 Ω + fusível 3,5 Ω (3,09·10⁻⁵ A²s) **mais** a carga de C202 10 µF pelo limitador do regulador a 200 mA (1,0·10⁻⁵ A²s) = 4,09·10⁻⁵ → margem **9,3×** (I_LIM máximo) / 10,4× (I_LIM típico 117 mA) / 13,9× a 24 V | O planejamento §2.6 só contou o C200; com a envolvente a 32 V o critério fica no fio | R206 = **47 Ω** dá 11,8× no pior caso (custa 0,41 V de queda a 8,7 mA — irrelevante para os 7 V mínimos do TPS7A4001) |
| **F8** | `C202` (saída do TPS7A4001) | SBVS162B §8.2.2.2 pág. 11: C_OUT **≥ 4,7 µF** para estabilidade, 10 µF recomendado | 10 µF/25 V em **0603** (X5R por construção), **sem MPN**. A perda por polarização DC a 5 V num 0603 deste valor é tipicamente 40–60 % | Sem MPN não se prova ≥ 4,7 µF efectivos; o risco é de instabilidade do regulador que alimenta toda a cadeia analógica | 10 µF X7R em 0805/1206 (≥ 25 V), ou dois em paralelo; fixar o MPN e verificar a curva de polarização |
| **F9** | `U601`-`U606` AL5809 com `D641`-`D646` BAT46W (resíduo de −0,4 V, pedido no LEIA-ME) | DS36625 pág. 3: V_InOut mínimo absoluto **−0,3 V**. DS30044 pág. 2: V_F do BAT46W 0,25 V a 0,1 mA e 0,45 V a 10 mA (máximos, 25 °C); fig. 1 pág. 3: a 0 °C sobe ~0,04 V | A ~3 mA de corrente inversa: V_F ≈ **0,40 V** (25 °C) a **0,44 V** (0 °C) → o limitador vê −0,40 a −0,44 V | Resíduo **confirmado**: 0,10–0,14 V acima do máximo absoluto. O BAT46W só cumpriria com corrente inversa < ~1 mA. A própria corrente inversa da falha depende da V_F directa do TVS 824520361, que **não consta** no PDF Würth | (a) Schottky de V_F menor a 3 mA (confirmar no datasheet da alternativa, não de memória); (b) aceitar, com argumento de raridade da falha e ausência de rating de energia; (c) pedir à Diodes o comportamento em inversa |
| **F10** | `U500` MCP3208, entradas, quando o `BAV199` conduz (`V10`) | DS21298E pág. 2: entradas −0,6 V a **V_DD + 0,6 V**. BAV199LT1/D pág. 2: V_F 0,90 V a 1 mA, 1,00 V a 10 mA (máx.) | O grampo liga o pino à **mesma rede** que alimenta V_DD (`3V3_REF`, com ou sem ferrite). Sempre que o BAV199 conduz mais de ~0,1 mA, V_pino = `3V3_REF` + V_F > V_DD + 0,6 **por construção**: com 3,4 mA, 4,67 V contra 4,32 V | **Em operação normal e com o limitador a regular, o BAV199 nunca conduz em DC** (V_MED máximo 2,96 V < 3,23 + 0,6): cumpre. Falha só com o limitador em curto ou em transitórios mais rápidos que o limitador. Aí a corrente reparte-se com os díodos internos do ADC (fig. 4-1), sem rating no datasheet | Topologia herdada da V4.1. (a) aceitar como falha dupla; (b) grampo a uma rede ≥ 0,4 V abaixo de V_DD (não existe hoje); (c) Schottky duplo em vez do BAV199 — mas a fuga de um Schottky a 70 °C (µA) sobre 3,41 kΩ vale vários LSB, e é por isso que o BAV199 (nA) está lá. Não há solução sem custo |

### 0.2 Falhas informativas (não pedem alteração, ficam registadas)

| # | Onde | Achado |
|---|---|---|
| F11 | `U500` MCP3208, fuga analógica | O **máximo** de datasheet (±1 µA, pág. 3) sobre R_S = 3,41 kΩ dá 3,4 mV = **5,6 LSB** de offset. É um offset DC por unidade, removido pela calibração de 6 pontos por canal; a **deriva** com a temperatura (fig. 2-39: ≈1–2 nA até 100 °C) vale ≈0,005 LSB e cumpre `RE2`. Registar no plano de teste que o offset de fábrica pode chegar a 5,6 LSB antes de calibrar |
| F12 | `RA4` com falha dupla (limitador em curto + 30 V injectados) | Sem o limitador, I = 30/(100+110) = 143 mA → **2,2 W em R611 e 2,0 W em R601** (1206). É exactamente o cenário da V4.1 que o `V8` corrigiu; fica como confirmação de que o AL5809 é a única protecção das resistências |
| F13 | `V7`, surto 10/1000 µs pela entrada | Com o D200 a grampear a 53,3 V, cada TVS de canal partilha ≈1,39 A pelo fusível de 9,2 Ω: em 8/20 µs o I²t (2,7·10⁻⁵ A²s) cabe nos 2·10⁻⁴ A²s do fusível; em **10/1000 µs (1,4·10⁻³ A²s) os seis fusíveis de canal abrem**. Sem requisito de surto (`RA3` reescrito) não é falha de projecto; é consequência a documentar |
| F14 | `U200` TPS7A4001 | «Arranque suave próprio» (planejamento §5) **não existe** no SBVS162B; entra na conta de F7 |
| F15 | `U601`-`U606` AL5809, fig. 10 | A fig. 10 admite ≈35 V a 70 °C para a versão de 25 mA, mas a figura é traçada para Tj = 145 °C, acima dos 125 °C que a pág. 8 impõe. A intenção citou-a a favor; **não pode ser usada como critério** |

### 0.3 Sem dado (12 linhas) — a primeira lista de perguntas ao projectista

| Falta | Linhas | Porque interessa |
|---|---|---|
| **MPN de C200, C202, C204, C207, C402, R204, R205, R206** | TPS7A4001 C_IN/C_OUT, SPX3819, ADR4525, MCP1824, TL431, R206 | Sem MPN não há curva de polarização DC (condensadores), tolerância (divisor do grampo) nem curva de impulso (R206: **1,13 mJ, 31 W de pico em 73 µs** a 32 V — exige série anti-surge) |
| Estabilidade do SPX3819 com cerâmico | U201 | O PDF rev. 2.0.5 só fala de electrolítico/tântalo e manda para a bancada; a V4.1 é evidência de campo, não especificação |
| V_OH do MCP3208 a V_DD = 3,3 V | U400 IND | Só está especificado a 4,5 V (4,1 V mín.); o ISO7141 pede ≥ 2,0 V. Saída CMOS, esperado ≈ V_DD − 0,1 V |
| Níveis do Raspberry Pi / base board | U400 INA/INB/INC, OUTD | Datasheet não está na pasta |
| Distância dos 100 nF aos pinos VCC1/VCC2 | U400 | «2 mm max» (fig. 20) — é da F3 |
| t_CSH e continuidade da transacção de 24 bits | U500 | Firmware (backend `expander.js`): CS alto ≥ 500 ns entre conversões e frame contínuo (a §6.2 dá 1,2 ms para os 13 relógios = 0,65 ms a 20 kHz) |
| V_F directa do 824520361 | U60x inversa | Não consta no PDF Würth; determina a corrente inversa real de F9 |
| Resposta do AL5809 a um degrau com o dispositivo já em condução | U60x | Só há t_ON 500 µs de arranque; num surto a frente de onda passa até R601/R611/BAV199 |
| Potência nominal de R611 (ERA8AEB) e R601 (RC1206) | R611/R601 | Datasheets não estão na pasta 2.3b (o escopo cita AOA0000C307); esperado 0,25 W contra 80/72 mW em curto |
| Tensão mínima dos transmissores instalados | `V9` | A 18 V e 20 mA sobram **10,5 V** (cota de 2,5 V no AL5809) ou 11,4 V (típico) |

---

## 1 · Âmbito: CI críticos e PDF usados

Todos os PDF estão em `datasheets\` (md5 em `LISTA.md`). Páginas indicadas = as pesquisadas e citadas; as figuras marcadas com † foram renderizadas e lidas na imagem, não só no texto extraído.

| Ref. | Peça | Ficheiro | Revisão | Páginas usadas |
|---|---|---|---|---|
| `U200` | TPS7A4001DGNR | `TPS7A4001__TI_TPS7A4001.pdf` | SBVS162B, jul-2015 | 4, 5, 10, 11, 12, 13, 14; pesquisa «soft» em todo o PDF |
| `U201` | SPX3819M5-L-3-3/TR | `SPX3819__1016_SPX3819.pdf` | rev. 2.0.5, dez-2019 | 1, 2, 3, 7, 8 |
| `U202` | ADR4525BRZ | `ADR4525__adr4520_4525_….pdf` | Rev. G | 4, 5, 10, 35, 36, 37, 38, 39 |
| `U203` | TL431BQDBZR | `TL431__TI_TL431.pdf` | SLVS543S, mai-2024 | 5, 6, 12, 13, 14, 17†, 18† (fig. 6-18), 23, 24, 25, 26, 31 |
| `U400` | ISO7141CCDBQR | `ISO7141__TI_ISO7141CC.pdf` | SLLSE83F, jan-2015 | 1, 4, 5, 6, 7, 8, 9, 10, 21, 22, 25 |
| `U401` | MCP1824ST-3302E/DB | `MCP1824__22070a.pdf` | DS22070A, 2007 | 3, 7, 8, 9, 17, 18, 19, 20, 21, 22 |
| `U500` | MCP3208T-BI/SL | `MCP3208__21298e.pdf` | DS21298E, 2008 | 2, 3, 4, 13, 15, 17, 18, 19, 20, 21, 22, 23 |
| `U601`-`U606` | AL5809-25P1-7 | `AL5809__AL5809.pdf` | DS36625 Rev. 5-2, dez-2016 | 1, 2, 3, 4, 5, 8† (fig. 9-11), 10† (fig. 14-19), 11†, 12 |
| `D621`-`D626` | BAV199LT1G | `BAV199__BAV199LT1-D.PDF` | Rev. 12, ago-2024 | 1, 2, 3† (fig. 2, 4) |
| `D641`-`D646` | BAT46W-7-F | `BAT46W__….pdf` | DS30044 Rev. 20-2, nov-2023 | 1, 2, 3† (fig. 1) |
| `D200` | SMA6J33A-Q | `SMA6J33A__Bourns_SMA6J33A-Q.pdf` | Bourns | 1, 2, 3 |
| `D601`-`D616` | 824520361 (SMBJ36A) | `824520361__Wurth_….pdf` | 001.003, 2023-11-24 | 1, 2, 3, 4, 8 |
| `D201`, `D202` | MBR1H100SFT3G | `MBR1H100SF__….pdf` | Rev. 3, jan-2025 | 1, 2, 3† (fig. 2) |
| `F201`, `F202` | CC12H250mA-TR, CC12H750mA-TR | `Eaton_fusible_lento.pdf` | Technical Data 4309, jul-2023 | 1, 2, 6† (derating) |
| `F601`-`F606` | 3413.0002.22 | `Schurter_USFF1206_3413.pdf` | 21.07.2026 | 1, 3† (derating, tabela), 4 |
| `R700` | NTCS0603E3103JLT | `ntcs0603e3t.pdf` | Vishay 29056, mai-2024 | 1, 2 |
| `D203`, `D204`, `D630` | KG EELP41.22-PHRH-35-A8J8-20-R18 | `KG_EELP41.22__KG-EELP41-22.pdf` | v1.4, 2026-08-07 | V_F @ 20 mA (grupo mínimo 1,60 V) |

Fora do âmbito por não estarem na pasta: Panasonic ERA8/ERA3 (burden, R701), Yageo RC0603/RC1206, Murata BLM18PG471SN1D e GRM, Harwin M20 (só o plano mecânico), base board V2.3 e Raspberry Pi. Onde um valor deles foi preciso, a linha diz «não está na pasta» e o veredito é *falta dado*, não *cumpre*.

Valores da BOM: extraídos da netlist com `bom_values.py --around` para cada CI (rede de cada pino e peças a um salto). Herdados da V4.1 (`[INHERITED]`): topologia do canal (série + burden + antialias + BAV199), MCP3208, ISO7141, SPX3819, ferrites, NTC e divisor. Cada um foi re-derivado contra este circuito, não aceite por herança.

---

## 2 · Tabela de verificação (gerada por `tabela.py`)

Comando: `python tabela.py verificacao_aplicacao_EBM2_V5_rows.json --lang pt`. As linhas em **FALHA** e **falta dado** estão discutidas na §0. Convenções dos valores: tensões em V, correntes em A, capacidades em F, resistências em Ω, temperaturas em °C, potências em W. `I_SHORT` = 26,9 mA (26,25 mA máximo da tabela do AL5809 + 2,5 % da fig. 17). `V24ADC` = tensão em `+24V_ADC` com os seis canais em curto. `I_REG` = 8,73 mA (carga do `+5V_ADC`, máximos de datasheet somados).

| CI | fonte (§/tabela/nota, pág.) | fórmula | valores usados | resultado | veredito |
|---|---|---|---|---|---|
| U200 TPS7A4001 | SBVS162B §6.3 Rec. Op., p.4 | `VIN >= 7 V (mín. recomendado)` | VIN_MIN=18.000, R_F201=3.500, VF_D201=0.45, R206=33.000, I_REG=0.008734 entrada a 18 V (RA1) | VIN_MIN - R_F201*I_REG - VF_D201 - R206*I_REG = 17.231 | cumpre |
| U200 TPS7A4001 | SBVS162B §6.1 Abs. max, p.4 | `IN, EN <= 105 V (abs.) ; §6.3 VIN <= 100 V` | VC_D200=53.300 no grampo do D200 (Bourns p.2, I_PP 11,3 A) | VC_D200 = 53.300 | cumpre |
| U200 TPS7A4001 | SBVS162B §8.1.1 Eq.1 / Fig.13, p.10 | `VOUT = VREF x (1 + R1/R2)  [R1=R201 OUT→FB, R2=R202 FB→GND]` | VREF=1.173, R1=3.24e+04, R2=1e+04 | VREF*(1+R1/R2) = 4.974 | cumpre |
| U200 TPS7A4001 | SBVS162B §6.5 nota(1) p.5 + §8.1.1 p.10 | `VOUT/(R1+R2) >= 10 µA (estabilidade sem carga)` | VOUT=4.974, R1=3.24e+04, R2=1e+04 | VOUT/(R1+R2) = 0.0001173 | cumpre |
| U200 TPS7A4001 | SBVS162B §8.2.2, p.11 | `R1 + R2 <= 500 kΩ (máx. de realimentação)` | R1=3.24e+04, R2=1e+04 | R1+R2 = 4.24e+04 | cumpre |
| U200 TPS7A4001 | SBVS162B §6.5 p.5 (VREF 1,161–1,185) + R ±1 % | `banda de +5V_ADC = VREF_min/max x (1 + R1/R2) com R1/R2 ±2 %` | VREF_MIN=1.161, VREF_MAX=1.185, ratio=3.240 limites: VIN mín do SPX3819 = 3,3+0,25 V ; VIN máx SPX3819 16 V | VREF_MIN*(1+ratio*0.98) = 4.847 ; VREF_MAX*(1+ratio*1.02) = 5.101 | cumpre |
| U200 TPS7A4001 | SBVS162B §6.1 Abs. max, p.4 | `FB pin <= 2 V` | V_FB=1.185 | V_FB = 1.185 | cumpre |
| U200 TPS7A4001 | SBVS162B §8.2.2.2, p.11 | `COUT >= 4,7 µF (mín. p/ estabilidade; 10 µF recomendado) — capacidade EFECTIVA a 5 V` | C202_nominal=1e-05, C202_efectiva_5V=? C202 = 10 µF/25 V em 0603 (X5R): perda por polarização DC a 5 V tipicamente 40–60 %; sem MPN não se prova ≥ 4,7 µF | missing: C202_efectiva_5V | **falta dado** |
| U200 TPS7A4001 | SBVS162B §8.2.2.2, p.11 (+ §9 p.12: 10 µF junto ao pino) | `CIN >= 1 µF — capacidade EFECTIVA a 32 V` | C200_nominal=2.2e-06, C200_efectiva_32V=? V6 aberta: sem MPN de C200 não há curva de polarização; §9 recomenda 10 µF | missing: C200_efectiva_32V | **falta dado** |
| U200 TPS7A4001 | SBVS162B §8.2.2.3, p.11 | `CBYP = 10 nF entre FB e OUT («highly recommended», não exigido p/ estabilidade)` | CBYP_nF=0 [RECOMENDAÇÃO AUSENTE] sem CBYP a resposta ao transitório de linha é a da fig.15 sem CBYP (~10x pior) | CBYP_nF = 0 | cumpre |
| U200 TPS7A4001 | SBVS162B §10.4 Eq.2 + §6.4 RθJA 66,7 °C/W, p.4/14 | `PD = (VIN−VOUT)·IOUT + VIN·IGND ; TJ = 70 + PD·RθJA <= 125 °C` | V_REG=31.231, VOUT=4.974, I_REG=0.008734, I_GND=6.5e-05, RthJA=66.700, TA=70.000 a 32 V; I_REG soma ICC2 ISO7141 4,9 + MCP3208 0,4 + ADR4525 1,42 + SPX 0,25 + LED 1,58 + divisor 0,12 mA | (V_REG-VOUT)*I_REG + V_REG*I_GND = 0.2314 ; TA + ((V_REG-VOUT)*I_REG + V_REG*I_GND)*RthJA = 85.432 | cumpre |
| U200 TPS7A4001 | SBVS162B §6.5 nota(2), p.5 | `«VIN limitado a 24 V pela dissipação a plena carga (50 mA)» → PD(32 V, carga real) <= (24−VREF)·50 mA = 1,14 W` | V_REG=31.231, VOUT=4.974, I_REG=0.008734 a nota permite >24 V se a dissipação couber | (V_REG-VOUT)*I_REG = 0.2293 | cumpre |
| U200 TPS7A4001 | SBVS162B §10.3, p.14 | `protecção térmica (170 °C) deve disparar >= 45 °C acima da ambiente máxima` | TSD=170.000, PD=0.2293, RthJA=66.700, TA=70.000 | TSD - PD*RthJA = 154.703 | cumpre |
| U200 TPS7A4001 | SBVS162B §6.3, p.4 | `IOUT <= 50 mA` | I_REG=0.008734 | I_REG = 0.008734 | cumpre |
| U200 TPS7A4001 | SBVS162B §6.5 p.5 | `VEN_HI >= 1,5 V (EN ligado a IN)` | V_REG_18=17.231 | V_REG_18 = 17.231 | cumpre |
| U200 TPS7A4001 | SBVS162B — pesquisa «soft»: 0 ocorrências | `arranque suave («arranque suave próprio», planejamento §5) — existe no datasheet?` | ocorrencias_soft=0 não consta: o arranque só é limitado por ILIM 51–200 mA (p.5) | ocorrencias_soft = 0 | **FALHA** |
| U201 SPX3819 | SPX3819 Operating Ratings, p.2 | `2,5 V <= VIN <= 16 V (V2 da intenção)` | V5_MIN=4.847, V5_MAX=5.101 | V5_MIN = 4.847 ; V5_MAX = 5.101 | cumpre |
| U201 SPX3819 | SPX3819 Abs. Max, p.2 | `VIN, EN dentro de −20..+20 V` | V5_MAX=5.101 | V5_MAX = 5.101 | cumpre |
| U201 SPX3819 | SPX3819 p.3 VIH >= 2,0 V ; I_EN máx 20 µA | `V_EN = VIN − I_EN·R203 >= 2,0 V` | V5_MIN=4.847, I_EN=2e-05, R203=1e+05 | V5_MIN - I_EN*R203 = 2.847 | cumpre |
| U201 SPX3819 | SPX3819 p.2 Dropout (• sobre temp.) 250 mV @ 50 mA | `VIN − VOUT >= 0,25 V` | V5_MIN=4.847, V33_MAX=3.366 | V5_MIN - V33_MAX = 1.481 | cumpre |
| U201 SPX3819 | SPX3819 p.7 «requires an output capacitor»; especificações com CL = 1 µF | `COUT >= 1 µF (valor)` | C204=2.2e-06 sem MPN de C204 | C204 = 2.2e-06 | cumpre |
| U201 SPX3819 | SPX3819 p.7 «2,2 µF aluminium… 1 µF tantalum… bench testing is the best method» | `estabilidade com condensador CERÂMICO de baixa ESR — especificada?` | ESR_min_especificada=? não está neste PDF (rev 2.0.5). [INHERITED] a V4.1 usa o mesmo LDO (U11) com cerâmicos — evidência de campo, não especificação | missing: ESR_min_especificada | **falta dado** |
| U201 SPX3819 | SPX3819 p.3 / p.7 | `BYP = 10 nF` | C208=1e-08 | C208 = 1e-08 | cumpre |
| U201 SPX3819 | SPX3819 nota 1 p.2: PD(max) = (TJ(max)−TA)/θJA, θJA(SOT23-5) 191 °C/W | `PD = (VIN−VOUT)·IL + VIN·IGND <= (125−70)/191` | V5_MAX=5.101, VOUT=3.300, IL=0.00672, IGND=0.00025, thJA=191.000, TA=70.000 | (V5_MAX-VOUT)*IL + V5_MAX*IGND = 0.01338 ; (125-TA)/thJA = 0.288 | cumpre |
| U201 SPX3819 | SPX3819 p.2 tolerância ±2 % (•) | `banda 3V3_REF = 3,3 V ±2 % → 3,234..3,366 V (usada nas linhas seguintes)` | V33_MIN=3.234, V33_MAX=3.366 + regulação de linha 0,2 %/V·(5,08−4,3)=0,16 % e de carga 0,4 % não somadas | V33_MIN = 3.234 ; V33_MAX = 3.366 | cumpre |
| U202 ADR4525 | ADR45xx Rev.G Tabela 2, p.4: «VIN = 3 V to 15 V»; VDO <= 500 mV | `3V3_REF_min >= VOUT + VDO = 2,5 + 0,5 = 3,0 V` | V33_MIN=3.234, VOUT=2.500, VDO=0.5 margem 0,234 V; ligação directa (sem ferrite) | V33_MIN - (VOUT+VDO) = 0.234 | cumpre |
| U202 ADR4525 | ADR45xx Rev.G Tabela 11 p.35: COUT mín 1,0 µF ; Tabela 2 p.5: load capacitance 1..100 µF | `C207 + C500 com tolerância −10 % >= 1,0 µF` | C207=1e-06, C500=1e-07, tol=0.1 1,0 µF nominal É o mínimo: qualquer tolerância fica abaixo, antes de polarização DC e temperatura; sem MPN de C207 | (C207+C500)*(1-tol) = 9.9e-07 | **FALHA** |
| U202 ADR4525 | ADR45xx Rev.G p.35 Input Capacitors | `CIN 1..10 µF + 0,1 µF cerâmico em paralelo` | C_in_bulk=2.2e-06, C_in_hf=1e-07 C204 + C205/C206 na rede 3V3_REF; a colocação junto ao pino 2 é da F3 | C_in_bulk = 2.2e-06 | cumpre |
| U202 ADR4525 | ADR45xx Rev.G Tabela 2 p.4: IL sourcing <= 10 mA | `I_VREF(MCP3208 máx 150 µA) + I_NTC(70 °C) <= 10 mA` | I_VREF=0.00015, R_NTC_70=2210, R701=5620, VREF=2.500 | I_VREF + VREF/(R_NTC_70+R701) = 0.0004693 | cumpre |
| U202 ADR4525 | ADR45xx Rev.G Tabela 2 p.4: load regulation 80 ppm/mA (máx) — interacção com o divisor NTC | `ΔI_NTC(0→70 °C)·80 ppm/mA <= 1 LSB (244 ppm)` | VREF=2.500, R_NTC_0=2.87e+04, R_NTC_70=2210, R701=5620, LR=80.000 ppm; erro comum a todos os canais | (VREF/(R_NTC_70+R701) - VREF/(R_NTC_0+R701))*1e3*LR = 19.715 | cumpre |
| U202 ADR4525 | ADR45xx Rev.G p.35 Power Dissipation: PD = (TJ−TA)/θJA ; Tabela 8 p.10 θJA 120 °C/W (2 camadas) | `PD = (VIN−VOUT)·IL + VIN·IQ <= (125−70)/120` | V33_MAX=3.366, VOUT=2.500, IL=0.00047, IQ=0.00095, thJA=120.000, TA=70.000 | (V33_MAX-VOUT)*IL + V33_MAX*IQ = 0.003605 | cumpre |
| U202 ADR4525 | ADR45xx Rev.G Tabela 7 p.10 Abs. max supply 16 V | `3V3_REF grampeado <= 16 V` | V_CLAMP_MAX=3.716 | V_CLAMP_MAX = 3.716 | cumpre |
| U202 ADR4525 | ADR45xx Rev.G Tabela 2 p.4: TCVOUT B grade 4 ppm/°C (bowtie) | `deriva 25→70 °C = 4·45 ppm <= orçamento RE2 (2000 ppm)` | TC=4.000, dT=45.000 ppm | TC*dT = 180.000 | cumpre |
| U202 ADR4525 | ADR45xx Rev.G Tabela 2 p.4: histerese térmica 25→70→0→25 °C: −8 ppm (típ.) | `∣hist∣ <= 1 LSB (244 ppm)` | hist=8.000 ppm, típico — não é limite | hist = 8.000 | cumpre |
| U203 TL431B | SLVS543S §9.2.2.2.1 p.26: Vo = (1+R1/R2)·Vref ± Iref·R1  [R1=R204, R2=R205] | `Vo nominal <= 3,7 V (RA4)` | VREF=2.495, R204=4420, R205=1e+04, IREF=4e-06 | (1+R204/R205)*VREF + IREF*R204 = 3.615 | cumpre |
| U203 TL431B | SLVS543S §6.13 p.14 (TL431BQ): Vref 2,483–2,507; VI(dev) 34 mV; Iref 4 µA; ∣Z_KA∣ 0,5 Ω  + R ±1 % | `Vo máx = (1+R1·1,01/(R2·0,99))·(Vref_max+VI(dev)) + Iref·R1 + ZKA·I_K <= 3,7 V (RA4)` | VREF_MAX=2.507, VIDEV=0.034, R204=4420, R205=1e+04, IREF=4e-06, ZKA=0.5, I_K=0.02021 tolerância 1 % ASSUMIDA (R204/R205 sem MPN); com 0,1 % dá 3,695 V e cumpre | (1+R204*1.01/(R205*0.99))*(VREF_MAX+VIDEV) + IREF*R204*1.01 + ZKA*I_K = 3.715 | **FALHA** |
| U203 TL431B | SLVS543S §6.13 p.14 — mínimo do grampo vs máximo de 3V3_REF | `Vo mín = (1+R1·0,99/(R2·1,01))·(Vref_min−VI(dev)) > 3V3_REF_max (TL431 desligado em operação normal)` | VREF_MIN=2.483, VIDEV=0.034, R204=4420, R205=1e+04, V33_MAX=3.366 | (1+R204*0.99/(R205*1.01))*(VREF_MIN-VIDEV) = 3.510 ; V33_MAX = 3.366 | cumpre |
| U203 TL431B | SLVS543S §6.4 p.5: IKA 1..100 mA ; §6.13 Imin 0,7 mA | `corrente de grampo por canal (limitador em curto, 30 V) e total de 6 canais dentro de 1..100 mA` | I_CH=0.003368, I_TOT=0.02021 | I_CH = 0.003368 ; I_TOT = 0.02021 | cumpre |
| U203 TL431B | SLVS543S §6.13 p.14: Ioff <= 0,5 µA (VKA = 36 V) | `consumo do grampo desligado em operação normal desprezável (<1 % de IQ do ADR4525)` | IOFF=5e-07, IQ_ADR=0.0007 | IOFF = 5e-07 | cumpre |
| U203 TL431B | SLVS543S §9.4 p.31 «be sure that the capacitance is within the stability criteria shown in Figure 6-16 and 6-18»; Fig.6-18 p.18 | `C_L no cátodo fora da zona de oscilação: C_L <= 0,01 µF ou C_L >= 6 µF (curva A, VKA=Vref; a 3,6 µF a curva A está em ≈25 mA)` | C_L=3.6e-06 C204+C205+C206+C403+C501+C502 (ferrites transparentes a <1 MHz). VKA = 3,6 V fica entre a curva A (Vref) e a B (5 V, estável acima de ~1,5 µF): não demonstrável estável a 3–21 mA; só a bancada ou C_L ≥ 10 µF fecham | C_L = 3.6e-06 | **FALHA** |
| U203 TL431B | SLVS543S §6.3 p.5 RθJA(DBZ) 206 °C/W ; §6.4 nota(1) PD = (TJ−TA)/θJA | `PD = Vo·I_K(6 canais) <= (125−70)/206` | Vo=3.716, I_K=0.02021, thJA=206.000, TA=70.000 | Vo*I_K = 0.07509 ; (125-TA)/thJA = 0.267 | cumpre |
| U400 ISO7141 | SLLSE83F §6.3 p.5: VCC1,VCC2 2,7..5,5 V ; §9.1 p.21 «3 V to 5.5 V» | `VCC1 (MCP1824 ±2,5 %) dentro de 3,0..5,5 V` | VCC1_MIN=3.217, VCC1_MAX=3.382 | VCC1_MIN = 3.217 ; VCC1_MAX = 3.382 | cumpre |
| U400 ISO7141 | SLLSE83F §6.3 p.5 / §9.1 p.21 | `VCC2 = 3V3_REF − R_DC(FB400)·ICC2 dentro de 3,0..5,5 V` | V33_MIN=3.234, R_FB=0.3, ICC2=0.0049 R_DC do BLM18PG471SN1D ≈ 0,3 Ω (não está na pasta; estimativa) | V33_MIN - R_FB*ICC2 = 3.233 | cumpre |
| U400 ISO7141 | SLLSE83F §6.1 p.5 Abs. max VCC 6 V | `VCC2 durante o grampo do TL431 <= 6 V` | V_CLAMP_MAX=3.716 | V_CLAMP_MAX = 3.716 | cumpre |
| U400 ISO7141 | SLLSE83F §6.7 p.6: VOH >= VCC−0,5 V (IOH=−4 mA) ; DS21298E p.3: VIH(MCP3208) = 0,7·VDD | `OUTA/B/C → DIN/CLK/CS: VCC2_min − 0,5 >= 0,7·VDD_ADC_max` | V33_MIN=3.234, V33_MAX=3.366 | V33_MIN - 0.5 = 2.734 ; 0.7*V33_MAX = 2.356 | cumpre |
| U400 ISO7141 | SLLSE83F §6.3 p.5: VIH >= 2,0 V (IND) ; DS21298E p.3: VOH só especificado a VDD=4,5 V (4,1 V) | `DOUT(MCP3208 a 3,3 V) >= 2,0 V` | VOH_MCP3208_3V3=? DS21298E não especifica VOH a 3,3 V; saída CMOS, esperado ≈ VDD−0,1 V; não garantido por datasheet | missing: VOH_MCP3208_3V3 | **falta dado** |
| U400 ISO7141 | SLLSE83F §6.3 p.5: VIH >= 2,0 V, VIL <= 0,8 V (INA/B/C do Raspberry Pi a 3,3 V) | `VOH(Pi) >= 2,0 V` | VOH_PI=? datasheet da base board / BCM não está na pasta | missing: VOH_PI | **falta dado** |
| U400 ISO7141 | SLLSE83F §6.7 p.6: VOH(OUTD) <= VCC1 (G2) | `OUTD → MISO do Pi: VCC1_max <= 3,3 + 0,3 (abs. max típico de GPIO 3,3 V)` | VCC1_MAX=3.382 limite do Pi não está na pasta; 3,6 V é o valor habitual — a conferir | VCC1_MAX = 3.382 | cumpre |
| U400 ISO7141 | SLLSE83F §10 p.25 + Fig.20 p.22: 0,1 µF em VCC1 e VCC2, «2 mm max from VCC» | `C401 = C403 = 100 nF` | C401=1e-07, C403=1e-07 | C401 = 1e-07 | cumpre |
| U400 ISO7141 | SLLSE83F Fig.20 p.22: «2 mm max from VCC1/VCC2» | `distância pino→condensador <= 2 mm` | d_C401_mm=?, d_C403_mm=? F3 — placement | missing: d_C401_mm, d_C403_mm | **falta dado** |
| U400 ISO7141 | SLLSE83F §6.13 p.10: ICC1 máx 3,1 mA (3,3 V, DC-1 Mbps) | `ICC1 <= 300 mA do MCP1824` | ICC1=0.0031 | ICC1 = 0.0031 | cumpre |
| U400 ISO7141 | SLLSE83F §6.1 p.5: IO <= ±15 mA | `saídas atacam entradas CMOS (fugas ±10 µA)` | I_IN_MCP=1e-05 | I_IN_MCP = 1e-05 | cumpre |
| U400 ISO7141 | SLLSE83F p.1 «suffix F… default output low; otherwise default output HIGH»; §6.10 tfs 8 µs | `com VCC1 ausente, OUTC (CS_ADC_ISO) vai a ALTO → MCP3208 desseleccionado (CS/SHDN alto = standby, DS21298E §3.7 p.15)` | default_high=1.000 estado seguro com o barramento desligado | default_high = 1.000 | cumpre |
| U400 ISO7141 | SLLSE83F §11.1 p.25 «A minimum of four layers is required» | `camadas >= 4` | camadas=4.000 escopo §4 item 4: 4 camadas | camadas = 4.000 | cumpre |
| U400 ISO7141 | SLLSE83F §6.3 p.5: signaling rate <= 40 Mbps (VCC<4,5 V) | `SPI 20 kHz` | f_spi=2e+04 | f_spi = 2e+04 | cumpre |
| U401 MCP1824S | DS22070A p.7: VIN 2,1..6,0 V ; nota 1: VIN >= VOUT(max)+VDROPOUT(max) | `+5V do barramento dentro de [3,3·1,025+0,32 ; 6,0]` | V5BUS_MIN=4.750, V5BUS_MAX=5.250, VCC1_MAX=3.382, VDO=0.32 tolerância do +5V do barramento NÃO documentada; assumido ±5 % | V5BUS_MIN = 4.750 ; VCC1_MAX+VDO = 3.702 | cumpre |
| U401 MCP1824S | DS22070A p.7 Abs. Max: VIN 6,5 V | `tecto garantido do +5V do barramento (grampo do TVS D53 da base board, V13) <= 6,5 V` | V_CLAMP_D53=9.200, VBR_D53=6.700 [INHERITED] valores da leitura da netlist da base board V2.3 (intenção V13). FALHA só se o transitório existir; não há medição do barramento | V_CLAMP_D53 = 9.200 ; VBR_D53 = 6.700 | **FALHA** |
| U401 MCP1824S | DS22070A §4.3 p.19: COUT >= 1 µF (cerâmico ok, ESR <= 1 Ω) | `C402 com tolerância −10 % >= 1,0 µF` | C402=1e-06, tol=0.1 1 µF nominal É o mínimo; aplicação típica p.3/p.21 usa 4,7 µF; sem MPN de C402 | C402*(1-tol) = 9e-07 | **FALHA** |
| U401 MCP1824S | DS22070A §4.4 p.19: CIN 1,0..4,7 µF, «equivalent (or higher) value than the output capacitor» | `C400 >= C402` | C400=1e-06, C402=1e-06 | C400 = 1e-06 | cumpre |
| U401 MCP1824S | DS22070A §5.2 p.21 Eq.5-1..5-3: PLDO = (VIN−VOUT)·IOUT ; θJA(SOT-223) 62 °C/W | `TJ = 70 + PD·62 <= 125` | V5BUS_MAX=5.250, VCC1_MIN=3.217, ICC1=0.0031, IQ=0.00022, thJA=62.000, TA=70.000 | TA + ((V5BUS_MAX-VCC1_MIN)*ICC1 + V5BUS_MAX*IQ)*thJA = 70.462 | cumpre |
| U401 MCP1824S | DS22070A p.8: regulação fixa VR ±2,5 % | `banda de +3.3V_DIG = 3,2175..3,3825 V (usada nas linhas do ISO7141)` | VCC1_MIN=3.217, VCC1_MAX=3.382 | VCC1_MIN = 3.217 ; VCC1_MAX = 3.382 | cumpre |
| U500 MCP3208 | DS21298E p.3: VDD 2,7..5,5 V | `VDD_ADC = 3V3_REF − R_DC(FB500)·IDD dentro de 2,7..5,5 V (também no grampo 3,716 V)` | V33_MIN=3.234, R_FB=0.3, IDD=0.0004, V_CLAMP_MAX=3.716 | V33_MIN - R_FB*IDD = 3.234 | cumpre |
| U500 MCP3208 | DS21298E p.2: VREF 0,25 V .. VDD | `2,5 V <= VDD_min` | VREF=2.500, V33_MIN=3.234 | VREF = 2.500 | cumpre |
| U500 MCP3208 | DS21298E p.3: fCLK <= 1,0 MHz @ VDD 2,7 V (sem valor a 3,3 V) | `SPI 20 kHz (Rodrigo, 2026-09-24) <= 1,0 MHz` | f_spi=2e+04 | f_spi = 2e+04 | cumpre |
| U500 MCP3208 | DS21298E §6.2 p.22: do fim da amostragem ao 12.º bit <= 1,2 ms (85 °C) | `13 relógios / f_spi <= 1,2 ms` | f_spi=2e+04, n_clk=13.000 margem ≈1,85x; a transacção de 3 bytes tem de ser contínua (firmware) | n_clk/f_spi = 0.00065 | cumpre |
| U500 MCP3208 | DS21298E Fig.4-2 p.18 (curva VDD 2,7 V): fCLK máx vs RS ; RS = R621 + R611‖(R601+…) ≈ 3,41 kΩ → ≈0,9 MHz | `f_spi <= fCLK_max(RS)` | f_spi=2e+04, fCLK_max_RS_3k41=9e+05 leitura da figura (típica); e C601 100 nF no pino fornece a carga dos 20 pF | fCLK_max_RS_3k41 = 9e+05 | cumpre |
| U500 MCP3208 | DS21298E Fig.4-1 p.18: CSAMPLE 20 pF — carga tirada de C601 por amostra | `ΔV = 20 pF·2,5 V / C601 <= 1 LSB` | CS=2e-11, VFS=2.500, C601=1e-07, LSB=0.0006104 | CS*VFS/C601 = 0.0005 | cumpre |
| U500 MCP3208 | planejamento §2.7d (reposição de carga): ΔV = f_canal·44 pC·RS <= 1 LSB | `f_canal <= 4,07 kHz ; cadência real: 10 amostras/500 ms` | f_canal=20.000, Q=4.4e-11, RS=3410, LSB=0.0006104 | f_canal*Q*RS = 3.001e-06 | cumpre |
| U500 MCP3208 | DS21298E p.2 Abs. Max: entradas −0,6 .. VDD+0,6 V — operação normal e limitador em regulação | `V_pino máx = I_SHORT·R611 <= VDD_min + 0,6` | I_SHORT=0.02691, R611=110.000, V33_MIN=3.234 com o AL5809 a regular, o BAV199 NUNCA conduz em DC (precisaria V_MED > 3V3_REF+0,6) | I_SHORT*R611 = 2.960 ; V33_MIN+0.6 = 3.834 | cumpre |
| U500 MCP3208 | DS21298E p.2 Abs. Max: VDD+0,6 V — grampo BAV199 a conduzir (limitador em curto ou transitório) — V10 | `V_pino = 3V3_REF_grampo + VF(BAV199 @3,4 mA) <= VDD+0,6 = 3V3_REF_grampo + 0,6` | V_CLAMP=3.716, VF_BAV199_3mA4=0.953 BAV199LT1/D p.2: VF máx 0,90 V @1 mA, 1,00 V @10 mA (interp. log a 3,4 mA); a 0 °C sobe ~+0,05 V (fig.2). Por construção VF > 0,6 V acima de ~0,1 mA: o grampo à MESMA rede que VDD não pode cumprir o abs. max | V_CLAMP + VF_BAV199_3mA4 = 4.669 ; V_CLAMP+0.6 = 4.316 | **FALHA** |
| U500 MCP3208 | DS21298E p.2 Abs. Max — CH5 preso a 3V3_REF | `3V3_REF_max <= VDD_min + 0,6` | V33_MAX=3.366, V33_MIN=3.234 lê 4095 (entrada > VREF) | V33_MAX = 3.366 | cumpre |
| U500 MCP3208 | DS21298E p.3: fuga analógica ±1 µA MÁX × RS | `offset = 1 µA·3410 Ω <= 1 LSB (0,61 mV)` | I_LEAK_MAX=1e-06, RS=3410, LSB=0.0006104 offset DC por unidade → removido pela calibração de 6 pontos; a deriva é a da linha seguinte | I_LEAK_MAX*RS = 0.00341 ; LSB = 0.0006104 | **FALHA** |
| U500 MCP3208 | DS21298E Fig.2-39 p.13: fuga típica ≈1–2 nA até 100 °C (VDD 5 V) | `deriva de offset 25→70 °C ≈ 1 nA·3410 Ω <= 1 LSB` | dI_LEAK=1e-09, RS=3410, LSB=0.0006104 | dI_LEAK*RS = 3.41e-06 | cumpre |
| U500 MCP3208 | DS21298E §6.4 p.23: bypass 1 µF junto ao pino | `C501 + C502 >= 1 µF` | C501=1e-06, C502=1e-07 | C501+C502 = 1.1e-06 | cumpre |
| U500 MCP3208 | DS21298E Fig.6-3 p.23: 1 µF na referência | `C207 + C500 >= 1 µF (nominal)` | C207=1e-06, C500=1e-07 o mínimo do ADR4525 (Tabela 11) é avaliado na linha do U202 | C207+C500 = 1.1e-06 | cumpre |
| U500 MCP3208 | DS21298E p.2: INL ±1 LSB (grau -B) — RE1 residual | `2 LSB / 20 mA <= 0,2 %` | LSB_A=5.549e-06 % do fundo de escala 20 mA | 2*LSB_A/20e-3*100 = 0.05549 | cumpre |
| U500 MCP3208 | DS21298E Eq.4-1 p.17: código = 4096·VIN/VREF — RM2 (FE >= 20,5 mA) e NE43 (21 mA legível) | `FE = VREF/R611 >= 20,5 mA e 21 mA·R611 < VREF` | VREF=2.500, R611=110.000 | VREF/R611 = 0.02273 ; 21e-3*R611 = 2.310 | cumpre |
| U500 MCP3208 | DS21298E p.3: tCSH >= 500 ns ; §3.7 p.15 CS alto entre conversões | `firmware — não verificável na netlist` | tCSH_firmware=? restrição a passar ao backend (expander.js) | missing: tCSH_firmware | **falta dado** |
| U60x AL5809-25 | DS36625 p.4 Rec. Op.: VInOut 2,5..60 V ; Fig.15 p.10: I=0 abaixo de ~1,35 V, 20 mA a ≈1,6 V (25 °C, típ.) | `V_InOut em operação normal (4–20 mA) >= 2,5 V` | V_InOut_20mA_tip=1.600 o circuito vive 100 % do tempo abaixo do mínimo recomendado; a queda 1,4–1,6 V é típica a 25 °C, sem mín/máx nem temperatura — V9 não fecha com datasheet | V_InOut_20mA_tip = 1.600 | **FALHA** |
| U60x AL5809-25 | DS36625 p.4 Tabela: AL5809-25 23,75..26,25 mA (−40..125 °C) ; Fig.17 p.10 +1..+2,5 % a 25 V | `I_curto >= saturação do ADC (22,7 mA) e <= fusível 50 mA derated a 70 °C (Schurter p.3 ≈85 %)` | I_MIN=0.02375, I_SHORT=0.02691, I_SAT=0.02273, I_F_DER=0.0425 curto lê 4095 e o fusível não abre (é o limitador que protege) | I_SAT = 0.02273 ; I_SHORT = 0.02691 ; I_F_DER = 0.0425 | cumpre |
| U60x AL5809-25 | DS36625 p.3 Abs. Max VInOut +80 V ; p.4 Rec. <= 60 V — surto grampeado pelo D60x | `V_InOut = V_Clamp(D60x) − I_SHORT·(R601+R611) <= 60 V` | VC_D60x=58.100, I_SHORT=0.02691, R601=100.000, R611=110.000 | VC_D60x - I_SHORT*(R601+R611) = 52.450 | cumpre |
| U60x AL5809-25 | DS36625 p.3 Abs. Max VInOut −0,3 V ; BAT46W DS30044 p.2: VF 0,25 V @0,1 mA, 0,45 V @10 mA (máx, 25 °C) | `−VF(BAT46W @ 3 mA) >= −0,3 V` | VF_BAT46W_3mA=0.398 interp. log entre 0,1 e 10 mA; fig.1 p.3: a 0 °C sobe ~+0,04 V → −0,44 V. Excede o abs. max em 0,10–0,14 V (resíduo confirmado). Cumpriria só com I_rev <~1 mA (VF=0,3 V a 25 °C) | -VF_BAT46W_3mA = -0.398 | **FALHA** |
| U60x AL5809-25 | DS36625 p.3 Abs. Max VInOut −0,3 V — corrente inversa real na falha | `I_rev = (VF_directa(D60x) − VF(BAT46W))/(R601+R611)` | VF_fwd_SMBJ36A=?, R601=100.000, R611=110.000 V_F directa do 824520361 não consta no PDF Würth (só I_peak directo 100 A); com 0,8–1,0 V dá 2–3 mA | missing: VF_fwd_SMBJ36A | **falta dado** |
| U60x AL5809-25 | DS36625 p.8: «junction temperature must be kept <= +125 °C»; PD = VInOut·I ; nota 4 p.4 θJA 148,61 °C/W (ilha mín. + 10×10 mm) | `curto do transmissor a 32 V: TJ = 70 + [V24ADC − I·(R_F60x+R601+R611)]·I·θJA <= 125` | V24ADC=31.370, I=0.02691, R_ser=219.200, thJA=148.610, TA=70.000 TSHDN 165 °C (p.4) → corte térmico em ciclo; a leitura alterna 0 ↔ 4095 | (V24ADC - I*R_ser)*I = 0.6854 ; TA + (V24ADC - I*R_ser)*I*thJA = 171.850 | **FALHA** |
| U60x AL5809-25 | DS36625 p.8 + nota 5 p.4: θJA 81,39 °C/W (25,4×25,4 mm de cobre em GETEK 50,8 mm) | `curto a 32 V com cobre alargado: TJ <= 125` | V24ADC=31.370, I=0.02691, R_ser=219.200, thJA=81.390, TA=70.000 condição da nota 5 (1 pol² de cobre por peça, substrato GETEK) não é realizável em 6 canais desta placa | TA + (V24ADC - I*R_ser)*I*thJA = 125.781 | **FALHA** |
| U60x AL5809-25 | DS36625 p.8 + nota 4 p.4 (θJA 148,61) | `curto do transmissor a 24 V: TJ <= 125` | V24ADC=23.370, I=0.02691, R_ser=219.200, thJA=148.610, TA=70.000 | (V24ADC - I*R_ser)*I = 0.4701 ; TA + (V24ADC - I*R_ser)*I*thJA = 139.862 | **FALHA** |
| U60x AL5809-25 | DS36625 p.8 + nota 5 p.4 (θJA 81,39) | `curto do transmissor a 24 V com cobre alargado: TJ <= 125` | V24ADC=23.370, I=0.02691, R_ser=219.200, thJA=81.390, TA=70.000 | TA + (V24ADC - I*R_ser)*I*thJA = 108.261 | cumpre |
| U60x AL5809-25 | DS36625 Fig.9 p.8: PDI em FR4 (placa de aplicação, TJ=145 °C): 0,80 W @25 °C → ≈0,13 W @125 °C | `PD(curto, 32 V) <= PD_fig9(70 °C) ≈ 0,80·(145−70)/(145−25)` | PD=0.6854, PD_fig9_70=0.5 a figura já admite TJ = 145 °C, acima dos 125 °C da pág. 8 | PD = 0.6854 ; PD_fig9_70 = 0.5 | **FALHA** |
| U60x AL5809-25 | DS36625 Fig.10 p.8: VInOut máx (25 mA, PDI/FR4, TJ 145 °C) a 70 °C ≈ 35 V | `V_InOut(curto, 32 V) <= 35 V` | V_InOut=25.472, Vmax_fig10_70=35.000 cumpre a figura, mas a figura assume TJ 145 °C — inconsistente com o texto da pág. 8; não usar como critério | V_InOut = 25.472 | cumpre |
| U60x AL5809-25 | DS36625 p.4: tON_MIN 500 µs (arranque) | `resposta a um degrau de corrente com o dispositivo já em condução — especificada?` | t_resp_degrau=? não consta; num surto o limitador pode deixar passar a frente de onda até R601/R611/BAV199 | missing: t_resp_degrau | **falta dado** |
| D64x BAT46W | DS30044 p.2: VRRM 100 V | `inversa máx = V_InOut do AL5809 (curto a 32 V / surto) <= 100 V` | V_rev_curto=25.472, V_rev_surto=52.450 | V_rev_curto = 25.472 ; V_rev_surto = 52.450 | cumpre |
| D64x BAT46W | DS30044 p.2: IR 7,5 µA @10 V/60 °C, 15 µA @50 V/60 °C | `fuga em paralelo com o AL5809 — não passa pelo burden (sem efeito na medida); só consumo` | IR_60C_50V=1.5e-05 a 70 °C ≈ 1,5×; irrelevante para RE2 | IR_60C_50V = 1.5e-05 | cumpre |
| D62x BAV199 | BAV199LT1/D p.1: IFSM 500 mA (1 ms), IF 215 mA | `corrente pelo grampo num surto = (V_Clamp(D60x) − 3V3_REF − VF)/R621 <= 500 mA` | VC=58.100, V33=3.700, VF=1.000, R621=3300 | (VC-V33-VF)/R621 = 0.01618 | cumpre |
| D62x BAV199 | BAV199LT1/D p.2: IR 5 nA máx (70 V, 25 °C) ; fig.4 p.3 ≈1 nA @70 °C típ. | `IR·RS <= 1 LSB` | IR_max_25=5e-09, RS=3410, LSB=0.0006104 | IR_max_25*RS = 1.705e-05 | cumpre |
| D62x BAV199 | BAV199LT1/D p.1: PD 225 mW (FR-5) | `VF·I_clamp (limitador em curto) <= 225 mW` | VF=0.953, I=0.003368 | VF*I = 0.00321 | cumpre |
| D62x BAV199 | RA4 (escopo): injectar 30 V numa entrada e medir 3V3_REF <= 3,7 V — com o limitador a funcionar | `V_MED = I_SHORT·R611 < 3V3_REF_min + VF_min(0,6) → grampo não conduz → 3V3_REF fica em 3,3 V` | I_SHORT=0.02691, R611=110.000, V33_MIN=3.234 o RA4 só solicita o TL431 se o AL5809 falhar em curto | I_SHORT*R611 = 2.960 ; V33_MIN+0.6 = 3.834 | cumpre |
| D62x BAV199 | RA4 com o AL5809 em curto (falha dupla): I_burden = 30·110/210/110 | `P(R611) = I²·110 e P(R601) = I²·100 <= 0,25 W (1206)` | V_INJ=30.000, R601=100.000, R611=110.000 sem o limitador, 30 V queimam R611 e R601 (≈2 W cada); é o cenário da V4.1 | (V_INJ/(R601+R611))**2*R611 = 2.245 ; (V_INJ/(R601+R611))**2*R601 = 2.041 | **FALHA** |
| D200 SMA6J33A | Bourns SMA6J p.2: VRWM 33 V, IR 1 µA | `VRWM >= VIN_max` | VRWM=33.000, VIN_MAX=32.000 margem 1 V (3 %) — qualquer sobre-elevação de um controlador solar acima de 33 V põe o TVS a conduzir | VRWM - VIN_MAX = 1.000 | cumpre |
| D200 SMA6J33A | Bourns SMA6J p.2: VBR mín 36,7 V | `VBR_min > VIN_max` | VBR_MIN=36.700, VIN_MAX=32.000 | VBR_MIN = 36.700 | cumpre |
| D200 SMA6J33A | Bourns SMA6J p.2: VRSM (clamp) 53,3 V @ 11,3 A — RA3: grampo < menor abs. max a jusante | `53,3 V <= min(F201/F202 63 V, MBR1H100SF 100 V, C200/C201 100 V, TPS7A4001 105 V)` | VC=53.300, V_fuse=63.000, V_MBR=100.000, V_C=100.000, V_TPS=105.000 | min(V_fuse,V_MBR,V_C,V_TPS) - VC = 9.700 | cumpre |
| D200 SMA6J33A | V7 — quem conduz primeiro: Bourns p.2 VBR(D200) mín 36,7 V ; Würth p.1 VBR(D61x) 42,1 V ±5 % + VF(D202) | `VBR_min(D200) < VBR_min(D61x) + VF(D202)` | VBR_D200=36.700, VBR_D61x_min=39.995, VF_D202=0.5 D200 conduz primeiro; os D61x só entram acima de ≈40,5 V de entrada | VBR_D61x_min + VF_D202 = 40.495 | cumpre |
| D200 SMA6J33A | V7 — partilha: no grampo do D200 (53,3 V) a corrente por cada D61x é limitada pelo fusível de canal (9,2 Ω) | `I_D61x = (VC_D200 − VF_D202 − VBR_D61x)/R_F60x <= IPeak(D61x) 10,4 A` | VC=53.300, VF_D202=0.5, VBR_D61x_min=39.995, R_F60X=9.200 | (VC-VF_D202-VBR_D61x_min)/R_F60X = 1.392 | cumpre |
| D200 SMA6J33A | V7 — I²t no fusível de canal durante o surto 8/20 µs (Schurter p.3: I²t fusão 0,0002 A²s) | `I²·20 µs·0,7 <= 0,0002` | I=1.392, t=2e-05, k=0.7, I2t_fus=0.0002 | I**2*t*k = 2.712e-05 | cumpre |
| D200 SMA6J33A | V7 — idem para 10/1000 µs | `I²·1 ms·0,7 <= 0,0002` | I=1.392, t=0.001, k=0.7, I2t_fus=0.0002 sem requisito de surto (RA3 reescrito); consequência: um surto 10/1000 de fonte abre os 6 fusíveis de canal | I**2*t*k = 0.001356 | **FALHA** |
| D6xx 824520361 | Würth 824520361 p.1: VDC 36 V máx, ILeak 1 µA @ VDC | `D611-616 (LOOPk_V+): +24V_ADC(32 V) <= 36 V` | V24ADC_32=31.370 | V24ADC_32 = 31.370 | cumpre |
| D6xx 824520361 | Würth 824520361 p.1: VDC 36 V | `D601-606 (AINk-): tensão do nó no curto do transmissor a 32 V <= 36 V` | V24ADC_32=31.370, I=0.02691, R_F60X=9.200 | V24ADC_32 - I*R_F60X = 31.122 | cumpre |
| D6xx 824520361 | Würth 824520361 p.1: VClamp 58,1 V máx | `grampo <= abs. max do AL5809 (80 V) e do BAT46W (100 V)` | VC=58.100, V_AL=80.000, V_BAT=100.000 | VC = 58.100 | cumpre |
| D6xx 824520361 | Würth 824520361 p.1: ILeak 1 µA @ 36 V, 20 °C — D60x em paralelo com o caminho de medida | `fuga a <= 8,4 V (nó AINk- a 20 mA) <= 1 LSB (5,5 µA) — usando o limite a 36 V como tecto` | ILEAK_36V_20C=1e-06, LSB_A=5.549e-06 sem curva fuga×temperatura no PDF; a 8 V a fuga é ordens de grandeza menor que a 36 V | ILEAK_36V_20C = 1e-06 ; LSB_A = 5.549e-06 | cumpre |
| D201/D202 MBR1H100SF | MBR1H100SF p.2: VRRM 100 V | `inversa máx: entrada a −1 V (D200 directo) com C201 a 32 V → 33 V <= 100 V` | V_rev=33.000 | V_rev = 33.000 | cumpre |
| D201/D202 MBR1H100SF | MBR1H100SF p.2: IO 1,0 A ; IFSM 50 A | `I_médio(6 curtos + LED) <= 1 A ; pico de arranque a 32 V = VIN/R_F202 <= 50 A` | I_avg=0.1629, VIN_MAX=32.000, R_F202=0.8 pico teórico só com a resistência fria do fusível; a impedância real da base board baixa-o | I_avg = 0.1629 ; VIN_MAX/R_F202 = 40.000 | cumpre |
| D201/D202 MBR1H100SF | MBR1H100SF fig.2 p.3: VF máx ≈0,50 V @0,13 A (25 °C) ; θJA 330 °C/W (ilha 20 mm²) | `TJ = 70 + VF·I·θJA <= 175` | VF=0.5, I=0.13, thJA=330.000, TA=70.000 | TA + VF*I*thJA = 91.450 | cumpre |
| F202 CC12H750mA | Eaton 4309 p.2: I²t pré-arco típ. 0,15 A²s, R frio 800 mΩ ; RA2 >= 10x ; E = ½CV² → I²t = V²C/(2R) | `0,15 / [32²·10 µF/(2·0,8)] >= 10` | I2t_fus=0.15, VIN_MAX=32.000, C201=1e-05, R=0.8 | VIN_MAX**2*C201/(2*R) = 0.0064 ; I2t_fus/(VIN_MAX**2*C201/(2*R)) = 23.437 | cumpre |
| F202 CC12H750mA | Eaton 4309 p.2: 63 Vdc ; derating p.6 ≈90 % a 70 °C | `63 V >= 53,3 V grampo ; 0,75·0,9 >= I(6 curtos + LED)` | V_fuse=63.000, VC=53.300, I_der=0.675, I_load=0.1629 | I_der = 0.675 ; I_load = 0.1629 | cumpre |
| F201 CC12H250mA | Eaton 4309 p.2: I²t 0,00038 A²s, R 3,5 Ω ; RA2 >= 10x ; arranque = C200 via R206 + carga de C202 pelo ILIM do TPS7A4001 (SBVS162B p.5: 200 mA máx) | `0,00038 / [32²·2,2 µF/(2·(33+3,5)) + ILIM²·(C202·5 V/ILIM)] >= 10` | I2t_fus=0.00038, VIN_MAX=32.000, C200=2.2e-06, R206=33.000, R_F201=3.500, ILIM=0.2, C202=1e-05, VOUT=5.000 o planejamento §2.6 ignorou a carga de C202 (10 µF) pelo regulador; com ILIM típ. 117 mA dá 10,4x | VIN_MAX**2*C200/(2*(R206+R_F201)) = 3.086e-05 ; ILIM**2*(C202*VOUT/ILIM) = 1e-05 ; I2t_fus/(VIN_MAX**2*C200/(2*(R206+R_F201)) + ILIM**2*(C202*VOUT/ILIM)) = 9.300 | **FALHA** |
| F201 CC12H250mA | idem, ILIM típico 117 mA (SBVS162B p.5) | `margem RA2 >= 10x` | I2t_fus=0.00038, VIN_MAX=32.000, C200=2.2e-06, R206=33.000, R_F201=3.500, ILIM=0.117, C202=1e-05, VOUT=5.000 R206 = 47 Ω daria 11,8x no pior caso | I2t_fus/(VIN_MAX**2*C200/(2*(R206+R_F201)) + ILIM**2*(C202*VOUT/ILIM)) = 10.351 | cumpre |
| F201 CC12H250mA | idem a 24 V, ILIM máx | `margem RA2 >= 10x` | I2t_fus=0.00038, VIN=24.000, C200=2.2e-06, R206=33.000, R_F201=3.500, ILIM=0.2, C202=1e-05, VOUT=5.000 | I2t_fus/(VIN**2*C200/(2*(R206+R_F201)) + ILIM**2*(C202*VOUT/ILIM)) = 13.889 | cumpre |
| F201 CC12H250mA | Eaton 4309 p.2: 63 Vdc ; derating ≈90 % a 70 °C | `63 >= 53,3 ; 0,25·0,9 >= I_REG` | V_fuse=63.000, VC=53.300, I_der=0.225, I_REG=0.008734 | I_der = 0.225 ; I_REG = 0.008734 | cumpre |
| F60x 3413.0002.22 | Schurter USFF1206 p.3: derating ≈85 % a 70 °C ; 1,0·In 4 h | `50 mA·0,85 >= I_SHORT (o fusível NÃO abre com o transmissor em curto — por desenho)` | I_der=0.0425, I_SHORT=0.02691 | I_der = 0.0425 ; I_SHORT = 0.02691 | cumpre |
| F60x 3413.0002.22 | Schurter USFF1206 p.3: 10·In máx 1 ms ; 63 Vdc | `curto de LOOPk_V+ à massa: I = V24ADC/R_F60x >= 10·In → abre <= 1 ms ; 63 V >= 58,1 V` | V24ADC_32=31.370, R_F60X=9.200, In=0.05, V_fuse=63.000, VC=58.100 | V24ADC_32/R_F60X = 3.410 | cumpre |
| F60x 3413.0002.22 | Schurter USFF1206 p.1: temperatura admissível −55..90 °C ; Eaton p.6: −55..125 °C | `70 °C dentro` | TA=70.000 | TA = 70.000 | cumpre |
| R206 33R 0805 | V5 — energia do impulso de arranque a 32 V: E = ½·C200·V² ; P_pico = V²/R206 ; τ = R206·C200 | `E <= E_pulso_máx(MPN) ; P_pico <= P_pulso(MPN, 73 µs)` | C200=2.2e-06, VIN_MAX=32.000, R206=33.000, E_pulso_max=? sem MPN não há curva de impulso; 1,13 mJ / 31 W de pico em 73 µs exige série anti-surge | missing: E_pulso_max | **falta dado** |
| R206 33R 0805 | dissipação contínua | `I_REG²·R206 <= 0,125 W (0805)` | I_REG=0.008734, R206=33.000 | I_REG**2*R206 = 0.002517 | cumpre |
| R611 ERA8AEB111V / R601 RC1206 | curto do transmissor: P = I_SHORT²·R | `P(R611), P(R601) <= P_nominal(1206)` | I_SHORT=0.02691, R611=110.000, R601=100.000, P_nom_1206=? datasheets Panasonic ERA8 / Yageo RC1206 não estão na pasta 2.3b (o escopo cita AOA0000C307); esperado 0,25 W | missing: P_nom_1206 | **falta dado** |
| R621/C601 antialias | RM3: fc = 1/(2π·RS·C) entre 400 e 550 Hz, com R ±1 % e C ±10 % | `400 <= fc_min e fc_max <= 550` | RS=3410, C=1e-07, tolR=0.01, tolC=0.1 RS inclui o burden (3,3k + 110) | 1/(2*pi*RS*C) = 466.730 ; 1/(2*pi*RS*(1+tolR)*C*(1+tolC)) = 420.099 ; 1/(2*pi*RS*(1-tolR)*C*(1-tolC)) = 523.827 | cumpre |
| R700 NTC / R701 | Vishay 29056 p.1: NTCS0603E3103*LT → B25/85 = 3435 K ; R_T = 10k·exp(B·(1/T − 1/298,15)) | `código = 4096·R701/(R_T+R701) < 4095 a 0, 25 e 70 °C` | B=3435, R25=1e+04, R701=5620 códigos a 0 / 25 / 70 °C; o software actual não lê o CH4 | 4096*R701/(R25*2.718281828**(B*(1/273.15-1/298.15))+R701) = 670.648 ; 4096*R701/(R25+R701) = 1474 ; 4096*R701/(R25*2.718281828**(B*(1/343.15-1/298.15))+R701) = 2941 | cumpre |
| R700 NTC / R701 | DS21298E Fig.4-2 p.18 (2,7 V): RS = R_T‖R701 máx a 0 °C | `fCLK_max(RS≈4,7 kΩ) ≈ 0,8 MHz >= 20 kHz` | RS_0C=4700, fmax_fig42=8e+05, f_spi=2e+04 leitura da figura; C700 100 nF no pino | RS_0C = 4700 | cumpre |
| R700 NTC / R701 | Vishay 29056 p.1: factor de dissipação 3,0 mW/K | `auto-aquecimento = V_NTC²/R_T / 3 mW/K <= 0,5 K (a 25 °C, pior caso)` | VREF=2.500, R25=1e+04, R701=5620, D=0.003 | (VREF*R25/(R25+R701))**2/R25/D = 0.08539 | cumpre |
| LED D203/D630/D204 | KG EELP41.22 v1.4: VF @20 mA (grupo mín. 1,60 V) — corrente a 32 V pelo 14,7 kΩ ; P no 0603 | `I <= 20 mA ; P = (32−VF)²/R <= 0,1 W` | VIN_MAX=32.000, VF=1.600, R=1.47e+04 ERJ-3EKF 0,1 W (datasheet não está na pasta) | (VIN_MAX-VF)/R = 0.002068 ; (VIN_MAX-VF)**2/R = 0.06287 | cumpre |
| LED D203/D630/D204 | idem a 18 V — LED ainda visível? | `I(18 V) >= 1 mA` | VIN_MIN=18.000, VF=1.600, R=1.47e+04 | (VIN_MIN-VF)/R = 0.001116 | cumpre |
| Consumo RA5 | RA5 (escopo): <= 200 mA na entrada de 24 V com 6 canais a 20 mA | `6·20 mA + 2 LED + ramo do regulador <= 200 mA` | I_LOOPS=0.12, I_LED=0.003, I_REG=0.008734 | I_LOOPS + I_LED + I_REG = 0.1317 | cumpre |
| Consumo RA5 | RA5 — pior caso: 6 transmissores em curto (limitador) | `6·I_SHORT + LED + regulador <= 200 mA` | I_SHORT=0.02691, I_LED=0.003, I_REG=0.008734 | 6*I_SHORT + I_LED + I_REG = 0.1732 | cumpre |
| V9 tensão ao transmissor | cadeia a 18 V, 20 mA: V_tx = 18 − R_F202·I_tot − VF(D202) − R_F60x·I − V_InOut(AL5809, cota 2,5 V) − (R601+R611)·I | `V_tx >= V_min_transmissor` | VIN_MIN=18.000, R_F202=0.8, I_tot=0.1215, VF_D202=0.5, R_F60X=9.200, I=0.02, V_AL=2.500, R601=100.000, R611=110.000, V_min_tx=? 1.º valor com a cota de 2,5 V do AL5809, 2.º com o típico da fig.15 (1,6 V); o mínimo dos transmissores instalados não está no escopo | missing: V_min_tx | **falta dado** |

cumpre: 103 · FALHA: 17 · falta dado: 12

---

## 3 · Teste de uma multiplicação — cadeias analógicas

### 3.1 Um canal de campo (igual nos seis), 3 tensões × 4 correntes

Cadeia: `+24V` → F202 (0,8 Ω, 121,5 mA no total) → D202 (V_F 0,50 V máx. a 0,13 A, fig. 2) → `+24V_ADC` → F60x (9,2 Ω) → `LOOPk_V+` → transmissor → `AINk-` → AL5809 (queda típica 1,6 V da fig. 15 / cota 2,5 V do mínimo recomendado) → `AINk_LIM` → R601 100 Ω → `AINk_MED` (burden R611 110 Ω a `GND_ADC`) → R621 3,3 kΩ → `AINk_ADC` (C601 100 nF, BAV199 a `GND_ADC`/`3V3_REF`) → CH do MCP3208 (V_REF 2,5 V, 1 LSB = 0,61 mV = 5,54 µA).

| V_IN | I laço | V burden = pino ADC (DC) | Código | `AINk_LIM` | `AINk-` típ. / cota | Sobra ao transmissor típ. / cota |
|---|---|---|---|---|---|---|
| 18 V | 4 mA | 0,440 V | 720 | 0,84 V | 2,44 / 3,34 V | 14,9 / 14,0 V |
| 18 V | 20 mA | 2,200 V | 3604 | 4,20 V | 5,80 / 6,70 V | 11,4 / **10,5 V** |
| 18 V | 22,7 mA (saturação) | 2,497 V | 4091 | 4,77 V | 6,37 / 7,27 V | 10,8 / 9,9 V |
| 18 V | curto (26,9 mA) | 2,959 V | 4095 | 5,65 V | 17,16 V (= `LOOP_V+`) | — · V_InOut 11,5 V · 0,31 W · Tj 116 °C (nota 4) |
| 24 V | 4 mA | 0,440 V | 720 | 0,84 V | 2,44 / 3,34 V | 20,9 / 20,0 V |
| 24 V | 20 mA | 2,200 V | 3604 | 4,20 V | 5,80 / 6,70 V | 17,4 / 16,5 V |
| 24 V | 22,7 mA | 2,497 V | 4091 | 4,77 V | 6,37 / 7,27 V | 16,8 / 15,9 V |
| 24 V | curto | 2,959 V | 4095 | 5,65 V | 23,16 V | — · V_InOut 17,5 V · **0,47 W · Tj 140 °C (nota 4) / 108 °C (nota 5)** |
| 32 V | 4 mA | 0,440 V | 720 | 0,84 V | 2,44 / 3,34 V | 28,9 / 28,0 V |
| 32 V | 20 mA | 2,200 V | 3604 | 4,20 V | 5,80 / 6,70 V | 25,4 / 24,5 V |
| 32 V | 22,7 mA | 2,497 V | 4091 | 4,77 V | 6,37 / 7,27 V | 24,8 / 23,9 V |
| 32 V | curto | 2,959 V | 4095 | 5,65 V | 31,16 V | — · V_InOut 25,5 V · **0,69 W · Tj 172 °C (nota 4) / 126 °C (nota 5)** |

O que a tabela mostra: (1) a medida não depende de V_IN nem do limitador — o pino do ADC só vê I × 110 Ω; (2) `RM2` cumpre (fundo de escala 22,73 mA ≥ 20,5 mA) e o alarme NE43 de 21 mA lê-se (2,31 V < 2,5 V); (3) a intenção escreveu «≥ 10,5 V a 18 V e 20 mA»: **confirma-se** (10,52 V com a cota), e 9,9 V a 22,7 mA; (4) em curto, o limitador dissipa 0,31/0,47/0,69 W a 18/24/32 V — é a **F1**; (5) `AINk-` máximo em operação normal é 7,3 V, contra 36 V de standoff do TVS D60x e 80 V absolutos do AL5809 — folga grande.

### 3.2 Cadeia de alimentação a 18 / 24 / 32 V

Carga do `+5V_ADC` (máximos de datasheet): ISO7141 I_CC2 4,9 mA (3,3 V, DC–1 Mbps, §6.13) + MCP3208 0,4 mA + ADR4525 0,95 mA de quiescente + 0,15 mA de V_REF + 0,32 mA do divisor NTC a 70 °C + SPX3819 0,25 mA de massa + LED D204 1,58 mA + divisor FB 0,12 mA + TPS7A4001 0,065 mA = **8,73 mA**.

| V_IN | `+24V_REG` (após F201, D201, R206) | P no TPS7A4001 | Tj TPS7A4001 (RθJA 66,7) | `+5V_ADC` | `3V3_REF` | `+2V5_REF` |
|---|---|---|---|---|---|---|
| 18 V | 17,23 V (≥ 7 V) | 107 mW | 77 °C | 4,85–5,10 V | 3,234–3,366 V | 2,500 V ± 0,02 % |
| 24 V | 23,23 V | 159 mW | 81 °C | idem | idem | idem |
| 32 V | 31,23 V (≤ 100 V) | 229 mW | **85 °C** (≤ 125; disparo térmico 155 °C acima de ambiente ≥ 115 °C) | idem | idem | idem |

Verificações de encadeamento que cumprem: `+5V_ADC` mínimo 4,85 V ≥ 3,3 + 0,25 V de dropout do SPX3819; `3V3_REF` mínimo 3,234 V ≥ 3,0 V mínimo do ADR4525 (margem **0,234 V** — é a mais apertada da cadeia); ≥ 3,0 V do ISO7141 (§9.1) e ≥ 2,7 V do MCP3208; V_REF 2,5 V ≤ V_DD; V_OH do ISO7141 a 3,3 V (≥ 2,73 V) ≥ V_IH do MCP3208 (≤ 2,36 V). Dissipações do SPX3819 (12 mW), ADR4525 (3,6 mW) e MCP1824 (7,5 mW) desprezáveis. Consumo total `RA5`: 131,7 mA a 20 mA nos seis canais, 176 mA com os seis em curto — ambos ≤ 200 mA.

Grampo de `3V3_REF` (TL431B + 4k42/10k): nominal 3,616 V; mínimo 3,510 V (com 1 %) — o TL431 fica **desligado** em operação normal (3,366 V máximo do SPX3819, margem 0,144 V); máximo **3,715 V** com 1 % (F4) ou 3,694 V com 0,1 %.

### 3.3 Termístor (CH4 — não lido pelo software actual)

R700 NTCS0603E3103JLT: B25/85 = 3435 K (tabela pág. 1, sufixo L). Divisor a `+2V5_REF` com R701 5,62 kΩ; leitura ratiométrica (mesma referência que V_REF).

| T | R_T | V pino | Código | R_S = R_T ‖ 5,62 kΩ | Corrente no ADR4525 | Auto-aquecimento (3 mW/K) |
|---|---|---|---|---|---|---|
| 0 °C | 28,7 kΩ | 0,409 V | 670 | 4,70 kΩ | 73 µA | 0,02 K |
| 25 °C | 10,0 kΩ | 0,899 V | 1473 | 3,60 kΩ | 160 µA | 0,09 K |
| 70 °C | 2,21 kΩ | 1,795 V | 2940 | 1,59 kΩ | 319 µA | 0,07 K |

Não satura (código máximo 2940 < 4095). R_S máximo 4,7 kΩ a 0 °C: a fig. 4-2 (curva 2,7 V) dá ≈0,8 MHz, 40× acima dos 20 kHz do SPI, e C700 100 nF fornece a carga da amostra. A variação de 246 µA na carga da referência entre 0 e 70 °C vale 20 ppm pela regulação de carga (80 ppm/mA): 0,08 LSB, comum a todos os canais.

---

## 4 · Itens abertos que o autor deixou — fechados ou refutados

| Item | Resultado |
|---|---|
| **V7** (qual TVS conduz primeiro) | **Fechado.** D200 (V_BR mínimo 36,7 V) conduz antes dos D61x (V_BR mínimo 40,0 V + 0,5 V do D202 = 40,5 V de entrada). No grampo do D200 (53,3 V) cada D61x partilha ≈1,39 A, limitado pelo fusível de canal de 9,2 Ω: aguenta 8/20 µs; em 10/1000 µs os fusíveis de canal abrem (F13). Os D60x (retornos) não participam num surto da fonte |
| **V9** (tensão ao transmissor a 18 V) | **Quantificado, não fechado.** 10,5 V a 20 mA e 9,9 V a 22,7 mA com a cota de 2,5 V do AL5809; 11,4 V / 10,8 V com o típico da fig. 15. A cota é a única garantia, porque o AL5809 trabalha fora das condições recomendadas (F2). Falta o mínimo dos transmissores instalados — requisito de campo |
| **V10** (máximo absoluto da entrada do ADC) | **Fechado em duas partes.** Com o limitador a regular, o BAV199 nunca conduz em DC (V_MED ≤ 2,96 V) — cumpre. Quando conduz (limitador em curto, ou transitório), V_pino = `3V3_REF` + V_F > V_DD + 0,6 V **por construção**: 4,67 V contra 4,32 V a 3,4 mA (F10). A corrente de grampo é 3,4 mA por canal, e não os 12,5 mA do planejamento (confirma a correcção de 2026-09-23) |
| **V13** (`+5V_IC` contra o MCP1824) | **Confirmado como falha condicionada** (F5): 9,2 V de grampo do D53 contra 6,5 V absolutos. Precisa de medição do barramento ou de protecção local |
| Resíduo de −0,4 V no AL5809 | **Confirmado** (F9): −0,40 V a 25 °C e −0,44 V a 0 °C a 3 mA, contra −0,3 V. A corrente inversa real depende da V_F directa do TVS, que não consta no PDF |
| **V5** (MPN de R206) | Continua aberto; a conta a 32 V dá 1,13 mJ e 31 W de pico em 73 µs — exige série anti-surge com curva de impulso (falta dado) |
| **V6** (MPN de C200) | Continua aberto; ≥ 1 µF efectivo a 32 V é o mínimo do TPS7A4001 (falta dado) |
| Afirmações da intenção **refutadas** | «Arranque suave próprio» do TPS7A4001 (não existe no datasheet); «Tj ≈ 125 °C com cobre alargado, no limite» a 32 V — a conta com a fig. 17 (+2,5 %) e o fusível de 9,2 Ω dá **126 °C**, e a condição da nota 5 (25,4 mm² de cobre em GETEK) não é realizável; a fig. 10 usada a favor assume Tj 145 °C |
| Afirmações da intenção **confirmadas** | ≥ 10,5 V ao transmissor a 18 V; o limitador em curto lê 4095 e o fusível de 50 mA não abre; 20 kHz cumpre §6.2 com 1,85× de margem; fc do antialias 424–519 Hz dentro de `RM3`; NTC não satura a 70 °C; `RA5` cumpre; margem I²t do F202 23× a 32 V; D200 grampeia abaixo de todos os absolutos a jusante; VCC1 a 3,3 V fecha o G2 |

---

## 5 · O que nenhuma ferramenta viu

Tudo o que está na §0 passou pelo ERC (0 erros), pela verificação de pinagem da 2.3 (sem divergências) e passaria por um analisador de netlist e por SPICE, porque:

1. **ERC/DRC só vêem ligações.** Um condensador de 1,0 µF onde o datasheet pede ≥ 1,0 µF é uma ligação correcta (F6, F8). Um AL5809 com o pino certo no nó certo e 172 °C de junção em falha é uma ligação correcta (F1).
2. **SPICE só vê o que se lhe dá.** A instabilidade do TL431 com 3,6 µF (F3) só aparece se o modelo tiver a compensação interna real e se alguém simular o modo de falha em que o grampo conduz — em operação normal está desligado. A queda do AL5809 abaixo de 2,5 V (F2) não está em nenhum modelo, porque o fabricante não a especifica.
3. **Um analisador não lê notas de rodapé.** «Junction temperature must be kept ≤ 125 °C» está num parágrafo de texto (DS36625 pág. 8), não numa tabela; a fig. 6-18 do TL431 é um gráfico; a nota (2) do TPS7A4001 sobre 24 V está no rodapé de uma tabela eléctrica.
4. **As interacções são entre peças, não dentro delas.** O máximo absoluto do MCP3208 (F10) falha por causa do V_F do BAV199 **e** de o grampo ir à mesma rede que o V_DD **e** do valor do burden que decide se o grampo conduz. O I²t do F201 (F7) falha por causa do I_LIM do TPS7A4001 (peça a jusante) somado ao C200 (peça a montante). Nenhuma peça isolada está errada.
5. **Herdado ≠ verificado.** A topologia BAV199→`3V3_REF` vem da V4.1 e a V4.1 funciona em campo; o abs. max do ADC é violado só em falha, e ninguém o mediu. O SPX3819 com cerâmico vem da V4.1; o datasheet nunca o especificou.
6. **Os cenários de falha não estão na netlist.** Transmissor em curto, limitador em curto, 30 V numa entrada, `+5V` com transitório, fonte a 32 V com painel solar — nenhum é um estado do esquemático; são estados do campo, e é neles que 9 das 17 falhas aparecem.
7. **O que a bancada tem de fazer e o datasheet não pode:** queda do AL5809 a 4/20 mA a 0/25/70 °C; grampo do TL431 com 1 e 6 canais em falha (oscilação); estabilidade do SPX3819 com a capacidade final de `3V3_REF`; comportamento térmico do AL5809 em curto a 32 V/70 °C na placa real; transitórios do `+5V_IC` no painel.

---

## 6 · Limites desta revisão

- **Só datasheets da pasta.** Panasonic, Yageo, Murata, Harwin (eléctrico), base board e Raspberry Pi não estão lá; as 12 linhas *falta dado* são em parte isso. Nada foi citado de memória: onde não havia PDF, a linha diz-o.
- **Leituras de figuras são leituras.** Fig. 6-18 do TL431 (fronteira a 3,6 µF ≈ 25 mA), fig. 15 do AL5809 (1,6 V a 20 mA), fig. 9/10 do AL5809, fig. 4-2 do MCP3208 (0,9 MHz a 3,4 kΩ), fig. 2 do BAV199, fig. 1 do BAT46W, fig. 2 do MBR1H100SF, curvas de derating dos fusíveis: precisão de ±10 % na leitura, indicada nas linhas.
- **Tolerâncias assumidas** onde a BOM não as fixa: R204/R205 a 1 %; barramento `+5V` a ±5 %; condensadores a −10 %. Cada assunção está na coluna «valores usados».
- **Não avaliado:** layout (F3) — distâncias, ilhas térmicas, retorno de massa < 5 mΩ (`V1`), keepouts; firmware (`t_CSH`, continuidade do frame, tratamento do código 4095); EMC; a barreira funcional além dos níveis lógicos; conectores Harwin (corrente/tensão — plano mecânico apenas); LEDs além da corrente e potência; ferrites (impedância/DCR).
- **Independência:** sessão nova, modelo Fable 5.1, sem o histórico da autoria. Foram lidos a intenção, o escopo e o planejamento **como afirmações a conferir**; onde discordo deles está na §4.
- **Não foi tocado** nenhum ficheiro do projecto KiCad. Saídas desta etapa: este relatório, `verificacao_aplicacao_EBM2_V5_rows.json` (linhas avaliadas) na mesma pasta.

---

## 7 · Rastreabilidade

| | |
|---|---|
| Netlist | `EBM2_V5.net`, md5 `29a8e75fb2e3`, 120 componentes, 81 redes |
| Esquemático PDF | `esquematico_EBM2_V5.pdf`, md5 `721681c9510d` |
| Linhas da tabela | `verificacao_aplicacao_EBM2_V5_rows.json` (132 linhas), md5 `8122fcce5722` |
| Scripts | `grep_datasheet.py` (pesquisa e render), `bom_values.py` (valores por CI), `tabela.py` (avaliação) — skill `2shw-pcb:verificar-aplicacao-datasheet` |
| Reprodução | `python tabela.py verificacao_aplicacao_EBM2_V5_rows.json --lang pt` → 103 cumpre · 17 FALHA · 12 falta dado, exit 1 |
