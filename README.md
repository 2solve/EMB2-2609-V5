# IC2S Extension Board EBM2 V5 — 6 entradas 4-20 mA

Placa de extensão da família IC2S (2Solve), código **IC2S-EBM2-2609-V5.0**. Seis entradas analógicas de 4-20 mA
para a Universal Baseboard; **substituição directa da EBM2 V4.1** (contorno 60 × 60 mm, furação e pinagem de
`P1`/`P2` congelados). Projecto em **KiCad 10**.

## Estado (2026-09-28)

| Fase | Estado |
|---|---|
| F0/F1 — escopo e planeamento | fechadas |
| F2 — esquemático, diagrama, BOM preliminar, mapa de pinos | **Portão 1 aprovado** (pacote congelado em `Portao1_aprovado_2026-09-25`) |
| F3 — layout | contorno e placement inicial feitos (DRC 0, paridade 0); falta o Portão 3 e o roteamento |

**Alteração posterior ao Portão 1 (2026-09-28)**, trazida da revisão da EBM7 V2.3: ramo único de 24 V (saem F1, D3 e
R3), 100 nF a 50 V fora do 24 V e um só MPN de 1 µF. Detalhe em
`Documentos_…/00-Especificações_Técnicas_…/alteracoes_reuniao_2026-09-28.md` e na folha 2, notas 3, 11, 13 e 14. O
pacote congelado do Portão 1 não foi tocado; a BOM preliminar foi regenerada (42 linhas, 123 peças montadas).

## Organização (modelo de pastas de Produtos)

```
Desenvolvimento_IC2S-EBM2-2609-V5.0/
  Arquivos_Fabricação_IC2S-EBM2-2609-V5.0/
    00-Gerbers_…            (vazio até à F3)
    01-BOM_List_…           BOM preliminar (.md/.csv) e respostas cruas da API Mouser (2026-09-25)
    02-Pick-and-Place_…     (vazio até à F3)
    03-Stencil_…            (vazio até à F3)
  Documentos_IC2S-EBM2-2609-V5.0/
    00-Especificações_Técnicas_…   escopo, intenção, planeamento, relatórios, verificações da F2, Portão 1, F3
    01-Esquemáticos_…              PDF de revisão da F2 (esquemático + diagrama + mapa de pinos), PNG e SVG por folha
    02-Pinout_…                    mapa de pinos de P1/P2/U6/U7 e regras para o firmware
    03-Diagrama_Blocos_…           diagrama de blocos (SVG)
  Projeto_IC2S-EBM2-2609-V5.0/
    IC2S_Extension_Board-EBM2_V5.kicad_pro/.kicad_sch/.kicad_pcb e as 7 folhas
    symbols/, footprints/   bibliotecas próprias do projecto (sym-lib-table e fp-lib-table relativas)
    Ferramentas/            scripts Python de geração e verificação (ERC, netlist contra a intenção, BOM, PDF, F3)
    Documentos_de_Referência-IC2S-EBM2-2609-V5.0/   lista dos datasheets usados (nome e md5)
```

## O que não está neste repositório, e porquê

- **Datasheets dos fabricantes**: não se redistribuem num repositório público. `LISTA_datasheets.md` dá o nome e o
  md5 de cada ficheiro usado.
- Backups intermédios (`.antes_*`), netlists e relatórios ERC de passos intermédios, estado local do KiCad
  (`.kicad_prl`, `.history`).
- Ficheiros da V4.1 (Gerbers de origem usados para conferir o contorno): são de outro produto.

## Notas

- Os ficheiros KiCad mantêm o nome `IC2S_Extension_Board-EBM2_V5`: renomear o projecto partiria as instâncias
  dos símbolos nas folhas.
- Referências R1, R2… desde 2026-09-25; uma referência de três dígitos num documento é da numeração antiga
  (tabela em `tabela_correspondencia_refs_EBM2_V5.md`).
- Os scripts em `Ferramentas/` usam os caminhos locais de desenvolvimento (`C:\hw\hw-ebm2-v5`); a consulta à
  Mouser lê a chave de `MOUSER_API_KEY` e nunca a grava.
