# -*- coding: utf-8 -*-
"""Construtor de folhas KiCad 10 para a F2 da EBM2 V5.

Gera uma subfolha inteira a partir de uma especificacao em Python: simbolos
(copiados das definicoes embebidas nas folhas ja verificadas, da biblioteca
padrao do KiCad, da V4.1 ou da Legacy), portos de trilho, fios, juncoes,
rotulos hierarquicos e locais, no-connects, texto e linhas tracejadas.

Antes de escrever, recusa se:
  - uma ponta de fio ficar solta, um pino cair no meio de um fio, um no de 3+
    ligacoes nao tiver juncao, ou houver juncao desnecessaria;
  - um pino de simbolo ficar sem ligacao nem no-connect;
  - um rotulo nao estiver sobre uma ponta de fio ou um pino;
  - uma coordenada colocada sair da grelha de 1,27 mm;
  - um texto sair do quadro (A4, ou A3 com papel = "A3") ou invadir o bloco de titulo;
  - falhar qualquer das cinco guardas de escrita da casa.
A prova final nao e este ficheiro: e a netlist exportada pelo kicad-cli.
"""
import io, math, os, re, uuid
from netlist_diff import parse, filhos

RAIZ_UUID = "873bf552-94cb-4fe4-9213-f79e9821baca"
PROJECTO = "IC2S_Extension_Board-EBM2_V5"
STD = r"C:\Program Files\KiCad\10.0\share\kicad\symbols"


def r4(v):
    return round(v + 0.0, 4)


def nu():
    return str(uuid.uuid4())


def f(v):
    return ("%.4f" % v).rstrip("0").rstrip(".")


def fim(s, i):
    d = 0; den = False
    while True:
        c = s[i]
        if c == '"' and s[i - 1] != "\\":
            den = not den
        elif not den:
            if c == "(":
                d += 1
            elif c == ")":
                d -= 1
                if d == 0:
                    return i + 1
        i += 1


# ------------------------------------------------------------------ bibliotecas
def blocos_lib_de_folha(caminho):
    t = io.open(caminho, encoding="utf-8").read()
    out = {}
    a = t.find("\n\t(lib_symbols")
    if a < 0:
        return out
    b = fim(t, a + 1)
    k = a
    while True:
        k = t.find("\n\t\t(symbol \"", k, b)
        if k < 0:
            break
        e = fim(t, k + 1)
        blk = t[k + 1:e]
        nome = re.match(r'\t\t\(symbol "([^"]+)"', blk).group(1)
        out[nome] = blk
        k = e          # procurar a partir do fim: o bloco seguinte comeca logo pela quebra de linha
    return out


def bloco_lib_padrao(ficheiro, nome, lib):
    t = io.open(os.path.join(STD, ficheiro), encoding="utf-8").read()
    k = t.find('\n\t(symbol "%s"' % nome)
    assert k >= 0, "%s nao encontrado em %s" % (nome, ficheiro)
    e = fim(t, k + 1)
    blk = t[k + 1:e]
    assert "(extends" not in blk, "simbolo com extends: tratar a parte"
    blk = blk.replace('(symbol "%s"' % nome, '(symbol "%s:%s"' % (lib, nome), 1)
    return "\t" + blk.replace("\n", "\n\t")


def pinos_de_bloco(blk):
    arv = parse(blk)
    pins = {}
    def anda(n):
        for x in n:
            if isinstance(x, list) and x:
                if x[0] == "pin":
                    at = filhos(x, "at")[0]
                    num = filhos(x, "number")[0][1]
                    nome = filhos(x, "name")[0][1]
                    pins[num] = (float(at[1]), float(at[2]), nome, x[1])
                elif x[0] == "symbol":
                    anda(x)
    anda(arv)
    return pins


def pos_pino(px, py, X, Y, rot, espelho=None):
    x, y = px, -py
    if espelho == "y":
        x = -x
    elif espelho == "x":
        y = -y
    a = math.radians(rot)
    return round(X + x * math.cos(a) + y * math.sin(a), 4), round(Y - x * math.sin(a) + y * math.cos(a), 4)


def efeitos(just=None):
    j = "\n\t\t\t\t(justify %s)" % just if just else ""
    return "(effects\n\t\t\t\t(font\n\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)%s\n\t\t\t)" % j


def prop(nome, valor, x, y, ang, visivel, just=None):
    h = "" if visivel else "\n\t\t\t(hide yes)"
    return ('\t\t(property "%s" "%s"\n\t\t\t(at %s %s %s)%s\n\t\t\t(show_name no)\n\t\t\t(do_not_autoplace no)\n\t\t\t%s\n\t\t)'
            % (nome, valor, f(x), f(y), f(ang), h, efeitos(just)))


# ------------------------------------------------------------------ folha
class Folha:
    def __init__(self, caminho, folha_uuid, libs):
        self.caminho = caminho
        self.folha_uuid = folha_uuid
        self.libs = libs                # {lib_id: bloco}
        self.usadas = {}
        self.simbolos = []              # texto
        self.pinos = {}                 # "REF.N" -> (x, y)
        self.pinos_simbolo = {}         # ref -> [pinos]
        self.portos = []                # (valor, x, y)
        self.fios, self.juncoes, self.nc = [], [], []
        self.rotulos = []               # (tipo, nome, x, y, ang, forma, just)
        self.textos, self.linhas = [], []
        self.n_pwr = 0
        self.papel = "A4"                # rev. 2.4: a folha 06 passa a A3

    def _lib(self, lib_id):
        assert lib_id in self.libs, "biblioteca sem %s" % lib_id
        self.usadas[lib_id] = self.libs[lib_id]
        return pinos_de_bloco(self.libs[lib_id])

    def simbolo(self, lib_id, ref, valor, x, y, rot=0, pegada="", mpn="", descr="", espelho=None,
                ref_pos=None, val_pos=None, bom=True, ds=""):
        pins = self._lib(lib_id)
        x, y = r4(x), r4(y)
        ref_pos = ref_pos or (x + 2.54, y - 1.27, 0, "left")
        val_pos = val_pos or (x + 2.54, y + 1.27, 0, "left")
        # Regra medida em 2026-09-23 numa experiencia com 16 casos: o KiCad desenha o
        # campo a (angulo guardado + rotacao do simbolo) e, se der 180, vira-o e troca o
        # justify. Guardar o simetrico da rotacao da texto horizontal e justify fiel.
        # EXCEPCAO medida depois (exp180, 23-09-2026, dir do texto no PDF): com o simbolo a
        # 180, guardar 180 sai de pernas para o ar no PDF; guardar 0 sai direito.
        ang_h = 0 if rot % 360 == 180 else (-rot) % 360
        ref_pos = (ref_pos[0], ref_pos[1], ang_h, ref_pos[3])
        val_pos = (val_pos[0], val_pos[1], ang_h, val_pos[3])
        m = "\n\t\t(mirror %s)" % espelho if espelho else ""
        linhas = ['\t(symbol\n\t\t(lib_id "%s")\n\t\t(at %s %s %s)%s\n\t\t(unit 1)\n\t\t(body_style 1)\n'
                  '\t\t(exclude_from_sim no)\n\t\t(in_bom %s)\n\t\t(on_board yes)\n\t\t(in_pos_files yes)\n'
                  '\t\t(dnp no)\n\t\t(uuid "%s")' % (lib_id, f(x), f(y), f(rot), m, "yes" if bom else "no", nu())]
        linhas.append(prop("Reference", ref, *ref_pos[:3], ref_pos[3] is not False and not str(ref).startswith("#"), ref_pos[3] or None))
        linhas.append(prop("Value", valor, *val_pos[:3], True, val_pos[3] or None))
        linhas.append(prop("Footprint", pegada, x, y, rot, False))
        linhas.append(prop("Datasheet", ds, x, y, rot, False))
        linhas.append(prop("Description", descr, x, y, rot, False))
        if mpn is not None:
            linhas.append(prop("MPN", mpn, x, y, rot, False))
        for n in sorted(pins, key=lambda z: (len(z), z)):
            linhas.append('\t\t(pin "%s"\n\t\t\t(uuid "%s")\n\t\t)' % (n, nu()))
            self.pinos["%s.%s" % (ref, n)] = pos_pino(pins[n][0], pins[n][1], x, y, rot, espelho)
        self.pinos_simbolo[ref] = list(pins)
        linhas.append('\t\t(instances\n\t\t\t(project "%s"\n\t\t\t\t(path "/%s/%s"\n\t\t\t\t\t(reference "%s")\n'
                      '\t\t\t\t\t(unit 1)\n\t\t\t\t)\n\t\t\t)\n\t\t)\n\t)' % (PROJECTO, RAIZ_UUID, self.folha_uuid, ref))
        self.simbolos.append("\n".join(linhas))
        return {n: self.pinos["%s.%s" % (ref, n)] for n in pins}

    def porto(self, valor, x, y, lib_id, rot=0, val_pos=None, prefixo="#PWR", base=0):
        """Porto de trilho: o nome da rede e o campo Value (AMBIENTE 4.4)."""
        self.n_pwr += 1
        x, y = r4(x), r4(y)
        ref = "%s%d" % (prefixo, base + self.n_pwr)
        if val_pos is None:
            baixo = lib_id == "power:GND"
            val_pos = (x, y + (3.81 if baixo else -3.81), 0, None)
        self.simbolo(lib_id, ref, valor, x, y, rot, mpn=None, val_pos=val_pos, ref_pos=(x, y, rot, False))
        self.portos.append((valor, x, y))

    def fio(self, *pts):
        pts = [(r4(a), r4(b)) for a, b in pts]
        for i in range(len(pts) - 1):
            self.fios.append((pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1]))

    def juncao(self, x, y):
        self.juncoes.append((r4(x), r4(y)))

    def no_connect(self, p):
        self.nc.append((r4(p[0]), r4(p[1])))

    def rotulo(self, nome, x, y, ang=0, just="left bottom"):
        self.rotulos.append(("label", nome, r4(x), r4(y), ang, None, just))

    def hier(self, nome, x, y, ang, forma, just):
        self.rotulos.append(("hierarchical_label", nome, r4(x), r4(y), ang, forma, just))

    def texto(self, linhas, x, y, dy=3.81):
        for i, L in enumerate(linhas):
            self.textos.append((L, x, y + i * dy))

    def linha_tracejada(self, *pts):
        self.linhas.append(pts)

    # -------------------------------------------------------------- verificacao
    def verifica(self):
        erros = []
        pts_pino = {}
        for k, p in self.pinos.items():
            if k.startswith("#"):
                continue
            pts_pino.setdefault(p, set()).add(k.split(".")[0])
        for v, x, y in self.portos:
            pts_pino.setdefault((x, y), set()).add("porto:%s@%s,%s" % (v, x, y))
        pontas = {}
        for s in self.fios:
            for p in ((s[0], s[1]), (s[2], s[3])):
                pontas[p] = pontas.get(p, 0) + 1
            if s[0] != s[2] and s[1] != s[3]:
                erros.append("fio diagonal %s" % (s,))

        def sobre(p, s):
            (x, y), (x1, y1, x2, y2) = p, s
            if abs(x1 - x2) < 1e-6:
                return abs(x - x1) < 1e-6 and min(y1, y2) + 1e-6 < y < max(y1, y2) - 1e-6
            return abs(y - y1) < 1e-6 and min(x1, x2) + 1e-6 < x < max(x1, x2) - 1e-6
        for p, n in pontas.items():
            tot = n + len(pts_pino.get(p, ()))
            if tot == 1:
                if not any(r[2] == p[0] and r[3] == p[1] for r in self.rotulos):
                    erros.append("ponta de fio solta em %s" % (p,))
            if tot >= 3 and p not in self.juncoes:
                erros.append("no de %d ligacoes sem juncao em %s" % (tot, p))
        for p, quem in pts_pino.items():
            for s in self.fios:
                if sobre(p, s):
                    erros.append("pino %s no meio do fio %s" % (sorted(quem), s))
        for s in self.fios:
            for t2 in self.fios:
                if s is not t2:
                    for p in ((s[0], s[1]), (s[2], s[3])):
                        if sobre(p, t2) and p not in self.juncoes:
                            erros.append("ponta de fio %s encosta no meio do fio %s sem juncao" % (p, t2))
        for p in self.juncoes:
            if pontas.get(p, 0) + len(pts_pino.get(p, ())) < 3:
                erros.append("juncao desnecessaria em %s" % (p,))
        ligados = set(pontas) | set(self.juncoes)
        for tipo, nome, x, y, a, fo, j in self.rotulos:
            if (x, y) not in ligados and (x, y) not in pts_pino and not any(sobre((x, y), s) for s in self.fios):
                erros.append("rotulo %s em %s,%s nao toca fio nem pino" % (nome, x, y))
        for k, p in self.pinos.items():
            if k.startswith("#"):
                continue
            outros = pts_pino.get(p, set()) - {k.split(".")[0]}
            if p not in ligados and p not in self.nc and not outros:
                erros.append("pino sem ligacao: %s em %s" % (k, p))
        for p in self.nc:
            if p not in pts_pino:
                erros.append("no-connect fora de pino em %s" % (p,))
            elif p in pontas:
                erros.append("no-connect num pino ligado em %s" % (p,))
        return erros

    # -------------------------------------------------------------- escrita
    def texto_ficheiro(self, comentarios):
        t0 = io.open(self.caminho, encoding="utf-8").read()
        cab = t0[:t0.find("\n\t(title_block")]
        if self.papel != "A4":
            assert cab.count('(paper "A4")') == 1, "cabecalho sem paper A4"
            cab = cab.replace('(paper "A4")', '(paper "%s")' % self.papel)
        tb = ('\n\t(title_block\n\t\t(title "IC2S Extension Board EBM2 V5 - 6AI")\n\t\t(date "2026-09-25")\n'
              '\t\t(rev "V5")\n\t\t(company "2Solve")\n' +
              "".join('\t\t(comment %d "%s")\n' % (i + 1, c) for i, c in enumerate(comentarios)) + "\t)")
        libs = "\n".join(self.usadas[k] for k in sorted(self.usadas))
        itens = []
        for s in self.fios:
            itens.append('\t(wire\n\t\t(pts\n\t\t\t(xy %s %s) (xy %s %s)\n\t\t)\n\t\t(stroke\n\t\t\t(width 0)\n'
                         '\t\t\t(type default)\n\t\t)\n\t\t(uuid "%s")\n\t)' % (f(s[0]), f(s[1]), f(s[2]), f(s[3]), nu()))
        for x, y in self.juncoes:
            itens.append('\t(junction\n\t\t(at %s %s)\n\t\t(diameter 0)\n\t\t(color 0 0 0 0)\n\t\t(uuid "%s")\n\t)'
                         % (f(x), f(y), nu()))
        for x, y in self.nc:
            itens.append('\t(no_connect\n\t\t(at %s %s)\n\t\t(uuid "%s")\n\t)' % (f(x), f(y), nu()))
        for tipo, nome, x, y, a, forma, just in self.rotulos:
            fo = "\n\t\t(shape %s)" % forma if forma else ""
            itens.append('\t(%s "%s"%s\n\t\t(at %s %s %s)\n\t\t(effects\n\t\t\t(font\n\t\t\t\t(size 1.27 1.27)\n'
                         '\t\t\t)\n\t\t\t(justify %s)\n\t\t)\n\t\t(uuid "%s")\n\t)' % (tipo, nome, fo, f(x), f(y), f(a), just, nu()))
        for pts in self.linhas:
            xy = " ".join("(xy %s %s)" % (f(a), f(b)) for a, b in pts)
            itens.append('\t(polyline\n\t\t(pts\n\t\t\t%s\n\t\t)\n\t\t(stroke\n\t\t\t(width 0.254)\n\t\t\t(type dash)\n'
                         '\t\t\t(color 176 48 48 1)\n\t\t)\n\t\t(uuid "%s")\n\t)' % (xy, nu()))
        for L, x, y in self.textos:
            itens.append('\t(text "%s"\n\t\t(exclude_from_sim no)\n\t\t(at %s %s 0)\n\t\t(effects\n\t\t\t(font\n'
                         '\t\t\t\t(size 1.27 1.27)\n\t\t\t)\n\t\t\t(justify left bottom)\n\t\t)\n\t\t(uuid "%s")\n\t)'
                         % (L, f(x), f(y), nu()))
        corpo = "\n".join(itens + self.simbolos)
        return cab + tb + "\n\t(lib_symbols\n" + libs + "\n\t)\n" + corpo + "\n\t(embedded_fonts no)\n)\n"

    def guardas(self, t):
        erros = []
        if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", t): erros.append("caractere de controlo")
        if re.search(r"\(at [-\d.]+ [-\d.]+ \)", t): erros.append("(at x y) sem angulo")
        if "999999" in t: erros.append("999999")
        if "justify center" in t: erros.append("justify center")
        d = 0; den = False
        for i, c in enumerate(t):
            if c == '"' and t[i - 1] != "\\":
                den = not den
            elif not den:
                d += (c == "(") - (c == ")")
                if d < 0:
                    erros.append("parentese a mais em %d" % i); break
        if d != 0 or den: erros.append("parenteses desequilibrados")
        a = t.find("\n\t(lib_symbols"); b = fim(t, a + 1)
        colocado = re.sub(r'\n\t\(text "[^"]*"\n\t\t\(exclude_from_sim no\)\n\t\t\(at [^)]*\)', "", t[:a] + t[b:])
        fora = sorted({v for m in re.finditer(r"\((?:at|xy) (-?[\d.]+) (-?[\d.]+)", colocado)
                       for v in m.groups() if abs(float(v) / 1.27 - round(float(v) / 1.27)) > 0.004})
        if fora: erros.append("fora da grelha: %s" % fora[:12])
        for L, x, y in self.textos:
            xe = x + len(L) * 1.15
            W, H = {"A4": (297, 210), "A3": (420, 297)}[self.papel]
            if xe > W - 10 or y > H - 15 or (xe > W - 122 and y > H - 46):
                erros.append("texto fora do quadro ou no bloco de titulo: %r" % L)
            if '"' in L or "\\" in L:
                erros.append("aspas ou barra num texto: %r" % L)
        return erros
