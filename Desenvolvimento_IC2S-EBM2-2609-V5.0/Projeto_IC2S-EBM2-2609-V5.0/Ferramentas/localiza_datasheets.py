# -*- coding: utf-8 -*-
"""Localiza o datasheet de cada peca PELO CONTEUDO (texto das 3 primeiras paginas), nunca pelo nome.

Motivo: em 2026-09-23 o ficheiro «eaton-cc12h-high-i2t-chip-fuses-data-sheet.pdf» da pasta de
referencia da EBM7 continha o datasheet do ADR45xx, e o «iso7131cc.pdf» ja tinha sido tomado
pelo do ISO7141. Uso: python localiza_datasheets.py saida.json
"""
import fitz, glob, hashlib, json, os, re, sys

PASTAS = [r"C:\hw", os.path.expanduser(r"~\Downloads")]
# peca -> (padrao que tem de aparecer no texto, padrao que confirma a variante)
PECAS = {
    "TPS7A4001": (r"TPS7A40", r"TPS7A4001"),
    "SPX3819": (r"SPX3819", r"SPX3819"),
    "ADR4525": (r"ADR4525", r"ADR4525"),
    "TL431": (r"TL431", r"TL431"),
    "ISO7141": (r"ISO7141", r"ISO7141"),
    "MCP1824": (r"MCP1824", r"MCP1824"),
    "MCP3208": (r"MCP3208", r"MCP3204/3208|MCP3208"),
    "AL5809": (r"AL5809", r"AL5809"),
    "SMA6J33A": (r"SMA6J", r"SMA6J33A|SMA6J"),
    "MBR1H100": (r"MBR1H100", r"MBR1H100"),
    "824520361": (r"824520361|SMBJ36A", r"824520361"),
    "BAV199": (r"BAV199", r"BAV199"),
    "BAT46W": (r"BAT46W", r"BAT46W"),
    "LG Q396": (r"Q396|LG Q396", r"Q396"),
    "M20-782 (Harwin)": (r"M20-78|M20-782", r"M20-78"),
    "NTCS0603": (r"NTCS0603", r"NTCS0603"),
}


def texto(pdf, n=3):
    try:
        d = fitz.open(pdf)
        return " ".join(d[i].get_text() for i in range(min(n, d.page_count)))
    except Exception:
        return ""


def main():
    pdfs = []
    for pasta in PASTAS:
        pdfs += glob.glob(os.path.join(pasta, "**", "*.pdf"), recursive=True)
    vistos, res = {}, {k: [] for k in PECAS}
    for f in pdfs:
        if "revisao_F2" in f or "esquematico_" in os.path.basename(f):
            continue
        try:
            h = hashlib.md5(open(f, "rb").read()).hexdigest()
        except Exception:
            continue
        if h in vistos:
            continue
        vistos[h] = f
        t = texto(f)
        for k, (pat, conf) in PECAS.items():
            if re.search(pat, t):
                titulo = bool(re.search(conf, t[:1500]))
                res[k].append({"ficheiro": f, "md5": h[:12], "no_topo": titulo})
    for k in res:
        res[k].sort(key=lambda x: (not x["no_topo"], len(x["ficheiro"])))
    json.dump(res, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    for k, v in res.items():
        print("%-18s %d candidato(s)%s" % (k, len(v), (" | melhor: %s%s" % (os.path.basename(v[0]["ficheiro"]), " (no topo)" if v[0]["no_topo"] else "")) if v else "  <-- FALTA"))


if __name__ == "__main__":
    main()
