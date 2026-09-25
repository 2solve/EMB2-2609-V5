# -*- coding: utf-8 -*-
"""Correccoes de TEXTO achadas na inspeccao ampliada da 2.5 (2026-09-25). Nenhuma ligacao muda.

- D200: a nota dizia grampo 58,1 V (e o SMA6J36A); o SMA6J33A grampeia a 53,3 V a 11,3 A (Bourns pag. 2,
  confirmado no texto e na imagem da tabela). Margens escritas corrigidas; as decisoes nao mudam.
- Folha 03: dissipacao do U200 a 32 V (a nota era a 24 V); nivel do TL431 3,52 V (rev. 2.5b).
- Folha 04: C402 2,2 uF (rev. 2.5). Folha 06: cabecalho e bloco de titulo citavam a rev. 2.4.
- Folha 07: impedancia do no do NTC de 0 a 70 C (B25/85 3435 K, NTCS0603E3103*LT, Vishay pag. 1), no lugar
  do valor a -40 C (fora do envelope RB1).
- Data do bloco de titulo 2026-09-23 -> 2026-09-25 nas 8 folhas (so metadados; a folha 01 continua congelada
  no desenho).
Uso: python aplica_textos_F2_25c.py PASTA_DO_PROJECTO   (backup .antes_textos25c de cada folha tocada)
Cada troca tem de aparecer exactamente uma vez; a netlist tem de sair identica (confere-se fora).
"""
import io, os, shutil, sys

P = sys.argv[1]
T = lambda s: '(text "%s"' % s
TROCAS = {
 "02_entrada.kicad_sch": [
  (T("   clamp 58,1 V @ 11,3 A - tabela de seleccao, linha VRWM=33."),
   T("   clamp 53,3 V @ 11,3 A (Bourns pag. 2, linha SMA6J33A; corrigido 2026-09-25).")),
  (T("   ATENCAO: a folha equivalente da EBM7 legacy cita 53,3 V:"),
   T("   A 1.a versao desta nota dizia 58,1 V: esse valor e o do SMA6J36A.")),
  (T("   esse valor e da linha VRWM=30. Para esta peca sao 58,1 V."),
   T("   A EBM7 Legacy (53,3 V) estava certa. As decisoes 4 e 5 nao mudam.")),
  (T("   o clamp de 58,1 V sobrariam 1,9 V. D201 = regulador, D202 = lacos."),
   T("   o clamp de 53,3 V sobrariam 6,7 V. D201 = regulador, D202 = lacos.")),
  (T("   da V4.1 (C12/C28) ficariam 8,1 V abaixo do clamp."),
   T("   da V4.1 (C12/C28) ficariam 3,3 V abaixo do clamp.")),
 ],
 "03_alimentacao.kicad_sch": [
  (T("   Carga real ~3,7 mA (ADC 0,55 + ISO lado 2 ~2 + ADR 0,95 + NTC 0,21)."),
   T("   Carga ~3,7 mA (ADC, ISO lado 2, ADR, NTC) + LED 1,4 mA + divisores: <= 7 mA.")),
  (T("   Dissipa (24-5) x 5 mA = 95 mW no HVSSOP com pad termico."),
   T("   A 32 V: (30,4 - 5) V x 7 mA = 0,18 W no HVSSOP, +12 C (66,7 C/W).")),
  (T("7. U203 TL431 a 3,6 V = SUMIDOURO dos clamps de campo."),
   T("7. U203 TL431 a 3,52 V (rev. 2.5b) = SUMIDOURO dos clamps de campo.")),
 ],
 "04_barreira.kicad_sch": [
  (T("   estavel com 1 uF ceramico a saida (pag. 1). Nao tem enable: EN1 e do isolador."),
   T("   estavel com >= 1 uF ceramico (pag. 1); C402 = 2,2 uF (rev. 2.5). Sem enable: EN1 e do isolador.")),
 ],
 "06_lacos.kicad_sch": [
  (T("DECISOES DESTA FOLHA (F2 - intencao_EBM2_V5.md rev. 2.4, sec. 9)"),
   T("DECISOES DESTA FOLHA (F2 - intencao_EBM2_V5.md rev. 2.5c, sec. 9 e 17)")),
  ('(comment 2 "Fonte de verdade: intencao rev. 2.4 ate ao 1.o ERC limpo; depois este ficheiro")',
   '(comment 2 "Fonte de verdade: intencao rev. 2.5c ate ao 1.o ERC limpo; depois este ficheiro")'),
 ],
 "07_ntc.kicad_sch": [
  (T("2. C700 e novo. O no tem 3,6 kohm a 25 C e 5,5 kohm a -40 C; a fig. 4-2 do DS21298E"),
   T("2. C700 e novo. O no tem 1,6-4,7 kohm de 70 a 0 C (B25/85 3435 K); a fig. 4-2 do DS21298E")),
  (T("   de contar. Constante de tempo 0,36 ms, irrelevante para uma temperatura."),
   T("   de contar. Constante de tempo 0,16-0,47 ms, irrelevante para uma temperatura.")),
  ('(property "Description" "NOVO: sem ele o canal sai da fig. 4-2 do DS21298E a 1 MHz (3,6-5,5 kohm de fonte)"',
   '(property "Description" "NOVO: sem ele o canal sai da fig. 4-2 do DS21298E a 1 MHz (1,6-4,7 kohm de fonte, 0-70 C)"'),
 ],
}
DATA = ('(date "2026-09-23")', '(date "2026-09-25")')
FOLHAS = ["01_conectores.kicad_sch", "02_entrada.kicad_sch", "03_alimentacao.kicad_sch", "04_barreira.kicad_sch",
          "05_adc.kicad_sch", "06_lacos.kicad_sch", "07_ntc.kicad_sch", "IC2S_Extension_Board-EBM2_V5.kicad_sch"]

novos = {}
for f in FOLHAS:
    t = io.open(os.path.join(P, f), encoding="utf-8", newline="").read()   # preserva CRLF (a raiz vem assim do KiCad)
    for a, b in TROCAS.get(f, []) + [DATA]:
        assert t.count(a) == 1, (f, a[:80], t.count(a))
        t = t.replace(a, b)
    novos[f] = t
for f, t in novos.items():                       # so escreve depois de todas as trocas passarem
    c = os.path.join(P, f)
    shutil.copy2(c, c + ".antes_textos25c")
    io.open(c, "w", encoding="utf-8", newline="").write(t)
print("escritas %d folhas; %d trocas de texto + data" % (len(novos), sum(len(v) for v in TROCAS.values())))
