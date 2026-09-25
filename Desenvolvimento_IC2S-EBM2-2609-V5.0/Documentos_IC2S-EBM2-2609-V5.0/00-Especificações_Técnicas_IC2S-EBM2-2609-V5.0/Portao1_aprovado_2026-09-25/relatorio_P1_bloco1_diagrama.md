# Portão 1 — verificação independente do BLOCO 1 (diagrama de blocos), EBM2 V5

| | |
|---|---|
| Âmbito | Só o diagrama de blocos (`diagrama_blocos_EBM2_V5.svg`, também pág. 9 do `EBM2_V5_F2_revisao_2026-09-25.pdf`) contra `EBM2_V5.net` e `intencao_EBM2_V5.md` |
| Autor do material | Outro modelo (Claude Opus 5.5) |
| Verificador | Independente, sem participação no F2 |
| Método | SVG e PDF pág. 9 renderizados com PyMuPDF (`fitz`) a 2×, comparados pixel a pixel (idênticos); todo o texto do SVG lido como XML; cada afirmação do diagrama confrontada com `EBM2_V5.net` (grep por `ref`/`net`/`name`) |

## Veredicto do bloco: **APROVADO COM RESSALVAS**

Todas as afirmações verificáveis do diagrama (peças principais, valores, trilhos,
mapa de canais, barreira) batem com a netlist actual, incluindo os valores da
revisão mais recente do próprio dia (2.5c: `R206` 150 Ω, `R204` 4k12). Não há
nada desactualizado nem nenhuma peça ou rede inventada. As ressalvas são de
clareza de rótulo, não de erro eléctrico.

## Achados

| # | Onde | Achado | Evidência | Severidade |
|---|---|---|---|---|
| 1 | Caixas "Alimentacao" e "Seis lacos" | Os rótulos internos usam a tensão genérica ("24 V", "5 V") em vez do nome de rede exacto na entrada de cada regulador | `U200` (`TPS7A4001`, caixa "Alimentacao"): pinos `IN`/`EN` estão na rede `+24V_REG`, não `+24V` (net code 8, `EBM2_V5.net` ~L10413). `U201` (`MCP1824`, mesma caixa): pino `VIN` está em `+5V_ADC`, não `+5V` (net code 4, ~L10137). `U640` (`TPS7A4001`, caixa "Seis lacos", rótulo "+12V_TPS: U640 TPS7A4001 24->12V"): pinos `IN`/`EN` estão em `+24V_ADC`, não `+24V` (net code 7, ~L10336, confirmado nós `U640` pino 5 `EN` e pino 8 `IN`) | Média — é exactamente a confusão que `intencao_EBM2_V5.md` §1.2 já registou como incidente real ("se a folha 01 tivesse um porto `+5V`, as duas redes fundiam-se e a barreira ficava anulada sem mensagem de erro nenhuma"). A netlist em si está correcta (nets `+5V`/`+5V_ADC`/`+24V`/`+24V_ADC`/`+24V_REG` confirmadas distintas, sem merge), mas um diagrama que volta a escrever o rótulo curto reintroduz o mesmo risco de leitura para quem só vê o diagrama |
| 2 | Caixa "P1 Baseboard" e "P2 Campo" | Etiqueta de folha diz "conn" em vez de "01" (a folha 1 é "1 Conectores" na netlist, `Sheetfile` `01_conectores.kicad_sch`, confirmada para `P1`/`P2`) | `EBM2_V5.net`, propriedade `Sheetname`="1 Conectores" nos `comp` de `P1`/`P2` | Baixa — cosmético; inconsistente com a convenção numérica usada nas outras seis caixas (02-07), mas não induz em erro sobre a topologia |
| 3 | Caixa "Seis lacos" | A topologia por canal mostrada ("TVS 33V → TPS26613 → burden 110Ω → 3,3k+100nF → BAV199 → 4,7k") omite o fusível de canal `F60x`, o TVS de trilho `D611`-`D616` (36 V, `SMBJ36A`, no `LOOPk_V+`) e a ilha `R601` (0 Ω) | `intencao_EBM2_V5.md` §9; `EBM2_V5.net` confirma `F601`.. `D611`.. `R601` existentes nas folhas 06, não representados na caixa | Informativo — simplificação aceitável para um diagrama de blocos (o objectivo declarado do diagrama é o fluxo de sinal, não o esquemático completo); não é tratado como defeito |

## O que foi confirmado correcto (evidência)

- **Peças principais**: `U200`/`U640` = `TPS7A4001DGN`; `U201` = `MCP1824T-3302E/OT`; `U202` = `ADR4525WBRZ-R7`; `U203` = `TL431B` (MPN `TL431BQDBZR`); `U400` = `ISO7141CCDBQR`; `U401` = `MCP1824ST-3302E/DB`; `U500` = `MCP3208T-BI/SL`; `U601`-`U606` = `TPS26613DDFR`; `R206` = 150 Ω; TVS de retorno = `SMA6J33A-Q` (entrada) e `SMBJ33A` de 33 V nos laços — todos conferidos por grep directo na netlist.
- **Barreira**: confirmado por varrimento da netlist (nets `DGND` × `GND_ADC`) que **só `U400`** tem pinos nas duas redes de massa — nenhum outro componente atravessa. Bate com o texto do diagrama e com a regra do §3 do documento de intenção.
- **Trilhos**: as 11 redes citadas (`+24V`, `+24V_ADC`, `+24V_REG`, `+5V_ADC`, `+5V`, `3V3_REF`, `+2V5_REF`, `+12V_TPS`, `+3.3V_DIG`, `DGND`, `GND_ADC`) existem todas como redes distintas na netlist, sem fusão — o erro que a rev. 2 corrigiu na folha 03 não voltou.
- **Mapa de canais**: `U500` liga a `+2V5_REF` (VREF), `AIN1..6_ADC` (`CH0,1,2,3,6,7`), `NTC_ADC` (`CH4`) e `3V3_REF` (`CH5`) — exactamente como o diagrama e o §8 do documento de intenção descrevem.
- **`TL431` "grampo 3,52 V"**: valor batido por conta, não só por texto. Netlist confirma a topologia `3V3_REF —R204(4k12)— nó REF —R205(10k)— GND_ADC`, com `REF` no `U203`. Com `V_ref` típico 2,495 V: `2,495 × (1 + 4,12/10) = 3,523 V ≈ 3,52 V`. Bate com a revisão mais recente (2.5b, `R204` 4k12), não com o valor antigo (3,60 V, que usava `R204`=4k42) — prova de que o diagrama foi actualizado no mesmo dia que a última revisão da netlist.
- **Termístor**: `R700` (10k NTC) de `+2V5_REF` a `NTC_ADC`, `R701` (5k62) e `C700` (100 nF, novo) de `NTC_ADC` a `GND_ADC` — confirmado.
- **Conectores**: `P1` = `M20-7822046` (20 pinos, `HDR1X20_FEMALE`), `P2` = `M20-7821446` (14 pinos, `HDR1X14_FEMALE`); `P1.20`=`+24V`, `P1.17`=`+5V` — confirmado.
- **Render SVG vs. PDF pág. 9**: pixel a pixel idênticos (2376×1680 a 2×), sem sobreposição de texto, sem caixas cortadas, sem espaços vazios suspeitos.

## Limites desta verificação

- Não se verificou o esquemático (`.kicad_sch`) directamente, só a netlist exportada (`EBM2_V5.net`) — se a netlist não reflectir o `.kicad_sch` mais recente (ex.: gerada antes de um ERC ainda por limpar nas folhas 01/04/05/06/07, como o cabeçalho do documento de intenção adverte), esta verificação herda essa defasagem.
- Não se conferiu o `.kicad_sch` para a nota do §17 item 11 ("porto `DGND` do `P1.12` deslocado na folha 01... o triângulo tapava o `P1.13`") — é um achado de folha 01, fora do diagrama de blocos.
- Não se avaliaram os valores de engenharia por trás dos rótulos (dimensionamento térmico do `TPS26613`, I²t do fusível, etc.) — isso é âmbito da verificação de aplicação de datasheet (`V8`, `V9`, `V13`, `V14` já em aberto no próprio documento de intenção), não do diagrama de blocos.
- Não foi possível confirmar por netlist a afirmação "TTL" da caixa "Barreira" nem o "INL +-1 LSB" da caixa "Conversor A/D" — são especificações de datasheet, não topologia; aceites por conhecimento do MPN.
