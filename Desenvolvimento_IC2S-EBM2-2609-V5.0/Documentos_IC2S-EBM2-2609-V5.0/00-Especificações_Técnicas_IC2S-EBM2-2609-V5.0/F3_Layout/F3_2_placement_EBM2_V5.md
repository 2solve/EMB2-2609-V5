# F3 · 3.2 placement inicial — IC2S Extension Board EBM2 V5 (6AI)

| | |
|---|---|
| Data | 2026-09-25 |
| Base | Planta de zonas aprovada pelo projectista (`planta_zonas_EBM2_V5.png`) |
| Respostas do projectista (perguntas obrigatórias) | Contorno confirmado · **componentes só na face de cima** · alturas iguais à V4.1 |
| Ferramenta | `ferramentas/coloca_F3.py` (tabela de posições; o que está bloqueado não se toca) · medições em `ferramentas/mede_placement_F3.py` |
| Render | `KiCad_EBM2_V5/output/F3_placement_top.png` |
| Estado | **Placement inicial para iteração · Portão 3 por assinar** |

## Portas

| Porta | Resultado |
|---|---|
| DRC (`kicad-cli`, com paridade) | **0 violações, 0 problemas de paridade** (289 ligações por rotear — esperado) |
| Face | 131 pegadas colocadas, todas na face de cima (o script recusa uma virada); fixas intocadas: P1, P2, H1, H2, D1, D5, D24 |
| Pátio do `U7` | A pegada `SOIC16` tinha o pátio só no `User.15` (conversão do CircuitStudio): o DRC não via sobreposições com o conversor. Copiado para `F.CrtYd` (±3,4 × ±5,1 mm) na biblioteca (backup `.antes_crtyd`) e na placa |

## Barreira funcional (medida pad a pad, fora do U6)

A barreira da própria peça (`U6` ISO7141, entre filas de pads) é de **3,700 mm**. Fora dela:

| Folga | Entre | Leitura |
|---|---|---|
| **3,580 mm** | `P1.17` (+5V) ↔ `P1.19` (GND_24V) | **Herdada**: passo do conector congelado (`RC2`), igual à V4.1; não se altera |
| 3,857 mm | `P1.17` (+5V) ↔ `D2.2` (GND_24V) | ok (estava a 2,80 mm na 1.ª passagem; `D2` descido) |
| 4,056 mm | `U6.1` ↔ `C13.1` | ok (3,57 na 1.ª passagem) |
| 4,677 mm | `U5.3` ↔ `C4.1` | ok |

Tudo o que não é o próprio conector fica ≥ 3,857 mm, acima da barreira do `U6`.

## Desacoplamento (centro do pad ao centro do pino)

| Condensador | Pino | Distância |
|---|---|---|
| `C17`-`C22` | +Vs dos `U8`-`U13` | 2,46 mm (os seis iguais) |
| `C33` / `C7` | C_BYP do `U14` / `U1` | 1,88 / 4,36 mm |
| `C4` / `C31`-`C32` | saída do `U1` / `U14` | 2,38 / 3,96-4,06 mm |
| `C1` / `C30` | entrada do `U1` (pino 5) / `U14` | 3,43 / 2,80 mm |
| `C16` / `C14` | VDD / VREF do `U7` | 3,20 / 3,80 mm (`C15` 1 µF a 4,50) |
| `C13` / `C12` | VCC2 / VCC1 do `U6` | 2,70 / 3,88 mm |
| `C5` | saída do `ADR4525` | 3,44 mm |
| `C8` / `C9` | saída do `U4` / 3V3_REF no TL431 | 2,63 / 4,00 mm |

## O que ficou onde

- **Digital (DGND):** `U5` em baixo à esquerda (entrada `+5V` junto do `P1.17`), `C10`/`C11`, `C12` junto do VCC1, `TP8`.
- **Isolador:** `U6` na posição e rotação do `U4` da V4.1; `FB1`/`C13` do lado de campo.
- **Conversor:** `U7` a 180° (canais para a direita, SPI para a esquerda, para o `U6`); por cima o `ADR4525` `U2` com `C5`,
  o termístor `TH1`/`R40`/`C35` junto do pino 5 (CH4); faixa de cima com `U4`, o grampo `U3`/`R8`/`R9` e `C3`/`C8`/`C9`.
- **Seis laços:** uma fila por canal, `y = 85,45 + 5,9 (k−1)`, da direita para a esquerda: TVS do terminal, TVS do
  retorno, fusível sobre o burden, TPS26613 com o seu 100 nF, 0 Ω sobre o 3k3, BAV199, C do filtro sobre o 4k7.
  Os seis canais são idênticos (mesmas posições relativas), o que ajuda a `V1` e a revisão.
- **Alimentação:** `U1` a 90° (OUT/FB para baixo, junto de `C4`/`C7`/`R5`/`R6`); entrada de 24 V em baixo à esquerda
  (`D2` junto de `P1.19/20`, `F1`→`D3`→`R3` e `F2`→`D4`→`C2`, `R2` net-tie); `U14` em baixo à direita com o divisor `VSNS`.

## Pendente antes do Portão 3

- Serigrafia: arrumar as referências que se sobrepõem (`C16`, `FB2`, `C35`, `R4`/`R5`, `C32`/`R35`, `R1`/`R34`).
- Iteração com o projectista («sobe U5», «afasta …»), com render 3D a cada passo.
- Para a 3.3 (roteamento, humano): `V1` (retorno < 5 mΩ, cobre interno de 17,5 µm), cobre nos `U8`-`U13`, land pattern
  do `C1` 1210, planos In1/In2 com a separação da barreira.
