# Portão 1 — registo de aprovação · IC2S Extension Board EBM2 V5 (6AI)

| | |
|---|---|
| Portão | **P1** (skill `2shw-pcb:fluxo`): diagrama de blocos, esquemático com ERC limpo + intenção, BOM preliminar e mapa de pinos |
| Veredicto | **APROVADO** |
| Projectista | Javier Rivadineira — «aprobado portao 1», 2026-09-25 10:01 |
| Verificação cruzada | 3 sessões independentes (Claude Sonnet, modelo ≠ autor Opus 5.5), uma por bloco: bloco 1 aprovado com ressalvas · bloco 2 aprovado com ressalvas · bloco 3 aprovado · **0 bloqueantes** |
| Ressalvas | Todas tratadas na tanda **P1-R** (2026-09-25), antes da aprovação: rótulos de rede do diagrama, biblioteca de símbolos própria, intenção §5/§9, grau W do `ADR4525` documentado, descrição do `TPS26613` |

Esta pasta é uma **cópia congelada** do pacote aprovado. Não se edita; `Documentos/portao1/` continua a ser
regenerado por `ferramentas/prepara_pacote_portao1.py`. Qualquer alteração ao esquemático depois desta data é
uma tanda nova, com revisão independente própria.

## Artefactos aprovados (md5, 12 primeiros caracteres)

| Ficheiro | md5 |
|---|---|
| `EBM2_V5_F2_revisao_2026-09-25.pdf` (12 págs.: 8 folhas + diagrama + mapa de pinos) | `469fffd0e6da` |
| `EBM2_V5.net` (netlist kicadsexpr exportada pelo `kicad-cli`) | `19fa4fbbb692` |
| `erc.json` (0 erros) | `5850952abc06` |
| `bom_preliminar_EBM2_V5.md` / `.csv` (43 linhas, 126 montados, 0 sem MPN) | `e01b74742a1b` / `f38120f58c5d` |
| `intencao_EBM2_V5.md` | `20bf6668aabb` |
| `mapa_pinos_EBM2_V5.md` (66 pinos, 0 divergências) | `7109eedf075d` |
| `diagrama_blocos_EBM2_V5.svg` | `a95b8c24828f` |
| `tabela_correspondencia_refs_EBM2_V5.csv` (renumeração de 2026-09-25) | `71a911a11bb6` |
| `relatorio_P1_bloco1_diagrama.md` · `bloco2_esquematico` · `bloco3_bom_pinos` | `c9cbba26c358` · `7c40736f1001` · `5faeae552778` |

Os três relatórios da verificação cruzada usam a **numeração antiga** (R206, U601…), anterior à renumeração;
traduzir por `tabela_correspondencia_refs_EBM2_V5.md`.

## O que a aprovação liberta

1. **BOM preliminar a Suprimentos** para conferência de estoque e **compra antecipada** (o Hardware não compra):
   - `ISO7141CCDBQ` / `DBQR` (U6) — 0 em stock na Mouser em todas as variantes (2026-09-25);
   - `ADR4525WBRZ-R7` (U2) — família «Restricted Availability»; pedir à ADI, com a compra, a confirmação de que o
     WBRZ cumpre a tabela 2 do grau B;
   - Schurter `3413.0002.11` (F3-F8; a `.22` tem prazo de 269 dias);
   - Würth `824520361` (D12-D17; 82 em stock) e LED por `Q65113A7469`.
2. **F3 — layout** (`2shw-pcb:layout`), contorno primeiro.

## Em aberto que não bloqueou (sobe para a F3 ou para a bancada)

- `V13` (+5V_IC da base board, TVS D53 de 9,2 V contra 6,5 V abs max do MCP1824) e `V14` (SPI e MISO sempre
  activo) — precisam do painel.
- Ensaios `T26` / `T27`; consulta à Microchip sobre a corrente de injecção do `MCP3208`.
- F3: land pattern TDK do `C1` 1210 (PA 2,0-2,4 mm) contra a pegada IPC do projecto (1,8 mm); cobre no `U8`-`U13`.
