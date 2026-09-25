# -*- coding: utf-8 -*-
"""Lista V4.1 -> V5: que peca havia, que peca fica, e porque.

Referencias e part numbers saem das DUAS netlists exportadas (V4.1 so leitura, V5
actual); a correspondencia e a tabela da intencao rev. 2 sec. 2; as justificacoes
citam o planejamento rev. 3 e a intencao. Nada de valores escritos a mao.

Uso: python gera_lista_componentes.py v41.net v5.net saida.md
"""
import io, re, sys
from collections import OrderedDict
from netlist_diff import ler

v41, _, _ = ler(sys.argv[1])
v5, _, _ = ler(sys.argv[2])


def peca(c, r):
    x = c[r]
    return x.get("MPN") or x["value"]


def tem_mpn(c, r):
    return bool(c[r].get("MPN"))


def norm(s):
    return re.sub(r"[-\s]", "", s).upper()


# (funcao, [refs V4.1], [refs V5], porque) -- correspondencia da intencao rev. 2 sec. 2
PARES = [
    ("Conector do barramento", ["P1"], ["P1"], "Pinagem congelada (RC2)."),
    ("Conector de campo", ["P2"], ["P2"], "Pinagem congelada (RC2)."),
    ("Isolador digital", ["U4"], ["U400"], "Mesma peça. VCC1 passa a 3,3 V pelo U401 novo (fecha G2). Símbolo da EBM7 Legacy."),
    ("Conversor A/D", ["U5"], ["U500"], "Grau -CI → -BI: mesmo encapsulamento e pinagem, INL ±1 LSB em vez de ±2 (planejamento 2.1, 2.7b)."),
    ("LDO 3,3 V do ADC", ["U11"], ["U201"], "Mesma peça; o MPN completo passa a constar."),
    ("Ferrite do VCC2 do isolador", ["FB2"], ["FB400"], ""),
    ("Ferrite do VDD do conversor", ["FB3"], ["FB500"], ""),
    ("Desacoplamento VCC1 do isolador", ["C7"], ["C401"], ""),
    ("Desacoplamento VCC2 do isolador", ["C8"], ["C403"], ""),
    ("Desacoplamento VDD do conversor", ["C10"], ["C502"], "Mantém-se; acresce o C501 de 1 µF que o datasheet pede (§ 6.4, pág. 23)."),
    ("Termístor de placa", ["R5"], ["R700"], "Mesma peça. Topo em +2V5_REF em vez de 3V3_REF (planejamento 2.7e); símbolo de NTC."),
    ("Divisor do termistor", ["R8"], ["R701"], ""),
    ("Pull-up do EN do SPX3819", ["R34"], ["R203"], ""),
    ("Canais 1-6: fusível", ["F1", "F2", "F3", "F4", "F5", "F6"], ["F601", "F602", "F603", "F604", "F605", "F606"],
     "100 mA 0603 → 50 mA 1206, a peça da EBM7 Legacy. Rev. 2.1: abre só no curto franco à massa (~2,5 A); o curto do transmissor é do limitador U60x."),
    ("Canais 1-6: TVS no retorno", ["D4", "D7", "D13", "D22", "D2", "D12"], ["D601", "D602", "D603", "D604", "D605", "D606"], "30 V SMA → 36 V SMB 600 W (rev. 2.2): envolvente 18–32 V; em curto o retorno sobe ao trilho (31,4 V)."),
    ("Canais 1-6: TVS no trilho", ["D3", "D6", "D10", "D1", "D11", "D21"], ["D611", "D612", "D613", "D614", "D615", "D616"],
     "Mantidos os seis, num trilho único (+24V_ADC). 30 V → 36 V (rev. 2.2): a 32 V o trilho chega a 31,4 V. É o da EBM7."),
    ("Canais 1-6: série de protecção", ["R6", "R11", "R18", "R15", "R1", "R4"], ["R601", "R602", "R603", "R604", "R605", "R606"], "249 Ω 0603 → 100 Ω 1206 (rev. 2.1/2.2): o curto passa a ser do limitador; 100 Ω para a tensão ao transmissor a 18 V."),
    ("Canais 1-6: burden", ["R9", "R13", "R21", "R17", "R3", "R14"], ["R611", "R612", "R613", "R614", "R615", "R616"],
     "160 Ω 1 % → 110 Ω 0,1 % 25 ppm/°C: com VREF 2,5 V, 20 mA x 110 Ω = 2,2 V (planejamento 2.5). Em 1206 desde a rev. 2.1."),
    ("Canais 1-6: antialias 3,3 kΩ", ["R7", "R12", "R19", "R16", "R2", "R10"], ["R621", "R622", "R623", "R624", "R625", "R626"], ""),
    ("Canais 1-6: condensador do filtro", ["C9", "C13", "C18", "C3", "C1", "C2"], ["C601", "C602", "C603", "C604", "C605", "C606"], ""),
    ("Canais 1-6: clamp", ["D5", "D8", "D14", "D23", "D9", "D20"], ["D621", "D622", "D623", "D624", "D625", "D626"],
     "BAT54S → BAV199 (EBM7): fuga de 5 nA a 25 °C contra µA do Schottky (planejamento 2.1)."),
    ("LED do 5 V", ["D18"], ["D204"], "Passa a indicar +5V_ADC (intenção § 11)."),
    ("LED de trilho de laço", ["D19"], ["D630"], "Passa a indicar +24V_ADC, o F202 inteiro."),
    ("LED de trilho de laço", ["D25"], ["D203"], "Passa a indicar a entrada de +24V."),
    ("Resistência do LED do 5 V", ["R24"], ["R208"], ""),
    ("Resistência do LED", ["R25"], ["R630"], ""),
    ("Resistência do LED", ["R26"], ["R207"], ""),
]

# o que sai e o que entra: o porque vem do planejamento § 2.2-2.4 e da intenção
SAI = OrderedDict([
    (("U1", "U7", "U8"), "Conversores isolados: a V5 alimenta o campo a partir do 24 V, sem isolamento de potência (folhas 02 e 03)."),
    (("D15", "D16", "D24"), "PMEG6010CEH de 60 V: curto contra o grampo de 58,1 V do D200; substituídos pelo MBR1H100SF de 100 V."),
    (("D17",), "Sai (lista da intenção § 2). **Motivo individual não escrito.**"),
    (("D26",), "Zener de 2,45 V em serie na entrada: conduzia ~130 mA de uma peça de classe µA (notas da folha 02)."),
    (("F7", "F9"), "I²t de fusão 1,5e-3 A²s contra 5,65e-3 A²s de arranque dos 10 µF: avaria medida na V4.1 (notas da folha 02). Substituidos por CC12H (Eaton)."),
    (("F8",), "Sai com a entrada antiga (lista da intenção § 2). **Motivo individual não escrito.**"),
    (("C12", "C28"), "Electrolíticos de 50 V ficavam 8,1 V abaixo do grampo; substituídos pelo cerâmico C201 de 100 V."),
    (("FB4",), "Sai (lista da intenção § 2). **Motivo individual não escrito.**"),
])


def refs_ordenados(rs):
    return sorted(rs, key=lambda r: (re.sub(r"\d", "", r), int(re.sub(r"\D", "", r) or 0)))


def agrupa(c, refs):
    g = OrderedDict()
    for r in refs:
        k = ("`%s`" % peca(c, r)) if (c is v41 or tem_mpn(c, r)) else ("%s *(sem MPN)*" % peca(c, r))
        g.setdefault(k, []).append(r)
    return "<br>".join("%s %s" % (p, ", ".join(rs)) for p, rs in g.items())


usados41, usados5 = set(), set()
L = []
L.append("# Componentes: V4.1 → V5 — EBM2 V5 (6AI 4-20 mA)\n")
L.append("Data: 2026-09-23. Estado: esquemático da F2, etapa 2.2b.\n")
L.append("Gerado por `ferramentas/gera_lista_componentes.py` a partir das duas netlists exportadas pelo")
L.append("KiCad: a da V4.1 (`C:\\hw\\hw-ebm2-v4.1`, só leitura) e a da V5 actual. A correspondência")
L.append("entre designadores é a da `intencao_EBM2_V5.md` rev. 2, §2; as justificações citam o")
L.append("`planejamento_pcb_EBM2_V5.md` rev. 3 e a intenção. Os part numbers não foram escritos à mão.\n")
L.append("## 1 · Peças que continuam, com o designador novo\n")
L.append("| Função | V4.1 | V5 | Muda? | Porquê |")
L.append("|---|---|---|---|---|")
n_igual = n_muda = n_fixar = 0
# mesma peca com o MPN escrito de outra forma (SPX3819-3.3 = SPX3819M5-L-3-3/TR, SOT-23-5)
MESMA = {"LDO 3,3 V do ADC"}
for func, a, b, pq in PARES:
    for r in a: assert r in v41, r
    for r in b: assert r in v5, r
    usados41.update(a); usados5.update(b)
    pa = {norm(peca(v41, r)) for r in a}; pb = {norm(peca(v5, r)) for r in b}
    if func in MESMA:
        estado = "não"
    elif not all(tem_mpn(v5, r) for r in b):
        estado = "MPN por fixar"; n_fixar += 1
    elif pa != pb:
        estado = "**sim**"
    else:
        estado = "não"
    n_muda += estado == "**sim**"; n_igual += estado == "não"
    L.append("| %s | %s | %s | %s | %s |" % (func, agrupa(v41, a), agrupa(v5, b), estado, pq or "—"))

L.append("\n## 2 · Peças da V4.1 que saem\n")
L.append("| V4.1 | Porquê |")
L.append("|---|---|")
sai_expl = set()
for rs, pq in SAI.items():
    for r in rs: assert r in v41, r
    sai_expl.update(rs)
    L.append("| %s | %s |" % (agrupa(v41, rs), pq))
resto41 = refs_ordenados(set(v41) - usados41 - sai_expl)
if resto41:
    L.append("| %s | Condensadores sem correspondente na V5: a intenção (§2) di-los ao serviço dos conversores que saem. **Não se conferiu um a um.** |"
             % agrupa(v41, resto41))

L.append("\n## 3 · Peças novas na V5\n")
NOVO_PQ = OrderedDict([
    ("D200", "TVS de entrada 33 V: a V4.1 não tem nenhum (planejamento 2.2)."),
    ("F201", "Fusível da rama do regulador, CC12H 250 mA (a série não tem 100 mA)."),
    ("F202", "Fusível da rama dos laços, CC12H 750 mA: margem de arranque 41,7× (planejamento 2.6)."),
    ("D201", "Bloqueio 100 V da rama do regulador."), ("D202", "Bloqueio 100 V da rama dos laços."),
    ("R206", "Limitador de arranque 33 Ω (rev. 2.2, margem 12,3× a 32 V): sem ele o F201 não cumpre RA2. **MPN por fixar (V5).**"),
    ("R200", "Net-tie 0 Ω, único caminho GND_24V ↔ GND_ADC."),
    ("C200", "Entrada do regulador 2,2 µF/100 V 1206. **MPN por fixar (V6).**"),
    ("C201", "Bulk dos laços 10 µF/100 V, no lugar dos electrolíticos."),
    ("U200", "Regulador 24 → 4,974 V (EBM7)."), ("R201", "Divisor do U200."), ("R202", "Divisor do U200."),
    ("C202", "Saída do U200."), ("C203", "Saída do U200."),
    ("C204", "Saída do SPX3819."), ("C205", "Saída do SPX3819."), ("C208", "BP do SPX3819: baixo ruído."),
    ("U202", "Referência 2,5 V ±0,02 % (EBM7): VREF deixa de ser o VDD."),
    ("C206", "Entrada do ADR4525."), ("C207", "Saída do ADR4525."),
    ("U203", "TL431 a 3,6 V: sumidouro dos clamps; a V4.1 não tem nenhum."), ("R204", "Divisor do TL431."), ("R205", "Divisor do TL431."),
    ("U401", "LDO 3,3 V para o VCC1 do isolador: fecha G2."), ("C400", "Entrada do U401."), ("C402", "Saída do U401."),
    ("C500", "VREF no pino do ADC."), ("C501", "1 µF no VDD, pedido pelo datasheet."),
    ("C700", "100 nF no canal do NTC (fig. 4-2 do DS21298E)."),
    ("U601", "Limitador de corrente 23,75-26,25 mA no retorno (rev. 2.1): fecha a V8, herdada da V4.1."),
    ("U602", "Idem, canal 2."), ("U603", "Idem, canal 3."), ("U604", "Idem, canal 4."), ("U605", "Idem, canal 5."), ("U606", "Idem, canal 6."),
    ("D641", "Schottky antiparalelo ao U601: o AL5809 só aguenta −0,3 V em inversão."),
    ("D642", "Idem, canal 2."), ("D643", "Idem, canal 3."), ("D644", "Idem, canal 4."), ("D645", "Idem, canal 5."), ("D646", "Idem, canal 6."),
])
L.append("| V5 | Porquê |")
L.append("|---|---|")
novos = refs_ordenados(set(v5) - usados5)
tps = [r for r in novos if r.startswith("T")]; fid = [r for r in novos if r.startswith("FID")]
for r in novos:
    if r in tps or r in fid:
        continue
    L.append("| %s | %s |" % (agrupa(v5, [r]), NOVO_PQ.get(r, "**sem justificação nesta lista — conferir**")))
L.append("| %s | Pontos de prova: a V4.1 tem zero (RD1). |" % ", ".join("`%s`" % r for r in tps))
L.append("| %s | Fiduciais: a V4.1 tem zero (RD2). |" % ", ".join("`%s`" % r for r in fid))

L.append("\n## 4 · Contagem\n")
L.append("| | Peças |")
L.append("|---|---|")
L.append("| V4.1 | %d |" % len(v41))
L.append("| V5 | %d |" % len(v5))
L.append("| Continuam (§1) | %d na V4.1 → %d na V5, em %d linhas: %d iguais, %d mudam de peça, %d com MPN por fixar na V5 |"
         % (len(usados41), len(usados5), len(PARES), n_igual, n_muda, n_fixar))
sem = refs_ordenados(r for r in v5 if not tem_mpn(v5, r) and not r.startswith(("T", "FID")))
L.append("| Peças da V5 ainda sem MPN no esquemático | %d: %s |" % (len(sem), ", ".join(sem)))
L.append("| Saem (§2) | %d |" % (len(v41) - len(usados41)))
L.append("| Novas (§3) | %d |" % (len(v5) - len(usados5)))
L.append("\nEm aberto: os MPN em falta (fecham na BOM preliminar da F2; `R206` é a `V5` e `C200` a `V6`")
L.append("da intenção) e três saídas sem motivo individual escrito (`D17`, `F8`, `FB4`).")
io.open(sys.argv[3], "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
print("escrito", sys.argv[3], "| V4.1", len(v41), "| V5", len(v5), "| pares", len(usados41), "->", len(usados5),
      "| saem", len(v41) - len(usados41), "| novas", len(v5) - len(usados5))
sem = [r for r in novos if r not in tps and r not in fid and r not in NOVO_PQ]
print("novas sem justificacao:", sem or "nenhuma")
