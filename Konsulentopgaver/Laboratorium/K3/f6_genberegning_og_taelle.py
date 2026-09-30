"""
Forsøg F6 (K3): Kan "regn igen" give bit-for-bit samme tal? Og hvad fylder tælle-tabellen?

Spørgsmål A: K2 foreslår at regne dagstal igen i stedet for at gemme dem, og
T13 kræver "samme fingeraftryk" på to maskiner. Giver en sum af kommatal
(netto efter omkostning) samme bits, når rækkefølgen af rækkerne ændres
(som den kan, når arbejdet deles på flere tråde eller computere)?

Spørgsmål B: Hvad fylder én million tælle-rækker (K1's felter), og hvad
koster 50 lokkedue-runder?

Kun opdigtede tal.
"""
import os
import shutil
import numpy as np
import pandas as pd
import duckdb

HER = os.path.dirname(os.path.abspath(__file__))
UD = os.path.join(HER, "f6_ud")
shutil.rmtree(UD, ignore_errors=True)
os.makedirs(UD)
rng = np.random.default_rng(6)

# ---------------- A: samme tal, anden rækkefølge ----------------
n = 3_000_000
brutto_ticks = rng.integers(-40, 41, n)                  # hele ticks
omk_ticks = 1.37                                          # kommission omregnet giver ofte brøkdele
netto_float = brutto_ticks - omk_ticks                    # kommatal
perm = rng.permutation(n)

s1 = float(np.sum(netto_float))
s2 = float(np.sum(netto_float[perm]))
s3 = float(sum(netto_float[perm].tolist()))               # simpel løkke, anden rækkefølge
print("A) Sum af netto som kommatal:")
print(f"   rækkefølge 1: {s1!r}\n   rækkefølge 2: {s2!r}\n   løkke       : {s3!r}")
print(f"   bit-identiske? {s1 == s2 == s3}")

# Samme i hele hundrededele af et tick (heltal): omkostning 1,37 tick = 137 hundrededele
netto_int = brutto_ticks * 100 - 137
i1 = int(np.sum(netto_int))
i2 = int(np.sum(netto_int[perm]))
print(f"   Som heltal (1/100 tick): {i1} / {i2}  -> bit-identiske? {i1 == i2}")

# DuckDB: gruppesum med flere tråde, to gange
df = pd.DataFrame({"celle": rng.integers(0, 2000, n), "netto": netto_float})
fing = []
for traade in (1, 4):
    con = duckdb.connect()
    con.execute(f"SET threads={traade}")
    r = con.execute("SELECT celle, sum(netto) AS s FROM df GROUP BY celle ORDER BY celle").fetchdf()
    fing.append(pd.util.hash_pandas_object(r, index=False).sum())
    con.close()
print(f"   DuckDB gruppesum 1 tråd vs 4 tråde, samme fingeraftryk? {fing[0] == fing[1]}")

# ---------------- B: tælle-tabellens størrelse ----------------
m = 1_000_000
taelle = pd.DataFrame({
    "koersel_id": np.int32(7),
    "fast_filter_id": rng.choice([f"F{i:04d}" for i in range(381)], m),
    "n1": rng.integers(1, 26, m).astype("int16"), "n2": rng.integers(1, 26, m).astype("int16"),
    "barstr_min": rng.choice(np.arange(5, 65, 5), m).astype("int16"),
    "retning": rng.choice(["LANG", "KORT"], m), "horisont_min": rng.choice([15, 60, 240], m).astype("int16"),
    "er_kontrol": True, "lokkedue_runde": np.int16(3), "froe": np.int64(123456789),
    "resultat": rng.choice(["BESTAAET", "IKKE_BESTAAET", "KAN_IKKE_DOEMMES"], m, p=[0.001, 0.8, 0.199]),
    "signaler": rng.integers(0, 20000, m).astype("int32"), "dage": rng.integers(0, 1250, m).astype("int16"),
    "netto_hundrededele": rng.integers(-500, 500, m).astype("int32"),
    "t": rng.normal(0, 1, m).astype("float32"), "plateau": rng.integers(0, 8, m).astype("int8"),
})
pq = os.path.join(UD, "taelle.parquet")
taelle.to_parquet(pq, index=False, compression="zstd")
dbf = os.path.join(UD, "taelle.duckdb")
con = duckdb.connect(dbf)
con.execute("CREATE TABLE t AS SELECT * FROM taelle")
con.close()
# PostgreSQL-skøn: 27 bytes række-overhead + ca. 70 bytes felter (tekst + tal) + evt. jsonb ~ 100 bytes
pg_skoen = (27 + 70) * m / 1e6
print("\nB) Én million tælle-rækker:")
print(f"   Parquet zstd : {os.path.getsize(pq) / 1e6:6.1f} MB")
print(f"   DuckDB       : {os.path.getsize(dbf) / 1e6:6.1f} MB")
print(f"   PostgreSQL   : ca. {pg_skoen:.0f} MB uden indeks (regnet, ikke målt; nøgletal som jsonb gør det større)")
celler = 12_000_000          # øvre skøn for celler pr. fuld RSA-kørsel (del3_K3.md afs. 4)
for runder in (20, 50):
    raekker = celler * (1 + runder)
    print(f"   1 ægte + {runder} lokkedue-runder x {celler/1e6:.0f} mio. celler = {raekker/1e6:,.0f} mio. rækker"
          f" ~ {raekker * (27 + 70) / 1e9:,.0f} GB i PostgreSQL (regnet) / "
          f"{raekker * os.path.getsize(pq) / m / 1e9:,.1f} GB i Parquet")
