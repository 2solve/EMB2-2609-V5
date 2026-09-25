# -*- coding: utf-8 -*-
"""F2 2.2b: acrescenta as pecas da intencao rev. 2 que faltam nas folhas 02 e 03.

  folha 02: T206 (+24V_ADC), T207 (+24V_REG), D203 + R207 14k7 (LED de +24V a GND_24V)
  folha 03: D204 + R208 2k2 (LED de +5V_ADC a GND_ADC)

As folhas 02 e 03 ja estao desenhadas e verificadas: aqui NAO se regeneram. Os itens
novos constroem-se com o Folha (mesmas regras de campo e de grelha) e enxertam-se
antes do fecho do ficheiro. O LED e a resistencia copiam o D630/R630 da folha 06
(mesma peca LG Q396-PS-35, mesma pegada 0603LED com pino 1 = catodo).
MPN dos passivos: os da V4.1 (R26 ERJ-3EKF1472V; R24 RC0603FR-072K2L).

Uso: python aplica_leds_tps_F2.py 02|03 [--aplicar]
"""
import io, os, re, shutil, sys
from construtor import Folha, blocos_lib_de_folha, bloco_lib_padrao, fim

P = r"C:\hw\hw-ebm2-v5\KiCad_EBM2_V5"
FICH = {"02": "02_entrada.kicad_sch", "03": "03_alimentacao.kicad_sch"}
UUID = {"02": "c2f29862-7f8d-4bfc-b53d-4b6e8f2da933"}
R, TP, LED = "Device:R", "Connector:TestPoint", "Device:LED"
UP, DOWN = "power:+24V", "power:GND"


def campos_rc(x, y):
    return dict(ref_pos=(x + 2.54, y - 1.27, 0, "left"), val_pos=(x + 2.54, y + 1.27, 0, "left"))


def tp(fo, ref, valor, x, y):
    fo.simbolo(TP, ref, valor, x, y, 0, pegada="EBM2_V5:TestPad_Via", mpn=None,
               ref_pos=(x, y - 7.62, 0, None), val_pos=(x, y - 5.08, 0, None))


def contexto(fo, pontos):
    """Pinos que JA existem na folha, so para a verificacao das ligacoes novas."""
    for i, (x, y) in enumerate(pontos):
        fo.portos.append(("existente%d" % i, x, y))


def folha02(fo):
    # T206 e T207 na ponta dos trilhos, a direita do porto e do PWR_FLAG que la estao.
    # A 151,13 o texto do ponto de prova fica fora do texto do porto (133,8-143,0 mm).
    for ref, val, y in (("T207", "TP_+24V_REG", 63.50), ("T206", "TP_+24V_ADC", 101.60)):
        contexto(fo, [(138.43, y), (138.43, y), (138.43, y)])     # fio que chega, porto, PWR_FLAG
        fo.fio((138.43, y), (151.13, y)); fo.juncao(138.43, y)
        tp(fo, ref, val, 151.13, y)
    # LED de entrada, com os seus proprios portos, no espaco livre a esquerda
    fo.porto("+24V", 33.02, 88.90, UP, base=220)
    fo.simbolo(R, "R207", "14k7", 33.02, 92.71, 0, pegada="EBM2_V5:0603R", mpn="ERJ-3EKF1472V",
               descr="LED de entrada, 1,5 mA (V4.1 R26)", **campos_rc(33.02, 92.71))
    fo.fio((33.02, 96.52), (33.02, 99.06))
    fo.rotulo("LED_24V", 33.02, 97.79)
    fo.simbolo(LED, "D203", "LG Q396-PS-35", 33.02, 102.87, 90, pegada="EBM2_V5:0603LED", mpn="LG Q396-PS-35",
               descr="Aceso = ha entrada de 24 V. Posicao fisica igual a V4.1 D25 (V11)", **campos_rc(33.02, 102.87))
    fo.porto("GND_24V", 33.02, 106.68, DOWN, base=220)


def folha03(fo):
    fo.porto("+5V_ADC", 25.40, 83.82, "power:+5V", base=320)
    fo.simbolo(R, "R208", "2k2", 25.40, 87.63, 0, pegada="EBM2_V5:0603R", mpn="RC0603FR-072K2L",
               descr="LED do +5V_ADC, 1,4 mA (V4.1 R24)", **campos_rc(25.40, 87.63))
    fo.fio((25.40, 91.44), (25.40, 93.98))
    fo.rotulo("LED_5V_ADC", 25.40, 92.71)
    fo.simbolo(LED, "D204", "LG Q396-PS-35", 25.40, 97.79, 90, pegada="EBM2_V5:0603LED", mpn="LG Q396-PS-35",
               descr="Aceso = F201 e regulador bem. Posicao fisica igual a V4.1 D18 (V11)", **campos_rc(25.40, 97.79))
    fo.porto("GND_ADC", 25.40, 101.60, DOWN, base=320)


def main():
    k = sys.argv[1]; aplicar = "--aplicar" in sys.argv
    alvo = os.path.join(P, FICH[k])
    t0 = io.open(alvo, encoding="utf-8").read()
    if "\r\n" in t0:
        sys.exit("ABORTA: o ficheiro tem CRLF; este enxerto escreve LF")
    if re.search(r'\(property "Reference" "(T206|T207|D203|R207|D204|R208)"', t0):
        sys.exit("ABORTA: a folha %s ja tem as pecas novas. Restaurar o .antes_leds antes de repetir." % k)
    fu = UUID.get(k) or re.search(r'\(path "/[^/]+/([^"]+)"', t0).group(1)
    libs = blocos_lib_de_folha(alvo)
    libs[LED] = bloco_lib_padrao("Device.kicad_sym", "LED", "Device")
    fo = Folha(alvo, fu, libs)
    (folha02 if k == "02" else folha03)(fo)
    erros = fo.verifica()
    if erros:
        print("verificacao das ligacoes novas:"); [print("   ", e) for e in erros]; sys.exit(1)

    # corpo novo: os itens que o Folha gerou, sem cabecalho nem lib_symbols
    inteiro = fo.texto_ficheiro([])
    a = inteiro.find("\n\t(lib_symbols"); b = fim(inteiro, a + 1)
    corpo = inteiro[b:inteiro.rindex("\n\t(embedded_fonts no)")]
    t = t0
    if '\t\t(symbol "Device:LED"' not in t:
        a = t.find("\n\t(lib_symbols"); b = fim(t, a + 1)
        fecho = t.rindex("\n\t)", a, b + 1)
        t = t[:fecho] + "\n" + libs[LED] + t[fecho:]
    # a folha 02 foi escrita a mao e fecha so com ")"; a 03 fecha com (embedded_fonts no)
    fecho = t.rfind("\n\t(embedded_fonts no)")
    if fecho < 0:
        fecho = t.rindex("\n)")
    t = t[:fecho] + corpo + t[fecho:]
    if k == "02":
        # notas 12,7 mm para a direita: o T207 e o T206 ocupam 144,8-157,5 mm
        t, n = re.subn(r'(\(text "[^"]*"\n\t\t\(exclude_from_sim no\)\n\t\t\(at )152\.4 ', r"\g<1>165.1 ", t)
        print("notas deslocadas:", n)
    novos = set(fo.guardas(t)) - set(fo.guardas(t0))
    if novos:
        print("GUARDAS NOVAS FALHADAS:"); [print("   ", e) for e in novos]; sys.exit(1)
    print("folha %s: %d simbolos novos, %d fios, %d juncoes, %d rotulos -> OK"
          % (k, len(fo.simbolos), len(fo.fios), len(fo.juncoes), len(fo.rotulos)))
    if aplicar:
        bak = alvo + ".antes_leds"
        if not os.path.exists(bak):
            shutil.copy2(alvo, bak)
        io.open(alvo, "w", encoding="utf-8", newline="").write(t)
        print("escrito:", FICH[k], "| backup:", os.path.basename(bak))


if __name__ == "__main__":
    main()
