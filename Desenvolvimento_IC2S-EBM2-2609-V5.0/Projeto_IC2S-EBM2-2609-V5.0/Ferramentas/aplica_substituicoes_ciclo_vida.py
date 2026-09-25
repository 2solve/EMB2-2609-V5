# -*- coding: utf-8 -*-
"""Substituicoes por ciclo de vida (2026-09-24), sem mudar pegada nem ligacao.

  LG Q396-PS-35      -> KG EELP41.22-PHRH-35-A8J8-20-R18  (obsoleto: DigiKey 2026-09-14 «Obsoleto», ultima
                        compra 2026-07-02; datasheet ams OSRAM v1.9 «Discontinued». Substituto = o da EBM7
                        V2.3, alteracoes_mouser 2026-09-15; KG EELP41.22 v1.4 2026-08-07: -40..105 C, IF min
                        0,5 mA, 0603, catodo marcado; DigiKey «Active», 186 041 em stock)
  GRM188R71E104KA01D -> GRM188R72A104KA35D                (DigiKey: «Obsolete and no longer manufactured»; o
                        GRM188R71H104KA93D tambem esta obsoleto; o KA35D e o substituto indicado pela DigiKey:
                        100 nF X7R 100 V 0603, -55..125 C, «Active», 862 866 em stock)
  BAT46W-E3-08       -> BAT46W-7-F                         (Vishay «Active» mas 0 em stock ate 2027-01-11;
                        Diodes DS30044 rev. 20: 100 V, VF max 0,25 V @0,1 mA e 0,45 V @10 mA, SOD123, banda
                        de catodo: os mesmos maximos do Vishay; DigiKey «Active», em stock)

Uso:  python aplica_substituicoes_ciclo_vida.py gerador     # so o gerador (ferramenta, nao o projecto)
      python aplica_substituicoes_ciclo_vida.py folhas      # folhas 02 e 03 (desenhadas a mao); exige KiCad fechado
"""
import io, os, shutil, subprocess, sys

RAIZ = r"C:\hw\hw-ebm2-v5"
LED_V, LED_MPN = "KG EELP41.22", "KG EELP41.22-PHRH-35-A8J8-20-R18"


def troca(p, pares, bak):
    if not os.path.exists(p + bak):
        shutil.copy2(p, p + bak)
    t = io.open(p, encoding="utf-8").read()
    for a, b, n in pares:
        assert t.count(a) == n, (os.path.basename(p), a[:70], t.count(a), n)
        t = t.replace(a, b)
    io.open(p, "w", encoding="utf-8", newline="").write(t)
    print("ok", os.path.basename(p))


def gerador():
    troca(os.path.join(RAIZ, "ferramentas", "gera_folhas_F2.py"), [
        ('mpn="GRM188R71E104KA01D"', 'mpn="GRM188R72A104KA35D"', 6),   # C401, C403, C500, C502, C60k (lacete, 6 pecas), C700 = 11 pecas
        ('mpn="BAT46W-E3-08"', 'mpn="BAT46W-7-F"', 1),
        ('100 V; VF max 0,25 V a 0,1 mA, 0,45 V a 10 mA (Vishay 86406)"',
         '100 V; VF max 0,25 V a 0,1 mA, 0,45 V a 10 mA (Diodes DS30044 rev. 20; alternativa Vishay BAT46W-E3-08)"', 1),
        ('fo.simbolo("Device:LED", "D630", "LG Q396-PS-35", 20.32, 176.53, 90, pegada="EBM2_V5:0603LED", mpn="LG Q396-PS-35",',
         'fo.simbolo("Device:LED", "D630", "%s", 20.32, 176.53, 90, pegada="EBM2_V5:0603LED", mpn="%s",' % (LED_V, LED_MPN), 1),
    ], ".antes_ciclo_vida")


def folhas():
    tit = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
                          os.path.join(RAIZ, "ferramentas", "janelas_kicad.ps1")], capture_output=True, text=True)
    if tit.returncode != 0:
        sys.exit("ABORTA: o projecto EBM2 V5 esta aberto no KiCad")
    for f in ("02_entrada.kicad_sch", "03_alimentacao.kicad_sch"):
        troca(os.path.join(RAIZ, "KiCad_EBM2_V5", f), [
            ('(property "Value" "LG Q396-PS-35"', '(property "Value" "%s"' % LED_V, 1),
            ('(property "MPN" "LG Q396-PS-35"', '(property "MPN" "%s"' % LED_MPN, 1),
        ], ".antes_ciclo_vida")


if __name__ == "__main__":
    {"gerador": gerador, "folhas": folhas}[sys.argv[1]]()
