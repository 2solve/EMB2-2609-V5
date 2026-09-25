# Pacote da etapa 2.3b — verificação de aplicação · EBM2 V5 (6AI 4-20 mA)

Data: 2026-09-24. Esquemático: `C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\` (intenção rev. 2.3, pinagem
conferida na 2.3 sem divergências).

## Regras (skill `2shw-pcb:verificar-aplicacao-datasheet`)

- **Quem desenhou não valida.** Sessão nova, **modelo diferente** do autor (Claude Opus 5.5), sem
  o histórico da conversa de autoria. Sugestão: Claude Sonnet 5 ou Claude Fable 5.1.
- **Cada fórmula e cada nota de rodapé** da secção de aplicação de cada CI crítico vira uma linha,
  avaliada com os valores da BOM. Se faltar um valor, a linha diz `missing data`.
- **Citar por pesquisa no PDF, nunca de memória**, com a página. **Texto E figura**
  (`grep_datasheet.py --render N`).
- **Herdado ≠ verificado.** Valores vindos da V4.1 ou da EBM7 entram marcados `[INHERITED]` e
  re-derivam-se contra este circuito.
- **O datasheet é portão, não opção.** Se um limite do datasheet choca com compatibilidade ou
  herança, ganha o limite.
- **A tabela gera-se por avaliação** (`tabela.py rows.json`), não escrevendo vereditos à mão.
- **Só leitura** no projecto KiCad.

## Envelope de operação (escopo, `RA1` e `RB1`)

- **Alimentação:** 18 a 32 V (rede, bateria ou painel solar). **Arranque e dissipação a 32 V;
  tensão ao transmissor a 18 V.**
- **Temperatura:** 0 a +65 °C certificado, **dimensionar a +70 °C**.
- **Laços:** 4-20 mA; alarme NAMUR NE43 ≥ 21 mA; o ADC satura a 22,7 mA; transmissor em curto
  limitado pelo `U60x`.

## O que está na pasta

| Ficheiro | Para quê |
|---|---|
| `EBM2_V5.net` | Netlist (kicadsexpr) com `Value` e `MPN` de cada peça |
| `esquematico_EBM2_V5.pdf` | As 8 folhas |
| `intencao_EBM2_V5.md` | Especificação e o porquê de cada decisão. **As contas lá escritas são afirmações a conferir**, não verdade |
| `escopo_EBM2_V5.md` | Requisitos e critérios de aceite (`RA`, `RE`, `RM`, `RB`, `RC`) |
| `datasheets/` | 18 PDF escolhidos pelo conteúdo; `LISTA.md` com md5 |

Scripts da skill: `C:\Users\Javier Rivadineira\.claude\marketplaces\hardware-claude-plugins\2shw-pcb\skills\verificar-aplicacao-datasheet\scripts\`
(`grep_datasheet.py`, `bom_values.py`, `tabela.py`).

## Âmbito — CI e peças críticas

| Ref | Peça | O que a secção de aplicação costuma pedir (para não esquecer; o datasheet manda) |
|---|---|---|
| `U200` | TPS7A4001 | Condensadores de entrada/saída e estabilidade, divisor de realimentação, `EN`, dissipação a 32 V, ilha térmica |
| `U201` | SPX3819 | Condensadores, `BP`, `EN`, queda a partir do `+5V_ADC` |
| `U202` | ADR4525 | Condensadores (entrada/saída), carga total (inclui o divisor do NTC), queda a partir de `3V3_REF` |
| `U203` | TL431 | Gama de corrente de cátodo, divisor, **estabilidade com a capacidade ligada ao cátodo** |
| `U400` | ISO7141 | Desacoplamento, `EN`, níveis de entrada/saída contra o SPI a 3,3 V |
| `U401` | MCP1824S | Condensadores, gama de entrada contra o `+5V` do barramento (e os seus transitórios) |
| `U500` | MCP3208 | `VREF`, impedância de fonte (fig. 4-2), relógio mínimo (§6.2; o firmware usa 20 kHz), desacoplamento, gama de entrada contra os clamps |
| `U601`-`U606` | AL5809-25 | Tensão mínima de funcionamento, dissipação/térmica no curto, inversão (−0,3 V) com o `BAT46W` em paralelo |
| `D200` | SMA6J33A-Q | Standoff contra 32 V, grampo contra o máximo absoluto das peças a jusante |
| `D601`-`D616` | 824520361 | Standoff contra o trilho, grampo contra `U60x`/`D64x`/fusíveis |
| `D621`-`D626` | BAV199 | Corrente de clamp em falha e em transitório, fuga |
| `D641`-`D646` | BAT46W-7-F | Tensão directa na corrente de falha inversa; tensão inversa no curto |
| `D201`, `D202` | MBR1H100SF | Tensão inversa contra o grampo, corrente de arranque |
| `F201`, `F202`, `F601`-`F606` | CC12H / 3413.0002.22 | I²t de fusão contra o arranque a 32 V (`RA2` ≥ 10×), abertura em curto à massa, tensão nominal |
| `R700`/`R701`/`C700` | NTC e divisor | Impedância de fonte contra a fig. 4-2 do MCP3208 de 0 a 70 °C (o software actual **não lê** o CH4) |

**Teste de uma multiplicação** (obrigatório): cada canal a 4, 20 e 22,7 mA e em curto; a cadeia de
alimentação a 18, 24 e 32 V; o NTC a 0, 25 e 70 °C.

## Itens abertos que o autor deixou (conferir ou refutar, não assumir)

`V7` (qual TVS conduz primeiro num surto), `V9` (tensão ao transmissor a 18 V), `V10` (clamps em
transitório), `V13` (`+5V_IC` contra o `MCP1824`), o resíduo de −0,4 V sobre o `AL5809` em inversão, e
os MPN em falta de `C200` (`V6`) e `R206` (`V5`). Ver a tabela de verificações da intenção.

## Saída pedida

`C:\hw\hw-ebm2-v5\Documentos\verificacao_2_3b\verificacao_aplicacao_EBM2_V5.md`, com:

1. a lista de CI críticos e os PDF usados (ficheiro, revisão, páginas);
2. a tabela (gerada por `tabela.py`): `IC | secção/tabela/nota, pág. | fórmula literal | valores da BOM | resultado | pass / FAIL / missing data`;
3. o teste de uma multiplicação por cadeia analógica;
4. «O que nenhuma ferramenta viu» — o que ERC, DRC, analisador e SPICE não detectam aqui;
5. os limites da própria revisão.

## Mensagem para colar na sessão nova

> Faz a etapa 2.3b (verificação de aplicação) do esquemático EBM2 V5 com a skill
> `2shw-pcb:verificar-aplicacao-datasheet`. Lê primeiro
> `C:\hw\hw-ebm2-v5\Documentos\verificacao_2_3b\LEIA-ME_2.3b.md` e usa o material dessa pasta (o
> projecto KiCad pode ser lido, nunca editado). Avalia cada fórmula e cada nota de rodapé da secção
> de aplicação de cada CI crítico com os valores da BOM, gera a tabela com `tabela.py` e escreve
> `verificacao_aplicacao_EBM2_V5.md` na mesma pasta. As contas da intenção são afirmações a
> conferir: o objectivo é encontrar o que não cumpre.
