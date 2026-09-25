# -*- coding: utf-8 -*-
"""F3 etapa 3.1 (skill 2shw-pcb:layout): cria o .kicad_pcb da EBM2 V5 com o contorno e as restricoes duras.

Transfere a netlist aprovada (as 139 pegadas, redes pino a pino, caminho /folha/simbolo para o
«Update PCB from Schematic» casar sem apagar nada) e fixa, copiadas da V4.1 (Gerber de origem conferido por
confere_mecanica_gerber_V41.py, RC1 0,1 mm):
  - contorno 60,000 x 60,000 mm, Edge.Cuts 0,1 mm, nas mesmas coordenadas da V4.1 convertida;
  - P1 (20 pinos) e P2 (14) na face inferior: rotacao escolhida pela que poe CADA pad sobre o pad homonimo
    da V4.1 (< 0,01 mm), nao por suposicao;
  - H1/H2: furos de fixacao 3,2 mm metalizados, pad 6,0 mm, sem rede (como a V4.1), board_only;
  - LED da V11 nas posicoes da V4.1: D1 <- V4.1 D25 (entrada), D5 <- V4.1 D18 (+5V_ADC), D24 <- V4.1 D19 (lacos);
  - FID1-3 nas posicoes dos fiduciais da V4.1.
P1, P2, H1, H2 e os tres LED ficam bloqueados. O resto fica FORA da placa, em grelha a direita, para a 3.2.
4 camadas (V4.1: Top / Ground / Power / Bottom), espessura 1,6 mm nominal (a V4.1 nao a declara).
Recusa escrever se o .kicad_pcb ja existir.
Uso: "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" gera_pcb_F3.py NETLIST.net
"""
import io, json, os, re, sys
import pcbnew

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from netlist_diff import parse, filhos  # noqa: E402

R = r"C:\hw\hw-ebm2-v5"
K = os.path.join(R, "KiCad_EBM2_V5")
PCB = os.path.join(K, "IC2S_Extension_Board-EBM2_V5.kicad_pcb")
LIB = os.path.join(K, "footprints", "EBM2_V5.pretty")
V41 = r"C:\hw\hw-ebm2-v4.1\KiCad_EBM2_V4.1\IC2S_Extension_Board-EBM2_V4.1.kicad_pcb"
MEC = json.load(io.open(os.path.join(R, "Documentos", "F3", "mecanica_V41.json"), encoding="utf-8"))
MM = pcbnew.FromMM
if os.path.exists(PCB):
    sys.exit("ABORTA: %s ja existe" % PCB)


def v(n, k):
    f = filhos(n, k)
    return f[0][1] if f and len(f[0]) > 1 else None


def xy(p):
    return pcbnew.VECTOR2I(MM(p[0]), MM(p[1]))


# ---------- netlist aprovada
a = parse(io.open(sys.argv[1], encoding="utf-8").read())
comps = []
for c in filhos(filhos(a, "components")[0], "comp"):
    props = {v(p, "name"): v(p, "value") for p in filhos(c, "property")}
    sp = filhos(c, "sheetpath")[0]
    comps.append(dict(ref=v(c, "ref"), valor=v(c, "value"), fp=v(c, "footprint"), mpn=props.get("MPN"),
                      fora_bom="exclude_from_bom" in props, caminho=v(sp, "tstamps") + v(c, "tstamps"),
                      descr=v(c, "description") or "", ds=v(c, "datasheet") or ""))
pino = {}
redes = []
for n in filhos(filhos(a, "nets")[0], "net"):
    nome = v(n, "name"); redes.append(nome)
    for x in filhos(n, "node"):
        pino[(v(x, "ref"), v(x, "pin"))] = nome

b = pcbnew.NewBoard(PCB)
b.SetCopperLayerCount(4)
ds = b.GetDesignSettings()
ds.SetBoardThickness(MM(1.6))
b.SetLayerName(pcbnew.In1_Cu, "In1.Cu")
b.SetLayerName(pcbnew.In2_Cu, "In2.Cu")
net = {}
for nome in redes:
    ni = pcbnew.NETINFO_ITEM(b, nome); b.Add(ni); net[nome] = ni

# ---------- contorno (as mesmas linhas da V4.1)
for s in MEC["contorno"]:
    sh = pcbnew.PCB_SHAPE(b); sh.SetShape(pcbnew.SHAPE_T_SEGMENT)
    sh.SetStart(xy(s["ini"])); sh.SetEnd(xy(s["fim"])); sh.SetLayer(pcbnew.Edge_Cuts); sh.SetWidth(MM(0.1))
    b.Add(sh)

# ---------- pegadas
v41 = pcbnew.LoadBoard(V41)
pads41 = {f.GetReference(): {p.GetNumber(): (pcbnew.ToMM(p.GetPosition().x), pcbnew.ToMM(p.GetPosition().y)) for p in f.Pads()}
          for f in v41.GetFootprints() if f.GetReference()}
fid41 = sorted({(round(pcbnew.ToMM(p.GetPosition().x), 4), round(pcbnew.ToMM(p.GetPosition().y), 4))
                for f in v41.GetFootprints() if not f.GetReference() for p in f.Pads() if p.GetAttribute() == pcbnew.PAD_ATTRIB_SMD})
LED = {"D1": "D25", "D5": "D18", "D24": "D19"}
FIX = [(126.501, 131.004), (170.501, 79.004)]


def carrega(nome):
    fp = pcbnew.FootprintLoad(LIB, nome)
    assert fp is not None, nome
    fp.SetFPID(pcbnew.LIB_ID("EBM2_V5", nome))
    return fp


def poe_na_face_de_baixo(fp):
    try:
        fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_TOP_BOTTOM)
    except (AttributeError, TypeError):
        fp.Flip(fp.GetPosition(), False)


def encaixa(fp, alvo, face_baixo):
    """escolhe a rotacao que poe cada pad no pad homonimo da V4.1; devolve o pior desvio em mm"""
    melhor = None
    for rot in (0, 90, 180, -90):
        fp.SetOrientationDegrees(rot)
        um = alvo["1"]
        p1 = [p for p in fp.Pads() if p.GetNumber() == "1"][0]
        d = pcbnew.VECTOR2I(MM(um[0]), MM(um[1])) - p1.GetPosition()
        fp.Move(d)
        pior = max(((pcbnew.ToMM(p.GetPosition().x) - alvo[p.GetNumber()][0]) ** 2 +
                    (pcbnew.ToMM(p.GetPosition().y) - alvo[p.GetNumber()][1]) ** 2) ** 0.5 for p in fp.Pads() if p.GetNumber() in alvo)
        if melhor is None or pior < melhor[0]:
            melhor = (pior, rot, fp.GetPosition())
    fp.SetOrientationDegrees(melhor[1]); fp.SetPosition(melhor[2])
    # confirma depois de repor
    pior = max(((pcbnew.ToMM(p.GetPosition().x) - alvo[p.GetNumber()][0]) ** 2 +
                (pcbnew.ToMM(p.GetPosition().y) - alvo[p.GetNumber()][1]) ** 2) ** 0.5 for p in fp.Pads() if p.GetNumber() in alvo)
    return pior, melhor[1]


relat = {}
col, lin = 0, 0
fids = iter(fid41)
for c in comps:
    lib, nome = c["fp"].split(":", 1)
    fp = carrega(nome)
    fp.SetReference(c["ref"]); fp.SetValue(c["valor"])
    fp.SetPath(pcbnew.KIID_PATH(c["caminho"].rstrip("/")))
    # campos iguais aos do simbolo (a paridade do DRC compara-os)
    for campo, valor in (("MPN", c["mpn"]), ("Description", c["descr"]), ("Datasheet", c["ds"])):
        if valor:
            fp.SetField(campo, valor)
    if c["fora_bom"]:
        fp.SetAttributes(fp.GetAttributes() | pcbnew.FP_EXCLUDE_FROM_BOM)
    b.Add(fp)
    for p in fp.Pads():
        if p.GetNumber() and (c["ref"], p.GetNumber()) in pino:
            p.SetNet(net[pino[(c["ref"], p.GetNumber())]])
    r = c["ref"]
    if r in ("P1", "P2"):
        poe_na_face_de_baixo(fp)
        pior, rot = encaixa(fp, pads41[r], True)
        assert pior < 0.01, (r, pior)
        fp.SetLocked(True); relat[r] = "face inferior, rot %s, pior pad %.4f mm da V4.1" % (rot, pior)
    elif r in LED:
        f41 = [f for f in v41.GetFootprints() if f.GetReference() == LED[r]][0]
        fp.SetOrientation(f41.GetOrientation()); fp.SetPosition(f41.GetPosition())
        d = ((pcbnew.ToMM(fp.GetPosition().x - f41.GetPosition().x)) ** 2 + (pcbnew.ToMM(fp.GetPosition().y - f41.GetPosition().y)) ** 2) ** 0.5
        fp.SetLocked(True); relat[r] = "posicao da V4.1 %s (%.4f, %.4f) rot %s, desvio %.4f mm" % (
            LED[r], pcbnew.ToMM(f41.GetPosition().x), pcbnew.ToMM(f41.GetPosition().y), f41.GetOrientationDegrees(), d)
    elif r.startswith("FID"):
        p = next(fids); fp.SetPosition(xy(p)); relat[r] = "fiducial da V4.1 em (%.3f, %.3f)" % p
    else:
        # fora da placa, grelha a direita, pela ordem da netlist
        fp.SetPosition(xy((190 + 10 * col, 76 + 10 * lin)))
        col += 1
        if col == 10:
            col, lin = 0, lin + 1

for i, (x, y) in enumerate(FIX, 1):
    fp = carrega("MountingHole_3.2mm_Pad6.0")
    fp.SetReference("H%d" % i); fp.SetValue("MountingHole_3.2mm_Pad6.0")
    fp.SetPosition(xy((x, y))); fp.SetLocked(True)
    b.Add(fp); relat["H%d" % i] = "furo 3,2 mm em (%.3f, %.3f), Gerber V4.1 T6" % (x, y)

pcbnew.SaveBoard(PCB, b)
print("escrito:", PCB, "|", len(comps), "pegadas da netlist + 2 furos |", len(redes), "redes")
for k in sorted(relat):
    print("  %-4s %s" % (k, relat[k]))
