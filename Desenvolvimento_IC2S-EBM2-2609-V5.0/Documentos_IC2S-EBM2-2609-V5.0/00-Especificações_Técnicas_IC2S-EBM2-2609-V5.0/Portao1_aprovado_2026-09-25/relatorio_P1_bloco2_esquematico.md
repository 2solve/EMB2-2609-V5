# Relatório — Portão 1, Bloco 2 (esquemático + intenção) — EBM2 V5

**Verificador:** Claude Sonnet 5, sessão independente (sem histórico de autoria). Autor do esquemático: Claude Opus 5.5.
**Âmbito deste relatório:** só o **Bloco 2** (esquemático KiCad + documento de intenção), conforme pedido. Blocos 1 (diagrama) e 3 (BOM/mapa de pinos) **não** foram avaliados aqui.
**Data:** 2026-09-25. Netlist analisada: `EBM2_V5.net` (export 2026-09-25T07:10:38, o mais recente na pasta — inclui a correcção da tanda C do `C200`). ERC analisado: `erc.json` (mesmo timestamp).

## Veredicto do bloco: **APROVADO COM RESSALVAS**

Não encontrei nenhum bloqueante. Encontrei duas ressalvas de higiene/documentação (nenhuma altera um valor eléctrico) e algumas limitações de leitura de curvas que não pude confirmar ao pixel. Ver tabela de achados e limites abaixo.

---

## 1. ERC

**Resultado: 0 erros — confirmado duas vezes de forma independente.**

- `erc.json` do autor: `included_severities: ["error"]`, todas as 8 folhas com `"violations": []`. Erros = 0.
- Reproduzi com a ferramenta MCP do servidor KiCad (`run_erc`), conforme o hábito de dupla verificação. Na primeira tentativa obtive **54 erros falsos** (rótulos hierárquicos "não podem ligar a uma folha pai inexistente", `MOSI`/`CLK`/`CS_ADC`/`MISO`/`LOOPn_V+`/`AINn-`, etc.) — isto era um artefacto da **minha** configuração: o `kicad_set_project` tinha escolhido por omissão `01_conectores.kicad_sch` como ficheiro-raiz, quando a raiz real do projecto é `IC2S_Extension_Board-EBM2_V5.kicad_sch` (confirmado por `grep` nos `.kicad_sch`, que mostra as folhas filhas referenciadas a partir desse ficheiro). Corrigindo o `sch_file` para a raiz real, o `run_erc` do MCP devolveu **VERDICT: WARN, 0 erros, 292 avisos** — concorda com o `erc.json` do autor (que filtra avisos).
- Os 292 avisos são quase todos de resolução de bibliotecas (ver achado #2), não de conectividade.

**Conclusão: ERC limpo confirmado. Este ponto do Portão 1 está cumprido.**

## 2. Polaridade de díodos/TVS/LED e orientação de CI

Verifiquei por **render ampliado (PyMuPDF, 8-12×)** do PDF, símbolo a símbolo, contra a **netlist** (pino 1 = cátodo, convenção documentada na própria folha 02, nota 7: "Diodos: pino 1 = CATODO"):

| Peça(s) | Papel | Orientação esperada (netlist) | Confirmado no render | Nota |
|---|---|---|---|---|
| `D200` (SMA6J33A-Q) | TVS de entrada | K→`+24V`, A→`GND_24V` | ✔ barra no topo (+24V), triângulo para baixo (GND_24V) | grampo verificado, ver §3 |
| `D201`, `D202` (MBR1H100SF) | Schottky série (polaridade inversa) | K→trilho a jusante, A→lado do fusível | ✔ seta aponta fusível→trilho nos dois | consistente com §4/§8 da intenção |
| `D203`, `D204`, `D630` (KG EELP41.22, LED) | Indicadores | A→resistência/trilho, K→GND | ✔ nos três | ligações conferem com §11: `D203`="há entrada", `D204`="F201 e regulador bem", `D630`="F202 inteiro" |
| `D601`-`D606` (SMBJ33A) | TVS retorno (`AINn-`) | K→`AINn-`, A→`GND_ADC` | ✔ amostra `D601` | uniformidade das 6 instâncias confirmada por netlist (todas com o mesmo padrão de pino) |
| `D611`-`D616` (824520361/SMBJ36A) | TVS terminal (`LOOPn_V+`, depois do fusível) | K→`LOOPn_V+`, A→`GND_ADC` | ✔ amostra `D611` | idem; localização "depois do fusível, no lado do terminal" confirmada (D611 está no nó pin2 de `F601`, não em `+24V_ADC`) |
| `D621`-`D626` (BAV199) | Clamp duplo do sinal filtrado | COM(pino3)→sinal, A1(pino1)→`GND_ADC`, K2(pino2)→`3V3_REF` | ✔ amostra `D621` | **Confirmado contra a FIGURA da pág. 1 do datasheet onsemi `BAV199LT1/D`**: pino 1 = Anode, pino 2 = Cathode, pino 3 = nó comum Cathode/Anode. A aplicação usa o nó comum como sinal e os dois terminais como grampos para `GND_ADC` (baixo) e `3V3_REF` (alto) — topologia correcta para grampo duplo |
| `U400` (ISO7141CCDBQR) | Isolador digital | 16 pinos, canal D reverso (MISO) | ✔ | **16/16 pinos conferidos directamente contra a tabela da pág. 4 do datasheet TI `SLLSE83F` (coluna ISO7141)** — nome, direcção (`IND`=campo/entrada, `OUTD`=barramento/saída, é o único canal reverso) e rede batem certo com a netlist e com a intenção §7. A própria folha regista a armadilha do datasheet (pinos 5,6,11,12 trocam entre ISO7131/ISO7140/ISO7141) e usa a coluna certa |
| `U401` (MCP1824ST-3302E/DB) | LDO do lado do barramento | 4 pinos | ✔ | 4/4 pinos conferidos contra a intenção/netlist (VIN=+5V, GND=DGND, VOUT=+3.3V_DIG, patilha=DGND) |
| `U500` (MCP3208T-BI/SL) | ADC | 16 pinos | ✔ | **16/16 pinos conferidos contra a tabela §8 da intenção e a netlist** — mapa de canais não sequencial confirmado (`CH6`=`AIN5_ADC`, `CH7`=`AIN6_ADC`), rótulo "canal N → CHx" também presente no desenho da folha 06 |

Adicionalmente confirmei, por netlist, que **`R200` é a única ligação entre `GND_24V` e `GND_ADC`** (5 nós no total em `GND_24V`: `D200`, `D203`, `P1.19`, `R200.1`, `T202`) e que **`DGND` não tem nenhum nó em comum com `GND_ADC`** a não ser através do isolador `U400` — confirma a nota 6 da folha 02 e a "barreira funcional" desenhada na folha 04.

**Texto sobre símbolo / fora da moldura:** inspeccionei as 8 folhas (renders de página inteira) — nenhuma sobreposição de texto sobre símbolo nem texto fora da moldura em nenhuma das folhas.

**O que NÃO foi feito individualmente:** não renderizei cada uma das 18 instâncias das famílias D60x/D61x/D62x uma a uma — verifiquei uma amostra visual de cada família (`D601`, `D611`, `D621`) e confirmei por netlist que as restantes 15 instâncias têm exactamente o mesmo padrão de ligação por pino. Assumo que a geometria do símbolo (não só a rede) se repete de forma idêntica nas seis colunas — isto é plausível (a folha 06 mostra os seis blocos visualmente idênticos) mas não confirmei geometricamente cada um.

## 3. Tandas — contas refeitas

### `R206` 150 Ω / `RA2` do `F201` (rev. 2.5c)

Conferido contra `Eaton_fusible_lento.pdf` (Technical Data 4309, CC12H):
- **Pág. 2, tabela**: linha `CC12H250mA`: resistência DC a frio típ. **3500 mΩ = 3,5 Ω**; I²t de pré-arco típ. **0,00038 A²s = 3,8×10⁻⁴ A²s**; nota 3 "Typical pre-arcing I²t value is measured at 10In rated current" — **texto e tabela batem exactamente** com o que a intenção cita.
- Refiz a conta: `I_max = 32 V / (150 + 3,5) Ω = 32/153,5 = 0,2084 A` ✔ (bate com "0,21 A" citado).
  `∫I² ≤ I_max × Q_total = 0,2084 × (70+92)×10⁻⁶ = 3,376×10⁻⁵ A²s` ✔ (bate com "3,4×10⁻⁵" citado).
  `Razão = 3,8×10⁻⁴ / 3,4×10⁻⁵ = 11,18×` ✔ **bate exactamente** com o "11,2×" citado no §17.
  A 18 V, 7 mA de carga: `V_R206 = 0,007×150 = 1,05 V` ✔ bate exactamente.
- **Pág. 4, curva I²t vs. tempo**: a leitura da curva a 0,1-0,5 ms (~6×10⁻⁴ a 1,5×10⁻³ A²s) é **plausível pela forma/posição da curva de 250 mA**, mas não medi ao pixel — fica como limitação, não como confirmado.
- **Não reproduzi** de forma independente o cálculo dos 92 µC "a jusante" (soma de cargas de `C202`, trilho `3V3_REF` e `C207` — não abri todos os nós envolvidos) nem o valor "realista" de 14,3×. Fica como limitação.
- **Netlist confirma** o valor final: `R206` = `150R`, MPN `SG73P2ATTD1500F` (KOA), consistente com a decisão 2.5c.

### Grampo do `D200` = 53,3 V

Confirmado **exactamente** contra `SMA6J33A__Bourns_SMA6J33A-Q.pdf`, pág. 2, tabela: linha `SMA6J33A` (unidireccional, marcação `6JM`): `V_RWM` = 33 V, `V_BR` 36,7-40,6 V, **`V_RSM` (grampo máximo) = 53,3 V** a `I_RSM` = 11,3 A. A folha 02 do esquemático regista a auto-correcção (a versão anterior dizia 58,1 V, que era o valor do `SMA6J36A`, não do `33A`) — a versão actual está certa.

### `SG73P` (impulso de `R206`)

`SG73P.pdf` pág. 2 tem a curva "One-Pulse Limiting Electric Power" para o tamanho 0805 (`SG73P 1E-2A`). O valor citado (~26 W a 0,6 ms) é consistente com a ordem de grandeza da curva log-log nessa duração, mas **não medi ao pixel** — limitação.

### `C200` (2,2 µF / 100 V, X7R 1210, `C3225X7R2A225K230AB`)

`C3225X7R2A225K230AB.pdf` pág. 1: capacitância nominal 2,2 µF ±10 %, 100 V, X7R (±15 %) — confirmado. Pág. 2, curva "DC Bias Characteristic": a 30,4 V a curva está claramente na parte descendente inicial, valor lido compatível com a ordem de grandeza de ~1,5 µF citada (não medido ao pixel). A conta `1,54 × 0,90 × 0,85 = 1,178 ≈ 1,18 µF` está aritmeticamente certa e fica acima de 1 µF (mínimo do `TPS7A4001`) com folga. Netlist confirma `C200` = MPN `C3225X7R2A225K230AB`, footprint `C_1210_3225Metric`.

### Folha 01 — porto `DGND` do `P1.12`

Confirmado **legível**: no render ampliado, o triângulo `DGND` do pino 12 está agora deslocado para a direita/baixo e **não** sobrepõe o texto "13 ID3 — manter desligado" — a correcção da tanda "Textos 25c" está aplicada e visível.

## 4. Amostras da netlist contra as tabelas da intenção (§8, §9) — e além

Fiz mais do que as 3-5 amostras pedidas, dado que os pinos de CI de barramento largo (16 pinos) são fáceis de conferir por completo e valem mais do que uma amostra parcial:

1. **`U400` (ISO7141) — 16/16 pinos** conferidos contra §7 e a tabela do datasheet (ver secção 2 acima).
2. **`U500` (MCP3208) — 16/16 pinos** conferidos contra §8 (ver secção 2 acima); mapa de canais não sequencial confirmado.
3. **Canal 1 completo (§9)** conferido nó a nó: `+24V_ADC → F601 → LOOP1_V+` (`P2.2`) e `D611` cátodo no mesmo nó (depois do fusível, como diz a rev. 2.3); retorno `AIN1- → P2.3`, `D601` cátodo aqui, `U601` pino 4 (`IN`) aqui; `U601` pino 5 (`OUT`) → `AIN1_LIM` → `R601` (0 Ω) → `AIN1_MED` → `R611` (110 Ω, burden, a `GND_ADC`) e `R621` (3k3, antialias) → `AIN1_FILT` → `C601` (100 nF a `GND_ADC`) e `D621` (`COM`) → **`R661` (4k7) → `AIN1_ADC`**. Tudo bate, **excepto** que `R661` não está mencionado na prosa do §9 (ver achado #13).
4. **`U401` (MCP1824) — 4/4 pinos** conferidos.
5. Confirmei por netlist que os seis canais (`D601`-`D606`, `D611`-`D616`, `D621`-`D626`, `U601`-`U606`, `R60x`/`R61x`/`R62x`/`R66x`, `C60x`) têm **conectividade uniforme** entre si (mesmo padrão pino-a-rede, só muda o índice do canal) — consistente com a tabela §9 e com o render da folha 06 (seis blocos visualmente idênticos, cada um rotulado "canal N → CHx").

---

## Tabela de achados

| # | Onde | Achado | Evidência | Severidade |
|---|---|---|---|---|
| 1 | `sym-lib-table` do projecto KiCad | Aponta para 10 bibliotecas `EBM7_V23_proyectoN.kicad_sym` em `${KIPRJMOD}/symbols/`, mas **essa pasta não existe** no projecto EBM2_V5 (só existe `footprints/EBM2_V5.pretty`, com `fp-lib-table` correcto e auto-suficiente). Parece um `sym-lib-table` copiado do projecto EBM7 sem limpeza. Não gera erro de ERC porque o KiCad usa o cache de símbolos embebido no `.kicad_sch`, mas **numa sessão MCP limpa gerou 292 avisos de resolução de biblioteca**, e significa que o projecto não é portátil: abrir noutra máquina, ou usar "Update Symbol from Library", pode falhar ou substituir símbolos | `C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\sym-lib-table`; ausência confirmada de `KiCad_EBM2_V5\symbols\`; `run_erc` via MCP (292 avisos, 0 erros) | Ressalva |
| 2 | `intencao_EBM2_V5.md` §5 (linha 185) | A prosa da folha 02 ainda diz "`R206` ... 33 Ω (rev. 2.2)", desactualizada — o valor final (rev. 2.5c, §17 linhas 647-648) é **150 Ω**, e é o que está no esquemático/netlist. Um leitor que só leia §5 fica com o valor errado | `intencao_EBM2_V5.md:185` vs. `:647-648`; netlist `R206`=`150R` | Ressalva (documentação; o esquemático está certo) |
| 3 | `intencao_EBM2_V5.md` §9 | A prosa "o outro terminal de `R621` forma `AIN1_ADC`" omite o resistor série `R661`-`R666` (4k7, introduzido na rev. 2.5, §17 linha 657, com justificação e cálculo próprios) que está realmente entre o nó do filtro e o pino do ADC. O componente está correcto e bem justificado noutro sítio do documento, só a narrativa do §9 não foi actualizada | `intencao_EBM2_V5.md:368` vs. `:657`; netlist confirma `R661`-`R666` presentes | Ressalva (documentação) |
| 4 | Curva pág. 4 do Eaton CC12H; curva pág. 2 do SG73P; curva "DC Bias" pág. 2 do TDK C3225X7R2A225K230AB | Os valores citados nas três curvas (I²t a 0,1-0,5 ms; potência de impulso a 0,6 ms; capacitância a 30,4 V) são plausíveis pela forma/posição das curvas, mas **não foram medidos ao pixel** — não posso confirmar a 2ª casa decimal | PDFs citados, pág. 4/2/2 respectivamente | Nota / limitação |
| 5 | `U202` (`ADR4525WBRZ-R7`), pinos `NIC`/`DNC` | Ligação (`VIN`=`3V3_REF`, `VOUT`=`+2V5_REF`, `GND`=`GND_ADC`, `NIC`/`DNC` sem ligação) é internamente consistente na netlist; **não fui ao datasheet do ADR4525 confirmar a figura de pinagem** nem à tabela 14/nota 2 (grau B vs. W) citada no §17 — isso é matéria de BOM/grau de peça (Bloco 3), fora do âmbito pedido para este relatório | netlist `U202` | Nota / fora de âmbito (Bloco 3) |
| 6 | Geometria dos símbolos `D602`-`D606`, `D612`-`D616`, `D622`-`D626` | Só verifiquei visualmente uma amostra por família (`D601`, `D611`, `D621`); as restantes 15 instâncias foram confirmadas só por netlist (conectividade), não por render individual da geometria do símbolo | render PDF + netlist | Nota / limitação |

**Nenhum achado bloqueante.**

---

## O que foi conferido e o que não foi (limites)

**Conferido:**
- ERC = 0 erros, duas vezes, com fontes independentes (autor + MCP, depois de eu corrigir a raiz do projecto).
- Polaridade de todas as famílias de díodo/TVS/LED por render ampliado + netlist; orientação completa (16/16, 16/16, 4/4 pinos) de `U400`, `U500`, `U401` contra os respectivos datasheets/intenção.
- Coordenação fusível/resistor `F201`/`R206` (rev. 2.5c) recalculada com os números exactos do datasheet Eaton.
- Grampo do `D200` (53,3 V) confirmado exactamente contra a tabela do datasheet Bourns.
- Legibilidade da folha 01 (porto `DGND` do `P1.12`).
- Isolamento de domínios de massa (`GND_24V`↔`GND_ADC` só por `R200`; `DGND` sem ligação directa a `GND_ADC`).
- Ausência de texto sobreposto ou fora da moldura nas 8 folhas.
- Canal 1 completo (§9) nó a nó.

**Não conferido / limitações:**
- Leitura ao pixel das curvas Eaton (I²t-tempo), KOA SG73P (potência de impulso) e TDK C3225 (DC bias) — só validado por ordem de grandeza e forma da curva.
- Cálculo independente completo dos "92 µC a jusante" do `R206`.
- Datasheet do ADR4525 (pinagem/grau) — matéria de BOM, fora do âmbito deste relatório de Bloco 2.
- Geometria de símbolo individual das 15 instâncias de TVS/clamp não amostradas (só a conectividade foi confirmada para todas).
- Blocos 1 e 3 (diagrama, BOM, mapa de pinos) — fora do âmbito pedido.
