# -*- coding: utf-8 -*-
"""Renumeracao das referencias da EBM2 V5 (2026-09-25): R1, R2, ... por ordem hierarquica, em vez de R2xx/R6xx.

Regra (decidida para o projecto; ver cabecalho de tabela_correspondencia_refs.md):
  1. Ordem das folhas 01 -> 07 (a ordem da hierarquia no raiz). Numeracao continua por prefixo, a comecar em 1.
  2. Dentro de cada folha: da esquerda para a direita e, na mesma coluna, de cima para baixo (x, depois y) — o
     sentido do sinal nas folhas 02 e 03.
  3. Folha 06 (seis lacos iguais): por FUNCAO e depois por canal 1..6. Assim o canal k de cada funcao e sempre
     base + k - 1 e as faixas antigas (U601-U606, D601-D616, ...) continuam contiguas. Depois, o bloco do U640.
  4. Prefixos: T -> TP (T e transformador; TP e o padrao da biblioteca KiCad), NTC R700 -> TH (padrao do
     simbolo Device:Thermistor_NTC). P1/P2 ficam: a pinagem congelada da V4.1 e o firmware citam P1/P2.
     FID101-103 -> FID1-3.
Nenhuma ligacao muda. As redes com nome automatico (Net-(R206-Pad1)) mudam de nome com a referencia, e o
rotulo FB_U640 passa a FB_<novo U>; a topologia tem de sair identica (confirmar com confere_renumeracao.py).

Uso: python renumera_referencias.py            -> so escreve a tabela e mostra o que mudaria (nada e gravado)
     python renumera_referencias.py --aplica   -> grava (backup .antes_renumera) nas folhas e nos ficheiros VIVOS
"""
import csv, glob, io, os, re, shutil, sys

R = r"C:\hw\hw-ebm2-v5"
K = os.path.join(R, "KiCad_EBM2_V5")
FOLHAS = ["01_conectores", "02_entrada", "03_alimentacao", "04_barreira", "05_adc", "06_lacos", "07_ntc"]
# Ficheiros vivos (documentos e ferramentas que continuam a ser usados). Os relatorios datados, as verificacoes
# anteriores, os scripts aplica_* e gera_lista_componentes.py (comparacao V4.1 x V5 de 23-09) sao registo historico:
# ficam com a numeracao antiga + a tabela de correspondencia. Como a nova numeracao nunca passa de 2 digitos
# (R40 e a maior), uma referencia de 3 digitos num texto e sempre da numeracao antiga, sem ambiguidade.
VIVOS = ["Documentos/intencao_EBM2_V5.md", "Documentos/planejamento_pcb_EBM2_V5.md",
         "Documentos/plano_teste_EBM2_V5_esqueleto.md", "Documentos/escopo_EBM2_V5_gaps.md",
         "Documentos/mapa_pinos_EBM2_V5.md", "Documentos/bom_preliminar_EBM2_V5.md",
         "Documentos/bom_preliminar_EBM2_V5.csv",
         "ferramentas/verifica_F2.py", "ferramentas/gera_bom_prelim.py", "ferramentas/gera_mapa_pinos.py",
         "ferramentas/gera_diagrama_blocos.py",
         "ferramentas/portao1/checklist_P1_projetista.md", "ferramentas/portao1/LEIA-ME_verificacao_cruzada_P1.md"]
NOVO_PREFIXO = {"T": "TP", "FID": "FID"}


def bloco(t, i):
    d = 0
    for j in range(i, len(t)):
        d += (t[j] == "(") - (t[j] == ")")
        if d == 0:
            return j + 1


def simbolos(t):
    for m in re.finditer(r"\n\t\(symbol\n", t):
        a = m.start(); b = bloco(t, a + 2)
        s = t[a:b]
        ref = re.search(r'\(property "Reference" "([^"]*)"', s).group(1)
        if ref.startswith("#"):
            continue
        at = re.search(r'\n\t\t\(at ([-\d.]+) ([-\d.]+)', s)
        lib = re.search(r'\(lib_id "([^"]*)"', s).group(1)
        yield ref, lib, float(at.group(1)), float(at.group(2))


def divide(ref):
    m = re.fullmatch(r"([A-Z]+)(\d+)", ref)
    return m.group(1), int(m.group(2))


# ---------- 1. tabela de correspondencia ----------
ordem, info = [], {}
for f in FOLHAS:
    t = io.open(os.path.join(K, f + ".kicad_sch"), encoding="utf-8", newline="").read()
    syms = list(simbolos(t))
    for ref, lib, x, y in syms:
        info[ref] = (f, lib, x, y)
    if f == "06_lacos":
        canal = [s for s in syms if divide(s[0])[0] in "RCDUF" and divide(s[0])[1] // 10 in (60, 61, 62, 66)
                 and 1 <= divide(s[0])[1] % 10 <= 6]
        resto = [s for s in syms if s not in canal]
        pos1 = {(divide(s[0])[0], divide(s[0])[1] // 10): (s[2], s[3]) for s in canal if divide(s[0])[1] % 10 == 1}
        canal.sort(key=lambda s: (pos1[(divide(s[0])[0], divide(s[0])[1] // 10)], divide(s[0])[1] % 10))
        syms = canal + sorted(resto, key=lambda s: (s[2], s[3]))
    else:
        syms.sort(key=lambda s: (s[2], s[3]))
    ordem += [s[0] for s in syms]

cont, MAPA = {}, {}
for ref in ordem:
    p, n = divide(ref)
    if p == "P":
        MAPA[ref] = ref
        continue
    np_ = "TH" if info[ref][1] == "Device:Thermistor_NTC" else NOVO_PREFIXO.get(p, p)
    cont[np_] = cont.get(np_, 0) + 1
    MAPA[ref] = "%s%d" % (np_, cont[np_])
assert len(set(MAPA.values())) == len(MAPA)

# ---------- 2. substituicao de texto (tokens, faixas, curingas) ----------
ANT = set(MAPA)


def novo_num(r):
    return divide(MAPA[r])


def faixa(refs):
    """refs antigas -> 'X1–X6' se as novas forem contiguas e do mesmo prefixo; senao None."""
    novos = sorted(novo_num(r) for r in refs)
    if len({p for p, _ in novos}) != 1:
        return None
    ns = [n for _, n in novos]
    if ns != list(range(ns[0], ns[0] + len(ns))):
        return None
    p = novos[0][0]
    return "%s%d" % (p, ns[0]) if len(ns) == 1 else "%s%d-%s%d" % (p, ns[0], p, ns[-1])


pend = []  # o que nao se consegue traduzir automaticamente


def traduz(txt, onde):
    # a) faixas "D601-D616" / "R661-666" / "R661–R666"
    def f_faixa(m):
        p, a, p2, b = m.group(1), int(m.group(2)), m.group(3) or m.group(1), int(m.group(4))
        if p2 != p:
            return m.group(0)
        refs = [r for r in ANT if divide(r)[0] == p and a <= divide(r)[1] <= b]
        if "%s%d" % (p, a) not in ANT or "%s%d" % (p, b) not in ANT:
            return m.group(0)
        out = faixa(refs)
        if out is None:
            pend.append((onde, m.group(0), "faixa nao contigua depois da renumeracao"))
            return m.group(0)
        return out
    txt = re.sub(r"\b([A-Z]{1,3})(\d{3})\s?[-–]\s?([A-Z]{1,3})?(\d{3})\b", f_faixa, txt)

    # b) curingas "U60x" (todos) e "U60k" (canal k)
    def f_cur(m):
        p, dd, w = m.group(1), m.group(2), m.group(3)
        refs = sorted((r for r in ANT if divide(r)[0] == p and str(divide(r)[1]).startswith(dd)
                       and len(str(divide(r)[1])) == 3), key=lambda r: divide(r)[1])
        if not refs:
            return m.group(0)
        if w == "x":
            out = faixa(refs)
        else:  # canal k: so vale se 1..6 existirem e forem contiguos
            um = [r for r in refs if 1 <= divide(r)[1] % 10 <= 6]
            out = None
            if len(um) == 6 and faixa(um):
                pn, n1 = novo_num(um[0])
                out = "%s(%d+k)" % (pn, n1 - 1)
        if out is None:
            pend.append((onde, m.group(0), "curinga sem traducao contigua"))
            return m.group(0)
        return out
    txt = re.sub(r"\b([A-Z]{1,3})(\d{2})([xk])\b", f_cur, txt)

    # c) referencias isoladas
    return re.sub(r"\b([A-Z]{1,3}\d{3})\b", lambda m: MAPA.get(m.group(1), m.group(1)), txt)


def trata_folha(t, onde):
    # referencias dos simbolos e das instancias
    def f_sym(m):
        s = m.group(0)
        ref = re.search(r'\(property "Reference" "([^"]*)"', s).group(1)
        if ref.startswith("#") or ref not in MAPA:
            return s
        n = MAPA[ref]
        s = s.replace('(property "Reference" "%s"' % ref, '(property "Reference" "%s"' % n, 1)
        s = s.replace('(reference "%s")' % ref, '(reference "%s")' % n)
        return s
    partes, i = [], 0
    for m in re.finditer(r"\n\t\(symbol\n", t):
        a = m.start(); b = bloco(t, a + 2)
        partes.append(t[i:a]); partes.append(f_sym(re.match(r"[\s\S]*", t[a:b])))
        i = b
    partes.append(t[i:])
    t = "".join(partes)
    # textos, descricoes, rotulos: so dentro de cadeias entre aspas
    return re.sub(r'"((?:[^"\\]|\\.)*)"', lambda m: '"' + traduz(m.group(1), onde) + '"', t)


tabela = os.path.join(R, "Documentos", "tabela_correspondencia_refs_EBM2_V5.csv")
alvo = [(os.path.join(K, f + ".kicad_sch"), True) for f in FOLHAS] + [(os.path.join(R, v), False) for v in VIVOS]
novos = {}
for f, e_folha in alvo:
    t = io.open(f, encoding="utf-8", newline="").read()
    n = trata_folha(t, os.path.basename(f)) if e_folha else traduz(t, os.path.basename(f))
    novos[f] = (t, n)
    ant = set(re.findall(r"\b[A-Z]{1,3}\d{3}\b", t)) & ANT
    sobra = set(re.findall(r"\b[A-Z]{1,3}\d{3}\b", n)) & ANT - {"P1", "P2"}
    print("%-44s %4d refs antigas -> sobram %d %s" % (os.path.basename(f), len(ant), len(sobra), sorted(sobra)[:8]))
for p in pend:
    print("PENDENTE:", p)

with io.open(tabela, "w", encoding="utf-8", newline="") as h:
    w = csv.writer(h)
    w.writerow(["folha", "ref_antiga", "ref_nova", "lib_id", "x_mm", "y_mm"])
    for ref in ordem:
        f, lib, x, y = info[ref]
        w.writerow([f, ref, MAPA[ref], lib, x, y])
print("tabela:", tabela, "|", len(MAPA), "referencias |", {p: c for p, c in sorted(cont.items())})

if "--aplica" in sys.argv:
    if pend:
        sys.exit("ABORTA: ha pendentes; traduzir a mao antes de aplicar")
    for f, (t, n) in novos.items():
        if t != n:
            shutil.copy2(f, f + ".antes_renumera")
            io.open(f, "w", encoding="utf-8", newline="").write(n)
    print("aplicado em", sum(1 for t, n in novos.values() if t != n), "ficheiros")
