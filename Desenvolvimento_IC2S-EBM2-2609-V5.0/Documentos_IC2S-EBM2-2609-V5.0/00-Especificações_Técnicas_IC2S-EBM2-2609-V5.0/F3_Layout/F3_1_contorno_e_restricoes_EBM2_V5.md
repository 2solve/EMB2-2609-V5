# F3 · 3.0 recebimento e 3.1 contorno — IC2S Extension Board EBM2 V5 (6AI)

| | |
|---|---|
| Data | 2026-09-25 |
| Skill | `2shw-pcb:layout`, etapas 3.0 e 3.1 |
| Entrada | Esquemático aprovado no Portão 1 (`Documentos/portao1_aprovado_2026-09-25/`) |
| Saída | `KiCad_EBM2_V5/IC2S_Extension_Board-EBM2_V5.kicad_pcb` (gerado por `ferramentas/gera_pcb_F3.py`) |
| Estado | **3.0 fechada · 3.1 à espera da conferência do projectista** |

## 3.0 — Conferência de recebimento

| Confere | Como | Resultado |
|---|---|---|
| Igual ao aprovado | `confere_recebimento_F3.py`: netlist de agora contra a do pacote congelado | **Igual**: 139 componentes, 99 redes, valor, pegada e MPN |
| ERC | `kicad-cli sch erc` | **0 erros** (os 274 avisos são de ambiente: o `kicad-cli` não resolve a tabela global aninhada «KiCad»; os da biblioteca do projecto foram a zero na tanda P1-R) |
| Hierarquia | `gera_pdf_F2.py` | 8 SVG = raiz + 7 folhas |
| Designadores | regra `#?[A-Za-z_]+\d+` | todos válidos |
| Pegadas | fp-lib-table + `.kicad_mod` | 139/139 com pegada existente na biblioteca `EBM2_V5` |
| Pinos × pads | cada pino da netlist tem pad, cada pad eléctrico tem pino | 139/139 sem diferença |
| Fidelidade à intenção | `verifica_F2.py` | tudo confere com a intenção rev. 2.5 |

A conferência foi **sabotada** para provar que reprova: um valor trocado (`R28` 4k7 → 4k8) e um pino sem pad
(`U7` pino `VDD`) — ambos detectados, saída 1.

## 3.1 — Contorno e restrições duras (RC1: idênticos aos Gerbers da V4.1, tolerância 0,1 mm)

Fontes: (1) **Gerbers de origem da V4.1** (CircuitStudio, pasta `Outputs`, cópia em `Documentos/F3/gerber_V41/`);
(2) a V4.1 convertida para KiCad e auditada (`C:\hw\hw-ebm2-v4.1`, só leitura; 139/139 furos e IoU 99,69 %
contra os mesmos Gerbers). As duas fontes foram cruzadas por `confere_mecanica_gerber_V41.py` (sabotado: um furo
deslocado 0,15 mm é reprovado).

| # | Restrição | Valor | Gerber × convertida | Na V5 |
|---|---|---|---|---|
| 1 | Contorno | **60,000 × 60,000 mm**, rectângulo sem raios nem recortes (Outline: 2,36221 in) | 60,0001 × 60,0001 · 60,0000 × 60,0000 | Edge.Cuts 0,1 mm nas mesmas coordenadas (118,5011; 75,0036)-(178,5011; 135,0036) |
| 2 | Furo de fixação H1 | Ø 3,2 mm metalizado, pad 6,0 mm, sem rede (TXT, ferramenta T6) | desvio 0,0004 mm | (126,501; 131,004), bloqueado, `board_only` |
| 3 | Furo de fixação H2 | idem | desvio 0,0006 mm | (170,501; 79,004), bloqueado, `board_only` |
| 4 | `P1` 20 pinos (base board) | face **inferior**, passo 2,54 mm, furo 0,9, pad 1,5 mm | pior pad 0,0001 mm | cada pad sobre o homónimo da V4.1: **0,0000 mm**; rot. −90°; bloqueado |
| 5 | `P2` 14 pinos (campo) | face **inferior**, idem; a 56,007 mm de `P1` | pior pad 0,0001 mm | **0,0000 mm**; rot. −90°; bloqueado |
| 6 | LED `D1` (entrada) — `V11` | posição da V4.1 `D25` (152,636; 120,808), rot. 90°, face superior | — | desvio 0,0000 mm; bloqueado |
| 7 | LED `D5` (+5V_ADC) — `V11` | posição da V4.1 `D18` (140,165; 120,808) | — | idem |
| 8 | LED `D24` (laços) — `V11` | posição da V4.1 `D19` (164,422; 120,808) | — | idem |

Copiado da V4.1 sem ser restrição dura: **fiduciais** `FID1`-`FID3` nas posições da V4.1 (121,394; 133,127),
(133,459; 77,501), (176,639; 116,693).

**Empilhamento:** 4 camadas como a V4.1 (Top / Ground / Power / Bottom, relatório de Gerbers). A V4.1 não
declara espessura; adoptado o da placa irmã **EBM7 V2.3**: 1,6 mm, cobre externo 35 µm, **interno 17,5 µm**,
prepreg 0,21 mm, núcleo 1,065 mm, FR4, acabamento ENIG. O cobre interno de meia onça entra na conta do `V1`
(retorno dos laços < 5 mΩ).

## Conferência cruzada (servidor MCP do KiCad)

| Porta | Resultado | Leitura |
|---|---|---|
| DRC com paridade de esquemático (`kicad-cli`) | **0 problemas de paridade**; 289 desligados (nada roteado); 5 avisos de serigrafia no bordo (textos de `P1`/`P2`, a arrumar na 3.2) | ok |
| `pcb_stackup_consistency_gate` | PASS (4 camadas na tabela e no empilhamento) | ok depois de copiar o empilhamento |
| `pcb_transfer_quality_gate` | FAIL, 29 «pad-net mismatches» | **Falso positivo, conferido pad a pad**: os 388 pads da placa têm exactamente a rede da netlist do KiCad; os 29 são pinos sem ligação, a que o próprio KiCad dá a rede `unconnected-(…)`, e a ferramenta espera «sem rede» |
| `validate_footprints_vs_schematic` | FAIL: `H1`, `H2` sem símbolo | **Intencional**: furos só de placa (`board_only`), como na V4.1 |

## Para a 3.2

- O resto das pegadas está **fora da placa**, em grelha à direita.
- O valor dos três LED sai na serigrafia (texto longo do MPN): esconder na 3.2.
- Pendentes que chegam à 3.2/3.3: land pattern do `C1` 1210 (TDK PA 2,0-2,4 mm contra 1,8 mm da pegada IPC);
  cobre nos `U8`-`U13`; `V1` < 5 mΩ; `V13`/`V14` continuam a pedir o painel.
