# -*- coding: utf-8 -*-
"""Cada simbolo colocado tem de listar EXACTAMENTE os pinos da sua definicao embebida.

Causa medida em 2026-09-23: o U200 (TPS7A4001, folha 03) listava os pinos 1-8 e
nao o 9 (PAD escondido). O KiCad acrescenta o pino ao abrir e mostra «Foi encontrado
um erro ao carregar o esquema que foi automaticamente corrigido»; o kicad-cli nao
o acusa, nem o ERC, nem a netlist.

Uso: python verifica_pinos_instancia.py folha.kicad_sch [...]   (sai com 1 se falhar)
"""
import io, re, sys
from construtor import fim, pinos_de_bloco


def verifica(caminho):
    t = io.open(caminho, encoding="utf-8").read()
    a = t.find("\n\t(lib_symbols"); b = fim(t, a + 1)
    libs, i = {}, a
    for m in re.finditer(r'^\t\t\(symbol "([^"]+)"', t[a:b], re.M):
        ini = a + m.start() + 1
        libs[m.group(1)] = set(pinos_de_bloco(t[ini:fim(t, ini)]))
    falhas, n = [], 0
    for m in re.finditer(r'\n\t\(symbol\n', t[b:]):
        ini = b + m.start() + 1; blk = t[ini:fim(t, ini)]
        lib = re.search(r'\(lib_id "([^"]+)"\)', blk).group(1)
        ref = re.search(r'\(property "Reference" "([^"]+)"', blk).group(1)
        pins = re.findall(r'^\t\t\(pin "([^"]+)"', blk, re.M)
        n += 1
        if sorted(pins) != sorted(libs[lib]) or len(pins) != len(set(pins)):
            falhas.append("%s (%s): lista %s, a definicao tem %s"
                          % (ref, lib, sorted(pins, key=lambda z: (len(z), z)), sorted(libs[lib], key=lambda z: (len(z), z))))
    return n, falhas


if __name__ == "__main__":
    total = 0
    for c in sys.argv[1:]:
        n, fs = verifica(c)
        total += len(fs)
        print("%-45s %3d simbolos, %d com pinos em falta ou a mais" % (c.split("\\")[-1].split("/")[-1], n, len(fs)))
        for x in fs: print("    ", x)
    sys.exit(1 if total else 0)
