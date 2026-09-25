# Portão 1 — verificação cruzada · EBM2 V5 (6AI 4-20 mA)

**Quem desenhou não valida.** O autor é o Claude Opus 5.5. Esta verificação corre numa **sessão nova, com modelo
diferente**, sem o histórico da conversa de autoria. O objectivo é **encontrar o que impede a assinatura**, não
confirmar o que o autor escreveu.

## O que o Portão 1 aprova (skill `2shw-pcb:fluxo`, portão P1)

Os **três blocos da F2**: (1) diagrama de blocos; (2) **esquemático KiCad com ERC limpo** + documento de intenção;
(3) **BOM preliminar e mapa de pinos**. Assinado o P1 liberta-se a compra antecipada (Suprimentos) e a F3 (layout).

## Material (nesta pasta; só leitura fora dela)

| Ficheiro | Bloco |
|---|---|
| `diagrama_blocos_EBM2_V5.svg` | 1 |
| `EBM2_V5_F2_revisao_2026-09-25.pdf` (esquemático do KiCad + diagrama + mapa de pinos) | 1, 2, 3 |
| `EBM2_V5.net` (netlist exportada agora), `erc.json` | 2 |
| `intencao_EBM2_V5.md` (ver §9, §17), `escopo_EBM2_V5.md` (critérios `RA`, `RB`, `RC`, `RE`) | 2 |
| `LEIA-ME_F2_2.5.md` (portas e achados da etapa 2.5) | 2 |
| `bom_preliminar_EBM2_V5.md/.csv`, `bom_dados_mouser_*.json` (resposta crua da Mouser, 2026-09-25) | 3 |
| `mapa_pinos_EBM2_V5.md` | 3 |
| `datasheets/` (`LISTA.md` com md5) | todos |

O projecto KiCad (`C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\`) e as verificações anteriores
(`C:\hw\hw-ebm2-v5\Documentos\verificacao_2_3b*`) podem ser **lidos, nunca editados**.

## Onde está o risco (prioridade da revisão)

A última revisão independente foi a 2.3b da rev. 2.5b. **Depois dela entraram tandas que só passaram portas
automáticas** — e a skill `2shw-pcb:esquematico` diz que uma tanda é esquemático novo e precisa de revisão
independente (na EBM7, dez correcções passaram todas as portas e criaram dois bloqueantes novos):

| Tanda | O que mudou | O que conferir |
|---|---|---|
| rev. 2.5c | `R3` 68 → **150 Ω** | `RA2` do `F1` (Eaton 4309 pág. 2 e curva pág. 4); arranque a 18 V (VIN mín. do `U1`); o `R3` num curto de `+24V_REG` |
| Textos 25c | Notas de 5 folhas; grampo do `D2` corrigido para 53,3 V | Que o novo número está certo (Bourns SMA6J33A pág. 2) e que nenhuma decisão dependia do antigo |
| BOM tanda A | 14 MPN; **`C4` em 1206** `C3216X5R1H106K160AB`; pontos de prova fora da BOM | Cada MPN contra o valor, a tensão e a pegada da netlist; a pegada nova do `C4` |
| BOM tanda B | `U2` → **`ADR4525WBRZ-R7`**; `R3` = **KOA `SG73P2ATTD1500F`**; porto DGND do `P1.12` na folha 01 | Equivalência de grau e pinagem do ADR (tabela 14 pág. 40); curva de impulso do SG73P (pág. 2); a folha 01 ampliada |
| `C1` | (ver `intencao` §17 linha 11) | ≥ 1 µF efectivo a 32 V e ≤ 2,2 µF (`RA2`) |

## O que fazer

1. **Bloco 2 — esquemático.** ERC (erros = 0, sem ignorar avisos que sejam achados). Netlist contra as tabelas da
   intenção (§4, §8, §9, §17). **Polaridade de cada díodo, TVS, LED e CI por render ampliado**, peça a peça, contra
   a netlist — a skill diz que nenhuma ferramenta substitui isto. Texto sobre símbolo ou fora da moldura.
2. **Bloco 3 — BOM e pinos.** Cada linha da BOM contra a netlist (refs, quantidades, MPN, pegada); cada MPN contra
   o seu datasheet (valor, tensão, dieléctrico, encapsulamento); dados comerciais com data e fonte (nada estimado);
   alternativas «verificadas» realmente equivalentes. O mapa de pinos contra a netlist.
3. **Bloco 1 — diagrama.** Coerente com o esquemático actual (peças, trilhos, barreira).
4. **As tandas da tabela acima**, uma a uma, com a conta refeita e a página citada (texto E figura).
5. Tudo o que a revisão não conseguiu verificar entra como limitação, não como «ok».

## Saída pedida

`relatorio_verificacao_cruzada_P1_EBM2_V5.md` nesta pasta, em **português**, com:
- veredicto por bloco: **aprovado / aprovado com ressalvas / reprovado**, e o veredicto do portão;
- tabela de achados: `# | bloco | onde | achado | evidência (ficheiro, página) | severidade (bloqueante / ressalva / nota)`;
- o que foi conferido e o que não foi (limites).
