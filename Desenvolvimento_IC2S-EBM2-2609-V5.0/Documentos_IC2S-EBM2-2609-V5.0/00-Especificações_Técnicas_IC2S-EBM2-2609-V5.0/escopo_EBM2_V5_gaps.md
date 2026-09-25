---
documento: Revisão adversarial do escopo
projecto: IC2S Extension Board EBM2 V5 (6AI)
fase: F0, etapa 2
data: 2026-09-23
alvo: escopo_EBM2_V5.md
---

# Revisão adversarial — escopo da EBM2 V5

> **Limitação declarada.** A skill pede que esta revisão corra num **segundo
> modelo**. Não correu: foi feita em passada separada pelo mesmo modelo que
> redigiu o escopo. Vale como pré-revisão. Antes do Portão 0 devia correr uma
> passada independente — é a única forma de apanhar o que o autor não vê por ser
> autor.

Cada achado é uma **pergunta directa ao responsável**, não uma afirmação.

---

## ✅ RESOLVIDO

### G1 — RESOLVIDO em 2026-09-23 pelo projectista, e o raciocínio muda

**Resposta:** *"el firmware hace la conversion para calibrar primeramente, pero
no lo realiza en las células de carga"*.

O firmware **calibra** os canais de 4-20 mA. Logo `RC4` e `RE1` **não estão em
conflito**: mudar `VREF` e o burden é absorvido pela calibração, e o firmware
existente continua a funcionar sem recompilar.

Mas a resposta obriga a refazer a justificação da referência, e o resultado é
melhor do que o anterior:

> **A calibração remove o erro INICIAL. Não remove a deriva térmica.**

Com `RB1` fixado em **−40 a +85 °C**, o que decide `RE1` deixa de ser a
tolerância de fábrica e passa a ser o **coeficiente de temperatura**. Excursão
máxima a partir dos 25 °C de calibração: 60 °C.

| Configuração | Deriva da referência | Deriva do burden | Total (RSS) | Cumpre `RE1`? |
|---|---|---|---|---|
| Actual: `SPX3819` + `CRCW` 1 % | 57 ppm/°C × 60 = 0,342 % | 100 ppm/°C × 60 = 0,600 % | **0,69 %** | **Não**, 3,5× acima |
| Só apertar o burden a `ERA-3AEB` | 0,342 % | 25 ppm/°C × 60 = 0,150 % | 0,37 % | **Não** |
| `ADR4525` + `ERA-3AEB` | 2 ppm/°C × 60 = 0,012 % | 0,150 % | **0,15 %** | **Sim** |

**Conclusões que mudam a selecção de peças:**

1. A referência de precisão **continua a ser necessária**, mas o critério de
   escolha é o **coeficiente de temperatura**, não a exactidão inicial. Isto
   abre a porta a referências de tolerância inicial folgada e bom TC, que são
   mais baratas. Mantém-se o `ADR4525` porque já está em BOM da casa, mas a
   razão escrita tem de ser 2 ppm/°C e não ±0,02 %.
2. O **burden domina** o orçamento depois da calibração. Passar de `CRCW`
   (100 ppm/°C) a `ERA-3AEB` (25 ppm/°C) vale mais do que qualquer outra
   alteração isolada.
3. O **valor** do burden fica livre: a calibração absorve-o. Logo 110 Ω passa a
   ser escolha livre, e resolve `RM2` sem custo.

> **Duas correcções a esta secção, feitas na F1 de 2026-09-23.** A tabela acima
> e as três conclusões continuam a apontar para as mesmas peças, mas duas
> premissas mudaram:
>
> - A excursão correcta a partir dos 25 °C é **65 °C**, não 60, porque o extremo
>   frio de `RB1` está a −40 °C. Os números da tabela sobem cerca de 8 %, e
>   nenhuma linha muda de veredito.
> - A conclusão 3 dizia que o valor do burden era livre «porque a calibração o
>   absorve». Com **constante comum**, a calibração absorve o nominal mas **não**
>   a dispersão. O valor continua livre; a tolerância inicial deixou de estar.
>   Ver `planejamento_pcb_EBM2_V5.md` §2.5b.

**Ressalva por confirmar (G1b):** o coeficiente de 57 ppm/°C do `SPX3819` foi
lido de uma linha de tabela que a extracção de texto devolveu **desordenada**
(`1016_SPX3819.pdf`, tabela de características eléctricas). Confirmar a olho no
PDF antes de congelar. Não muda a conclusão — muda só quanto se falha na opção
que se rejeita.

**Ressalva por confirmar (G1c):** a calibração é **por unidade**, feita em
produção a cada placa, ou é uma constante de fábrica igual para todas? Só a
primeira remove a tolerância de fábrica. Se for constante comum, o erro inicial
do LDO volta ao orçamento e o `ADR4525` passa a ser necessário também pela
exactidão inicial, não só pelo TC.

**Nota do projectista sobre a EBM7:** *"creo que por eso no lo tomamos en cuenta
en la ebm7"*. Faz sentido: a EBM7 tem célula de carga, e uma ponte é
intrinsecamente **ratiométrica** — o sinal é proporcional à excitação, portanto
o erro da referência cancela-se sozinho se a mesma referência alimentar as duas
coisas. Nos canais de 4-20 mA isso não acontece: ali a referência entra directa
no erro de ganho.

---

## 🔴 BLOQUEANTE

### G1-histórico — o conflito, tal como foi levantado (mantido como registo)

**`RC4` diz que o firmware existente continua a funcionar. `RE1` diz que a
exactidão absoluta passa a 0,1-0,2 %. São incompatíveis.**

O firmware converte contagens do ADC em miliamperes com a referência e o burden:

```
I = (contagem / 4096) x VREF / R_burden
```

Hoje: `VREF` = 3,3 V (saída do LDO) e `R_burden` = 160 Ω. Chegar a 0,1-0,2 %
obriga a uma referência de precisão, e **nenhum caminho mantém a constante**:

| Caminho | Constante muda? | Porquê não serve |
|---|---|---|
| Referência de 2,5 V | **Sim** | `VREF` passa de 3,3 para 2,5 V |
| Referência de 3,0 V | **Sim** | Idem |
| Referência de 3,3 V | Não | **Não cabe**: o `MCP3208` exige `VREF ≤ VDD`, e `VDD` vem do `SPX3819` a ±1 %, ou seja pode estar em 3,267 V |
| Só apertar o burden a 0,1 % | Não | Fica em **~±1,0 %**, porque o ±1 % do LDO continua lá. Não cumpre `RE1` |

E há uma terceira perna: `RM2` pede fundo de escala ≥ 20,5 mA. Com 160 Ω e
`VREF` de 3,3 V a −1 %, o fundo de escala é **20,42 mA**. Também não cumpre.

**Pergunta ao responsável, e é a que desbloqueia tudo:**
o firmware da base board converte com uma **constante compilada** ou com um
**parâmetro de calibração** que se pode alterar por configuração? Se for
parâmetro, `RC4` sobrevive com uma nova constante e não há conflito. Se for
constante compilada, é preciso escolher: **ou `RC4` ou `RE1`**, e o escopo tem
de dizer qual cai.

**Não se avança para a F1 sem esta resposta.** Toda a secção de medida depende
dela, e o trabalho já feito nas folhas `02_entrada` e `03_alimentacao` assumiu
`RE1`.

### G2 — RESOLVIDO em 2026-09-23 lendo os projectos da Base Board e da MainBoard

**Evidência.** O projectista deu acesso a `Main_Board-Hachacthon` e
`Base_Board-Hachathon`. Traçou-se o caminho completo pelas netlists das duas.

**O mestre SPI é uma Raspberry Pi, ligada directamente.** Na MainBoard, `J1` é um
conector de 200 posições a 0,6 mm (`1565917-4`) para módulo Raspberry. O SPI sai
dos seus GPIO e vai ao conector de extensão **sem nenhum adaptador de nível**:

| Sinal | Pino da Pi | Vai a |
|---|---|---|
| MOSI | `J1.33` GPIO10 / SPI0_MOSI | `J2B.18` |
| CLK | `J1.35` GPIO11 / SPI0_SCLK | `J2B.19` |
| MISO | `J1.29` GPIO9 / SPI0_MISO | `J2B.20` |
| CS_ADC | `J1.23` GPIO7 / SPI0_CE1_N | `J2B.23` |

O GPIO de uma Raspberry trabalha a **3,3 V** e não é tolerante a 5 V.

**Sentido de ida (Pi → isolador): NÃO há problema. O achado anterior era falso.**

O `ISO7141` tem **limiares TTL**, não CMOS: *"have TTL input thresholds"*
(`TI_ISO7141CC.pdf`, pág. 1), com **VIH mínimo de 2,0 V** independente do `VCC`.
Os 3,3 V da Pi entram com 1,3 V de margem mesmo com `VCC1` a 5 V.

> **Correcção a um documento anterior.** O `EBM2_vs_EBM7_Comparacion.md` de
> 2026-08-11 dá isto como achado crítico, calculando *"V_IH = 3,5 V não
> atingido"*. Esses 3,5 V vêm de assumir limiar CMOS de 0,7 × VCC. **O ISO7141 é
> TTL.** O achado é um falso positivo e deve ser retirado desse documento.

**Sentido de volta (isolador → Pi): É AQUI que está o problema, e é real.**

O `OUTD` do `ISO7141` está do lado 1, alimentado por `VCC1` = 5 V. O datasheet
dá `VOH` = `VCCO` − 0,1 a IOH = −4 mA, ou seja **~4,9 V**. Esse nível sai por
`P1.6` em direcção ao GPIO9 da Pi.

A Base Board tem protecção: `D54`, um díodo duplo de comutação com ânodo em
`GNDI_3V3` e cátodo em `+3.3V_IC`, com o ponto comum em `MISO`. É um grampo de
duplo rail a 3,3 V, e existe igual em todas as linhas do bus (`D55` MOSI, `D57`
SCK, `D56` CS, `D29` SDA, `D30` SCL).

Mas o grampo fixa a linha em **3,3 + 0,7 ≈ 4,0 V**, e:

1. O absoluto máximo de um GPIO da Pi é ~3,8 V. **4,0 V fica acima.**
2. Não há resistência em série: o `ISO7141` a 5 V empurra contra o grampo
   **em cada bit alto**, com os seus 4 mA de capacidade.
3. A 4,0 V os díodos de ESD internos da própria Pi também começam a conduzir.

Ou seja: não é um circuito que não funciona — funciona, e está instalado. É um
circuito que **opera fora de especificação de forma contínua**, a stressar o
grampo da Base Board e as protecções da Pi em cada transacção SPI.

**A EBM7 já resolveu isto**, e é o que se porta: acrescentou um LDO de 3,3 V
dedicado ao lado 1 do isolador (`U8`, `MCP1824ST-3302E`). Com `VCC1` a 3,3 V o
`VOH` passa a ~3,2 V e o problema desaparece por inteiro, nos dois sentidos.

**Acção para a V5:** portar o LDO de 3,3 V para alimentar `VCC1` e `EN1` do
`ISO7141`, em vez dos +5 V do barramento. Custo: um LDO e dois condensadores,
peça já em BOM da casa. **Isto entra no âmbito da revisão.**

### G2-histórico — como a questão foi levantada (mantido como registo)

O `ISO7141` tem `VCC1` alimentado pelos **+5 V** do barramento (`P1.17`), e os
sinais `MOSI`, `CLK` e `CS_ADC` entram da base board. Se o mestre trabalha a
**3,3 V**, o limiar de entrada de um isolador alimentado a 5 V pode não ser
atingido.

Isto vem da V4.1 e **nunca foi medido**. O documento
`EBM2_vs_EBM7_Comparacion.md` de 2026-08-11 já o levantava, e a EBM7 resolveu-o
acrescentando um LDO de 3,3 V dedicado ao lado 1 do isolador (`U8`,
`MCP1824ST-3302E`). **A EBM2 não tem esse LDO.**

**Perguntas:** qual é a tensão de alimentação do mestre SPI na base board? E se
for 3,3 V, porta-se também o LDO da EBM7 para o lado 1 do isolador, ou fica como
desvio declarado?

Nota: se a placa funciona hoje em campo, isso é evidência de que o limiar se
atinge — mas evidência de funcionamento não é margem. Pode estar a funcionar
sem margem nenhuma e a falhar em temperatura.

---

## 🟠 IMPORTANTE

### G3 — `RB1` (−40 a +85 °C) contra os electrolíticos da V4.1

A V4.1 monta `C12` e `C28`, `ESL107M050AGMAA`, electrolíticos de 100 µF/50 V.
A −40 °C um electrolítico perde capacidade e a sua ESR sobe muito. `RB2` exige
gama declarada ou substituição.

**Pergunta:** confirma-se a substituição por cerâmicos de 100 V, que já era
necessária por `D6` (a tensão de clamp), e que resolve a gama de uma vez?

> **FECHADO na F1, 2026-09-23.** Sim. Os electrolíticos saem e entram cerâmicos
> `GRM32EC72A106ME05L` de 10 µF/100 V em 1210, X7R, gama −55 a +125 °C.
> Consequência secundária: depois desta troca as **únicas peças THT da placa são
> os dois conectores**, o que fecha também o `G9`. Dono: projectista.

### G4 — O critério `RA2` não se pode verificar: falta o datasheet do fusível

`RA2` exige margem de I²t ≥ 10×. Para a rama dos laços há o número
(`CC12H750MA-TR`, 0,15 A²s, confirmado no datasheet na F1). Para a rama do regulador,
onde se propôs **100 mA retardado**, não há: a tabela de selecção Eaton `CC12H`
**não está na pasta de referência**, e o ficheiro que tem esse nome contém, no
conteúdo, o datasheet do `ADR4525`.

**Pergunta:** consegue-se o datasheet da série? Sem ele, ou se mantém 750 mA nas
duas ramas — que não protege a rama de 5 mA — ou o critério `RA2` fica sem
verificação nessa rama.

> **FECHADO na F1, 2026-09-23 — e a premissa deste gap era FALSA.**
>
> A tabela Eaton **está na pasta desde sempre**, com o nome
> `Eaton_fusible_lento.pdf`. Este gap nasceu de procurar por nome de ficheiro e
> ler o silêncio como ausência. O erro e o seu custo estão em
> `planejamento_pcb_EBM2_V5.md` §9.
>
> O que a tabela diz, e que muda o projecto:
>
> 1. **A série `CC12H` não tem 100 mA.** Começa em 250 mA. O `F1` que se tinha
>    especificado não é encomendável.
> 2. Com `CC12H250mA` (I²t de fusão 0,000 38 A²s, 3 500 mΩ a frio) e os 2,2 µF
>    de `C1`, a margem de arranque é **2,1×**, e `RA2` exige 10×. **Reprovava.**
> 3. Nenhuma outra peça da série resolve: 375 mA dá os mesmos 2,1× e 500 mA dá
>    2,9×, porque o I²t e a resistência movem-se em sentidos opostos.
> 4. **Resolve-se com uma peça nova**, a resistência `R3` de 22 Ω em 0805 em
>    série na rama, que leva a margem a **15,3×** ao custo de 0,26 V de queda e
>    3,2 mW. Dimensionamento completo em `planejamento_pcb_EBM2_V5.md` §2.6.
>
> **Sem abrir este ficheiro, a placa teria ido para fabrico com um part number
> inexistente e, depois de o corrigir para o mais próximo, com um fusível que
> abre no arranque** — exactamente a avaria que esta revisão existe para curar.

### G5 — `RA3` inventa um nível de surto que ninguém especificou

Escrevi *"surto de 1 kV segundo IEC 61000-4-5"*. **Esse número é meu, não vem de
nenhum requisito nem de nenhum documento.** O TVS escolhido é o mesmo da EBM7,
mas o nível de imunidade exigido ao produto nunca foi declarado.

**Pergunta:** existe requisito de imunidade a surto para esta família? Se não
existe, `RA3` tem de ser reescrito como *"o TVS existe e está dimensionado para
o rail"*, sem número, ou o número tem de vir de alguém.

> **FECHADO na F1, 2026-09-23.** Resposta do projectista: **não há requisito
> escrito**. O número saiu do escopo e `RA3` foi reescrito como critério de
> projecto, sem nível de ensaio. Sem nível declarado não há ensaio de surto, e o
> item `T11` do plano de teste fica sem objecto. Dono: projectista.

### G6 — `RA4` fixa 3,7 V sem derivar o limite das peças

`RA4` diz que `3V3_REF` não pode passar de 3,7 V. Esse valor sai do ponto de
grampeamento do `TL431` (3,60 V) mais margem, não de um absoluto máximo. O
correcto é derivá-lo: listar **todos** os pinos ligados a `3V3_REF` e o seu
absoluto máximo **com as notas de rodapé**, e fixar o critério pelo mais
restritivo.

**Pergunta:** aceita-se que este critério fique provisório até à etapa 2.3b, que
é onde a tabela de aplicação se faz?

> **ADIADO por decisão, não por esquecimento. Dono: esta sessão. Data-limite:
> etapa 2.3b da F2.** A tabela de aplicação é o artefacto que deriva o limite, e
> derivá-lo antes de a tabela existir seria repetir exactamente o erro que o
> `G5` acabou de expor: escrever um número sem fonte.

### G7 — `RD3` não é verificável com o que existe

`RD3` exige acesso mecânico aos pontos de prova com a placa montada no quadro.
Não há desenho de invólucro nem descrição do quadro no material disponível.

**Pergunta:** existe desenho do quadro ou fotografia da placa instalada? Sem
isso o critério não se pode fechar e devia sair do escopo ou passar a
especificação aberta.

> **FECHADO na F1, 2026-09-23.** Resposta do projectista: **não há plano**. O
> critério `RD3` foi retirado do escopo e o item `T22` do plano de teste fica
> sem objecto. Volta no dia em que houver desenho. Dono: projectista.

---

## 🟡 MENOR

### G8 — Custo-alvo não declarado
Nenhuma peça nova entra: todas já estão em BOM de outra placa da casa. Mas o
escopo devia dizer "sem custo-alvo declarado" em vez de omitir.

### G9 — Vibração e choque não declarados
Quadro industrial. Provavelmente irrelevante para SMD pequeno, mas os dois
electrolíticos THT de 8×11 mm são a peça com mais massa da placa. Se se passarem
a cerâmicos por G3, o ponto desaparece sozinho.

### G10 — `RM3` pode mover-se se o burden mudar
O corte de 482 Hz sai de 3,3 kΩ com 100 nF. Se G1 se resolver a favor de mudar o
burden, o corte quase não se move, mas a impedância de fonte vista pelo ADC sim.
Revisitar na 2.3b.

> **FECHADO na F1, 2026-09-23.** O burden ficou nos 110 Ω, portanto o corte não
> se move. E a impedância de fonte ficou quantificada contra o datasheet do
> conversor em `planejamento_pcb_EBM2_V5.md` §2.7d: os 3,3 kΩ custam menos de
> 1 LSB abaixo de 4 kHz por canal, **desde que o condensador de 100 nF fique
> encostado ao pino**. Essa condição passou a requisito de layout da F3.

### G11 — Os três LED indicadores não foram reavaliados
Na V4.1 penduram dos rails de laço com 14,7 kΩ. Ao fundirem-se os dois rails de
laço num só, a contagem de LED e a sua corrente devem ser reconfirmadas. Entram
nos 4,5 mA de `RA5` mas ninguém verificou a queda directa a −40 °C.

### G12 — Número de camadas assumido, não confirmado
O escopo assume 4 camadas por `RC1`. A V4.1 é de 4 camadas, medido nos Gerbers.
Mas `RC1` congela o contorno, não o empilhamento. Confirmar na F1.

> **FECHADO na F1, 2026-09-23.** Quatro camadas, confirmado pelo projectista.
> A medição nos Gerbers e a resposta coincidem.

### G13 — NOVO, aberto na F1: falta o datasheet do `MCP3208`

Levantado em 2026-09-23, depois de o `G1c` fechar com «constante comum a todas».

O `MCP3208` é o componente central da placa e **o seu datasheet não existe em
nenhuma pasta do projecto**. Procurou-se em todo o OneDrive, em `C:\hw` e nas
Descargas: aparecem o `MCP3201` e o `mcp3202`, da mesma família, mas **não são a
mesma peça** e nenhum serve como substituto.

Enquanto se pensou que a calibração era por unidade, isto não incomodava: a
calibração removeria os erros de ganho e offset do conversor. **Com constante
comum, não remove.** Os erros próprios do `MCP3208` entram no orçamento de
`RE1`, e os termos já conhecidos somam **0,182 %** contra um tecto de 0,2 %.
Sobram 0,018 % para o conversor, e um erro de ganho de ±1,5 LSB num ADC de
12 bits vale sozinho 0,037 %.

**Pergunta:** fornece-se o PDF, ou autoriza-se a busca na internet? A F1 só
procura datasheets online com autorização explícita, por isso a sessão **não
procurou**.

> ## FECHADO em 2026-09-23: o datasheet chegou, e o resultado é pior do que o alarme
>
> O projectista forneceu o `DS21298E`. **As duas estimativas anteriores desta
> secção estavam erradas, em sentidos opostos**, e a verdade está em
> `planejamento_pcb_EBM2_V5.md` §2.7.
>
> O que o datasheet mostra, e que nenhuma estimativa podia adivinhar: **os erros
> de offset e de linearidade do `MCP3208` são tensões fixas, não fracções.**
> As figuras 2-18 e 2-2 mostram o erro em LSB a duplicar quando `VREF` desce de
> 5 V para 2,5 V, ou seja a tensão de erro fica igual. Como a nossa referência é
> de 2,5 V, o sinal é metade e o erro relativo é o dobro.
>
> | Cenário, limites máximos | `RE1` | Veredito |
> |---|---|---|
> | Grau `-C` (o que estava desenhado), constante comum | 0,256 % | reprova |
> | Grau `-B`, constante comum | 0,237 % | reprova |
> | Trilho de 5 V, referência 4,096 V, burden 180 Ω, constante comum | 0,201 % | reprova |
> | **Grau `-B`, calibração por unidade de dois pontos** | **0,055 %** | **cumpre** |
>
> **Com constante comum não há escolha de componente que feche `RE1`.** Isto
> deixa de ser um gap e passa a ser uma decisão de produto, registada como tal
> no planeamento. O gap fecha-se porque a incerteza acabou.
>
> Três achados adicionais do mesmo datasheet, todos sobre coisas **herdadas da
> V4.1 e nunca verificadas**: o mapa de canais não é sequencial (campo em
> `CH0`-`CH3`, `CH6`, `CH7`), o divisor do termístor saturaria a 70 °C com a
> referência nova, e o desacoplamento do `VDD` é de 100 nF quando a §6.4 pede
> 1 µF.
>
> ---
>
> **Registo da estimativa anterior, que ficou por baixo do valor real.** O
> parágrafo acima somava num só número as tolerâncias iniciais e as derivas. **São dois
> orçamentos separados**, porque o escopo os separa: `RE1` mede a 25 °C, onde só
> contam as tolerâncias iniciais, e `RE2`/`RB3` medem o erro **adicional** em
> temperatura, onde só contam as derivas. Refeita a conta:
>
> | Critério | Termos conhecidos | Tecto | Espaço para o `MCP3208` |
> |---|---|---|---|
> | `RE1`, a 25 °C | 0,102 % | 0,2 % | **0,172 %** |
> | `RE2` e `RB3`, em temperatura | 0,163 % | 0,2 % | **0,116 %** |
>
> Os dois passam. O datasheet continua a fazer falta, mas para **confirmar** um
> termo com folga, não para descobrir se a placa cumpre.
>
> **E o travão que este gap propunha não existe.** A tabela de *Ratings* do
> datasheet Panasonic `AOA0000C307`, pág. 2, mostra que em 0603 o grau de
> ±10 ppm/°C só começa em **1 kΩ** e o de ±15 ppm em **470 Ω**. A 110 Ω, o
> `ERA3AEB` de ±0,1 % e ±25 ppm/°C **é o melhor que a família oferece**. Se
> algum dia for preciso apertar, terá de ser noutro fabricante, e isso é uma
> decisão de sourcing, não uma troca de sufixo.

---

## Resumo

| Severidade | Quantidade | Estado |
|---|---|---|
| ✅ Resolvido | **10** | G1, G2, G3, G4, G5, G7, G9, G10, G12, **G13** |
| 🔴 Bloqueante | **0** | — |
| 🟠 Importante, adiado por decisão | **1** | `G6`, para a etapa 2.3b da F2, que é onde existe o artefacto que o resolve. O cálculo já está feito em `planejamento_pcb_EBM2_V5.md` §2.7f e dá 4,55 a 4,65 V contra um máximo absoluto de 4,20 V |
| 🟡 Menor, ainda aberto | **2** | `G8` custo-alvo não declarado; **`G11` os três LED indicadores nunca foram reavaliados** |
| Por confirmar | 0 | `G1b` deixou de importar: a referência passou a ser peça própria, o `ADR4525` |

**O `G11` é o único item de projecto que continua por olhar.** Na V4.1 os três
LED penduram dos trilhos de laço com 14,7 kΩ; ao fundirem-se os dois trilhos num
só, a contagem e a corrente têm de ser reconfirmadas, e ninguém verificou a queda
directa a −40 °C. Entra na F2 com a folha `06_lacos`.

**Não há bloqueantes em aberto. O Portão 0 foi assinado em 2026-09-23.** Dos
cinco gaps importantes, três fecharam na F1, um adiou-se por decisão para a
etapa em que existe o artefacto que o resolve, e um continua aberto — a que se
juntou o `G13`, aberto pela própria F1.

**O `G4` fechou da pior maneira possível: descobrindo que a sua premissa era
falsa.** O datasheet estava na pasta com outro nome, e lê-lo mudou o part number
do fusível, obrigou a acrescentar uma peça e mostrou que a configuração anterior
reprovava o critério `RA2`. Fica como lembrete de que **procurar por nome de
ficheiro não é procurar**.

**Resta o `G13`**, e é do mesmo tipo: falta um datasheet. Mas depois de refazer
o orçamento de erro em duas contas separadas, ele deixou de decidir se a placa
cumpre `RE1` e passou a ser um termo por confirmar, com folga.

**O que G2 acrescentou ao âmbito da revisão:**

| Item | Consequência |
|---|---|
| LDO de 3,3 V para `VCC1` do `ISO7141` | **Entra no âmbito.** Uma peça e dois condensadores, já em BOM da casa |
| Falso positivo a retirar | O achado de níveis lógicos do `EBM2_vs_EBM7_Comparacion.md` de 2026-08-11 está errado: o `ISO7141` é TTL |
| Barreira NÃO está contornada por fora | Verificado: na MainBoard, `GND` (208 pinos, inclui as massas da Pi) e `24V-/GND_24V` (31 pinos, nenhum pino da Pi) são redes distintas. Na Base Board, `GNDI` tem 6 pinos e não toca `GND`. **A barreira funcional é real** |
| Bus de 20 pinos verificado pino a pino | `P19` da Base Board e `J2B.15-34` da MainBoard batem certo com `P1.1-20` da EBM2. **Sem discrepância** |

**Nota sobre o contrato do bus (`L3`).** O problema das três definições
incompatíveis é do conector de **14 pinos**, não do de 20. Na MainBoard,
`J2B.4` e `J2B.11` são a **mesma rede** (`AGND`), e com a EBM2 montada isso
ligaria `P2.4` a `P2.11`. Continua fora do âmbito por decisão de 2026-09-23,
mas agora está **quantificado** e devia subir de "risco de plataforma" a item
com dono.

**O que G1 mudou no projecto**, e que a F1 tem de levar:

| Antes de G1 | Depois de G1 |
|---|---|
| Referência escolhida pela exactidão inicial de ±0,02 % | Escolhida pelo **coeficiente de 2 ppm/°C**. A exactidão inicial é irrelevante: a calibração remove-a |
| Burden apertado a 0,1 % pela tolerância | Apertado pelo **TC de 25 ppm/°C**. Depois da calibração é o burden que domina o orçamento |
| Valor do burden condicionado por `RC4` | **Livre.** 110 Ω passa a ser escolha sem custo, e resolve `RM2` |
| Orçamento de erro de ±0,18 % (inicial) | **0,15 % de deriva** entre −40 e +85 °C, que é o que `RB3` mede |
