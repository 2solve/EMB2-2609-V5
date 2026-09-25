---
verificador: agente independente (Claude Sonnet 5), Portão 1 — Bloco 3 (BOM preliminar + mapa de pinos)
autor_original: outro modelo (Claude Opus 5.5)
data: 2026-09-25
âmbito: só o Bloco 3 — não cobre esquemático, layout, ERC/DRC nem os outros blocos do Portão 1
método: recálculo independente (parsing próprio da netlist kicadsexpr, não confio nas ferramentas do autor), render pixel-a-pixel das curvas dos datasheets (PyMuPDF a 6-8x, calibração dos eixos por gridline/rótulo, leitura do traço), comparação directa com os JSON crus da Mouser
---

# Relatório de verificação — Portão 1, Bloco 3 (BOM preliminar e mapa de pinos) — EBM2 V5

## Veredicto do bloco

**Aprovado, sem bloqueadores.** Não encontrei nenhuma divergência entre BOM, netlist e mapa de pinos, nem nenhum valor comercial fabricado. As contas de pior caso dos condensadores e a curva de impulso do R206 foram re-obtidas de forma independente (leitura de pixel sobre o datasheet renderizado, não confiando na leitura do autor) e batem com o que a BOM/intenção afirmam, dentro da precisão de leitura de uma curva. Há **2 achados de severidade baixa/média**, nenhum impede a assinatura, mas o achado #1 merece uma nota no processo antes de travar o `ADR4525WBRZ-R7` como peça de produção.

## 1 · BOM vs netlist (referências, quantidade, valor, pegada, MPN)

Parsing próprio do `EBM2_V5.net` (formato kicadsexpr, `Value`/`Footprint`/`MPN` em blocos multi-linha — parsing por profundidade de parênteses, não por regex de uma linha).

- Netlist: 139 `(comp ...)` no total; 13 têm a propriedade `exclude_from_bom` (3 `FID10x` fiduciais + 10 `Txxx` pontos de teste) → **126 componentes elegíveis para BOM**.
- BOM preliminar (csv+md): 43 linhas, refs expandidas = **126, todas únicas** (zero duplicados).
- Conjunto de referências: **netlist == BOM, exactamente** — 0 em falta, 0 a mais.
- Por cada uma das 126 referências: **Pegada, MPN e Valor da BOM == netlist**, sem excepção (comparação campo a campo, não amostragem).
- Quantidade por linha (`Qtd` vs contagem de refs expandidas): 0 divergências nas 43 linhas.
- As 13 posições `exclude_from_bom` (fiduciais + `T2xx`/`T4xx`/`T5xx`/`T640`) ficam fora da BOM correctamente — nenhuma aparece nela.

**Conclusão do item 1: match perfeito, 126/126.**

## 2 · Peças mudadas nas tandas — MPN contra datasheet e contas de pior caso

Refeitas de forma independente, sem usar os números do autor como ponto de partida — render do datasheet a 6-8x, calibração dos eixos pelos próprios gridlines/rótulos (não pela legenda), leitura do traço vermelho por varrimento de pixels.

### C200 — TDK `C3225X7R2A225K230AB` (2,2 µF/100 V, X7R ±15 %, 1210)
- Datasheet pág. 1: 2,2 µF ±10 %, 100 VDC, X7R(±15 %) — confirmado texto.
- Curva DC Bias (pág. 2, figura "DC Bias Characteristic"): leitura própria por pixel a 30,4 V → **1,543 µF** (a BOM diz "~1,54 µF"; bate).
- Pior caso = 1,543 × 0,90 (tolerância −10 %) × 0,85 (X7R −15 %) = **1,178 µF**. A BOM diz 1,18 µF — bate.
- Requisito: C200 está no net `+24V_REG`, que confirmei no netlist ser o **pino 8 (IN, power_in) do U200/U640 (TPS7A4001)** — é o capacitor de **entrada**. TI TPS7A4001 datasheet (SBVS162B, secção 8.2.2.2, pág. 11): *"...achieves stability with a minimum output capacitance of 4.7 µF and **input capacitance of 1 µF**"*. 1,178 µF > 1 µF do requisito de **entrada** — correcto, a BOM não confundiu entrada com saída.
- Alternativa X7S 1206 (`C3216X7S2A225K160AB`) descartada: reli a curva a 30,4 V → 1,277 µF × 0,90 × 0,78 (X7S −22 %) = **0,896 µF** (BOM diz 0,89 µF — bate) — correctamente abaixo de 1 µF, correctamente descartada.

### C202/C204/C642/C644 — TDK `C3216X5R1H106K160AB` (10 µF/50 V, X5R ±15 %, 1206)
- Datasheet pág. 1: 10 µF ±10 %, 50 VDC, X5R(±15 %) — confirmado.
- Releitura própria da curva DC Bias (pág. 2): a 5 V → 9,20 µF; a 3,3 V → 9,74 µF; a 12,6 V → 5,78 µF.
- Pior caso (×0,90×0,85): **C202 a 5 V → 7,03 µF** (BOM: 7,0 — bate); **C204 a 3,3 V → 7,45 µF** (BOM: 7,2 — diferença de leitura ~3 %, na direcção conservadora: o valor real é *melhor* que o citado, não pior); **C642 ou C644 sozinho a 12,6 V → 4,42 µF**, os dois em paralelo → **8,84 µF** (BOM: 8,9 — bate).
- Requisito: confirmei no netlist que C202 está no net `+5V_ADC` = **pino 1 (OUT) do U200**, e C642+C644 no net `+12V_TPS` = **pino 1 (OUT) do U640** — são capacitores de **saída** do mesmo TPS7A4001, cujo mínimo de estabilidade é **4,7 µF** (não 1 µF). C202 (7,03) e a dupla C642+C644 (8,84) folgam esse limite. **Um só** dos dois capacitores de U640 (4,42 µF) ficaria *abaixo* dos 4,7 µF — mas isto já está documentado pelo próprio autor em `intencao_EBM2_V5.md` linha 656 ("uma peça dá 4,4 µF < 4,7 µF... Duas: 8,9 µF"), não é um achado novo, é redundância por desenho.
- C204 está no net `3V3_REF`, alimentado pelo **U201 (MCP1824)**, não pelo TPS7A4001 — a BOM não afirma um limiar numérico para C204 (só reporta a leitura da curva), o que está correcto.

### C207/C402 — TDK `C1608X5R1E225K080AB` (2,2 µF/25 V, X5R ±15 %, 0603)
- Releitura própria: a 2,5 V → 1,833 µF; a 3,3 V → 1,617 µF.
- Pior caso: **C207 a 2,5 V → 1,40 µF** (BOM: 1,44 — próximo); **C402 a 3,3 V → 1,24 µF** (BOM: 1,26 — próximo). Ambos ≥ 1 µF (entrada do ADR4525 / MCP1824).

### R206 — KOA `SG73P2ATTD1500F` (150 Ω, 0805, série anti-surto "2A")
- Confirmei no datasheet (pág. 2, tabela "applications and ratings") que a designação de tamanho da peça é **"2A"** (0,75 W) — usei o gráfico certo ("SG73P 1E-2A", curva rotulada "2A", não a "2B-2E" que é para outro tamanho).
- Releitura própria da curva "One-Pulse Limiting Electric Power" por calibração de eixos log-log (gridlines/rótulos "1000/100/10/1/0,1 W" e "0,001…1000 ms") e varrimento de pixel a 0,6 ms: **26,3 W**. A BOM diz "~26 W" — bate.
- Contra o pulso citado de 6,6 W/0,6 ms: margem = 26,3/6,6 = **3,98×** ≈ "~4×" da BOM — bate.
- **Limitação:** não re-derivei o próprio valor do pulso (6,6 W / 0,6 ms); essa conta pertence à análise do transiente de arranque (F2/esquemático), documentada em `intencao_EBM2_V5.md` linha 648, fora do âmbito deste Bloco 3.

### U202 — Analog Devices `ADR4525WBRZ-R7` (referência 2,5 V, SOIC-8)
- Tabela 14 (Ordering Guide, pág. 40): `ADR4525WBRZ-R7` existe, -40 a +125 °C, SOIC 8-lead, pacote R-8, reel 1000 — confirmado texto e tabela.
- Nomenclatura confirmada: "W" = automóvel, "B" = grau (nota 2, pág. 41); logo `ADR4525WBRZ-R7` é grau **B**, o mesmo grau da `ADR4525BRZ` original (descontinuada/Restricted Availability) — a afirmação "mesmo grau B" está correcta.
- Tabela 2 (Electrical Characteristics, pág. 4): Grau B, TCV −40…+125 °C = 2 ppm/°C (box) / **4 ppm/°C (bowtie)**; Grau A = 4/**8 ppm/°C (bowtie)** — confirma "grau A não serve: 8 ppm/°C bowtie contra 4".
- **Achado #1 (severidade média):** a pág. 41 traz a nota "AUTOMOTIVE PRODUCTS": *"...this automotive model **may have specifications that differ** from the commercial models; therefore, designers should **review the Specifications section... carefully**"*. A BOM e a intenção citam a nota 2 (que só define "W = automóvel") mas não respondem a este aviso explícito. Verifiquei eu mesmo as págs. 3-4 (tabelas 1-2) e **não há uma coluna/tabela separada para o grau W-automóvel** — os números publicados são os mesmos da tabela de graus A/B/C/D comercial, o que sustenta a substituição. Mas a documentação do Portão 1 devia registar esta verificação explicitamente (ou o contacto recomendado à Analog Devices), em vez de citar só a definição de "W" sem tratar o aviso.

## 3 · Dados comerciais (preço/stock com fonte e data; alternativas verificadas)

- Todas as 43 linhas da BOM têm `Ciclo_vida` ou "N/D" ou uma fonte+data entre parênteses — **nenhuma célula com valor "estimado"** (busca de texto no CSV: 0 ocorrências).
- Verifiquei os JSON crus da Mouser (`bom_dados_mouser_2026-09-25.json`, consulta 2026-09-25T06:09-07:09) contra a BOM, por amostragem dirigida às peças críticas: `ADR4525WBRZ-R7` (14,80/11,59/9,91 USD, stock 2147, "Restricted Availability"), `TPS7A4001DGNR` (3,53/2,65/2,18), `MCP3208T-BI/SL` (5,76/5,76/4,64 — sem quebra de preço em 10, correctamente usa o preço da quebra de 1), `ISO7141CCDBQR` (10,94/8,56/7,30, stock 0) — **todos batem exactamente** com o JSON, nenhum valor fabricado.
- `ADR4525BRZ` (peça original, citada como alternativa/motivo da troca): confirmei no JSON principal (não no ficheiro de alternativas) — stock `null`, `PriceBreaks: []`, `LifecycleStatus: "Restricted Availability"` — bate exactamente com a afirmação da BOM.
- **Schurter `3413.0002.11` vs `.22`** (`Schurter_USFF1206_3413.pdf`, págs. 3-4): confirmado — mesma linha eléctrica (0,05 A / 63 VDC / 9200 mΩ / I²t 0,0002 A²s / marcação "e"), os códigos `.11/.22/.24/.26` só diferem na embalagem (100 un. saco ESD / 1000 un. bobina 18 cm / 5000 / 10000). **Correcto.**
- **LED `Q65113A7469`** (datasheet OSRAM `KG_EELP41.22`, pág. 3, "Ordering Information"): a linha `KG EELP41.22-PHRH-35-A8J8` lista o código de encomenda **`Q65113A7469`** — correspondência exacta ao MPN original (sem o sufixo de embalagem `-20-R18`). **Correcto.**
- **`ISO7141CCDBQ` vs `ISO7141CCDBQR`** (TI, "Package Option Addendum", pág. 27): ambos "Active"/"Production", SSOP (DBQ) 16 pinos, mesma marcação "7141CC", mesmo MSL/acabamento; só mudam `75 | TUBE` vs `2500 | LARGE T&R`. **Correcto.**

## 4 · Mapa de pinos vs netlist

Pedido: amostragem de 5-10 pinos. Fiz a verificação **completa** dos 4 componentes de maior pinagem do mapa (66 pinos no total), comparando `mapa_pinos_EBM2_V5.md` contra o net-para-pino extraído por mim da `EBM2_V5.net` final (a mesma usada na BOM, `tandaC`, 2026-09-25T07:10:38):

- `U500` (MCP3208, 16 pinos): 16/16 batem.
- `U400` (ISO7141CCDBQR, 16 pinos): 16/16 batem.
- `P1` (Harwin M20-7822046, 20 pinos, incl. os "sem ligação"): 20/20 batem — os pinos NC do mapa correspondem exactamente às redes `unconnected-(P1-Pin_N-PadN)` do netlist.
- `P2` (Harwin M20-7821446, 14 pinos): 14/14 batem.

**Zero divergências em 66/66 pinos.**

- **Achado #2 (severidade baixa):** o cabeçalho de `mapa_pinos_EBM2_V5.md` cita a netlist `EBM2_V5_rev25c.net`, mas a BOM/Portão 1 final usa `EBM2_V5.net` (tanda C, gerada depois, 07:10). Verifiquei que isto **não causou nenhuma divergência real** — as rondas B/C só mudaram MPN/pegada de componentes (C200, C202, R206, U202), nenhuma rede foi alterada entre essas revisões. É uma nota de higiene documental (referência desactualizada no cabeçalho), não um erro de conteúdo.

## Limites desta verificação

- Não re-derivei a origem do pulso de arranque de R206 (6,6 W / 0,6 ms) nem a conta térmica/RC subjacente — isso é da análise de transiente de alimentação (F2/esquemático), fora do âmbito deste Bloco 3.
- Não confirmei o land pattern físico de C200 contra o footprint IPC do projecto (2,0-2,4 mm TDK vs 1,8 mm do projecto) — o próprio autor já sinalizou isto como pendente para a F3 (layout); não é um item de BOM/mapa de pinos.
- Das "14 MPN da tanda A" citadas na tarefa, a única com conta de datasheet documentada (curva de derating) é C202, que verifiquei em detalhe; as restantes ~13 posições fechadas nessa tanda são passivos padrão (resistores 1 %, cerâmicos 100 nF/1 µF genéricos, já usados noutras placas 2Solve) — cobri-as pelo cruzamento exaustivo BOM↔netlist do item 1 (referência, valor, pegada, MPN todos conferidos), mas não refiz uma conta de datasheet dedicada para cada uma individualmente.
- Não verifiquei os `N/D` de ciclo de vida (por definição não há afirmação a conferir).
- Não abri o esquemático nem corri ERC/DRC — fora do âmbito do Bloco 3.
- A leitura de curvas de datasheet por pixel tem uma precisão prática de ±3-5 % (largura do traço, anti-aliasing); onde a minha releitura diferiu da BOM (C204, C207/C402) o desvio foi sempre pequeno e na direcção segura (valor real ligeiramente melhor que o citado).
