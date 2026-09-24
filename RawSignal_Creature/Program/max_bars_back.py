# Regner ud, hvor mange bars en formel ser tilbage (Max Bars Back), ved de
# højeste parameterværdier. Resultatet skrives i filernes hoved.
#
# Kan det ikke regnes sikkert (ukendt funktion), stopper bygningen, så der
# aldrig skrives et gættet tal. Så skal funktionen tilføjes herunder.

import math
import re

from formel import ByggeFejl, tal_tekst, udskift

# Funktioner, der ser tilbage i historikken, og hvilke argumenter (tællet
# fra 0) der er en længde i bars. Den længste længde bestemmer, hvor mange
# bars funktionen skal bruge.
LAENGDE_ARGUMENTER = {
    "averagetruerange": [0], "avgtruerange": [0],
    "average": [1], "xaverage": [1], "standarddev": [1],
    "highest": [1], "lowest": [1], "rsi": [1],
    "macd": [1, 2],
    "dmiplus": [0], "dmiminus": [0], "adx": [0],
}
# Funktioner uden egen historik. Deres argumenter undersøges stadig.
# and/or/not står med, fordi "and (" ligner et funktionskald.
UDEN_HISTORIK = {"data", "maxlist", "minlist", "floor", "absvalue", "truerange",
                 "and", "or", "not"}
# Dagsværdier: første argument er antal DAGE tilbage, ikke bars. De styres
# ikke af Max Bars Back, men de første dage i dataene har ingen gyldig værdi.
DAGS_FUNKTIONER = {"opend", "highd", "lowd", "closed"}
# Regnefunktioner, som en længde må indeholde
REGNE = {"maxlist": max, "minlist": min, "floor": math.floor, "absvalue": abs}

FUNKTIONSKALD = re.compile(r"([A-Za-z_]\w*)\s*\(")


def _del_argumenter(tekst):
    """Deler 'a, f(b, c), d' ved de kommaer, der ikke står inde i en parentes."""
    dele, dybde, start = [], 0, 0
    for i, t in enumerate(tekst):
        if t == "(":
            dybde += 1
        elif t == ")":
            dybde -= 1
        elif t == "," and dybde == 0:
            dele.append(tekst[start:i])
            start = i + 1
    dele.append(tekst[start:])
    return dele


def _regn(udtryk):
    """Regner et taludtryk ud, fx '5 * 25'. None, hvis det ikke er et rent tal.
    Kun de fire regnearter og REGNE-funktionerne er tilladt."""
    try:
        v = eval(udtryk.lower(), {"__builtins__": {}}, REGNE)
    except Exception:
        return None
    return v if isinstance(v, (int, float)) else None


def _tilbage(tekst, fid, dage):
    """Hvor mange bars et stykke formel ser tilbage. Dage tilbage for
    dagsværdier samles i listen 'dage'."""
    stoerst = 0
    # Bar-henvisninger som High[1]
    for m in re.finditer(r"\[([^\[\]]+)\]", tekst):
        v = _regn(m.group(1))
        if v is None:
            raise ByggeFejl(f"Filter {fid}: kan ikke regne [{m.group(1)}] ud.")
        stoerst = max(stoerst, int(math.ceil(v)))

    # Funktionskald: navn( ... )
    i = 0
    while True:
        m = FUNKTIONSKALD.search(tekst, i)
        if not m:
            break
        navn = m.group(1).lower()
        # Find den tilhørende slutparentes
        dybde, j = 1, m.end()
        while dybde:
            dybde += {"(": 1, ")": -1}.get(tekst[j], 0)
            j += 1
        indhold = tekst[m.end():j - 1]
        args = _del_argumenter(indhold)
        inde = max(_tilbage(x, fid, dage) for x in args)

        if navn in LAENGDE_ARGUMENTER:
            laengder = []
            for nr in LAENGDE_ARGUMENTER[navn]:
                v = _regn(args[nr]) if nr < len(args) else None
                if v is None:
                    raise ByggeFejl(f"Filter {fid}: kan ikke regne længden i {m.group(1)}({indhold}) ud.")
                laengder.append(int(math.ceil(v)))
            # En funktion af en funktion skal bruge begges historik
            stoerst = max(stoerst, max(laengder) + inde)
        elif navn in UDEN_HISTORIK:
            stoerst = max(stoerst, inde)
        elif navn in DAGS_FUNKTIONER:
            v = _regn(args[0])
            if v is None:
                raise ByggeFejl(f"Filter {fid}: kan ikke regne antal dage i {m.group(1)}({indhold}) ud.")
            dage.append((m.group(1), int(math.ceil(v))))
            stoerst = max(stoerst, inde)
        else:
            raise ByggeFejl(f"Filter {fid}: Max Bars Back kender ikke funktionen {m.group(1)}. "
                            "Programmet skal udvides, før filteret kan bygges.")
        i = j
    return stoerst


def tekst(a):
    """Linjerne om Max Bars Back til filernes hoved."""
    hoejeste = {"Filter1_" + x["navn"]: tal_tekst(x["slut"]) for x in a["parametre"]}
    formel = udskift(a["formel"], hoejeste)
    dage = []
    bars = _tilbage(formel, a["id"], dage)

    if bars == 0:
        linjer = ["Formlen ser ikke tilbage i bars. Auto Detect er nok."]
    else:
        vaerdier = ", ".join(f"{k.replace('Filter1_', '')}={v}" for k, v in hoejeste.items())
        ved = f" ved {vaerdier}" if vaerdier else ""
        linjer = [f"Længste beregning er {bars} bars{ved}.",
                  f"Sæt Max Bars Back til mindst {bars}."]
    if dage:
        flest = max(d for _, d in dage)
        navne = ", ".join(sorted({n for n, _ in dage}))
        linjer += [f"Formlen bruger dagsværdier ({navne}) op til {flest} dag(e) tilbage.",
                   "De tælles i dage og styres ikke af Max Bars Back. De første",
                   f"{flest} handelsdag(e) i dataene har ingen gyldig dagsværdi."]
    return linjer
