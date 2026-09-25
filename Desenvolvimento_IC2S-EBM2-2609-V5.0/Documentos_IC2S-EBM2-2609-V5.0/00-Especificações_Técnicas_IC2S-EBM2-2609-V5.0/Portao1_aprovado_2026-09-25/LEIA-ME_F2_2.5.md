# F2 · etapa 2.5 — PDF para a revisão humana · EBM2 V5

| | |
|---|---|
| Data | 2026-09-25 |
| Estado do esquemático | Intenção **rev. 2.5c** + correcções de texto (§3) + tandas A, B e C da BOM (§17 linha 11: MPN, pegadas do C202 e do C200, porto da folha 01); netlist `EBM2_V5_bom_tandaC.net`, **mesmas redes** que a rev. 2.5c |
| Entregável | **`EBM2_V5_F2_revisao_2026-09-25.pdf`** (12 págs., md5 `f8a838d4ff9c`, regenerado depois da tanda C) — é este que vai à mesa e ao Portão 1 |
| Gerado por | `ferramentas/gera_pdf_F2.py` (reprodutível; recusa entregar se uma porta falhar) |
| Skill | `2shw-pcb:esquematico`, etapa 2.5 |

## 1 · Conteúdo do PDF (com marcadores por folha)

| Págs. | Conteúdo | Origem |
|---|---|---|
| 1-8 | Esquemático, 8 folhas (raiz + 7), bloco de título preenchido em cada uma; folha 06 em A3 | `kicad-cli sch export pdf` (o próprio KiCad, não um gerador) |
| 9 | Diagrama de blocos (2.1), **revisão B** — actualizado nesta etapa (TPS26613, +12V_TPS, MCP1824, R206 150 Ω, grampo 3,52 V) | `ferramentas/gera_diagrama_blocos.py` (guardas G1-G8) |
| 10-12 | Mapa de pinos (2.4): U500, U400, P1, P2 + regras para o firmware | `ferramentas/gera_mapa_pinos.py` (rede lida da netlist, cotejada com a intenção) |

Na pasta ficam também `esquematico_EBM2_V5.pdf` (só o KiCad), `svg/` (preto e branco) e `png/` (3200 px).

## 2 · Portas

| Porta | Resultado |
|---|---|
| SVG da hierarquia = N + 1 | **8** ficheiros (raiz + 7 filhas): árvore hierárquica válida |
| Páginas do esquemático | 8, cada uma com «IC2S Extension Board EBM2 V5» e «Folha n de 8» no bloco |
| Sobreposições de texto (`mede_solape_pdf.py`) | **0** nas 8 páginas (160 a 1091 textos por página) |
| ERC (`kicad-cli`, erros) | **0** |
| `verifica_F2.py` (netlist contra as tabelas da intenção) | tudo confere |
| Netlist antes/depois das correcções de texto | idêntica |
| Consolidado | 12 págs. = 8 + 1 + 3 |
| **Inspecção ampliada** (obrigatória) | Feita: as 8 folhas em quadrantes a partir do SVG, mais o diagrama e o mapa. Resultados em §3 |

## 3 · O que a inspecção ampliada encontrou

**Nenhum defeito de ligação ou de polaridade.** Encontrou texto desactualizado e **um dado errado**:

| # | Onde | Achado | Acção |
|---|---|---|---|
| 1 | Folha 02, nota 1 (e `planejamento` l. 64/68, `escopo` D5/D6) | **Grampo do D200 escrito como 58,1 V** (é o SMA6J36A). O SMA6J33A grampeia a **53,3 V @ 11,3 A** (Bourns pág. 2, texto e imagem da tabela). A nota acusava a EBM7 Legacy de erro — a Legacy estava certa | Corrigido. Erro conservador: **nenhuma decisão muda** (MBR1H100SF de 100 V fica a 46,7 V de margem; o bulk de 50 V da V4.1 continua abaixo do grampo) |
| 2 | Folha 03, nota 1 | Dissipação do U200 calculada a 24 V | Refeita a 32 V: 0,18 W, +12 °C |
| 3 | Folha 03, nota 7 | «TL431 a 3,6 V» | 3,52 V (rev. 2.5b) |
| 4 | Folha 04, nota 3 | C402 «1 uF» | 2,2 µF (rev. 2.5) |
| 5 | Folha 06, cabeçalho e bloco de título | Citavam a rev. 2.4 | rev. 2.5c |
| 6 | Folha 07, nota 2 e descrição do C700 | Impedância do nó a −40 °C (fora do envelope `RB1`) | 1,6-4,7 kΩ de 70 a 0 °C (B25/85 **3435 K**, NTCS0603E3103\*LT, Vishay pág. 1, texto e imagem) |
| 7 | 8 folhas | Data do bloco 2026-09-23 | 2026-09-25 (só metadados) |
| 8 | Diagrama de blocos | Mostrava SPX3819, R206 22 Ω, cadeia sem TPS26613, sem +12V_TPS | Revisão B |
| 9 | Intenção §8, restrição 6 | «Curto dá 4095» (era do AL5809) | Com o TPS26613 a leitura alterna 4095 / ~0 mA |
| 10 | `planejamento` §5 | «O TPS7A4001 tem arranque suave próprio» — não existe no SBVS162B | Riscado e corrigido |
| **11** | **Folha 01 (congelada, arrumada pelo projectista)** | O triângulo de massa (DGND) do `P1.12` fica **em cima do no-connect do `P1.13` e toca o texto «ID3»**. Eléctrico correcto (netlist: P1.12 = DGND, P1.13 sem ligação); só leitura. O medidor de sobreposições **não o vê** (compara texto com texto, não símbolo com texto) | **Corrigido na tanda B (2026-09-25), a pedido do projectista:** o porto DGND do P1.12 foi para x = 78,74 no mesmo fio e o texto do ID3 voltou ao alinhamento das outras linhas. Nota: com o porto encostado ao pino, o PDF do KiCad desenhava os textos do P1 e o «DGND» **duas vezes** no mesmo sítio (335 → 312 palavras na pág. 2 depois da correcção; nenhum texto se perdeu) |

Correcções aplicadas com `ferramentas/aplica_textos_F2_25c.py` (backups `.antes_textos25c`), repetidas no gerador
(`gera_folhas_F2.py`, `construtor.py`) e conferidas: o gerador regenera as folhas 04, 06 e 07 com textos idênticos.

## 4 · O que este PDF não prova

- **Nada do dimensionamento.** As portas acima provam que o desenho é o da intenção e que se lê; os valores foram
  verificados na 2.3b (três corridas independentes: `verificacao_2_3b/`, `_rev24/`, `_rev25/`).
- **Sobreposição símbolo × texto** não é medida automaticamente (achado 11): só a inspecção a vê.
- O PDF é do esquemático; pegadas, layout e EMC são da F3.

## 5 · Em aberto para o Portão 1

| Item | Estado |
|---|---|
| MPN | **Todos fechados** (C200 na tanda C: TDK C3225X7R2A225K230AB, 1210) |
| `V13` — +5V_IC da base board (grampo 9,2 V) contra 6,5 V do `U401` | Medir o barramento num painel |
| `V14` — referências do SPI na base board; **MISO sempre activo** (ISO7141 EN1 fixo, herdado da V4.1/Legacy): contenção se o MISO for partilhado | Confirmar na cablagem de um painel |
| Pino do MCP3208 em curto (~30-50 µA de injecção com `R66x`) | Ensaio T26 e consulta à Microchip |
| `R206` como elemento fusível num curto de `+24V_REG` | Aceite e documentado; confirmar no T26 |
| Folha 01, achado 11 | **Fechado** na tanda B |
