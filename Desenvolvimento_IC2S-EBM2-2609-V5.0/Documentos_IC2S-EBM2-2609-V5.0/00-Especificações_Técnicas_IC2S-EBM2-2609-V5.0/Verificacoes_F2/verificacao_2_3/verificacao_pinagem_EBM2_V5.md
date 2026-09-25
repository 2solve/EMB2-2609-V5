# Verificação de pinagem (etapa 2.3) — EBM2 V5

| Campo | Valor |
|---|---|
| Data | 2026-09-24 |
| Quem verificou | **Javier Rivadineira**, revisão humana |
| Independência | Quem desenhou foi o Claude Opus 5.5; quem verificou foi o projectista, sem participar na autoria do desenho. A skill aceita e recomenda a conferência humana nas primeiras placas |
| Âmbito | Os **16 grupos** de `inventario_pinos_EBM2_V5.md`: 45 componentes, 173 pinos (circuitos integrados, díodos, LED, limitadores e conectores) |
| Material | Pacote desta pasta: inventário gerado da netlist, `EBM2_V5.net`, `esquematico_EBM2_V5.pdf`, `intencao_EBM2_V5.md` e os 15 datasheets de `datasheets/` (escolhidos pelo conteúdo; md5 em `LISTA.md`) |
| **Resultado** | **Sem divergências** nos 16 grupos |

## Por grupo

| Grupo | Nível de confiança (LEIA-ME) | Veredito |
|---|---|---|
| `D200` SMA6J33A-Q | Convenção KiCad (pino 1 = cátodo) | OK |
| `D201`, `D202` MBR1H100SFT3G | Convenção KiCad | OK |
| `D203`, `D204`, `D630` KG EELP41.22 | Convenção KiCad | OK |
| `D601`-`D606`, `D611`-`D616` 824520361 | Convenção KiCad | OK |
| `D621`-`D626` BAV199LT1G | Datasheet | OK |
| `D641`-`D646` BAT46W-7-F | Convenção KiCad | OK |
| `P1` M20-7822046 | Convenção (1…n); função congelada `RC2` | OK |
| `P2` M20-7821446 | Convenção (1…n); função congelada `RC2` | OK |
| `U200` TPS7A4001DGNR | Datasheet | OK |
| `U201` SPX3819M5-L-3-3/TR | Biblioteca KiCad | OK |
| `U202` ADR4525BRZ | Datasheet | OK |
| `U203` TL431BQDBZR | Biblioteca KiCad | OK |
| `U400` ISO7141CCDBQR | Datasheet | OK |
| `U401` MCP1824ST-3302E/DB | Datasheet | OK |
| `U500` MCP3208T-BI/SL | Biblioteca KiCad | OK |
| `U601`-`U606` AL5809-25P1-7 | Datasheet | OK |

## Limitações declaradas

- **Não correu a conferência por sessão de outro modelo.** A skill pede uma sessão nova com
  modelo diferente, ou declarar a limitação. A independência aqui é humana, não de modelo. O
  **Portão 1** inclui uma verificação cruzada com modelo diferente sobre o esquemático.
- Este registo resume o veredito do projectista por grupo. **Não reproduz a tabela pino a pino**:
  a conferência pino a pino foi feita pelo projectista sobre o inventário.
- As pegadas ficaram conferidas **no que o inventário mostra** (número e posição das ilhas). O
  *land pattern* completo contra o desenho de cada encapsulamento revê-se na F3.
