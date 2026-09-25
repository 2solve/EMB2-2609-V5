# -*- coding: utf-8 -*-
"""Pacote da 2.3b para a intencao rev. 2.4 (TPS26613 + trilho +12V_TPS), sessao independente.

Nao toca no pacote da primeira 2.3b (verificacao_2_3b/), que guarda os resultados dessa corrida.
Reutiliza os datasheets de la (escolhidos pelo conteudo) e junta o TPS2661x, conferido pelo texto.
Uso: python prepara_pacote_2_3b_rev24.py
"""
import glob, hashlib, io, os, shutil, subprocess, sys
import fitz

RAIZ = r"C:\hw\hw-ebm2-v5"
OUT = os.path.join(RAIZ, "Documentos", "verificacao_2_3b_rev24")
P1 = os.path.join(RAIZ, "Documentos", "verificacao_2_3b", "datasheets")
CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
EBM7REF = glob.glob(r"C:\hw\hw-ebm7-v2.2\Desenvolvimento_IC2S-EBM7-2608-V2.2\Projeto_IC2S-EBM7-2608-V2.2\Documentos_de_Refer*")[0]
EXTRA = {os.path.join(EBM7REF, "TI_TPS2661x.pdf"): "TPS26613"}   # ficheiro -> texto obrigatorio nas 3 primeiras pags.
SAI = {"AL5809__AL5809.pdf", "BAT46W__fetch-1790247975568-happxg.pdf"}   # pecas que sairam na rev. 2.4


def md5(f):
    return hashlib.md5(open(f, "rb").read()).hexdigest()[:12]


def main():
    if os.path.exists(OUT):
        sys.exit("ABORTA: %s ja existe" % OUT)
    ds = os.path.join(OUT, "datasheets")
    os.makedirs(ds)
    linhas = ["| Ficheiro | md5 | Págs. | Origem |", "|---|---|---|---|"]
    for f in sorted(glob.glob(os.path.join(P1, "*.pdf"))):
        if os.path.basename(f) in SAI:
            continue
        shutil.copy2(f, ds)
        linhas.append("| `%s` | %s | %d | pacote 2.3b |" % (os.path.basename(f), md5(f), fitz.open(f).page_count))
    for f, txt in EXTRA.items():
        t = " ".join(" ".join(p.get_text() for p in list(fitz.open(f))[:3]).split())
        if txt.upper() not in t.upper():
            sys.exit("ABORTA: %s nao contem %r" % (f, txt))
        dst = os.path.join(ds, os.path.basename(f))
        shutil.copy2(f, dst)
        linhas.append("| `%s` | %s | %d | %s |" % (os.path.basename(f), md5(dst), fitz.open(dst).page_count, f))
    linhas.append("\n**Sem datasheet no disco** (procurado pelo conteúdo em `Downloads` e `C:\\hw`): `SMBJ33A-13-F` "
                  "(`D601`-`D606`) e `C3216X5R1H106K160AB` (`C642`). Linhas que dependam deles: `missing data`.")
    io.open(os.path.join(ds, "LISTA.md"), "w", encoding="utf-8").write(
        "# Datasheets do pacote 2.3b rev. 2.4 — escolhidos pelo conteúdo\n\n" + "\n".join(linhas) + "\n")
    sch = os.path.join(RAIZ, "KiCad_EBM2_V5", "IC2S_Extension_Board-EBM2_V5.kicad_sch")
    for args in (["netlist", "--format", "kicadsexpr", "-o", os.path.join(OUT, "EBM2_V5.net")],
                 ["pdf", "-o", os.path.join(OUT, "esquematico_EBM2_V5.pdf")]):
        r = subprocess.run([CLI, "sch", "export"] + args + [sch], capture_output=True)
        assert r.returncode == 0, r.stderr
    for f in ("intencao_EBM2_V5.md", "escopo_EBM2_V5.md", "planejamento_pcb_EBM2_V5.md"):
        shutil.copy2(os.path.join(RAIZ, "Documentos", f), OUT)
    print("datasheets:", len(glob.glob(os.path.join(ds, "*.pdf"))), "| netlist, PDF e documentos em", OUT)


if __name__ == "__main__":
    main()
