# Pacote da etapa 2.3b (2.ª corrida) — verificação de aplicação · EBM2 V5 rev. 2.4

Data: 2026-09-24. Esquemático: `C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\` (intenção **rev. 2.4**). A primeira
corrida da 2.3b está em `..\verificacao_2_3b\` (132 linhas, 17 FAIL). Depois dela mudou a folha 06: o
limitador `AL5809` + `BAT46W` foi substituído pelo protector `TPS26613` e entrou o trilho `+12V_TPS`
(`U640`), copiados da EBM7 V2.3 Legacy com três desvios justificados na intenção §9.

## Regras (skill `2shw-pcb:verificar-aplicacao-datasheet`)

- **Quem desenhou não valida.** O autor é o Claude Opus 5.5; esta verificação corre noutro modelo, sem
  o histórico da conversa de autoria.
- **Cada fórmula e cada nota de rodapé** da secção de aplicação de cada CI crítico vira uma linha,
  avaliada com os valores da BOM (`EBM2_V5.net`). Se faltar um valor, `missing data`. Nunca supor.
- **Citar por pesquisa no PDF, com página. Texto E figura** (`grep_datasheet.py --render N`).
- **Herdado ≠ verificado.** O que vem da EBM7 Legacy entra `[INHERITED]` e re-deriva-se contra este
  circuito (a Legacy tem burden, trilho e envelope próprios).
- **O datasheet é portão.** Se um limite choca com a herança, ganha o limite.
- **A tabela gera-se por avaliação** (`tabela.py rows.json`), não à mão.
- **Só leitura** no projecto KiCad e nos documentos fora desta pasta.

## Envelope de operação

- **Alimentação:** 18 a 32 V (rede, bateria ou painel solar). Arranque e dissipação a 32 V; tensão ao
  transmissor a 18 V.
- **Temperatura:** 0 a +65 °C certificado, **dimensionar a +70 °C**.
- **Laços:** 4-20 mA; alarme NAMUR NE43 ≥ 21 mA; ADC satura a 22,7 mA; transmissor em curto e ligação
  invertida têm de ficar dentro dos máximos absolutos de todas as peças do caminho.
- Critérios de aceite no `escopo_EBM2_V5.md` (`RA2` ≥ 10× de margem de I²t no arranque, `RA3` grampo
  abaixo do menor máximo absoluto a jusante, etc.).

## O que está na pasta

| Ficheiro | Para quê |
|---|---|
| `EBM2_V5.net` | Netlist rev. 2.4 (kicadsexpr) com `Value` e `MPN` |
| `esquematico_EBM2_V5.pdf` | As 8 folhas (a 06 em A3) |
| `intencao_EBM2_V5.md` | Especificação e porquê. **As contas escritas são afirmações a conferir** |
| `escopo_EBM2_V5.md`, `planejamento_pcb_EBM2_V5.md` | Requisitos e o dimensionamento da F1 |
| `datasheets/` | 17 PDF escolhidos pelo conteúdo; `LISTA.md` com md5 e o que **falta** |

Scripts da skill: `C:\Users\Javier Rivadineira\.claude\marketplaces\hardware-claude-plugins\2shw-pcb\skills\verificar-aplicacao-datasheet\scripts\`.

## Âmbito

Todos os CI e peças críticas, com **prioridade** ao que mudou na rev. 2.4:

| Ref | Peça | Pontos mínimos (o datasheet manda) |
|---|---|---|
| `U601`-`U606` | TPS26613DDFR | `+Vs` contra `VOUT_OVLO`; divisor `VSNS` (tabela 8-2, notas 1 e 2) com `I(OL)` mín/máx; `MODE`; dissipação e temperatura em curto a 32 V/70 °C com os temporizadores e a fig. 7-19; inversão; `IN`/`OUT` contra o grampo do TVS; queda ao transmissor; `SGOOD` |
| `U640` | TPS7A4001 | Divisor de realimentação e tolerância da saída; condensadores de entrada e saída com polarização e temperatura; dissipação a 32 V; `EN` |
| `D601`-`D606` | SMBJ33A-13-F | Standoff contra o retorno em curto; grampo contra `IN` do TPS26613 (sem datasheet: dizê-lo) |
| `R601`-`R606`, `R611`-`R616` | 0 Ω e burden | Potência no limite de corrente, em pico e em média |
| `F202` | CC12H750mA | `RA2` com toda a capacidade nova ligada a `+24V_ADC` e a carga de `C642` pelo limite do `U640` |
| O resto | como na 1.ª corrida | Re-avaliar as 17 FAIL da 1.ª corrida: continuam, mudaram ou deixaram de se aplicar |

**Teste de uma multiplicação** (obrigatório): cada canal a 4, 20 e 22,7 mA e em curto; a cadeia a 18,
24 e 32 V; o `+12V_TPS` nos extremos de tolerância.

## Saída pedida

Nesta pasta: `verificacao_aplicacao_EBM2_V5_rev24.md` e `verificacao_aplicacao_EBM2_V5_rev24_rows.json`,
com: CI e PDF usados (página); a tabela gerada por `tabela.py`; o teste de uma multiplicação; «o que
nenhuma ferramenta viu»; os limites da revisão. Em **português**.
