# Pacote de revisão — EBM2 V5, F2

Data: 2026-09-23. Projecto KiCad: `C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\`.

## O que se pede a quem revê

**Quem escreveu não valida.** Este pacote é para uma revisão independente, noutra
sessão, sem o histórico de autoria.

| # | Revisar | Ficheiro | Contra o quê |
|---|---|---|---|
| 1 | Diagrama de blocos, etapa 2.1 | `diagrama_blocos_EBM2_V5.svg` | `planejamento_pcb_EBM2_V5.md` rev. 3 |
| 2 | Esquemático completo, etapa 2.2b: as 8 páginas | `esquematico_EBM2_V5_2026-09-23_folhas_completas.pdf` | `intencao_EBM2_V5.md` rev. 2 (aprovada em 2026-09-23), V4.1 auditada e datasheets da pasta de referência |

Páginas do PDF: 1 raiz, 2 conectores, 3 entrada, 4 alimentação, 5 barreira digital,
6 ADC, 7 laços, 8 NTC. Cada folha traz em azul as decisões que tomou e a fonte.

## Onde olhar primeiro

1. **Mapa de canais do conversor** (página 6): campo em `CH0`-`CH3`, `CH6`, `CH7`;
   `CH4` termístor; `CH5` no trilho `3V3_REF`. Confirmar contra a netlist da V4.1.
2. **Barreira** (página 5): só o `U400` a atravessa. Símbolo da EBM7 V2.3 Legacy
   (`EBM7_V23_proyecto4:ISO7141CC`), copiado sem alterações. Pinagem na figura da
   sec. 5, pág. 4, do SLLSE83F; a mesma página traz o ISO7131 e o ISO7140 com pinos trocados.
3. **Nomes dos trilhos de 5 V**: `+5V` só no barramento, `+5V_ADC` só no campo.
   Um porto com o nome errado funde os domínios e anula a barreira.
4. **`V8`, transmissor em curto** (página 7, nota 3): ~64 mA sustentados, fusível
   de 50 mA que pode não abrir, 249 Ω em 0603 a ~1 W. Confirmar ou refutar a conta.
5. **Polaridades**: `D201`, `D202`, `D200` (pág. 3); `TL431` (pág. 4); TVS
   `D601`-`D616`, `BAV199` `D621`-`D626` e LED `D630` (pág. 7).
6. **`U401` MCP1824S** (pág. 5): símbolo próprio `EBM2_V5:MCP1824ST-3302E`, cópia
   do Legacy com o corpo alargado. Pinos e números iguais; conferir contra a
   figura da pág. 2 do DS22070A.

## Estado das verificações automáticas neste pacote

| Porta | Resultado |
|---|---|
| Netlist contra as tabelas da intenção rev. 2 (`verifica_F2.py`): 39 redes exactas, 6 trilhos, barreira, nomes, no-connects | tudo confere |
| Positivo de controlo da porta anterior: a netlist antiga tem de reprovar | reprova |
| ERC | 0 erros. 225 avisos de biblioteca: 216 são do modo sem interface; 9 são as bibliotecas `EBM7_V23_proyecto3/4/9/10` na tabela do projecto sem o `.kicad_sym` (os símbolos estão embebidos; limpeza pendente) |
| Sobreposição de texto, texto fora do quadro e texto invertido, medidos no PDF | 0 nas 8 páginas |
| Rotas de instância contra a hierarquia | 225 instâncias, 0 anomalias |

O que estas portas **não** vêem: se um valor está certo para o circuito, se a
pinagem de um símbolo corresponde ao datasheet (etapa 2.3) e se as fórmulas das
secções de aplicação se cumprem (etapa 2.3b). Isso é o trabalho da revisão.

## Acrescentado depois da primeira versão deste pacote

- Folha 02: `T206` (+24V_ADC), `T207` (+24V_REG), `D203`+`R207` (LED do +24V).
  As notas da folha passaram 12,7 mm para a direita para dar lugar aos pontos de prova.
- Folha 03: `D204`+`R208` (LED do +5V_ADC).
- Folha 07: `R700` com o símbolo `Device:Thermistor_NTC` (a V4.1 e a Legacy desenhavam o NTC
  como resistência fixa). Designador mantido. Netlist sem alteração.
- Porta nova `verifica_pinos_instancia.py`: cada símbolo lista todos os pinos da definição
  (a falta do pino 9 do `U200` causava o aviso de auto-correcção do KiCad ao abrir).
- Cada folha com a netlist idêntica ao diff declarado; `verifica_F2.py` continua a conferir.

## Ainda por fechar

- `C200`: MPN (`V6`). `R206`: MPN (`V5`).
