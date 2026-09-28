# Alterações de 2026-09-28 — decisões da revisão da EBM7 V2.3 trazidas para a EBM2 V5

Na reunião de 28-09 a equipa pediu, para a EBM7 V2.3: um só ramo de 24 V, rever o condensador de entrada da fonte,
baixar a tensão dos condensadores de 100 V do lado analógico e usar o mesmo MPN para a mesma função. Aqui aplicam-se
as mesmas decisões à EBM2 V5. **É uma alteração posterior ao Portão 1**: o pacote `Portao1_aprovado_2026-09-25`
fica como estava, e esta nota regista o desvio.

Notas no esquemático: **folha 2, notas 3, 11, 13 e 14**.

## 1. Ramo único de 24 V

**Antes:** depois do TVS D2 havia dois ramos:
- F1 (CC12H250MA) → D3 → R3 (150 Ω) → +24V_REG, que alimentava só o U1 (TPS7A4001, 5 V);
- F2 (CC12H750MA) → D4 → +24V_ADC, para os laços, o U14 (12 V) e o LED.

**Agora:** saem **F1, D3 e R3**. F2 → D4 → **+24V_ADC** alimenta tudo; o nome +24V_REG deixa de existir.

Na EBM7 ficou o ramo do conversor e saiu o dos laços. Aqui é ao contrário, e isto não é escolha:
- o F1 funde com 3,8e-4 A²s, e o arranque só do C2 (10 µF a 32 V) dá 6,4e-3 A²s (nota 2), ou seja, o F1 abriria ao
  ligar. Só o F2 (0,15 A²s) aguenta a placa inteira;
- o R3 existia apenas para limitar a corrente do F1 (nota 11: «sem R3 seria 1,2×»). Sem F1 perde a função e sai;
- o **C1 (2,2 µF / 100 V) fica**: é o Cin do U1, que o TPS7A4001 pede (> 1 µF, nota 10).

Contas:
- Corrente no F2 (750 mA) e no D4 (MBR1H100SF, 1 A): 125 mA dos laços e LEDs + ~7 mA do U1 = ~132 mA.
- I²t no arranque, a 32 V com R = 0,8 Ω (fórmula da nota 2): ~22 µF nominais a jusante (C2 + C30 + C1 + 100 nF) dão
  1,4e-2 A²s contra 0,15 A²s: **≥ 10× de margem**. A nota 2 dava 23,4× porque contava só o C2. Com a capacidade
  efectiva a 32 V, mais baixa, a margem real é maior. Estimativa, não medida.
- Perde-se a selectividade: um curto no +24V_ADC abre o F2 e desliga a placa toda.
- O requisito **RA2** do planeamento (margem do fusível do regulador, 11,3×) deixa de se aplicar como estava escrito:
  o regulador passa a depender do F2.
- **TP3** fica no mesmo sítio, à entrada do U1, agora em +24V_ADC (valor `TP_+24V_U1`).

PCB (sem pistas ainda): saíram as pegadas de F1, D3 e R3; os pads de C1, TP3 e U1 (5, 8) passaram a +24V_ADC.

## 2. Condensador de entrada da fonte

O U1 é um TPS7A4001, e não o R-78HB da EBM7. O C1 foi verificado na F2 (tanda C) contra o datasheet da TI e contra a
curva TDK: ~1,54 µF a 30,4 V, e 1,18 µF no pior caso, acima de 1 µF. **Sem alteração.**

## 3. Tensão dos 100 nF

Todos os 22 eram GRM188R72A104KA35D (100 V). Só o **C29**, em +24V_ADC (até 53,3 V no clamp), precisa de 100 V.

| Grupo | Tensão máxima | Peça |
|---|---|---|
| C29 em +24V_ADC | 53,3 V | fica GRM188R72A104KA35D, 100 V (`100nF/100V`) |
| C17-C22 (+Vs dos TPS26613) e C34 (VSNS), em +12V_TPS | 12 V; até ~32 V (Vin) se o U14 falhar | **TDK C1608X7R1H104K080AA, 50 V** |
| C3, C6, C9, C12-C14, C16, C23-C28, C35 (3,3 / 5 V, ADC, filtros) | ≤ 5 V | **TDK C1608X7R1H104K080AA, 50 V** |

25 V não serve, porque não cobre o caso do U14 em falha. Fonte: catálogo TDK *MLCC commercial general*, p.34. São 21
peças, com o valor escrito `100nF/50V`. Na intenção do projecto, C17-C22 estavam a 100 V só por herança dos
C26/C29/C31/C32 da EBM7 Legacy, que também passaram a 50 V.

## 4. Mesmo MPN para a mesma função

- **1 µF (C10, C15):** já tinham um só MPN (KEMET C0603C105K4RACTU, 16 V). Passam a **TDK C1608X7R1H105K080AB**
  (50 V, catálogo p.35), o mesmo da EBM7, para as duas placas usarem uma só peça. Valor `1uF/50V`.
- 10 µF / 50 V, 2,2 µF, 10 nF e 10 µF / 100 V: já tinham um MPN cada. Sem alteração.

## Verificação

- Netlist antes/depois: saem F1, D3, R3 e as redes `+24V_FUS_REG` e `+24V_DIO_REG`; C1, TP3 e U1 (pinos 5 e 8)
  passam de +24V_REG a +24V_ADC; 23 condensadores mudam de valor/MPN. Nenhuma outra ligação muda.
- ERC: 0 erros; os avisos são os de antes, menos os das três peças.
- DRC (`--severity-all --schematic-parity`): 0 violações, **paridade 0**; 286 ligações por fazer (placa sem roteamento).
- BOM preliminar regenerada com `Ferramentas/gera_bom_prelim.py` e os mesmos dados Mouser de 25-09: 42 linhas, 123
  peças montadas. Os dois TDK novos aparecem sem preço/stock (N/D), porque não foram consultados na Mouser.
- `01-Esquemáticos/esquematico_EBM2_V5.pdf` regenerado. O PDF de revisão da F2 (`EBM2_V5_F2_revisao_2026-09-25.pdf`)
  é do Portão 1 e não foi refeito.
