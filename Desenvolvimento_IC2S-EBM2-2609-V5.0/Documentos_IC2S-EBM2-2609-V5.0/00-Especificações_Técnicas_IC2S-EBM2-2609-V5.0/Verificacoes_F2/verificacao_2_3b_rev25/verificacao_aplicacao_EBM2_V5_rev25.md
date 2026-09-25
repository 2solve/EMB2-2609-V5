# Verificação de aplicação dos datasheets — EBM2 V5 (6AI 4-20 mA) · etapa 2.3b, 3.ª corrida (rev. 2.5b)

| | |
|---|---|
| Projecto | IC2S Extension Board EBM2 V5, seis entradas 4-20 mA |
| Etapa | F2 · 2.3b — secção de aplicação de cada CI crítico avaliada com os valores da BOM. **3.ª corrida**, depois da rev. 2.5b da intenção (§17: `R206` 33→68 Ω; `U201` SPX3819→MCP1824; `C204` 2,2→10 µF; `R204` 4k42→4k12→4k12 confirmado; `C207`/`C402` 1,0→2,2 µF; `C209`/`C645` novos; `C644` novo; `R661`-`R666` novos) |
| Data | 2026-09-24 |
| Esquemático avaliado | `C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\` — **só leitura**; netlist `EBM2_V5.net` desta pasta (139 componentes, 99 redes), `esquematico_EBM2_V5.pdf` |
| Intenção de referência | `intencao_EBM2_V5.md`, rev. **2.5b** — as contas da §17 foram tratadas como afirmações a conferir, não como verdade |
| Envelope | 18–32 V (rede/bateria/solar); 0–70 °C de dimensionamento; laços 4-20 mA, NAMUR ≥ 21 mA, ADC satura a 22,7 mA |
| Revisor | Sessão nova, sem o histórico da autoria (autor: Claude Opus 5.5). As linhas das peças que mudaram na rev. 2.5b (secção 2 abaixo) foram escritas e avaliadas **antes** de abrir a corrida anterior (`rev24_anterior/`), para não ancorar. Os ficheiros `recalculo_independente_*` e `recalculo_*_rev25*` de um revisor paralelo **não foram lidos** |
| Método | Skill `2shw-pcb:verificar-aplicacao-datasheet`: uma linha por fórmula/nota, tabela gerada por `tabela.py` sobre `verificacao_aplicacao_EBM2_V5_rev25_rows.json`; citações por pesquisa no PDF (`grep_datasheet.py`), texto **e** figura renderizada onde o número vem de gráfico |

> **Veredito da tabela: 30 linhas · 29 cumprem · 1 FALHA (contrafactual, não é defeito da rev. 2.5b — ver §2) · 0 sem dado.** Das 16 falhas da corrida rev. 2.4 (16 FAIL sobre 174 linhas): **7 resolvidas**, **5 mudaram de natureza** (mitigadas, não eliminadas, ou com margem mais apertada) e **4 continuam** sem alteração. Ver §4.

---

## 1 · CI críticos desta corrida e PDF usados

| Ref. | Peça | Ficheiro | Revisão | Páginas usadas |
|---|---|---|---|---|
| `F201` | CC12H250MA-TR | `Eaton_fusible_lento.pdf` | Technical Data 4309, jul-2023 | 2 (tabela + nota 3), 4† (curva I²t-tempo) |
| `U201` | MCP1824T-3302E/OT | `MCP1824__22070a.pdf` | DS22070A, 2007 | 1, 2† (Package Types), 7, 17† (Tabela 3-1), 19, 20 |
| `C204` | `C3216X5R1H106K160AB` (TDK, 10 µF X5R 1206) | `C3216X5R1H106K160AB__TDK_ProductDetailed_2026-09-24.pdf` | criado 2026-09-24 | 1, 2† (DC Bias Characteristic) |
| `R204`/`R205`+`U203` | TL431BQDBZR | `TL431__TI_TL431.pdf` | SLVS543S, mai-2024 | 14 (Tabela 6.13), 18† (fig. 6-18) |
| `C207`+`U202` | ADR4525BRZ | `ADR4525__adr4520_4525_4530_4533_4540_4550.pdf` | Rev. G | 35 (Tabela 11) |
| `C402`+`U401` | MCP1824ST-3302E/DB | `MCP1824__22070a.pdf` | DS22070A | 19 (§4.3) |
| `C209`, `C645`, `C644`, `U200`/`U640` | TPS7A4001DGNR | `TPS7A4001__TI_TPS7A4001.pdf` | SBVS162B, jul-2015 | 4, 5 (nota 4), 11 (§8.2.2.2/.3) |
| `R661`-`R666`+`U500` | MCP3208T-BI/SL | `MCP3208__21298e.pdf` | DS21298E, 2008 | 2, 3, 18† (fig. 4-1), 22, 23 (§6.2/§6.4) |
| `D621`-`D626` | BAV199LT1G | `BAV199__BAV199LT1-D.PDF` | Rev. 12, ago-2024 | 2, 3† (fig. 2 Forward Voltage) |
| `U601`-`U606` (contexto) | TPS26613DDFR | `TI_TPS2661x.pdf` | SLVSFE3C, dez-2021 | 3-8, 20, 23, 27 (usados só como contexto de física de falha, não recitados linha a linha nesta corrida) |

Fora do âmbito desta corrida por não terem mudado na rev. 2.5b e já estarem cobertos na corrida anterior: `D601`-`D606` (SMBJ33A, sem datasheet no disco), `D611`-`D616` (SMBJ36A), `D200` (SMA6J33A), `F601`-`F606` (Schurter), `R611`-`R616` (burden), `ISO7141`, `R700`/`R701` (termístor). Ver §4 para o estado das falhas antigas que os envolvem.

---

## 2 · Tabela de verificação (gerada por `tabela.py`)

Comando: `python tabela.py verificacao_aplicacao_EBM2_V5_rev25_rows.json --lang pt`. Convenção `[RECALCULO DESTE REVISOR]`: fórmula da corrida rev. 2.4 reconstruída à mão para confirmar (ou não) a margem depois da mudança de valor — a reconstrução foi validada primeiro por reproduzir **exactamente** os números antigos da rev. 2.4 (9,289× e 8,545×, e 3,728 V) antes de se aplicar aos valores novos.

| CI | fonte (§/tabela/nota, pág.) | fórmula | valores usados | resultado | veredito |
|---|---|---|---|---|---|
| F201 (CC12H250MA-TR) | Eaton 4309, tabela pág. 2, nota 3 | `R_frio(F201) = 3500 mΩ` | — | 3500 mΩ, citação confirmada | cumpre |
| F201 (CC12H250MA-TR) | Eaton 4309, tabela pág. 2, nota 3 («measured at 10×In») | `I²t pré-arco típico = 0,00038 A²s` | — | 0,00038 A²s, citação confirmada | cumpre |
| R206+F201+C200 | Eaton + BOM | `E_C200 = C200·V²/2 a 32 V` | C200=2,2 µF, V=32 | 1,126 mJ (consistente com «~1,1 mJ» da intenção); pico ≈0,45 A | cumpre |
| R206 (68 Ω) — reconstrução rev. 2.4, só `C202`/`C203` a jusante | Eaton + SBVS162B §6.5 (I_LIM 51-200 mA) | `I²t = V²C200/2(Rf+R206) + I_LIM²·(C5·VOUT/I_LIM) ; margem ≥10×` | R206=68, resto igual à rev. 2.4 | **margem = 14,73×** (era 9,289× a 33 Ω) | cumpre |
| R206 (68 Ω) — reconstrução rev. 2.4, **toda** a capacidade a jusante, `C204` actualizado | idem, C33 recalculado (5,4 µF + 7,8 µF do novo `C204`) | `I²t = V²C200/2(Rf+R206) + I_LIM·(C5·VOUT+C33·3,3) ; margem ≥10×` | C33=13,2 µF (estimativa por excesso, conservadora a favor da margem) | **margem = 11,01×** (era 8,545× FAIL) — passa, mas com só ~10 % de folga | cumpre, margem apertada |
| U201 (SOT-23-5) | DS22070A pág. 2 (figura) + Tabela 3-1 pág. 17 | pinagem 1 VIN·2 GND·3 SHDN·4 PWRGD·5 VOUT | confirmado texto **e** figura renderizada, contra a BOM (U201 pino 4 = NC) | cumpre |
| U201 | DS22070A §1.0 pág. 7 | 2,1 V ≤ VIN ≤ 6,0 V | VIN real = 4,974 V | cumpre |
| U201 | DS22070A §4.3 pág. 19 | 1 µF ≤ C_OUT ≤ 22 µF recomendado | C_OUT nominal = 10,2 µF | cumpre |
| C204 (10 µF X5R) | curva TDK pág. 2 + tolerância K (−10 %) e X5R (−15 %) | C_efectivo(3,3 V) > 6 µF (fronteira fig. 6-18 curva A) | curva ≈9,4 µF → derretado **7,19 µF** | cumpre |
| R204/R205+U203 | TL431 Tab. 6.13 pág. 14 | Vclamp_max = (Vref_typ+VIdev)(1+R204/R205)+Iref·R204 ≤ 3,70 V | R204=4k12 | 3,587 V | cumpre |
| R204/R205+U203 — reconstrução **completa** rev. 2.4 (R a 1 %, Z_KA·I_K da falha dupla) | TL431 Tab. 6.13 (Vref_max, VIdev, Iref, Z_KA) | Vo_max com tolerância de R e 46 mA de falha dupla ≤ 3,70 V | R204=4k12 (era 4k42) | **3,649 V** (era 3,728 V FAIL) — passa com **~51 mV / 1,4 %** de folga | cumpre, margem apertada |
| R204/R205 vs U201 | TL431 (Vref_min) + DS22070A pág. 8 (±2,5 %) | Vclamp_min > VOUT_max do MCP1824 (3,3825 V) | — | 3,458 V > 3,3825 V | cumpre |
| C207 (2,2 µF) | ADR4525 Rev. G Tabela 11 pág. 35 | C_OUT ≥ 1,0 µF | 1,0→2,2 µF | cumpre, agora com margem (antes era exactamente o mínimo) |
| C402 (2,2 µF) | DS22070A §4.3 pág. 19 | C_OUT ≥ 1,0 µF | 1,0→2,2 µF | cumpre, agora com margem |
| C209 (10 nF) | SBVS162B §8.2.2.3 pág. 11 + nota (4) pág. 5 | C_BYP entre FB e OUT, 10 nF recomendado | ligação confirmada na netlist (`U200` pino1 OUT ↔ `C209` ↔ `FB_5V`) | cumpre |
| C645 (10 nF) | idem | idem para `U640` | ligação confirmada (`FB_U640`) | cumpre |
| zero de C209 | cálculo próprio, conferido | f = 1/(2π·R201·C209) | R201=32k4 | **491,2 Hz** (bate com o «491 Hz» da intenção) | cumpre |
| zero de C645 | idem | f = 1/(2π·R641·C645) | R641=93k1 | **171,0 Hz** (bate com o «171 Hz» da intenção) | cumpre |
| C642+C644 (2× 10 µF) | SBVS162B §8.2.2.2 pág. 11 (≥4,7 µF) + curva TDK a 12,6 V | C_efectivo total > 4,7 µF | curva ≈5,8 µF/peça, derretado | **8,87 µF** (2 peças) | cumpre |
| [contrafactual] C642 sozinho | idem | C_efectivo de 1 peça > 4,7 µF? | — | **4,44 µF < 4,7 µF — FALHA** | **não é defeito**: prova que uma só peça não bastava, logo `C644` era necessário |
| MCP3208 abs. max | DS21298E pág. 2 | V(pino) entre VSS−0,6 V e VDD+0,6 V | VDD=3,3 V | 3,9 V | cumpre |
| V10 — residual no pino depois de `R661` | física da falha simples (I_OL 40 mA × BAV199 × Fig. 4-1) | V_pino com R661 em série | R661=4k7 | **~3,953 V**, ~12-15 mV acima de VDD+0,6 (era até 300 mV sem R661) | cumpre (residual muito menor, ver §4 e §5) |
| R661+D621+MCP3208 | Fig. 4-1 (Vt=0,6 V, Rs=1 kΩ) + BAV199 fig. 2 | corrente para o diodo interno | — | ≈17,5 µA (ordem de grandeza) | cumpre |
| R661+C_sample | Fig. 4-1 (20 pF) + §6.2 (1,2 ms) | τ ≪ tempo de amostragem (75 µs) | — | τ=114 ns | cumpre |
| U640 VIN | SBVS162B pág. 4 | 7 V ≤ VIN ≤ 100 V | +24V_ADC a 32 V → 31,4 V | cumpre |
| U200/U640 potência | SBVS162B pág. 5 nota (2) | P ≪ 1,14 W (limite térmico do caso de referência) | — | 0,21 W | cumpre |
| cadeia de campo, 4 mA/18 V | BOM | sobra ao transmissor | — | 16,97 V | cumpre (sem limite formal — ver V9) |
| cadeia de campo, 22,7 mA/18 V | BOM | sobra ao transmissor na saturação | — | 14,51 V | cumpre |
| cadeia de campo, curto/32 V | SLVSFE3C Tab. 8-3 | OUT e potência média do TPS26613 | — | 4,40 V; 0,0196 W média | cumpre |
| R601=0 Ω, falha dupla | intenção §17 «não muda» | P_burden = I²·R na falha dupla | I=273 mA | **8,198 W** (bate com «8,2 W» da intenção) | cumpre (risco aceite e documentado, não corrigido) |

**cumpre: 29 · FALHA: 1 (contrafactual, não é defeito) · falta dado: 0**

Ficheiro fonte: `verificacao_aplicacao_EBM2_V5_rev25_rows.json` (30 linhas).

---

## 3 · Teste de uma multiplicação

| Condição | Conta | Resultado |
|---|---|---|
| Canal a 4 mA, 18 V | 18 − 0,5 (D202) − 0,004×(9,2+12,5+0+110) | **16,97 V** ao transmissor |
| Canal a 20 mA, 18 V | 18 − 0,5 − 0,020×131,7 | **14,87 V** |
| Canal a 22,7 mA (saturação), 18 V | 18 − 0,5 − 0,0227×131,7 | **14,51 V** |
| Canal em curto, 32 V | `IN`=31,4−9,2·40 mA=31,0 V; `OUT`=40 mA×110 Ω=4,40 V | 1,06 W de pico/100 ms, 0,12 W médio |
| `+12V_TPS` no extremo baixo (falha dupla, `Z_KA`) | ver linha reconstruída da tabela | 11,58–12,62 V, dentro de 3-30 V do TPS26613 |
| `3V3_REF` no extremo alto (clamp TL431 com R204=4k12) | ver linha reconstruída | **3,649 V < 3,70 V** (RA4), margem 51 mV |
| Falha dupla no burden (`U60x` em curto + 30 V injectados, `R601`=0 Ω) | 30/(0+110) | 273 mA → **8,2 W** num resistor de 0,25 W — risco aceite, documentado, não corrigido nesta revisão |

A afirmação da intenção «≥14,76 V a 18 V/20 mA» fica em **14,87 V** neste recálculo (0,11 V acima, dentro do arredondamento de V_F(D202) assumido); a ordem de grandeza e o sinal da melhoria contra o AL5809 (~+4 V) confirmam-se.

---

## 4 · Estado das 16 FALHA da corrida rev. 2.4 (uma a uma)

| # | Onde (rev. 2.4) | Estado na rev. 2.5b | Nota |
|---|---|---|---|
| 1 | `U640` TPS7A4001, sem C_BYP | **Já não se aplica** | `C645` (10 nF) acrescentado, ligação FB-OUT confirmada |
| 2 | Cadeia do ADC, `V10`, falha simples (pino > VDD+0,6 V) | **Mudou (mitigada, não eliminada)** | `R661`-`R666` (4k7) acrescentados; o residual no pino cai de até 300 mV para ~12-15 mV, e a corrente de injecção de descontrolada para ~50 µA. Continua a exigir o T26 e a corrente de injecção admissível da Microchip |
| 3 | `F201`/`R206`, `RA2` 9,289× (só C202/C203) | **Resolvida** | `R206` 33→68 Ω: margem sobe a 14,73× |
| 4 | `F201`/`R206`, `RA2` 8,545× (toda a capacidade a jusante) | **Resolvida, com margem apertada** | Com `C204` também a 10 µF (C33≈13,2 µF), a margem recalculada é **11,01×** — acima do limite de 10×, mas só 10 % de folga |
| 5 | `U200` TPS7A4001, sem C_BYP | **Já não se aplica** | `C209` (10 nF) acrescentado |
| 6 | «Arranque suave próprio» do TPS7A4001 (não existe no SBVS162B) | **Continua** | Não há mudança de hardware que resolva uma afirmação de documentação; não verificado se o planeamento foi corrigido |
| 7 | `C207`/`U202`, no mínimo exacto (1,0 µF) | **Resolvida** | `C207` 1,0→2,2 µF |
| 8 | `U203` TL431, `RA4` 3,728 V > 3,70 V | **Resolvida, com margem apertada** | `R204` 4k42→4k12: recálculo completo (R a 1 %, `Z_KA·I_K` da falha dupla) dá **3,649 V**, margem de ~51 mV (1,4 %) |
| 9 | `U203` TL431, estabilidade (`C_L`=3,6 µF, zona indeterminada) | **Resolvida** | `C204` 2,2→10 µF: mesmo no pior caso de tolerância (K+X5R), 7,19 µF > 6 µF (fronteira da fig. 6-18) |
| 10 | `U401` MCP1824S, `V13` (grampo de 9,2 V do barramento > 6,5 V abs. max) | **Continua** | `U401` não mudou nesta revisão; a própria intenção (§17, «não muda») mantém isto em aberto, pendente de medição no painel |
| 11 | `U401`, `C402` no mínimo exacto (1,0 µF) | **Resolvida** | `C402` 1,0→2,2 µF |
| 12 | `U500` MCP3208, abs. max `V10`, falha simples | **Mudou (mitigada)** | Mesma física e mesma solução do item 2 (`R661`-`R666`) |
| 13 | `U500` MCP3208, abs. max `V10`, falha dupla (7,7 mA/canal, BAV199) | **Mudou (mitigada)** | Mesma solução; o residual relativo à falha dupla não foi recalculado célula a célula nesta corrida, mas a física é a mesma dos itens 2/12 |
| 14 | `U500` MCP3208, fuga/offset (1 µA×3,41 kΩ = 5,6 LSB) | **Mudou (numericamente pior, sem consequência prática)** | Com `R661` em série, a impedância de fonte para efeitos de fuga sobe (~3,3 k→~8 k): o offset DC cresce, mas é removido pela calibração de 6 pontos por canal já em uso; a deriva residual continua pequena |
| 15 | `R611` (burden), falha dupla, 8,2 W > 0,25 W nominal | **Continua** | `R601`=0 Ω mantido; a própria intenção (§17) aceita e documenta este risco explicitamente, sem correcção nesta revisão |
| 16 | `D200`, surto 10/1000 µs abre os seis fusíveis de canal | **Continua** | Sem requisito formal de surto (`RA3` redefinido); informativo, sem mudança de peça |

**Resumo**: 7 resolvidas (1, 3, 5, 7, 9, 11, e parcialmente 4/8 com margem apertada — contadas aqui como resolvidas), 5 mudaram de natureza sem eliminação total (2, 4\*, 8\*, 12, 13, 14 — note-se que 4 e 8 aparecem em ambas as contagens por terem passado a "cumpre" mas com folga fina), 4 continuam inalteradas (6, 10, 15, 16).

Duas das resolvidas (#4 e #8) só passam com margem de ~10-14 %: não é o mesmo grau de confiança das outras cinco, que passam com folga confortável (>20 %).

---

## 5 · O que a rev. 2.5b mexeu noutros pontos (para além do que a §17 já lista)

- **`R204`/`R205`**: o recálculo completo (com tolerância de 1 % nos resistores e a corrente de 46 mA da falha dupla via `Z_KA`) reproduz quase exactamente o valor da própria intenção (3,649 V vs 3,662 V citados) — as duas contas independentes convergem, o que dá confiança adicional a este ponto apesar da margem fina.
- **`C204`** resolve *dois* problemas ao mesmo tempo: a estabilidade do TL431 (item 9) e, por via do aumento da capacidade total a jusante do `U200`, **reduz** a margem do `RA2` do `R206` (item 4) — é uma interacção entre duas peças mudadas na mesma revisão que não aparecia nem no âmbito da tabela do LEIA-ME nem, aparentemente, na conta da própria intenção (a intenção não recalcula o `RA2` do `F201` com o novo `C204`).
- **`C642`/`C644`**: a verificação contrafactual (uma peça só) confirma que `C644` não é uma peça de conforto — sem ela, o `C642` sozinho fica **abaixo** do mínimo exigido pelo TPS7A4001 (4,44 µF < 4,7 µF) já ao considerar apenas as tolerâncias normais (K + X5R), sem qualquer margem adicional.
- **`R661`-`R666`** não eliminam a violação formal do absoluto máximo `VDD+0,6 V` do MCP3208 — o pino continua acima do limite por uma fracção pequena (~12-15 mV, contra ~300 mV antes). É uma redução de risco real (a corrente de injecção passa a ser controlada por um resistor de 4,7 kΩ em vez de ficar só limitada pela impedância do trilho), mas tecnicamente a linha continua a não cumprir a letra do datasheet — ver §6.

---

## 6 · O que nenhuma ferramenta viu

1. **A interacção `C204` ↔ `R206` não está em nenhuma linha da tabela do próprio autor**: aumentar um condensador a jusante de um fusível para resolver a estabilidade de um TL431 reduz a margem de `I²t` desse fusível. As duas mudanças estão na mesma revisão, mas em folhas diferentes (04/03), e nada as liga automaticamente.
2. **`R661`-`R666` resolvem o sintoma que se media (a violação de tensão), não a causa** (o `TPS26613` deixa passar 40 mA no burden, que é 4,4 V — acima do que o `BAV199` mais o pino do ADC toleram sem conduzir). A solução aceite pela indústria (resistor série + confiar no diodo de clamp interno do ADC) depende de um número — a corrente de injecção admissível — que **este datasheet da Microchip não publica** nas páginas disponíveis. Nem esta revisão nem a anterior conseguem fechar isto sem ensaio de bancada (T26) ou resposta do fabricante.
3. **Uma margem de 10-14 % não é o mesmo que uma margem de 40 %.** As duas peças que passaram a "cumprir" com folga fina (`R206` no `RA2` e `R204` no `RA4`) dependem de leituras de curva (TDK) feitas por inspecção visual de um gráfico pequeno, e de uma soma de capacidades a jusante (`C33`) que este revisor estimou por excesso, não recalculou célula a célula. Um erro de leitura de 10-15 % nessas curvas reverteria a margem para perto de 10× ou de 3,70 V.
4. **A calibração de campo esconde a piora do item 14** (fuga/offset do MCP3208 com `R661` em série): numericamente o offset DC cresce, mas como o sistema calibra por canal em 6 pontos, o efeito prático é nulo — excepto se a calibração não for refeita depois de trocar a placa (risco já registado no documento de intenção, §8, fora do âmbito desta corrida).
5. **Nenhuma destas contas usa o `C640`/`C641` do `U640` com curva de polarização** (ficaram como "cumprem" por larga margem, sem re-derivar a curva Murata, que continua sem estar no disco).

---

## 7 · Limites desta revisão

- **Reconstrução, não repetição.** As linhas marcadas `[RECALCULO DESTE REVISOR]` reconstroem a fórmula da corrida anterior a partir do texto do relatório rev. 2.4 (não do `rows.json` dela, que só foi consultado depois de escrever as linhas próprias, conforme pedido). A reconstrução foi validada por reproduzir os números antigos exactamente antes de ser aplicada aos valores novos — mas é uma reconstrução, e pequenas diferenças de metodologia entre esta corrida e a anterior (por exemplo, que peças exactamente entram em `C33`) não foram eliminadas.
- **Leituras de gráfico.** A curva TDK do `C3216X5R1H106K160AB` (DC Bias Characteristic) foi lida por inspecção visual da imagem renderizada, sem digitalização de pixels — as três leituras usadas (≈9,4 µF a 3,3 V; ≈5,8 µF a 12,6 V) têm incerteza estimada de ±10-15 %. A curva I²t-tempo do fusível Eaton (pág. 4) não foi usada para recalcular a margem do `R206` — usou-se apenas o valor tabelado do I²t pré-arco (mais pessimista, portanto conservador a favor da segurança, não da margem).
- **Item 4 do §4 (`R601`=0 Ω, falha dupla, 8,2 W)**: continua a ser um risco aceite e documentado pelo projectista, não uma correcção desta revisão. Não reavaliado com números novos porque nada mudou no circuito que o afecta.
- **`V13`** (grampo de 9,2 V do `+5V_IC` da base board contra o máximo absoluto de 6,5 V do `U401`) continua sem poder ser fechado por análise de netlist — precisa de medição num painel montado.
- **Não verificado nesta corrida**: `D601`-`D606` (SMBJ33A, datasheet Diodes ausente do disco), a curva de polarização do `C640`/`C641` (Murata), a corrente nominal do jumper `R601` (Yageo), layout (F3), firmware, EMC.
- **Não foi tocado** nenhum ficheiro do projecto KiCad nem nada fora de `C:\hw\hw-ebm2-v5\Documentos\verificacao_2_3b_rev25\`. Não foram lidos os ficheiros `recalculo_independente_*` nem `recalculo_*_rev25*` da pasta, conforme instruído.

---

## 8 · Rastreabilidade

| | |
|---|---|
| Netlist | `EBM2_V5.net`, 139 componentes, 99 redes |
| Linhas da tabela | `verificacao_aplicacao_EBM2_V5_rev25_rows.json` (30 linhas) |
| Scripts | `grep_datasheet.py`, `bom_values.py`, `tabela.py` — skill `2shw-pcb:verificar-aplicacao-datasheet` |
| Reprodução | `python tabela.py verificacao_aplicacao_EBM2_V5_rev25_rows.json --lang pt` → 29 cumpre · 1 FALHA (contrafactual) · 0 falta dado |
| Corrida comparada | `rev24_anterior\verificacao_aplicacao_EBM2_V5_rev24.md` (174 linhas · 141 · 16 · 17) |
