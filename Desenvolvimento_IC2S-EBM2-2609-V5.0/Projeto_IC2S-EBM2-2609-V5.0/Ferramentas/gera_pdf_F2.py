# -*- coding: utf-8 -*-
"""F2 etapa 2.5 - PDF para a revisao humana (skill 2shw-pcb:esquematico), EBM2 V5.

1. Esquematico exportado pelo proprio KiCad (kicad-cli sch export pdf): percorre a hierarquia inteira.
2. SVG a preto e branco (kicad-cli sch export svg --black-and-white): tem de sair N+1 = 8 ficheiros
   (raiz + 7 folhas filhas), prova de que a arvore hierarquica esta valida.
3. Rasterizacao dos SVG a alta resolucao para a inspeccao ampliada (PyMuPDF; o rasteriza_svg.py da skill
   precisa de cairosvg, que nao esta instalado).
4. PDF consolidado, na ordem da skill: esquematico, diagrama de blocos (2.1), mapa de pinos (2.4), com
   marcadores por folha e metadados.
Portas (recusa entregar se falhar): N+1 SVG; 8 paginas de esquematico; 0 sobreposicoes, 0 texto invertido e
0 fora do quadro (mede_solape_pdf.py); cada folha com o seu titulo no bloco; paginas finais = 8 + 1 + mapa.
Uso: python gera_pdf_F2.py
"""
import datetime, glob, html, io, os, re, shutil, subprocess, sys
import fitz

RAIZ = r"C:\hw\hw-ebm2-v5"
K = os.path.join(RAIZ, "KiCad_EBM2_V5")
SCH = os.path.join(K, "IC2S_Extension_Board-EBM2_V5.kicad_sch")
DOC = os.path.join(RAIZ, "Documentos")
SAI = os.path.join(DOC, "revisao_F2_2.5")
CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
HOJE = datetime.date.today().isoformat()
FOLHAS = ["Raiz", "1 Conectores", "2 Entrada", "3 Alimentacao", "4 Barreira", "5 ADC", "6 Lacos", "7 NTC"]
falhas = []


def corre(args):
    r = subprocess.run([CLI] + args, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("kicad-cli falhou: %s\n%s" % (" ".join(args), r.stderr))


# ---------------------------------------------------------------- 1 e 2: exportacao pelo KiCad
if os.path.exists(SAI):
    shutil.rmtree(SAI)
os.makedirs(os.path.join(SAI, "svg"))
os.makedirs(os.path.join(SAI, "png"))
pdf_sch = os.path.join(SAI, "esquematico_EBM2_V5.pdf")
corre(["sch", "export", "pdf", "--output", pdf_sch, SCH])
corre(["sch", "export", "svg", "--output", os.path.join(SAI, "svg"), "--black-and-white", SCH])
svgs = sorted(glob.glob(os.path.join(SAI, "svg", "*.svg")))
if len(svgs) != len(FOLHAS):
    falhas.append("SVG: %d ficheiros, esperado N+1 = %d" % (len(svgs), len(FOLHAS)))

# ---------------------------------------------------------------- 3: rasterizacao para a inspeccao
for s in svgs:
    d = fitz.open(s)
    pg = d[0]
    z = 3200.0 / pg.rect.width
    pg.get_pixmap(matrix=fitz.Matrix(z, z)).save(os.path.join(SAI, "png", os.path.basename(s)[:-4] + ".png"))

# ---------------------------------------------------------------- portas sobre o PDF do esquematico
d = fitz.open(pdf_sch)
if d.page_count != len(FOLHAS):
    falhas.append("PDF do esquematico: %d paginas, esperado %d" % (d.page_count, len(FOLHAS)))
for i, pg in enumerate(d):
    txt = pg.get_text()
    if "IC2S Extension Board EBM2 V5" not in txt:
        falhas.append("pagina %d sem o titulo no bloco" % (i + 1))
    if ("Folha %d de 8" % (i + 1)) not in txt:
        falhas.append("pagina %d: o bloco nao diz 'Folha %d de 8'" % (i + 1, i + 1))
r = subprocess.run([sys.executable, os.path.join(RAIZ, "ferramentas", "mede_solape_pdf.py"), pdf_sch],
                   capture_output=True, text=True, encoding="utf-8", errors="replace")
ms = r.stdout
for linha in ms.splitlines():
    m = re.match(r"pagina (\d+): (\d+) textos, (\d+) sobreposicoes", linha)
    if m and int(m.group(3)):
        falhas.append("pagina %s: %s sobreposicoes" % (m.group(1), m.group(3)))
for k in ("INVERTIDO", "FORA"):
    if k in ms.upper() and ("0 " + k) not in ms.upper():
        falhas.append("mede_solape_pdf assinala %s" % k)

# ---------------------------------------------------------------- 4a: diagrama de blocos (SVG -> PDF)
dg = fitz.open(os.path.join(DOC, "diagrama_blocos_EBM2_V5.svg"))
pdf_dg = fitz.open("pdf", dg.convert_to_pdf())


# ---------------------------------------------------------------- 4b: mapa de pinos (Markdown -> PDF)
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"~~(.+?)~~", r"<s>\1</s>", s)
    s = re.sub(r"`([^`]+)`", r'<code>\1</code>', s)
    return s


def md_html(md):
    out, tab, par = [], [], []

    def fecha_tab():
        if tab:
            h = tab[0]
            corpo = [r for r in tab[2:]]
            out.append("<table><tr>" + "".join("<th>%s</th>" % inline(c) for c in h) + "</tr>" +
                       "".join("<tr>" + "".join("<td>%s</td>" % inline(c) for c in r) + "</tr>" for r in corpo) + "</table>")
            tab.clear()

    def fecha_par():
        if par:
            out.append("<p>%s</p>" % inline(" ".join(par)))
            par.clear()
    for L in md.splitlines():
        if L.startswith("|"):
            fecha_par()
            tab.append([c.strip() for c in L.strip().strip("|").split("|")])
            continue
        fecha_tab()
        if L.startswith("## "):
            fecha_par(); out.append("<h2>%s</h2>" % inline(L[3:]))
        elif L.startswith("# "):
            fecha_par(); out.append("<h1>%s</h1>" % inline(L[2:]))
        elif not L.strip():
            fecha_par()
        else:
            par.append(L.strip())
    fecha_tab(); fecha_par()
    return "\n".join(out)


CSS = """
* { font-family: sans-serif; }
body { font-size: 7.4pt; color: #1a1a1a; }
h1 { font-size: 14pt; margin: 0 0 4pt 0; }
h2 { font-size: 10pt; margin: 9pt 0 3pt 0; color: #203a60; }
p { margin: 2pt 0; }
table { border-collapse: collapse; width: 100%; margin: 2pt 0 4pt 0; }
th { background-color: #e9eef7; text-align: left; border: 0.5pt solid #7a8aa0; padding: 1.5pt 3pt; }
td { border: 0.5pt solid #b0b8c4; padding: 1.5pt 3pt; vertical-align: top; }
code { font-family: monospace; font-size: 7pt; }
"""
mp_md = io.open(os.path.join(DOC, "mapa_pinos_EBM2_V5.md"), encoding="utf-8").read()
story = fitz.Story(html=md_html(mp_md), user_css=CSS)
A4P = fitz.paper_rect("a4-l")
buf_mp = io.BytesIO()          # em memoria: um ficheiro temporario ficava preso pelo Windows
w = fitz.DocumentWriter(buf_mp)
mais = True
n_mp = 0
while mais:
    dev = w.begin_page(A4P)
    mais, _ = story.place(A4P + (36, 36, -36, -40))
    story.draw(dev)
    w.end_page()
    n_mp += 1
w.close()
pdf_mp = fitz.open("pdf", buf_mp.getvalue())
for i, pg in enumerate(pdf_mp):     # rodape em cada pagina do mapa
    pg.insert_text((36, A4P.height - 18), "EBM2 V5 - mapa de pinos (F2 2.4) - pagina %d de %d - gerado de %s"
                   % (i + 1, pdf_mp.page_count, "EBM2_V5_rev25c.net"), fontsize=7, color=(0.4, 0.4, 0.4))

# ---------------------------------------------------------------- 4c: consolidado com marcadores
final = fitz.open()
final.insert_pdf(d)
final.insert_pdf(pdf_dg)
final.insert_pdf(pdf_mp)
toc = [[1, "Esquematico (kicad-cli)", 1]] + [[2, "Folha %d - %s" % (i + 1, f), i + 1] for i, f in enumerate(FOLHAS)]
toc += [[1, "Diagrama de blocos (2.1)", len(FOLHAS) + 1], [1, "Mapa de pinos (2.4)", len(FOLHAS) + 2]]
final.set_toc(toc)
final.set_metadata({"title": "IC2S Extension Board EBM2 V5 - F2 esquematico para revisao (2.5)",
                    "author": "2Solve - Javier Rivadineira", "subject": "Intencao rev. 2.5c; netlist EBM2_V5_rev25c",
                    "creator": "ferramentas/gera_pdf_F2.py + KiCad 10.0.5", "keywords": "EBM2 V5, F2, Portao 1"})
esperado = len(FOLHAS) + 1 + n_mp
if final.page_count != esperado:
    falhas.append("consolidado: %d paginas, esperado %d" % (final.page_count, esperado))
out = os.path.join(SAI, "EBM2_V5_F2_revisao_%s.pdf" % HOJE)
final.save(out, garbage=3, deflate=True)

print("SVG:", len(svgs), "| esquematico:", d.page_count, "pag. | diagrama: 1 | mapa de pinos:", n_mp, "pag.")
print(ms.strip().replace("\n", " | "))
if falhas:
    print("\n*** %d PORTAS FALHARAM ***" % len(falhas))
    for f in falhas:
        print("   ", f)
    sys.exit(1)
print("OK ->", out, "(%d paginas)" % final.page_count)
