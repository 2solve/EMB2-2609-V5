---
documento: Documento de Planejamento do PCB
projecto: IC2S Extension Board EBM2 V5 (6AI)
fase: F1
data: 2026-09-23
rodadas_entrevista: 1
duvidas_abertas: 0
estado: LOOP FECHADO tecnicamente; RE1 em conflito com o escopo (decisao de escopo pendente). F2 prossegue: o hardware nao depende dela
revisao: 3 — datasheet do MCP3208 (DS21298E) fornecido e estudado; loop FECHADO
duvidas_abertas_reais: 0
calibracao: CONSTANTE COMUM (confirmado 2026-09-23; o registo anterior de calibracao por unidade foi anulado)
---

# Planejamento do PCB — EBM2 V5

> **Esta é a segunda escrita do documento, no mesmo dia.** A primeira afirmava
> que o datasheet do fusível Eaton não existia. Existe, com outro nome, e o que
> ele diz **muda o projecto**. A secção §9 conta o erro e o que ele custou.

> **O loop da F1 está encerrado.** O datasheet do `MCP3208` chegou em
> 2026-09-23 e está estudado em §2.7. Não restam dúvidas técnicas. Resta **uma
> decisão de produto**, que não é minha: se a calibração continua a ser uma
> constante comum, **o critério `RE1` não se cumpre no pior caso**, e nenhuma
> troca de componente o resolve. Ver §2.7c.

---

## 1 · Sumário do produto

Shield de quadro PLC da família IC2S com seis entradas analógicas de 4-20 mA.
Monta sobre a Universal Baseboard pelo conector `P1` de 20 pinos e liga ao campo
por `P2` de 14 pinos. O mestre SPI é uma Raspberry Pi que vive na MainBoard. A
V5 é uma **revisão de correcção** da V4.1, que está em campo desde 2024, e é
**substituição directa** dela: contorno, furação e pinagem congelados.

## 2 · Tabela mestre de componentes

Origem: **[HERD]** herdado da V4.1 · **[EBM7]** portado da EBM7 V2.3, já em BOM
da casa · **[NOVO]** não existe noutra placa.

> **Designadores definitivos** estão em `intencao_EBM2_V5.md` rev. 2, §2: `U4` passa a `U400`, `U5` a `U500`, o `MCP1824` a `U401`, `R5`/`R8` a `R700`/`R701`. Os desta tabela são os da F1.

### 2.1 · Núcleo de medida

| Ref | Função | Part number | Origem | Justificação |
|---|---|---|---|---|
| `U5` | ADC 12 bits SPI, 8 canais | **`MCP3208T-BI/SL`** | **[HERD]** alterado | **MUDA de `-CI` para `-BI`**: mesmo encapsulamento e pinagem, INL de ±1 LSB em vez de ±2. Ver §2.7b |
| `U4` | Isolador digital 4 canais | `ISO7141CCDBQR` | **[HERD]** | Única barreira da placa. Limiares **TTL**, VIH 2,0 V |
| `U202` | Referência de tensão 2,5 V | `ADR4525BRZ` | **[EBM7]** | ±0,02 % inicial; **4 ppm/°C pelo método bowtie**, que é o que conta a partir de 25 °C. Substitui `VREF` = `VDD` |
| `R×6` | Burden dos laços, 110 Ω | `ERA3AEB111V` (Panasonic) | **[NOVO]** valor | ±0,1 % e ±25 ppm/°C. **É o melhor que existe a 110 Ω — ver §2.5** |
| `R×6` | Série de protecção, 249 Ω | `RC0603FR-07249RL` | **[HERD]** | Não se toca: é protecção. Revisão na 2.3b |
| `R×6` | Anti-aliasing, 3,3 kΩ | `RC0603FR-073K3L` | **[HERD]** | Corte a 482 Hz com 100 nF. **O condensador é o reservatório de carga do ADC — ver §2.7d** |
| `R8` | Divisor do NTC, 5,62 kΩ | `ERA3AEB5621V` | **[HERD]** | Já na V4.1. **Passa a pender de `+2V5_REF` e não de `3V3_REF` — ver §2.7e** |
| `R5` | Termístor de placa, 10 kΩ | `NTCS0603E3103JLT` | **[HERD]** | Canal 4 do ADC. Sensor de temperatura da própria placa |
| `C_VDD` | Desacoplamento do ADC, 1 µF | cerâmico X7R 0603 | **[NOVO]** | **O datasheet pede 1 µF, a V4.1 tem 100 nF.** §6.4, pág. 23 |
| `C_VREF` | Desacoplamento da referência, 1 µF | cerâmico X7R 0603 | **[NOVO]** | Figura 6-3, pág. 23 |
| `D×6` | Clamp de entrada | `BAV199` | **[EBM7]** | Substitui `BAT54S`. Fuga 5 nA a 25 °C contra µA do Schottky |
| `D×12` | TVS de campo, 30 V | `824500301` (Würth) | **[HERD]** | Dois por canal |

### 2.2 · Entrada e protecção de 24 V

| Ref | Função | Part number | Origem | Justificação |
|---|---|---|---|---|
| `D200` | TVS de entrada, 33 V | `SMA6J33A-Q` (Bourns) | **[EBM7]** | A V4.1 **não tem TVS nenhum** na entrada. Grampeia a 58,1 V @ 11,3 A |
| `F202` | Fusível rama dos laços | `CC12H750MA-TR` (Eaton) | **[EBM7]** | I²t de fusão **0,15 A²s**. Margem de arranque **41,7×** — ver §2.6 |
| `F201` | Fusível rama do regulador | `CC12H250MA-TR` (Eaton) | **[EBM7]** família | **MUDOU.** Era «100 mA»; **a série não tem 100 mA**, começa em 250 mA |
| `R206` | Limitador de arranque, 22 Ω 0805 | resistência de impulso, 0805 | **[NOVO]** | **Peça nova, obrigatória.** Sem ela `F201` não cumpre `RA2` — ver §2.6 |
| `D201`, `D202` | Bloqueio, 100 V | `MBR1H100SF` | **[EBM7]** | `D201` serve o regulador e `D202` os laços, como no esquemático. Substitui o zener `D26` em série da V4.1; o `PMEG6010CEH` de 60 V é curto contra 58,1 V |
| `R200` | Net-tie das massas, 0 Ω | `RC0603JR-070RL` | **[EBM7]** | Único caminho `GND_24V` ↔ `GND_ADC` |
| `C200` | Entrada do regulador, 2,2 µF/100 V, **1206** | **MPN por fixar — V6** | **[NOVO]** | Pequeno **de propósito**: é ele que fixa a energia de arranque. **Correcção 2026-09-23:** esta linha dava `GRM31CR72A225KA73L` com origem EBM7. **A EBM7 Legacy não tem nenhum 2,2 µF de 100 V**: os seus 2,2 µF são `C1608X5R1E225K080AB`, 0603 de 25 V, e era daí que vinha a pegada 0603 herdada. O part number não consta do catálogo Murata da pasta. Especificação: 2,2 µF, ≥ 100 V, X7R, 1206, ≥ 1 µF efectivo a 24 V |
| `C201` | Bulk dos laços, 10 µF/100 V | `GRM32EC72A106ME05L` | **[EBM7]** | **Substitui os electrolíticos de 50 V `ESL107M050AGMAA`.** Fecha `G3` |

### 2.3 · Regulação

| Ref | Função | Part number | Origem | Justificação |
|---|---|---|---|---|
| `U200` | Regulador 24 → 4,974 V | `TPS7A4001DGNR` | **[EBM7]** | Entrada 7-100 V, 50 mA máx contra cerca de 12 mA de carga. Divisor 32k4/10k |
| `U201` | LDO 5 → 3,3 V | `SPX3819M5-L-3-3/TR` | **[HERD]** | Já na V4.1 como `U11`. Baixo ruído, último estágio antes do ADC |
| `U203` | Grampo activo a 3,6 V | `TL431BQDBZR` | **[EBM7]** | **Sumidouro dos clamps.** A V4.1 não tem nenhum |
| `U204` | LDO 3,3 V para o isolador | `MCP1824ST-3302E/DB` | **[EBM7]** | **Fecha `G2`.** Datasheet confirmado na pasta |

### 2.4 · Diagnóstico

| Ref | Função | Origem | Justificação |
|---|---|---|---|
| `T20x` | 9 pontos de prova | **[NOVO]** | A V4.1 tem **zero**. Requisito `RD1` |
| `Fid1-3` | 3 fiduciais | **[EBM7]** | A V4.1 tem **zero**. Requisito `RD2` |

### 2.5 · O burden: porque 110 Ω e ±25 ppm/°C, e porque não se pode fazer melhor

A resposta do projectista fixou que a calibração é uma **constante comum a todas
as placas**. Uma constante comum não segue a dispersão de peça para peça, logo a
**tolerância inicial não se calibra** e volta ao orçamento.

A primeira escrita deste documento propunha, como travão de emergência, «uma
peça de 0,05 % e 10 ppm/°C». **Essa peça não existe a 110 Ω.** A tabela de
*Ratings* do datasheet Panasonic `AOA0000C307`, pág. 2, lida na figura
renderizada e não no texto extraído, diz o seguinte para o tamanho 0603:

| Grau | T.C.R. | Tolerância | **Gama de resistência** |
|---|---|---|---|
| `ERA3AEB` | ±25 ppm/K | ±0,1 % | **47 Ω a 330 kΩ** |
| `ERA3APB` | ±15 ppm/K | ±0,1 % | 470 Ω a 100 kΩ |
| `ERA3ARB` | ±10 ppm/K | ±0,1 % | 1 kΩ a 100 kΩ |
| `ERA3ARW` | ±10 ppm/K | ±0,05 % | 1 kΩ a 100 kΩ |

**Os graus finos começam acima de 110 Ω.** O de ±15 ppm só desce a 470 Ω, e o de
±10 ppm a 1 kΩ. Os tamanhos 0805 e 1206 têm exactamente os mesmos limites. A
110 Ω, dentro desta família, **`ERA3AEB` é o melhor que existe** — e é o que já
estava especificado. O travão de emergência que a revisão 1 anunciava não era
real, e retira-se.

E 110 Ω não é negociável para cima: com a referência de 2,5 V, 20 mA × 110 Ω dá
2,200 V, ou 88 % da escala, e o fundo de escala fica em 22,7 mA. Subir o burden
satura o conversor antes dos 20 mA.

Nomenclatura: 110 Ω é valor da série E24, e a nota `*5` do datasheet obriga os
valores duplicados a seguir a codificação E24 de **três dígitos**. O part number
é **`ERA3AEB111V`**, não `ERA3AEB1100V` como a revisão 1 escrevia.

### 2.5b · O orçamento de erro, com o datasheet do conversor na mão

O escopo define **dois** critérios com **dois** orçamentos independentes, e
misturá-los inventa um problema que não existe:

- **`RE1`** mede a 25 °C, com a placa calibrada. Só entram as **tolerâncias
  iniciais**.
- **`RE2` e `RB3`** medem o **erro adicional** entre −40 e +85 °C, sem
  recalibrar. Só entram as **derivas**.

A conta completa está em §2.7c, depois de o datasheet do conversor a poder
fechar. O resultado, em duas linhas:

| Critério | Termos conhecidos | Tecto | Veredito |
|---|---|---|---|
| `RE2` e `RB3`, deriva térmica | **0,165 %** | 0,2 % | **cumpre**, com 83 % do orçamento gasto |
| `RE1` a 25 °C, **constante comum** | **0,237 %** | 0,2 % | **NÃO CUMPRE** |
| `RE1` a 25 °C, **calibração por unidade** | **0,055 %** | 0,2 % | cumpre com folga de 3,6× |

### 2.6 · Os fusíveis, com o datasheet na mão

Toda esta secção usa **A²s**, e não «mA²s». A revisão 1 escrevia mA²s em todo o
lado com valores que eram A²s — um erro de rótulo de um factor de um milhão. Os
**rácios** estavam certos, porque o mesmo factor aparecia dos dois lados da
divisão, e por isso **nenhuma conclusão muda**. Mas o rótulo estava errado e
corrige-se aqui.

Dados de `Technical Data 4309`, Eaton `CC12H`, pág. 2, tabela *Product
specifications*, coluna «Typical pre-arcing I²t», medida a 10× a corrente
nominal:

| Peça | Corrente | Resistência a frio | I²t de fusão |
|---|---|---|---|
| `CC12H250mA` | 0,25 A | 3 500 mΩ | 0,000 38 A²s |
| `CC12H375mA` | 0,375 A | 1 750 mΩ | 0,000 77 A²s |
| `CC12H500mA` | 0,5 A | 980 mΩ | 0,001 9 A²s |
| `CC12H750mA` | 0,75 A | 800 mΩ | **0,15 A²s** |

**A série não tem 100 mA.** Começa em 250 mA, e o `F201` de «100 mA» que a
revisão 1 especificava **não é encomendável**.

Repare-se no salto entre 500 mA e 750 mA: o I²t multiplica-se por 79 enquanto a
corrente cresce 50 %. Não é um erro de tabela — a folha diz na primeira página
que a qualificação AEC-Q200 cobre **«750 mA to 30 A»**, ou seja as peças de
750 mA para cima são de outra construção. **É esse degrau que faz o projecto.**

Energia de arranque de um condensador carregado através de uma resistência
série, que é toda a energia que o fusível vê:

```
I2t = V^2 * C / (2R)        com V = 24 V
```

**Rama dos laços, `F202` = `CC12H750mA`, com `C201` = 10 µF:**

```
I2t = 576 * 10e-6 / (2 * 0,8) = 3,6e-3 A2s
margem = 0,15 / 3,6e-3 = 41,7x           cumpre RA2 (>= 10x)
```

**Rama do regulador, `F201` = `CC12H250mA`, com `C200` = 2,2 µF e mais nada:**

```
I2t = 576 * 2,2e-6 / (2 * 3,5) = 1,81e-4 A2s
margem = 3,8e-4 / 1,81e-4 = 2,1x         REPROVA RA2
```

**Reprova.** E não se resolve escolhendo outra peça da série: o de 375 mA dá
exactamente o mesmo 2,1×, porque o I²t duplica enquanto a resistência se reduz a
metade. O de 500 mA dá 2,9×. Só o de 750 mA passaria, e pôr 750 mA numa rama que
consome 12 mA é não ter protecção nenhuma.

**A solução é a resistência `R206`, e é barata.** Para chegar aos 10× exigidos:

```
I2t <= 3,8e-4 / 10 = 3,8e-5
R   >= 576 * 2,2e-6 / (2 * 3,8e-5) = 16,7 ohm
```

Com o valor normalizado de **22 Ω**, somado aos 3,5 Ω do próprio fusível:

```
I2t = 576 * 2,2e-6 / (2 * 25,5) = 2,48e-5 A2s
margem = 3,8e-4 / 2,48e-5 = 15,3x        cumpre RA2
```

O que custa: com 12 mA de consumo, a queda são **0,26 V** e a dissipação
**3,2 mW**. O `TPS7A4001` precisa de 7 V à entrada e, no pior caso de 20 V de
alimentação menos o Schottky menos esta queda, ficam **19,2 V**. Não custa nada.
O pico de arranque é 24/25,5 = 0,94 A durante uma constante de tempo de 56 µs, e
a energia que a resistência absorve é 0,55 mJ — daí o encapsulamento **0805** e
não 0603.

**E o mais importante, que não é o tamanho de nenhum fusível.** O que queimou a
EBM7 V1.1 e está presente na V4.1 é **bulk atrás de fusível pequeno**. Na V4.1,
`F7` e `F9` são `3413.0008.22`, Schurter USFF1206 de 160 mA com I²t de fusão
**0,0015 A²s** (datasheet `Schurter_USFF1206_3413.pdf`, presente na pasta), e
cada um tem 10 µF atrás. Contando apenas a resistência do próprio fusível:

```
I2t = 576 * 10e-6 / (2 * 0,51) = 5,65e-3 A2s   ->  3,8x ACIMA do I2t de fusao
I2t = 576 * 10e-6 / (2 * 1,7)  = 1,69e-3 A2s   ->  1,13x ACIMA
```

Acima nos dois casos, em três ramas independentes. **A correcção estrutural da
V5 é topológica:** todo o bulk fica atrás do `CC12H750mA`, e atrás dos fusíveis
pequenos de canal só ficam os laços, que não têm condensador nenhum. Nenhum
fusível pequeno volta a ver energia de arranque.

### 2.7 · O conversor: o que o datasheet DS21298E obriga a mudar

Datasheet `MCP3204/3208`, Microchip **DS21298E**, revisão de 2008, fornecido
pelo projectista em 2026-09-23. Tudo o que segue sai dele, com página.

#### 2.7a · O mapa de canais não é o que se assumia — e é o achado mais perigoso

Antes de tocar em números, uma verificação de pinagem na V4.1, feita pad a pad
contra o desenho de encapsulamento da pág. 1:

| Pino | Função (DS21298E, pág. 1) | Rede na V4.1 | O que é |
|---|---|---|---|
| 1 | `CH0` | `AIN1_ADC` | canal de campo 1 |
| 2 | `CH1` | `AIN2_ADC` | canal de campo 2 |
| 3 | `CH2` | `AIN3_ADC` | canal de campo 3 |
| 4 | `CH3` | `AIN4_ADC` | canal de campo 4 |
| **5** | **`CH4`** | `NetR5_2` | **termístor da placa**, divisor `R5`/`R8` |
| **6** | **`CH5`** | `3V3_REF` | **ligado ao trilho**, lê sempre 4095 |
| **7** | **`CH6`** | `AIN5_ADC` | **canal de campo 5** |
| **8** | **`CH7`** | `AIN6_ADC` | **canal de campo 6** |
| 9 | `DGND` | `GND_ADC` | |
| 10 | `CS/SHDN` | `CS_ADC_ISO` | |
| 11 | `DIN` | `MOSI_ADC_ISO` | |
| 12 | `DOUT` | `MISO_ADC_ISO` | |
| 13 | `CLK` | `CLK_ADC_ISO` | |
| 14 | `AGND` | `GND_ADC` | pino separado do `DGND` |
| 15 | `VREF` | `NetC10_2` | **o mesmo nó que o `VDD`** — é o defeito `D7` |
| 16 | `VDD` | `NetC10_2` | |

**Os seis canais de campo não estão em `CH0` a `CH5`. Estão em `CH0`, `CH1`,
`CH2`, `CH3`, `CH6` e `CH7`.** O `CH4` é o termístor e o `CH5` está preso ao
trilho. Se a V5 fosse desenhada com os seis canais em sequência, o firmware
existente leria o termístor no lugar do canal 5 e um valor saturado no lugar do
canal 6, **sem dar erro nenhum** — apenas dois valores errados. Isso quebraria o
critério `RC4` da maneira mais difícil de diagnosticar que existe.

**Decisão: o mapa de canais fica congelado exactamente como está acima.**

Nota de projecto, não de erro: os pinos `AGND` (14) e `DGND` (9) são **pinos
distintos** no conversor e na V4.1 estão os dois em `GND_ADC`. Está certo — a
placa tem um só domínio de massa analógica deste lado da barreira — mas a
separação existe no silício e o layout deve respeitá-la (§2.7f).

#### 2.7b · Porque o grau muda de `-C` para `-B`

A pág. 37, *Product Identification System*, diz que o sufixo de grau é a
especificação de linearidade: **`B` = ±1 LSB INL, `C` = ±2 LSB INL**. A V4.1
monta `MCP3208T-CI/SL`, ou seja o grau de ±2 LSB.

O `MCP3208T-BI/SL` existe, está listado na mesma página, tem **o mesmo
encapsulamento SOIC de 16 pinos, a mesma pinagem e o mesmo protocolo**. Não toca
em `RC4`, não toca no layout, não toca no firmware.

**E o INL é o único erro do conversor que nenhuma calibração remove**, porque
não é offset nem ganho: é curvatura. Passar de `-C` a `-B` corta esse termo a
metade, e ele passa a ser o termo dominante em qualquer cenário com calibração
por unidade. **Decisão tomada: `MCP3208T-BI/SL`.**

#### 2.7c · Os erros do conversor são tensões fixas, e é isso que estraga a conta

Esta é a leitura que decide o projecto, e só se vê cruzando a tabela da pág. 2
com as figuras 2-2, 2-15 e 2-18 da secção de curvas típicas.

A tabela especifica tudo a `VREF` = 5 V. As curvas mostram o que acontece quando
se baixa a referência:

- **Figura 2-18, offset vs `VREF`:** o erro sobe de cerca de 1,5 LSB a 5 V para
  cerca de 3 LSB a 2,5 V. Como o LSB é metade, **a tensão de erro é a mesma**.
- **Figura 2-2, INL vs `VREF`:** o ramo negativo passa de −0,35 LSB a 5 V para
  −0,7 LSB a 2,5 V. Mesma leitura: **tensão constante**.
- **Figura 2-15, ganho vs `VREF`:** fica entre −0,5 e −1 LSB de 1 a 5 V, ou seja
  **este sim é proporcional**, uma fracção.

Logo, convertidos a tensão, os limites máximos valem:

| Erro | Limite (pág. 2) | Em tensão | % do nosso fundo de escala de 2,200 V |
|---|---|---|---|
| Offset | ±3 LSB | ±3,662 mV | **0,166 %** |
| INL, grau `-B` | ±1 LSB | ±1,221 mV | **0,055 %** |
| INL, grau `-C` | ±2 LSB | ±2,441 mV | 0,111 % |
| Ganho | ±5 LSB | fracção | **0,122 %** |

**A consequência é dura: baixar a referência de 5 V para 2,5 V duplica, em
termos relativos, o peso do offset e do INL.** O sinal encolheu para metade e o
erro não.

Orçamento de `RE1` a 25 °C, com o grau `-B` e limites máximos:

| Contribuição | Valor |
|---|---|
| Referência `ADR4525B`, erro inicial | ±0,020 % |
| Burden `ERA3AEB`, tolerância inicial | ±0,100 % |
| `MCP3208` ganho, ±5 LSB | ±0,122 % |
| `MCP3208` offset, ±3 LSB | ±0,166 % |
| `MCP3208` INL, ±1 LSB | ±0,055 % |
| **Soma quadrática** | **0,237 %** |

**Excede o tecto de 0,2 %, e o conversor sozinho já vale 0,215 %.** Não é o
burden, não é a referência: é o conversor.

Cenários avaliados, todos com limites máximos:

| Cenário | Total | Veredito |
|---|---|---|
| Grau `-C`, constante comum (o que estava desenhado) | 0,256 % | reprova |
| Grau `-B`, constante comum | 0,237 % | reprova |
| Grau `-B`, constante comum, **valores típicos** em vez de máximos | 0,139 % | passa |
| `VDD` 5 V + referência 4,096 V + burden 180 Ω, constante comum | ~~0,201 %~~ **0,192 %** | ~~reprova na mesma~~ **passa, com margem de 4 %** — *correcção de 2026-09-23: os 0,201 % usavam o INL do grau -C; com o -B dá 0,192 %. Ver `Relatorio_Melhorias_Isolamento_V8_RE1_2026-09-23.md` §2* |
| **Grau `-B`, calibração por unidade de dois pontos** | **0,055 %** | **passa com folga de 3,6×** |

**Dentro da família do `MCP3208`, não existe escolha de componente que feche `RE1` com
constante comum.** *Correcção de 2026-09-23:* a frase dizia «não existe escolha de componente»
sem restrição, mas só se avaliaram variantes do `MCP3208`. O `AD7124-8` da EBM7 (24 bits,
Σ-Δ; Rev. F pág. 5: INL ±4 ppm FSR máx. a ganho 1, erro de ganho ±0,0025 % a 25 °C, offset
±15 µV típico) dá ≈ 0,10 % no pior caso, dominado pelo burden — **cumpre**. Não entra porque
parte o `RC4`: protocolo SPI por registos, o firmware actual não o lê sem recompilar. A linha
do meio mostra porquê: mesmo mudando o trilho para 5 V, pondo uma referência de
4,096 V e subindo o burden a 180 Ω — que obriga a 1206 por dissipação e a uma
peça nova fora da BOM da casa — o total fica em 0,201 %, na mesma linha do tecto.

A última linha mostra o que funciona, e não custa uma peça: **calibrar cada placa
em dois pontos**. Uma calibração de dois pontos remove o offset e o ganho por
completo, e sobra só o INL. E o ensaio que a produz **já está no plano de teste**:
o item `T7` obriga a injectar 4, 12 e 20 mA em cada canal contra padrão
rastreável. Guardar dois números por canal em vez de deitar fora a medição é
tempo de teste zero.

> ## CALIBRAÇÃO: **CONSTANTE COMUM** a todas as placas — confirmado pelo projectista em 2026-09-23
>
> Uma mensagem anterior foi lida como «calibração por unidade» e chegou a ser
> registada como decisão. **O projectista corrigiu: não se calibra placa a placa.**
> O registo anterior fica anulado.
>
> **Consequência, que não muda: `RE1` não se cumpre no pior caso.** Com constante
> comum e limites máximos do datasheet, o pior caso é **0,237 %** contra o tecto
> de 0,2 %. Com valores típicos são **0,139 %**. Nenhuma troca de componente o
> resolve — a tabela de cenários acima prova-o, incluindo o trilho de 5 V.
>
> **O hardware é o mesmo em qualquer caso**, por isso a F2 prossegue. O que
> fica em aberto é uma **decisão de escopo**, e volta ao Portão 0:
>
> - ou `RE1` passa a ser especificado pelo valor que a placa garante no pior caso;
> - ou `RE1` fica a 0,2 % declarado como **típico**, com o pior caso registado.

> **Actualização 2026-09-24 — `RB1` passou a 0 a +70 °C.** Com calibração a 25 °C a maior excursão é de 45 °C: referência 4 ppm/°C → 0,018 %, burden 25 ppm/°C → 0,113 %, conversor e carga iguais → **≈ 0,114 %**. No campo calibra-se à temperatura do painel: o pior caso é calibrar a 0 °C e operar a +70 °C (70 °C de excursão) → **≈ 0,178 %**. **Cumpre nos dois**, com menos folga no segundo. A tabela abaixo é a de −40/+85 °C e fica como histórico.

Orçamento de deriva, `RE2` e `RB3`, para uma excursão de 65 °C:

| Contribuição | Valor |
|---|---|
| `ADR4525B`, **4 ppm/°C pelo método bowtie** | ±0,026 % |
| Burden `ERA3AEB`, 25 ppm/°C | ±0,163 % |
| `MCP3208`, deriva medida nas figuras 2-19 e 2-22 | ±0,006 % |
| Regulação de carga da referência com a excursão do termístor | ±0,003 % |
| **Soma quadrática** | **0,165 %** |

**Cumpre.** Duas notas sobre os números:

1. A revisão 2 usava **2 ppm/°C** para a referência. Esse é o valor do **método
   box**; o datasheet dá também **4 ppm/°C pelo método bowtie** (pág. 4), e é o
   bowtie que responde à pergunta «quanto se afasta do ponto de calibração a
   25 °C». Corrigido. Não muda o veredito porque o burden domina.
2. **A deriva do conversor é desprezável.** As figuras 2-19 e 2-22 mostram o
   ganho a variar cerca de 0,08 LSB e o offset cerca de 0,08 LSB entre −40 e
   +85 °C. É o melhor que se podia esperar, e significa que toda a deriva da
   placa está nas duas resistências.

#### 2.7d · A impedância de fonte: porque 3,3 kΩ é aceitável, e em que condição

O datasheet é explícito na §6.3, pág. 22: *«If the signal source for the A/D
converter is not a low impedance source, it will have to be buffered»*, e a
figura 6-3 desenha um amplificador operacional a atacar a entrada. **O nosso
circuito não tem buffer e tem 3,41 kΩ em série.** É preciso justificar, com
conta, porque é que passa.

O modelo da entrada, figura 4-1, pág. 18: interruptor de amostragem de 1 kΩ e
condensador de amostra de **20 pF**. A figura 4-2 dá o relógio máximo em função
da resistência de fonte para não passar de 0,1 LSB de desvio de INL.

**O que salva o circuito é o condensador de 100 nF do filtro, que está no próprio
pino do conversor.** Aos MHz do instante de amostragem ele é um curto-circuito, e
a carga dos 20 pF sai dele, não da resistência. O condensador é 5 000 vezes maior
do que o de amostra: cada amostra baixa-o 0,44 µV.

O que os 3,41 kΩ custam é a **reposição** dessa carga entre amostras:

```
carga por amostra = 20 pF * 2,2 V = 44 pC
queda DC = f_canal * 44 pC * 3410 ohm
```

| Cadência por canal | Queda | Em LSB | % do fundo de escala |
|---|---|---|---|
| 100 Hz | 0,015 mV | 0,02 | 0,0007 % |
| 1 kHz | 0,150 mV | 0,25 | 0,007 % |
| **4,07 kHz** | **0,610 mV** | **1,00** | 0,027 % |
| 7 kHz | 1,050 mV | 1,72 | 0,048 % |

**Abaixo de cerca de 4 kHz por canal, os 3,3 kΩ custam menos de 1 LSB.** Acima,
começa a aparecer como erro de ganho — sistemático, igual em todas as placas, e
por isso removível por uma constante comum, ao contrário de tudo o resto.

> **Restrição de layout para a F3, e não é opcional:** o condensador de 100 nF
> tem de ficar **encostado ao pino do canal**, do lado do conversor. É ele que
> substitui o buffer que o datasheet pede. Se o layout o afastar e deixar
> resistência de pista entre ele e o pino, a justificação acima deixa de valer e
> passa a aplicar-se a figura 4-2 com 3,41 kΩ, que a esse valor limita o relógio
> a algumas centenas de kHz.

#### 2.7e · O termístor saturava a 70 °C — defeito encontrado e corrigido

Na V4.1 o divisor do termístor é `NTCS0603E3103JLT` de 10 kΩ, de `3V3_REF` até
ao `CH4`, e `ERA-3AEB5621V` de 5,62 kΩ do `CH4` até `GND_ADC`. Na V4.1 isso
funciona porque **`VREF` também é o trilho de 3,3 V**: a leitura é ratiométrica e
a tolerância do trilho cancela-se.

**Na V5, `VREF` passa a ser os 2,5 V do `ADR4525`. Se o divisor continuasse
pendurado nos 3,3 V, a ratiometria quebrava-se e o canal saturava.** A conta:

```
saturacao quando  3,3 * 5,62 / (R_ntc + 5,62) = 2,5   ->  R_ntc = 1,80 kohm
para o NTCS0603E3103 (10 kohm a 25 C, B = 3936 K) isso corresponde a  T = 70 C
```

**Setenta graus, dentro da gama de operação de −40 a +85 °C que o critério `RB1`
exige.** O sensor de temperatura da placa deixaria de funcionar exactamente
quando começa a ser preciso.

**Decisão: o topo do divisor passa de `3V3_REF` para `+2V5_REF`.** E o melhor
desta correcção é que ela **não muda nada para o firmware**:

```
V4.1:  codigo = 4096 * (3,3 * ratio) / 3,3 = 4096 * ratio
V5:    codigo = 4096 * (2,5 * ratio) / 2,5 = 4096 * ratio
```

**O código é idêntico.** A tabela de conversão de código para temperatura do
firmware continua a valer, letra por letra, e `RC4` fica intacto.

Custo para a referência: o divisor consome 160 µA a 25 °C e 354 µA a 85 °C. O
`ADR4525` fornece **10 mA** (pág. 4), e a sua regulação de carga é de 80 ppm/mA
no pior caso, o que sobre a excursão de 347 µA dá **0,003 %**. Está na tabela de
deriva acima e é desprezável.

#### 2.7f · O resto do que o datasheet obriga

| # | O que o datasheet diz | Onde | O que fazemos |
|---|---|---|---|
| 1 | *«A bypass capacitor should always be used... A bypass capacitor value of **1 µF** is recommended»* | §6.4, pág. 23 | **A V4.1 tem 100 nF (`C10`).** Passa a 1 µF mais 100 nF, no pino |
| 2 | A figura de aplicação põe **1 µF** na referência | Fig. 6-3, pág. 23 | Acrescenta-se 1 µF em `+2V5_REF` |
| 3 | *«no traces running underneath the device or the bypass capacitor»* | §6.4, pág. 23 | Restrição de F3, entra como regra de layout |
| 4 | *«Use of an analog ground plane is recommended»* e alimentação em **estrela** | §6.4 e fig. 6-4, pág. 23 | Já é a intenção; passa a requisito escrito |
| 5 | Relógio máximo **2,0 MHz a 5 V, 1,0 MHz a 2,7 V** | pág. 3 | A 3,3 V **não há valor garantido**. Adopta-se o de 2,7 V: **SPI ≤ 1 MHz** |
| 6 | *«a 85 °C... o tempo entre o fim da amostragem e a saída dos 12 bits **não pode exceder 1,2 ms**»* | §6.2, pág. 22 | **Restrição de firmware.** Ver abaixo |
| 7 | Máximos absolutos das entradas: **`VSS` − 0,6 V a `VDD` + 0,6 V** | pág. 2 | Fecha o cálculo do `G6`. Ver abaixo |
| 8 | `VIH` = 0,7 `VDD` = 2,31 V a 3,3 V | pág. 3 | O `ISO7141` do lado 2 sai de `3V3_REF`. Cumpre |

**Sobre o item 6, e é o que mais me preocupa num mestre Raspberry Pi.** O
datasheet explica que a carga do condensador de amostra se esvai: a 85 °C o
conversor só a garante durante **1,2 ms** depois de terminada a amostragem. Se a
transacção SPI for interrompida a meio — e num Linux não preemptivo isso é
exactamente o que acontece quando o escalonador decide — a conversão sai com
erro de linearidade **sem qualquer indicação de erro**. A leitura parece boa.
**Requisito para o firmware: a transacção de 24 bits de cada canal tem de ser
atómica**, num só descritor de transferência, e nunca partida em três escritas
de um byte com o escalonador pelo meio.

**Sobre o item 7, que fecha o cálculo em falta do `G6`.** O máximo absoluto da
entrada é `VDD` + 0,6 V. Com `VDD` = `3V3_REF` e o `TL431` a grampear esse trilho
em 3,60 V, o tecto da entrada é **4,20 V**. Numa falha de campo, o TVS de 30 V
grampeia em cerca de 48 V e a corrente pelo caminho de 249 Ω mais 3,3 kΩ é de
cerca de **12,5 mA**; a essa corrente o `BAV199` cai qualquer coisa como 0,95 a
1,05 V, o que põe o pino em **4,55 a 4,65 V**.

> **Correcção de 2026-09-23 a este parágrafo.** Os 12,5 mA abaixo ignoram o burden de 110 Ω, que fica em paralelo a `GND_ADC` no nó de medida e desvia a maior parte da corrente da falha antes dos 3,3 kΩ. A corrente real de clamp é da ordem de 3 a 4,5 mA e a queda do `BAV199` é menor. A conclusão de ultrapassar o máximo absoluto fica **por confirmar**, não por afirmar; é a `V10` da intenção, e fecha na 2.3b.

**Isso ultrapassa o máximo absoluto em cerca de 0,4 V.** Não é conclusão fechada,
porque falta a curva directa do `BAV199` à corrente certa, e essa é a primeira
linha da tabela da etapa 2.3b. Mas o número já não é uma suspeita: é uma conta
com as duas pontas conhecidas.

## 3 · Interacções entre componentes, em linguagem natural

Este é o texto que a F2 consome.

**Entrada.** Os 24 V entram pelo pino 20 de `P1`, vindos da Universal Baseboard.
Desse nó sai um ponto de prova e o cátodo do TVS `D200`, cujo ânodo vai a
`GND_24V`. Do mesmo nó saem duas ramas em paralelo. A primeira passa pelo
fusível `F202`, entra no ânodo do Schottky `D202`, e o cátodo forma `+24V_ADC`,
que é o rail dos laços: dele saem os seis fusíveis de canal e o bulk `C201`. A
segunda passa por `F201`, entra no ânodo de `D201`, e do cátodo sai a
resistência `R206`, cujo outro terminal forma `+24V_REG`, onde fica `C200` e a
entrada do regulador. **A ordem importa:** `R206` fica depois do díodo e antes
do condensador, porque é entre o fusível e o condensador que ela tem de estar
para limitar o arranque. `GND_24V` liga-se a `GND_ADC` pela resistência de 0 Ω
`R200`, **e por mais nada em toda a placa**.

**Regulação.** `+24V_REG` entra no pino IN do `TPS7A4001`, cujo EN liga ao mesmo
nó. A saída é fixada em 4,974 V pelo divisor de 32k4 sobre 10k ligado ao pino
FB. Essa saída forma `+5V`, que alimenta a entrada do `SPX3819`, com o enable
puxado por 100 kΩ. A saída do `SPX3819` forma `3V3_REF`, que alimenta, por
ferrite, o `VDD` do `MCP3208` e o `VCC2` do isolador, e directamente a entrada
da referência `ADR4525`. O `TL431` fica com o cátodo em `3V3_REF` e o ânodo em
`GND_ADC`, com o divisor de 4k42 sobre 10k no pino de referência, o que o faz
grampear o rail a 3,60 V. A saída da referência forma `+2V5_REF`, **que vai
exclusivamente ao pino VREF do `MCP3208`**.

**Barreira.** O `ISO7141` tem o lado 1 em `DGND` e o lado 2 em `GND_ADC`. Três
canais vão do lado 1 para o lado 2 — MOSI, CLK e CS_ADC — e um volta, o MISO. O
`VCC1` e o `EN1` deixam de pender dos +5 V do barramento e passam a ser
alimentados pelo `MCP1824`.

**Mapa de canais do conversor — congelado por `RC4`, e não é sequencial.** Os
seis canais de campo ocupam `CH0`, `CH1`, `CH2`, `CH3`, `CH6` e `CH7`. O `CH4`
lê o termístor da placa e o `CH5` está preso ao trilho de 3,3 V. Ver §2.7a: pôr
os seis canais em sequência partiria o firmware em silêncio.

**Termístor, canal 4.** O termístor de 10 kΩ `R5` liga de **`+2V5_REF`** ao nó
do `CH4`, e desse nó a resistência de 5,62 kΩ `R8` desce a `GND_ADC`. O topo do
divisor é a mesma referência que alimenta o `VREF`, de propósito: a leitura fica
ratiométrica e o código sai idêntico ao da V4.1. Ver §2.7e.

**Cadeia por canal, exemplo do primeiro canal de campo.** O pino de `P2` recebe
o retorno do laço. Desse nó sai o cátodo de um TVS de 30 V cujo ânodo vai a `GND_ADC`, e sai
também um terminal da resistência série de 249 Ω. O outro terminal forma o nó de
medida, onde ficam o burden de 110 Ω até `GND_ADC` e a resistência de
anti-aliasing de 3,3 kΩ. Do outro lado dessa resistência fica o condensador de
100 nF até `GND_ADC`, o clamp duplo `BAV199` entre `GND_ADC` e `3V3_REF`, e o
pino do canal do `MCP3208`.

## 4 · Decisões de encapsulamento

| Peça | Encapsulamento | Motivo |
|---|---|---|
| Passivos por omissão | 0603 | O que a V4.1 já usa. Solda manual possível para retrabalho |
| **`R206`** | **0805** | Absorve 0,55 mJ em cada arranque. O 0603 não tem essa margem de impulso |
| Bulk de 100 V | 1210 | A tensão obriga; não há 10 µF/100 V em 0805 |
| Fusíveis | 1206 | Herdado do footprint da V4.1, e é o tamanho da série `CC12H` |
| TVS de entrada | DO-214 (SMA) | Área de dissipação para o pico |
| `TPS7A4001` | HVSSOP-8 com pad térmico | Dissipa cerca de 95 mW; o pad é o caminho |
| `ADR4525` | SOIC-8 | Menos sensível a tensões mecânicas da placa que um SOT pequeno |
| Conectores | THT | **Congelados** por `RC2` |
| Electrolíticos | **eliminados** | Passam a cerâmico 1210. Tira a única peça com vida útil limitada |

Depois desta revisão, as **únicas peças THT são os dois conectores**.

## 5 · Arquitectura de alimentação

```
P1.20 (24 V) --+-- TP -- TVS 33 V --> GND_24V
               |
               +-- F202 750 mA -- D202 --> +24V_ADC --> 6 fusiveis de canal --> campo
               |                              +-- C201 10 uF/100 V + 100 nF
               |                                 (todo o bulk fica deste lado)
               |
               +-- F201 250 mA -- D201 -- R206 22R --> +24V_REG -- C200 2u2/100 V
                                                          |
                                                          +-> TPS7A4001 --> +5V
                                                                 +-> SPX3819 --> 3V3_REF
                                                                       +- ferrite -> VDD do ADC
                                                                       +- ferrite -> VCC2 do isolador
                                                                       +- ADR4525 -> +2V5_REF -+-> VREF do ADC
                                                                       |                       +-> topo do divisor do NTC
                                                                       +- TL431 -> grampo 3,60 V

P1.17 (+5 V) --> MCP1824 --> +3.3V_DIG --> VCC1 e EN1 do isolador        [fecha G2]

GND_24V --[R200 0 ohm]-- GND_ADC           DGND separado pelo ISO7141
```

**Sequenciamento:** não há requisito. Os rails sobem em cascata e nenhum
componente exige ordem. O `TPS7A4001` tem arranque suave próprio.

**Empilhamento:** 4 camadas, igual à V4.1.

**Retorno de massa — restrição para a F3.** Com as massas unidas, o retorno dos
seis laços, até 120 mA, circula por `GND_ADC`. Para a queda IR ficar abaixo de
1 LSB (0,610 mV com a referência de 2,5 V), a resistência entre as massas dos
burden e o `AGND` do ADC tem de ser **< 5 mΩ**. Isto condiciona o layout e o
ponto único de união.

## 6 · Requisitos de DFT incorporados

Nove pontos de prova: `+24V`, `+24V_ADC`, `+24V_REG`, `+5V`, `3V3_REF`,
`+2V5_REF`, `GND_24V`, `GND_ADC` e `DGND`. O de `DGND` fica do lado do
barramento, porque uma sonda no lado de campo com a placa ligada atravessaria a
separação pela massa do osciloscópio. Três fiduciais na face SMD.

**Retirado do escopo:** o critério `RD3`, de acesso mecânico aos pontos com a
placa montada no quadro. Não há plano do quadro, e um critério que ninguém pode
verificar não se congela.

## 7 · Registo de dúvidas

| # | Pergunta | Resposta | Data | Estado |
|---|---|---|---|---|
| D1 | Substituição directa da V4.1? | Sim, intercambiável | 2026-09-23 | Fechada |
| D2 | Ambiente? | ~~Industrial, −40 a +85 °C~~ **0 a +65 °C certificado, dimensionado a +70 °C** (projectista, 2026-09-24) | 2026-09-24 | Fechada |
| D3 | Certificação? | Nenhuma, barreira funcional | 2026-09-23 | Fechada |
| D4 | Contrato do bus de 14 pinos entra? | Não, fora de âmbito | 2026-09-23 | Fechada |
| D5 | O firmware calibra? | Sim, com **constante comum** | 2026-09-23 | Fechada |
| D6 | Requisito de imunidade a surto? | **Não há requisito escrito** | 2026-09-23 | Fechada, `RA3` reescrito |
| D7 | Empilhamento? | 4 camadas | 2026-09-23 | Fechada |
| D8 | Plano do quadro? | Não há | 2026-09-23 | Fechada, `RD3` retirado |
| **D9** | **Datasheet do `MCP3208`** | **Fornecido: `DS21298E`** | 2026-09-23 | **FECHADA**, ver §2.7 |

### D9 — fechada, e trouxe mais do que se esperava

O projectista forneceu o `DS21298E` em 2026-09-23. O estudo está em §2.7 e
produziu quatro alterações ao projecto e três restrições de firmware.

**A revisão 2 deste documento estimou que o conversor teria folga de sobra.
Estava errada, e por um motivo que só o datasheet mostra:** os erros de offset e
de INL do `MCP3208` são **tensões fixas**, não fracções. Ao baixar a referência
de 5 V para os nossos 2,5 V, o sinal encolhe para metade e o erro não, portanto
o peso relativo duplica. Com constante comum, o conversor sozinho vale 0,215 %
contra um tecto de 0,2 % para a placa inteira.

**Item menor, que já não bloqueia nada:** o coeficiente de 57 ppm/°C do
`SPX3819` foi lido de uma tabela que o extractor devolveu desordenada. Saiu do
orçamento quando a referência passou a ser peça própria.

### Calibração: constante comum, e o conflito que isso deixa com `RE1`

Confirmado pelo projectista em 2026-09-23: **a calibração é uma constante comum
a todas as placas, não por unidade.**

| Critério | Pior caso | Típico | Tecto | Veredito |
|---|---|---|---|---|
| `RE1`, a 25 °C | **0,237 %** | 0,139 % | 0,2 % | **reprova no pior caso** |
| `RE2` e `RB3`, deriva 0 a +70 °C | **0,114 %** (cal. a 25 °C) · **0,178 %** (cal. a 0 °C, op. a 70 °C) | — | 0,2 % | cumpre |

O conversor sozinho vale 0,215 % no pior caso, porque os seus erros de offset e
INL são tensões fixas e a referência de 2,5 V duplica-lhes o peso relativo.
**Nenhum componente o resolve**, e o hardware não muda com esta decisão.

**Fica uma decisão de escopo em aberto, que volta ao Portão 0:** reescrever
`RE1` pelo pior caso garantido, ou mantê-lo a 0,2 % declarado como típico.

## 8 · Encerramento do loop

**ENCERRADO tecnicamente em 2026-09-23: zero dúvidas técnicas.** A calibração
é uma **constante comum**, confirmado pelo projectista. Isso deixa o critério
`RE1` em conflito com o escopo — 0,237 % no pior caso contra 0,2 % — e essa é
uma **decisão de escopo** que volta ao Portão 0. Não bloqueia a F2, porque o
hardware é idêntico qualquer que seja a resposta.

| Gap da F0 | Estado |
|---|---|
| G3 electrolíticos | **Fechado**: saem, entram cerâmicos de 100 V |
| G4 fusível da rama do regulador | **Fechado**: `CC12H250mA-TR` mais `R206` de 22 Ω. Margem 15,3× |
| G5 nível de surto inventado | **Fechado**: não há requisito, o critério reescreve-se sem número |
| G6 limite de `3V3_REF` | **Adiado** para a etapa 2.3b, que é onde se derivam os absolutos máximos |
| G7 acesso mecânico | **Fechado**: `RD3` sai do escopo |
| G13 datasheet do `MCP3208` | **Fechado**: fornecido e estudado. Ver §2.7 |

## 8b · O que a F1 deixou por corrigir no esquemático — lista fechada para a F2

A folha `02_entrada.kicad_sch` foi povoada **antes** desta F1 e, a partir de
agora, **contradiz o planeamento em quatro pontos**. Não se tocou no CAD: a F1
está aberta e a etapa 2.2b é o lugar onde isto se aplica. A lista é fechada, e
qualquer diferença fora dela na F2 é defeito de transcrição, não alteração.

| # | O que está na folha hoje | O que tem de ficar |
|---|---|---|
| 1 | `F201` com valor `100mA T` | **FEITO 2026-09-23.** `CC12H250MA-TR` |
| 2 | Não existe `R206` | **FEITO 2026-09-23.** 22 Ω em 0805 entre o cátodo de `D201` e a derivação de `C200`. **A versão anterior desta linha dizia `D202`, que é o diodo dos laços: o esquemático provou o contrário e a linha estava errada** |
| 3 | Notas com «1,69 mA2s», «0,37 mA2s», «5,65 mA2s», «1,5 mA2s» | **FEITO 2026-09-23.** Notas refeitas em A²s, e a nota 5, que dizia que `C200` era de 10 µF, corrigida |
| 4 | Ressalva do bloco de título: «F1 formal saltada. MPN do F201 por confirmar» | **FEITO 2026-09-23** |

Um quinto ponto a **verificar**, não a corrigir: a nota 3 da folha estima o
consumo da rama do regulador em cerca de 5 mA e esta F1 usou 12 mA. A conta de
`R206` é insensível à diferença — mesmo a 20 mA a queda seria 0,44 V, contra os
7 V que o `TPS7A4001` precisa e os 19 V disponíveis. Mas o número deve ser
fixado de uma vez na etapa 2.3b, e o `ADR4525` acrescenta-lhe até 950 µA de
corrente de repouso que ainda não estava contada.

### O que o datasheet do conversor acrescentou à lista, para as folhas 05 e 07

Estas folhas ainda não estão desenhadas, por isso não são correcções: são
**especificações de partida**, e ficam aqui para que a 2.2b não as reinvente.

| # | Requisito | Origem |
|---|---|---|
| 5 | Mapa de canais: campo em `CH0`,`CH1`,`CH2`,`CH3`,`CH6`,`CH7`; `CH4` termístor; `CH5` no trilho | Pinagem da V4.1 medida pad a pad, §2.7a |
| 6 | `U5` passa a `MCP3208T-BI/SL` | DS21298E pág. 37, §2.7b |
| 7 | Topo do divisor do termístor em `+2V5_REF`, não em `3V3_REF` | §2.7e. Sem isto o canal satura a 70 °C |
| 8 | 1 µF **mais** 100 nF no `VDD` do conversor, no pino | DS21298E §6.4, pág. 23 |
| 9 | 1 µF em `+2V5_REF` | DS21298E fig. 6-3, pág. 23 |
| 10 | O 100 nF de cada canal encostado ao pino do canal | §2.7d. É o que substitui o buffer que o datasheet pede |
| 11 | `AGND` (pino 14) e `DGND` (pino 9) ligados os dois a `GND_ADC`, mas com percursos próprios | §2.7a |

### Verificações abertas da F2

> A lista única e numerada da F2 vive em `intencao_EBM2_V5.md` rev. 2, §14. As duas linhas abaixo são as mesmas `V5` e `V6` de lá.

| # | O quê | Porque está aberto | Fecha com |
|---|---|---|---|
| V5 | MPN de `R206`, 22 Ω 0805 anti-surto | Tem de aguentar 0,55 mJ em 56 µs a cada arranque; nenhum datasheet de resistência de impulso está na pasta | Datasheet com curva de impulso |
| V6 | MPN de `C200`, 2,2 µF ≥ 100 V X7R 1206 | O part number candidato não consta do catálogo Murata da pasta | Datasheet com curva de capacidade vs polarização DC |

### Três restrições que não são de hardware e têm de chegar ao firmware

1. **Relógio SPI ≤ 1 MHz.** Os 2 MHz só estão garantidos a `VDD` = 5 V. A 3,3 V
   o datasheet não dá valor, e o único garantido abaixo disso é o de 2,7 V.
2. **A transacção de 24 bits de cada canal tem de ser atómica.** A 85 °C o
   conversor só garante a carga do condensador de amostra durante 1,2 ms depois
   do fim da amostragem. Uma transacção partida pelo escalonador do Linux dá uma
   leitura com erro de linearidade **e sem indicação de erro**.
3. **Cadência por canal abaixo de 4 kHz.** Acima disso a resistência de 3,3 kΩ
   começa a custar mais de 1 LSB a repor a carga do filtro.

## 9 · O erro desta sessão, e o que ele custou

A revisão 1 deste documento afirmou que **a tabela de selecção do fusível Eaton
não estava na pasta de referência**. Está. Chama-se `Eaton_fusible_lento.pdf`.

A afirmação nasceu de um facto verdadeiro: o ficheiro chamado
`eaton-cc12h-high-i2t-chip-fuses-data-sheet.pdf` contém, no seu interior, o
datasheet do `ADR4525`. Disso concluiu-se que a tabela não existia.
**Procurou-se por nome e leu-se o silêncio como ausência**, que é exactamente o
mesmo erro de método que já tinha acontecido com os Gerbers nesta mesma sessão.

Duas tentativas de correcção falharam antes de acertar, e vale registá-las:

1. Uma busca com `strings` sobre os PDF devolveu **zero** ocorrências de tudo,
   inclusive de `ADR4525` num ficheiro onde ele está. O texto de um PDF vive
   comprimido, e `strings` não o vê. **Um zero devolvido por uma ferramenta que
   não consegue ler o formato não é um zero.**
2. A extracção de texto da tabela de códigos Panasonic entrelaçou duas colunas e
   produziu emparelhamentos falsos. Só a **página renderizada como imagem** deu
   a leitura correcta.

O que a busca certa mudou no projecto:

| | Revisão 1 | Revisão 2, com o datasheet |
|---|---|---|
| `F201` | «Eaton `CC12H` 100 mA» | `CC12H250mA-TR` — **não existe 100 mA na série** |
| Margem de I²t de `F201` | não calculada | 2,1×, **reprova** `RA2` sem `R206` |
| `R206` | não existia | **peça nova obrigatória**, 22 Ω 0805 |
| Unidades de I²t | «mA²s» | **A²s** — rótulo errado por um factor de 10⁶ |
| Travão do orçamento de erro | «burden de 0,05 % e 10 ppm» | **não existe a 110 Ω** |
| `RE1` | «no limite, 0,182 % contra 0,2 %» | **passa com folga**: eram dois orçamentos, não um |

Cinco dos seis itens são consequência de não ter aberto dois ficheiros.

### Revisão 3, com o datasheet do conversor

O projectista forneceu o `DS21298E` no mesmo dia. O que ele mudou:

| | Revisão 2 | Revisão 3, com o datasheet |
|---|---|---|
| Mapa de canais | assumido sequencial, `CH0` a `CH5` | **`CH0`-`CH3`, `CH6`, `CH7`**; `CH4` é o termístor |
| Grau do conversor | `-CI`, herdado sem olhar | **`-BI`**: metade do INL, mesma peça no resto |
| Termístor | herdado a pender de `3V3_REF` | **passa a `+2V5_REF`**: saturava a 70 °C |
| Desacoplamento do `VDD` | 100 nF, herdado | **1 µF**, que é o que o datasheet pede |
| Peso do conversor no orçamento | «sobra espaço, 0,116 a 0,172 %» | **0,215 % sozinho**: os erros são tensões fixas |
| `RE1` com constante comum | «passa com folga» | **reprova a 0,237 %**, e nenhuma peça o resolve |
| Deriva da referência | 2 ppm/°C | **4 ppm/°C**, que é o método bowtie |

**O padrão repete-se e vale a pena dizê-lo: quatro dos sete itens são coisas
herdadas da V4.1 que eu tinha copiado sem verificar.** O mapa de canais, o grau
do conversor, o divisor do termístor e o desacoplamento. Nenhum dava erro em
nenhuma ferramenta. O mapa de canais em particular teria produzido duas leituras
erradas em campo sem uma única mensagem de aviso.

```yaml
evidencia:
  skill: 2shw-pcb:planejamento
  artefatos: [planejamento_pcb_EBM2_V5.md]
  componentes_total: 27
  componentes_biblioteca: 0
  componentes_novos: 4
  rodadas_entrevista: 1
  duvidas_abertas: 0
  decisoes_de_produto_pendentes: 1
  datasheets_verificados_nesta_fase: 4
  avanco_escopo_pct: 95
```

> **Nota sobre a biblioteca de blocos.** A skill manda consultar primeiro a
> biblioteca 2Solve. **Não há caminho de repositório configurado** — é uma
> pendência de padrão da casa declarada na própria skill. Por isso
> `componentes_biblioteca` é zero e a origem está marcada como herdado ou
> portado da EBM7.
