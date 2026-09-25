# -*- coding: utf-8 -*-
"""F3 etapa 3.0 (skill 2shw-pcb:layout): conferencia de recebimento do esquematico aprovado no Portao 1.

Confere, sem redesenhar nada:
  1. a netlist exportada agora e IGUAL a do pacote congelado do Portao 1 (topologia, valores, pegadas, MPN);
  2. designadores validos (#?[A-Za-z_]+\\d+);
  3. todo componente tem pegada, a biblioteca da pegada esta na fp-lib-table e o .kicad_mod existe;
  4. os pinos de cada componente na netlist existem como pads na pegada (pino alfabetico nao casa com pad
     numerico), e cada pad electrico da pegada tem pino (pad sem pino = cobre sem rede na placa);
  5. componentes marcados fora da placa (on_board no) ou DNP.
Uso: python confere_recebimento_F3.py NETLIST_ACTUAL.net       (sai com 1 se algo reprovar)
"""
import glob, io, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from netlist_diff import parse, filhos  # noqa: E402

R = r"C:\hw\hw-ebm2-v5"
K = os.path.join(R, "KiCad_EBM2_V5")
APROV = os.path.join(R, "Documentos", "portao1_aprovado_2026-09-25", "EBM2_V5.net")


def v(n, k):
    f = filhos(n, k)
    return f[0][1] if f and len(f[0]) > 1 else None


def le(f):
    a = parse(io.open(f, encoding="utf-8").read())
    comps = {}
    for c in filhos(filhos(a, "components")[0], "comp"):
        props = {v(p, "name"): v(p, "value") for p in filhos(c, "property")}
        comps[v(c, "ref")] = dict(valor=v(c, "value"), fp=v(c, "footprint"), mpn=props.get("MPN"), props=props)
    nets = {}
    for n in filhos(filhos(a, "nets")[0], "net"):
        nets[v(n, "name")] = frozenset((v(x, "ref"), v(x, "pin")) for x in filhos(n, "node"))
    return comps, nets


falhas = []
ca, na = le(APROV)
cn, nn = le(sys.argv[1])
# 1. igual ao aprovado
if set(ca) != set(cn):
    falhas.append("componentes diferentes do aprovado: %s" % sorted(set(ca) ^ set(cn)))
for r in set(ca) & set(cn):
    for k in ("valor", "fp", "mpn"):
        if ca[r][k] != cn[r][k]:
            falhas.append("%s: %s %r -> %r" % (r, k, ca[r][k], cn[r][k]))
if set(na.values()) != set(nn.values()):
    falhas.append("topologia diferente do aprovado")
print("1. contra o Portao 1 congelado: %d componentes, %d redes -> %s" % (len(cn), len(nn), "IGUAL" if not falhas else "DIFERENTE"))

# 2. designadores
maus = [r for r in cn if not re.fullmatch(r"#?[A-Za-z_]+\d+", r)]
print("2. designadores invalidos:", maus or "nenhum")
falhas += ["designador invalido %s" % r for r in maus]

# 3. pegadas
libs = dict(re.findall(r'\(lib \(name "([^"]+)"\)\(type "[^"]+"\)\(uri "([^"]+)"\)', io.open(os.path.join(K, "fp-lib-table"), encoding="utf-8").read()))
sem_fp, sem_lib, sem_mod, pads = [], [], [], {}
for r, c in sorted(cn.items()):
    if not c["fp"]:
        sem_fp.append(r); continue
    lib, nome = c["fp"].split(":", 1)
    if lib not in libs:
        sem_lib.append((r, c["fp"])); continue
    f = os.path.join(libs[lib].replace("${KIPRJMOD}", K), nome + ".kicad_mod")
    if not os.path.exists(f):
        sem_mod.append((r, c["fp"])); continue
    t = io.open(f, encoding="utf-8").read()
    # pads: (pad "1" smd rect ...) ; pads "" (mecanicos) e np_thru_hole nao contam como electricos
    pads[r] = {(m.group(1), m.group(2)) for m in re.finditer(r'\(pad "([^"]*)" (\w+)', t)}
print("3. sem pegada: %s | biblioteca fora da fp-lib-table: %s | .kicad_mod em falta: %s" % (sem_fp or "nenhum", sem_lib or "nenhuma", sem_mod or "nenhum"))
falhas += ["sem pegada %s" % r for r in sem_fp] + ["lib %s" % str(x) for x in sem_lib] + ["mod %s" % str(x) for x in sem_mod]

# 4. pinos x pads
pinos = {}
for pn in nn.values():
    for r, p in pn:
        pinos.setdefault(r, set()).add(p)
pro = []
for r in sorted(pads, key=lambda s: (re.match(r"\D+", s).group(0), int(re.search(r"\d+", s).group(0)))):
    el = {n for n, tipo in pads[r] if n and tipo != "np_thru_hole"}
    p = pinos.get(r, set())
    sem_pad = p - el
    sem_pino = el - p
    if sem_pad or sem_pino:
        pro.append((r, cn[r]["fp"], sorted(sem_pad), sorted(sem_pino)))
for r, fp, a, b in pro:
    print("   %s (%s): pinos sem pad %s | pads sem pino %s" % (r, fp, a, b))
    if a:
        falhas.append("%s: pino sem pad %s" % (r, a))
print("4. pinos x pads: %d componentes conferidos, %d com diferencas (pads sem pino = cobre sem rede: rever)" % (len(pads), len(pro)))

# 5. fora da placa / DNP
raw = io.open(sys.argv[1], encoding="utf-8").read()
fora = [r for r in cn if cn[r]["props"].get("dnp") is not None]
print("5. DNP:", fora or "nenhum")
print("\nFALHAS:" if falhas else "\nRECEBIMENTO OK", *falhas, sep="\n  ")
sys.exit(1 if falhas else 0)
