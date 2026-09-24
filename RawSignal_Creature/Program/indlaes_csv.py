# Læser en RawSignal-CSV-fil ind i TradingDB, i filterets egen tabel i
# schemaet rawsignal, fx rawsignal.rawsignal001.
#
# Brug:  python indlaes_csv.py <filter_case_id>
#        fx  python indlaes_csv.py 1   ->  RawSignal001.csv -> rawsignal.rawsignal001
#
# - Findes tabellen ikke, oprettes den (kolonner som CSV-filen).
# - Tabellens gamle linjer slettes først, så intet bliver dobbelt, når et
#   signal køres igen.
# - Alt sker i én transaktion: fejler noget, ændres intet.
# - Hver linjes RunID skal være filnavnet. Ellers indlæses intet.
# - CSV-filen bliver liggende. Den bruges også af EdgeFinder.
#
# Kør først, når backtesten i TradeStation er helt færdig. Ellers er filen
# ikke skrevet færdig.

import csv
import os
import sys

from faelles import CSV_MAPPE, forbind, log, signal_navn

SCHEMA = "rawsignal"

# CSV-kolonne -> kolonne i den midlertidige tabel
KOLONNER = {
    "RunID": "runid", "N1": "n1", "N2": "n2", "Starttid": "starttid",
    "AntalBars": "antalbars", "Afsluttet": "afsluttet",
}


def main():
    if len(sys.argv) != 2 or not sys.argv[1].isdigit():
        print("Brug: python indlaes_csv.py <filter_case_id>")
        return 2
    navn = signal_navn(int(sys.argv[1]))
    tabel = f"{SCHEMA}.{navn.lower()}"
    sti = os.path.join(CSV_MAPPE, navn + ".csv")
    if not os.path.exists(sti):
        log(f"STOP: {sti} findes ikke. Kør strategien i TradeStation først.")
        return 1

    with open(sti, encoding="utf-8-sig", newline="") as f:
        overskrift = next(csv.reader(f), None)
    if not overskrift or any(k not in KOLONNER for k in overskrift):
        log(f"STOP: {navn}.csv har en ukendt overskrift: {overskrift}")
        return 1
    csv_kolonner = ", ".join(KOLONNER[k] for k in overskrift)

    db = forbind()
    try:
        with db.cursor() as c:
            # Først ind i en midlertidig tabel, så indholdet kan tjekkes,
            # før filterets tabel røres.
            c.execute("""create temp table ny (
                             runid text, n1 numeric, n2 numeric, starttid timestamp,
                             antalbars integer, afsluttet smallint) on commit drop""")
            with open(sti, encoding="utf-8-sig", newline="") as f:
                c.copy_expert(f"copy ny ({csv_kolonner}) from stdin with (format csv, header true)", f)
            c.execute("select count(*), count(*) filter (where runid <> %s) from ny", (navn,))
            antal, forkerte = c.fetchone()
            if forkerte:
                db.rollback()
                log(f"STOP: {forkerte} linjer i {navn}.csv har et andet RunID end {navn}. Intet indlæst.")
                return 1

            c.execute(f"""create table if not exists {tabel} (
                              runid text not null, n1 numeric, n2 numeric,
                              starttid timestamp not null, antalbars integer not null,
                              afsluttet smallint not null)""")
            c.execute(f"create index if not exists {navn.lower()}_n1_n2_starttid on {tabel} (n1, n2, starttid)")
            c.execute(f"delete from {tabel}")
            slettet = c.rowcount
            c.execute(f"""insert into {tabel} (runid, n1, n2, starttid, antalbars, afsluttet)
                          select runid, n1, n2, starttid, antalbars, afsluttet from ny""")
            c.execute("select count(*) filter (where afsluttet = 0) from ny")
            aabne = c.fetchone()[0]
        db.commit()
        log(f"{navn}: {antal} signaler indlæst i {tabel} "
            f"({aabne} stadig tændt på sidste bar). {slettet} gamle linjer slettet først.")
        return 0
    except Exception as e:
        db.rollback()
        log(f"STOP: {navn}.csv kunne ikke indlæses: {e}")
        return 1
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
