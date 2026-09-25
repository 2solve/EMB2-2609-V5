# -*- coding: utf-8 -*-
"""F2 / 2.2b - desenhar as folhas 01, 04, 05, 06 e 07 e ligar a hierarquia na raiz.

Especificacao: intencao_EBM2_V5.md rev. 2, aprovada pelo projectista em 2026-09-23.
Sem argumentos: ENSAIO (constroi em memoria, verifica, nao escreve).
Com --aplicar: backup .antes_F2 de cada ficheiro tocado e escreve.
A verificacao da netlist corre depois, com verifica_F2.py.
"""
import io, os, re, shutil, subprocess, sys, uuid
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from construtor import (Folha, blocos_lib_de_folha, bloco_lib_padrao, nu, f, fim, RAIZ_UUID, PROJECTO)

P = r"C:\hw\hw-ebm2-v5\KiCad_EBM2_V5"
LEG = r"C:\hw\hw-ebm7-v2.2\Desenvolvimento_IC2S-EBM7-2608-V2.2\Projeto_IC2S-EBM7-2608-V2.2\KiCad_EBM7_V23_LEGACY_4-20"
APLICAR = "--aplicar" in sys.argv
# --so 06,raiz escolhe o que se escreve. A folha 01 esta CONGELADA desde 2026-09-23 19:04: o Javier
# arrumou-a a mao no KiCad (massas para baixo, rotulos junto do conector). So se regenera com --so 01.
SO = sys.argv[sys.argv.index("--so") + 1].split(",") if "--so" in sys.argv else ["04", "05", "06", "07", "raiz"]
UUID_FOLHA = {"01": "954355e8-dd7d-45e2-ac29-f7991216bbbd", "04": "833ea678-a46e-43c7-a2d9-3cb876c3643f",
              "05": "ea82ea26-3859-44df-990e-172417c66408", "06": "92de0a46-fdcc-4d6a-8efe-79265455fb08",
              "07": "d5ebff84-abd6-4f7d-8ee2-84b59953a0c9"}
FICH = {"01": "01_conectores.kicad_sch", "04": "04_barreira.kicad_sch", "05": "05_adc.kicad_sch",
        "06": "06_lacos.kicad_sch", "07": "07_ntc.kicad_sch"}

tit = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                      os.path.join(os.path.dirname(os.path.abspath(__file__)), "janelas_kicad.ps1")],
                     capture_output=True, text=True).stdout
if APLICAR and ("EBM2_V5" in tit or "EBM2 V5" in tit):
    sys.exit("ABORTA: o projecto EBM2 V5 esta aberto no KiCad")
for k, fic in FICH.items():
    if k in SO and "(symbol\n" in io.open(os.path.join(P, fic), encoding="utf-8").read():
        sys.exit("ABORTA: a folha %s ja tem simbolos. Restaurar o backup antes de repetir." % fic)


# ------------------------------------------------------------------ simbolo proprio do ISO7141
def bloco_iso7141():
    """Pinagem da figura da seccao 5, pag. 4, do SLLSE83F (ISO7141, nao ISO7131/ISO7140)."""
    def pino(tipo, num, nome, x, y, ang):
        return ('\t\t\t\t(pin %s line\n\t\t\t\t\t(at %s %s %d)\n\t\t\t\t\t(length 2.54)\n\t\t\t\t\t(name "%s"\n'
                '\t\t\t\t\t\t(effects\n\t\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t\t)\n'
                '\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t\t(number "%s"\n\t\t\t\t\t\t(effects\n\t\t\t\t\t\t\t(font\n'
                '\t\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t\t)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)'
                % (tipo, f(x), f(y), ang, nome, num))
    def pl(pts, tipo="default", w=0.254, fill="none"):
        xy = " ".join("(xy %s %s)" % (f(a), f(b)) for a, b in pts)
        return ('\t\t\t\t(polyline\n\t\t\t\t\t(pts\n\t\t\t\t\t\t%s\n\t\t\t\t\t)\n\t\t\t\t\t(stroke\n\t\t\t\t\t\t(width %s)\n'
                '\t\t\t\t\t\t(type %s)\n\t\t\t\t\t)\n\t\t\t\t\t(fill\n\t\t\t\t\t\t(type %s)\n\t\t\t\t\t)\n\t\t\t\t)'
                % (xy, f(w), tipo, fill))
    def pr(nome, val, x, y, hide):
        h = "\n\t\t\t\t(hide yes)" if hide else ""
        return ('\t\t\t(property "%s" "%s"\n\t\t\t\t(at %s %s 0)\n\t\t\t\t(show_name no)\n\t\t\t\t(do_not_autoplace no)%s\n'
                '\t\t\t\t(effects\n\t\t\t\t\t(font\n\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t)' % (nome, val, f(x), f(y), h))
    esq = [("power_in", "1", "VCC1", 8.89), ("input", "7", "EN1", 6.35), ("input", "3", "INA", 3.81),
           ("input", "4", "INB", 1.27), ("input", "5", "INC", -1.27), ("output", "6", "OUTD", -3.81),
           ("power_in", "2", "GND1", -6.35), ("power_in", "8", "GND1", -8.89)]
    dir_ = [("power_in", "16", "VCC2", 8.89), ("input", "10", "EN2", 6.35), ("output", "14", "OUTA", 3.81),
            ("output", "13", "OUTB", 1.27), ("output", "12", "OUTC", -1.27), ("input", "11", "IND", -3.81),
            ("power_in", "9", "GND2", -6.35), ("power_in", "15", "GND2", -8.89)]
    g = [('\t\t\t\t(rectangle\n\t\t\t\t\t(start -10.16 11.43)\n\t\t\t\t\t(end 10.16 -11.43)\n\t\t\t\t\t(stroke\n'
          '\t\t\t\t\t\t(width 0.254)\n\t\t\t\t\t\t(type default)\n\t\t\t\t\t)\n\t\t\t\t\t(fill\n\t\t\t\t\t\t(type background)\n'
          '\t\t\t\t\t)\n\t\t\t\t)'),
         pl([(0, 11.43), (0, -11.43)], tipo="dash")]
    for y, sentido in ((3.81, 1), (1.27, 1), (-1.27, 1), (-3.81, -1)):
        for x0 in (-3.81, 1.778):
            a, b = (x0, x0 + 2.032) if sentido == 1 else (x0 + 2.032, x0)
            g.append(pl([(a, y + 1.016), (a, y - 1.016), (b, y), (a, y + 1.016)], fill="outline"))
    pinos = [pino(t, n, nm, -12.70, y, 0) for t, n, nm, y in esq] + [pino(t, n, nm, 12.70, y, 180) for t, n, nm, y in dir_]
    return ('\t\t(symbol "EBM2_V5:ISO7141CCDBQR"\n\t\t\t(pin_names\n\t\t\t\t(offset 0.508)\n\t\t\t)\n\t\t\t(exclude_from_sim no)\n'
            '\t\t\t(in_bom yes)\n\t\t\t(on_board yes)\n\t\t\t(in_pos_files yes)\n\t\t\t(duplicate_pin_numbers_are_jumpers no)\n'
            + pr("Reference", "U", 0, 13.97, False) + "\n" + pr("Value", "ISO7141CCDBQR", 0, -13.97, False) + "\n"
            + pr("Footprint", "EBM2_V5:SSOP16-4.9x3.9mm", 0, 0, True) + "\n" + pr("Datasheet", "", 0, 0, True) + "\n"
            + pr("Description", "Isolador digital 4 canais, 3 para o lado 2 e 1 de volta. Pinagem: SLLSE83F sec. 5 pag. 4", 0, 0, True)
            + '\n\t\t\t(symbol "ISO7141CCDBQR_0_1"\n' + "\n".join(g) + '\n\t\t\t)\n'
            + '\t\t\t(symbol "ISO7141CCDBQR_1_1"\n' + "\n".join(pinos) + '\n\t\t\t)\n\t\t\t(embedded_fonts no)\n\t\t)')



# ------------------------------------------------------------------ simbolo proprio do AL5809
def bloco_al5809():
    """Regulador de corrente de dois terminais (Diodes DS36625 rev. 5, pag. 1-2: In = pino 1,
    Out = pino 2; a corrente entra em In). Horizontal: In a esquerda, Out a direita."""
    def pino(num, nome, x, ang):
        return ('\t\t\t\t(pin passive line\n\t\t\t\t\t(at %s 0 %d)\n\t\t\t\t\t(length 2.54)\n\t\t\t\t\t(name "%s"\n'
                '\t\t\t\t\t\t(effects\n\t\t\t\t\t\t\t(font\n\t\t\t\t\t\t\t\t(size 1.016 1.016)\n\t\t\t\t\t\t\t)\n'
                '\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t\t(number "%s"\n\t\t\t\t\t\t(effects\n\t\t\t\t\t\t\t(font\n'
                '\t\t\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t\t\t)\n\t\t\t\t\t\t)\n\t\t\t\t\t)\n\t\t\t\t)' % (f(x), ang, nome, num))
    def pr(nome, val, y, hide):
        h = "\n\t\t\t\t(hide yes)" if hide else ""
        return ('\t\t\t(property "%s" "%s"\n\t\t\t\t(at 0 %s 0)\n\t\t\t\t(show_name no)\n\t\t\t\t(do_not_autoplace no)%s\n'
                '\t\t\t\t(effects\n\t\t\t\t\t(font\n\t\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t)' % (nome, val, f(y), h))
    caixa = ('\t\t\t\t(rectangle\n\t\t\t\t\t(start -3.81 1.905)\n\t\t\t\t\t(end 3.81 -1.905)\n\t\t\t\t\t(stroke\n'
             '\t\t\t\t\t\t(width 0.254)\n\t\t\t\t\t\t(type default)\n\t\t\t\t\t)\n\t\t\t\t\t(fill\n\t\t\t\t\t\t(type background)\n'
             '\t\t\t\t\t)\n\t\t\t\t)')
    return ('\t\t(symbol "EBM2_V5:AL5809"\n\t\t\t(pin_names\n\t\t\t\t(offset 0.508)\n\t\t\t)\n\t\t\t(exclude_from_sim no)\n'
            '\t\t\t(in_bom yes)\n\t\t\t(on_board yes)\n\t\t\t(in_pos_files yes)\n\t\t\t(duplicate_pin_numbers_are_jumpers no)\n'
            + pr("Reference", "U", 3.81, False) + "\n" + pr("Value", "AL5809", -3.81, False) + "\n"
            + pr("Footprint", "EBM2_V5:PowerDI123_TypeB", 0, True) + "\n"
            + pr("Datasheet", "https://www.diodes.com/assets/Datasheets/AL5809.pdf", 0, True) + "\n"
            + pr("Description", "Regulador de corrente de dois terminais. In = 1, Out = 2 (DS36625 rev. 5, pag. 2)", 0, True)
            + '\n\t\t\t(symbol "AL5809_0_1"\n' + caixa + '\n\t\t\t)\n'
            + '\t\t\t(symbol "AL5809_1_1"\n' + pino("1", "In", -6.35, 0) + "\n" + pino("2", "Out", 6.35, 180)
            + '\n\t\t\t)\n\t\t\t(embedded_fonts no)\n\t\t)')


# ------------------------------------------------------------------ bibliotecas
LIBS = {}
LIBS.update(blocos_lib_de_folha(os.path.join(P, "02_entrada.kicad_sch")))
LIBS.update(blocos_lib_de_folha(os.path.join(P, "03_alimentacao.kicad_sch")))


def bloco_mcp1824():
    """Copia do simbolo do Legacy com o corpo alargado: no original o GND e o TAB estao
    em x = -1,27/+1,27 (fora da grelha de 2,54) e o nome TAB, vertical, cai em cima do
    VOUT (medido no PDF da folha 04). Pinos, numeros e tipos ficam iguais ao original."""
    s = blocos_lib_de_folha(os.path.join(LEG, "03_alimentacao.kicad_sch"))["EBM7_V23_proyecto2:MCP1824ST-3302E"]
    s = s.replace('"EBM7_V23_proyecto2:MCP1824ST-3302E"', '"EBM2_V5:MCP1824ST-3302E"')
    trocas = [("(start -7.62 2.54)", "(start -10.16 2.54)"), ("(end 7.62 -2.54)", "(end 10.16 -2.54)"),
              ("(at -10.16 0 0)", "(at -12.7 0 0)"), ("(at 10.16 0 180)", "(at 12.7 0 180)"),
              ("(at -1.27 -5.08 90)", "(at -2.54 -5.08 90)"), ("(at 1.27 -5.08 90)", "(at 2.54 -5.08 90)")]
    for x, y in trocas:
        assert s.count(x) == 1, x
        s = s.replace(x, y)
    return s


LIBS["EBM2_V5:MCP1824ST-3302E"] = bloco_mcp1824()
LIBS["EBM7_V23_proyecto3:BAV199"] = blocos_lib_de_folha(os.path.join(LEG, "06_lacos.kicad_sch"))["EBM7_V23_proyecto3:BAV199"]
for nome, fic, lib in (("Conn_01x20", "Connector_Generic.kicad_sym", "Connector_Generic"),
                       ("Conn_01x14", "Connector_Generic.kicad_sym", "Connector_Generic"),
                       ("MCP3208", "Analog_ADC.kicad_sym", "Analog_ADC"),
                       ("LED", "Device.kicad_sym", "Device"),
                       ("Thermistor_NTC", "Device.kicad_sym", "Device"),
                       ("Fiducial", "Mechanical.kicad_sym", "Mechanical")):
    LIBS["%s:%s" % (lib, nome)] = bloco_lib_padrao(fic, nome, lib)
# ISO7141: o simbolo da EBM7 V2.3 Legacy, copiado sem alteracoes (em grelha, pinagem conferida la
# contra o datasheet TI). O bloco_iso7141() proprio fica so como historico: nao se usa.
LIBS["EBM2_V5:AL5809"] = bloco_al5809()
LIBS["Device:D_Schottky"] = bloco_lib_padrao("Device.kicad_sym", "D_Schottky", "Device")
LIBS["EBM7_V23_proyecto4:ISO7141CC"] = blocos_lib_de_folha(os.path.join(LEG, "04_barreira.kicad_sch"))["EBM7_V23_proyecto4:ISO7141CC"]
# rev. 2.4: protector de laco e o seu LDO, os simbolos da folha 06 da Legacy, sem alteracoes
_L06 = blocos_lib_de_folha(os.path.join(LEG, "06_lacos.kicad_sch"))
for _n in ("EBM7_V23_proyecto7:TPS26613DDFR", "EBM7_V23_proyecto9:TPS7A4001DGN"):
    LIBS[_n] = _L06[_n]

UP, DOWN, FLAG = "power:+24V", "power:GND", "power:PWR_FLAG"
C = "Device:C"; R = "Device:R"; TP = "Connector:TestPoint"; FB = "Device:L_Ferrite"
TVS = "Device:D_Zener"; FUS = "Device:Fuse"


def campos_rc(x, y):
    return dict(ref_pos=(x + 2.54, y - 1.27, 0, "left"), val_pos=(x + 2.54, y + 1.27, 0, "left"))


def campos_h(x, y):            # resistencia/fusivel/ferrite horizontal: texto por cima e por baixo
    return dict(ref_pos=(x, y - 2.54, 0, None), val_pos=(x, y + 2.54, 0, None))


def tp(fo, ref, valor, x, y):
    fo.simbolo(TP, ref, valor, x, y, 0, pegada="EBM2_V5:TestPad_Via", mpn=None, bom=False,   # ilha/via: nao se compra
               ref_pos=(x, y - 7.62, 0, None), val_pos=(x, y - 5.08, 0, None))


# ================================================================== FOLHA 01
def folha01():
    fo = Folha(os.path.join(P, FICH["01"]), UUID_FOLHA["01"], LIBS)
    p1 = fo.simbolo("Connector_Generic:Conn_01x20", "P1", "M20-7822046", 40.64, 68.58, 0, espelho="y",
                    pegada="EBM2_V5:HDR1X20_FEMALE", mpn="M20-7822046",
                    descr="Conector para a base board. Pinagem congelada (RC2), igual a V4.1",
                    ref_pos=(40.64, 40.64, 0, None), val_pos=(40.64, 99.06, 0, None))
    NC_P1 = {1: "USB1", 2: "USB2", 7: "CS_DAC", 8: "LDAC_DAC", 10: "CS4", 11: "ID1 - manter desligado",
             13: "ID3 - manter desligado", 14: "SDA", 15: "SCL", 18: "nao existe na V4.1"}
    for n in range(1, 21):
        x, y = p1[str(n)]
        assert abs(x - 45.72) < 1e-6, "P1 espelhado devia ter os pinos em x=45,72: %s" % ((x, y),)
        if n in NC_P1:
            fo.no_connect((x, y))
            fo.texto(["%s (nao usado)" % NC_P1[n] if "ID" not in NC_P1[n] else NC_P1[n]], 48.26, y + 0.635)
        elif n in (4, 5, 6, 9):
            nome = {4: "MOSI", 5: "CLK", 6: "MISO", 9: "CS_ADC"}[n]
            fo.fio((x, y), (63.50, y)); fo.hier(nome, 63.50, y, 0, "passive", "left")
        elif n in (3, 12):
            fo.fio((x, y), (53.34, y))
            fo.porto("DGND", 53.34, y, DOWN, rot=90, val_pos=(59.69, y, 0, None), base=100)
        elif n == 16:          # DGND vem de um conector passivo: PWR_FLAG legitimo (AMBIENTE 9)
            fo.fio((x, y), (111.76, y), (111.76, 99.06), (111.76, 104.14)); fo.juncao(111.76, 99.06)
            fo.porto("DGND", 111.76, 104.14, DOWN, base=100)
            fo.porto("PWR_FLAG", 111.76, 99.06, FLAG, rot=270, val_pos=(120.65, 99.06, 0, None), prefixo="#FLG", base=100)
        elif n == 17:          # +5V do barramento: idem
            # porto a apontar para cima, no fim de um fio horizontal: correccao do Javier (autosave 17:04)
            fo.fio((x, y), (93.98, y), (93.98, 99.06), (93.98, 105.41), (97.79, 105.41)); fo.juncao(93.98, 99.06)
            fo.porto("+5V", 97.79, 105.41, UP, val_pos=(97.79, 101.60, 0, None), base=100)
            fo.porto("PWR_FLAG", 93.98, 99.06, FLAG, rot=270, val_pos=(102.87, 99.06, 0, None), prefixo="#FLG", base=100)
        elif n == 19:
            fo.fio((x, y), (78.74, y), (78.74, 99.06), (78.74, 104.14))
            fo.juncao(78.74, 99.06)
            fo.porto("GND_24V", 78.74, 104.14, DOWN, base=100)
            fo.porto("PWR_FLAG", 78.74, 99.06, FLAG, rot=270, val_pos=(87.63, 99.06, 0, None), prefixo="#FLG", base=100)
        elif n == 20:
            fo.fio((x, y), (63.50, y), (63.50, 99.06), (63.50, 105.41), (68.58, 105.41))
            fo.juncao(63.50, 99.06)
            fo.porto("+24V", 68.58, 105.41, UP, val_pos=(68.58, 101.60, 0, None), base=100)
            fo.porto("PWR_FLAG", 63.50, 99.06, FLAG, rot=270, val_pos=(71.12, 99.06, 0, None), prefixo="#FLG", base=100)
    p2 = fo.simbolo("Connector_Generic:Conn_01x14", "P2", "M20-7821446", 149.86, 60.96, 0, espelho="y",
                    pegada="EBM2_V5:HDR1X14_FEMALE", mpn="M20-7821446",
                    descr="Conector de campo, 6 lacos 4-20 mA. Pinagem congelada (RC2), igual a V4.1",
                    ref_pos=(149.86, 40.64, 0, None), val_pos=(149.86, 83.82, 0, None))
    for n in range(1, 15):
        x, y = p2[str(n)]
        if n == 1:
            fo.no_connect((x, y)); fo.texto(["nao ligado, como na V4.1"], 157.48, y + 0.635)
        elif n == 14:
            fo.fio((x, y), (162.56, y))
            fo.porto("GND_ADC", 162.56, y, DOWN, rot=90, val_pos=(170.18, y, 0, None), base=100)
        else:
            k = n // 2
            nome = ("LOOP%d_V+" % k) if n % 2 == 0 else ("AIN%d-" % k)
            fo.fio((x, y), (172.72, y)); fo.hier(nome, 172.72, y, 0, "passive", "left")
    for i, x in enumerate((200.66, 215.90, 231.14)):
        fo.simbolo("Mechanical:Fiducial", "FID%d" % (101 + i), "Fiducial", x, 50.80, 0,
                   pegada="EBM2_V5:Fiducial_Point_Top-Bot", mpn=None, bom=False,
                   ref_pos=(x, 45.72, 0, None), val_pos=(x, 55.88, 0, None))
    fo.texto([
        "DECISOES DESTA FOLHA (F2 2.2b - intencao_EBM2_V5.md rev.2, sec. 4)",
        "1. P1 e P2 com a pinagem da V4.1, pino a pino (RC2). Nada se renumera.",
        "2. Pinos do barramento que esta placa nao usa levam no-connect explicito.",
        "3. ID1 (P1.11) e ID3 (P1.13) ficam desligados: sao, muito provavelmente, a identidade",
        "   da placa perante a base board. Liga-los pode partir o RC4. Copia-se o original.",
        "4. +5V e o 5 V do BARRAMENTO (DGND). O de campo chama-se +5V_ADC. Um porto +5V",
        "   nas folhas de campo fundia os dois dominios e anulava a barreira sem erro nenhum.",
        "5. PWR_FLAG em +24V e GND_24V: o conector e uma fonte real e passiva.",
        "6. Fiduciais FID101-FID103 na face dos SMD (RD2).",
    ], 25.40, 124.46)
    return fo, ["Folha 2 de 8 - 1 Conectores - P1 barramento, P2 campo, fiduciais",
                "Fonte de verdade: intencao rev.2 ate ao 1.o ERC limpo; depois este ficheiro",
                "Pinagem de P1 e P2 congelada (RC2), copiada da V4.1 auditada."]


# ================================================================== FOLHA 04
def folha04():
    fo = Folha(os.path.join(P, FICH["04"]), UUID_FOLHA["04"], LIBS)
    u = fo.simbolo("EBM7_V23_proyecto4:ISO7141CC", "U400", "ISO7141CCDBQR", 139.70, 88.90, 0,
                   pegada="EBM2_V5:SSOP16-4.9x3.9mm", mpn="ISO7141CCDBQR",
                   descr="Isolador digital, unica barreira da placa. Pinagem SLLSE83F sec. 5 pag. 4",
                   ref_pos=(139.70, 74.93, 0, None), val_pos=(139.70, 102.87, 0, None))
    # lado 1: sinais do barramento
    for pin, nome in (("3", "MOSI"), ("4", "CLK"), ("5", "CS_ADC"), ("6", "MISO")):
        x, y = u[pin]; fo.fio((101.60, y), (x, y)); fo.hier(nome, 101.60, y, 180, "passive", "right")
    for pin, nome in (("14", "MOSI_ADC_ISO"), ("13", "CLK_ADC_ISO"), ("12", "CS_ADC_ISO"), ("11", "MISO_ADC_ISO")):
        x, y = u[pin]; fo.fio((x, y), (177.80, y)); fo.hier(nome, 177.80, y, 0, "passive", "left")
    # LDO do lado 1
    l = fo.simbolo("EBM2_V5:MCP1824ST-3302E", "U401", "MCP1824ST-3302E/DB", 86.36, 66.04, 0,
                   pegada="EBM2_V5:SOT-223-3", mpn="MCP1824ST-3302E/DB",
                   descr="LDO 3,3 V para VCC1/EN1 do isolador; fecha o G2. Pinos: DS22070A pag. 2 figura",
                   ref_pos=(86.36, 57.15, 0, None), val_pos=(86.36, 59.69, 0, None))
    vin, vout, gnd, tab = l["1"], l["3"], l["2"], l["4"]
    fo.fio((66.04, 66.04), (71.12, 66.04), vin); fo.juncao(71.12, 66.04)
    fo.porto("+5V", 66.04, 66.04, UP, base=400)
    fo.simbolo(C, "C400", "1uF", 71.12, 69.85, 0, pegada="EBM2_V5:0603C", mpn="C0603C105K4RACTU",
               descr="Entrada do MCP1824S", ref_pos=(68.58, 68.58, 0, "right"), val_pos=(68.58, 71.12, 0, "right"))
    fo.porto("DGND", 71.12, 73.66, DOWN, base=400)
    fo.fio(gnd, (86.36, 71.12), tab); fo.juncao(86.36, 71.12)
    fo.porto("DGND", 86.36, 71.12, DOWN, base=400)
    fo.fio(vout, (101.60, 66.04), (111.76, 66.04), (116.84, 66.04))
    for xj in (101.60, 111.76):
        fo.juncao(xj, 66.04)
    fo.porto("+3.3V_DIG", 116.84, 66.04, "power:+3V3", base=400)
    fo.simbolo(C, "C402", "2u2", 101.60, 69.85, 0, pegada="EBM2_V5:0603C", mpn="C1608X5R1E225K080AB",
               descr="Saida do MCP1824S. Rev. 2.5: 2,2 uF (1 uF era o minimo exacto do DS22070A sec. 4.3). MPN na BOM", **campos_rc(101.60, 69.85))
    fo.porto("DGND", 101.60, 73.66, DOWN, base=400)
    fo.simbolo(C, "C401", "100nF", 111.76, 69.85, 0, pegada="EBM2_V5:0603C", mpn="GRM188R72A104KA35D",
               descr="Desacoplamento do VCC1, no pino (V4.1 C7)", **campos_rc(111.76, 69.85))
    fo.porto("DGND", 111.76, 73.66, DOWN, base=400)
    # simbolo na ordem do encapsulamento: VCC1/GND1 em cima, EN1/GND1 em baixo; porto em cada pino
    for pin, val, lib, rot, dx in (("1", "+3.3V_DIG", "power:+3V3", 90, 8.89), ("2", "DGND", DOWN, 270, 6.35),
                                   ("7", "+3.3V_DIG", "power:+3V3", 90, 8.89), ("8", "DGND", DOWN, 270, 6.35)):
        x, y = u[pin]; fo.fio((x, y), (124.46, y))
        fo.porto(val, 124.46, y, lib, rot=rot, val_pos=(124.46 - dx, y, 0, None), base=400)
    tp(fo, "T400", "TP_DGND", 78.74, 101.60); fo.porto("DGND", 78.74, 101.60, DOWN, base=400)
    # lado 2
    fo.fio(u["16"], (157.48, 80.01))
    fo.fio((157.48, 80.01), (157.48, 66.04), (160.02, 66.04), (162.56, 66.04), (170.18, 66.04))
    fo.juncao(162.56, 66.04); fo.juncao(160.02, 66.04)
    x, y = u["10"]; fo.fio((x, y), (154.94, y)); fo.rotulo("VCC2_ISO", 154.94, y)      # EN2 ao VCC2
    fo.porto("PWR_FLAG", 160.02, 66.04, FLAG, prefixo="#FLG", base=400)   # VCC2 sai da ferrite FB400: fonte passiva
    fo.rotulo("VCC2_ISO", 157.48, 77.47, 90)
    fo.simbolo(C, "C403", "100nF", 162.56, 69.85, 0, pegada="EBM2_V5:0603C", mpn="GRM188R72A104KA35D",
               descr="Desacoplamento do VCC2, no pino (V4.1 C8)", **campos_rc(162.56, 69.85))
    fo.porto("GND_ADC", 162.56, 73.66, DOWN, base=400)
    fb = fo.simbolo(FB, "FB400", "BLM18PG471SN1D", 173.99, 66.04, 90, pegada="EBM2_V5:0603FB", mpn="BLM18PG471SN1D",
                    descr="Ferrite do VCC2 do isolador a partir de 3V3_REF (V4.1 FB2)",
                    ref_pos=(173.99, 60.96, 0, None), val_pos=(173.99, 63.50, 0, None))
    fo.fio(fb["2"], (187.96, 66.04))
    fo.porto("3V3_REF", 187.96, 66.04, "power:+3V3", base=400)
    for pin in ("15", "9"):
        x, y = u[pin]; fo.fio((x, y), (154.94, y))
        fo.porto("GND_ADC", 154.94, y, DOWN, rot=90, val_pos=(154.94 + 7.62, y, 0, None), base=400)
    fo.linha_tracejada((139.70, 35.56), (139.70, 71.12))
    fo.linha_tracejada((139.70, 106.68), (139.70, 157.48))
    fo.texto(["BARREIRA FUNCIONAL - so o U400 a atravessa"], 142.24, 40.64)
    fo.texto(["LADO DO BARRAMENTO - DGND"], 99.06, 45.72)
    fo.texto(["LADO DE CAMPO - GND_ADC"], 146.05, 45.72)
    fo.texto([
        "DECISOES DESTA FOLHA (F2 2.2b - intencao_EBM2_V5.md rev.2, sec. 7)",
        "1. U400 ISO7141CCDBQR: pinagem conferida na figura da sec. 5, pag. 4, do SLLSE83F.",
        "   A mesma pagina traz o ISO7131 e o ISO7140 com os pinos 5, 6, 11 e 12 trocados.",
        "   Simbolo da EBM7 V2.3 Legacy (EBM7_V23_proyecto4:ISO7141CC), copiado sem alteracoes.",
        "2. VCC1 a 3,3 V pelo U401, nao a 5 V: fecha o G2. A 5 V o OUTD punha ~4,9 V",
        "   no GPIO9 da Raspberry Pi, acima do maximo dela, sem resistencia serie.",
        "3. U401 MCP1824S SOT-223-3: pinos na figura da pag. 2 do DS22070A. Entrada 2,1-6,0 V;",
        "   estavel com >= 1 uF ceramico (pag. 1); C402 = 2,2 uF (rev. 2.5). Sem enable: EN1 e do isolador.",
        "4. VCC2 pela ferrite FB400 a partir de 3V3_REF, como na V4.1.",
        "5. T400 em DGND do lado do barramento: uma sonda do lado de campo com a placa",
        "   ligada atravessava a separacao pela massa do osciloscopio.",
    ], 25.40, 124.46)
    return fo, ["Folha 5 de 8 - 4 Barreira - ISO7141 e o LDO do lado do barramento",
                "Fonte de verdade: intencao rev.2 ate ao 1.o ERC limpo; depois este ficheiro",
                "Pinagem do U400 conferida na figura; confirmar na etapa 2.3 (sessao independente)."]


# ================================================================== FOLHA 05
def folha05():
    fo = Folha(os.path.join(P, FICH["05"]), UUID_FOLHA["05"], LIBS)
    u = fo.simbolo("Analog_ADC:MCP3208", "U500", "MCP3208T-BI/SL", 139.70, 91.44, 0,
                   pegada="EBM2_V5:SOIC16", mpn="MCP3208T-BI/SL",
                   descr="ADC 12 bits, grau B (INL +-1 LSB). Pinagem DS21298E pag. 1 figura",
                   ref_pos=(152.40, 106.68, 0, "left"), val_pos=(152.40, 109.22, 0, "left"))
    for pin, nome in (("1", "AIN1_ADC"), ("2", "AIN2_ADC"), ("3", "AIN3_ADC"), ("4", "AIN4_ADC"),
                      ("5", "NTC_ADC"), ("7", "AIN5_ADC"), ("8", "AIN6_ADC")):
        x, y = u[pin]; fo.fio((104.14, y), (x, y)); fo.hier(nome, 104.14, y, 180, "passive", "right")
    x, y = u["6"]; fo.fio((116.84, y), (x, y))
    fo.porto("3V3_REF", 116.84, y, "power:+3V3", rot=90, val_pos=(109.22, y, 0, None), base=500)
    for pin, nome in (("13", "CLK_ADC_ISO"), ("12", "MISO_ADC_ISO"), ("11", "MOSI_ADC_ISO"), ("10", "CS_ADC_ISO")):
        x, y = u[pin]; fo.fio((x, y), (175.26, y)); fo.hier(nome, 175.26, y, 0, "passive", "left")
    vr, vd = u["15"], u["16"]
    # rede de VREF/VDD 7,62 mm acima do U500: os textos GND_ADC dos C50x tocavam o topo do simbolo (render)
    fo.fio(vr, (vr[0], 63.50), (vr[0], 58.42)); fo.juncao(vr[0], 63.50)
    fo.porto("+2V5_REF", vr[0], 58.42, "power:+3V3", base=500)
    fo.fio((vr[0], 63.50), (119.38, 63.50))          # afastado do pino 1 do U500: o texto de massa caia em cima dele
    fo.simbolo(C, "C500", "100nF", 119.38, 67.31, 0, pegada="EBM2_V5:0603C", mpn="GRM188R72A104KA35D",
               descr="VREF no pino; o 1 uF da fig. 6-3 e o C207, a saida do ADR4525",
               ref_pos=(116.84, 66.04, 0, "right"), val_pos=(116.84, 68.58, 0, "right"))
    fo.porto("GND_ADC", 119.38, 71.12, DOWN, base=500)
    fo.fio(vd, (vd[0], 63.50), (vd[0], 58.42), (152.40, 58.42)); fo.juncao(vd[0], 63.50)
    fo.rotulo("VDD_ADC", vd[0], 62.23, 90)
    fb = fo.simbolo(FB, "FB500", "BLM18PG471SN1D", 156.21, 58.42, 90, pegada="EBM2_V5:0603FB", mpn="BLM18PG471SN1D",
                    descr="Ferrite do VDD do ADC a partir de 3V3_REF (V4.1 FB3)", **campos_h(156.21, 58.42))
    fo.fio(fb["2"], (165.10, 58.42))
    fo.porto("3V3_REF", 165.10, 58.42, "power:+3V3", base=500)
    fo.fio((vd[0], 63.50), (152.40, 63.50), (162.56, 63.50), (167.64, 63.50)); fo.juncao(152.40, 63.50); fo.juncao(162.56, 63.50)
    fo.porto("PWR_FLAG", 167.64, 63.50, FLAG, rot=270, val_pos=(176.53, 63.50, 0, None), prefixo="#FLG", base=500)
    fo.simbolo(C, "C501", "1uF", 152.40, 67.31, 0, pegada="EBM2_V5:0603C", mpn="C0603C105K4RACTU",
               descr="VDD: o DS21298E sec. 6.4 pag. 23 recomenda 1 uF no pino", **campos_rc(152.40, 67.31))
    fo.porto("GND_ADC", 152.40, 71.12, DOWN, base=500)
    fo.simbolo(C, "C502", "100nF", 162.56, 67.31, 0, pegada="EBM2_V5:0603C", mpn="GRM188R72A104KA35D",
               descr="VDD, alta frequencia (V4.1 C10)", **campos_rc(162.56, 67.31))
    fo.porto("GND_ADC", 162.56, 71.12, DOWN, base=500)
    ag, dg = u["14"], u["9"]
    fo.fio(ag, (ag[0], 109.22), (140.97, 109.22), (dg[0], 109.22), dg); fo.juncao(140.97, 109.22)
    fo.porto("GND_ADC", 140.97, 109.22, DOWN, base=500)
    tp(fo, "T500", "TP_GND_ADC", 185.42, 116.84); fo.porto("GND_ADC", 185.42, 116.84, DOWN, base=500)
    fo.texto([
        "DECISOES DESTA FOLHA (F2 2.2b - intencao_EBM2_V5.md rev.2, sec. 8)",
        "1. U500 MCP3208T-BI/SL: grau B, INL +-1 LSB (DS21298E pag. 37). Mesma pinagem que o -CI.",
        "2. MAPA DE CANAIS CONGELADO (RC4), igual a V4.1: CH0-CH3 campo 1-4, CH4 termistor,",
        "   CH5 preso a 3V3_REF (le sempre 4095), CH6-CH7 campo 5-6. Nao e sequencial.",
        "3. VREF = +2V5_REF (ADR4525), ja nao o VDD. C500 100 nF no pino.",
        "4. VDD pela ferrite FB500 com 1 uF + 100 nF no pino (sec. 6.4, pag. 23).",
        "5. AGND e DGND vao os dois a GND_ADC, com percursos proprios no layout.",
        "6. FIRMWARE: SPI <= 1 MHz (2 MHz so garantido a VDD 5 V). Transaccao de 24 bits",
        "   atomica: a 85 C a amostra so dura 1,2 ms (sec. 6.2). Cadencia <= 4 kHz por canal.",
    ], 25.40, 124.46)
    return fo, ["Folha 6 de 8 - 5 ADC - MCP3208 com referencia propria",
                "Fonte de verdade: intencao rev.2 ate ao 1.o ERC limpo; depois este ficheiro",
                "Mapa de canais nao sequencial, congelado por RC4."]


# ================================================================== FOLHA 06
def folha06():
    # rev. 2.4 (2026-09-24): protector TPS26613 por canal e o seu trilho +12V_TPS, copiados da
    # EBM7 V2.3 Legacy (U8-U11, U12). A folha passa a A3: o TPS26613 e mais alto que o AL5809.
    fo = Folha(os.path.join(P, FICH["06"]), UUID_FOLHA["06"], LIBS)
    fo.papel = "A3"
    CANAL_ADC = {1: "CH0", 2: "CH1", 3: "CH2", 4: "CH3", 5: "CH6", 6: "CH7"}
    for k in range(1, 7):
        col, lin = (k - 1) // 3, (k - 1) % 3
        cx = (20.32, 157.48)[col]
        yA = 45.72 + lin * 60.96
        yB = yA + 30.48                                   # rev. 2.4: espaco para o +Vs por cima do TPS26613
        # linha de alimentacao do laco
        fo.porto("+24V_ADC", cx, yA, UP, base=600)
        fo.fio((cx, yA), (cx + 8.89, yA))
        fz = fo.simbolo(FUS, "F60%d" % k, "50mA", cx + 12.70, yA, 90, pegada="EBM2_V5:1206F", mpn="3413.0002.22",
                        descr="Schurter USFF1206 50 mA, 9,2 ohm a frio (Legacy). Abre no curto do + a massa; o do transmissor e do U60x",
                        ref_pos=(cx + 12.70, yA - 2.54, 0, None), val_pos=(cx + 17.78, yA - 2.54, 0, "left"))
        assert fz["2"] == (round(cx + 16.51, 4), round(yA, 4)), fz["2"]
        # rev. 2.3: TVS do laco DEPOIS do fusivel, no terminal (EBM7 Legacy: D9/D10/D12/D13 em +24V_AINk).
        fo.fio(fz["2"], (cx + 19.05, yA), (cx + 22.86, yA)); fo.juncao(cx + 19.05, yA)
        d = fo.simbolo(TVS, "D61%d" % k, "824520361", cx + 19.05, yA + 3.81, 270, pegada="EBM2_V5:DO-214AA",
                       mpn="824520361", descr="TVS 36 V SMBJ36A 600 W no terminal LOOPk_V+, depois do fusivel (rev. 2.3, como a EBM7)",
                       ref_pos=(cx + 21.59, yA + 2.54, 0, "left"), val_pos=(cx + 21.59, yA + 5.08, 0, "left"))
        assert d["1"] == (round(cx + 19.05, 4), round(yA, 4)), "catodo do TVS no laco: %s" % (d["1"],)
        fo.porto("GND_ADC", cx + 19.05, yA + 7.62, DOWN, base=600)
        fo.hier("LOOP%d_V+" % k, cx + 22.86, yA, 0, "passive", "left")
        # linha de retorno e medida
        fo.hier("AIN%d-" % k, cx, yB, 180, "passive", "right")
        fo.fio((cx, yB), (cx + 7.62, yB), (cx + 11.43, yB)); fo.juncao(cx + 7.62, yB)
        fo.simbolo(TVS, "D60%d" % k, "SMBJ33A", cx + 7.62, yB + 3.81, 270, pegada="EBM2_V5:DO-214AA",
                   mpn="SMBJ33A-13-F", descr="TVS 33 V 600 W no retorno (rev. 2.4): standoff 33 V > 31,4 V do retorno em curto; grampo 53,3 V < 55 V do IN do TPS26613",
                   ref_pos=(cx + 5.08, yB + 2.54, 0, "right"), val_pos=(cx + 5.08, yB + 5.08, 0, "right"))
        fo.porto("GND_ADC", cx + 7.62, yB + 7.62, DOWN, base=600)
        # rev. 2.4: protector TPS26613 (Legacy U8-U11). IN no retorno, OUT para o burden.
        X = cx + 21.59
        u = fo.simbolo("EBM7_V23_proyecto7:TPS26613DDFR", "U60%d" % k, "TPS26613DDFR", X, yB, 0,
                       pegada="EBM2_V5:SOT-23-8", mpn="TPS26613DDFR",
                       descr="Protector de laco TI SLVSFE3C: limita 25-40 mA, 100 ms e novo arranque a 800 ms (MODE=GND); +-55 V. Legacy U8-U11",
                       ref_pos=(X + 11.43, yB + 3.81, 0, "left"), val_pos=(X + 11.43, yB + 6.35, 0, "left"))
        assert u["4"] == (round(cx + 11.43, 4), round(yB, 4)), u["4"]
        assert u["6"] == (round(X + 6.35, 4), round(yB - 12.7, 4)), u["6"]
        fo.porto("+12V_TPS", *u["6"], UP, base=600)
        # GND, MODE e -Vs a GND_ADC (unipolar, MODE = GND: sem o pulso de 2 x IOL)
        yb = yB + 15.24
        fo.fio(u["1"], (X - 6.35, yb), (X - 3.81, yb))
        fo.fio(u["3"], (X - 1.27, yb), (X - 3.81, yb))
        fo.fio(u["2"], (X - 3.81, yb), (X - 3.81, yb + 2.54)); fo.juncao(X - 3.81, yb)
        fo.porto("GND_ADC", X - 3.81, yb + 2.54, DOWN, base=600)
        fo.fio(u["7"], (X + 1.27, yb + 2.54)); fo.rotulo("VSNS", X + 1.27, yb + 2.54)
        fo.no_connect(u["8"])                               # SGOOD sem uso, como na Legacy (decisao na intencao)
        # desacoplamento do +Vs, um por CI (Legacy C26/C29/C31/C32)
        fo.porto("+12V_TPS", cx + 40.64, yB - 19.05, UP, base=600)
        fo.simbolo(C, "C61%d" % k, "100nF/100V", cx + 40.64, yB - 15.24, 0, pegada="EBM2_V5:0603C", mpn="GRM188R72A104KA35D",
                   descr="Desacoplamento do +Vs do U60%d, junto do pino 6 (SLVSFE3C sec. 11.1)" % k, **campos_rc(cx + 40.64, yB - 15.24))
        fo.porto("GND_ADC", cx + 40.64, yB - 11.43, DOWN, base=600)
        dx = 33.02
        rs = fo.simbolo(R, "R60%d" % k, "0R", cx + dx + 15.24, yB, 90, pegada="EBM2_V5:0603R", mpn="RC0603JR-070RL",
                        descr="Rev. 2.4: 0 ohm, a posicao do R10 da Legacy. O curto e limitado pelo U60x",
                        ref_pos=(cx + dx + 15.24, yB - 5.08, 0, None), val_pos=(cx + dx + 15.24, yB - 2.54, 0, None))
        assert rs["1"] == (round(cx + dx + 11.43, 4), round(yB, 4)), rs["1"]
        fo.fio(u["5"], rs["1"])
        fo.rotulo("AIN%d_LIM" % k, cx + 33.02, yB)
        fo.fio(rs["2"], (cx + dx + 25.40, yB), (cx + dx + 29.21, yB)); fo.juncao(cx + dx + 25.40, yB)
        fo.rotulo("AIN%d_MED" % k, cx + dx + 20.32, yB)          # no de medida: nunca nome gerado
        fo.simbolo(R, "R61%d" % k, "110R 0,1%", cx + dx + 25.40, yB + 3.81, 0, pegada="EBM2_V5:1206R", mpn="ERA8AEB111V",
                   descr="Burden 110 ohm 0,1 % 25 ppm/C (F1 sec. 2.5). 1206: 40 mA de pico no limite do U60x = 0,18 W",
                   ref_pos=(cx + dx + 27.94, yB + 2.54, 0, "left"), val_pos=(cx + dx + 27.94, yB + 5.08, 0, "left"))
        fo.porto("GND_ADC", cx + dx + 25.40, yB + 7.62, DOWN, base=600)
        ra = fo.simbolo(R, "R62%d" % k, "3k3", cx + dx + 33.02, yB, 90, pegada="EBM2_V5:0603R", mpn="RC0603FR-073K3L",
                        descr="Antialias; com o C a 482 Hz (RM3)",
                        ref_pos=(cx + dx + 33.02, yB - 5.08, 0, None), val_pos=(cx + dx + 33.02, yB - 2.54, 0, None))
        assert ra["1"] == (round(cx + dx + 29.21, 4), round(yB, 4)), ra["1"]
        cx += dx                                            # daqui para a frente o canal e o de antes, deslocado
        fo.fio(ra["2"], (cx + 43.18, yB), (cx + 60.96, yB), (cx + 64.77, yB))
        fo.juncao(cx + 43.18, yB); fo.juncao(cx + 60.96, yB)
        fo.rotulo("AIN%d_FILT" % k, cx + 44.45, yB)
        # rev. 2.5: serie ate ao pino do ADC. Em curto o BAV199 cai 0,67-0,72 V (fig. 2): limita a
        # corrente para o diodo interno do MCP3208 (0,6 V, fig. 4-1) a ~30 uA. Ver intencao sec. 17
        rsa = fo.simbolo(R, "R66%d" % k, "4k7", cx + 68.58, yB, 90, pegada="EBM2_V5:0603R", mpn="RC0603FR-074K7L",
                         descr="Serie do pino do ADC (rev. 2.5): (0,74 - 0,6) V / 4,7 kohm = 30 uA no diodo interno em curto; fuga tipica 2 nA = 9 uV",
                         ref_pos=(cx + 68.58, yB - 5.08, 0, None), val_pos=(cx + 68.58, yB - 2.54, 0, None))
        assert rsa["1"] == (round(cx + 64.77, 4), round(yB, 4)), rsa["1"]
        fo.fio(rsa["2"], (cx + 76.20, yB))
        fo.simbolo(C, "C60%d" % k, "100nF", cx + 43.18, yB + 3.81, 0, pegada="EBM2_V5:0603C", mpn="GRM188R72A104KA35D",
                   descr="Reservatorio de carga do ADC: tem de ficar encostado ao pino (F1 sec. 2.7d)",
                   ref_pos=(cx + 45.72, yB + 2.54, 0, "left"), val_pos=(cx + 45.72, yB + 5.08, 0, "left"))
        fo.porto("GND_ADC", cx + 43.18, yB + 7.62, DOWN, base=600)
        b = fo.simbolo("EBM7_V23_proyecto3:BAV199", "D62%d" % k, "BAV199", cx + 60.96, yB + 5.08, 180,
                       pegada="EBM2_V5:SOT23-3", mpn="BAV199LT1G",
                       descr="Clamp de baixa fuga: pino 3 no sinal, 1 a GND_ADC, 2 a 3V3_REF (BAV199LT1/D pag. 1)",
                       ref_pos=(cx + 60.96, yB - 5.08, 0, None), val_pos=(cx + 60.96, yB - 2.54, 0, None))
        assert b["3"] == (round(cx + 60.96, 4), round(yB, 4)), "o comum do BAV199 devia cair no sinal: %s" % (b["3"],)
        fo.porto("GND_ADC", *b["1"], DOWN, base=600)
        fo.porto("3V3_REF", *b["2"], "power:+3V3", rot=180, val_pos=(b["2"][0], b["2"][1] + 3.81, 0, None), base=600)
        fo.hier("AIN%d_ADC" % k, cx + 76.20, yB, 0, "passive", "left")
        fo.texto(["canal %d -> %s" % (k, CANAL_ADC[k])], cx + 76.20, yB - 3.81)
    # ---------------------------------------------------------- LED do trilho dos lacos
    yL = 243.84
    fo.porto("+24V_ADC", 20.32, yL - 7.62, UP, base=600)
    fo.simbolo(R, "R630", "14k7", 20.32, yL - 3.81, 0, pegada="EBM2_V5:0603R", mpn="ERJ-3EKF1472V",
               descr="LED do trilho dos lacos, 1,5 mA (V4.1 R25)", **campos_rc(20.32, yL - 3.81))
    fo.fio((20.32, yL), (20.32, yL + 2.54))
    fo.rotulo("LED_24V_ADC", 20.32, yL + 1.27)
    fo.simbolo("Device:LED", "D630", "KG EELP41.22", 20.32, yL + 6.35, 90, pegada="EBM2_V5:0603LED", mpn="KG EELP41.22-PHRH-35-A8J8-20-R18",
               descr="Aceso = F202 inteiro. Posicao fisica igual a V4.1 D19 (V11)", **campos_rc(20.32, yL + 6.35))
    fo.porto("GND_ADC", 20.32, yL + 10.16, DOWN, base=600)
    # ---------------------------------------------------------- rev. 2.4: trilho +12V_TPS (Legacy U12)
    bx = 45.72
    fo.porto("+24V_ADC", bx, yL, UP, base=600)
    fo.fio((bx, yL), (bx + 5.08, yL), (bx + 22.86, yL), (bx + 38.10, yL), (bx + 43.18, yL))
    fo.juncao(bx + 5.08, yL); fo.juncao(bx + 22.86, yL); fo.juncao(bx + 38.10, yL)
    fo.simbolo(C, "C641", "100nF/100V", bx + 5.08, yL + 3.81, 0, pegada="EBM2_V5:0603C", mpn="GRM188R72A104KA35D",
               descr="Entrada do U640, alta frequencia (Legacy C36)", **campos_rc(bx + 5.08, yL + 3.81))
    fo.porto("GND_ADC", bx + 5.08, yL + 7.62, DOWN, base=600)
    fo.simbolo(C, "C640", "10uF/100V", bx + 22.86, yL + 3.81, 0, pegada="EBM2_V5:C_1210_3225Metric", mpn="GRM32EC72A106ME05L",
               descr="Entrada do U640 >= 1 uF (SBVS162B sec. 8.2.2.2); Legacy C35. RA2: F202 fica a 11,6x a 32 V",
               **campos_rc(bx + 22.86, yL + 3.81))
    fo.porto("GND_ADC", bx + 22.86, yL + 7.62, DOWN, base=600)
    X2, Y2 = bx + 53.34, yL + 2.54
    g = fo.simbolo("EBM7_V23_proyecto9:TPS7A4001DGN", "U640", "TPS7A4001DGN", X2, Y2, 0, pegada="EBM2_V5:HVSSOP-8-1EP",
                   mpn="TPS7A4001DGNR",
                   descr="LDO do +12V_TPS, +Vs dos U601-U606 (Legacy U12). 12,09 V = 1,173 x (1 + 93,1/10). ~10,8 mA; 0,21 W a 32 V",
                   ref_pos=(X2, Y2 - 16.51, 0, None), val_pos=(X2, Y2 - 13.97, 0, None))
    assert g["8"] == (round(bx + 43.18, 4), round(yL, 4)), g["8"]
    assert g["4"] == g["9"], "PAD e GND no mesmo ponto"
    fo.fio(g["5"], (bx + 38.10, g["5"][1]), (bx + 38.10, yL))
    fo.porto("GND_ADC", *g["4"], DOWN, base=600)
    for n in ("3", "6", "7"):
        fo.no_connect(g[n])
    # saida, divisor de realimentacao, condensador de saida e ponto de prova
    xo = g["1"][0]
    assert g["1"] == (round(xo, 4), round(yL, 4)), g["1"]
    xr, xc, xc2, xt, xp, xs = 121.92, 137.16, 152.40, 165.10, 180.34, 190.50
    fo.fio(g["1"], (xr, yL), (xc, yL), (xc2, yL), (xt, yL), (xp, yL), (xs, yL))
    for x in (xr, xc, xc2, xt, xp):
        fo.juncao(x, yL)
    fo.simbolo(R, "R641", "93k1", xr, yL + 3.81, 0, pegada="EBM2_V5:0603R", mpn="RMCF0603FT93K1",
               descr="Realimentacao do U640, lado de cima (Legacy R25)", **campos_rc(xr, yL + 3.81))
    fo.fio(g["2"], (xo + 2.54, g["2"][1]), (xo + 2.54, yL + 7.62), (xr, yL + 7.62)); fo.juncao(xr, yL + 7.62)
    fo.rotulo("FB_U640", xo + 2.54, yL + 7.62)
    fo.simbolo(R, "R642", "10k", xr, yL + 11.43, 0, pegada="EBM2_V5:0603R", mpn="RC0603FR-0710KL",
               descr="Realimentacao do U640, lado de baixo (Legacy R26); corrente do divisor 117 uA >= 10 uA", **campos_rc(xr, yL + 11.43))
    fo.porto("GND_ADC", xr, yL + 15.24, DOWN, base=600)
    fo.simbolo(C, "C642", "10uF/50V", xc, yL + 3.81, 0, pegada="EBM2_V5:C_1206_3216Metric", mpn="C3216X5R1H106K160AB",
               descr="Saida do U640: > 4,7 uF efectivos a 12 V sobre temperatura e tolerancia (SBVS162B p.1); Legacy C38",
               **campos_rc(xc, yL + 3.81))
    fo.porto("GND_ADC", xc, yL + 7.62, DOWN, base=600)
    # rev. 2.5: a curva TDK da 5,8 uF a 12,6 V; com -10 % e -15 % (X5R) uma peca fica em 4,4 uF < 4,7 uF
    fo.simbolo(C, "C644", "10uF/50V", xc2, yL + 3.81, 0, pegada="EBM2_V5:C_1206_3216Metric", mpn="C3216X5R1H106K160AB",
               descr="Rev. 2.5: segunda saida do U640, em paralelo com C642. Duas pecas: 8,9 uF no pior caso (curva TDK, X5R -15 %, -10 %)",
               **campos_rc(xc2, yL + 3.81))
    fo.porto("GND_ADC", xc2, yL + 7.62, DOWN, base=600)
    # rev. 2.5: C_BYP entre OUT e FB (SBVS162B nota 4 pag. 5, sec. 8.2.2.3)
    fo.porto("+12V_TPS", xt, yL + 13.97, UP, base=600)
    fo.simbolo(C, "C645", "10nF", xt, yL + 17.78, 0, pegada="EBM2_V5:0603C", mpn="GCM188R71H103KA37J",
               descr="C_BYP do U640 (OUT-FB), recomendado pela TI sec. 8.2.2.3. Zero a 171 Hz com 93k1. MPN na BOM",
               **campos_rc(xt, yL + 17.78))
    fo.fio((xt, yL + 21.59), (xt, yL + 24.13)); fo.rotulo("FB_U640", xt, yL + 24.13)
    tp(fo, "T640", "TP_+12V_TPS", xt, yL)
    fo.porto("+12V_TPS", xp, yL, UP, base=600)
    # divisor do VSNS (tabela 8-2 do SLVSFE3C): desce a 5,0 V, sobe a 8,6 V
    fo.simbolo(R, "R643", "13k3", xs, yL + 3.81, 0, pegada="EBM2_V5:0603R", mpn="RC0603FR-0713K3L",
               descr="VSNS, lado de cima. Rev. 2.4: 13k3 em vez dos 11k5 da Legacy (R22): limiar de 5,0 V acima dos 4,4 V do burden a 40 mA",
               **campos_rc(xs, yL + 3.81))
    yv = yL + 7.62
    fo.fio((xs, yv), (xs + 12.70, yv), (xs + 25.40, yv), (xs + 33.02, yv))
    fo.juncao(xs, yv); fo.juncao(xs + 12.70, yv); fo.juncao(xs + 25.40, yv)
    fo.rotulo("VSNS", xs + 33.02, yv)
    for ref, x in (("R644", xs), ("R645", xs + 12.70)):
        fo.simbolo(R, ref, "6k65", x, yv + 3.81, 0, pegada="EBM2_V5:0603R", mpn="RC0603FR-076K65L",
                   descr="VSNS, lado de baixo: 6k65 || 6k65 = 3k325, como a Legacy (R23, R24)", **campos_rc(x, yv + 3.81))
        fo.porto("GND_ADC", x, yv + 7.62, DOWN, base=600)
    fo.simbolo(C, "C643", "100nF/100V", xs + 25.40, yv + 3.81, 0, pegada="EBM2_V5:0603C", mpn="GRM188R72A104KA35D",
               descr="Filtro do VSNS (Legacy C37)", **campos_rc(xs + 25.40, yv + 3.81))
    fo.porto("GND_ADC", xs + 25.40, yv + 7.62, DOWN, base=600)
    fo.texto([
        "DECISOES DESTA FOLHA (F2 - intencao_EBM2_V5.md rev. 2.5c, sec. 9 e 17)",
        "1. Topologia da V4.1. Mudam: burden 160 -> 110 ohm 0,1 %, clamp BAT54S -> BAV199, fusivel 50 mA 1206 (Legacy).",
        "2. TVS: D61x 36 V no terminal apos o fusivel (rev. 2.3); D60x 33 V no retorno (rev. 2.4: grampo 53,3 V < 55 V).",
        "3. Rev. 2.4: protector TPS26613 no retorno, copiado da EBM7 V2.3 Legacy (U8-U11). MODE=GND: 25-40 mA durante",
        "   100 ms, corta e tenta de novo a cada 800 ms. Em curto a leitura alterna 4095 e ~0 mA. SGOOD sem uso.",
        "4. +12V_TPS pelo U640 (Legacy U12). VSNS 13k3/3k325: limiar 5,0 V (a Legacy tem 11k5, 4,46 V: 1,4 % de margem).",
        "5. Prova: 20 mA x 110 ohm = 2,200 V; saturacao a 22,7 mA. A 18 V sobram >= 14,76 V ao transmissor.",
        "6. Rev. 2.5: R66x 4k7 no pino do ADC (30 uA em curto); C644 e C645 no U640.",
    ], 60.96, 15.24)
    return fo, ["Folha 7 de 8 - 6 Lacos - seis entradas 4-20 mA",
                "Fonte de verdade: intencao rev. 2.5c ate ao 1.o ERC limpo; depois este ficheiro",
                "Rev. 2.5: serie do ADC, segundo C de saida e C_BYP do U640."]


# ================================================================== FOLHA 07
def folha07():
    fo = Folha(os.path.join(P, FICH["07"]), UUID_FOLHA["07"], LIBS)
    fo.porto("+2V5_REF", 50.80, 50.80, "power:+3V3", base=700)
    # simbolo de termistor NTC (a V4.1 e a Legacy desenhavam-no como resistencia fixa: Javier
    # apontou-o em 2026-09-23). Designador R700 mantido: esquema da intencao rev. 2 e V4.1 R5.
    fo.simbolo("Device:Thermistor_NTC", "R700", "10k NTC", 50.80, 54.61, 0, pegada="EBM2_V5:0603R", mpn="NTCS0603E3103JLT",
               descr="Termistor da placa 10 kohm, B 3936 K (V4.1 R5). Topo em +2V5_REF: ratiometrico",
               **campos_rc(50.80, 54.61))
    fo.fio((50.80, 58.42), (50.80, 60.96), (60.96, 60.96), (71.12, 60.96))
    fo.juncao(50.80, 60.96); fo.juncao(60.96, 60.96)
    fo.simbolo(R, "R701", "5k62 0,1%", 50.80, 64.77, 0, pegada="EBM2_V5:0603R", mpn="ERA3AEB5621V",
               descr="Divisor do termistor (V4.1 R8)",
               ref_pos=(48.26, 63.50, 0, "right"), val_pos=(48.26, 66.04, 0, "right"))
    fo.porto("GND_ADC", 50.80, 68.58, DOWN, base=700)
    fo.simbolo(C, "C700", "100nF", 60.96, 64.77, 0, pegada="EBM2_V5:0603C", mpn="GRM188R72A104KA35D",
               descr="NOVO: sem ele o canal sai da fig. 4-2 do DS21298E a 1 MHz (1,6-4,7 kohm de fonte, 0-70 C)",
               **campos_rc(60.96, 64.77))
    fo.porto("GND_ADC", 60.96, 68.58, DOWN, base=700)
    fo.hier("NTC_ADC", 71.12, 60.96, 0, "passive", "left")
    fo.texto([
        "DECISOES DESTA FOLHA (F2 2.2b - intencao_EBM2_V5.md rev.2, sec. 10)",
        "1. Topo do divisor em +2V5_REF e nao em 3V3_REF: pendurado em 3,3 V o canal saturava",
        "   a 70 C com a referencia nova. Assim fica ratiometrico e o codigo e o da V4.1:",
        "   4096 x ratio nos dois casos. A tabela de temperatura do firmware nao muda.",
        "2. C700 e novo. O no tem 1,6-4,7 kohm de 70 a 0 C (B25/85 3435 K); a fig. 4-2 do DS21298E",
        "   so garante 1 MHz ate ~1,5 kohm. Com 100 nF no pino a resistencia de fonte deixa",
        "   de contar. Constante de tempo 0,16-0,47 ms, irrelevante para uma temperatura.",
    ], 25.40, 88.90)
    return fo, ["Folha 8 de 8 - 7 NTC - termistor da placa",
                "Fonte de verdade: intencao rev.2 ate ao 1.o ERC limpo; depois este ficheiro",
                "C700 novo: condensador no pino, justificado pela fig. 4-2 do DS21298E."]


# ================================================================== RAIZ
def raiz():
    f0 = os.path.join(P, "IC2S_Extension_Board-EBM2_V5.kicad_sch")
    t = io.open(f0, encoding="utf-8").read()
    SPI = ["MOSI", "CLK", "CS_ADC", "MISO"]
    SPI_ISO = ["MOSI_ADC_ISO", "CLK_ADC_ISO", "CS_ADC_ISO", "MISO_ADC_ISO"]
    LACO = [n for k in range(1, 7) for n in ("LOOP%d_V+" % k, "AIN%d-" % k)]
    ADC = ["AIN%d_ADC" % k for k in range(1, 7)]
    ySPI = [35.56 + 2.54 * i for i in range(4)]
    yLACO = [60.96 + 2.54 * i for i in range(12)]
    yADC = [63.50 + 2.54 * i for i in range(6)]
    yNTC = 106.68
    GEO = {  # ficheiro: (x, y, w, h, pinos [(nome, lado, y)])
        "01_conectores.kicad_sch": (20.32, 30.48, 38.10, 63.50,
                                    [(n, "d", y) for n, y in zip(SPI, ySPI)] + [(n, "d", y) for n, y in zip(LACO, yLACO)]),
        "04_barreira.kicad_sch": (88.90, 30.48, 38.10, 17.78,
                                  [(n, "e", y) for n, y in zip(SPI, ySPI)] + [(n, "d", y) for n, y in zip(SPI_ISO, ySPI)]),
        "06_lacos.kicad_sch": (88.90, 55.88, 38.10, 38.10,
                               [(n, "e", y) for n, y in zip(LACO, yLACO)] + [(n, "d", y) for n, y in zip(ADC, yADC)]),
        "07_ntc.kicad_sch": (88.90, 101.60, 38.10, 10.16, [("NTC_ADC", "d", yNTC)]),
        "05_adc.kicad_sch": (157.48, 30.48, 38.10, 81.28,
                             [(n, "e", y) for n, y in zip(SPI_ISO, ySPI)] + [(n, "e", y) for n, y in zip(ADC, yADC)]
                             + [("NTC_ADC", "e", yNTC)]),
        "02_entrada.kicad_sch": (218.44, 30.48, 38.10, 25.40, []),
        "03_alimentacao.kicad_sch": (218.44, 68.58, 38.10, 25.40, []),
    }
    pos_pinos = {}
    blocos = []
    k = 0
    while True:
        k = t.find("\n\t(sheet\n", k)
        if k < 0: break
        a = k + 1; b = fim(t, a); blocos.append((a, b)); k = a
    for a, b in reversed(blocos):
        blk = t[a:b]
        fic = re.search(r'"Sheetfile" "([^"]+)"', blk).group(1)
        x, y, w, h, pinos = GEO[fic]
        blk = re.sub(r"\n\t\t\(at [-\d.]+ [-\d.]+\)", "\n\t\t(at %s %s)" % (f(x), f(y)), blk, count=1)
        blk = re.sub(r"\n\t\t\(size [-\d.]+ [-\d.]+\)", "\n\t\t(size %s %s)" % (f(w), f(h)), blk, count=1)
        blk = re.sub(r'(\(property "Sheetname" "[^"]*"\n\t\t\t\(at )[-\d.]+ [-\d.]+( 0\))', r"\g<1>%s %s\2" % (f(x), f(y - 0.7116)), blk)
        blk = re.sub(r'(\(property "Sheetfile" "[^"]*"\n\t\t\t\(at )[-\d.]+ [-\d.]+( 0\))', r"\g<1>%s %s\2" % (f(x), f(y + h + 0.5846)), blk)
        pts = []
        for nome, lado, yp in pinos:
            xp = x if lado == "e" else x + w
            ang, just = (180, "left") if lado == "e" else (0, "right")
            pts.append('\t\t(pin "%s" passive\n\t\t\t(at %s %s %d)\n\t\t\t(uuid "%s")\n\t\t\t(effects\n\t\t\t\t(font\n'
                       '\t\t\t\t\t(size 1.27 1.27)\n\t\t\t\t)\n\t\t\t\t(justify %s)\n\t\t\t)\n\t\t)' % (nome, f(xp), f(yp), ang, nu(), just))
            pos_pinos.setdefault(nome, []).append((xp, yp))
        if pts:
            i = blk.find("\n\t\t(instances")
            blk = blk[:i] + "\n" + "\n".join(pts) + blk[i:]
        t = t[:a] + blk + t[b:]
    fios = []
    for nome, ps in pos_pinos.items():
        assert len(ps) == 2, "pino de folha %s aparece %d vezes" % (nome, len(ps))
        (x1, y1), (x2, y2) = sorted(ps)
        assert abs(y1 - y2) < 1e-6, "pinos de %s nao estao alinhados: %s" % (nome, ps)
        fios.append('\t(wire\n\t\t(pts\n\t\t\t(xy %s %s) (xy %s %s)\n\t\t)\n\t\t(stroke\n\t\t\t(width 0)\n\t\t\t(type default)\n'
                    '\t\t)\n\t\t(uuid "%s")\n\t)' % (f(x1), f(y1), f(x2), f(y2), nu()))
    i = t.find("\n\t(sheet\n")
    t = t[:i] + "\n" + "\n".join(fios) + t[i:]
    return t, len(fios)


# ================================================================== execucao
saida = {}
falhou = False
for chave, fn in (("01", folha01), ("04", folha04), ("05", folha05), ("06", folha06), ("07", folha07)):
    if chave not in SO:
        continue
    fo, com = fn()
    erros = fo.verifica()
    texto = fo.texto_ficheiro(com)
    erros += fo.guardas(texto)
    n_simb = sum(1 for k in fo.pinos_simbolo if not k.startswith("#"))
    print("folha %s: %d componentes, %d portos, %d fios, %d juncoes, %d no-connect, %d rotulos -> %s"
          % (chave, n_simb, len(fo.portos), len(fo.fios), len(fo.juncoes), len(fo.nc), len(fo.rotulos),
             "OK" if not erros else "%d ERROS" % len(erros)))
    for e in erros[:25]:
        print("     ", e)
    falhou |= bool(erros)
    saida[FICH[chave]] = texto
if "raiz" in SO:
    t_raiz, n_fios = raiz()
    print("raiz: %d fios hierarquicos" % n_fios)
if falhou:
    sys.exit("ENSAIO COM ERROS: nada escrito.")
if not APLICAR:
    print("ENSAIO limpo. Nada escrito. Correr com --aplicar.")
    sys.exit(0)
for fic, texto in list(saida.items()) + ([("IC2S_Extension_Board-EBM2_V5.kicad_sch", t_raiz)] if "raiz" in SO else []):
    cam = os.path.join(P, fic)
    shutil.copy2(cam, cam + ".antes_F2")
    io.open(cam, "w", encoding="utf-8", newline="").write(texto)
    print("escrito:", fic)
