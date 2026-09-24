# Læser et filter fra filter_case og bestemmer, hvordan filerne skal bygges.
#
# Regler (OPGAVEBESKRIVELSE_RawSignal.md og BYGGEVEJLEDNING_RawSignal.md):
#  - Formlen sættes ind ordret. Kun Filter1_N1 og Filter1_N2 udskiftes.
#  - Hvilke parametre filteret bruger, afgøres af formelteksten, ikke af
#    databasekolonnerne.
#  - Værdi/plads-opdelingen (N2_Vaerdi/N2_Indeks) bruges KUN, når
#    parameteren har decimaltal. Ellers er N1 (eller N2) både værdi og plads.

import re
from decimal import Decimal

from faelles import signal_navn

# Største _end-værdi i hele filter_case er 25. Arrays har altid denne
# størrelse, så Fra/Til/Step senere kan hæves uden at ramme grænsen.
ARRAY_STOERRELSE = 25

# Indbyggede funktioner, der husker deres forrige værdi. Kaldes de i en
# løkke med skiftende parametre, kan tallene blive forkerte uden fejl.
# Listen bruges KUN til at afgøre, om advarslen skal i filens hoved.
SERIEFUNKTIONER = [
    "MACD", "RSI", "StandardDev", "Average", "XAverage", "DMIplus",
    "DMIminus", "ADX", "ChaikinMoneyFlow", "AvgTrueRange",
]


class ByggeFejl(Exception):
    """Filteret kan ikke bygges sikkert. Programmet stopper hellere end at gætte."""


def tal_tekst(v):
    """1 i stedet for 1.00, 0.25 med punktum."""
    d = Decimal(str(v))
    if d == d.to_integral_value():
        return str(int(d))
    return format(d.normalize(), "f")


def er_decimal(*vaerdier):
    return any(v is not None and Decimal(str(v)) != Decimal(str(v)).to_integral_value()
               for v in vaerdier)


def bruger(formel, navn):
    """Står navnet som et helt ord i formlen (store/små bogstaver ligegyldige)?"""
    return re.search(r"\b" + navn + r"\b", formel, re.IGNORECASE) is not None


def udskift(formel, navne):
    """Udskifter hele ord, fx Filter1_N1 -> N1. Intet andet i formlen ændres."""
    for gammel, ny in navne.items():
        formel = re.sub(r"\b" + gammel + r"\b", ny, formel, flags=re.IGNORECASE)
    return formel


def analyser(raekke):
    """Læser formlen og returnerer det, der skal bruges til at bygge filerne."""
    fid = raekke["filter_case_id"]
    raa = raekke["filtere"]
    if raa is None or raa.strip() == "":
        raise ByggeFejl(f"Filter {fid}: formlen er tom.")
    # { } ville afslutte kommentarblokken i filens hoved, hvor formlen står.
    if "{" in raa or "}" in raa or "\n" in raa or "\r" in raa:
        raise ByggeFejl(f"Filter {fid}: formlen indeholder {{, }} eller linjeskift.")

    formel = raa.strip()
    if formel.endswith(";"):
        formel = formel[:-1].rstrip()

    # Navnene, der sættes ind i stedet for Filter1_N1/N2, må ikke findes i
    # formlen i forvejen - så kunne kontrollen af ordret formel snydes.
    for optaget in ("N1", "N2", "N1_Vaerdi", "N2_Vaerdi", "Vis_N1", "Vis_N2"):
        if bruger(formel, optaget):
            raise ByggeFejl(f"Filter {fid}: formlen indeholder allerede navnet {optaget}.")

    parametre = []
    for nr in ("1", "2"):
        if not bruger(formel, "Filter1_N" + nr):
            continue
        start = raekke[f"filter1_n{nr}_start"]
        slut = raekke[f"filter1_n{nr}_end"]
        step = raekke[f"filter1_n{nr}_step"]
        if start is None or slut is None or step is None:
            raise ByggeFejl(f"Filter {fid}: formlen bruger Filter1_N{nr}, men Fra/Til/Step er tomme.")
        if Decimal(str(step)) <= 0:
            raise ByggeFejl(f"Filter {fid}: N{nr}_Step skal være større end 0.")
        antal_trin = int((Decimal(str(slut)) - Decimal(str(start))) / Decimal(str(step))) + 1
        decimal = er_decimal(start, slut, step)
        # Uden decimaler er værdien også pladsen i arrayet, så største værdi
        # skal kunne være der. Med decimaler tælles pladsen 1, 2, 3 ...
        stoerste_plads = antal_trin if decimal else int(Decimal(str(slut)))
        if stoerste_plads > ARRAY_STOERRELSE or Decimal(str(start)) < 0:
            raise ByggeFejl(f"Filter {fid}: N{nr} fylder mere end arrayets {ARRAY_STOERRELSE} pladser.")
        parametre.append({
            "navn": "N" + nr,
            "decimal": decimal,
            "start": start, "slut": slut, "step": step,
            # Variablen, der bruges i formlen og i CSV-linjen
            "vaerdi": f"N{nr}_Vaerdi" if decimal else f"N{nr}",
            # Variablen, der bruges som plads i arrayet
            "plads": f"N{nr}_Indeks" if decimal else f"N{nr}",
        })

    fundne = [f for f in SERIEFUNKTIONER
              if re.search(r"\b" + f + r"\s*\(", formel, re.IGNORECASE)]

    return {
        "id": fid,
        "navn": signal_navn(fid),
        "kontrol_navn": signal_navn(fid) + "_Kontrol",
        "raa_formel": raa.strip(),
        "formel": formel,
        "parametre": parametre,
        "bruger_b": bruger(formel, "DataFilter_B"),
        "seriefunktioner": fundne,
    }
