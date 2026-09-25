# -*- coding: utf-8 -*-
"""Pacote do Portao 1 (P1) da EBM2 V5: os 3 blocos da F2 + a verificacao cruzada (modelo diferente do autor).

Gera Documentos/portao1/ a partir do estado ACTUAL do projecto (netlist exportada agora, PDF da 2.5, BOM,
intencao, mapa de pinos, datasheets escolhidos pelo conteudo). Correr de novo depois de qualquer tanda.
Recusa se o PDF da 2.5 for mais velho que o esquematico (entregar um PDF desactualizado ao portao e o erro
que este script existe para impedir).
Uso: python prepara_pacote_portao1.py
"""
import glob, hashlib, io, os, shutil, subprocess, sys

R = r"C:\hw\hw-ebm2-v5"
K = os.path.join(R, "KiCad_EBM2_V5")
D = os.path.join(R, "Documentos")
OUT = os.path.join(D, "portao1")
CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
SCH = os.path.join(K, "IC2S_Extension_Board-EBM2_V5.kicad_sch")
PDF = os.path.join(D, "revisao_F2_2.5", "EBM2_V5_F2_revisao_2026-09-25.pdf")
DL = r"C:\Users\Javier Rivadineira\Downloads"
EXTRA_DS = {  # datasheets fornecidos depois do pacote 2.3b rev25 (ficheiro -> texto obrigatorio)
    os.path.join(DL, "SG73P.pdf"): "SG73P",
    os.path.join(DL, "c1608x5r1e22k0.pdf"): "C1608X5R1E225K080AB",
    os.path.join(DL, "C3225X7R2A225K230AB.pdf"): "C3225X7R2A225K230AB",
    os.path.join(DL, "C3216X7S2A225K160AB.pdf"): "C3216X7S2A225K160AB",
    os.path.join(DL, "ProductDetailed.pdf"): "C3216X5R1H106K160AB",
}


def md5(f):
    return hashlib.md5(open(f, "rb").read()).hexdigest()[:12]


mais_novo = max(os.path.getmtime(f) for f in glob.glob(os.path.join(K, "*.kicad_sch")))
if os.path.getmtime(PDF) < mais_novo:
    sys.exit("ABORTA: o PDF da 2.5 e mais velho que o esquematico. Correr gera_pdf_F2.py primeiro.")
# Os relatorios da verificacao cruzada sao o registo do portao: guardam-se antes de recriar a pasta.
guardados = {os.path.basename(f): io.open(f, "rb").read() for f in glob.glob(os.path.join(OUT, "relatorio_*.md"))}
if os.path.exists(OUT):
    shutil.rmtree(OUT)
os.makedirs(os.path.join(OUT, "datasheets"))
for nome, dados in guardados.items():
    io.open(os.path.join(OUT, nome), "wb").write(dados)
subprocess.run([CLI, "sch", "export", "netlist", "--format", "kicadsexpr", "-o", os.path.join(OUT, "EBM2_V5.net"), SCH],
               capture_output=True, check=True)
r = subprocess.run([CLI, "sch", "erc", "--format", "json", "--severity-error", "-o", os.path.join(OUT, "erc.json"), SCH],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
for f in (PDF, os.path.join(D, "bom_preliminar_EBM2_V5.md"), os.path.join(D, "bom_preliminar_EBM2_V5.csv"),
          os.path.join(D, "bom_dados_mouser_2026-09-25.json"), os.path.join(D, "bom_dados_mouser_alternativas_2026-09-25.json"),
          os.path.join(D, "intencao_EBM2_V5.md"), os.path.join(D, "escopo_EBM2_V5.md"), os.path.join(D, "mapa_pinos_EBM2_V5.md"),
          os.path.join(D, "diagrama_blocos_EBM2_V5.svg"), os.path.join(D, "revisao_F2_2.5", "LEIA-ME_F2_2.5.md"),
          os.path.join(D, "tabela_correspondencia_refs_EBM2_V5.md"), os.path.join(D, "tabela_correspondencia_refs_EBM2_V5.csv"),
          os.path.join(R, "ferramentas", "portao1", "LEIA-ME_verificacao_cruzada_P1.md"),
          os.path.join(R, "ferramentas", "portao1", "checklist_P1_projetista.md")):
    shutil.copy2(f, OUT)
vistos, linhas = set(), ["| Ficheiro | md5 | Origem |", "|---|---|---|"]
for f in sorted(glob.glob(os.path.join(D, "verificacao_2_3b_rev25", "datasheets", "*"))):
    if f.lower().endswith(".pdf") and os.path.basename(f).lower() not in vistos:
        vistos.add(os.path.basename(f).lower())
        shutil.copy2(f, os.path.join(OUT, "datasheets"))
        linhas.append("| `%s` | %s | pacote 2.3b rev. 2.5 |" % (os.path.basename(f), md5(f)))
import fitz  # noqa: E402
for f, txt in EXTRA_DS.items():
    if not os.path.exists(f):
        continue
    t = " ".join(p.get_text() for p in list(fitz.open(f))[:3])
    if txt not in t:
        sys.exit("ABORTA: %s nao contem %r" % (f, txt))
    dst = os.path.join(OUT, "datasheets", os.path.basename(f))
    shutil.copy2(f, dst)
    linhas.append("| `%s` | %s | Downloads do projectista (conferido pelo conteúdo: %s) |" % (os.path.basename(f), md5(dst), txt))
io.open(os.path.join(OUT, "datasheets", "LISTA.md"), "w", encoding="utf-8").write(
    "# Datasheets do pacote do Portão 1\n\n" + "\n".join(linhas) + "\n")
print("pacote:", OUT, "| ERC:", r.stdout.strip().splitlines()[0] if r.stdout else "?", "| datasheets:", len(linhas) - 2,
      "| PDF md5", md5(PDF))
