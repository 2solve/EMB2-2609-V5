# -*- coding: utf-8 -*-
"""Prepara o pacote da etapa 2.3b (verificacao de aplicacao, sessao independente).

Reutiliza os datasheets da 2.3 (ja escolhidos pelo conteudo) e junta os das pecas de proteccao
que a 2.3b precisa (fusiveis, NTC). Cada PDF novo e conferido pelo texto antes de copiar.
Uso: python prepara_pacote_2_3b.py
"""
import glob, hashlib, io, os, re, shutil, subprocess, sys
import fitz

RAIZ = r"C:\hw\hw-ebm2-v5"
OUT = os.path.join(RAIZ, "Documentos", "verificacao_2_3b")
P23 = os.path.join(RAIZ, "Documentos", "verificacao_2_3", "datasheets")
CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
EBM7REF = glob.glob(r"C:\hw\hw-ebm7-v2.2\Desenvolvimento_IC2S-EBM7-2608-V2.2\Projeto_IC2S-EBM7-2608-V2.2\Documentos_de_Refer*")[0]
EXTRA = {  # ficheiro de origem -> texto que tem de estar nas 3 primeiras paginas
    os.path.join(EBM7REF, "Eaton_fusible_lento.pdf"): "CC12H",
    os.path.join(EBM7REF, "Schurter_USFF1206_3413.pdf"): "3413",
    os.path.join(EBM7REF, "ntcs0603e3t.pdf"): "NTCS0603",
}


def md5(f):
    return hashlib.md5(open(f, "rb").read()).hexdigest()[:12]


def main():
    ds = os.path.join(OUT, "datasheets")
    os.makedirs(ds, exist_ok=True)
    linhas = ["| Ficheiro | md5 | Págs. | Origem |", "|---|---|---|---|"]
    for f in sorted(glob.glob(os.path.join(P23, "*.pdf"))):
        shutil.copy2(f, ds)
        linhas.append("| `%s` | %s | %d | pacote 2.3 |" % (os.path.basename(f), md5(f), fitz.open(f).page_count))
    for f, txt in EXTRA.items():
        t = " ".join(" ".join(p.get_text() for p in list(fitz.open(f))[:3]).split())
        if txt.upper() not in t.upper():
            sys.exit("ABORTA: %s nao contem %r" % (f, txt))
        dst = os.path.join(ds, os.path.basename(f))
        shutil.copy2(f, dst)
        linhas.append("| `%s` | %s | %d | %s |" % (os.path.basename(f), md5(dst), fitz.open(dst).page_count, f))
    io.open(os.path.join(ds, "LISTA.md"), "w", encoding="utf-8").write(
        "# Datasheets do pacote 2.3b — escolhidos pelo conteúdo\n\n" + "\n".join(linhas) + "\n")
    sch = os.path.join(RAIZ, "KiCad_EBM2_V5", "IC2S_Extension_Board-EBM2_V5.kicad_sch")
    subprocess.run([CLI, "sch", "export", "netlist", "--format", "kicadsexpr", "-o", os.path.join(OUT, "EBM2_V5.net"), sch], capture_output=True)
    subprocess.run([CLI, "sch", "export", "pdf", "-o", os.path.join(OUT, "esquematico_EBM2_V5.pdf"), sch], capture_output=True)
    for f in ("intencao_EBM2_V5.md", "escopo_EBM2_V5.md"):
        shutil.copy2(os.path.join(RAIZ, "Documentos", f), OUT)
    print("datasheets:", len(linhas) - 2, "| netlist, PDF, intencao e escopo copiados para", OUT)


if __name__ == "__main__":
    main()
