# -*- coding: utf-8 -*-
"""BOM preliminar da EBM2 V5 (skill 2shw-pcb:bom, modo preliminar).

Parte da NETLIST real (kicad-cli), agrupa por MPN, tira o que tem in_bom = no (pontos de prova, fiduciais) e
junta, se existir, a resposta crua da Mouser gravada por consultar_mouser_bom.py. Sem dado Mouser, preco,
stock e codigo ficam N/D: nunca se estimam. O ciclo de vida so se declara com fonte e data.
Uso: python gera_bom_prelim.py NETLIST.net SAIDA_SEM_EXTENSAO [MOUSER.json]
"""
import csv, glob, io, json, os, re, sys
from netlist_diff import ler

NET, SAI = sys.argv[1], sys.argv[2]
MOU = json.load(io.open(sys.argv[3], encoding="utf-8")) if len(sys.argv) > 3 and os.path.exists(sys.argv[3]) else {}
# Alternativas consultadas a parte (mesma API, mesma data): {palavra-chave: [pecas Mouser]}
ALTJ = json.load(io.open(sys.argv[4], encoding="utf-8")) if len(sys.argv) > 4 and os.path.exists(sys.argv[4]) else {}
ALTP = {str(p.get("ManufacturerPartNumber")).strip(): p for lst in ALTJ.values() for p in lst}
# Alternativas VERIFICADAS no datasheet (mesma peca electrica); so estas entram no cenario de compra
ALT_V = {"ADR4525WBRZ-R7": ("ADR4525BRZ", "O MPN original: mesmo grau B em tubo de 98; na Mouser sem preço nem stock e «Restricted Availability» (2026-09-25). A WBRZ-R7 entrou na tanda B por isso (ADR45xx Rev. G, tabela 14 pág. 40, nota 2 pág. 41)"),
         "3413.0002.22": ("3413.0002.11", "Mesma linha eléctrica (50 mA, 63 VDC, 9200 mΩ, 0,0002 A²s); só muda a embalagem: 100 un. em fita (Schurter USFF, págs. 3-4)"),
         "KG EELP41.22-PHRH-35-A8J8-20-R18": ("Q65113A7469", "Código de encomenda OSRAM do mesmo tipo e bin, KG EELP41.22-PHRH-35-A8J8 (datasheet v1.4 pág. 3)"),
         "ISO7141CCDBQR": ("ISO7141CCDBQ", "Mesma peça, tubo de 75 em vez de bobina de 2500 (TI, package option addendum pág. 27)")}
LOTE_STOCK = 10     # alerta de stock se a Mouser nao cobre este numero de placas
c, _, _ = ler(NET)
raw = io.open(NET, encoding="utf-8").read()
fora = {m.group(1) for m in re.finditer(r'\(comp\s+\(ref "([^"]+)"\)(.*?)\n\t\t\)\n', raw, re.S)
        if "exclude_from_bom" in m.group(2) or "(name \"dnp\")" in m.group(2)}

FAB = [("GRM", "Murata"), ("GCM", "Murata"), ("BLM", "Murata"), ("RC0603", "Yageo"), ("RC1206", "Yageo"),
       ("ERJ-", "Panasonic"), ("ERA", "Panasonic"), ("C1608", "TDK"), ("C3216", "TDK"), ("C0603C", "KEMET"),
       ("TPS", "Texas Instruments"), ("TL431", "Texas Instruments"), ("ISO7141", "Texas Instruments"),
       ("MCP", "Microchip"), ("ADR", "Analog Devices"), ("BAV199", "onsemi"), ("MBR", "onsemi"),
       ("SMA6J", "Bourns"), ("SMBJ", "Diodes Inc."), ("8245", "Würth Elektronik"), ("CC12H", "Eaton"),
       ("3413", "Schurter"), ("M20-", "Harwin"), ("NTCS", "Vishay"), ("RMCF", "Stackpole"), ("KG ", "ams OSRAM")]
# Ciclo de vida COM FONTE (Relatorio_Ciclo_Vida_EBM2_V5_2026-09-24.md); o resto e N/D ate a consulta Mouser
CV = {m: "Activo (DigiKey 2026-09-24)" for m in ("MCP3208T-BI/SL", "MBR1H100SFT3G", "CC12H250MA-TR", "GRM32EC72A106ME05L",
      "ERA8AEB111V", "ERA3AEB5621V", "ERJ-3EKF1472V")}
CV.update({m: "Activo (BOM EBM7 2026-09-14)" for m in ("TPS7A4001DGNR", "TL431BQDBZR", "ISO7141CCDBQR", "MCP1824ST-3302E/DB",
           "BAV199LT1G", "SMA6J33A-Q", "824520361", "CC12H750MA-TR", "3413.0002.22", "BLM18PG471SN1D", "RC0603FR-072K2L",
           "RC0603FR-073K3L", "RC0603JR-070RL", "NTCS0603E3103JLT", "M20-7822046", "M20-7821446")})
CV["KG EELP41.22-PHRH-35-A8J8-20-R18"] = "Activo (substituto do LG Q396 obsoleto, relatório 2026-09-24)"
CV["GRM188R72A104KA35D"] = "Activo (substituto do GRM188R71E104KA01D obsoleto, relatório 2026-09-24)"
CV["C3216X5R1H106K160AB"] = "Production (ficha TDK 2026-09-24)"
CV["C3225X7R2A225K230AB"] = "Production (ficha TDK 2026-09-25)"
CV["C1608X5R1E225K080AB"] = "Production (ficha TDK 2026-09-24)"
NOTA = {"ISO7141CCDBQR": "**0 em stock na Mouser** (BOM EBM7 2026-09-14): risco de abastecimento",
        "824520361": "Stock baixo (314 D / 82 M) para 6 por placa",
        "ERA3AEB5621V": "Prazo de fábrica 49 semanas (DigiKey 2026-09-24)",
        "C1608X5R1E225K080AB": "Curva TDK conferida (ficha 2026-09-24): pior caso 1,44 µF a 2,5 V (C5) e 1,26 µF a 3,3 V (C11), ≥ 1 µF",
        "C3225X7R2A225K230AB": "C1: curva TDK ~1,54 uF a 30,4 V; pior caso 1,18 uF > 1 uF (TPS7A4001); RA2 11,3x. X7S 1206 descartado (0,89 uF)",
        "SG73P2ATTD1500F": "R3: pulso de arranque 6,6 W / 0,6 ms contra ~26 W da curva 2A (KOA SG73P pág. 2): ~4x",
        "ADR4525WBRZ-R7": "Família «Restricted Availability» na Mouser: comprar cedo",
        "C3216X5R1H106K160AB": "Curva TDK conferida: C4 7,0 µF a 5 V, C8 7,2 µF a 3,3 V, C31+C32 8,9 µF a 12,6 V (pior caso)",
        "TPS26613DDFR": "Novo na rev. 2.4 (protector de laço)", "SMBJ33A-13-F": "Novo na rev. 2.4 (DS19002 conferido)",
        "MCP1824T-3302E/OT": "Novo na rev. 2.5 (U4)"}
ALT = {"GRM32EC72A106ME05L": "GRM32EC72A106KE05L (±10 %, mesma série; troca feita na EBM7 por falta de stock)",
       "GRM188R72A104KA35D": "—", "BAT46W-7-F": "—"}
# Biblioteca da casa: MPN ja usados na EBM7 V2.3 (Legacy e Mouser) ou na V4.1
casa = set()
for f in glob.glob(r"C:\hw\hw-ebm7-v2.2\**\*.net", recursive=True) + glob.glob(r"C:\hw\hw-ebm2-v4.1\**\*.net", recursive=True):
    if ".history" in f:
        continue
    try:
        casa |= set(re.findall(r'\(name "MPN"\) "([^"]+)"', io.open(f, encoding="utf-8", errors="replace").read()))
    except OSError:
        pass


def fab(m):
    return next((v for k, v in FAB if m.startswith(k)), "N/D")


def preco(pb, q):
    """Preco unitario no escalao que a quantidade atinge; None se nao ha."""
    melhor = None
    for b in sorted(pb, key=lambda b: int(b.get("Quantity", 0))):
        if int(b.get("Quantity", 0)) <= q:
            s = re.sub(r"[^\d,.]", "", str(b.get("Price", "")))
            s = s.replace(".", "").replace(",", ".") if "," in s and s.rfind(",") > s.rfind(".") else s.replace(",", "")
            try:
                melhor = float(s)
            except ValueError:
                pass
    return melhor


grupos = {}
for ref, v in c.items():
    if ref in fora:
        continue
    k = v.get("MPN") or "SEM MPN: %s %s" % (v["value"], v["footprint"].split(":")[-1])
    grupos.setdefault(k, {"refs": [], "val": set(), "fp": v["footprint"].split(":")[-1]})
    grupos[k]["refs"].append(ref)
    grupos[k]["val"].add(v["value"])


def ordem(r):
    return (re.sub(r"\d", "", r), int(re.sub(r"\D", "", r) or 0))


linhas, nd_mpn, nd_mouser, alertas, stock_alertas = [], [], [], [], []
cen = {1: 0.0, 10: 0.0, 100: 0.0}
cen_falta = {1: set(), 10: set(), 100: set()}
tot = {1: 0.0, 10: 0.0, 100: 0.0}
completo = {1: True, 10: True, 100: True}
for k in sorted(grupos, key=lambda k: ordem(sorted(grupos[k]["refs"], key=ordem)[0])):
    g = grupos[k]
    refs = sorted(g["refs"], key=ordem)
    n = len(refs)
    sem = k.startswith("SEM MPN")
    mpn = "—" if sem else k
    m = MOU.get(k, {}) if not sem else {}
    p = m.get("peca") or {}
    cod = p.get("MouserPartNumber") or "N/D"
    stock = str(p.get("AvailabilityInStock") or p.get("Availability") or "N/D")
    lcm = p.get("LifecycleStatus")
    cv = ("%s (Mouser 2026-09-25)" % lcm) if lcm else (CV.get(k) or "N/D")
    un = {q: (preco(p.get("PriceBreaks") or [], n * q) if p else None) for q in tot}
    try:
        st = int(str(p.get("AvailabilityInStock") or 0))
    except ValueError:
        st = 0
    alt = ALT_V.get(k)
    ap = ALTP.get(alt[0]) if alt else None
    try:
        ast = int(str((ap or {}).get("AvailabilityInStock") or 0))
    except ValueError:
        ast = 0
    if p and st < n * LOTE_STOCK:
        stock_alertas.append("%s (%s): %d em stock para %d por placa%s" % (k, ", ".join(refs), st, n,
            ("; alternativa verificada %s: %d em stock" % (alt[0], ast)) if alt else ""))
    for q in tot:     # cenario compravel: principal se ha stock; senao a alternativa verificada com stock
        usa = un[q]
        if (usa is None or st < n * q) and ap and ast >= n * q:
            usa = preco(ap.get("PriceBreaks") or [], n * q)
        if usa is None or (st < n * q and not (ap and ast >= n * q)):
            cen_falta[q].add(k)
        if usa is not None:
            cen[q] += usa * n * q
    for q in tot:
        if un[q] is None:
            completo[q] = False
        else:
            tot[q] += un[q] * n * q
    if sem:
        nd_mpn.append(", ".join(refs))
    elif not p:
        nd_mouser.append(k)
    if cv != "N/D" and not cv.lower().startswith(("activo", "production", "active", "new")):
        alertas.append("%s — %s" % (k, cv))
    linhas.append({"Refs": ", ".join(refs), "Qtd": n, "Valor": " / ".join(sorted(g["val"])), "Pegada": g["fp"],
                   "Fabricante": "N/D" if sem else fab(k), "MPN": mpn, "Mouser": cod, "Stock": stock,
                   "USD_1": "N/D" if un[1] is None else "%.4f" % un[1], "USD_10": "N/D" if un[10] is None else "%.4f" % un[10],
                   "USD_100": "N/D" if un[100] is None else "%.4f" % un[100], "Ciclo_vida": cv,
                   "Origem": "—" if sem else ("biblioteca 2Solve" if k in casa else "NOVO"),
                   "Alternativas": ("%s — %s" % ALT_V[k]) if k in ALT_V else ALT.get(k, "N/D"), "Notas": NOTA.get(k, "")})

cons = MOU.get("_consulta", {})
moeda = next((b.get("Currency") for v in MOU.values() if isinstance(v, dict) for b in (v.get("peca") or {}).get("PriceBreaks") or [] if b.get("Currency")), None) or "N/D (sem consulta)"
fonte = ("Mouser Search API, consulta de %s" % cons["quando"]) if cons else "**sem dados Mouser (modo degradado)**: preço, stock e código Mouser N/D"
with io.open(SAI + ".csv", "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(linhas[0]), delimiter=";")
    w.writeheader()
    w.writerows(linhas)

md = ["---", "projeto: IC2S Extension Board EBM2 V5 (6AI 4-20 mA)", "etapa: BOM preliminar (2shw-pcb:bom, modo preliminar)",
      "netlist: %s" % os.path.basename(NET), "fonte_dados: %s" % fonte.replace("**", ""), "moeda: %s" % moeda, "---", "",
      "# BOM preliminar — EBM2 V5", "",
      "**Só se liberta a Suprimentos com o Portão 1 assinado. Hardware não compra.**", "",
      "Fonte dos dados comerciais: %s. Ciclo de vida só com fonte e data; sem fonte é `N/D`, nunca «activo» por omissão." % fonte, "",
      "## 1 · Alertas", ""]
md += ["- **Sem MPN (%d linha(s)):** %s — precisam da curva do fabricante antes de fixar (ver §4)." % (len(nd_mpn), "; ".join(nd_mpn))] if nd_mpn else []
md += ["- **Ciclo de vida fora de «activo»:** " + "; ".join(alertas)] if alertas else ["- Ciclo de vida: nenhuma peça declarada fora de «activo» **entre as que têm fonte**; %d linhas sem fonte (`N/D`) até à consulta Mouser." % sum(1 for l in linhas if l["Ciclo_vida"] == "N/D")]
md += ["- **Sem dado Mouser:** %d MPN." % len(nd_mouser)] if nd_mouser else []
md += ["- **Stock Mouser abaixo de %d placas:**" % LOTE_STOCK] + ["  - " + s for s in stock_alertas] if stock_alertas else []
md += ["", "### Alternativas verificadas (mesma peça eléctrica, conferida no datasheet)", "",
       "| Principal | Alternativa | Stock Mouser | Evidência |", "|---|---|---:|---|"]
for k2, (a2, ev) in ALT_V.items():
    md.append("| `%s` | `%s` | %s | %s |" % (k2, a2, (ALTP.get(a2) or {}).get("AvailabilityInStock") or "N/D", ev))
md += ["", "## 2 · Linhas (%d, %d componentes montados)" % (len(linhas), sum(l["Qtd"] for l in linhas)), "",
       "| Refs | Qtd | Valor | Pegada | Fabricante | MPN | Mouser | Stock | Unit. lote 1 | Unit. lote 10 | Unit. lote 100 | Ciclo de vida | Origem | Notas |",
       "|---|---:|---|---|---|---|---|---|---:|---:|---:|---|---|---|"]
for l in linhas:
    md.append("| %s | %d | %s | %s | %s | `%s` | %s | %s | %s | %s | %s | %s | %s | %s |" % (
        l["Refs"], l["Qtd"], l["Valor"], l["Pegada"], l["Fabricante"], l["MPN"], l["Mouser"], l["Stock"],
        l["USD_1"], l["USD_10"], l["USD_100"], l["Ciclo_vida"], l["Origem"], l["Notas"]))
md += ["", "## 3 · Totais da placa (%s)" % moeda, "", "| Lote | Total | Por placa |", "|---:|---:|---:|"]
sem_preco = [l["Refs"] for l in linhas if l["USD_1"] == "N/D"]
cen_txt = []
for q in tot:
    cen_txt.append("| %d | %.2f | %.2f | %s |" % (q, cen[q], cen[q] / q, ", ".join("`%s`" % x for x in sorted(cen_falta[q])) or "—"))
for q in tot:
    if completo[q]:
        md.append("| %d | %.2f | %.2f |" % (q, tot[q], tot[q] / q))
    elif cons and len(sem_preco) < len(linhas):
        md.append("| %d | parcial %.2f (faltam %d linhas) | parcial %.2f |" % (q, tot[q], len(sem_preco), tot[q] / q))
    else:
        md.append("| %d | N/D | N/D |" % q)
if sem_preco and cons:
    md += ["", "Linhas sem preço (fora do parcial): " + "; ".join(sem_preco) + "."]
md += ["", "Preço no escalão que a quantidade do lote atinge (qtd por placa × placas); mínimos e múltiplos de embalagem "
       "não somados — Suprimentos confirma no carrinho."]
if cons:
    md += ["", "### Cenário comprável hoje na Mouser", "",
           "Principal quando há stock para o lote; senão a alternativa verificada com stock. As linhas em «sem stock» "
           "entram a preço de lista mas **não se compram hoje** na Mouser.", "",
           "| Lote | Total | Por placa | Sem stock para o lote |", "|---:|---:|---:|---|"] + cen_txt
md += ["", "## 4 · Compra antecipada (críticos / long-lead) e acções", "",
       "| Peça | Porquê | Acção sugerida |", "|---|---|---|",
       "| `ISO7141CCDBQR` (U6) | **0 em stock na Mouser em todas as variantes** (DBQR, DBQ, DBQRG4; 2026-09-25); prazo 112 dias (DBQR) / 63 dias (DBQ, tubo). Única peça que atravessa a barreira; a versão F (saída por defeito baixa) **não serve**: deixava o ADC seleccionado com o barramento desligado | Encomendar `ISO7141CCDBQ` à fábrica logo após o Portão 1, ou outro distribuidor autorizado |",
       "| `3413.0002.22` (F3-F8, 6 por placa) | 0 em stock, **prazo 269 dias** | Protótipo com `3413.0002.11` (mesma peça, 100 un. em fita; 8838 em stock) |",
       "| `ADR4525WBRZ-R7` (U2) | Família inteira **«Restricted Availability»** na Mouser (a BRZ original sem preço nem stock; trocada na tanda B) | Comprar com o protótipo (2147 em stock). Grau A **não** serve: 8 ppm/°C bowtie contra 4 |",
       "| `ADR4525WBRZ-R7` (U2): grau W | A pág. 41 do ADR45xx Rev. G avisa que o modelo automóvel «may have specifications that differ from the commercial models». "
       "Conferido (2026-09-25): as tabelas 1-2 (págs. 3-5) só têm os graus A, B, C e D, **sem coluna W**; a guia de encomenda (pág. 40) dá o WBRZ-R7 como grau B, −40…+125 °C, SOIC-8. "
       "O datasheet **não publica** nenhuma especificação própria do W; se existir, só a ADI a dá | Decisão mantida (U2 = WBRZ-R7, fechada pelo projectista). "
       "Pedir à ADI, com a compra, a confirmação de que o WBRZ cumpre a tabela 2 do grau B (ou o relatório Automotive Reliability) |",
       "| LED `KG EELP41.22` (3) | 0 em stock pelo código comprido | Pedir por `Q65113A7469` (mesmo tipo e bin; 15898 em stock) |",
       "| `824520361` (D12-D17, 6 por placa) | 82 em stock: chega para 13 placas; prazo 154 dias | Reservar para o protótipo |",
       "| `ERA3AEB5621V`, `ERA8AEB111V` | Prazo de fábrica 343 dias (Mouser); stock 8540 / 7280 | Comprar com o protótipo |",
       "| `C1` | **Fechado na tanda C:** TDK `C3225X7R2A225K230AB` em 1210 (pior caso 1,18 µF a 30,4 V). Descartados: TDK X7S 1206 (0,89 µF) e Murata GRM31CR72A225KA73L / GRM32ER72A225KA35L (obsoleto / fim de vida) | Land pattern TDK (PA 2,0-2,4 mm) contra a pegada IPC do projecto (1,8 mm): conferir na F3 |",
       "| `R3` | **Fechado na tanda B:** KOA `SG73P2ATTD1500F`, pulso conferido (~4x) | — |",
       "| `C5`, `C11` | **Conferido:** curva TDK dá ≥ 1,26 µF no pior caso | — |",
       "", "```yaml", "evidencia:", "  skill: 2shw-pcb:bom", "  modo: preliminar",
       "  artefatos: [%s.md, %s.csv]" % (os.path.basename(SAI), os.path.basename(SAI)),
       "  itens: %d" % len(linhas), "  alertas_ciclo_vida: %d" % len(alertas),
       "  itens_nd: %d" % (len(nd_mpn) + len(nd_mouser)),
       "  total_1un: %s" % ("%.2f" % tot[1] if completo[1] else "N/D"),
       "  total_100un: %s" % ("%.2f" % tot[100] if completo[100] else "N/D"),
       "  fonte_dados: %s" % ("wrapper(%s)" % cons["quando"] if cons else "sem_dados"), "```", ""]
io.open(SAI + ".md", "w", encoding="utf-8").write("\n".join(md))
print("BOM: %d linhas, %d componentes montados, %d fora da BOM | sem MPN: %d | sem Mouser: %d | fonte: %s"
      % (len(linhas), sum(l["Qtd"] for l in linhas), len(fora), len(nd_mpn), len(nd_mouser), "Mouser" if cons else "nenhuma"))
