# -*- coding: utf-8 -*-
"""Pacote da 2.3b para a intencao rev. 2.5b (correccoes da 2.3b rev. 2.4), sessao independente.

Nao toca nos pacotes anteriores. Reutiliza os datasheets do pacote da rev. 2.4 (escolhidos pelo conteudo,
ja com TPS2661x, SMBJ33A da Diodes e as fichas da TDK) e junta os relatorios da rev. 2.4 para comparacao.
Uso: python prepara_pacote_2_3b_rev25.py
"""
import glob, hashlib, io, os, shutil, subprocess, sys
import fitz

RAIZ = r"C:\hw\hw-ebm2-v5"
OUT = os.path.join(RAIZ, "Documentos", "verificacao_2_3b_rev25")
P24 = os.path.join(RAIZ, "Documentos", "verificacao_2_3b_rev24")
CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"


def md5(f):
    return hashlib.md5(open(f, "rb").read()).hexdigest()[:12]


def main():
    if os.path.exists(OUT):
        sys.exit("ABORTA: %s ja existe" % OUT)
    ds = os.path.join(OUT, "datasheets")
    os.makedirs(ds)
    linhas = ["| Ficheiro | md5 | Págs. | Origem |", "|---|---|---|---|"]
    for f in sorted({os.path.normcase(x): x for x in glob.glob(os.path.join(P24, "datasheets", "*.pdf")) + glob.glob(os.path.join(P24, "datasheets", "*.PDF"))}.values()):
        shutil.copy2(f, ds)
        linhas.append("| `%s` | %s | %d | pacote 2.3b rev. 2.4 |" % (os.path.basename(f), md5(f), fitz.open(f).page_count))
    io.open(os.path.join(ds, "LISTA.md"), "w", encoding="utf-8").write(
        "# Datasheets do pacote 2.3b rev. 2.5b — escolhidos pelo conteúdo\n\n" + "\n".join(linhas) + "\n\n"
        "SMBJ33A (Diodes DS19002) e C3216X5R1H106K160AB (TDK: catálogo geral e ficha com a curva DC bias) "
        "fornecidos pelo projectista em 2026-09-24.\n")
    ant = os.path.join(OUT, "rev24_anterior")
    os.makedirs(ant)
    for f in ("verificacao_aplicacao_EBM2_V5_rev24.md", "verificacao_aplicacao_EBM2_V5_rev24_rows.json",
              "recalculo_independente_dimensionamento_EBM2_V5_rev24.md"):
        shutil.copy2(os.path.join(P24, f), ant)
    sch = os.path.join(RAIZ, "KiCad_EBM2_V5", "IC2S_Extension_Board-EBM2_V5.kicad_sch")
    for args in (["netlist", "--format", "kicadsexpr", "-o", os.path.join(OUT, "EBM2_V5.net")],
                 ["pdf", "-o", os.path.join(OUT, "esquematico_EBM2_V5.pdf")]):
        r = subprocess.run([CLI, "sch", "export"] + args + [sch], capture_output=True)
        assert r.returncode == 0, r.stderr
    for f in ("intencao_EBM2_V5.md", "escopo_EBM2_V5.md", "planejamento_pcb_EBM2_V5.md"):
        shutil.copy2(os.path.join(RAIZ, "Documentos", f), OUT)
    print("datasheets:", len(linhas) - 2, "| netlist, PDF, documentos e relatorios da rev. 2.4 em", OUT)


if __name__ == "__main__":
    main()
