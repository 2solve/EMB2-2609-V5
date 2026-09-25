# Portão 1 — lista do projectista (revisão com o PDF impresso) · EBM2 V5

Imprimir `EBM2_V5_F2_revisao_2026-09-25.pdf` (a folha 06 é **A3**). Caneta vermelha. Marcar cada linha.

## Bloco 1 — diagrama de blocos (pág. 9)

- [ ] As caixas e os trilhos correspondem ao que a placa tem de ser (6 laços, isolador, ADC, alimentação).
- [ ] A barreira funcional está no sítio certo: só o `U6` a atravessa.

## Bloco 2 — esquemático (págs. 1-8) e intenção

- [ ] **Pinagem congelada de `P1` e `P2`** igual à V4.1 (`RC2`): nenhum pino mudou de função.
- [ ] **Mapa de canais do ADC** igual à V4.1: laço 1-4 = CH0-CH3, laço 5-6 = CH6-CH7, CH4 = NTC, CH5 = 4095.
- [ ] **Polaridade** de cada díodo, TVS e LED (ampliar): D2, D3, D4, D1/D5/D24, D6-D17, D18-D23.
- [ ] Folha 06: `U8`-`U13` TPS26613 com `IN` no retorno e `OUT` para o burden; `+12V_TPS` do `U14`.
- [ ] Folha 03: `U4` MCP1824 (pino 4 PWRGD sem ligação); grampo `TL431` com `R8` 4k12.
- [ ] Folha 01: o porto DGND do `P1.12` deslocado (tanda B) e o texto do `ID3` realinhado — conferir que se lê.
- [ ] As notas de decisão de cada folha dizem o mesmo que a intenção (§9, §17).
- [ ] Nada que eu saiba do campo que o esquemático contradiga (transmissores instalados, cablagem do painel).

## Bloco 3 — BOM e mapa de pinos

- [ ] BOM (`bom_preliminar_EBM2_V5.md`): 43 linhas, 126 peças montadas; nada de estranho nas quantidades.
- [ ] Decisões registadas: `U2` = **ADR4525WBRZ-R7** (fechada); `R3` = KOA SG73P2ATTD1500F; `C4` em 1206.
- [ ] Alternativas para compra: fusível `3413.0002.11`, LED `Q65113A7469`, ISO7141 em tubo (`ISO7141CCDBQ`).
- [ ] Mapa de pinos: as regras para o firmware (secção final) estão certas e podem ir ao Rodrigo.

## Em aberto que NÃO bloqueia a assinatura (precisa de painel ou de bancada)

`V13` (+5V_IC da base board), `V14` (SPI e MISO sempre activo), ensaios T26/T27, consulta à Microchip sobre a
corrente de injecção do MCP3208.

## Assinatura

| | Nome | Data | Veredicto |
|---|---|---|---|
| Projectista | Javier Rivadineira | | aprovado / aprovado com ressalvas / reprovado |
| Verificação cruzada | (sessão independente, modelo ≠ Opus 5.5) | | ver `relatorio_verificacao_cruzada_P1_EBM2_V5.md` |

Com o P1 assinado: libertar a compra antecipada — **ISO7141** (0 em stock na Mouser), **ADR4525WBRZ-R7**
(família restrita), fusíveis Schurter — e começar a F3 (`2shw-pcb:layout`).
