# Recálculo independente — dimensionamento EBM2 V5 rev. 2.5b

**Revisor:** Claude Sonnet 5, sem histórico da sessão de autoria (autor: Claude Opus 5.5). Cálculo do zero a
partir da netlist (`EBM2_V5.net`) e dos datasheets da pasta `datasheets/`. A intenção (`intencao_EBM2_V5.md`
§17) e o planeamento só foram abertos **depois** de fechados os números da Fase 1, como pedido.

Envelope usado em todo o documento: 18–32 V, 0–70 °C (dimensionamento; certificação 0–65 °C), laços 4-20 mA,
NAMUR ≥ 21 mA, ADC satura a 22,7 mA, curto/inversão/falha dupla. Critérios: `escopo_EBM2_V5.md` (`RA2` ≥ 10×,
`RA3`, `RA4` 3V3_REF ≤ 3,7 V com 30 V injectados).

Extracção de texto com PyMuPDF (`fitz`); páginas com curvas/tabelas renderizadas e lidas como imagem (Eaton
I²t, TDK DC-bias, TL431 fig. 6-18). Onde não renderizei eu próprio a figura (BAV199 fig. 2), digo-o
explicitamente e não assino o número às cegas.

---

## 1 · F201 (Eaton CC12H250mA) — I²t de arranque contra `R206`

**Fonte:** `Eaton_fusible_lento.pdf`, Technical Data 4309, pág. 2 (tabela) e pág. 4 (curva I²t-tempo, só
gráfico, sem eixos numerados extraíveis por texto — confirmei que o ponto da tabela pág. 2 é o mesmo dado que
alimenta essa curva, não há segunda fonte independente nela).

**Dados de peça (pág. 2, `CC12H250mA`):** resistência a frio típ. 3,5 Ω; I²t de pré-arco típ. **3,8×10⁻⁴ A²s**
medido a 10× a corrente nominal (nota 3); queda de tensão típ. 1400 mV.

**Netlist:** `F201` = `CC12H250MA-TR` — `+24V` → `F201` → `D200` (TVS) → `R206` (68 Ω, 0805) → nó
`+24V_REG` → `U200` (`TPS7A4001`, `IN`=pino 8) ‖ `C200` (2,2 µF/100 V X7R 1206, descrição da BOM: "≥ 1 µF
efectivo a 24 V", **MPN por fixar**, logo sem curva de derating própria — uso o nominal 2,2 µF, que é o lado
conservador para I²t).

**Método (adiabático, igual ao usado pelo autor):**

`I²t = C₂₀₀·V²/(2·R206)` (carga directa de `C200`) `+ I_LIM²·t_carga` (corrente de arranque do `U200` a
carregar tudo o que está a jusante — `C202` 10 µF a 5 V, o trilho `3V3_REF` (`C204`+`C205`+`C206`) e `C207`
2,2 µF via `ADR4525` — limitada pelo próprio limite de corrente do `TPS7A4001`, já que a eficiência de um LDO
linear faz `I_IN ≈ I_OUT`).

- `I_LIM` do `U200`: **aqui o datasheet do `TPS7A4001` (SBVS162B) contradiz-se a si próprio.** A pág. 8,
  §7.3.1 (texto corrido) diz *"the current limit (309 mA, typical)"*. Mas a tabela de Electrical
  Characteristics, pág. 5, dá `ILIM`: mín. 51 mA / típ. 117 mA (`VIN=17V,VOUT_NOM=18V`) ou 128 mA
  (`VIN=9V`) / **máx. 200 mA** nas duas condições. Uso o **máximo garantido da tabela (200 mA)**, por ser o
  valor vinculativo (a tabela é a que tem de ser cumprida; o texto pode ser resíduo de outra revisão do
  chip). Isto já é, por si, um achado a registar — texto e tabela do próprio fabricante não batem certo.
- `t_carga` = `C_jusante·V_alvo / I_LIM`, com `C_jusante` = `C202`(10) + `C203`(0,1) + `C209`(0,01) +
  `C204`(10) + `C205`(0,1) + `C206`(0,1) + `C207`(2,2) ≈ **22,5 µF**, `V_alvo` ≈ 5 V (o mais alto dos três
  patamares — sobrestima ligeiramente a energia dos ramos a 3,3 V/2,5 V, o que é o lado seguro).

**Cálculo a 32 V:**

- `I²t_C200` = 2,2×10⁻⁶ · 32² / (2·68) = **1,66×10⁻⁵ A²s**
- `t_carga` = 22,5×10⁻⁶ · 5 / 0,2 = 5,63×10⁻⁴ s
- `I²t_downstream` = 0,2² · 5,63×10⁻⁴ = **2,25×10⁻⁵ A²s**
- `I²t_total` ≈ **3,91×10⁻⁵ A²s**
- Margem = `I²t_fusão / I²t_total` = 3,8×10⁻⁴ / 3,91×10⁻⁵ = **9,7×**

**Veredito: FALHA (por pouco).** `RA2` pede ≥ 10×; obtenho 9,7× com o valor garantido do datasheet. Se em
vez disso se usa o «309 mA típico» do texto (pior caso ainda, corrente maior): `t_carga`=3,64×10⁻⁴ s,
`I²t_downstream`=3,48×10⁻⁵, total=5,14×10⁻⁵, margem=**7,4×** — falha por mais folga. Nas duas leituras do
datasheet a margem fica **abaixo** de 10×, nunca aos 11,2× do autor (ver Fase 2).

**Arranque a 18 V:** aqui não é o pior caso para `I²t` (V² é menor), é uma verificação de tensão mínima. Com
o `U200` a tentar puxar corrente através de `R206`=68 Ω a partir de só 18 V, o próprio resistor auto-limita a
corrente muito antes de o chip atingir o seu `ILIM` activo (18 V/68 Ω=264 mA é o tecto físico, e ele cai à
medida que o nó carrega) — o regime é de queda em `R206`, não de limitação activa do CI, o que é benigno
para o fusível. Em regime (pós-transiente), consumo a jusante ≈ 10-15 mA (ADC + `ADR4525` + `TL431` fora de
condução): `VIN(U200)` = 18 − 0,015·68 = **16,98 V**, folga ampla sobre os 7 V mínimos do `TPS7A4001` e sobre
os ~5,3 V que o `U201` precisa a montante. **Cumpre** o requisito de tensão mínima de arranque a 18 V.

**Falta dado:** capacitância efectiva real de `C200` a 24-32 V (MPN por fixar; usei o nominal 2,2 µF, que é
conservador para I²t mas não está medido). E o próprio fabricante não resolve qual dos dois `ILIM` do
`TPS7A4001` é o real — pede bancada (T26).

---

## 2 · U201 (MCP1824T-3302E/OT) — pinagem, entrada, condensadores, tolerância

**Fonte:** `MCP1824__22070a.pdf`, DS22070A: tabela 3-1 pág. 17 (pinagem), pág. 7-8 (AC/DC characteristics),
pág. 19 §4.3 (condensador de saída).

**Pinagem SOT-23-5, versão fixa** (tabela 3-1, coluna "5-Pin Fixed" de SOT-23): 1=`VIN`, 2=`GND`, 3=`SHDN`,
4=`PWRGD`, 5=`VOUT`. **Confere exactamente** com a netlist (`U201` pino1→`+5V_ADC`(IN), pino2→`DGND`(GND),
pino3→`SHDN_3V3`(via `R203` 100 kΩ, pull-up a `+5V_ADC`), pino4→ `unconnected-(U201-PG-Pad4)`, pino5→
`3V3_REF`(OUT)).

**Entrada:** `VIN` do `U201` é o nó `+5V_ADC`, que é a saída do `U200` (`TPS7A4001`) regulada por
`R201`=32k4/`R202`=10k: `VOUT(U200) = 1,173·(1+32,4/10) = 4,97 V` nominal. Está dentro de `VIN` 2,1-6,0 V
(pág. 7) com folga ampla nos dois extremos de tensão de rede (18-32 V), já que `+5V_ADC` é regulado a
montante e não segue directamente a rede.

**Condensador de saída (`C204`, na 3V3_REF):** mínimo de estabilidade 1 µF, máximo recomendado 22 µF (§4.3,
pág. 19). `C204` nominal 10 µF, pior caso pela curva TDK (secção 4) ≈ 7,1-7,2 µF — dentro da janela 1-22 µF.
**Cumpre.**

**Tolerância de saída** (Fixed-Output Characteristics, pág. 8): `VOUT = VR ± 2,5%` no pior caso. A 3,3 V:
3,2175 a 3,3825 V. Isto é **antes** do grampo do TL431 entrar em condução (que só actua acima de ~3,52 V,
secção 3) — em regime normal quem define `3V3_REF` é este ±2,5 %, não o TL431.

**Verdicto geral do item: cumpre.**

---

## 3 · TL431BQ (U203) com R204/R205 — nível do grampo, estabilidade, corrente de cátodo

**Fonte:** `TL431__TI_TL431.pdf`, SLVS543S: tabela 6.13 pág. 14 (grau BQ), fig. 6-18 pág. 18 (estabilidade).

**Topologia (netlist):** `U203` cátodo(pino1)→`3V3_REF`; ânodo(pino3)→`GND_ADC`; `REF`(pino2)→nó
`FB_CLAMP`, entre `R204`(4k12, para `3V3_REF`) e `R205`(10k, para `GND_ADC`).

**Tabela 6.13 (grau BQ, 25 °C, `IKA`=10 mA):** `Vref` = 2483/2495/2507 mV; `VI(dev)` (desvio sobre toda a gama
de temperatura) = 14 típ / **34 mV máx**; `Imin` (corrente mínima de cátodo para regular) = **0,4/0,7 mA**
(não 1 mA — o autor corrige isto na §17, e está certo: a tabela não dá 1 mA em lado nenhum).

**Nível do grampo, todos os extremos** (combino o pior caso de `Vref` a 25 °C com todo o `VI(dev)` máx. no
mesmo sentido — é a leitura mais conservadora, não decomposta por sinal):

- `Vref` mín. combinado = 2483 − 34 = 2449 mV; máx. combinado = 2507 + 34 = 2541 mV
- `V_clamp = Vref·(1+R204/R205)`, com `R204/R205` nominal = 0,412 (tolerância de `R204`/`R205` **não consta
  na netlist** — nem MPN nem % — assumo ±1 % por prática de casa e sinalizo como falta de dado):
  - mín.: 2,449·(1+0,4038) = **3,438 V**
  - típ.: 2,495·(1+0,412) = **3,523 V**
  - máx.: 2,541·(1+0,4202) = **3,609 V**

**Contra `RA4` (3V3_REF ≤ 3,7 V):** máx. 3,609 V < 3,7 V — **cumpre, com 91 mV / 2,5 % de margem.**
**Contra o máximo do `MCP1824` (3,3825 V, item 2):** o grampo mínimo (3,438 V) fica **acima** do máximo do
LDO em todos os extremos — o TL431 nunca interfere com a regulação normal, só entra em condução acima dela.
Confirma a lógica de projecto (grampo = rede de segurança, não regulador em paralelo).

**Estabilidade (fig. 6-18, curva B — `VKA≈5V` é a mais restritiva das desenhadas e a nossa condição de falha
fica entre a curva A (`Vref`=2,495 V) e B (5 V); uso B por ser a mais conservadora):** a região instável na
imagem renderizada não ultrapassa, mesmo no pico, uma capacitância de carga de ~2-4 µF (eixo `CL`, log,
0,001-10 µF). A capacitância efectiva no cátodo (`C204` pior caso ~7,1-7,2 µF, secção 4, + `C205`+`C206`
0,2 µF ≈ **7,3-7,4 µF**) fica à direita de toda a região instável desenhada, tanto no ponto de operação normal
(`IKA`≈0) como no de falha (`IKA` na casa das dezenas de mA). **Cumpre** — confirma a citação do autor
("> 6 µF, fig. 6-18").

**Corrente de cátodo:**
- **Falha simples** (30 V injectados por um canal): o `BAV199` desse canal conduz para `3V3_REF`, mas a
  corrente é pequena (secção 5: ~0,13 mA) frente ao consumo próprio do trilho (~4 mA) — o `TL431` **nem chega
  a regular** (fica abaixo do seu `Imin` 0,4-0,7 mA e a queda adicional é absorvida pelo LDO a fornecer menos
  corrente própria). **Confirmo** a leitura do autor (§17, "não muda").
- **Falha dupla** (`R601`=0 Ω não muda + protector em curto + 30 V injectados no mesmo canal): o burden
  (`R611`=110 Ω) vê os 30 V praticamente directos (30/0,110 = **273 mA**, **8,2 W** nele — valor do autor,
  confirmado por aritmética simples `I²R`=0,273²·110=8,19 W). Uma fracção disso (a definir por `R621`=3k3
  contra o `TL431` já em condução) entra no cátodo — **ordem de grandeza de dezenas de mA**, dentro da gama
  0-100 mA da fig. 6-18 e da corrente contínua do TL431. **Falta dado:** o datasheet do `TPS26613` não dá o
  comportamento exacto do estágio de saída já em fast-trip simultâneo com a falha externa — pede-se o T26 tal
  como o autor já assinala.

---

## 4 · TDK C3216X5R1H106K160AB — capacitância efectiva (curva DC-bias)

**Fonte:** `C3216X5R1H106K160AB__TDK_ProductDetailed_2026-09-24.pdf`, pág. 1 (10 µF ±10 %, 50 VDC, X5R
±15 %) e pág. 2 (gráfico "DC Bias Characteristic", renderizado e lido por pixel, não só por texto — o PDF não
tem os valores da curva em texto extraível).

**Pontos lidos na curva (nominal/típico, sem tolerância aplicada):** 0 V→10,05 µF; 10 V→6,8 µF; 16 V→4,5 µF;
20 V→3,8 µF; 30 V→2,0 µF; 40 V→1,4 µF; 50 V→1,05 µF.

**C204 a 3,3 V (3V3_REF):** interpolando entre 0 e 10 V, ≈ **9,3-9,4 µF** típico. Pior caso, combinando a
tolerância de fabrico (±10 %) com a característica X5R (±15 % sobre a gama de temperatura, garantida pelo
próprio datasheet pág. 1): `9,35 × 0,90 × 0,85 ≈` **7,15 µF**. Usado na secção 3.

**C642/C644 a ~12,6 V (+12V_TPS, saída do U640):** interpolando entre 10 V (6,8) e 16 V (4,5),
`≈ 5,8 µF` típico por peça a 12,6 V. Pior caso por peça: `5,8 × 0,90 × 0,85 ≈` **4,44 µF** — **abaixo** dos
4,7 µF que o `TPS7A4001` exige por si só (confirma o motivo de existir `C644` em paralelo). Duas peças:
**8,88 ≈ 8,9 µF** — **cumpre** com folga sobre 4,7 µF.

Esta leitura da curva **bate exactamente** com o número que o autor cita para `C642`+`C644` (8,9 µF, §17
item 9) — é o único ponto em que consegui reconstruir o método do autor dígito a dígito e confirma que a
curva foi lida correctamente dos dois lados.

---

## 5 · Entrada do ADC por canal (R661-R666) — curto do transmissor

**Fontes:** `TI_TPS2661x.pdf` pág. 5 (`I(OL)`), `BAV199__BAV199LT1-D.PDF` pág. 2 (tabela `VF`) e pág. 3
(fig. 2, **não renderizada por mim** — uso o valor que a tabela e a interpolação dão, e sinalizo onde me apoio
só na leitura do autor), `MCP3208__21298e.pdf` pág. 17-18 (§4.1, fig. 4-1/4-2).

**`I(OL)` do `TPS26613`:** tabela pág. 5, "Bipolar current limit", `V(IN)-V(OUT)=±1V`: mín. 25 / típ. 32 /
**máx. 40 mA**. Uso 40 mA (garantido, pior caso).

**Circuito (netlist):** `U601` `OUT`(pino5) → `R601`(0 Ω) → nó `AIN1_MED` → `R611`(110 Ω) a `GND_ADC` ‖
`R621`(3k3) → nó `AIN1_FILT` (com `C601` 100 nF e o clamp `D621` `BAV199`: `A1`→`GND_ADC`, `K2`→`3V3_REF`,
`COM`→`AIN1_FILT`) → `R661`(4k7) → `AIN1_ADC` (pino do `MCP3208`).

**KCL no nó `AIN1_MED`** com fonte de corrente ideal 40 mA (compliance do `TPS26613` em curto) e o nó
`AIN1_FILT` grampeado a `V(3V3_REF) + Vf(BAV199)`:

`40 mA = V_MED/R611 + (V_MED − V_clamp)/R621`

Com `V_clamp ≈ 3,3 + 0,67 = 3,97 V` (3,3 V = `3V3_REF` normal, sem o TL431 ainda a conduzir — a corrente de
falha simples não o activa, secção 3; `0,67 V` = `Vf` do `BAV199` a ~0,1-0,15 mA, **lido da fig. 2 do
BAV199LT1/D pelo autor — não re-renderizei esta curva especificamente, uso o valor citado como referência,
com a tabela da pág. 2 como cota superior de plausibilidade: a 1 mA o máximo é 900 mV, por isso 670 mV a
~0,13 mA é consistente com a inclinação log-linear típica de um díodo**):

`40×10⁻³ = V/110 + (V−3,97)/3300` → `132 = 30V + V − 3,97` → `V = 4,386 V`
`I_R621 = (4,386 − 3,97)/3300 ≈` **0,126 mA** — **confirma** a ordem de grandeza que o autor cita (~0,15 mA);
a pequena diferença é a sensibilidade ao `Vf` exacto, que não tenho de fonte própria.

Esta corrente entra no nó `AIN1_FILT`/grampo; a fracção que continua por `R661` até ao pino do ADC é limitada
pela diferença entre o nó grampeado (~3,97-4,0 V) e o limiar do díodo interno do `MCP3208` (modelo da fig.
4-1, `VT=0,6 V` acima de `VDD_ADC`≈3,3 V, ou seja ~3,9 V): a diferença é de poucas dezenas de mV a ~0,1 V,
dando uma corrente no pino da ordem de **dezenas de µA** — a mesma ordem de grandeza que o autor calcula
(30 µA). **Cumpre** em ambas as leituras: a corrente que atinge fisicamente o pino do `MCP3208` é muito
inferior a qualquer limite de dano plausível para um clamp de ESD.

**Amostragem (fig. 4-1/4-2, DS21298E pág. 17-18):** o modelo de entrada recomenda `RS` (resistência de fonte
externa) ≤ 1 kΩ para manter o erro de INL < 0,1 LSB a 1 MHz de clock. Com `R661`=4,7 kΩ em série directa ao
pino (sem condensador depois dele, ao contrário do canal NTC que ganhou `C700` exactamente por este motivo,
citando a mesma fig. 4-2 a 1 MHz), os canais AIN1-6 têm o **mesmo problema estrutural** que motivou `C700` no
NTC — mas não receberam o mesmo remendo. **Achado de consistência (nem FALHA nem confirmação limpa):** ou o
requisito da fig. 4-2 não se aplica de facto (porque o firmware fixa o SPI/clock de conversão em **20 kHz**,
50× mais lento que os 1 MHz do caso citado para o NTC — a 20 kHz o orçamento de tempo de amostragem é ~50×
maior e `RS`=4,7 kΩ deixa de ser um problema em qualquer dos canais), e então `C700` no NTC é conservadorismo
a mais e não um requisito; ou, se a fig. 4-2 for mesmo o critério a cumprir à letra do datasheet
independentemente do clock real, falta o equivalente a `C700` nos seis canais AIN. Isto não estava no âmbito
explícito da rev. 2.5b e não bloqueia nenhum critério de aceite (a calibração de campo absorve qualquer erro
de ganho residual), mas é uma assimetria que vale a pena registar.

---

## 6 · ADR4525 (U202, C207) e MCP1824 do barramento (U401, C400/C401/C402)

**Fonte:** `ADR4525__adr4520_4525_4530_4533_4540_4550.pdf` pág. 35 (Tabela 11); `MCP1824__22070a.pdf` pág. 19
(§4.3) e pág. 17 (pinagem, já verificada na secção 2 para o `U201` — `U401` é a mesma família/pinagem).

**ADR4525 (`C207`):** Tabela 11 exige `COUT` mínimo **1,0 µF** para o `ADR4525`. `C207`=2,2 µF — **cumpre**
com folga (2,2×). Entrada: `VIN` do `ADR4525` é `3V3_REF` (~3,3-3,6 V), acima do mínimo de queda 500 mV sobre
2,5 V de saída (`VIN_min`≈3,0 V) em todos os cantos, mas com margem mais apertada no canto frio/baixo (LDO a
−2,5 % = 3,2175 V, folga de só 217 mV sobre o mínimo 3,0 V, ~43 % de reserva). **Cumpre, sem ser folgado.**

**MCP1824 do barramento (`U401`, alimenta `+3.3V_DIG` a partir de `+5V`):** `C400`=1 µF na entrada — dentro
da recomendação 1-4,7 µF de §3.2 (pág. 17). `C401`=100 nF (desacoplamento adicional). `C402`=2,2 µF na saída
— acima do mínimo de 1 µF de estabilidade (§4.3, pág. 19) e abaixo do máximo recomendado de 22 µF.
**Cumpre.**

---

## Resumo da Fase 1

| Item | Veredito |
|---|---|
| 1. `F201`/`R206` I²t de arranque | **FALHA** — margem 9,7× (tabela) a 7,4× (texto do datasheet), ambas < 10× exigido por `RA2`. Arranque a 18 V cumpre (tensão) |
| 2. `U201` MCP1824 pinagem/entrada/cap/tolerância | Cumpre |
| 3. TL431BQ grampo/estabilidade/corrente | Cumpre (grampo 3,44-3,61 V < 3,7 V; estável; correntes de falha dentro da gama) |
| 4. TDK C3216 curva DC-bias | Confirma os dois usos (C204 > 6 µF, C642+C644 > 4,7 µF) |
| 5. Entrada do ADC em curto | Cumpre para dano/fuga; assimetria de consistência entre canais AIN e NTC quanto à fig. 4-2 (não bloqueante) |
| 6. ADR4525 / MCP1824 do barramento | Cumpre (ADR4525 com margem mais apertada no canto frio) |

---

## Fase 2 — comparação com a §17 da intenção (rev. 2.5b)

Li a §17 só depois de fechar os números acima.

| # autor | Item | Número do autor | O meu número | Divergência? |
|---|---|---|---|---|
| 1 | `R206`/`F201` `RA2` a 32 V | **11,2×** (cumpre) | **9,7×** (tabela, máx. 200 mA) a **7,4×** (texto, 309 mA típ.) — **FALHA** nas duas leituras | **SIM, divergência real.** O autor usa o mesmo método (`C·V²/2R` + `I_LIM²·t`), mas o resultado não bate. Não consigo reconstruir que `I_LIM` ele usou para chegar a 11,2×: com `ILIM`=117-128 mA (típico da tabela, condição mais próxima da nossa) dava uma margem maior que a minha mas ainda não tão alta como 11,2× salvo se a capacitância a jusante usada for menor que os ~22,5 µF que somei (ele cita "C202 a 5V, o trilho 3V3_REF e C207" — a mesma lista que eu). Registo como divergência a esclarecer: **o meu recálculo não confirma que `R206`=68 Ω feche `RA2` com 10× de margem**; fecha, na melhor leitura do datasheet, a 9,7×. Recomendo medir o arranque real em bancada (T26) antes de aceitar a peça. |
| 4 | `C204` — TDK a 3,3 V | típ. 9,4 µF; pior caso 7,2 µF + "1,3 µF do resto do trilho" = 8,5 µF | típ. ≈ 9,3-9,4 µF (bate); pior caso 7,15-7,2 µF (bate); **C205+C206 juntos são só 0,2 µF, não 1,3 µF** | Divergência pequena, não muda o veredito (7,2+0,2=7,4 µF, ainda > 6 µF). A origem do "1,3 µF" do autor não é óbvia a partir da netlist (não encontrei mais nenhum condensador nesse trilho) — fica como nota, não como falha. |
| 5 | `R204` grampo, extremos | 4k12 → 3,427-3,662 V (38 mV sob 3,70 V) | 3,438-3,609 V (91 mV sob 3,70 V) | Mesma ordem de grandeza e mesmo veredito (cumpre), mas os extremos não coincidem ao mV — provavelmente diferença em como cada um decompõe `VI(dev)` (eu apliquei os 34 mV inteiros no mesmo sentido que o `Vref` de 25 °C já pior-casado; o autor parece ter feito o mesmo, "os 34 mV inteiros para cada lado", mas o resultado não é idêntico). Não é uma divergência de mais de 5 % no essencial (ambos < 3,7 V com margem de dezenas de mV), mas os números não são reprodutíveis um a partir do outro sem mais detalhe do `R204`/`R205` real (tolerância não está na netlist). |
| 9 | `C642`+`C644` a 12,6 V | 8,9 µF | 8,88 ≈ 8,9 µF | **Confirma exactamente.** |
| 6, 7 | `C207`, `C402` mínimos | 1,0 µF era o mínimo; subiu para 2,2 µF | Confirmado (Tabela 11 ADR4525 = 1,0 µF; §4.3 MCP1824 = 1,0 µF) | Confirma |
| 10 | `R661`-`R666`, corrente no ADC | ~0,15 mA no `BAV199`, ~30 µA no pino do ADC | ~0,126 mA no clamp (KCL), dezenas de µA no pino | Confirma (mesma ordem de grandeza, mesmo veredito) |
| 2 | `U201` pinagem/tensão/cap | 2,1-6,0 V; ±2,5 %; 1-22 µF; pinagem 1-VIN 2-GND 3-SHDN 4-PWRGD 5-VOUT | Idêntico | Confirma |
| — | `R601`=0 Ω, falha dupla 273 mA/8,2 W | 273 mA, 8,2 W | Confirmado por aritmética (`I²R`) | Confirma |

**A única divergência que muda um veredito é o item 1** (`R206`/`F201`): o autor fecha `RA2` em 11,2× e o meu
recálculo, com o mesmo método e as mesmas fontes, fecha entre 7,4× e 9,7× — **abaixo do limite de 10×** nas
duas leituras possíveis do `ILIM` do `TPS7A4001` (o próprio datasheet da TI é inconsistente entre o texto
"309 mA típico" e a tabela "200 mA máx."). Isto é o achado principal a levar ao projectista.

---

## O que nenhuma ferramenta viu

- A **contradição interna do datasheet do `TPS7A4001`** (texto §7.3.1 "309 mA típico" vs. tabela pág. 5
  "200 mA máx.") não aparece em nenhuma extracção automática de texto — só se nota lendo as duas secções lado
  a lado e reparando que os números não podem ser ambos "típicos" para a mesma condição.
- A **assimetria `C700` (NTC) vs. ausência do equivalente nos seis canais AIN** só aparece comparando a
  netlist de duas sheets diferentes (`06_lacos` e `07_ntc`) contra a mesma figura do mesmo datasheet
  (`MCP3208` fig. 4-2) — nenhuma tabela isolada mostra isto.
- O facto de o `R204`/`R205` **não terem tolerância nem MPN na netlist** só aparece ao tentar reproduzir o
  cálculo do grampo ao mV — sem isso, os extremos do autor e os meus não são comparáveis ao dígito.

## Limites desta revisão

- Não abri `rev24_anterior/` nem os ficheiros `verificacao_aplicacao_*_rev25*` (outro revisor), como pedido.
- A fig. 2 do `BAV199LT1/D` (curva `VF` a baixa corrente) não foi renderizada por mim nesta corrida — usei a
  tabela (pontos discretos a 1/10/50/150 mA) e o valor citado pelo autor como referência plausível; se o
  projecto depender do dígito exacto desse `Vf`, deve re-renderizar-se e medir directamente.
- O comportamento do `TPS26613` em falha dupla simultânea com o fast-trip não está coberto pelo datasheet
  disponível — pede-se bancada (T26), tal como o autor já assinalava.
- A capacitância efectiva real de `C200` (MPN por fixar) não tem curva própria — usei o nominal 2,2 µF como
  valor conservador para `I²t`, não um dado medido.
- Este documento não reabre o layout nem a estratégia de retorno de massa; assume a netlist como desenhada.
