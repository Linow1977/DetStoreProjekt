"""
Forsøg F5 (K3): Jobkøens regler — lån, livstegn, billet-nummer, maks-forsøg.

Spørgsmål: Med 8 arbejdere, hvoraf nogle "dør" midt i et job og én "vågner op
for sent", bliver hvert job så gjort færdigt præcis én gang, og kan en
forsinket arbejder melde et job færdigt, som en anden har overtaget?

Opsætning: DuckDB-tabel `job` i én proces med 8 tråde (hver med sin egen
forbindelse). DuckDB har IKKE `SELECT ... FOR UPDATE SKIP LOCKED`; i stedet
tager en arbejder et job med én UPDATE ... WHERE status='VENTER' og lader
DuckDB's konfliktkontrol afvise, hvis to prøver samtidig. I PostgreSQL bruges
SKIP LOCKED (del3_K3.md afs. 10.2) — selve reglerne er de samme.
Kun opdigtede jobs.
"""
import os
import random
import shutil
import threading
import time
import duckdb

HER = os.path.dirname(os.path.abspath(__file__))
MAPPE = os.path.join(HER, "f5_ud")
shutil.rmtree(MAPPE, ignore_errors=True)
os.makedirs(MAPPE)
DB = duckdb.connect(os.path.join(MAPPE, "koe.duckdb"))
ANTAL_JOBS, MAKS_FORSOEG, LAAN_SEK = 400, 3, 0.5

DB.execute("""CREATE TABLE job (job_id INTEGER PRIMARY KEY, status TEXT, forsoeg INTEGER,
              billet INTEGER, laant_til DOUBLE, udfoert_af TEXT)""")
DB.execute(f"INSERT INTO job SELECT i, 'VENTER', 0, 0, NULL, NULL FROM range({ANTAL_JOBS}) t(i)")
DB.execute("CREATE TABLE udfoerelse (job_id INTEGER, arbejder TEXT, billet INTEGER)")  # "resultater"
statistik = {"konflikter": 0, "afviste_forsinkede": 0, "doede": 0}
laas = threading.Lock()
random.seed(5)


def tag_job(con, navn):
    """Tag et ledigt job (eller et job, hvis lån er udløbet). Returnerer (job_id, billet) eller None."""
    nu = time.time()
    try:
        r = con.execute("""
            UPDATE job SET status='I_GANG', forsoeg=forsoeg+1, billet=billet+1,
                           laant_til=?, udfoert_af=?
            WHERE job_id = (SELECT min(job_id) FROM job
                            WHERE (status='VENTER') OR (status='I_GANG' AND laant_til < ?))
            RETURNING job_id, billet, forsoeg""", [nu + LAAN_SEK, navn, nu]).fetchall()
    except duckdb.TransactionException:
        with laas:
            statistik["konflikter"] += 1
        return "prøv igen"
    if not r:
        return None
    job_id, billet, forsoeg = r[0]
    if forsoeg > MAKS_FORSOEG:
        con.execute("UPDATE job SET status='OPGIVET' WHERE job_id=? AND billet=?", [job_id, billet])
        return "prøv igen"
    return job_id, billet


def meld_faerdig(con, job_id, billet, navn):
    """Kun den, der har den NYESTE billet, må melde færdig (resultat + status i én transaktion)."""
    while True:
        try:
            con.execute("BEGIN")
            ok = con.execute("UPDATE job SET status='FAERDIG' WHERE job_id=? AND billet=? AND status='I_GANG' "
                             "RETURNING 1", [job_id, billet]).fetchall()
            if ok:
                con.execute("INSERT INTO udfoerelse VALUES (?, ?, ?)", [job_id, navn, billet])
                con.execute("COMMIT")
                return True
            con.execute("ROLLBACK")
            return False
        except duckdb.TransactionException:
            con.execute("ROLLBACK")          # skrivekonflikt: prøv at melde igen
            with laas:
                statistik["konflikter"] += 1


def arbejder(navn, doedsrisiko, sovende):
    con = DB.cursor()
    while True:
        t = tag_job(con, navn)
        if t is None:
            return
        if t == "prøv igen":
            continue
        job_id, billet = t
        if random.random() < doedsrisiko:      # arbejderen "dør": melder aldrig tilbage
            with laas:
                statistik["doede"] += 1
            continue                           # (tager bare næste job; det døde job hænger)
        if sovende and random.random() < 0.05:  # vågner op efter lånet er udløbet
            time.sleep(LAAN_SEK * 3)
        time.sleep(0.002)
        if not meld_faerdig(con, job_id, billet, navn):
            with laas:
                statistik["afviste_forsinkede"] += 1


traade = [threading.Thread(target=arbejder, args=(f"A{i}", 0.08 if i < 3 else 0.0, i == 7)) for i in range(8)]
t0 = time.time()
for t in traade:
    t.start()
for t in traade:
    t.join()
# Vagten: kør en sidste runde, indtil ingen lån hænger (arbejderne stoppede, da køen så tom ud)
while DB.execute("SELECT count(*) FROM job WHERE status='I_GANG'").fetchone()[0]:
    time.sleep(LAAN_SEK)
    arbejder("vagt-oprydder", 0.0, False)

fordeling = dict(DB.execute("SELECT status, count(*) FROM job GROUP BY 1").fetchall())
dubletter = DB.execute("SELECT count(*) FROM (SELECT job_id FROM udfoerelse GROUP BY 1 HAVING count(*)>1)").fetchone()[0]
mangler = DB.execute("SELECT count(*) FROM job WHERE job_id NOT IN (SELECT job_id FROM udfoerelse) AND status<>'OPGIVET'").fetchone()[0]
print(f"{ANTAL_JOBS} jobs, 8 arbejdere, {time.time() - t0:.1f} s")
print("Status til sidst:", fordeling)
print("Hændelser:", statistik)
print("Jobs med mere end ét godkendt resultat:", dubletter)
print("Jobs uden resultat (og ikke OPGIVET):", mangler)
