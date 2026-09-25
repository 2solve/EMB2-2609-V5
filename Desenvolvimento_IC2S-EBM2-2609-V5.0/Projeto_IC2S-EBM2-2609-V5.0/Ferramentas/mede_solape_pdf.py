# -*- coding: utf-8 -*-
"""Porta (b) da F2: medir sobreposicao de texto NO PDF EXPORTADO.

AMBIENTE_KICAD.md §5.1: o justify de um campo compoe-se com a rotacao do
simbolo, e um verificador de coordenadas pode dar zero achados sobre textos
visivelmente encimados. O PDF e o que o humano le; e ai que se mede.

Uso: python mede_solape_pdf.py esquema.pdf [pagina ...]
Sai com codigo 1 se houver pares de textos sobrepostos, texto fora do quadro ou invertido.
"""
import sys
import fitz

LIMIAR = 0.12      # fraccao da area do menor rectangulo que conta como sobreposicao


def spans(pg):
    out = []
    for b in pg.get_text("dict")["blocks"]:
        for ln in b.get("lines", []):
            for sp in ln.get("spans", []):
                tx = sp["text"].strip()
                if tx:
                    out.append((fitz.Rect(sp["bbox"]), tx, tuple(round(v) for v in ln["dir"])))
    return out


def main():
    doc = fitz.open(sys.argv[1])
    pags = [int(x) for x in sys.argv[2:]] or list(range(1, doc.page_count + 1))
    total = 0
    for n in pags:
        pg = doc[n - 1]
        ss = spans(pg)
        achados = []
        for i in range(len(ss)):
            for j in range(i + 1, len(ss)):
                a, ta = ss[i][:2]; b, tb = ss[j][:2]
                inter = a & b
                if inter.is_empty:
                    continue
                # o KiCad emite cada texto duas vezes no PDF, no mesmo sitio: nao e sobreposicao
                uniao = a | b
                if ta == tb and (inter.width * inter.height) / max(uniao.width * uniao.height, 1e-9) > 0.9:
                    continue
                area = inter.width * inter.height
                menor = min(a.width * a.height, b.width * b.height)
                if menor > 0 and area / menor > LIMIAR:
                    achados.append((area / menor, ta, tb, inter))
        print("pagina %d: %d textos, %d sobreposicoes" % (n, len(ss), len(achados)))
        # texto que sai do quadro: a moldura do KiCad fica a 10 mm do bordo da pagina
        marg = 10.0 / 25.4 * 72
        W, H = pg.rect.width, pg.rect.height
        fora = [(r, tx) for r, tx, _ in ss if r.x1 > W - marg + 0.5 or r.x0 < marg - 0.5
                or r.y1 > H - marg + 0.5 or r.y0 < marg - 0.5]
        for r, tx in fora:
            print("    FORA DO QUADRO: %r termina em x=%.0f (limite %.0f)" % (tx[:40], r.x1, W - marg))
        # texto de pernas para o ar: o KiCad le-se da esquerda (dir 1,0) ou de baixo para cima
        # (dir 0,-1, eixo y do PDF para baixo). dir -1,0 foi medido num porto a 180 graus
        # (exp180, 23-09-2026); 0,1 e o caso vertical equivalente.
        inv = [(r, tx, d) for r, tx, d in ss if d in ((-1, 0), (0, 1))]
        for r, tx, d in inv:
            print("    INVERTIDO: %r dir=%s em (%.0f, %.0f)" % (tx[:40], d, r.x0, r.y0))
        total += len(achados) + len(fora) + len(inv)
        for f, ta, tb, r in sorted(achados, key=lambda z: -z[0]):
            print("    %3.0f%%  %-28r x %-28r em (%.0f, %.0f)" % (f * 100, ta[:28], tb[:28], r.x0, r.y0))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
