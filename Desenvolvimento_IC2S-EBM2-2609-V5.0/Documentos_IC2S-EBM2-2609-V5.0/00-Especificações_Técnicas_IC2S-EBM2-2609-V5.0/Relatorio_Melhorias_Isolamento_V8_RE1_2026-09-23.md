# Melhorias propostas — isolamento, transmissor em curto (V8) e exactidão (RE1)

EBM2 V5 · 2026-09-23 · F2, antes do Portão 1

Contas reproduzíveis em `ferramentas/avalia_opcoes_V8_RE1.py`: cada número tem a fonte escrita
no próprio script, e as estimativas estão marcadas. **Nada disto foi medido**: são cálculos
sobre datasheets, a confirmar nas etapas 2.3b e na bancada.

---

## Adenda — envolvente de alimentação corrigido para 18–32 V (mesmo dia)

Os números deste relatório foram calculados com 20–28 V. O painel alimenta-se de rede,
bateria ou painel solar (decisão de 2026-08-31, `escopo_EBM7_respin.md` §7), e o `RA1`
passou a **18–32 V**. Com isso, na rev. 2.2 da intenção: TVS de canal `824520361` (36 V),
`R206` 33 Ω (margem de arranque 12,3× a 32 V) e série `R60x` 100 Ω. Valores actuais, de
`ferramentas/avalia_opcoes_V8_RE1.py`: a **18 V** o transmissor recebe **≥ 10,5 V**; em curto
a **32 V** o limitador dissipa **0,67 W** (Tj ≈ 140 °C com cobre alargado). **A opção 2 da
§2 (5 V / 4,096 V / 180 Ω) deixa só 9,1 V ao transmissor a 18 V e perde interesse.**

## 0 · Duas correcções antes de começar

Ao preparar esta análise encontrei dois erros em documentos que eu próprio escrevi.

1. **A `V8` não é uma regressão face à V4.1.** A intenção diz que os conversores isolados
   da V4.1 limitavam a corrente. O datasheet do `PDM2-S24-S24-S` (CUI, rev. 07/2024) diz
   o contrário: «short circuit protection: **1 s**», «the supply voltage must be discontinued
   at the end of the short circuit duration» e «the output circuit of this product has **no
   protection against overload**». Um transmissor em curto na V4.1 fazia passar ~65 mA
   (83 mA é a corrente nominal do conversor) e punha ~1,1 W numa resistência de 249 Ω 0603.
   **O defeito é herdado**; a V5 apenas o agrava um pouco (74 mA a 28 V, 1,4 W).
2. **Os seis laços da V4.1 não eram dois grupos flutuantes.** Na netlist da V4.1, as saídas
   de 0 V de `U1` e `U8` ligam as duas ao mesmo `GND_ADC`. Havia **um** domínio de campo,
   isolado do 24 V e alimentado por dois conversores. O que a V5 perde é esse isolamento
   entre o campo e a fonte de 24 V, e não um isolamento entre grupos.

Mais dois factos da V4.1 que pesam na decisão:
- o `PDM2-S24-S24-S` está **descontinuado** (histórico de revisões do datasheet, 06/2023);
- a entrada dele aceita **21,6 a 26,4 V**, e o `RA1` pede 20 a 28 V. A V4.1 já estava fora
  de especificação nos dois extremos.

---

## 1 · Transmissor em curto (`V8`) — **recomendação: limitador de corrente por canal**

### O problema, em números (28 V, máximo do `RA1`)

| | Corrente | Na série 249 Ω (0603, 0,1 W) | No burden (0603, 0,1 W) |
|---|---|---|---|
| V4.1 | 65,5 mA | 1,07 W | 0,69 W |
| V5 actual | 74,4 mA | **1,38 W** | **0,61 W** |

Nenhum fusível resolve: um fusível que conduz 22 mA em regime não abre de forma fiável a
65-75 mA. O de 50 mA actual só abre num curto franco à massa, que dá ~2,5 A. Um PTC também
não serve: os mais pequenos seguram 50 mA e disparam acima de 100 mA.

### A solução: um regulador de corrente de dois terminais, em série no retorno de cada canal

```
P2 AINk- --+-- [TVS D60x a GND_ADC] --+-- AL5809-25 (In→Out) --+-- R60x --+-- R61x (burden) -- GND_ADC
                                      |                        |          |
                                      +--|<|-- Schottky -------+          +-- 3,3 kΩ -- ADC
                                          (antiparalelo, protege o -0,3 V do AL5809)
```

- **Peça:** `AL5809-25P1-7` (Diodes, PowerDI123). Garante **23,75 a 26,25 mA de −40 a
  +125 °C**, aguenta 2,5 a 60 V (80 V de máximo absoluto) e tem θJA de 81,4 °C/W com cobre
  alargado (DS36625 rev. 5, pág. 4).
- **Porquê 25 mA:** o conversor satura a 22,7 mA, portanto não se perde nenhuma leitura. O
  alarme alto de 21 mA da NAMUR NE43 lê-se.
- **Porquê no retorno e não no `+`:** em série com o burden **não mexe na medida**, porque
  a corrente é a mesma. No retorno, um curto do `+` à massa não passa por ele: o fusível de
  50 mA abre como hoje. No `+`, esse curto punha os 24 V inteiros no limitador (0,6 W sem
  resistências a partilhar) e o fusível nunca abria. Assim fica também **explicada a razão
  do fusível de 50 mA**, que faltava escrever: abre no curto franco; o curto do transmissor
  é trabalho do limitador.
- **Schottky em antiparalelo:** o AL5809 só aguenta −0,3 V em inversão. Com o TVS
  unidireccional, o terminal pode ir a −0,7/−1 V. O díodo em paralelo não altera a medida
  (liga os mesmos dois nós). **Escolhido: `BAT46W-E3-08`** (Vishay 86406: 100 V; V_F máx.
  0,25 V a 0,1 mA e 0,45 V a 10 mA). A ~3 mA de falha inversa ficam ~0,40 V, acima dos
  −0,3 V do AL5809: **resíduo a confirmar na 2.3b**, com corrente de µA na junção interna.
- **A série de 249 Ω passa a 150 Ω em 1206.** Com o limitador, a função de protecção dela
  deixa de ser essencial, e a queda que sobra compensa a do limitador (ver tabela). O burden
  passa a 1206 (`ERA8AEB111V`: mesma família e tolerância, 47 Ω a 330 kΩ).

### Resultado calculado

| | Corrente de curto | P no limitador | Tj a 85 °C | P série / burden | Tensão para o transmissor (20 V, 20 mA) |
|---|---|---|---|---|---|
| V5 actual | 74,4 mA | — | — | 1,38 / 0,61 W ✗ | 12,04 V |
| **Proposta (A25)** | **26,2 mA** | 0,53 W | **128 °C** | 0,10 / 0,08 W ✓ | **11,52 V** |
| V4.1, para comparar | 65,5 mA | — | — | 1,07 / 0,69 W ✗ | 11,04 V |

**Ressalvas honestas:**
- 128 °C é o pior caso de tudo junto: 85 °C ambiente, 28 V e curto permanente. Fica abaixo
  dos 175 °C absolutos, mas acima dos 125 °C recomendados. Na F3 é preciso cobre (4 camadas,
  vias térmicas) para baixar o θJA para ≤ 75 °C/W.
- A queda do limitador a 20 mA usa o limite conservador de 2,5 V, o mínimo de regulação. O
  valor real a 20 mA, abaixo da corrente de regulação, deve ser menor e está por ler na curva
  ou medir.
- **O escopo não define a tensão mínima que os transmissores precisam.** É um gap. Os
  11,5 V ficam acima da V4.1, mas é preciso saber que transmissores estão instalados.
- Custo: 6 × (limitador + Schottky), ~12 peças pequenas. Não muda `P2` nem o firmware.

**Estudo completo do datasheet (DS36625 rev. 5-2, 16 págs., md5 7e46a75cc76e), 2026-09-23:**
- *Queda a 20 mA* — fig. 15 (25 °C): não conduz abaixo de ~1,4 V; a 20 mA fica em
  ~1,6-1,7 V. As contas usam 2,5 V (mínimo recomendado, págs. 4 e 5) porque a fig. 15 é
  só típica e só a 25 °C. A margem real para o transmissor deve ser ~0,8 V melhor.
- *Corrente em curto* — a tabela garante 23,75-26,25 mA a V_InOut = 3,5 V; a fig. 17
  mostra +1,5 a +2 % a 20 V. Máximo prático em curto ≈ **26,8 mA** (0,08 W no burden e
  0,11 W na série de 150 Ω: dentro de 1206).
- *Térmica* — o calor sai **pela ilha do pino OUT** (pág. 8: «additional vias between the
  pad of the OUT pin»), e `OUT` é a rede `AINk_LIM`, não a massa. Com a ilha mínima e
  10 × 10 mm de cobre (nota 4, θJA 148,6 °C/W), o pior caso (85 °C, 28 V, curto
  permanente, ~0,55 W) daria Tj ≈ 167 °C e o **corte térmico (165 °C, histerese 30 °C,
  fig. 18) entraria em ciclo**. Com cobre alargado (nota 5, 81,4 °C/W), Tj ≈ 130 °C. A
  fig. 10 (placa FR4 de 2 camadas) admite ~30 V a 85 °C para a versão de 25 mA, contra
  os ~20,8 V do nosso curto. **Na F3: cobre e vias na ilha OUT de cada U60x.** Mesmo com
  cobre insuficiente, a peça protege-se: corta, a leitura cai a 0 mA e recupera.
- As figuras térmicas do datasheet não são coerentes entre si (a fig. 10 a 25 °C pede
  1,25 W, mais do que a fig. 9 dá para FR4). Usa-se o caso pior e mede-se na bancada.
- Dois reguladores de corrente em série (o transmissor e o AL5809): abaixo de 23,75 mA
  o AL5809 está fora de regulação e não interage. Perto dos 24 mA os dois tentam
  regular; o ADC já saturou a 22,7 mA. **Ensaio de bancada:** transmissor forçado a
  alarme alto, a ver se há oscilação.

**Alternativa estudada e descartada:** o `NSI45030AZ` (onsemi) tem menos queda, mas a sua
corrente só está garantida a 25 °C (27-33 mA) e, no mesmo pior caso, chega a **152 °C
contra 150 °C de máximo**.

---

## 2 · Exactidão (`RE1`) — **recomendação: confirmar primeiro a rotina de calibração**

### O ponto de partida

| | Pior caso, constante comum |
|---|---|
| V4.1 | **1,43 %** (referência = LDO ±1 %, burden ±1 %, conversor grau -C) |
| V5 actual | **0,237 %** — seis vezes melhor, mas acima dos 0,2 % |

Na V5 domina o conversor: ganho 0,122 %, offset 0,166 %, INL 0,055 %.

### Opção 1 — a rotina de calibração do `RC4` (custo zero de hardware)

O próprio `RC4` diz: «a alteração de escala é absorvida pela **rotina de calibração
existente, executando a calibração de cada canal após a troca**». Duas consequências:

1. **A V5 já depende dessa rotina**, porque muda a escala face à V4.1 (burden de 160 para
   110 Ω, referência de 3,3 para 2,5 V). Sem ela, o firmware actual lê valores errados.
2. **Se a rotina calibra cada canal com uma corrente conhecida na instalação, o offset e o
   ganho desaparecem e o `RE1` fica em 0,055 %** (só o INL), com folga de 3,6×.

**Pergunta a fazer ao firmware:** a rotina mede cada canal contra correntes conhecidas, ou
só aplica um factor introduzido à mão? A resposta decide esta secção inteira.

### Opção 2 — subir o fundo de escala, mantendo o MCP3208 e o protocolo

`VDD` do conversor a 5 V (`+5V_ADC`, que já existe, 4,974 V), referência `ADR4540` de
4,096 V, e burden de 180 Ω.

| | V5 actual | Opção 2 |
|---|---|---|
| Fundo de escala a 20 mA | 2,200 V | 3,600 V |
| Offset (tensão fixa) | 0,166 % | 0,102 % |
| INL | 0,055 % | 0,034 % |
| **Pior caso** | **0,237 %** | **0,192 %** ✓ |
| Saturação | 22,7 mA | 22,8 mA |
| Resolução | 5,55 µA/LSB | 5,56 µA/LSB (igual) |
| Tensão para o transmissor (com o limitador da §1, série 100 Ω) | 11,52 V | 11,12 V |

**Correcção ao planejamento:** este cenário aparece lá como «0,201 %, reprova na mesma».
Esse cálculo usou o INL do grau **-C** (±2 LSB) num cenário que devia ser do grau -B. Com o
grau -B dá **0,192 %: passa**. A frase «não existe escolha de componente que feche `RE1`»
estava duplamente errada.

**Mas a margem é de 4 %**, e o custo é real:
- o `VDD` do ADC e o `VCC2` do isolador passam para `+5V_ADC`;
- os clamps `BAV199` têm de ir para um trilho acima de 4,1 V, com sumidouro (hoje o `TL431`
  grampeia `3V3_REF` a 3,6 V e começaria a cortar o sinal perto do fundo de escala);
- o `SPX3819` e o `3V3_REF` podem deixar de ser precisos;
- a folha 03 é refeita e o `+5V_ADC` precisa de margem para os 4,6 V que o `ADR4540` pede
  (4,974 V dá 0,37 V de folga);
- o divisor do NTC continua ratiométrico: o código lido não muda.

É uma opção sólida **só se a Opção 1 falhar**.

### Opção 3 — `AD7124-8` (o conversor da EBM7)

Cerca de 0,10 % no pior caso, com o burden a dominar, e ainda rejeição de 50/60 Hz e
diagnóstico de fio aberto. **Parte o `RC4`**: outro protocolo, firmware novo.

### Opção 4 — escopo

Declarar os 0,2 % como típico (0,139 %) e registar o pior caso.

---

## 3 · Isolamento — **recomendação: manter a decisão RI1-RI3, com duas salvaguardas baratas**

### O que se perdeu de facto

Na V4.1, o campo inteiro (`GND_ADC`) estava isolado da fonte de 24 V. Na V5, `GND_ADC` liga a
`GND_24V` pelo `R200`. A barreira com a Raspberry continua real: foi verificado que na
MainBoard `GND` e `GND_24V` são redes distintas.

**Quando isto importa:** só com fontes de campo ligadas à terra noutro ponto, tipicamente
transmissores de 4 fios com saída não isolada. Um transmissor de 2 fios alimentado pela placa
é flutuante e não cria laço de massa.

### Opções

| | O que é | Custo | Risco que resolve |
|---|---|---|---|
| **A (recomendada)** | Manter. Escrever no manual: 2 fios, ou 4 fios com saída isolada | Zero | Resolve por regra de instalação |
| A+ | A, mais uma **variante de montagem**: pegada para um módulo isolado e o `R200` como 0 Ω removível | Área de placa; o `RC1` fixa o contorno, mas a V4.1 cabia com três conversores | Permite isolar sem novo layout, se o campo o pedir |
| B | Um conversor isolado **regulado**, entrada 2:1 (cobre 20-28 V), saída 24 V, ≥ 5 W, a alimentar todo o campo; tirar o `R200` | Módulo, eficiência, EMI; o `RA5` (≤ 200 mA) fica justo a 20 V (~190 mA calculados); refazer o arranque e os fusíveis; revisão do RI1-RI3 no Portão 0 | Devolve o nível da V4.1, e com a gama de entrada certa |

**Pergunta a fazer ao campo:** há, nas instalações, transmissores de 4 fios com saída ligada
à terra? Se não houver, A basta. Se houver ou não se souber, A+ é o seguro barato.

---

## 4 · Resumo e ordem sugerida

| # | Acção | Custo | Efeito |
|---|---|---|---|
| 1 | Perguntar ao firmware como funciona a rotina de calibração do `RC4` | Zero | Pode fechar o `RE1` sem hardware |
| 2 | Limitador `AL5809-25` + Schottky por canal; série 150 Ω e burden em 1206 | ~12 peças pequenas | Fecha a `V8` |
| 3 | Perguntar ao campo pelos transmissores de 4 fios e pela tensão mínima deles | Zero | Decide o isolamento e fecha o gap de conformidade |
| 4 | Só se o 1 falhar: 5 V / 4,096 V / 180 Ω | Refazer a folha 03 | `RE1` 0,192 %, margem de 4 % |
| 5 | Só se o 3 o pedir: variante A+ ou opção B | Área / módulo | Isolamento campo ↔ 24 V |

## Fontes

- [CUI PDM2-S datasheet, rev. 07/22/2024](https://www.belfuse.com/media/datasheets/products/power-supplies/PDM2-S.pdf) — protecção de curto de 1 s, sem protecção de sobrecarga, entrada 21,6-26,4 V, modelo descontinuado.
- [Diodes AL5809, DS36625 rev. 5](https://www.diodes.com/assets/Datasheets/AL5809.pdf) — corrente sobre temperatura, 2,5-60 V, θJA, −0,3 V.
- [onsemi NSI45030AZ, rev. 3](https://www.onsemi.com/pdf/datasheet/nsi45030az-d.pdf) — 27-33 mA a 25 °C, 45 V, θJA.
- Microchip DS21298E (MCP3208), pág. 2 e figuras 2-2, 2-15 e 2-18 — na pasta de referência.
- Panasonic AOA0000C307, pág. 2 — gama do `ERA-xAEB`, conforme o planejamento §2.5.
- Netlist da V4.1, exportada em modo só leitura de `C:\hw\hw-ebm2-v4.1`.
