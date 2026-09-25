# Pacote da etapa 2.3b (3.ª corrida) — verificação de aplicação · EBM2 V5 rev. 2.5b

Data: 2026-09-24. Esquemático: `C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\` (intenção **rev. 2.5b**, §17). A 2.ª corrida
(rev. 2.4) está em `rev24_anterior/`: 174 linhas, 16 FAIL, mais um recálculo independente. A rev. 2.5 corrigiu
parte dessas FAIL; o objectivo desta corrida é **conferir as correcções e o que elas mexeram**, e re-avaliar o
resto.

## Regras (skill `2shw-pcb:verificar-aplicacao-datasheet`)

- **Quem desenhou não valida.** O autor é o Claude Opus 5.5; esta verificação corre noutro modelo, sem o
  histórico da conversa de autoria.
- **Cada fórmula e cada nota de rodapé** da secção de aplicação de cada CI crítico vira uma linha, avaliada com
  os valores da BOM (`EBM2_V5.net`). Falta um valor → `missing data`. Nunca supor.
- **Citar por pesquisa no PDF, com página. Texto E figura** quando o número vem de um gráfico.
- **As contas da §17 da intenção são afirmações a conferir**, não verdade. O autor já errou dois números nesta
  revisão (uma tolerância do TL431 de memória, um R206 que teve de subir de 47 para 68 Ω).
- **A tabela gera-se por avaliação** (`tabela.py rows.json`), não à mão. **Só leitura** fora desta pasta.

## Envelope

18–32 V (rede, bateria ou solar); 0 a +65 °C certificado, **dimensionar a +70 °C**; laços 4-20 mA, NAMUR ≥ 21 mA,
ADC satura a 22,7 mA; transmissor em curto, ligação invertida e falha dupla (protector em curto + 30 V
injectados). Critérios no `escopo_EBM2_V5.md` (`RA2` ≥ 10× I²t, `RA3`, `RA4` 3V3_REF ≤ 3,7 V com 30 V injectados).

## Âmbito — prioridade ao que mudou na rev. 2.5b

| Ref | Mudança | Pontos mínimos |
|---|---|---|
| `R206` | 33 → 68 Ω | `RA2` do `F201` a 32 V com toda a capacidade a jusante (inclui `C204` 10 µF e `C207` 2,2 µF); arranque a 18 V; energia e pico por arranque |
| `U201` | SPX3819 → `MCP1824T-3302E/OT` | Pinagem SOT-23-5 fixa (pino 4 = PWRGD sem ligação, `SHDN` por `R203`); gama de entrada contra `+5V_ADC`; condensadores (mín. e máx. recomendado); tolerância de saída |
| `C204` | 2,2 → 10 µF TDK `C3216X5R1H106K160AB` | Capacidade efectiva a 3,3 V (curva TDK) contra a estabilidade do TL431 (fig. 6-18) e contra o máximo do MCP1824 |
| `R204` | 4k42 → 4k12 | Nível do grampo TL431**BQ** (tabela 6.13) em todos os extremos, contra `RA4` e contra a saída máx. do MCP1824 |
| `C207`, `C402` | 1 → 2,2 µF | ADR4525 e MCP1824 |
| `C209`, `C645` | novos, 10 nF OUT–FB | TPS7A4001 §8.2.2.3 e nota 4; efeito no arranque/estabilidade |
| `C644` | novo, 10 µF em paralelo com `C642` | Capacidade efectiva a 12,6 V contra > 4,7 µF do TPS7A4001 |
| `R661`-`R666` | novas, 4k7 entre o filtro e o pino do ADC | Excursão e corrente no pino do MCP3208 em curto (V10); efeito na amostragem (fig. 4-2) e na fuga |
| resto | — | Re-avaliar as 16 FAIL da 2.ª corrida: continuam, mudaram ou já não se aplicam |

**Teste de uma multiplicação** (obrigatório): cada canal a 4, 20, 22,7 mA e em curto; a cadeia a 18, 24 e 32 V;
`3V3_REF` e `+12V_TPS` nos extremos de tolerância.

## Saída pedida

Nesta pasta: `verificacao_aplicacao_EBM2_V5_rev25.md` e `verificacao_aplicacao_EBM2_V5_rev25_rows.json`, com: CI e
PDF usados (página); a tabela de `tabela.py`; o teste de uma multiplicação; «o que nenhuma ferramenta viu»; os
limites da revisão. Em **português**.
