"""
Forsøg F3 (K3): "Ryd op og kør forfra" efter et nedbrud midt i et job.

Spørgsmål: Hvis indlæseren dør på et dårligt tidspunkt, efterlader den så
halve filer, dubletter eller rækker uden fil? Og giver oprydning + ny kørsel
PRÆCIS det samme slutresultat som en kørsel uden nedbrud?

Opsætning: Tre jobs (ét filter x tre barstørrelser) indlæses fra opdigtede
CSV-filer til Parquet + katalog i DuckDB. Hvert job kører i sin egen proces.
Processen dræbes hårdt (os._exit, som et strømsvigt) på tre steder:
  A  midt i skrivningen af den midlertidige fil
  B  efter filen er flyttet på plads, men før katalog-rækken er skrevet
  C  efter katalog-rækken, men før jobbet er meldt FAERDIG
Så køres den godkendte oprydning (ryd_op_job) og jobbet forfra. Til sidst
sammenlignes fingeraftryk (SHA-256) af alle filer og katalog-rækker med en
"ren" kørsel uden nedbrud.

Kun opdigtede data.
"""
import hashlib
import os
import shutil
import subprocess
import sys
import duckdb
import numpy as np
import pandas as pd

HER = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable


def sha(sti):
    with open(sti, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def lav_csv(mappe, barstr):
    rng = np.random.default_rng(barstr)
    t = pd.date_range("2020-01-02", "2024-12-13", freq=f"{barstr}min")
    idx = np.sort(rng.choice(len(t), 20_000, replace=False))
    df = pd.DataFrame({"runid": "RawSignal069", "n1": rng.integers(1, 26, 20_000),
                       "n2": rng.integers(1, 26, 20_000), "starttid": t[idx].strftime("%Y-%m-%d %H:%M"),
                       "antalbars": rng.integers(1, 20, 20_000), "afsluttet": 1})
    sti = os.path.join(mappe, f"indbakke_barstr{barstr}.csv")
    df.to_csv(sti, index=False, header=False)
    return sti


# ---------------- selve jobbet (kører i sin egen proces) ----------------
def koer_job(mappe, job_id, barstr, csv_sti, doer_ved):
    con = duckdb.connect(os.path.join(mappe, "tdb.duckdb"))
    df = pd.read_csv(csv_sti, names=["runid", "n1", "n2", "starttid", "antalbars", "afsluttet"])
    endelig = os.path.join(mappe, "arkiv", "test", "signaler", f"barstr={barstr}",
                           "filter=F0069", f"job={job_id:06d}.parquet")
    os.makedirs(os.path.dirname(endelig), exist_ok=True)
    midlertidig = endelig + ".tmp"
    # Deterministisk fil: samme input giver samme bytes (ingen tidsstempler i filen)
    tabel = df.drop(columns=["runid"]).sort_values(["starttid", "n1", "n2"])
    if doer_ved == "A":
        with open(midlertidig, "wb") as f:
            f.write(b"PAR1" + b"\0" * 5000)      # halv fil
        os._exit(9)
    tabel.to_parquet(midlertidig, index=False, compression="zstd")
    os.replace(midlertidig, endelig)
    if doer_ved == "B":
        os._exit(9)
    con.execute("INSERT INTO katalog VALUES (?, ?, ?, ?)", [job_id, endelig, len(tabel), sha(endelig)])
    if doer_ved == "C":
        os._exit(9)
    con.execute("UPDATE job SET status = 'FAERDIG' WHERE job_id = ?", [job_id])
    con.close()


# ---------------- oprydning (samme i alle tilfælde) ----------------
def ryd_op_job(mappe, job_id):
    """Slet ALT, jobbet har skrevet: katalog-række, endelig fil, midlertidig fil. Intet andet."""
    con = duckdb.connect(os.path.join(mappe, "tdb.duckdb"))
    con.execute("DELETE FROM katalog WHERE job_id = ?", [job_id])
    con.execute("UPDATE job SET status = 'VENTER', forsoeg = forsoeg + 1 WHERE job_id = ?", [job_id])
    con.close()
    for rod, _, filer in os.walk(os.path.join(mappe, "arkiv")):
        for f in filer:
            if f"job={job_id:06d}" in f:
                os.remove(os.path.join(rod, f))


def nat_tjek(mappe):
    """Natlig kontrol: filer uden katalog-række, katalog-rækker uden fil, .tmp-rester."""
    con = duckdb.connect(os.path.join(mappe, "tdb.duckdb"))
    i_katalog = {r[0] for r in con.execute("SELECT sti FROM katalog").fetchall()}
    con.close()
    paa_disk = {os.path.join(r, f) for r, _, fs in os.walk(os.path.join(mappe, "arkiv")) for f in fs}
    return {"filer uden katalog": len(paa_disk - i_katalog),
            "katalog uden fil": len(i_katalog - paa_disk),
            "tmp-rester": sum(1 for p in paa_disk if p.endswith(".tmp"))}


def ny_verden(navn):
    mappe = os.path.join(HER, "f3_ud", navn)
    shutil.rmtree(mappe, ignore_errors=True)
    os.makedirs(mappe)
    con = duckdb.connect(os.path.join(mappe, "tdb.duckdb"))
    con.execute("CREATE TABLE job (job_id INTEGER PRIMARY KEY, barstr INTEGER, status TEXT, forsoeg INTEGER)")
    con.execute("CREATE TABLE katalog (job_id INTEGER PRIMARY KEY, sti TEXT, raekker BIGINT, sha256 TEXT)")
    for j, b in [(1, 5), (2, 10), (3, 15)]:
        con.execute("INSERT INTO job VALUES (?, ?, 'VENTER', 0)", [j, b])
    con.close()
    return mappe


def start_proces(mappe, job_id, barstr, csv_sti, doer_ved):
    return subprocess.run([PY, __file__, "job", mappe, str(job_id), str(barstr), csv_sti, doer_ved]).returncode


def slutbillede(mappe):
    con = duckdb.connect(os.path.join(mappe, "tdb.duckdb"), read_only=True)
    kat = con.execute("SELECT job_id, raekker, sha256 FROM katalog ORDER BY job_id").fetchall()
    st = con.execute("SELECT job_id, status FROM job ORDER BY job_id").fetchall()
    con.close()
    return kat, st


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "job":
    koer_job(sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5], sys.argv[6])
    sys.exit(0)

if __name__ == "__main__":
    indbakke = os.path.join(HER, "f3_ud", "indbakke")
    shutil.rmtree(indbakke, ignore_errors=True)
    os.makedirs(indbakke)
    csv = {b: lav_csv(indbakke, b) for b in (5, 10, 15)}

    # 1) Ren kørsel
    ren = ny_verden("ren")
    for j, b in [(1, 5), (2, 10), (3, 15)]:
        start_proces(ren, j, b, csv[b], "-")
    ren_billede = slutbillede(ren)

    # 2) Kørsel med nedbrud på tre forskellige steder
    snavs = ny_verden("nedbrud")
    for j, b, doer in [(1, 5, "A"), (2, 10, "B"), (3, 15, "C")]:
        kode = start_proces(snavs, j, b, csv[b], doer)
        print(f"job {j}: døde ved {doer} (exit {kode})")
    print("Efter nedbrud, før oprydning:", nat_tjek(snavs), slutbillede(snavs)[1])

    # 3) Vagten ser tre jobs, der ikke blev FAERDIG -> ryd op og kør forfra
    for j, b in [(1, 5), (2, 10), (3, 15)]:
        ryd_op_job(snavs, j)
        start_proces(snavs, j, b, csv[b], "-")
    print("Efter oprydning + forfra:", nat_tjek(snavs))

    snavs_billede = slutbillede(snavs)
    print("\nRen kørsel     :", ren_billede[0])
    print("Nedbrud+forfra :", snavs_billede[0])
    print("\nSlutresultat identisk (rækker + SHA-256 af hver fil):", ren_billede[0] == snavs_billede[0])
    print("Status:", snavs_billede[1])
