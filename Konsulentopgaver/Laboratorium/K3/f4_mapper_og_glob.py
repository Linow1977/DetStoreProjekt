"""
Forsøg F4 (K3): Kan Parquet-mappestrukturen selv blande perioder?

Spørgsmål:
  1. Hvis test/, oos/ og embargo/ ligger under SAMME rodmappe (arkiv/), og en
     analyse læser "arkiv/**/*.parquet" (et helt almindeligt jokertegn), får den
     så OOS-rækker med uden at opdage det?
  2. Springer DuckDB filer over, når man filtrerer på mappe-nøgler (filter,
     barstørrelse)? (Det er grunden til opdelingen.)

Opsætning: Opdigtede Parquet-filer: 20 filtre x 12 barstørrelser i test/,
og 2 filtre i oos/. Kun opdigtede data.
"""
import os
import shutil
import time
import duckdb
import numpy as np
import pandas as pd

HER = os.path.dirname(os.path.abspath(__file__))
ROD = os.path.join(HER, "f4_ud")
shutil.rmtree(ROD, ignore_errors=True)
rng = np.random.default_rng(4)


def skriv(periode, filt, barstr, aar):
    mappe = os.path.join(ROD, "arkiv", periode, "signaler", f"barstr={barstr}", f"filter={filt}")
    os.makedirs(mappe, exist_ok=True)
    t = pd.date_range(f"{aar[0]}-01-02", f"{aar[1]}-12-10", freq=f"{barstr}min")
    n = min(50_000, len(t) // 2)
    idx = np.sort(rng.choice(len(t), n, replace=False))
    pd.DataFrame({"n1": rng.integers(1, 26, n).astype("int16"),
                  "n2": rng.integers(1, 26, n).astype("int16"),
                  "starttid": t[idx], "antalbars": rng.integers(1, 20, n).astype("int16")}
                 ).to_parquet(os.path.join(mappe, "job=000001.parquet"), index=False, compression="zstd")


for f in range(1, 21):
    for b in range(5, 65, 5):
        skriv("test", f"F{f:04d}", b, (2020, 2024))
for f in (1, 2):
    skriv("oos", f"F{f:04d}", 10, (2025, 2025))

# 1) Det uskyldige jokertegn
r = duckdb.sql(f"""SELECT year(starttid) AS aar, count(*) FROM read_parquet('{ROD}/arkiv/**/*.parquet')
                  GROUP BY 1 ORDER BY 1""").fetchall()
print("Læst med arkiv/**/*.parquet  ->  rækker pr. år:", r)
aar_2025 = sum(c for a, c in r if a == 2025)
print(f"  => {aar_2025:,} OOS-rækker (2025) kom med uden fejl eller advarsel.\n")

# 2) Opdeling: filter på mappe-nøgler
glob_test = f"{ROD}/arkiv/test/signaler/**/*.parquet"
t0 = time.time()
alle = duckdb.sql(f"SELECT count(*) FROM read_parquet('{glob_test}', hive_partitioning=true)").fetchone()[0]
t_alle = time.time() - t0
t0 = time.time()
en = duckdb.sql(f"""SELECT count(*) FROM read_parquet('{glob_test}', hive_partitioning=true)
                    WHERE filter = 'F0007' AND barstr = 10""").fetchone()[0]
t_en = time.time() - t0
plan = duckdb.sql(f"""EXPLAIN ANALYZE SELECT count(*) FROM read_parquet('{glob_test}', hive_partitioning=true)
                      WHERE filter = 'F0007' AND barstr = 10""").fetchall()[0][1]
linjer = [l.strip() for l in plan.splitlines() if "Files" in l or "Total Files" in l or "Scanning" in l]
print(f"Alle test-rækker: {alle:,} på {t_alle:.3f} s")
print(f"Ét filter x én barstørrelse: {en:,} rækker på {t_en:.3f} s")
print("Fra DuckDB's plan:", linjer[:4])

# 3) Værn i læse-funktionen: tjek filernes indbyggede min/max-statistik FØR der læses data
def sikker_laes_test(glob, sidste_testdag="2024-12-13"):
    """Nægt at læse, hvis blot én fil har starttid efter testperioden (koster kun metadata)."""
    maks = duckdb.sql(f"""
        SELECT file_name, max(stats_max) AS maks FROM parquet_metadata('{glob}')
        WHERE path_in_schema = 'starttid' GROUP BY 1 HAVING max(stats_max) > '{sidste_testdag}'
    """).fetchall()
    if maks:
        raise PermissionError(f"{len(maks)} fil(er) har data efter {sidste_testdag}, fx {maks[0][0][-60:]}")
    return duckdb.sql(f"SELECT * FROM read_parquet('{glob}', hive_partitioning=true)")

t0 = time.time()
try:
    sikker_laes_test(f"{ROD}/arkiv/**/*.parquet")
    print("\nVærn: jokertegn over hele arkivet blev LÆST (problem!)")
except PermissionError as e:
    print(f"\nVærn: jokertegn over hele arkivet afvist ({time.time() - t0:.3f} s): {e}")
n_ok = sikker_laes_test(glob_test).count("*").fetchone()[0]
print(f"Værn: kun test/-mappen læst normalt: {n_ok:,} rækker")
