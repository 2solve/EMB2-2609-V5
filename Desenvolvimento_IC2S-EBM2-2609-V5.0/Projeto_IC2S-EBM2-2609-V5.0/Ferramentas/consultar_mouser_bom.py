# -*- coding: utf-8 -*-
"""Consulta a Mouser Search API para os MPN da BOM da EBM2 V5 e guarda a resposta crua, com data e hora.

Baseado no consultar_mouser.py da EBM7 V2.3 (2026-09-16). As chamadas a rede fazem-se UMA vez; o documento
(gera_bom_prelim.py) refaz-se sem voltar a gastar quota. So se aceita a correspondencia EXACTA do
ManufacturerPartNumber; se nao houver, regista-se isso em vez de aceitar um parecido.

Chave: variavel de ambiente MOUSER_API_KEY, ou --chave FICHEIRO (fora do repositorio). Nunca se imprime.
So pesquisa: a API de pesquisa nao toca em carrinho nem em pedido («hardware nao compra»).
Uso: python consultar_mouser_bom.py NETLIST.net SAIDA.json [--chave FICHEIRO]
"""
import datetime, io, json, os, sys, time, urllib.error, urllib.parse, urllib.request
from netlist_diff import ler

NET, SAIDA = sys.argv[1], sys.argv[2]
chave = os.environ.get("MOUSER_API_KEY", "").strip()
if "--chave" in sys.argv:
    chave = io.open(sys.argv[sys.argv.index("--chave") + 1], encoding="utf-8").read().strip()
if not chave:
    sys.exit("Sem chave: definir MOUSER_API_KEY ou passar --chave FICHEIRO")
URL = "https://api.mouser.com/api/v1/search/keyword?apiKey=" + urllib.parse.quote(chave)


def pesquisar(mpn):
    corpo = json.dumps({"SearchByKeywordRequest": {"keyword": mpn, "records": 20}}).encode("utf-8")
    req = urllib.request.Request(URL, data=corpo, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode("utf-8"))


# Prova de uma chamada antes das restantes: uma chave invalida devolve o mesmo erro 41 vezes.
teste = pesquisar("TPS26613DDFR")
if teste.get("Errors"):
    sys.exit("Chave recusada pela Mouser: %s" % json.dumps(teste["Errors"], ensure_ascii=False)[:200])
c, _, _ = ler(NET)
mpns = sorted({(v.get("MPN") or "").strip() for v in c.values()} - {""})
resultado = {"_consulta": {"quando": datetime.datetime.now().isoformat(timespec="minutes"),
                           "fonte": "Mouser Search API /search/keyword", "netlist": os.path.basename(NET)}}
# --so-faltam: reaproveita o ficheiro anterior e so repete erros e aproximadas (limite da Mouser ~30/min)
if "--so-faltam" in sys.argv and os.path.exists(SAIDA):
    ant = json.load(io.open(SAIDA, encoding="utf-8"))
    resultado.update({k: v for k, v in ant.items() if k != "_consulta" and v.get("peca")})
    resultado["_consulta"]["quando"] = ant["_consulta"]["quando"] + " + reconsulta " + datetime.datetime.now().isoformat(timespec="minutes")
    mpns = [m for m in mpns if m not in resultado]
for i, mpn in enumerate(mpns, 1):
    e = {"mpn_pedido": mpn}
    try:
        d = pesquisar(mpn)
        if d.get("Errors"):
            e["erro"] = json.dumps(d["Errors"], ensure_ascii=False)[:300]
        else:
            partes = (d.get("SearchResults") or {}).get("Parts") or []
            norm = lambda s: str(s).strip().casefold()
            exacta = next((p for p in partes if norm(p.get("ManufacturerPartNumber", "")) == norm(mpn)), None)
            tipo = "exacta"
            if not exacta:   # a Panasonic publica ERA-8AEB111V com hifen: so o hifen pode diferir
                exacta = next((p for p in partes if norm(p.get("ManufacturerPartNumber", "")).replace("-", "") == norm(mpn).replace("-", "")), None)
                tipo = "exacta (sem hifen)"
            e["correspondencia"] = tipo if exacta else ("aproximada" if partes else "nenhuma")
            if exacta:
                e["peca"] = {k: exacta.get(k) for k in ("ManufacturerPartNumber", "Manufacturer", "MouserPartNumber",
                             "Description", "AvailabilityInStock", "Availability", "FactoryStock", "LeadTime",
                             "LifecycleStatus", "ROHSStatus", "ProductDetailUrl", "DataSheetUrl", "Min", "Mult",
                             "SuggestedReplacement")}
                e["peca"]["PriceBreaks"] = exacta.get("PriceBreaks") or []
            else:
                e["alternativas"] = [str(p.get("ManufacturerPartNumber")) for p in partes[:5]]
    except urllib.error.HTTPError as x:
        e["erro"] = "HTTP %s %s" % (x.code, x.reason)
    except Exception as x:                                   # noqa: BLE001
        e["erro"] = "%s: %s" % (type(x).__name__, x)
    resultado[mpn] = e
    print("  %2d/%d  %-34s %s" % (i, len(mpns), mpn, e.get("erro") or e.get("correspondencia")))
    time.sleep(2.2)          # Mouser: ~30 chamadas por minuto; acima disso devolve 403
io.open(SAIDA, "w", encoding="utf-8").write(json.dumps(resultado, ensure_ascii=False, indent=1))
print("gravado:", SAIDA)
