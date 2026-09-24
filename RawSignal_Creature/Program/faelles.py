# Fælles indstillinger og hjælpere for RawSignal Creature: mapper, log og
# forbindelsen til TradingDB.

import os
from datetime import datetime

import psycopg2

# ---- Mapper ----
PROGRAM_MAPPE = os.path.dirname(os.path.abspath(__file__))
LOGFIL = os.path.join(PROGRAM_MAPPE, "log", "rawsignal_creature.log")

FILTER_MAPPE = r"C:\TradingDB_Folder\FilterFolder"
EL_MAPPE_STRATEGI = os.path.join(FILTER_MAPPE, "RawSignal.EL")
EL_MAPPE_KONTROL = os.path.join(FILTER_MAPPE, "RawSignal_Kontrol.EL")
# Samme kode som .txt, så den kan læses uden TradeStation
TXT_MAPPE_STRATEGI = os.path.join(FILTER_MAPPE, "RawSignal.TXT")
TXT_MAPPE_KONTROL = os.path.join(FILTER_MAPPE, "RawSignal_Kontrol.TXT")
CSV_MAPPE = os.path.join(FILTER_MAPPE, "RawSignal.CSV")


def signal_navn(filter_case_id):
    """Strategiens navn: filter_case_id med tre cifre, fx 7 -> RawSignal007."""
    return f"RawSignal{filter_case_id:03d}"


def log(tekst):
    """Skriver både på skærmen og i logfilen, så intet går tabt."""
    linje = f"{datetime.now():%Y-%m-%d %H:%M:%S}  {tekst}"
    print(linje)
    os.makedirs(os.path.dirname(LOGFIL), exist_ok=True)
    with open(LOGFIL, "a", encoding="utf-8") as f:
        f.write(linje + "\n")


def forbind():
    """Forbindelse til TradingDB. Adgangskoden hentes automatisk fra pgpass.conf."""
    return psycopg2.connect(host="127.0.0.1", user="postgres", dbname="TradingDB")
