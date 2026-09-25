# -*- coding: utf-8 -*-
"""Posicao exacta dos pinos de um simbolo colocado numa folha KiCad 10.

A biblioteca usa Y para cima; a folha usa Y para baixo. A rotacao do simbolo
e anti-horaria vista no ecra. Convencao conferida contra dois casos conhecidos
da folha 02 (R200 a 90 graus e D201 a 180 graus) antes de ser usada:
    (x, y) = (px, -py)                  # biblioteca -> folha
    x' =  x cos a + y sin a             # rotacao anti-horaria no ecra, Y para baixo
    y' = -x sin a + y cos a
AMBIENTE_KICAD.md 4.1 avisa que o MCP gira para o lado errado: por isso esta
conta e feita aqui e confirmada pela netlist depois de cada escrita.
"""
import io, math, re, sys
sys.path.insert(0, __file__.rsplit("\\", 1)[0] if "\\" in __file__ else ".")
from netlist_diff import parse, filhos, val


def pinos_biblioteca(caminho_sch):
    """{lib_id: {numero: (px, py, angulo, nome)}} a partir do lib_symbols embebido."""
    arv = parse(io.open(caminho_sch, encoding="utf-8").read())
    out = {}
    for ls in filhos(arv, "lib_symbols"):
        for s in filhos(ls, "symbol"):
            lib = s[1]
            pins = {}
            def anda(no):
                for x in no:
                    if isinstance(x, list) and x:
                        if x[0] == "pin":
                            at = filhos(x, "at")[0]
                            num = filhos(x, "number")[0][1]
                            nome = filhos(x, "name")[0][1]
                            pins[num] = (float(at[1]), float(at[2]), float(at[3]) if len(at) > 3 else 0.0, nome)
                        elif x[0] == "symbol":
                            anda(x)
            anda(s)
            out[lib] = pins
    return out


def pos_pino(px, py, X, Y, rot, espelho=None):
    x, y = px, -py
    if espelho == "y":
        x = -x
    elif espelho == "x":
        y = -y
    a = math.radians(rot)
    xr = x * math.cos(a) + y * math.sin(a)
    yr = -x * math.sin(a) + y * math.cos(a)
    return round(X + xr, 4), round(Y + yr, 4)


if __name__ == "__main__":
    lib = pinos_biblioteca(sys.argv[1])
    for k in sys.argv[2:] or sorted(lib):
        print(k)
        for n, (px, py, a, nome) in sorted(lib[k].items(), key=lambda z: (len(z[0]), z[0])):
            print("   pino %-3s %-10s em (%7.2f, %7.2f) ang %3.0f" % (n, nome, px, py, a))
