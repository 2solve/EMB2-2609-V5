# -*- coding: utf-8 -*-
"""Porta da renumeracao: a netlist depois tem de ser a de antes com as referencias trocadas pela tabela.

Compara (1) componentes: valor, pegada, lib, MPN e campos, ref a ref pela tabela; (2) topologia: o conjunto de
pinos de cada rede, traduzido. Os nomes de rede so podem mudar nas redes com nome automatico que citam uma
referencia (Net-(R206-Pad1)) e no rotulo FB_U640; qualquer outra mudanca de nome e erro.
Uso: python confere_renumeracao.py antes.net depois.net tabela.csv     (sai com 1 se houver diferenca)
"""
import csv, io, re, sys

sys.path.insert(0, __file__.rsplit("\\", 1)[0])
from netlist_diff import tokens  # noqa: E402


def arvore(txt):
    pilha = [[]]
    for tk in tokens(txt):
        if tk == "(":
            pilha.append([])
        elif tk == ")":
            x = pilha.pop(); pilha[-1].append(x)
        else:
            pilha[-1].append(tk[1] if isinstance(tk, tuple) else tk)
    return pilha[0][0]


def filhos(n, nome):
    return [x for x in n if isinstance(x, list) and x and x[0] == nome]


def val(n, nome):
    f = filhos(n, nome)
    return f[0][1] if f and len(f[0]) > 1 else None


def le(f):
    a = arvore(io.open(f, encoding="utf-8").read())
    comps = {}
    for c in filhos(filhos(a, "components")[0], "comp"):
        props = {val(p, "name"): val(p, "value") for p in filhos(c, "property")}
        props.pop("Sheetname", None); props.pop("Sheetfile", None)
        comps[val(c, "ref")] = (val(c, "value"), val(c, "footprint"), str(filhos(c, "libsource")), val(c, "datasheet"),
                                val(c, "description"), tuple(sorted(props.items())))
    nets = {}
    for n in filhos(filhos(a, "nets")[0], "net"):
        nets[val(n, "name")] = frozenset((val(x, "ref"), val(x, "pin")) for x in filhos(n, "node"))
    return comps, nets


antes, depois, tab = sys.argv[1:4]
M = {r["ref_antiga"]: r["ref_nova"] for r in csv.DictReader(io.open(tab, encoding="utf-8"))}
ca, na = le(antes)
cd, nd = le(depois)
erros = []


def tr(s):
    return re.sub(r"\b([A-Z]{1,3}\d{3})\b", lambda m: M.get(m.group(1), m.group(1)), s) if s else s


REF = re.compile(r"\b[A-Z]{1,3}(?:\(\d+\+k\)|\d{1,3}[xk]?)(?:-[A-Z]{1,3}\d{1,3})?\b")


def masc(s):
    """textos: tira todas as referencias (isoladas, faixas, curingas); o resto tem de ser igual letra a letra"""
    return REF.sub("<REF>", s) if isinstance(s, str) else s


# 1. componentes
if set(M[r] for r in ca) != set(cd):
    erros.append("conjunto de referencias: faltam %s, sobram %s" % (sorted(set(M[r] for r in ca) - set(cd)),
                                                                     sorted(set(cd) - set(M[r] for r in ca))))
campos_mudados = 0
for r, (v, fp, lib, ds, de, pr) in ca.items():
    n = M[r]
    if n not in cd:
        continue
    v2, fp2, lib2, ds2, de2, pr2 = cd[n]
    if (v, fp, ds) != (v2, fp2, ds2) or masc(lib) != masc(lib2):
        erros.append("%s->%s: valor/pegada/lib/datasheet mudou" % (r, n))
    if (de, pr, lib) != (de2, pr2, lib2):
        campos_mudados += 1  # textos com referencias traduzidas: esperado
    if masc(de) != masc(de2) or tuple((k, masc(x)) for k, x in pr) != tuple((k, masc(x)) for k, x in pr2):
        erros.append("%s->%s: descricao/campos diferem alem das referencias" % (r, n))

# 2. topologia
ta = {frozenset((M[a], p) for a, p in pinos): nome for nome, pinos in na.items()}
td = {pinos: nome for nome, pinos in nd.items()}
for pinos in set(ta) ^ set(td):
    erros.append("rede so num dos lados: %s %s" % (ta.get(pinos) or td.get(pinos), sorted(pinos)[:6]))
renomeadas = []
for pinos in set(ta) & set(td):
    if ta[pinos] != td[pinos]:
        auto = ta[pinos].startswith("Net-(") or ta[pinos].startswith("unconnected-(") or "FB_U640" in ta[pinos]
        if not auto or tr(ta[pinos]).replace("FB_U640", "FB_" + M["U640"]) != td[pinos]:
            erros.append("nome de rede mudou sem ser automatico: %s -> %s" % (ta[pinos], td[pinos]))
        renomeadas.append((ta[pinos], td[pinos]))

print("componentes: %d antes, %d depois | redes: %d antes, %d depois | redes com nome automatico traduzido: %d"
      " | componentes com descricao traduzida: %d" % (len(ca), len(cd), len(na), len(nd), len(renomeadas), campos_mudados))
for a, b in sorted(renomeadas)[:400]:
    if not a.startswith("unconnected-("):
        print("   %s -> %s" % (a, b))
if erros:
    print("\n".join("ERRO: " + e for e in erros))
    sys.exit(1)
print("OK: topologia identica; so mudaram referencias e nomes automaticos")
