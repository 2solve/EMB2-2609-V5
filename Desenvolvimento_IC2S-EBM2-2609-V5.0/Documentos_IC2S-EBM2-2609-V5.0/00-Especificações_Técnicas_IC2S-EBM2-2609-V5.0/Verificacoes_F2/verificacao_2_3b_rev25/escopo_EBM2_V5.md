---
documento: Escopo de hardware
projecto: IC2S Extension Board EBM2 V5 (6AI)
fase: F0
data: 2026-09-23
autor: gerado por 2shw-pcb:escopo
estado: APROVADO no Portão 0
portao_0:
  aprovado_por: Javier Rivadineira (projectista responsável)
  data: 2026-09-23
  registado_por: sessão Claude Code (a aprovação é do humano; esta sessão só a regista)
  bloqueantes_por_resolver: 0
  gaps_importantes_abertos: 2   # G5 e G7 fechados em 2026-09-23; G3 fechado na F1; resta G4 e G6
---

> ## ✅ PORTÃO 0 — APROVADO
>
> Aprovado por **Javier Rivadineira** em **2026-09-23**.
>
> **Os critérios de aceite da secção 2 ficam CONGELADOS a partir desta data.**
> Eram 23 na assinatura. `RD3` foi **retirado** em 2026-09-23 por falta de
> desenho do invólucro, e `RA3` foi **reescrito** no mesmo dia para tirar um
> nível de surto que a sessão tinha inventado. **Ficam 22.** Retirar e reescrever
> um critério depois da assinatura é alteração de escopo, e fica aqui à vista.
> É contra eles que a F6 valida a placa, e não se reescrevem.
>
> **Estado dos gaps na assinatura** (ver `escopo_EBM2_V5_gaps.md`):
>
> | | |
> |---|---|
> | Bloqueantes | **0** — G1 e G2 resolvidos em 2026-09-23 |
> | Importantes em aberto | **5** — G3 a G7. Assinado com eles abertos; **cada um precisa de dono e data antes do fim da F1** |
> | Menores em aberto | 5 — G8 a G12 |
> | Por confirmar | 2 — G1b e G1c |
>
> **O que esta assinatura NÃO cobre, e quem a ler tem de saber:**
>
> 1. **Não houve kick-off gravado.** O escopo deriva de material técnico e de
>    cinco respostas directas do projectista, não de uma reunião multidisciplinar.
> 2. **A revisão adversarial correu no mesmo modelo que redigiu o escopo.** A
>    skill pede um segundo modelo. Vale como pré-revisão.
> 3. **O contrato do bus de 14 pinos fica fora de âmbito** por decisão expressa.
>    O risco de plataforma está quantificado em `L3` e no resumo dos gaps, e
>    continua aberto depois desta assinatura.
> 4. **`G1c` fechou em 2026-09-23, e mexeu no orçamento de erro.** A calibração
>    é uma **constante comum a todas as placas**, não por unidade. Uma constante
>    comum não segue a dispersão de peça para peça, portanto a tolerância
>    inicial volta à conta, e os erros do próprio `MCP3208` passam a contar. O
>    orçamento refeito está em `planejamento_pcb_EBM2_V5.md` §2.5b, **em duas
>    contas separadas**, porque é assim que os critérios estão escritos: `RE1`
>    mede a 25 °C e `RE2`/`RB3` medem o erro adicional em temperatura.
>    **Actualizado em 2026-09-23 com o datasheet `DS21298E` do conversor:**
>    a deriva fica em **0,165 %** contra 0,2 % e cumpre, mas `RE1` fica em
>    **0,237 %** e **não cumpre**, porque os erros de offset e linearidade do
>    `MCP3208` são tensões fixas e a nossa referência de 2,5 V duplica-lhes o
>    peso relativo. Nenhuma troca de componente o resolve. Com calibração por
>    unidade de dois pontos, `RE1` cai para 0,055 %. **É a decisão que falta
>    tomar.**

---

# Escopo de hardware — IC2S Extension Board EBM2 V5 (6AI)

> **Este documento substitui** o `escopo_EBM2_V5.md` mínimo escrito à posteriori
> em 2026-09-23. Aquele era um registo de lacunas; este é a F0 a sério.

> **Ressalva de insumos.** Não houve reunião de kick-off gravada. O escopo
> deriva de: o projecto V4.1 convertido e auditado, os Gerbers originais, a
> placa irmã EBM7 V2.3 como referência, 68 datasheets, quatro análises
> anteriores, o histórico de avaria em campo da EBM7 V1.1, e **quatro requisitos
> de produto respondidos directamente pelo projectista em 2026-09-23**. Tudo o
> que não vem dessas fontes está marcado como especificação aberta, nunca como
> escolha implícita.

---

## 1 · Contexto e objectivo

A EBM2 é um shield de quadro PLC da família IC2S com **seis entradas analógicas
de 4-20 mA**. Monta sobre uma base board pelo conector `P1` de 20 pinos e liga ao
campo pelo `P2` de 14 pinos. A revisão em campo é a **V4.1, de 2024**.

**Objectivo da V5:** corrigir defeitos identificados na V4.1 — um deles é o
mesmo mecanismo que já queimou fusíveis em campo na placa irmã — portando a
arquitectura de alimentação e de protecção de entrada da EBM7 V2.3, **sem
quebrar a compatibilidade com os quadros instalados**.

Não é um produto novo. É uma revisão de correcção.

## 2 · Requisitos, com critérios de aceite mensuráveis

Estes critérios **congelam na aprovação do Portão 0** e são contra eles que a
F6 valida a placa. Não se reescrevem depois.

### 2.1 · Compatibilidade — decisão do projectista, 2026-09-23

| ID | Requisito | Critério de aceite |
|---|---|---|
| **RC1** | A V5 é **substituição directa** da V4.1 num quadro instalado | Contorno, furação de fixação e posição dos conectores idênticos aos Gerbers da V4.1, medidos com tolerância de 0,1 mm |
| **RC2** | Pinagem de `P1` (20 pinos) e `P2` (14 pinos) **inalterada** | Comparação nó a nó da netlist da V5 contra a da V4.1: zero diferenças nos pinos de `P1` e `P2` |
| **RC3** | A base board não distingue uma V5 de uma V4.1 | Mesma sequência SPI, mesmos níveis, mesma codificação de ID nos pinos `ID1`/`ID2`/`ID3` |
| **RC4** | O firmware existente continua a funcionar | A placa monta num quadro instalado e é lida pelo firmware actual **sem recompilar**. A alteração de escala é absorvida pela rotina de calibração existente, executando a calibração de cada canal após a troca |

> **RC4 — cumpre-se, com uma condição de processo (2026-09-24).** Não é preciso recompilar: a escala
> nova absorve-se recalibrando cada canal pela tela. **Mas nada obriga a recalibrar ao trocar a
> placa**, e a calibração da V4.1 continua aplicada. Se ninguém recalibrar, a V5 lê **−9,3 %** em
> todos os canais (20 mA → 18,15 mA), e **4 mA lê 3,63 mA, colado ao corte de 3,6 mA**: um
> transmissor a 3,9 mA passa a `"null"` (falso laço aberto). O ajuste em lote que o firmware
> propõe (×0,9074 nos pontos) só corrige a escala nominal: arrasta os erros próprios da V4.1
> (±1 % do LDO usado como referência, ±1 % do burden). **Regra: recalibrar os seis canais ao
> instalar a V5.**

### 2.2 · Medida

| ID | Requisito | Critério de aceite |
|---|---|---|
| **RM1** | Seis canais de entrada 4-20 mA, independentes | Injectar 4,000 e 20,000 mA em cada canal e ler os seis sem diafonia acima de 1 LSB |
| **RM2** | Alcance útil igual ao da EBM7 legacy | Fundo de escala **não inferior a 20,5 mA** |
| **RE1** ⚠ | **Exactidão de 0,1 a 0,2 % do fundo de escala, DEPOIS de calibrada** | Com fonte de corrente rastreável, erro máximo em 4, 12 e 20 mA dentro de ±0,2 % a 25 °C. **EM CONFLITO**: a calibração é uma **constante comum** (confirmado 2026-09-23) e com ela o pior caso calculado é **0,237 %**, típico 0,139 %. Nenhum componente o resolve. **Decisão de escopo pendente no Portão 0**: especificar pelo pior caso ou declarar 0,2 % como típico. Ver `planejamento_pcb_EBM2_V5.md` §2.7c |

> **RE1 — conflito resolvido em 2026-09-24 com a resposta do firmware.** O conflito existia porque
> se assumiu «constante comum». O sistema **calibra cada canal no campo em 6 pontos**: offset e
> ganho do ADC, da referência e do burden saem da calibração. Sobra, a 25 °C: INL residual ≤ 0,055 %
> (limite de 1 LSB do grau -B, sem descontar o efeito dos 5 trechos), ruído da amostra única da
> captura ~0,028 % (±1 LSB, estimativa) e a exactidão da fonte de corrente do campo (**por
> conhecer**). RSS sem a fonte: **~0,062 %**, contra o tecto de 0,2 %. **Cumpre, desde que a
> calibração seja feita e a fonte seja ≤ 0,1 %.** O projectista tinha dito «não calibramos unidade
> por unidade»: não há calibração de fábrica, mas há a de campo, por canal.

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
| **RE2** | **A exactidão mantém-se em toda a gama de `RB1`** | Repetir `RE1` a 0 e +70 °C sem recalibrar. Erro adicional ≤ 0,2 %. **É este o critério que decide as peças**: a calibração remove o erro inicial, não a deriva térmica |
| **RM3** | Filtro anti-aliasing por canal | Frequência de corte medida entre 400 e 550 Hz |

### 2.3 · Alimentação e protecção

| ID | Requisito | Critério de aceite |
|---|---|---|
| **RA1** | Entrada única de 24 V vinda da base board. **Envolvente 18–32 V** (corrigido em 2026-09-23): o painel alimenta-se de rede, bateria ou painel solar, com e sem controlador de carga — decisão do projectista de 2026-08-31, «opção B, alimentação genérica», `escopo_EBM7_respin.md` §7, cenários S1-S4. A primeira versão deste escopo tomou a DRC-100B como única fonte e escreveu 20–28 V | Funciona de **18 a 32 V** sem degradação de medida acima de 1 LSB. Dimensionamento: arranque e dissipação a **32 V**, tensão ao transmissor a **18 V** |
| **RA2** | **Os fusíveis não abrem no arranque** | Ligar e desligar a alimentação 100 vezes seguidas sem abrir nenhum fusível. Margem calculada de I²t do arranque contra o I²t de fusão ≥ 10× |
| **RA3** | TVS na entrada de 24 V | **REESCRITO em 2026-09-23, fecha `G5`.** Não existe requisito de imunidade escrito, confirmado pelo projectista. O nível de 1 kV que aqui constava foi inventado pela sessão e retira-se. O critério passa a ser de projecto: existe TVS na entrada, a sua tensão de grampeamento fica abaixo do menor absoluto máximo de todas as peças do trilho, e essa margem está calculada e documentada. Sem nível de ensaio declarado, não há ensaio de surto |
| **RA4** | Todo o caminho de clamp termina num sumidouro real | Injectar 30 V numa entrada de campo e medir `3V3_REF`: não pode subir acima de 3,7 V |
| **RA5** | Consumo total na entrada de 24 V | ≤ 200 mA com os seis canais a 20 mA |

### 2.4 · Ambiente — decisão do projectista, 2026-09-23

| ID | Requisito | Critério de aceite |
|---|---|---|
| **RB1** | Gama de operação **declarada e certificada: 0 a +65 °C**; **dimensionamento a +70 °C** (margem de projecto pedida pelo projectista, 2026-09-24). **Corrigido em 2026-09-24 pelo projectista: 0 a +70 °C.** O −40 a +85 °C anterior foi proposto pela sessão na F0 como «o habitual em quadro de PLC» e escolhido nessa pergunta; não corresponde a nenhum painel instalado. | Todos os critérios de medida cumpridos em câmara a 0, +25 e **+70 °C** (ensaiar no limite de projecto cobre os 65 °C certificados) |
| **RB2** | Todos os componentes especificados para a gama, sem excepção | Auditoria da BOM: zero peças com gama inferior. Electrolíticos com gama e vida declaradas, ou substituídos por cerâmicos |
| **RB3** | Deriva térmica dentro do orçamento de erro | Erro adicional entre 0 e +70 °C ≤ 0,2 % do fundo de escala, **medido em relação à temperatura a que se calibrou** (no campo não é 25 °C) |

### 2.5 · Isolamento — decisão do projectista, 2026-09-23

| ID | Requisito | Critério de aceite |
|---|---|---|
| **RI1** | **Nenhuma certificação formal de isolamento.** A barreira é funcional | Declarado no dossier. **Não se invoca IEC 60664-1 nem se declara tensão de isolamento** |
| **RI2** | Separação funcional entre o barramento digital e o campo | O `ISO7141` é a única barreira. Nenhum condutor a atravessa no esquemático nem no layout |
| **RI3** | União de massas num ponto único | Existe exactamente **um** caminho entre `GND_24V` e `GND_ADC`, e é uma resistência de 0 Ω identificável |

### 2.6 · DFT

| ID | Requisito | Critério de aceite |
|---|---|---|
| **RD1** | Ponto de prova em cada trilho de alimentação | `+24V`, `+24V_ADC`, `+24V_REG`, `+5V`, `3V3_REF`, referência, `GND_24V`, `GND_ADC`, `DGND` — todos acessíveis com ponta de prova |
| **RD2** | Fiduciais para montagem automática | ≥ 3 fiduciais na face com SMD |
| ~~**RD3**~~ | ~~Acesso mecânico aos pontos de prova com a placa montada no quadro~~ | **RETIRADO em 2026-09-23, fecha `G7`.** Não existe desenho do invólucro nem do quadro, confirmado pelo projectista. Um critério que ninguém consegue verificar não se congela. Volta ao escopo no dia em que houver desenho |

## 3 · Componentes críticos já decididos

Só entram aqui os que a equipa já decidiu. Todos vêm da EBM7 V2.3, já montados
e portanto sem qualificação nova.

| Função | Peça | Origem da decisão |
|---|---|---|
| Aislador digital | `ISO7141` | Herdado da V4.1, mantém-se |
| Conversor A/D | **`MCP3208T-BI/SL`** | Herdado da V4.1, que monta o grau `-CI`. **Muda para `-BI` em 2026-09-23**: mesmo encapsulamento, mesma pinagem, mesmo protocolo, INL de ±1 LSB em vez de ±2. `RC4` intacto |
| TVS de entrada | `SMA6J33A-Q` | EBM7 V2.3, `D200` |
| Fusíveis retardados | família Eaton `CC12H` | EBM7 V2.3. **MPN do valor baixo por fixar — ver G4** |
| Díodo de bloqueio | `MBR1H100SF` | EBM7 V2.3 |
| Regulador de entrada alta | `TPS7A4001` | EBM7 V2.3, `U12` |
| LDO de 3,3 V | `SPX3819M5-L-3-3` | Já na V4.1 como `U11` |
| Grampo activo | `TL431B` | EBM7 V2.3, `U4` |
| Clamps de baixa fuga | `BAV199` | EBM7 V2.3 |
| Conectores | `M20-7822046` e `M20-7821446` (Harwin) | Herdados da V4.1, congelados por RC2 |

## 4 · Especificações abertas — decidem-se na F1

1. **Referência de tensão do ADC. FECHADA em 2026-09-23 — e a premissa mudou.**
   O `G1c` fechou com «constante comum a todas», o que inverte o raciocínio
   anterior: uma constante comum não acompanha a dispersão de peça para peça,
   logo **a tolerância inicial NÃO é removida pela calibração**. O texto que
   aqui estava, dando-a por removida, estava errado. Especificação corrigida:
   coeficiente **≤ 5 ppm/°C** *e* tolerância inicial **≤ 0,1 %**. Peça escolhida
   **`ADR4525BRZ`**, que cumpre as duas com folga larga: 0,02 % inicial e
   **4 ppm/°C pelo método bowtie** — o datasheet dá também 2 ppm/°C pelo método
   box, mas o bowtie é o que responde ao afastamento a partir do ponto de
   calibração e é esse que entra na conta.
2. **Valor e tecnologia do burden. FECHADA em 2026-09-23.** O **valor** continua
   livre, porque a constante comum absorve o nominal. A **dispersão** não:
   tolerância inicial e deriva entram as duas na conta e juntas fazem do burden
   o termo dominante do orçamento. Alvo **≤ 25 ppm/°C** e tolerância **≤ 0,1 %**.
   Valor fixado em **110 Ω**, que coloca o fundo de escala em 22,7 mA e cumpre
   `RM2` com folga. Peça **`ERA3AEB111V`**. **Se o orçamento de `RE1` não
   fechar, o problema não tem solução dentro desta família.** A tabela de
   *Ratings* do datasheet Panasonic `AOA0000C307`, pág. 2, mostra que em 0603 o
   grau de ±10 ppm/°C só desce a 1 kΩ e o de ±15 ppm a 470 Ω. **A 110 Ω,
   `ERA3AEB` é o melhor que existe**, e apertar mais obriga a mudar de
   fabricante. O part number correcto é `ERA3AEB111V`: 110 Ω é valor E24 e a
   nota `*5` do datasheet impõe a codificação de três dígitos.
3. **MPN e valor exacto dos passivos** do bloco de alimentação.
4. ~~**Número de camadas e empilhamento.**~~ **FECHADA em 2026-09-23**: quatro
   camadas, igual à V4.1. Confirmado pelo projectista e coerente com a medição
   feita nos Gerbers originais.
5. **Estratégia de retorno de massa** com os seis laços a partilharem
   `GND_ADC`. Decide-se com o layout, mas a restrição fixa-se na F1: a
   resistência entre as massas dos burden e o `AGND` do ADC tem de ser
   **< 5 mΩ** para que a queda IR fique abaixo de 1 LSB com 120 mA.

## 5 · Restrições

**Mecânicas.** Contorno, furação e posição de conectores congelados pela V4.1
(RC1). Os Gerbers originais são a referência dimensional.

**Ambientais.** 0 a +65 °C certificado, dimensionado a +70 °C (RB1, corrigido em 2026-09-24). Sem requisito de IP declarado para a placa:
a protecção é do quadro. Vibração não declarada.

**Regulatórias.** **Nenhuma.** Sem rádio, logo sem Anatel. Sem área
classificada, logo sem ATEX. Sem certificação de isolamento (RI1).

**Custo.** Não declarado. Registado como lacuna menor: todas as peças que entram
já estão em BOM de outra placa da casa.

## 6 · Orçamento de energia

~~Não aplicável: a placa é alimentada pelo quadro, não por bateria.~~ **Corrigido em
2026-09-23:** o quadro pode estar em bateria ou painel solar (`RA1`, 18–32 V). A placa não
gere a bateria, mas o consumo pesa na autonomia do painel; está coberto por RA5.

| Consumidor | Corrente a 24 V |
|---|---|
| Seis laços a 20 mA | 120 mA |
| Três LED indicadores | 4,5 mA |
| Electrónica (ADC, isolador, referência, NTC) | ~5 mA |
| **Total** | **~130 mA** |

## 7 · Interfaces externas

| Interface | Descrição | Estado |
|---|---|---|
| `P1`, 20 pinos | Barramento à base board: SPI, IDs, I2C, +5 V, 24 V e retornos | **Congelado** por RC2 |
| `P2`, 14 pinos | Campo: seis pares de alimentação e retorno de laço, mais `GND_ADC` | **Congelado** por RC2 |

**Aviso de plataforma.** O mesmo conector físico de 14 pinos tem **três
definições mutuamente incompatíveis** entre a MainBoard V5.1, a EBM2 e a EBM7
(fonte: `EBM2_vs_EBM7_Comparacion.md`, 2026-08-11). Escrever o contrato do bus
ficou **fora do âmbito** desta revisão por decisão do projectista em
2026-09-23. Regista-se como **risco de plataforma aberto**: cada modelo novo de
extensão vai continuar a chocar de maneira diferente.

## 8 · Fora de escopo, explicitamente

- Escrever ou auditar o contrato do bus de 14 pinos (decisão de 2026-09-23).
- Alterar o conversor A/D, o aislador ou os conectores.
- Alterar a pinagem de `P1` ou `P2`.
- Certificação de isolamento de qualquer tipo.
- Firmware. Esta placa não traz MCU; o firmware vive na base board.
- Invólucro novo.

## 9 · Defeitos da V4.1 que esta revisão corrige

Medidos nesta sessão, com a conta à vista. São a justificação da revisão.

| # | Defeito | Medida |
|---|---|---|
| D1 | **Mecanismo de avaria de fusíveis presente** | `F7`/`F9` são `3413.0008.22`, I²t de fusão **0,0015 A²s** (datasheet Schurter, confirmado na F1). Arranque dos 10 µF a 24 V = 0,00565 A²s com R=0,51 Ω, ou 0,00169 A²s com R=1,7 Ω. **Acima nos dois casos, em três ramas.** As unidades foram corrigidas de mA²s para A²s em 2026-09-23; os rácios e a conclusão não mudam |
| D2 | **Sem sumidouro em `3V3_REF`** | Seis clamps injectam ~4,5 mA cada num rail com um LDO que não absorve e 2,3 µF |
| D3 | **Zener de 2,45 V classe µA em série na entrada** | A conduzir os ~130 mA de toda a placa |
| D4 | **Sem TVS na entrada de 24 V** | A rede `+24V` tem só o zener e três fusíveis |
| D5 | **Díodo de bloqueio de 60 V** | Contra um clamp de TVS de 58,1 V: 1,9 V de margem |
| D6 | **Bulk de 50 V** | 8,1 V abaixo do clamp de 58,1 V |
| D7 | **Referência do ADC = saída do LDO** | ±1 % de tolerância vira erro de ganho directo |
| D8 | **Satura a 20,4 mA** | Não lê o alarme alto de 21 mA da NAMUR NE43 |
| D9 | **Zero pontos de prova e zero fiduciais** | |
| D10 | **`R34` com pinos trocados** entre esquemático e placa | No projecto original; inócuo mas prova dessincronização |

```yaml
evidencia:
  skill: 2shw-pcb:escopo
  artefatos: [escopo_EBM2_V5.md, escopo_EBM2_V5_gaps.md, plano_teste_EBM2_V5_esqueleto.md]
  criterios_aceite_definidos: 22   # 23 na assinatura; RD3 retirado em 2026-09-23
  gaps_bloqueantes: 1
  gaps_resolvidos: 1
  kick_off_gravado: nao
  requisitos_respondidos_pelo_projectista: 5
  avanco_escopo_pct: 85
  blocos_biblioteca_usados: []
```
