# -*- coding: utf-8 -*-
"""F3 etapa 3.1: restricoes mecanicas duras da EBM2 V4.1 (so leitura da placa convertida e auditada).

Le C:\\hw\\hw-ebm2-v4.1\\KiCad_EBM2_V4.1\\IC2S_Extension_Board-EBM2_V4.1.kicad_pcb com o pcbnew do KiCad 10
(LoadBoard nao grava nada) e escreve um JSON com: contorno (Edge.Cuts), furos nao metalizados e de fixacao,
P1/P2 (posicao, rotacao, face, pads), LED da V11 (D18, D19, D25) e empilhamento.
Uso: "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" extrai_mecanica_V41.py SAIDA.json
"""
import json, sys
import pcbnew

PCB = r"C:\hw\hw-ebm2-v4.1\KiCad_EBM2_V4.1\IC2S_Extension_Board-EBM2_V4.1.kicad_pcb"
b = pcbnew.LoadBoard(PCB)
mm = pcbnew.ToMM
out = {"fonte": PCB, "contorno": [], "furos_np": [], "fixacao": [], "conectores": {}, "led_V11": {}, "outros_th": []}

for d in b.GetDrawings():
    if d.GetLayer() == pcbnew.Edge_Cuts:
        s = {"forma": d.ShowShape(), "ini": [mm(d.GetStart().x), mm(d.GetStart().y)], "fim": [mm(d.GetEnd().x), mm(d.GetEnd().y)]}
        if d.GetShape() in (pcbnew.SHAPE_T_ARC,):
            s["centro"] = [mm(d.GetCenter().x), mm(d.GetCenter().y)]; s["raio"] = mm(d.GetRadius())
        if d.GetShape() == pcbnew.SHAPE_T_CIRCLE:
            s["centro"] = [mm(d.GetCenter().x), mm(d.GetCenter().y)]; s["raio"] = mm(d.GetRadius())
        out["contorno"].append(s)
bb = b.GetBoardEdgesBoundingBox()
out["caixa_contorno"] = {"x0": mm(bb.GetX()), "y0": mm(bb.GetY()), "largura": mm(bb.GetWidth()), "altura": mm(bb.GetHeight())}

for fp in b.GetFootprints():
    ref = fp.GetReference()
    for p in fp.Pads():
        if p.GetAttribute() == pcbnew.PAD_ATTRIB_NPTH:
            out["furos_np"].append({"ref": ref, "pad": p.GetNumber(), "xy": [mm(p.GetPosition().x), mm(p.GetPosition().y)],
                                    "furo": [mm(p.GetDrillSize().x), mm(p.GetDrillSize().y)]})
    if ref in ("P1", "P2") or ref.startswith("J"):
        out["conectores"][ref] = {
            "fpid": str(fp.GetFPID().GetUniStringLibItemName()), "xy": [mm(fp.GetPosition().x), mm(fp.GetPosition().y)],
            "rot": fp.GetOrientationDegrees(), "face": "bottom" if fp.IsFlipped() else "top",
            "pads": [{"n": p.GetNumber(), "xy": [mm(p.GetPosition().x), mm(p.GetPosition().y)],
                      "furo": mm(p.GetDrillSize().x), "tam": [mm(p.GetSize().x), mm(p.GetSize().y)]}
                     for p in sorted(fp.Pads(), key=lambda q: int(q.GetNumber()) if q.GetNumber().isdigit() else 999)]}
    if ref in ("D18", "D19", "D25"):
        out["led_V11"][ref] = {"fpid": str(fp.GetFPID().GetUniStringLibItemName()), "valor": fp.GetValue(),
                               "xy": [mm(fp.GetPosition().x), mm(fp.GetPosition().y)], "rot": fp.GetOrientationDegrees(),
                               "face": "bottom" if fp.IsFlipped() else "top"}
    if any(p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH for p in fp.Pads()) and ref not in ("P1", "P2"):
        out["outros_th"].append({"ref": ref, "fpid": str(fp.GetFPID().GetUniStringLibItemName()),
                                 "xy": [mm(fp.GetPosition().x), mm(fp.GetPosition().y)], "npads": len(fp.Pads())})
    if "hole" in str(fp.GetFPID().GetUniStringLibItemName()).lower() or "mount" in str(fp.GetFPID().GetUniStringLibItemName()).lower():
        out["fixacao"].append({"ref": ref, "xy": [mm(fp.GetPosition().x), mm(fp.GetPosition().y)]})

ds = b.GetDesignSettings()
out["camadas_cobre"] = b.GetCopperLayerCount()
out["espessura_mm"] = mm(ds.GetBoardThickness())
out["origem_aux"] = [mm(ds.GetAuxOrigin().x), mm(ds.GetAuxOrigin().y)]
out["n_footprints"] = len(b.GetFootprints())
json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("contorno:", len(out["contorno"]), "segmentos | caixa", out["caixa_contorno"], "| NPTH:", len(out["furos_np"]),
      "| camadas", out["camadas_cobre"], "| espessura", out["espessura_mm"], "| conectores", list(out["conectores"]),
      "| LED", list(out["led_V11"]))
