"""
Forsøg F7 (K3): K1's to nye låse (rødt hold, fase 3).

Spørgsmål:
  T1  Tvilling-bagdør: kan en kasseret familie "komme igen" som et andet filter,
      der giver næsten de samme signaler? Og stopper tvilling-låsen det?
  T2  Én OOS-runde, blinde tal: kan forskningen se 2025-tal, før runden er lukket?
      Kan en familie åbnes, efter runden er lukket (den skal så vente på en ny periode)?

Opsætning: DuckDB som stand-in for PostgreSQL (se del3_K3.md afs. 15b).
Overlap måles som andel fælles signaldage (Jaccard) mellem to filtres
opdigtede signalserier. Grænsen 0,8 er K1's forslag [Antagelse].
Kun opdigtede data.
"""
import numpy as np
import duckdb

rng = np.random.default_rng(7)
con = duckdb.connect()
udfald = []

# ---------- opdigtede signaldage for fire filtre ----------
dage = np.arange(1250)                                   # handelsdage 2020-2024
f69 = set(rng.choice(dage, 400, replace=False))          # det kasserede filter
tvilling = set(list(f69)[:360]) | set(rng.choice(dage, 40, replace=False))   # ~90 % ens
fjern = set(rng.choice(dage, 400, replace=False))        # et uafhængigt filter
serier = {"F0069": f69, "F0200": tvilling, "F0300": fjern}


def overlap(a, b):
    return len(a & b) / len(a | b)


con.execute("""
CREATE TABLE familie_status (fast_filter_id TEXT, retning TEXT, status TEXT,
                             PRIMARY KEY (fast_filter_id, retning));
CREATE TABLE tvilling (a TEXT, b TEXT, retning TEXT, overlap DOUBLE);
CREATE TABLE oos_runde (runde_id INTEGER PRIMARY KEY, regel_version TEXT NOT NULL,
                        aabnet BOOLEAN NOT NULL, lukket BOOLEAN NOT NULL);
CREATE TABLE aabning (runde_id INTEGER, fast_filter_id TEXT, retning TEXT,
                      UNIQUE (fast_filter_id, retning));
CREATE TABLE resultat (fast_filter_id TEXT, retning TEXT, netto_hundrededele BIGINT, bestaaet BOOLEAN);
CREATE VIEW dom_synlig AS               -- tal vises KUN, når runden er lukket
  SELECT r.* FROM resultat r JOIN aabning a USING (fast_filter_id, retning)
  JOIN oos_runde o USING (runde_id) WHERE o.lukket;
CREATE VIEW dom_blind AS
  SELECT fast_filter_id, retning, bestaaet FROM resultat;
""")
con.execute("INSERT INTO familie_status VALUES ('F0069','LANG','KASSERET')")


def frys_1(filt, retning, graense=0.8):
    """Tvilling-tjek ved frys 1: overlap mod ALLE familier, der er lukkede eller i samme runde."""
    for andet, serie in serier.items():
        if andet == filt:
            continue
        ov = overlap(serier[filt], serie)
        con.execute("INSERT INTO tvilling VALUES (?,?,?,?)", [filt, andet, retning, ov])
    tvillinger = con.execute("""
        SELECT t.b, t.overlap, s.status FROM tvilling t
        JOIN familie_status s ON s.fast_filter_id = t.b AND s.retning = t.retning
        WHERE t.a = ? AND t.retning = ? AND t.overlap > ? AND s.status IN ('KASSERET','AABNET','BESTAAET')
    """, [filt, retning, graense]).fetchall()
    if tvillinger:
        raise PermissionError(f"{filt}: tvilling af {tvillinger[0][0]} (overlap {tvillinger[0][1]:.2f}, "
                              f"status {tvillinger[0][2]}) - samme familie, må ikke åbnes")
    return "frosset"


for filt in ("F0200", "F0300"):
    try:
        udfald.append((f"T1 frys 1 af {filt}", frys_1(filt, "LANG")
                       + f" (overlap med F0069 = {overlap(serier[filt], f69):.2f})"))
    except PermissionError as e:
        udfald.append((f"T1 frys 1 af {filt}", "afvist: " + str(e)))

# ---------- T2: én runde, blinde tal ----------
con.execute("INSERT INTO oos_runde VALUES (1, 'regler_v007', true, false)")
con.execute("INSERT INTO aabning VALUES (1, 'F0300', 'LANG'), (1, 'F0400', 'KORT')")
con.execute("INSERT INTO resultat VALUES ('F0300','LANG', 1234, true), ('F0400','KORT', -50, false)")
udfald.append(("T2 tal synlige mens runden er åben", f"{len(con.execute('SELECT * FROM dom_synlig').fetchall())} rækker"))
udfald.append(("T2 blind dom mens runden er åben", str(con.execute('SELECT * FROM dom_blind').fetchall())))
con.execute("UPDATE oos_runde SET lukket = true WHERE runde_id = 1")   # (i PostgreSQL: kun-indsæt-hændelse)
udfald.append(("T2 tal synlige efter lukning", f"{len(con.execute('SELECT * FROM dom_synlig').fetchall())} rækker"))


def aabn_i_runde(runde_id, filt, retning):
    lukket = con.execute("SELECT lukket FROM oos_runde WHERE runde_id=?", [runde_id]).fetchone()[0]
    if lukket:
        raise PermissionError("OOS-runden er lukket; ny familie skal vente på en ny, uset periode EFTER 2026 (2026 er embargo)")
    con.execute("INSERT INTO aabning VALUES (?,?,?)", [runde_id, filt, retning])


try:
    aabn_i_runde(1, "F0500", "LANG")
    udfald.append(("T2 ny familie efter lukning", "ÅBNET - problem!"))
except PermissionError as e:
    udfald.append(("T2 ny familie efter lukning", "afvist: " + str(e)))

for navn, tekst in udfald:
    print(f"{navn:40s} {tekst}")
