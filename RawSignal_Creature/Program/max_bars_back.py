# Tjekker, om Max Bars Back er høj nok til en formel, og skriver det i
# filernes hoved.
#
# Max Bars Back står på STANDARD (1000) i TradeStation (besluttet 24-09-2026).
# Programmet regner ud, hvor mange bars formlen ser tilbage ved de højeste
# parameterværdier:
#   - højst STANDARD:            filen bygges, og behovet skrives i hovedet
#   - over STANDARD:             bygningen stopper - strategien ville fejle
#   - kan ikke regnes helt ud:   filen bygges, og hovedet siger, hvad der ikke
#                                kunne regnes ud, og at STANDARD antages nok
#                                (fx en funktion, programmet ikke kender endnu)

import math
import re

from formel import ByggeFejl, tal_tekst, udskift

# Max Bars Back som Thomas har sat den i TradeStation
STANDARD = 1000

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
# Dags- og sessionsværdier tæller i dage/sessioner, ikke bars, og styres ikke
# af Max Bars Back. Tallet angiver, hvilket argument der er "antal tilbage":
# OpenD(1) = i går, OpenSession(0, 1) = forrige session.
PERIODE_FUNKTIONER = {
    "opend": 0, "highd": 0, "lowd": 0, "closed": 0,
    "opensession": 1, "highsession": 1, "lowsession": 1, "closesession": 1,
}
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


def _tilbage(tekst, perioder, uvisse):
    """Hvor mange bars et stykke formel ser tilbage, så vidt det kan regnes ud.

    Dags-/sessionsværdier samles i 'perioder' som (funktion, antal tilbage).
    Det, der ikke kan regnes ud, samles i 'uvisse' som tekst.
    """
    stoerst = 0
    # Bar-henvisninger som High[1]
    for m in re.finditer(r"\[([^\[\]]+)\]", tekst):
        v = _regn(m.group(1))
        if v is None:
            uvisse.append(f"[{m.group(1)}]")
        else:
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
        inde = max(_tilbage(x, perioder, uvisse) for x in args)

        if navn in LAENGDE_ARGUMENTER:
            laengder = [_regn(args[nr]) if nr < len(args) else None
                        for nr in LAENGDE_ARGUMENTER[navn]]
            if None in laengder:
                uvisse.append(f"længden i {m.group(1)}")
                stoerst = max(stoerst, inde)
            else:
                # En funktion af en funktion skal bruge begges historik
                stoerst = max(stoerst, int(math.ceil(max(laengder))) + inde)
        elif navn in PERIODE_FUNKTIONER:
            nr = PERIODE_FUNKTIONER[navn]
            v = _regn(args[nr]) if nr < len(args) else None
            if v is None:
                uvisse.append(f"antal tilbage i {m.group(1)}")
            else:
                perioder.append((m.group(1), int(math.ceil(v))))
            stoerst = max(stoerst, inde)
        elif navn in UDEN_HISTORIK:
            stoerst = max(stoerst, inde)
        else:
            uvisse.append(f"funktionen {m.group(1)}")
            stoerst = max(stoerst, inde)
        i = j
    return stoerst


def tekst(a):
    """Linjerne om Max Bars Back til filernes hoved. Stopper bygningen, hvis
    formlen med sikkerhed skal bruge mere end STANDARD."""
    hoejeste = {"Filter1_" + x["navn"]: tal_tekst(x["slut"]) for x in a["parametre"]}
    formel = udskift(a["formel"], hoejeste)
    perioder, uvisse = [], []
    bars = _tilbage(formel, perioder, uvisse)

    vaerdier = ", ".join(f"{k.replace('Filter1_', '')}={v}" for k, v in hoejeste.items())
    ved = f" ved {vaerdier}" if vaerdier else ""
    if bars > STANDARD:
        raise ByggeFejl(f"Filter {a['id']}: formlen skal bruge {bars} bars{ved}, men Max Bars Back "
                        f"står på {STANDARD}. Hæv Max Bars Back for dette filter, eller sænk N-værdierne.")

    if bars == 0:
        linjer = [f"Står på {STANDARD} (standard). Formlen ser ikke tilbage i bars."]
    else:
        linjer = [f"Står på {STANDARD} (standard). Længste beregning er {bars} bars{ved}."]
    if perioder:
        flest = max(d for _, d in perioder)
        navne = ", ".join(sorted({n for n, _ in perioder}))
        linjer += [f"Formlen bruger dags-/sessionsværdier ({navne}) op til {flest} tilbage.",
                   "De styres ikke af Max Bars Back, men de første dage/sessioner i",
                   "dataene har ingen gyldig værdi."]
    if uvisse:
        linjer += [f"Kunne ikke regnes helt ud: {', '.join(sorted(set(uvisse)))}.",
                   f"{STANDARD} antages at være nok. Stopper strategien med en fejl om",
                   "for få bars, skal Max Bars Back hæves for dette filter."]
    return linjer
