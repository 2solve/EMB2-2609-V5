# Documento de intenção — IC2S Extension Board EBM2 V5 (6AI)

> # ⚠ SUPERADO EM OITO PONTOS — 2026-09-23
>
> Este texto foi escrito **antes** de existir F0 e F1. As duas fases correram
> depois, no mesmo dia, e **`planejamento_pcb_EBM2_V5.md` manda sobre este
> documento** em tudo o que se contradiga. Os quatro pontos conhecidos:
>
> 1. **O fusível da rama do regulador não pode ser de 100 mA.** A série Eaton
>    `CC12H` não tem essa corrente: começa em 250 mA. Passa a `CC12H250MA-TR`.
> 2. **Falta uma peça:** a resistência `R206` de 22 Ω em 0805, em série na rama
>    do regulador. Sem ela a margem de I²t é 2,1× e o critério `RA2`, que exige
>    10×, reprova. Com ela são 15,3×.
> 3. **As unidades de I²t deste documento estão erradas por um factor de 10⁶.**
>    Onde se lê mA²s deve ler-se A²s. Os rácios e as conclusões não mudam.
> 4. **A calibração é uma constante comum a todas as placas**, não por unidade.
>    A tolerância inicial de cada peça, por isso, **não** se calibra. O orçamento
>    de erro refez-se em duas contas separadas, a de 25 °C e a de temperatura, e
>    ambas passam.
>
> **Mais quatro pontos, depois de o datasheet `DS21298E` do conversor chegar:**
>
> 5. **O mapa de canais do ADC não é sequencial.** Os seis canais de campo estão
>    em `CH0`, `CH1`, `CH2`, `CH3`, `CH6` e `CH7`. O `CH4` lê o termístor da
>    placa e o `CH5` está preso ao trilho. Desenhá-los em sequência partiria o
>    firmware existente sem produzir um único erro visível.
> 6. **O conversor passa de `MCP3208T-CI/SL` para `-BI/SL`**, que tem metade do
>    INL com a mesma pinagem e o mesmo protocolo.
> 7. **O divisor do termístor passa a pender de `+2V5_REF`.** Mantido em
>    `3V3_REF`, o canal saturaria a 70 °C, dentro da gama de operação.
> 8. **`RE1` não se cumpre com calibração por constante comum.** O pior caso é
>    0,237 % contra um tecto de 0,2 %, porque os erros do conversor são tensões
>    fixas e a referência de 2,5 V duplica-lhes o peso. Com calibração por
>    unidade são 0,055 %.
>
> A ressalva abaixo, que diz não existir documento de F1, **já não é verdade**.
> Fica no sítio porque descreve com exactidão o estado em que este texto nasceu.

| | |
|---|---|
| Projecto | IC2S Extension Board EBM2, 6 entradas 4-20 mA |
| Revisão | V5 (parte da V4.1 convertida e auditada) |
| Data | 2026-09-23 |
| Fase | F2, etapa 2.2a |
| Autoridade | **Este documento manda até ao primeiro ERC limpo.** A partir daí manda o `.kicad_sch` e este texto congela como registo de intenção. |
| Estrutura | Hierárquica, 7 folhas, mesmo padrão da EBM7 V2.3 Legacy |

> **Ressalva de processo.** Não existe documento de F1 para esta revisão. O que
> substitui a F1 é a análise verificada da sessão de 2026-09-22/23: conversão
> auditada (16 critérios), netlist traçada canal a canal, e três decisões de
> produto respondidas pelo projectista. Quem assinar o Portão 1 tem de saber
> que a F1 formal foi saltada.

---

## 1 · Âmbito da alteração

Porta-se da **EBM7 V2.3 Legacy** apenas a **arquitectura de alimentação e a
protecção de entrada**. Decisão do projectista, 2026-09-23: *"usar el ejemplo de
la legacy en esta ebm2, solo las cosas así importantes tipo la alimentación"*.

**NÃO se porta** (analisado e descartado):

- Frontal de laço com eFuse `TPS26613` + rail de 12 V. São 6 eFuses, um rail novo
  e o divisor de `VSNS`; além disso o burden total actual da EBM2 (409 Ω) excede o
  tecto que o `TPS26613` admite com esse divisor.
- Conversor `AD7124-8` e o bloco de célula de carga. A EBM2 não tem ponte.

## 2 · Estrutura de folhas

Raiz sem componentes. Sete folhas, espelhando a Legacy menos a folha da célula:

| Folha | Conteúdo |
|---|---|
| `01_conectores` | `P1` (20 pinos, barramento) e `P2` (14 pinos, campo) |
| `02_entrada` | Entrada de 24 V: TVS, fusíveis, díodos de bloqueio, net-tie das massas |
| `03_alimentacao` | LDO de entrada alta, `SPX3819`, referência de 2,5 V |
| `04_barreira` | `ISO7141` e a barreira funcional |
| `05_adc` | `MCP3208` e o seu desacoplamento |
| `06_lacos` | Os 6 canais 4-20 mA |
| `07_ntc` | NTC de temperatura de placa e o seu divisor |

## 3 · Bloco de entrada de 24 V — `02_entrada`

### Ligações, como especificação

O pino 20 de `P1` traz os 24 V do barramento e o pino 19 traz o retorno. Do pino
20 sai um ponto de teste, e desse mesmo nó o cátodo de um TVS cujo ânodo vai a
`GND_24V`. Desse nó saem **duas ramas em paralelo**:

- **Rama dos laços.** Fusível retardado, depois o ânodo de um Schottky de bloqueio
  cujo cátodo forma a rede `+24V_ADC`. Nessa rede ficam o bulk de 10 µF/100 V e um
  100 nF/100 V, e dela saem os seis fusíveis de canal.
- **Rama do regulador.** Fusível retardado, depois o ânodo de um segundo Schottky
  cujo cátodo forma `+24V_REG`, com o seu próprio bulk de 10 µF/100 V, e alimenta
  a entrada do LDO de entrada alta da folha `03`.

`GND_24V` liga a `GND_ADC` por **uma única resistência de 0 Ω**, e por mais nada.

### Porquê

**Porque duas ramas e não uma.** Separar a alimentação dos sensores de campo da
alimentação da electrónica faz com que um curto no campo não derrube o ADC. É a
topologia da Legacy e é a razão pela qual ela tem `F1` e `F2` e não um só fusível.

**Porque o díodo de bloqueio substitui o zener.** A V4.1 tem `D26`, um zener de
2,45 V **em série** na entrada, com o cátodo virado ao barramento. Um zener de
classe µA a conduzir os ~130 mA de toda a placa. O mesmo defeito existia na EBM7
V1.1 (`D25`) e é provavelmente um erro de biblioteca, com ânodo e cátodo trocados
em relação ao footprint. Substitui-se por um Schottky de 100 V, que é o que a
função pede.

**Porque entra um TVS.** A rede `+24V` da V4.1 contém **só** o zener e os três
fusíveis: nenhum clamp. A única protecção do barramento está na base board, do
outro lado de um cabo, de um jumper e de pinos de conector, com toda a indutância
que isso acrescenta.

**Porque fusíveis retardados e não rápidos.** Este é o ponto mais importante do
documento. A EBM7 V1.1 queimou fusíveis em campo de forma recorrente. A causa foi
fechada: a ordenação dos I²t dos fusíveis contra os condensadores do lado de
carga. **A EBM2 V4.1 tem a mesma topologia, peça por peça:**

| Rama | Fusível actual | Condensador do lado de carga |
|---|---|---|
| Laços 1-3 | `F7`, 160 mA rápido | `C30`, 10 µF |
| Laços 4-6 | `F9`, 160 mA rápido | `C15`, 10 µF |
| Lógica | `F8`, 125 mA rápido | `C29`, 10 µF |

Três caminhos independentes, três fusíveis rápidos, três condensadores de 10 µF a
carregar através deles. É o mesmo mecanismo. Ao passar a **750 mA retardado** o
problema fecha-se por margem: a energia que o arranque dos 10 µF entrega não tem
relação com o I²t de um retardado dessa classe.

### Dimensionamento

| Grandeza | Valor | Como sai |
|---|---|---|
| Consumo dos laços | 120 mA | 6 canais × 20 mA, fundo de escala simultâneo |
| Consumo dos LED | 4,5 mA | 3 × (24 − 1,9) / 14,7 kΩ |
| Consumo da electrónica | ~4 mA | ver §4 |
| **Total na entrada** | **~130 mA** | soma |
| Fusível por rama | 750 mA retardado | 5,8× o consumo total; margem de I²t |
| Fusível por canal | 50 mA | 2,5× os 20 mA do laço; hoje são 100 mA |
| Díodo de bloqueio | Schottky 100 V | queda baixa e tensão de bloqueio muito acima dos 24 V |

## 4 · Bloco de alimentação — `03_alimentacao`

### Ligações, como especificação

`+24V_REG` entra no LDO de entrada alta, cuja saída forma `+5V`. Dessa rede sai a
entrada do `SPX3819-3.3`, cuja saída forma `3V3_REF`. De `3V3_REF` saem:

- uma ferrite até `VDD` do `MCP3208`;
- uma ferrite até `VCC2` e `EN2` do `ISO7141`;
- a entrada da referência de 2,5 V, cuja saída forma `+2V5_REF` e vai **só** ao
  pino `VREF` do `MCP3208`;
- os clamps superiores dos seis canais e o divisor do NTC.

### Porquê

**Porque não se porta o conversor comutado da Legacy.** A Legacy usa um `R-78HB`
de 0,5 A e precisa de ~45 mA de pré-carga para regular com carga leve. Mas o rail
de 5 V da EBM2 alimenta **só** o LDO, e atrás do LDO estão ~4 mA: o `MCP3208`, o
lado 2 do `ISO7141`, a referência e o divisor do NTC. Pôr um comutado de 500 mA e
deitar 45 mA à massa para que funcione é gastar onze vezes a carga real. Um linear
de entrada alta dissipa 19 V × 4 mA ≈ **76 mW**, sem pré-carga e sem dissipador.

**Porque continua a haver duas etapas.** O `SPX3819` admite no máximo ~16 V de
entrada, portanto não se lhe podem dar os 24 V directos: a etapa intermédia é
obrigatória. E mantê-la dá um segundo estágio de rejeição de ruído imediatamente
antes do ADC, que a 0,18 % de exactidão conta. *(Verificação V2: confirmar o
máximo de entrada no PDF; a linha da tabela saiu mal extraída.)*

**Porque a referência é peça própria e não o rail.** É a alteração que mais
exactidão compra, e sai de graça em pinos: o `MCP3208` tem `VREF` no pino 15 e
`VDD` no pino 16, **separados**. Hoje ambos penduram do mesmo nó e por isso a
referência da medida é a tolerância do regulador, ±1 %. Separá-los não exige tocar
no ADC.

## 5 · Massas e barreira — `02_entrada` e `04_barreira`

**Dois domínios depois da alteração**, não três:

| Domínio | Antes (V4.1) | Depois (V5) |
|---|---|---|
| `DGND` | isolado pelo `ISO7141` | **igual, não se toca** |
| `GND_24V` | isolado por `U1`/`U7`/`U8` | unido a `GND_ADC` pelo net-tie |
| `GND_ADC` | isolado | unido a `GND_24V` |

O `ISO7141` mantém-se e passa a ser a **única** barreira da placa. Declara-se
**funcional, não de segurança**, e não se declara IEC 60664-1. A premissa que o
sustenta foi confirmada pelo projectista em 2026-09-23 (*"la misma cosa que la
EBM7 legacy"*): os 24 V vêm sempre da fonte DRC-100B da base board, onde já existe
a barreira contra a rede.

A barreira desenha-se na folha como linha tracejada com texto, e confere-se no
desenho que nenhum condutor a atravessa.

## 6 · Cadeia analógica — `06_lacos`

Não muda a topologia. Mudam três valores, e um deles deixa de ser opcional.

### Ligações, como especificação (por canal, exemplo do canal 5)

O pino 11 de `P2` recebe o retorno do laço. Desse nó sai o cátodo de um TVS de
30 V cujo ânodo vai a `GND_ADC`, e sai também um dos terminais da resistência
série de 249 Ω. O outro terminal forma o nó de medida, onde ficam o burden até
`GND_ADC` e a resistência de antialias de 3,3 kΩ. Do outro lado da antialias fica
o condensador de 100 nF a `GND_ADC`, o clamp duplo de baixa fuga e o pino do canal
do `MCP3208`.

### O que muda, e porquê

| Peça | Antes | Depois | Porquê |
|---|---|---|---|
| Burden | 160 Ω 1 % | **110 Ω 0,1 %** | mesmo valor da Legacy; a 20 mA dá 2,200 V, 88 % da escala de 2,5 V, e o fundo de escala sobe a 22,7 mA |
| Clamp | `BAT54S` | **`BAV199`** | a fuga inversa de um Schottky sobre 3,3 kΩ come sozinha o orçamento de 0,18 % |
| Fusível de canal | 100 mA | **50 mA** | 2,5× os 20 mA do laço; alinha com a Legacy |

O clamp deixa de ser opcional por aritmética: o `BAV199` dá 5 nA a 25 °C, que
sobre 3,3 kΩ são **16 µV** contra 2,5 V, ou seja 0,0007 %. Um Schottky na mesma
posição está três ordens de grandeza acima.

**A resistência série de 249 Ω não se toca nesta etapa.** É protecção, e a regra
da casa é que uma protecção só se altera depois de listar todos os pinos da rede
contra os seus abs max e seguir a corrente de clamp até ao sumidouro. Isso faz-se
na 2.3b. *(Verificação V3.)*

### Prova de uma multiplicação

| Corrente no laço | Tensão no burden | Fracção da escala |
|---|---|---|
| 4 mA | 0,440 V | 17,6 % |
| 20 mA | 2,200 V | 88,0 % |
| 21 mA (alarme alto NAMUR) | 2,310 V | 92,4 % |
| 22,7 mA | 2,500 V | 100 %, saturação |

Um LSB = 2,5 V / 4096 = **0,610 mV**, que correspondem a **5,55 µA** de corrente
de laço.

## 7 · Orçamento de erro

| Fonte | Contribuição |
|---|---|
| Referência de 2,5 V, tolerância inicial | ±0,02 % |
| Burden 110 Ω a 0,1 % | ±0,10 % |
| Deriva do burden, 25 ppm/°C sobre 60 °C | ±0,15 % |
| **Soma quadrática** | **±0,18 %** |

Cumpre o objectivo de 0,1 a 0,2 % fixado pelo projectista. A V4.1 estava em
±1,4 %: é uma melhoria de factor oito.

## 8 · Lista de peças — nenhuma é nova

Todas as peças que entram **já estão montadas na EBM7 V2.3 Legacy**, portanto não
há qualificação de fornecedor nova nesta revisão:

| Função | Referência na Legacy |
|---|---|
| TVS de entrada | `D200` |
| Fusíveis retardados | `F1`, `F2` |
| Schottky de bloqueio | `D1`, `D5` |
| LDO de entrada alta | `U12` |
| LDO de 3,3 V | `U3` — e já existe na EBM2 como `U11` |
| Referência de 2,5 V | `U7` |
| Clamps de baixa fuga | `D11`, `D12` e outros |
| Net-tie das massas | `R200` |

Os MPN concretos fixam-se na 2.2b contra a BOM da Legacy, não aqui.

## 8b · Dimensionamento verificado contra datasheet

Todos os números desta secção saem de PDF lido nesta sessão, com a referência do
ficheiro. O que não foi lido está marcado como tal.

### TVS de entrada — Bourns SMA6J33A-Q

| Parâmetro | Valor | Fonte |
|---|---|---|
| Tensão de trabalho (VRWM) | 33 V | tabela de selecção |
| Tensão de ruptura (VBR) | 36,7 a 40,6 V | idem |
| Fuga a VRWM | 1,0 µA | idem |
| **Tensão de grampeamento (VRSM)** | **58,1 V a 11,3 A** | idem |

Os 58,1 V são o número que manda, e **obrigam a duas correcções** em relação ao
que a V4.1 tem montado:

**Correcção 1 — o díodo de bloqueio tem de ser de 100 V.** A EBM2 usa hoje
`PMEG6010CEH`, de 60 V. Com o TVS a grampear em 58,1 V sobram 1,9 V de margem,
o que não é margem. Usa-se o `MBR1H100SF` de 100 V, que é o que a Legacy monta.

**Correcção 2 — o bulk tem de ser de 100 V.** A EBM2 tem `C12` e `C28`,
electrolíticos `ESL107M050AGMAA` de 100 µF / **50 V**. A 58,1 V de grampeamento
ficam 8,1 V acima da sua tensão nominal. Substituem-se por cerâmicos de
100 V, como na Legacy. É também o que elimina o relógio de vida útil do
electrolítico.

### Regulador de entrada alta — TI TPS7A4001

| Parâmetro | Valor | Consequência |
|---|---|---|
| Faixa de entrada | 7 a 100 V | 24 V fica a meio da faixa |
| **Corrente de saída máxima** | **50 mA** | 10× a carga calculada |
| Corrente de repouso | 25 µA | irrelevante no orçamento |
| Queda (dropout) | 290 mV | folga enorme a 24 V de entrada |
| Exactidão | 1 % | não entra no erro de medida: a referência é peça própria |
| Estabilidade | Cout > 4,7 µF, Cin > 1 µF | fixa os condensadores do bloco |

### Referência — Analog Devices ADR4525

> **Achado de organização:** o PDF desta peça está na pasta de referência com o
> nome `eaton-cc12h-high-i2t-chip-fuses-data-sheet.pdf`. **O ficheiro está mal
> nomeado**: o conteúdo é o datasheet da família ADR4520/25/30/33/40/50. Renomear,
> ou o próximo que procure o fusível vai achar que não existe.

| Parâmetro | Valor | Consequência |
|---|---|---|
| **Erro inicial de saída** | **±0,02 %** (graus B, C, D) | é o número do orçamento de erro do §7 |
| Coeficiente de temperatura | 2 ppm/°C (grau B, −40 a +125 °C) | 0,012 % sobre 60 °C |
| Faixa de entrada | 3 a 15 V | alimenta-se de `3V3_REF`, não dos 5 V |
| Queda | 300 mV a 2 mA | com 3,3 V de entrada sobram **800 mV** |
| Corrente de repouso | 950 µA (máximo) | entra no balanço abaixo |

### Balanço de corrente do rail analógico

| Consumidor | Corrente |
|---|---|
| `MCP3208` | 0,55 mA |
| `ISO7141`, lado 2 | ~2 mA |
| `ADR4525` | 0,95 mA |
| Divisor do NTC | 0,21 mA |
| Clamps e fugas | desprezável |
| **Total** | **~3,7 mA; dimensiona-se a 5 mA** |

Dissipação do `TPS7A4001` a 24 → 5 V com 5 mA: **95 mW**. Do `SPX3819` a
5 → 3,3 V com 5 mA: **8,5 mW**. Nenhum dos dois precisa de área térmica.

### Porque se mantêm duas etapas de regulação

Com a referência separada, a exactidão do rail deixa de importar — mas o **ruído**
não. O `SPX3819` é especificado como baixo ruído e o `TPS7A4001` não. O rail que
alimenta `VDD` do ADC e a referência é o último, portanto é o que tem de ser
limpo. Somando que o `SPX3819` já está montado na EBM2 como `U11`, manter as duas
etapas não custa peça nova nem qualificação.

### Fusíveis

| Rama | Corrente que leva | Fusível | Margem |
|---|---|---|---|
| Laços | 125 mA (6 × 20 mA + LED) | 750 mA retardado | 6,0× |
| Regulador | ~5 mA | 100 mA retardado | 20× |
| Por canal | 20 mA | 50 mA | 2,5× |

O fusível da rama do regulador **não** é de 750 mA como na Legacy. Ali essa rama
alimenta mais coisas; aqui leva 5 mA, e um fusível de 750 mA sobre 5 mA não
protege nada. A 100 mA retardado a protecção é real e a energia de arranque do
bulk de 10 µF continua uma ordem de grandeza abaixo do seu I²t.

## 9 · Verificações abertas

| | Verificação | Fecha com |
|---|---|---|
| **V1** | Com as massas unidas, o retorno dos seis laços (até 120 mA) circula pela massa de referência do ADC. Para a queda IR ficar abaixo de 1 LSB (0,610 mV) a resistência entre as massas dos burden e o `AGND` do ADC tem de ser **< 5 mΩ**. | Layout (F3); decide-se aqui o ponto único |
| **V2** | Máximo de tensão de entrada do `SPX3819`. Lido como 16 V numa linha de tabela mal extraída. | `grep` no PDF, etapa 2.3b |
| **V3** | A resistência série de 249 Ω e os fusíveis de canal: caminho da corrente de clamp até ao sumidouro, com todos os pinos da rede contra os abs max. | Etapa 2.3b |
| **V4** | `R34` tem os pinos trocados entre esquemático e placa **no projecto original**. Inócuo por ser resistência, mas prova dessincronização. | Corrigir na 2.2b e registar |

## 10 · O que NÃO muda

Os seis canais mantêm topologia, conectores e ADC. O `ISO7141` mantém-se com o
lado 1 alimentado pelos +5 V do barramento — o que levanta uma questão que fica
**registada e não resolvida**: se o mestre da base board trabalha a 3,3 V, o
limiar de entrada do isolador alimentado a 5 V pode não ser atingido. Não se pode
decidir sem a especificação da base board, e não se toca nisso nesta revisão.

## 11 · Porta de verificação desta revisão

A estrutura passa de plana a hierárquica, e isso é transcrição de conectividade —
o tipo de trabalho que na primeira placa desta metodologia criou sete defeitos.
A porta que fecha esse risco:

> Exportar a netlist da V5 hierárquica e compará-la **nó a nó** com a netlist da
> V4.1 convertida e auditada. Toda rede cujo conjunto de pinos difira tem de estar
> na lista de alterações enumerada de antemão (§1, §6). Qualquer outra diferença é
> defeito de transcrição.

A V4.1 serve de referência porque a sua conversão está auditada: 16 critérios
cumpridos, ilhas fundidas 0, IoU 99,69 %, furos 139/139, pads 294/294, vias 76/76.
