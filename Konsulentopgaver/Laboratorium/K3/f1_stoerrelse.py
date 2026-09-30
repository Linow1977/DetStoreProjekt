"""
Forsøg F1 (K3): Hvor meget fylder én million signal-linjer?

Spørgsmål: Holder skønnet i del3_K3.md afsnit 4 (ca. 40 tegn pr. CSV-linje,
3-8 bytes pr. linje i Parquet)? Og hvad betyder sorteringen?

Opsætning: Opdigtede signal-linjer i samme format som RawSignal-CSV'en
(RunID,N1,N2,Starttid,AntalBars,Afsluttet) for ét filter på 5-min bars,
625 parameterkombinationer (25x25), 2020-2024. Starttider ligger på
5-minutters lukketider i en 23-timers session. Signalerne er trukket
uafhængigt for hver kombination (værste fald for komprimering; rigtige
nabo-kombinationer ligner hinanden og pakker sig bedre).

Kun opdigtede data. Intet fra TradingDB eller repoet.
"""
import os
import time
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import duckdb

UD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "f1_ud")
os.makedirs(UD, exist_ok=True)
rng = np.random.default_rng(20260929)

# --- Opdigtede 5-minutters lukketider, 2020-2024, 23 timer pr. handelsdag ---
dage = pd.bdate_range("2020-01-02", "2024-12-31")
bar_pr_dag = 23 * 12
minutter = (np.arange(1, bar_pr_dag + 1) * 5)  # lukketid efter sessionens start
# sessionen starter 17:00 dagen før (futures-agtigt); vi stempler i "børstid"
session_start = (dage - pd.Timedelta(hours=7)).values.astype("datetime64[m]")
alle_bars = (session_start[:, None] + minutter[None, :].astype("timedelta64[m]")).ravel()
print(f"Opdigtede 5-min bars 2020-2024: {len(alle_bars):,}")

MAAL_LINJER = 3_000_000          # ca. som RawSignal069 (114 MB) [Repo via Overordnet]
kombi = [(n1, n2) for n1 in range(2, 52, 2) for n2 in range(1, 26)]
pr_kombi = MAAL_LINJER // len(kombi)

dele = []
for n1, n2 in kombi:
    idx = np.sort(rng.choice(len(alle_bars), size=pr_kombi, replace=False))
    dele.append(pd.DataFrame({
        "runid": "RawSignal069",
        "n1": np.int16(n1),
        "n2": np.int16(n2),
        "starttid": alle_bars[idx],
        "antalbars": rng.geometric(0.2, size=pr_kombi).astype(np.int32),
        "afsluttet": np.int8(1),
    }))
df = pd.concat(dele, ignore_index=True)
df.loc[df.index[-1], "afsluttet"] = 0
n = len(df)
print(f"Signal-linjer: {n:,}")


def mb(sti):
    return os.path.getsize(sti) / 1e6


res = []

# CSV som TradeStation skriver den
csv = os.path.join(UD, "signal.csv")
tmp = df.copy()
tmp["starttid"] = pd.to_datetime(tmp["starttid"]).dt.strftime("%Y-%m-%d %H:%M")
tmp.to_csv(csv, index=False, header=False)
res.append(("CSV (som TradeStation)", mb(csv)))
del tmp

# Parquet: filter og barstørrelse ligger i mappenavnet, så runid gemmes ikke pr. linje
til_parquet = df.drop(columns=["runid"])
for navn, sortering in [("sorteret n1,n2,starttid", ["n1", "n2", "starttid"]),
                        ("sorteret starttid", ["starttid", "n1", "n2"])]:
    t = pa.Table.from_pandas(til_parquet.sort_values(sortering), preserve_index=False)
    for codec in ["snappy", "zstd"]:
        sti = os.path.join(UD, f"signal_{codec}_{sortering[0]}.parquet")
        pq.write_table(t, sti, compression=codec)
        res.append((f"Parquet {codec}, {navn}", mb(sti)))

# DuckDB-databasefil (stand-in for "rækker i en database"; PostgreSQL er større, se tekst)
dbsti = os.path.join(UD, "signal.duckdb")
if os.path.exists(dbsti):
    os.remove(dbsti)
con = duckdb.connect(dbsti)
con.register("df", til_parquet)
con.execute("CREATE TABLE s AS SELECT * FROM df ORDER BY n1, n2, starttid")
con.close()
res.append(("DuckDB-tabel (kolonnevis database)", mb(dbsti)))

# PostgreSQL-skøn: 23 bytes hoved + 4 bytes pointer + data (2+2+8+4+1 -> justeret til 24)
# + indeks på (n1,n2,starttid) ca. 8+12+hoved -> ~32 bytes. Groft skøn, ikke målt.
pg_bytes = (23 + 4 + 24) + 32
res.append(("PostgreSQL (regnet, ikke målt)", pg_bytes * n / 1e6))

print()
print(f"{'Format':45s} {'MB i alt':>9s} {'bytes/linje':>11s} {'MB pr. mio.':>11s}")
for navn, stoer in res:
    print(f"{navn:45s} {stoer:9.1f} {stoer * 1e6 / n:11.1f} {stoer * 1e6 / n:11.1f}")

# Hvor hurtigt kan DuckDB læse en Parquet-fil og lave dagstal?
sti = os.path.join(UD, "signal_zstd_n1.parquet")
t0 = time.time()
r = duckdb.sql(f"""
    SELECT n1, n2, CAST(starttid AS DATE) AS dag, count(*) AS antal
    FROM read_parquet('{sti}') GROUP BY ALL
""").fetchall()
print(f"\nDuckDB: dagsoptælling pr. kombination af {n:,} linjer: {time.time() - t0:.2f} s, {len(r):,} grupper")
