# -*- coding: utf-8 -*-
"""Prepara o pacote da etapa 2.3 (verificacao de pinagem, sessao independente).

Tudo sai dos ficheiros: a netlist exportada agora (com o nome de cada pino no simbolo), os
.kicad_sch (lib_id e folha), as pegadas do projecto (ilhas) e datasheets escolhidos PELO
CONTEUDO (localiza_datasheets.py + revisao manual). Nada de conclusoes da sessao de autoria:
o pacote diz o que conferir, nao o que se espera encontrar.

Uso: python prepara_pacote_2_3.py
"""
import glob, hashlib, io, os, re, shutil, subprocess, sys
from netlist_diff import parse, filhos, val

RAIZ = r"C:\hw\hw-ebm2-v5"
KI = os.path.join(RAIZ, "KiCad_EBM2_V5")
OUT = os.path.join(RAIZ, "Documentos", "verificacao_2_3")
CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
SCR = os.path.expanduser(r"~\.claude\projects\C--Users-Javier-Rivadineira\18536fc6-f453-4a6a-97aa-db52eff44a3a\tool-results")
EBM7REF = glob.glob(r"C:\hw\hw-ebm7-v2.2\Desenvolvimento_IC2S-EBM7-2608-V2.2\Projeto_IC2S-EBM7-2608-V2.2\Documentos_de_Refer*")[0]
DOWN = os.path.expanduser(r"~\Downloads")
DS_TMP = r"C:\Users\JAVIER~1\AppData\Local\Temp\claude\C--Users-Javier-Rivadineira\18536fc6-f453-4a6a-97aa-db52eff44a3a\scratchpad\ds"

# datasheet escolhido para cada familia: (ficheiro de origem, texto que TEM de estar na 1.a pagina)
DS = {
    "TPS7A4001": (os.path.join(EBM7REF, "TI_TPS7A4001.pdf"), "TPS7A4001"),
    "SPX3819": (None, "SPX3819"),                      # procurado abaixo (1016_SPX3819.pdf)
    "ADR4525": (os.path.join(DOWN, "adr4520_4525_4530_4533_4540_4550.pdf"), "ADR4525"),
    "TL431": (os.path.join(EBM7REF, "TI_TL431.pdf"), "TL431"),
    "ISO7141": (os.path.join(EBM7REF, "TI_ISO7141CC.pdf"), "ISO7141"),
    "MCP1824": (os.path.join(EBM7REF, "22070a.pdf"), "MCP1824"),
    "MCP3208": (os.path.join(DOWN, "21298e.pdf"), "MCP3208"),
    "AL5809": (os.path.join(DOWN, "AL5809.pdf"), "AL5809"),
    "SMA6J33A": (None, "SMA6J"),                       # Bourns_SMA6J33A-Q.pdf
    "MBR1H100SF": (os.path.join(SCR, "webfetch-1790203902626-3ncrcx.pdf"), "MBR1H100"),
    "824520361": (os.path.join(EBM7REF, "Wurth_824520361_SMBJ36A_DO-214AA.pdf"), "824520361"),
    "BAV199": (None, "BAV199"),                        # BAV199LT1-D.PDF
    "BAT46W": (os.path.join(SCR, "webfetch-1790247975568-happxg.pdf"), "BAT46W"),        # Diodes DS30044 (BAT46W-7-F)
    "KG EELP41.22": (os.path.join(DS_TMP, "KG-EELP41-22.pdf"), "EELP41"),
    "Harwin M20-782": (None, "M20-78"),                # Harwin_M20-782_plano.pdf
}
POR_NOME = {"SPX3819": "1016_SPX3819.pdf", "SMA6J33A": "Bourns_SMA6J33A-Q.pdf", "BAV199": "BAV199LT1-D.PDF",
            "Harwin M20-782": "Harwin_M20-782_plano.pdf"}

# que datasheet serve cada referencia (pelo MPN/valor da netlist)
def familia(v, mpn):
    s = (mpn or v or "").upper()
    for k, pat in (("TPS7A4001", "TPS7A4001"), ("SPX3819", "SPX3819"), ("ADR4525", "ADR4525"), ("TL431", "TL431"),
                   ("ISO7141", "ISO7141"), ("MCP1824", "MCP1824"), ("MCP3208", "MCP3208"), ("AL5809", "AL5809"),
                   ("SMA6J33A", "SMA6J33A"), ("MBR1H100SF", "MBR1H100"), ("824520361", "824520361"),
                   ("BAV199", "BAV199"), ("BAT46W", "BAT46W"), ("KG EELP41.22", "EELP41"), ("Harwin M20-782", "M20-782")):
        if pat in s:
            return k
    return None


def md5(f):
    return hashlib.md5(open(f, "rb").read()).hexdigest()[:12]


def main():
    import fitz
    os.makedirs(os.path.join(OUT, "datasheets"), exist_ok=True)
    # ---------------------------------------------------------------- datasheets, conferidos pelo conteudo
    achados = {}
    for k, (f, txt) in DS.items():
        if f is None:
            cand = [g for g in glob.glob(os.path.join(r"C:\hw", "**", POR_NOME[k]), recursive=True)]
            f = cand[0] if cand else None
        if not f or not os.path.exists(f):
            achados[k] = None; continue
        t = " ".join(fitz.open(f)[0].get_text().split())
        if txt not in t and txt.upper() not in t.upper():
            t2 = " ".join(" ".join(p.get_text() for p in list(fitz.open(f))[:3]).split())
            if txt.upper() not in t2.upper():
                sys.exit("ABORTA: %s nao contem %r: %s" % (k, txt, f))
        dst = os.path.join(OUT, "datasheets", re.sub(r"[^\w.-]", "_", k) + "__" + os.path.basename(f).replace("webfetch-", "fetch-"))
        shutil.copy2(f, dst)
        achados[k] = (os.path.basename(dst), md5(dst), fitz.open(dst).page_count, f)
    # ---------------------------------------------------------------- netlist nova, com nomes de pino
    net = os.path.join(OUT, "EBM2_V5.net")
    subprocess.run([CLI, "sch", "export", "netlist", "-o", net, os.path.join(KI, "IC2S_Extension_Board-EBM2_V5.kicad_sch")], capture_output=True)
    pdf = os.path.join(OUT, "esquematico_EBM2_V5.pdf")
    subprocess.run([CLI, "sch", "export", "pdf", "-o", pdf, os.path.join(KI, "IC2S_Extension_Board-EBM2_V5.kicad_sch")], capture_output=True)
    arv = parse(io.open(net, encoding="utf-8").read())
    comps = {}
    for sec in filhos(arv, "components"):
        for c in filhos(sec, "comp"):
            ref = val(c, "ref"); mpn = None
            for fs in filhos(c, "fields"):
                for fd in filhos(fs, "field"):
                    if val(fd, "name") == "MPN" and isinstance(fd[-1], str) and fd[-1] != "MPN": mpn = fd[-1]
            ls = filhos(c, "libsource")
            comps[ref] = dict(valor=val(c, "value"), pegada=val(c, "footprint"), mpn=mpn,
                              lib=("%s:%s" % (val(ls[0], "lib"), val(ls[0], "part"))) if ls else "?",
                              folha=(filhos(c, "sheetpath")[0][1][1] if filhos(c, "sheetpath") else "?"), pinos={})
    for sec in filhos(arv, "nets"):
        for r in filhos(sec, "net"):
            nome = val(r, "name")
            for nd in filhos(r, "node"):
                ref, pin = val(nd, "ref"), val(nd, "pin")
                if ref in comps:
                    comps[ref]["pinos"][pin] = (val(nd, "pinfunction") or "", val(nd, "pintype") or "", nome)
    alvo = sorted([r for r in comps if re.match(r"^(U|D|P)\d", r)], key=lambda z: (re.sub(r"\d", "", z), int(re.sub(r"\D", "", z))))
    # ---------------------------------------------------------------- pegadas: ilhas
    def ilhas(peg):
        lib, nome = peg.split(":")
        f = os.path.join(KI, "footprints", "EBM2_V5.pretty", nome + ".kicad_mod")
        if not os.path.exists(f): return "pegada nao encontrada em %s" % f, ""
        t = io.open(f, encoding="utf-8").read()
        d = re.search(r'\(descr "([^"]*)"', t)
        ps = re.findall(r'\(pad "([^"]+)" \w+ \w+\s+\(at ([-\d.]+) ([-\d.]+)(?: [-\d.]+)?\)\s+\(size ([\d.]+) ([\d.]+)\)', t)
        return ("; ".join("%s @(%s, %s) %sx%s" % p for p in ps), d.group(1) if d else "")
    # ---------------------------------------------------------------- inventario
    L = ["# Inventário de pinagem — EBM2 V5 (entrada da etapa 2.3)\n",
         "Gerado por `ferramentas/prepara_pacote_2_3.py` a partir da netlist exportada agora (`EBM2_V5.net`),",
         "das pegadas do projecto e dos datasheets desta pasta. **Não contém conclusões da sessão que desenhou.**\n",
         "Colunas por pino: número no símbolo → nome do pino no símbolo → tipo → rede. A verificação é conferir",
         "cada linha contra o datasheet (número, nome, função, direcção, nível) e a pegada contra o desenho do",
         "encapsulamento (ilha 1, marca de polaridade).\n"]
    grupos = {}
    for r in alvo:
        c = comps[r]
        chave = (c["lib"], c["valor"], c["pegada"], c["mpn"])
        grupos.setdefault(chave, []).append(r)
    for (lib, v, peg, mpn), refs in grupos.items():
        fam = familia(v, mpn)
        ds = achados.get(fam) if fam else None
        il, descr = ilhas(peg) if peg and ":" in peg else ("—", "")
        L.append("## %s — `%s` (%s)\n" % (", ".join(refs), mpn or v, v))
        L.append("- Símbolo: `%s` · Pegada: `%s` · Folha: `%s`" % (lib, peg, comps[refs[0]]["folha"]))
        L.append("- Datasheet: %s" % (("`datasheets/%s` (md5 %s, %d págs.)" % (ds[0], ds[1], ds[2])) if ds else "**FALTA — obter antes de concluir**"))
        L.append("- Ilhas da pegada: %s" % il)
        if descr: L.append("- Nota da pegada: %s" % descr)
        L.append("\n| Ref | Pino | Nome no símbolo | Tipo | Rede |\n|---|---|---|---|---|")
        for r in refs:
            for pin in sorted(comps[r]["pinos"], key=lambda z: (len(z), z)):
                pf, pt, nome = comps[r]["pinos"][pin]
                L.append("| %s | %s | %s | %s | `%s` |" % (r, pin, pf or "—", pt, nome))
        L.append("")
    io.open(os.path.join(OUT, "inventario_pinos_EBM2_V5.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
    # ---------------------------------------------------------------- lista de datasheets
    D = ["| Família | Ficheiro | md5 | Págs. | Origem |", "|---|---|---|---|---|"]
    for k, a in achados.items():
        D.append("| %s | %s | %s | %s | %s |" % (k, ("`%s`" % a[0]) if a else "**FALTA**", a[1] if a else "", a[2] if a else "", a[3] if a else ""))
    io.open(os.path.join(OUT, "datasheets", "LISTA.md"), "w", encoding="utf-8").write(
        "# Datasheets do pacote 2.3 — escolhidos pelo conteúdo, não pelo nome\n\n" + "\n".join(D) + "\n")
    shutil.copy2(os.path.join(RAIZ, "Documentos", "intencao_EBM2_V5.md"), os.path.join(OUT, "intencao_EBM2_V5.md"))
    print("componentes no inventario:", len(alvo), "em", len(grupos), "grupos | datasheets:",
          sum(1 for a in achados.values() if a), "de", len(achados), "| em falta:", [k for k, a in achados.items() if not a])


if __name__ == "__main__":
    main()
