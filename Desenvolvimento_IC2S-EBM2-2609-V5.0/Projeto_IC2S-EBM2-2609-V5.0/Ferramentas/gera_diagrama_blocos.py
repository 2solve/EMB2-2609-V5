# -*- coding: utf-8 -*-
"""Etapa 2.1 da F2 - diagrama de blocos da EBM2 V5. Rev. B (2026-09-25): intencao rev. 2.5c.
SVG A4 paisagem, folha 1 do PDF consolidado.

Guardas automaticas, porque o primeiro render tinha quatro defeitos que
o olho so apanhou depois de rasterizar:
  G1 moldura   - nada fora do quadro
  G2 travessia - nenhum segmento de ligacao atravessa uma caixa
  G3 rotulos   - nenhum rotulo de ligacao cai dentro de uma caixa
  G4 titulos   - o titulo cabe na largura util (caixa menos o crachá da folha)
"""
import io

W, H = 1188, 840
OUT = r"C:\hw\hw-ebm2-v5\Documentos\diagrama_blocos_EBM2_V5.svg"

C_LINE, C_MUTE, C_BAR = "#1a1a1a", "#6a6a6a", "#b03030"
C_PWR, C_ANA, C_DIG, C_CONN, C_NOTE = "#fdf0e3", "#eaf3ee", "#e9eef7", "#efe9f5", "#fffdf5"
CHAR_W = 8.2          # largura media de um caracter a 15 px, medida no render

# ---------------------------------------------------------------- caixas
# id: (x, y, w, h, titulo, [linhas], cor, cracha)
CAIXAS = {
 "ENT": (280, 150, 210, 185, "Entrada 24 V", [
     "TVS SMA6J33A-Q, 33 V",
     "F2 CC12H750mA + D4",
     "F1 CC12H250mA + D3",
     "R3 150 ohm limita o F1",
     "R2 0 ohm une as massas",
     "Todo o bulk fica deste lado"], C_PWR, "02"),
 "ALI": (570, 150, 210, 185, "Alimentacao", [
     "U1 TPS7A4001",
     "  +24V_REG -> +5V_ADC",
     "U4 MCP1824 -> 3V3_REF",
     "U2 ADR4525 -> +2V5_REF",
     "U3 TL431 grampo 3,52 V",
     "A referencia deixa de ser",
     "o proprio trilho"], C_PWR, "03"),
 "P1":  (950, 150, 195, 200, "P1 Baseboard", [
     "Harwin M20-7822046",
     "20 pinos THT, congelado",
     "",
     "p.20  +24V",
     "p.17  +5V (bus, DGND)",
     "SPI: MOSI MISO CLK CS",
     "DGND"], C_CONN, "01"),
 "LDO": (950, 420, 195, 120, "LDO isolador", [
     "MCP1824ST-3302E",
     "+5V -> +3.3V_DIG",
     "alimenta VCC1 e EN1",
     "fecha o gap G2"], C_PWR, "04"),
 "P2":  (40, 420, 150, 185, "P2 Campo", [
     "Harwin M20-7821446",
     "14 pinos THT",
     "congelado",
     "",
     "6 lacos 4-20 mA",
     "alimentados a",
     "+24V_ADC"], C_CONN, "01"),
 "LAC": (225, 420, 200, 185, "Seis lacos", [
     "Por canal, do campo:",
     "TVS 33 V -> TPS26613",
     "  (25-40 mA, retry)",
     "-> burden 110 ohm",
     "-> 3,3 k + 100 nF",
     "-> BAV199 -> 4,7 k",
     "+12V_TPS: U14 TPS7A4001",
     "  +24V_ADC -> 12 V"], C_ANA, "06"),
 "ADC": (460, 420, 200, 210, "Conversor A/D", [
     "MCP3208T-BI/SL",
     "12 bits, INL +-1 LSB",
     "VREF = +2V5_REF",
     "",
     "CH0 CH1 CH2 CH3 campo",
     "CH4 termistor",
     "CH5 trilho, le 4095",
     "CH6 CH7 campo"], C_ANA, "05"),
 "ISO": (700, 420, 215, 160, "Barreira", [], C_DIG, "04"),
 "NTC": (225, 660, 200, 110, "Termistor", [
     "NTCS0603E3103 10 kohm",
     "de +2V5_REF ao CH4",
     "ERA3AEB 5,62 kohm",
     "Ratiometrico com o VREF"], C_ANA, "07"),
}

# ------------------------------------------------------- ligacoes (polilinhas)
# (origem, destino, [pontos], rotulo, indice do segmento que leva o rotulo)
LIGACOES = [
 # (orig, dest, pontos, rotulo, segmento, centro do rotulo opcional)
 ("P1", "ENT", [(1047,150),(1047,115),(407,115),(407,150)], "+24V atravessa a barreira sem isolamento", 1, (560,106)),
 ("P1", "LDO", [(1047,350),(1047,420)], "+5V", 0, None),
 ("LDO","ISO", [(1000,540),(1000,600),(860,600),(860,580)], "+3.3V_DIG", 1, None),
 ("P1", "ISO", [(950,300),(932,300),(932,500),(915,500)], "SPI 3,3 V", 1, None),
 ("ISO","ADC", [(700,440),(660,440)], "SPI isolado", 0, (680,411)),
 ("ENT","ALI", [(490,240),(570,240)], "+24V_REG", 0, None),
 ("ALI","ADC", [(620,335),(620,420)], "+2V5_REF", 0, None),
 ("NTC","ADC", [(425,700),(492,700),(492,630)], "CH4", 0, None),
 ("LAC","ADC", [(425,440),(460,440)], "CH0-3, CH6-7", 0, (442,411)),
 ("P2", "LAC", [(190,440),(225,440)], "6 x 4-20 mA", 0, (207,411)),
 ("ENT","LAC", [(340,335),(340,420)], "+24V_ADC", 0, None),
]

NOTA = (520, 672, 270, 112)
TIT  = (40, 630, 175, 150)
BARR_X = 807

# ============================================================ desenho
p = []
def add(s): p.append(s)
def esc(s):
    return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def retas(pts):
    return [(pts[i][0], pts[i][1], pts[i+1][0], pts[i+1][1]) for i in range(len(pts)-1)]

# ---- G2: nenhum segmento atravessa uma caixa que nao seja a sua ponta
def seg_corta(x1,y1,x2,y2, bx,by,bw,bh, folga=4):
    ax0,ax1 = min(x1,x2), max(x1,x2)
    ay0,ay1 = min(y1,y2), max(y1,y2)
    return (ax0 < bx+bw-folga and ax1 > bx+folga and
            ay0 < by+bh-folga and ay1 > by+folga)


def larg(s, fs=12):
    k = fs / 12.0
    w = 0.0
    for c in s:
        if c.isupper() or c.isdigit() or c in "+_%&@#": w += 7.6
        elif c in " .,:;|!'": w += 3.5
        else: w += 6.3
    return w * k

falhas = []
for orig, dest, pts, rot, idx, lc in LIGACOES:
    for (x1,y1,x2,y2) in retas(pts):
        for cid,(bx,by,bw,bh,_,_,_,_) in CAIXAS.items():
            if cid in (orig,dest):
                continue
            if seg_corta(x1,y1,x2,y2,bx,by,bw,bh):
                falhas.append("G2 %s->%s atravessa %s no segmento (%d,%d)-(%d,%d)"
                              % (orig,dest,cid,x1,y1,x2,y2))
        for nome,(bx,by,bw,bh) in (("NOTA",NOTA),("TITULO",TIT)):
            if seg_corta(x1,y1,x2,y2,bx,by,bw,bh):
                falhas.append("G2 %s->%s atravessa %s" % (orig,dest,nome))

# ---- G3: rotulo fora de qualquer caixa
def rot_caixa(pts, idx, rot, lc=None):
    (x1,y1,x2,y2) = retas(pts)[idx]
    mx, my = (x1+x2)/2.0, (y1+y2)/2.0
    if lc:
        mx, my = lc[0], lc[1] + 10
    w = len(rot)*6.1 + 12
    return (mx-w/2, my-19, w, 17)

for orig,dest,pts,rot,idx,lc in LIGACOES:
    rx,ry,rw,rh = rot_caixa(pts,idx,rot,lc)
    for cid,(bx,by,bw,bh,_,_,_,_) in CAIXAS.items():
        if seg_corta(rx,ry,rx+rw,ry+rh, bx,by,bw,bh, folga=0):
            falhas.append("G3 rotulo '%s' (%s->%s) cai dentro de %s" % (rot,orig,dest,cid))

for orig,dest,pts,rot,idx,lc in LIGACOES:
    rx,ry,rw,rh = rot_caixa(pts,idx,rot,lc)
    for nome,(bx,by,bw,bh) in (("NOTA",NOTA),("TITULO",TIT)):
        if seg_corta(rx,ry,rx+rw,ry+rh,bx,by,bw,bh,folga=0):
            falhas.append("G3 rotulo '%s' cai dentro de %s" % (rot,nome))

# ---- G5: rotulo nao pode tapar a linha de outra ligacao nem a barreira
BARREIRA = (BARR_X, 96, BARR_X, H-58)
for orig,dest,pts,rot,idx,lc in LIGACOES:
    rx,ry,rw,rh = rot_caixa(pts,idx,rot,lc)
    alheias = [s for (o,d,ps,_,_,_) in LIGACOES if (o,d)!=(orig,dest) for s in retas(ps)]
    for (x1,y1,x2,y2) in alheias + [BARREIRA]:
        if seg_corta(x1,y1,x2,y2, rx,ry,rw,rh, folga=0):
            falhas.append("G5 rotulo '%s' tapa o segmento (%d,%d)-(%d,%d)" % (rot,x1,y1,x2,y2))

# ---- G6: texto das caixas cabe na caixa
for cid,(bx,by,bw,bh,tit,linhas,_,_) in CAIXAS.items():
    for L in linhas:
        if larg(L) + 14 > bw:
            falhas.append("G6 linha '%s' de %s nao cabe na largura" % (L,cid))
    if 45 + 16*(len(linhas)-1) + 6 > bh:
        falhas.append("G6 %s tem linhas demais para a altura" % cid)

# ---- G4: titulo cabe na largura util
for cid,(bx,by,bw,bh,tit,_,_,cr) in CAIXAS.items():
    util = bw - 24 - (52 if cr else 0)
    if len(tit)*CHAR_W > util:
        falhas.append("G4 titulo '%s' de %s precisa de %.0f px e so ha %d"
                      % (tit,cid,len(tit)*CHAR_W,util))

if falhas:
    print("GUARDAS FALHARAM:")
    for f in falhas: print("   ", f)
    raise SystemExit(1)
print("guardas G2/G3/G4: OK")

add('<?xml version="1.0" encoding="UTF-8"?>')
add('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W,H,W,H))
add('<defs><marker id="pt" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
    'orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="%s"/></marker></defs>' % C_LINE)
add('<rect width="%d" height="%d" fill="#ffffff"/>' % (W,H))
add('<rect x="14" y="14" width="%d" height="%d" fill="none" stroke="%s" stroke-width="1.4"/>' % (W-28,H-28,C_LINE))

add('<text x="34" y="52" font-family="Segoe UI,Arial" font-size="23" font-weight="700" fill="%s">'
    'IC2S Extension Board EBM2 V5 &#8212; diagrama de blocos</text>' % C_LINE)
add('<text x="34" y="74" font-family="Segoe UI,Arial" font-size="13" fill="%s">'
    'Seis entradas 4-20 mA. Fluxo de sinal da esquerda para a direita: campo, conversor, barreira, barramento.</text>' % C_MUTE)

# barreira: tracos explicitos, porque o rasterizador ignora stroke-dasharray
def tracejado(x, y0, y1, cor, tr=10, vao=6, esp=2.4):
    y = y0
    while y < y1:
        add('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="%.1f"/>'
            % (x, y, x, min(y+tr, y1), cor, esp))
        y += tr + vao
tracejado(BARR_X, 96, H-58, C_BAR)
add('<text x="%d" y="%d" font-family="Segoe UI,Arial" font-size="12.5" font-weight="700" fill="%s" '
    'text-anchor="middle">BARREIRA FUNCIONAL</text>' % (BARR_X, H-38, C_BAR))
add('<text x="300" y="%d" font-family="Segoe UI,Arial" font-size="11.5" font-weight="700" fill="%s" '
    'text-anchor="middle">DOMINIO DE CAMPO &#8212; GND_ADC, unido a GND_24V por R2</text>' % (H-38,C_MUTE))
add('<text x="1010" y="%d" font-family="Segoe UI,Arial" font-size="11.5" font-weight="700" fill="%s" '
    'text-anchor="middle">DOMINIO DIGITAL &#8212; DGND</text>' % (H-38,C_MUTE))

# ligacoes primeiro, para ficarem por baixo das caixas
for orig,dest,pts,rot,idx,lc in LIGACOES:
    d = "M %d %d " % pts[0] + " ".join("L %d %d" % q for q in pts[1:])
    add('<path d="%s" fill="none" stroke="%s" stroke-width="2"/>' % (d,C_LINE))
    (ax,ay),(bx_,by_) = pts[-2], pts[-1]
    import math
    ang = math.atan2(by_-ay, bx_-ax)
    L, A = 11, 0.42
    p1 = (bx_ - L*math.cos(ang-A), by_ - L*math.sin(ang-A))
    p2 = (bx_ - L*math.cos(ang+A), by_ - L*math.sin(ang+A))
    add('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
        % (bx_,by_,p1[0],p1[1],p2[0],p2[1],C_LINE))
    rx,ry,rw,rh = rot_caixa(pts,idx,rot,lc)
    add('<rect x="%.0f" y="%.0f" width="%.0f" height="%.0f" rx="3" fill="#ffffff" opacity="0.95"/>' % (rx,ry,rw,rh))
    add('<text x="%.0f" y="%.0f" font-family="Segoe UI,Arial" font-size="11.5" fill="%s" '
        'text-anchor="middle">%s</text>' % (rx+rw/2, ry+12.5, C_LINE, esc(rot)))

# caixas
for cid,(x,y,w,h,tit,linhas,cor,cr) in CAIXAS.items():
    add('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" stroke="%s" stroke-width="1.8"/>'
        % (x,y,w,h,cor,C_LINE))
    add('<text x="%d" y="%d" font-family="Segoe UI,Arial" font-size="15" font-weight="700" fill="%s">%s</text>'
        % (x+12,y+25,C_LINE,esc(tit)))
    yy = y+45
    for L in linhas:
        add('<text x="%d" y="%d" font-family="Segoe UI,Arial" font-size="12" fill="%s">%s</text>'
            % (x+12,yy,C_MUTE,esc(L)))
        yy += 16
    if cr:
        add('<rect x="%d" y="%d" width="44" height="18" rx="4" fill="#ffffff" stroke="%s" stroke-width="1"/>'
            % (x+w-54,y+9,C_MUTE))
        add('<text x="%d" y="%d" font-family="Segoe UI,Arial" font-size="10.5" font-weight="700" fill="%s" '
            'text-anchor="middle">%s</text>' % (x+w-32,y+22,C_MUTE,esc(cr)))

# texto do isolador: cabecalho a toda a largura, depois uma coluna de cada lado da barreira
ix, iy, iw, ih = CAIXAS["ISO"][:4]
CAB = "ISO7141CCDBQR, TTL"
assert ix + 12 + larg(CAB) <= ix + iw - 6, "G8: cabecalho do isolador nao cabe"
add('<text x="%d" y="%d" font-family="Segoe UI,Arial" font-size="12" fill="%s">%s</text>'
    % (ix+12, iy+45, C_MUTE, esc(CAB)))
COL_E = ["lado 2: campo", "GND_ADC", "VCC2 3V3_REF"]
COL_D = ["lado 1: bus",   "DGND",    "VCC1 +3.3V_DIG"]
for col, x0, x1 in ((COL_E, ix+10, BARR_X-6), (COL_D, BARR_X+6, ix+iw-6)):
    yy = iy + 82
    for L in col:
        assert x0 + larg(L, 11) <= x1, "G8: '%s' invade a barreira ou a borda (%.0f > %d)" % (L, x0+larg(L, 11), x1)
        add('<text x="%d" y="%d" font-family="Segoe UI,Arial" font-size="11" fill="%s">%s</text>'
            % (x0, yy, C_MUTE, esc(L)))
        yy += 16
print("guarda G8 (texto do isolador nao cruza a barreira): OK")

# a barreira atravessa o ISO7141 por cima da caixa: e dentro dele que ela existe
_, iy, _, ih = CAIXAS["ISO"][0], CAIXAS["ISO"][1], CAIXAS["ISO"][2], CAIXAS["ISO"][3]
tracejado(BARR_X, iy+58, iy+ih-4, C_BAR, tr=6, vao=4, esp=1.8)

# nota
nx,ny,nw,nh = NOTA
add('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" stroke="%s" stroke-width="1.2"/>'
    % (nx,ny,nw,nh,C_NOTE,C_MUTE))
add('<text x="%d" y="%d" font-family="Segoe UI,Arial" font-size="12.5" font-weight="700" fill="%s">'
    'O que muda face a V4.1</text>' % (nx+12,ny+21,C_LINE))
yy = ny+40
for L in ["1. A referencia do ADC deixa de ser o trilho.",
          "2. O caminho de clamp acaba num sumidouro.",
          "3. Limite de corrente por laco (TPS26613).",
          "4. O bulk fica atras do fusivel de alto I2t.",
          "5. O mapa de canais NAO e sequencial."]:
    add('<text x="%d" y="%d" font-family="Segoe UI,Arial" font-size="11.5" fill="%s">%s</text>'
        % (nx+12,yy,C_MUTE,esc(L)))
    yy += 15

# bloco de titulo
tx,ty,tw,th = TIT
add('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="#ffffff" stroke="%s" stroke-width="1.6"/>'
    % (tx,ty,tw,th,C_LINE))
LT = [("EBM2 V5 (6AI)", 14, "700", C_LINE),
      ("Diagrama  |  F2 / 2.1", 11, "400", C_MUTE),
      ("Revisao B  |  2026-09-25", 11, "400", C_MUTE),
      ("2Solve", 12, "700", C_LINE),
      ("Verdade: os .kicad_sch", 10, "400", C_MUTE)]
yy = ty + 28
for txt, fs, fw, cor in LT:
    assert len(txt)*fs*0.56 + 24 <= tw, "G7: '%s' nao cabe no bloco de titulo" % txt
    add('<text x="%d" y="%d" font-family="Segoe UI,Arial" font-size="%d" font-weight="%s" fill="%s">%s</text>'
        % (tx+12, yy, fs, fw, cor, esc(txt)))
    yy += 26
assert yy - 26 + 8 <= ty + th, "G7: o bloco de titulo nao cabe na altura"
print("guarda G7 (bloco de titulo): OK")

add('</svg>')
svg = "\n".join(p)

# ---- G1 moldura
import re
for m in re.finditer(r'\b(x|x1|x2)="(-?\d+(?:\.\d+)?)"', svg):
    assert float(m.group(2)) <= W-14, "G1: sai da moldura em x"
for m in re.finditer(r'\b(y|y1|y2)="(-?\d+(?:\.\d+)?)"', svg):
    assert float(m.group(2)) <= H-14, "G1: sai da moldura em y"
print("guarda G1 (moldura): OK")

io.open(OUT,"w",encoding="utf-8",newline="").write(svg)
print("escrito:", OUT, len(svg), "bytes")
