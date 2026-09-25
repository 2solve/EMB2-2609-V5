# -*- coding: utf-8 -*-
"""Porta (a) da F2: comparar duas netlists do KiCad rede a rede e no a no.

Uso:
  python netlist_diff.py antes.net depois.net                 # so mostra o diff
  python netlist_diff.py antes.net depois.net esperado.json   # exige que o diff seja EXACTAMENTE o esperado

A comparacao e feita por TOPOLOGIA (o conjunto de pinos de cada rede), e so
depois pelo nome. Duas netlists podem ter nomes iguais e ligacoes diferentes, ou
o contrario; e a topologia que decide se o circuito mudou.

esperado.json:
{
  "componentes_novos":     ["R206"],
  "componentes_removidos": [],
  "valores":               {"F201": "CC12H250MA-TR"},
  "pinos_que_mudam_de_rede": {"D202.1": "+24V_REG_PRE", "R206.1": "+24V_REG_PRE", "R206.2": "+24V_REG"}
}
Qualquer diferenca fora desta lista faz o script sair com codigo 1.
"""
import io, json, re, sys


def tokens(txt):
    i, n = 0, len(txt)
    while i < n:
        c = txt[i]
        if c in "()":
            yield c; i += 1
        elif c == '"':
            j = i + 1; buf = []
            while j < n and txt[j] != '"':
                if txt[j] == "\\" and j + 1 < n:
                    buf.append(txt[j + 1]); j += 2
                else:
                    buf.append(txt[j]); j += 1
            yield ("S", "".join(buf)); i = j + 1
        elif c.isspace():
            i += 1
        else:
            j = i
            while j < n and not txt[j].isspace() and txt[j] not in '()"':
                j += 1
            yield ("A", txt[i:j]); i = j


def parse(txt):
    pilha = [[]]
    for t in tokens(txt):
        if t == "(":
            pilha.append([])
        elif t == ")":
            no = pilha.pop(); pilha[-1].append(no)
        else:
            pilha[-1].append(t[1])
    return pilha[0][0]


def filhos(no, cab):
    return [x for x in no if isinstance(x, list) and x and x[0] == cab]


def val(no, cab):
    f = filhos(no, cab)
    return f[0][1] if f and len(f[0]) > 1 else None


def ler(caminho):
    arv = parse(io.open(caminho, encoding="utf-8", errors="replace").read())
    comps = {}
    for sec in filhos(arv, "components"):
        for c in filhos(sec, "comp"):
            ref = val(c, "ref")
            comps[ref] = {"value": val(c, "value"), "footprint": val(c, "footprint")}
            for campos in filhos(c, "fields"):
                for f in filhos(campos, "field"):
                    nome = val(f, "name")
                    if nome == "MPN":
                        comps[ref]["MPN"] = f[-1] if isinstance(f[-1], str) else None
    redes = {}
    for sec in filhos(arv, "nets"):
        for r in filhos(sec, "net"):
            nome = val(r, "name")
            nos = set()
            for nd in filhos(r, "node"):
                nos.add("%s.%s" % (val(nd, "ref"), val(nd, "pin")))
            redes[nome] = nos
    pino_rede = {p: n for n, ps in redes.items() for p in ps}
    return comps, redes, pino_rede


def main():
    ca, ra, pa = ler(sys.argv[1])
    cd, rd, pd = ler(sys.argv[2])
    esp = json.load(io.open(sys.argv[3], encoding="utf-8")) if len(sys.argv) > 3 else None

    real = {
        "componentes_novos": sorted(set(cd) - set(ca)),
        "componentes_removidos": sorted(set(ca) - set(cd)),
        "valores": {r: cd[r]["value"] for r in sorted(set(ca) & set(cd))
                    if ca[r]["value"] != cd[r]["value"]},
        "pinos_que_mudam_de_rede": {},
    }
    for p in sorted(set(pa) | set(pd)):
        if pa.get(p) != pd.get(p):
            real["pinos_que_mudam_de_rede"][p] = pd.get(p)

    # redes cuja TOPOLOGIA mudou, independentemente do nome
    topo_a = {frozenset(v) for v in ra.values() if len(v) > 1}
    topo_d = {frozenset(v) for v in rd.values() if len(v) > 1}
    so_a = topo_a - topo_d
    so_d = topo_d - topo_a

    print("componentes: %d -> %d | redes com 2+ pinos: %d -> %d"
          % (len(ca), len(cd), len(topo_a), len(topo_d)))
    print("nomes gerados depois (reprovacao): %s" % ([n for n in rd if n.startswith("Net-")] or "nenhum"))
    print("pinos com no-connect (legitimos): %d" % len([n for n in rd if n.startswith("unconnected-")]))
    for k, v in real.items():
        print("%-26s %s" % (k, v if v else "-"))
    print("redes cuja topologia so existe ANTES:  %d" % len(so_a))
    for s in sorted(so_a, key=lambda x: sorted(x)): print("     ", " ".join(sorted(s)))
    print("redes cuja topologia so existe DEPOIS: %d" % len(so_d))
    for s in sorted(so_d, key=lambda x: sorted(x)): print("     ", " ".join(sorted(s)))

    if esp is None:
        return 0
    falhas = []
    for k in ("componentes_novos", "componentes_removidos"):
        if sorted(esp.get(k, [])) != real[k]:
            falhas.append("%s: esperado %s, real %s" % (k, sorted(esp.get(k, [])), real[k]))
    if esp.get("valores", {}) != real["valores"]:
        falhas.append("valores: esperado %s, real %s" % (esp.get("valores", {}), real["valores"]))
    if esp.get("pinos_que_mudam_de_rede", {}) != real["pinos_que_mudam_de_rede"]:
        falhas.append("pinos: esperado %s, real %s"
                      % (esp.get("pinos_que_mudam_de_rede", {}), real["pinos_que_mudam_de_rede"]))
    if falhas:
        print("\n*** O DIFF NAO E O ESPERADO ***")
        for f in falhas: print("   ", f)
        return 1
    print("\nDIFF IDENTICO AO ESPERADO")
    return 0


if __name__ == "__main__":
    sys.exit(main())
