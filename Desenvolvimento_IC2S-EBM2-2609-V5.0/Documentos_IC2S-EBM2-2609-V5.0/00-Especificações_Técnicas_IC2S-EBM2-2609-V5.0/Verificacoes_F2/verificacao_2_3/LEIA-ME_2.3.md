# Pacote da etapa 2.3 — verificação de pinagem · EBM2 V5 (6AI 4-20 mA)

Data: 2026-09-23. Esquemático: `C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\` (intenção rev. 2.3).

## Regras (skill `2shw-pcb:esquematico`, etapa 2.3)

- **Quem escreveu não valida.** Esta verificação corre numa **sessão nova, com modelo diferente**
  do que desenhou (a autoria foi Claude Opus 5.5), **sem o histórico da conversa de autoria**.
  Sugestão: Claude Sonnet 5 ou Claude Fable 5.1.
- Conferência **pino a pino contra o datasheet**: número, nome, função, direcção, nível.
- **Os datasheets usam-se pelo conteúdo, não pelo nome.** Os desta pasta foram conferidos pelo
  texto; se precisar de outro, abra-o e confirme o número de peça na primeira página.
- Tratar os **três níveis de confiança separadamente** (tabela abaixo). Um veredito único esconde
  qual deles era o frágil.
- **Só leitura.** Não editar o projecto KiCad. Correcções vão para o relatório; quem desenhou aplica.
- Recomenda-se, além disto, **conferência humana em papel** do PDF (caneta vermelha).

## O que está na pasta

| Ficheiro | Para quê |
|---|---|
| `inventario_pinos_EBM2_V5.md` | Os 45 componentes a conferir, em 16 grupos: para cada pino, número → nome no símbolo → tipo → rede; símbolo, pegada, ilhas da pegada e datasheet |
| `EBM2_V5.net` | Netlist exportada pelo KiCad 10.0.5 no momento da preparação |
| `esquematico_EBM2_V5.pdf` | As 8 folhas, para ver o desenho |
| `intencao_EBM2_V5.md` | A especificação aprovada (rev. 2.3): o gabarito das ligações |
| `datasheets/` | 15 datasheets, um por família, e `LISTA.md` com md5 e origem |

**Fora do âmbito:** resistências, condensadores, ferrites, fusíveis e o NTC (dois terminais, sem
polaridade), e os pontos de prova (um terminal). As fórmulas e os valores são da etapa 2.3b.

## Níveis de confiança por grupo

| Grupo | Origem do símbolo | Nível | O que conferir |
|---|---|---|---|
| `U200` TPS7A4001 | Símbolo da EBM7 Legacy (`EBM7_V23_proyecto9`) | Datasheet (citado na descrição do símbolo) | Pino a pino, incluindo a ilha exposta |
| `U201` SPX3819 | Biblioteca padrão do KiCad | Biblioteca, **não conferida contra o datasheet** | Pino a pino; variante SOT-23-5 do MPN |
| `U202` ADR4525 | Símbolo da EBM7 Legacy (`EBM7_V23_proyecto10`) | Datasheet (descrição cita a figura) | Pino a pino, incluindo pinos NIC/DNC |
| `U203` TL431 | Biblioteca padrão do KiCad (`TL431DBZ`) | Biblioteca, **não conferida** | Pino a pino na variante SOT-23-3 (DBZ) |
| `U400` ISO7141 | Símbolo da EBM7 Legacy (`EBM7_V23_proyecto4`) | Datasheet | Pino a pino **na variante ISO7141**, lados 1 e 2 |
| `U401` MCP1824S | Próprio (cópia do Legacy, corpo alargado) | Datasheet | Pino a pino na variante SOT-223-3 |
| `U500` MCP3208 | Biblioteca padrão do KiCad | Biblioteca, **não conferida** | Pino a pino no SOIC-16; ordem dos canais |
| `U601-U606` AL5809 | Próprio | Datasheet | In/Out e a pegada (variante do encapsulamento) |
| `D621-D626` BAV199 | Símbolo da EBM7 Legacy (`EBM7_V23_proyecto3`) | Datasheet | Os três pinos e qual é o comum |
| Díodos de 2 terminais (`D200`, `D201/D202`, `D6xx`, `D641-D646`) e LED (`D203/D204/D630`) | Biblioteca padrão (`Device:D_*`, `Device:LED`) | **Convenção KiCad: pino 1 = cátodo** | Símbolo pino 1 = cátodo → ilha 1 da pegada = lado da marca de cátodo → marca do fabricante no datasheet |
| `P1`, `P2` | `Connector_Generic` | Convenção (1…n) | Numeração contra o desenho Harwin; a pinagem de função é congelada (`RC2`) e confere-se contra a V4.1, não contra o datasheet |

## Método sugerido

1. Para cada grupo do inventário, abrir o datasheet indicado e localizar a **figura de pinagem do
   encapsulamento declarado pelo MPN** (não outro encapsulamento da mesma família).
2. Conferir cada linha: número ↔ nome ↔ função. Depois, a **rede** faz sentido para essa função?
   (ex.: um pino de alimentação na rede de alimentação, um NC sem ligação indevida).
3. Conferir a **pegada**: número e posição das ilhas contra o desenho do encapsulamento e o
   *land pattern* recomendado; ilha 1 e marca de polaridade.
4. Conferir que o **MPN** (sufixo) corresponde ao encapsulamento da pegada.

## Pontos de atenção gerais (sem conclusões — são sítios onde costuma haver erro)

- Páginas de datasheet que mostram **várias peças da mesma família** com pinagens diferentes.
- Encapsulamentos com o **mesmo nome comercial em variantes** (Type A/B, com e sem ilha exposta,
  SOD-123 contra SOD-123FL).
- Nomes de pino no símbolo que **não coincidem** com os do datasheet.
- Díodos: o que a biblioteca chama pino 1 contra onde o fabricante põe a barra.

## Saída pedida

`C:\hw\hw-ebm2-v5\Documentos\verificacao_2_3\verificacao_pinagem_EBM2_V5.md`, com:

- cabeçalho: modelo e sessão usados, data, datasheets consultados (ficheiro e página);
- uma tabela por grupo: `Ref | Pino | Nome no símbolo | Rede | Datasheet (pág./figura) | Veredito (OK / DIVERGÊNCIA) | Correcção proposta`;
- tabela das pegadas: `Pegada | Ilhas conferidas | Ilha 1 / polaridade | Veredito`;
- um resumo por nível de confiança (datasheet / biblioteca / convenção), com o número de pinos
  conferidos e de divergências em cada um.

## Informação fora do âmbito da 2.3 (para não gastar tempo)

- Em 2026-09-24 trocaram-se três peças por ciclo de vida, sem mudar pegada nem ligação: LED →
  `KG EELP41.22-PHRH-35-A8J8-20-R18`, 100 nF → `GRM188R72A104KA35D`, Schottky → `BAT46W-7-F` (Diodes).
  Ver `Relatorio_Ciclo_Vida_EBM2_V5_2026-09-24.md`. O LED e o Schottky novos estão no inventário.

## Mensagem para colar na sessão nova

> Faz a etapa 2.3 (verificação de pinagem) do esquemático EBM2 V5, seguindo a skill
> `2shw-pcb:esquematico`. Lê primeiro `C:\hw\hw-ebm2-v5\Documentos\verificacao_2_3\LEIA-ME_2.3.md`
> e usa só o material dessa pasta (o projecto KiCad em `C:\hw\hw-ebm2-v5\KiCad_EBM2_V5\` pode ser
> lido, nunca editado). Confere pino a pino contra os datasheets da pasta e escreve o resultado em
> `verificacao_pinagem_EBM2_V5.md` na mesma pasta, no formato pedido. Não assumas que o desenho
> está certo: o objectivo é encontrar divergências.
