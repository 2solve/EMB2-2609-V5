# -*- coding: utf-8 -*-
"""Monta a copia do projecto EBM2 V5 na organizacao de pastas de Produtos (modelo: Axcel_Sensor / 00-TEMPLATE)
para o repositorio https://github.com/Javier2Solve/EMB2-2609-V5 (PUBLICO).

Codigo da placa: IC2S-EBM2-2609-V5.0 (padrao da EBM7: IC2S-EBM7-2608-V2.2). Decisoes do projectista (2026-09-25):
repositorio publico, SEM os datasheets dos fabricantes (so a lista com md5).
Fica de fora: backups .antes_*, netlists/ERC intermedios, .history, *.kicad_prl, o audio, e os ficheiros da V4.1
(Gerbers e renders de outro produto). Os ficheiros KiCad mantem o nome (renomear o projecto partiria as instancias).
Uso: python monta_repositorio.py DESTINO        (recusa se DESTINO ja tiver ficheiros alem de .git)
"""
import os, re, shutil, sys

R = r"C:\hw\hw-ebm2-v5"
D = os.path.join(R, "Documentos")
K = os.path.join(R, "KiCad_EBM2_V5")
DEST = sys.argv[1]
ID = "IC2S-EBM2-2609-V5.0"
BASE = os.path.join(DEST, "Desenvolvimento_" + ID)
FAB = os.path.join(BASE, "Arquivos_Fabricação_" + ID)
DOC = os.path.join(BASE, "Documentos_" + ID)
PRJ = os.path.join(BASE, "Projeto_" + ID)
P = {
    "gerbers": os.path.join(FAB, "00-Gerbers_" + ID), "bom": os.path.join(FAB, "01-BOM_List_" + ID),
    "pnp": os.path.join(FAB, "02-Pick-and-Place_" + ID), "stencil": os.path.join(FAB, "03-Stencil_" + ID),
    "espec": os.path.join(DOC, "00-Especificações_Técnicas_" + ID), "esq": os.path.join(DOC, "01-Esquemáticos_" + ID),
    "pinout": os.path.join(DOC, "02-Pinout_" + ID), "blocos": os.path.join(DOC, "03-Diagrama_Blocos_" + ID),
    "ref": os.path.join(PRJ, "Documentos_de_Referência-" + ID),
}
if os.path.exists(DEST) and [x for x in os.listdir(DEST) if x != ".git"]:
    sys.exit("ABORTA: %s nao esta vazio" % DEST)

FORA = re.compile(r"\.antes_|\.bak|__pycache__|\.history|\\datasheets(\\|$)|gerber_V41|V41_(top|bottom)|\.kicad_prl$|fp-info-cache", re.I)
copiados = []


def cp(src, dst_dir, nome=None):
    if FORA.search(src):
        return
    os.makedirs(dst_dir, exist_ok=True)
    dst = os.path.join(dst_dir, nome or os.path.basename(src))
    shutil.copy2(src, dst)
    copiados.append(dst)


def cp_arvore(src, dst):
    for raiz, dirs, fich in os.walk(src):
        dirs[:] = [d for d in dirs if not FORA.search(os.path.join(raiz, d))]
        for f in fich:
            s = os.path.join(raiz, f)
            if not FORA.search(s):
                cp(s, os.path.join(dst, os.path.relpath(raiz, src)))


for p in P.values():
    os.makedirs(p, exist_ok=True)

# --- fabrico: por enquanto só a BOM preliminar (Gerbers, PnP e stencil saem da F3)
for f in ("bom_preliminar_EBM2_V5.md", "bom_preliminar_EBM2_V5.csv", "bom_dados_mouser_2026-09-25.json",
          "bom_dados_mouser_alternativas_2026-09-25.json", "bom_dados_mouser_candidatos_C200_R206_2026-09-25.json"):
    cp(os.path.join(D, f), P["bom"])
# --- especificacoes tecnicas
for f in ("escopo_EBM2_V5.md", "escopo_EBM2_V5_gaps.md", "intencao_EBM2_V5.md", "intencao_EBM2_V5_rev1_historico.md",
          "planejamento_pcb_EBM2_V5.md", "plano_teste_EBM2_V5_esqueleto.md", "Relatorio_Ciclo_Vida_EBM2_V5_2026-09-24.md",
          "Relatorio_Componentes_V41_V5_2026-09-23.md", "Relatorio_Melhorias_Isolamento_V8_RE1_2026-09-23.md",
          "tabela_correspondencia_refs_EBM2_V5.md", "tabela_correspondencia_refs_EBM2_V5.csv",
          "Resumo_Reuniao_EBM2_V5_2026-09-25.html", "Roteiro_Audio_Reuniao_EBM2_V5_2026-09-25.txt"):
    cp(os.path.join(D, f), P["espec"])
cp_arvore(os.path.join(D, "F3"), os.path.join(P["espec"], "F3_Layout"))
for f in ("F3_contorno_top.png", "F3_contorno_bottom.png", "F3_placement_top.png"):
    cp(os.path.join(K, "output", f), os.path.join(P["espec"], "F3_Layout"))
cp_arvore(os.path.join(D, "portao1_aprovado_2026-09-25"), os.path.join(P["espec"], "Portao1_aprovado_2026-09-25"))
for v in ("revisao_F2", "verificacao_2_3", "verificacao_2_3b", "verificacao_2_3b_rev24", "verificacao_2_3b_rev25"):
    cp_arvore(os.path.join(D, v), os.path.join(P["espec"], "Verificacoes_F2", v))
# --- esquematicos, pinout, diagrama
cp_arvore(os.path.join(D, "revisao_F2_2.5"), P["esq"])
cp(os.path.join(D, "mapa_pinos_EBM2_V5.md"), P["pinout"])
cp(os.path.join(D, "diagrama_blocos_EBM2_V5.svg"), P["blocos"])
# --- projecto KiCad + ferramentas
for f in os.listdir(K):
    s = os.path.join(K, f)
    if os.path.isfile(s) and (f.endswith((".kicad_sch", ".kicad_pcb", ".kicad_pro")) or f in ("sym-lib-table", "fp-lib-table")):
        cp(s, PRJ)
cp_arvore(os.path.join(K, "symbols"), os.path.join(PRJ, "symbols"))
cp_arvore(os.path.join(K, "footprints"), os.path.join(PRJ, "footprints"))
cp_arvore(os.path.join(R, "ferramentas"), os.path.join(PRJ, "Ferramentas"))
# --- referencia: a lista dos datasheets (os PDF ficam fora: repositorio publico)
lista = open(os.path.join(D, "portao1_aprovado_2026-09-25", "datasheets", "LISTA.md"), encoding="utf-8").read()
open(os.path.join(P["ref"], "LISTA_datasheets.md"), "w", encoding="utf-8").write(
    lista.replace("# Datasheets do pacote do Portão 1",
                  "# Datasheets usados no projecto\n\nOs PDF dos fabricantes não se redistribuem neste repositório público. "
                  "Esta lista dá o nome e o md5 de cada ficheiro usado na verificação, para se obter a mesma revisão no "
                  "site do fabricante ou no distribuidor."))
# pastas ainda vazias: o git não guarda pastas vazias
for p in (P["gerbers"], P["pnp"], P["stencil"]):
    open(os.path.join(p, ".gitkeep"), "w").close()
print("ficheiros copiados:", len(copiados), "| destino:", BASE)
