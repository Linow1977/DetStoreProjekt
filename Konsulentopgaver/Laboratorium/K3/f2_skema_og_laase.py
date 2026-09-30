"""
Forsøg F2 (K3): Holder låsene i skemaet?

Spørgsmål:
  T1  Afviser test-laget en opdigtet 2025-række (CHECK-regel)?
  T2  Afviser indlæseren HELE filen, hvis én linje ligger i 2025, uden at
      efterlade rækker eller filer?
  T3  Kan engangsporten åbnes to gange for samme familie (filter x retning),
      også via en "nabo-celle"? Kan en anden familie stadig åbnes?
  T4  Kræver genstart efter nedbrud i OOS en godkendelse?
  T5  Tælle-tabellen: bliver et halvt skrevet parti rullet helt tilbage?

Opsætning: DuckDB som stand-in for PostgreSQL. DuckDB har CHECK, PRIMARY KEY,
UNIQUE og transaktioner, men IKKE roller/GRANT, triggere eller SECURITY
DEFINER-funktioner. Det, der i PostgreSQL ligger i en funktion, ligger her i
en Python-funktion med samme logik. Kun opdigtede data.
"""
import os
import shutil
import duckdb
import pandas as pd

MAPPE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "f2_ud")
shutil.rmtree(MAPPE, ignore_errors=True)
os.makedirs(MAPPE)
con = duckdb.connect(os.path.join(MAPPE, "tdb_legetoej.duckdb"))

SKEMA = """
CREATE SCHEMA kerne; CREATE SCHEMA pris_test; CREATE SCHEMA pris_oos;
CREATE SCHEMA taelle; CREATE SCHEMA port; CREATE SCHEMA katalog;

CREATE TABLE kerne.periode (
    profil TEXT, navn TEXT, opvarmning_start DATE, foerste_taellende DATE, sidste_dag DATE,
    PRIMARY KEY (profil, navn));
INSERT INTO kerne.periode VALUES
  ('RIGTIG','TEST',   DATE '2019-10-01', DATE '2020-01-02', DATE '2024-12-13'),
  ('RIGTIG','OOS',    DATE '2024-10-01', DATE '2025-01-02', DATE '2025-12-12'),
  ('RIGTIG','EMBARGO',DATE '2025-10-01', DATE '2026-01-02', DATE '2099-12-31');

CREATE TABLE pris_test.bar_1min (
    symbol TEXT NOT NULL, tidsstempel TIMESTAMP NOT NULL, handelsdato DATE NOT NULL,
    luk INTEGER NOT NULL,
    PRIMARY KEY (symbol, tidsstempel),
    CONSTRAINT kun_testperiode CHECK (handelsdato BETWEEN DATE '2019-10-01' AND DATE '2024-12-13'));

CREATE TABLE katalog.fil (
    job_id INTEGER PRIMARY KEY, sti TEXT NOT NULL, raekker BIGINT NOT NULL, sha256 TEXT NOT NULL);

CREATE TABLE taelle.test (
    koersel_id INTEGER, fast_filter_id TEXT, n1 INTEGER, n2 INTEGER, retning TEXT,
    er_kontrol BOOLEAN NOT NULL, resultat TEXT NOT NULL);

CREATE TABLE port.frys (
    frys_id INTEGER PRIMARY KEY, port TEXT CHECK (port IN ('OOS','EMBARGO')),
    familie_noegle TEXT NOT NULL, pakke_hash TEXT NOT NULL UNIQUE);
CREATE TABLE port.aabning (
    aabning_id INTEGER PRIMARY KEY, port TEXT NOT NULL, frys_id INTEGER NOT NULL,
    familie_noegle TEXT NOT NULL, antal_aegte BIGINT NOT NULL, antal_kontrol BIGINT NOT NULL,
    CONSTRAINT kun_en_gang UNIQUE (port, familie_noegle));
CREATE TABLE port.forsoeg (
    aabning_id INTEGER NOT NULL, nr INTEGER NOT NULL, haendelse TEXT NOT NULL,
    godkendt_af TEXT,
    PRIMARY KEY (aabning_id, nr),
    CONSTRAINT genstart_kraever_navn CHECK (haendelse <> 'GENSTART_GODKENDT' OR godkendt_af IS NOT NULL));
"""
con.execute(SKEMA)
udfald = []


def forventet_fejl(navn, sql_eller_funktion):
    """Kør noget, der SKAL fejle. Returner fejlteksten eller 'INGEN FEJL (problem!)'."""
    try:
        if callable(sql_eller_funktion):
            sql_eller_funktion()
        else:
            con.execute(sql_eller_funktion)
        udfald.append((navn, "INGEN FEJL - låsen holdt IKKE"))
    except Exception as e:  # noqa: BLE001 - vi vil netop se fejlen
        try:
            con.execute("ROLLBACK")      # hvis en transaktion stod åben
        except Exception:  # noqa: BLE001 - ingen åben transaktion
            pass
        udfald.append((navn, "afvist: " + str(e).splitlines()[0][:110]))


# ---------- T1: 2025-række direkte i test-laget ----------
con.execute("INSERT INTO pris_test.bar_1min VALUES ('SYM', TIMESTAMP '2024-12-12 10:00', DATE '2024-12-12', 100)")
forventet_fejl("T1 2025-række i pris_test",
               "INSERT INTO pris_test.bar_1min VALUES ('SYM', TIMESTAMP '2025-01-03 10:00', DATE '2025-01-03', 101)")
forventet_fejl("T1b buffer-række (2024-12-20) i pris_test",
               "INSERT INTO pris_test.bar_1min VALUES ('SYM', TIMESTAMP '2024-12-20 10:00', DATE '2024-12-20', 101)")


# ---------- T2: indlæseren afviser hele filen ----------
def indlaes_signalfil(job_id, csv_sti, profil="RIGTIG", periode="TEST"):
    """Stand-in for indlæseren: tjek -> midlertidig fil -> flyt -> katalog (i én transaktion)."""
    graense = con.execute("SELECT foerste_taellende, sidste_dag FROM kerne.periode WHERE profil=? AND navn=?",
                          [profil, periode]).fetchone()
    df = pd.read_csv(csv_sti, names=["runid", "n1", "n2", "starttid", "antalbars", "afsluttet"],
                     parse_dates=["starttid"])
    efter = df[df["starttid"].dt.date > graense[1]]
    if len(efter) > 0:
        raise ValueError(f"job {job_id}: {len(efter)} linje(r) efter {graense[1]} - hele filen afvist")
    df = df[df["starttid"].dt.date >= graense[0]]           # opvarmning smides bevidst væk
    endelig = os.path.join(MAPPE, "arkiv", periode.lower(), "signaler", f"job={job_id:06d}.parquet")
    midlertidig = endelig + ".tmp"
    os.makedirs(os.path.dirname(endelig), exist_ok=True)
    df.to_parquet(midlertidig, index=False)
    os.replace(midlertidig, endelig)
    con.execute("INSERT INTO katalog.fil VALUES (?, ?, ?, 'x')", [job_id, endelig, len(df)])


god = os.path.join(MAPPE, "god.csv")
ond = os.path.join(MAPPE, "ond.csv")
with open(god, "w") as f:
    f.write("RawSignal069,10,5,2020-03-15 10:45,4,1\nRawSignal069,10,5,2024-12-13 09:05,2,1\n")
with open(ond, "w") as f:
    f.write("RawSignal069,10,5,2020-03-15 10:45,4,1\nRawSignal069,10,5,2025-01-06 09:05,2,1\n")
indlaes_signalfil(1, god)
forventet_fejl("T2 signalfil med én 2025-linje", lambda: indlaes_signalfil(2, ond))
filer_job2 = [f for f in os.listdir(os.path.join(MAPPE, "arkiv", "test", "signaler")) if "000002" in f]
katalog_job2 = con.execute("SELECT count(*) FROM katalog.fil WHERE job_id = 2").fetchone()[0]
udfald.append(("T2 efterladt af job 2", f"{len(filer_job2)} filer, {katalog_job2} katalog-rækker"))


# ---------- T3: engangsporten ----------
def aabn_port(port_navn, frys_id):
    """Samme logik som port.aabn() i del3_K3.md afs. 7.5 (dér som SECURITY DEFINER-funktion)."""
    con.execute("BEGIN")
    fam = con.execute("SELECT familie_noegle FROM port.frys WHERE frys_id=? AND port=?",
                      [frys_id, port_navn]).fetchone()[0]
    aegte, kontrol = con.execute(
        "SELECT count(*) FILTER (WHERE NOT er_kontrol), count(*) FILTER (WHERE er_kontrol) FROM taelle.test").fetchone()
    ny_id = con.execute("SELECT coalesce(max(aabning_id),0)+1 FROM port.aabning").fetchone()[0]
    con.execute("INSERT INTO port.aabning VALUES (?,?,?,?,?,?)", [ny_id, port_navn, frys_id, fam, aegte, kontrol])
    con.execute("INSERT INTO port.forsoeg VALUES (?, 1, 'STARTET', NULL)", [ny_id])
    con.execute("COMMIT")
    return ny_id


con.execute("INSERT INTO taelle.test VALUES (1,'F0069',10,5,'LANG',false,'BESTAAET'), (1,'F0069',10,5,'LANG',true,'IKKE_BESTAAET')")
con.execute("INSERT INTO port.frys VALUES (1,'OOS','F0069|LANG','hash-a'), (2,'OOS','F0069|LANG','hash-b-nabo'), (3,'OOS','F0070|LANG','hash-c')")
a1 = aabn_port("OOS", 1)
udfald.append(("T3 første åbning F0069|LANG", f"åbnet (id {a1}); snapshot ægte/kontrol = "
               + str(con.execute('SELECT antal_aegte, antal_kontrol FROM port.aabning WHERE aabning_id=?', [a1]).fetchone())))
forventet_fejl("T3 samme parti igen", lambda: aabn_port("OOS", 1))
forventet_fejl("T3 nabo-celle i samme familie (ny frys)", lambda: aabn_port("OOS", 2))
a3 = aabn_port("OOS", 3)
udfald.append(("T3 anden familie F0070|LANG", f"åbnet (id {a3}) - som det skal"))


# ---------- T3c: bagdør via stavemåde af familie-nøglen ----------
# Familie-nøglen er her en fritekst. Hvad hvis nogen skriver den en smule anderledes?
con.execute("INSERT INTO port.frys VALUES (4,'OOS','F0069|lang','hash-d-stavefejl')")
try:
    a4 = aabn_port("OOS", 4)
    udfald.append(("T3c samme familie, anden stavemåde", f"ÅBNET (id {a4}) - BAGDØR! låsen holdt ikke"))
except Exception as e:  # noqa: BLE001
    con.execute("ROLLBACK")
    udfald.append(("T3c samme familie, anden stavemåde", "afvist"))

# (DuckDB: fremmednøgle kun inden for samme skema; i PostgreSQL ligger tabellen i kerne.)
# Rettelse: nøglen bygges af to felter med faste værdier og henvisning til filter-identiteten.
con.execute("""
CREATE TABLE port.filter_identitet (fast_filter_id TEXT PRIMARY KEY, definition_hash TEXT NOT NULL UNIQUE);
INSERT INTO port.filter_identitet VALUES ('F0069','h69'), ('F0070','h70');
CREATE TABLE port.aabning_v2 (
    aabning_id INTEGER PRIMARY KEY, port TEXT NOT NULL CHECK (port IN ('OOS','EMBARGO')),
    fast_filter_id TEXT NOT NULL REFERENCES port.filter_identitet(fast_filter_id),
    retning TEXT NOT NULL CHECK (retning IN ('LANG','KORT')),
    CONSTRAINT kun_en_gang UNIQUE (port, fast_filter_id, retning));
INSERT INTO port.aabning_v2 VALUES (1,'OOS','F0069','LANG');
""")
forventet_fejl("T3d rettet: 'lang' med lille",
               "INSERT INTO port.aabning_v2 VALUES (2,'OOS','F0069','lang')")
forventet_fejl("T3d rettet: ukendt filter 'F069'",
               "INSERT INTO port.aabning_v2 VALUES (3,'OOS','F069','LANG')")
forventet_fejl("T3d rettet: samme familie igen",
               "INSERT INTO port.aabning_v2 VALUES (4,'OOS','F0069','LANG')")

# ---------- T4: genstart efter nedbrud ----------
con.execute("INSERT INTO port.forsoeg VALUES (?, 2, 'NEDBRUD', NULL)", [a1])
forventet_fejl("T4 genstart uden godkender", f"INSERT INTO port.forsoeg VALUES ({a1}, 3, 'GENSTART_GODKENDT', NULL)")
con.execute("INSERT INTO port.forsoeg VALUES (?, 3, 'GENSTART_GODKENDT', 'thomas')", [a1])
udfald.append(("T4 genstart med godkender", "tilladt og logget"))

# ---------- T5: halvt skrevet tælle-parti ----------
foer = con.execute("SELECT count(*) FROM taelle.test").fetchone()[0]
try:
    con.execute("BEGIN")
    con.execute("INSERT INTO taelle.test SELECT 2,'F0071',i,1,'LANG',false,'IKKE_BESTAAET' FROM range(1000) t(i)")
    raise RuntimeError("simuleret nedbrud midt i partiet")
except RuntimeError:
    con.execute("ROLLBACK")
efter = con.execute("SELECT count(*) FROM taelle.test").fetchone()[0]
udfald.append(("T5 tælle-rækker før/efter nedbrud", f"{foer} / {efter} (0 halve rækker tilbage)"))

print(f"{'Test':45s} Udfald")
for navn, tekst in udfald:
    print(f"{navn:45s} {tekst}")
