---
documento: Esqueleto do plano de teste
projecto: IC2S Extension Board EBM2 V5 (6AI)
fase: F0, etapa 3
data: 2026-09-23
dono: **Testes e Qualidade**
origem: derivado de escopo_EBM2_V5.md
---

# Esqueleto do plano de teste — EBM2 V5

> **A partir daqui este documento pertence a Testes e Qualidade.** A F0 entrega
> o esqueleto: um item por critério de aceite, com método sugerido de bancada.
> Quem o completa, valida e assina é a T&Q.

> **Aviso, actualizado em 2026-09-23 no fim da F1.** Os dois gaps bloqueantes
> `G1` e `G2` fecharam, e com eles `T4` e `T7` deixaram de estar travados.
> Em contrapartida **`T11` e `T22` ficaram sem objecto**: os critérios que
> verificavam foram reescrito e retirado do escopo. E `T7` ganhou uma condição
> nova que não tinha: ver a nota abaixo da tabela da secção 2.

---

## 1 · Compatibilidade

| # | Critério | Método sugerido | Equipamento |
|---|---|---|---|
| T1 | `RC1` contorno e furação idênticos | Sobrepor os Gerbers da V5 aos da V4.1 e medir o desvio máximo | Comparação de Gerber por script; paquímetro na placa física |
| T2 | `RC2` pinagem de `P1` e `P2` inalterada | Comparação nó a nó das duas netlists | Script; **já disponível** e usado nesta sessão |
| T3 | `RC3` a base board não distingue as duas | Montar V4.1 e V5 no mesmo quadro e comparar leituras da base board | Quadro de ensaio com base board |
| T4 | `RC4` firmware existente funciona | **DESTRAVADO.** Montar a V5 num quadro com firmware actual, correr a calibração de fábrica e comparar leituras contra padrão em 4, 12 e 20 mA | Quadro de ensaio, fonte de corrente calibrada |
| **T4b** | `RC4` troca de placa (2026-09-24) | (a) Instalar a V5 num quadro com a calibração da V4.1 ainda activa e registar o erro (esperado ≈ −9,3 %) e os `"null"` perto de 4 mA; (b) recalibrar os seis canais pela tela (6 pontos) e repetir T7. Confirma a regra «recalibrar ao instalar» | Quadro de ensaio, fonte de corrente rastreável |

## 2 · Medida

| # | Critério | Método sugerido | Equipamento |
|---|---|---|---|
| T5 | `RM1` seis canais independentes | Injectar 4,000 e 20,000 mA num canal de cada vez e ler os seis. Diafonia < 1 LSB | Fonte de corrente calibrada, 4 dígitos e meio |
| T6 | `RM2` fundo de escala ≥ 20,5 mA | Rampa de corrente até saturação e registar o ponto onde a leitura deixa de subir | Fonte de corrente programável |
| T7 | `RE1` exactidão de 0,1 a 0,2 % | Três pontos (4, 12, 20 mA) em cada canal, contra padrão rastreável, **com a constante de calibração comum de fábrica, nunca uma por unidade** | Fonte de corrente rastreável |
| | *Nota 2026-09-24* | A calibração real é por canal, em campo, em 6 pontos (resposta do firmware). **T7 faz-se depois dessa calibração**, com uma fonte diferente da usada para calibrar, em pontos intermédios (6, 10, 14, 18 mA) além de 4, 12 e 20. Registar a exactidão da fonte | |
| T8 | `RM3` corte entre 400 e 550 Hz | Injectar corrente com componente alterna e varrer a frequência; achar o ponto de −3 dB | Gerador de corrente alterna sobre a média |

## 3 · Alimentação e protecção

| # | Critério | Método sugerido | Equipamento |
|---|---|---|---|
| T9 | `RA1` funciona de **18 a 32 V** (corrigido em 2026-09-23) | Varrer a alimentação e verificar que a medida não desvia mais de 1 LSB | Fonte de bancada |
| T10 | `RA2` **os fusíveis não abrem no arranque** | **100 ciclos de ligar e desligar** com os seis canais carregados. Nenhum fusível abre. Margens de I²t **a 32 V** (rev. 2.2) contra a tabela Eaton: **23,4×** na rama dos laços e **12,3×** na do regulador, com `R3` de **33 Ω**. **Com os 22 Ω anteriores eram 8,6× a 32 V e o critério reprovava; sem `R3`, 1,2×.** Fazer os 100 ciclos a 32 V | Comutador temporizado; osciloscópio na corrente de entrada com pinça |
| ~~T11~~ | ~~`RA3` surto na entrada~~ | **SEM OBJECTO a partir de 2026-09-23.** Não há requisito de imunidade escrito, e o nível de 1 kV que o escopo citava tinha sido inventado. `RA3` passou a critério de projecto e verifica-se na revisão documental, não em bancada | — |
| T12 | `RA4` clamp com sumidouro real | Injectar 30 V numa entrada de campo com a placa alimentada e medir `3V3_REF` com osciloscópio | Fonte de bancada, osciloscópio, ponta no ponto de prova de `3V3_REF` |
| T13 | `RA5` consumo ≤ 200 mA | Medir a corrente em `P1.20` com os seis canais a 20 mA | Multímetro em série, ou shunt no ponto de prova de `+24V` |
| **T26** | `V8` transmissor em curto (rev. 2.1) | Curto franco entre `LOOPk_V+` e `AINk-`, alimentação a **32 V**, câmara a **+70 °C**, **1 h** por canal e depois os seis ao mesmo tempo. Corrente entre 23,75 e 26,8 mA; limitador a ~25,5 V e ~0,68 W; nenhuma resistência acima da nominal (termografia); se o `U8-U13` entrar em corte térmico, registar o ciclo e recuperar sem dano. Repetir a −40 °C | Câmara, fonte de bancada, câmara térmica, multímetro em série |
| **T27** | Limitador não interfere com a medida nem oscila (rev. 2.1) | (a) T7 com e sem o `U8-U13` em ponte: diferença < 1 LSB. (b) Transmissor real forçado a alarme alto (≥ 22,5 mA) e a 3,6 mA: osciloscópio no nó `AINk_LIM`, sem oscilação. (c) Tensão em `U8-U13` a 20 mA a −40, +25 e +85 °C (a fig. 15 do datasheet só dá 25 °C) | Fonte de corrente, transmissor 2 fios, osciloscópio, câmara |

**T10 e T12 são os dois ensaios que fecham os defeitos que motivaram a
revisão.** Se algum deles falhar, a revisão não cumpriu o seu objectivo.

## 4 · Ambiente

| # | Critério | Método sugerido | Equipamento |
|---|---|---|---|
| T14 | `RB1` medida correcta a 0, +25 e +70 °C | Repetir T5, T6 e T7 dentro da câmara, com estabilização de 30 min por patamar | Câmara climática |
| T15 | `RB2` BOM sem peças fora de gama | Auditoria documental da BOM contra os datasheets | Revisão de documentos, não bancada |
| T16 | `RB3` deriva ≤ 0,2 % entre 0 e +70 °C (calibrar a 0 °C e medir a +70 °C, o pior caso) | Diferença entre os extremos de T14 | Câmara climática |

## 5 · Isolamento

| # | Critério | Método sugerido | Equipamento |
|---|---|---|---|
| T17 | `RI1` nada se declara | Verificação documental: o dossier **não** invoca IEC 60664-1 nem declara tensão de isolamento | Revisão de documentos |
| T18 | `RI2` nenhum condutor atravessa a barreira | Medição segmento a segmento da distância mínima entre os dois domínios, em todas as camadas, incluindo ilhas e vias | Script sobre o `.kicad_pcb`; **já existe**, usado nesta sessão na EBM7 |
| T19 | `RI3` união de massas num ponto único | Continuidade entre `GND_24V` e `GND_ADC` com o 0 Ω montado e com ele removido | Multímetro; e o mesmo script de T18 |

**T18 não é opcional.** Na placa irmã este ensaio destapou uma barreira de
0,3005 mm onde o relatório anunciava 1,2 mm, porque a medição original só tinha
olhado para o cobre roteado e não para o enchimento das zonas.

## 6 · DFT

| # | Critério | Método sugerido |
|---|---|---|
| T20 | `RD1` ponto de prova em cada trilho | Contagem e acesso com ponta de prova em cada um dos nove |
| T21 | `RD2` ≥ 3 fiduciais | Inspecção visual da face SMD |
| ~~T22~~ | ~~`RD3` acesso mecânico no quadro~~ | **SEM OBJECTO a partir de 2026-09-23**: `RD3` saiu do escopo por não haver desenho do quadro |

---

## Requisitos de DFT que a placa TEM de incorporar

Isto não é ensaio: é o que o esquemático tem de desenhar para que os ensaios
acima sejam possíveis. Vai para a F2 como requisito, não como sugestão.

1. **Ponto de prova em cada trilho de alimentação**, nove ao todo: `+24V`,
   `+24V_ADC`, `+24V_REG`, `+5V`, `3V3_REF`, a referência do ADC, `GND_24V`,
   `GND_ADC` e `DGND`.
2. **Ponto de prova do lado seguro da barreira.** O ponto de `DGND` fica no lado
   do barramento. Sonda no lado de campo com a placa ligada atravessa a
   separação pela massa do osciloscópio.
3. **Provisão para medir a corrente de entrada** sem cortar pista: o ponto de
   prova de `+24V` mais o retorno permitem pinça, ou prevê-se um shunt.
4. **Consolidar pontos no mesmo nó eléctrico.** Dois pads na mesma rede não
   medem nada diferente e custam área.
5. **≥ 3 fiduciais** na face com SMD.
6. ~~**Acesso mecânico** aos pontos com a placa montada~~ — **retirado** com o `RD3`.

## Cobertura

| | |
|---|---|
| Critérios de aceite no escopo, depois da F1 | 22 |
| Itens de teste derivados | 22 |
| Itens sem objecto, critério retirado ou reescrito | 2 — `T11` e `T22` |
| Itens destravados na F1 | 2 — `T4` e `T7` |
| Itens novos, abertos pelo datasheet do conversor | 3 — `T23`, `T24`, `T25` |
| **Itens prontos a escrever** | **23** |
| Itens que o cálculo já reprova | 1 — `T7`, se a calibração ficar comum |

**O Portão 0 foi assinado em 2026-09-23** e os critérios congelaram nesse
momento. É contra eles que a F6 valida, e a T&Q pode começar a escrever.

**Duas ressalvas que a T&Q tem de conhecer antes de começar:**

1. **`T10` e `T12` continuam a ser os dois ensaios que justificam esta revisão.**
   Se algum falhar, a V5 não corrigiu o que se propôs corrigir.
2. **`T7` reprova por cálculo no pior caso.** A calibração é uma **constante
   comum** (confirmado pelo projectista em 2026-09-23) e com ela o pior caso de
   `RE1` é **0,237 %** contra 0,2 %; o típico é 0,139 %. Enquanto o escopo não
   decidir se `RE1` é pior caso ou típico, **o critério de aprovação de `T7` não
   está definido**, e a T&Q não o deve escrever.
3. Uma nota para quando `T7` se escrever: a medição em 4, 12 e 20 mA contra
   padrão rastreável é a mesma que serviria para calibrar por unidade. A decisão
   de não o fazer é do produto; o custo de ensaio seria zero.
4. **`T14` e `T16` cumprem, mas com 83 % do orçamento gasto**, e quase tudo no
   burden. Se reprovarem não há troca fácil: a 110 Ω o grau de ±25 ppm/°C é o
   melhor que a família Panasonic ERA oferece, porque os graus finos só começam
   em 470 Ω e 1 kΩ. Apertar exige mudar de fabricante.
5. **Três ensaios novos que o datasheet do conversor obriga a acrescentar**, e
   que a T&Q tem de escrever:
   - **`T23`** — o canal 4 (termístor) lê correctamente a **+70 °C**. Com o
     divisor herdado da V4.1 saturaria a 70 °C. Corre dentro da câmara, junto
     com `T14`.
   - **`T24`** — mapa de canais. Injectar uma corrente distinta em cada um dos
     seis canais de campo e confirmar que o firmware os lê em `CH0`, `CH1`,
     `CH2`, `CH3`, `CH6` e `CH7`. **Uma troca aqui não dá erro nenhum**, só dois
     valores errados.
   - **`T25`** — integridade da transacção SPI. Com a placa a +70 °C, confirmar
     que a leitura não degrada sob carga do sistema operativo do mestre. O
     conversor só garante a carga do condensador de amostra durante 1,2 ms
     depois do fim da amostragem, e uma transacção partida pelo escalonador dá
     erro de linearidade sem qualquer indicação.
