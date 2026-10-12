"""
pharos_proto.py -- Prototype af Pharos' beregningsmotor (pharos_udkast.md afsnit 7). KUN OPDIGTEDE DATA.

Den månedlige kørsel, trin for trin:
  1. klip data ved as-of-datoen (ingen fremtidsviden)
  2. fuldstændigheds-tjek (mangler en dag -> ingen liste, "kræver dig")
  3. nøgletal pr. strategi (nettotal, nuværende nedtur, placering i forventningsbåndet)
  4. status pr. strategi efter en regel-funktion (K1's regler sættes ind her; standarden er kun et EKSEMPEL)
  5. størrelse: kontrakter = gulv(kapital x risiko pr. strategi / værste nedtur pr. kontrakt)
  6. lofter pr. marked og pr. retning (skaler ned, gulv)
  7. samlet nedturs-loft: blok-bootstrap af porteføljens dagstal; skaler ned, til 99 %-nedturen er under loftet
  8. forslag + grund på dansk + fingeraftryk af input, regelfil og resultat
Alle beløb er HELE tal (øre pr. kontrakt pr. dag), så en genkørsel giver bit for bit samme resultat.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass

import numpy as np


class KraeverDig(Exception):
    """Data mangler eller er i uorden: Pharos laver ingen liste og beder Thomas se på det."""


@dataclass
class Strategi:
    sid: str
    marked: str
    retning: str              # "LANG" eller "KORT"
    vaerste_dagstab: int      # øre pr. kontrakt (positivt tal): værste dag i 2020-2024 (fødselsattest)
    dagstab99: int            # øre pr. kontrakt: 99 %-dagstab fra risiko-Monte-Carlo i frys 2
    forv_maaned: int          # forventet netto pr. måned pr. kontrakt (øre), frys 2
    sd_maaned: int            # forventet spredning af én måneds netto pr. kontrakt (øre), frys 2
    nedtur95: int             # forventningsbånd for nedtur pr. kontrakt (øre), frys 2
    nedtur99: int
    start: np.datetime64      # første dag i papir-serien (frysedato 2)
    status: str = "AKTIV"     # AKTIV, PAUSE, PENSIONERET

    @property
    def risikomaal(self) -> int:
        """K1's 5.1 pkt. 2: det største af værste dagstab og 99 %-dagstab (øre pr. kontrakt)."""
        return max(self.vaerste_dagstab, self.dagstab99)


STANDARD_REGLER = {
    "kapital": 100_000_000,            # øre (1 mio.)
    "risiko_pr_strategi": 0.005,        # f højst 0,5 % af kapitalen pr. strategi på en "værste dag" (K1 5.1 pkt. 2)
    "samlet_risiko": 0.10,              # ... og f højst 10 % / antal aktive strategier (K1 5.1 pkt. 2)
    "loft_pr_marked": 0.25,             # andel af risikobudgettet (K1 5.1 pkt. 3)
    "loft_pr_retning": 0.60,
    "loft_samlet_nedtur99": 1.0,        # valgfri skalering FØR måneden (5.2 pkt. 6); 1.0 = slået fra (ikke i K1's regler)
    "mc_runder": 2000,
    "mc_blok_dage": 20,
    "mc_froe": 12345,
}


def eksempel_regel(nt: dict, s: Strategi) -> tuple[str, str]:
    """KUN ET EKSEMPEL til tests. K1's rigtige regler (pharos_udkast afs. 4) sættes ind her."""
    if s.status == "PENSIONERET":
        return "PENSIONERET", "pensioneret er endeligt"
    if nt["nedtur"] > s.nedtur99:
        return "PENSIONER", f"nedtur {nt['nedtur']} over 99 %-båndet {s.nedtur99}"
    if nt["nedtur"] > s.nedtur95:
        return "PAUSE", f"nedtur {nt['nedtur']} over 95 %-båndet {s.nedtur95}"
    if s.status == "PAUSE":
        return "GENOPTAG", "nedtur igen inden for 95 %-båndet"
    return "BEHOLD", f"nedtur {nt['nedtur']} inden for båndet"


def noegletal(p: np.ndarray, s: Strategi) -> dict:
    """p = dagstal (øre pr. kontrakt) siden frys 2, til og med as-of."""
    kurve = np.cumsum(p, dtype=np.int64)
    top = np.maximum.accumulate(np.r_[0, kurve])[1:]
    nedtur = int((top - kurve)[-1]) if len(p) else 0
    maaneder = max(len(p) / 21.0, 1e-9)
    z = (int(kurve[-1]) - s.forv_maaned * maaneder) / (s.sd_maaned * np.sqrt(maaneder)) if len(p) else 0.0
    return {"netto_i_alt": int(kurve[-1]) if len(p) else 0, "nedtur": nedtur, "z_mod_forventning": round(float(z), 9)}


def portefoelje_nedtur99(P: np.ndarray, kontrakter: np.ndarray, runder: int, blok: int, froe: int) -> int:
    """99 %-fraktil af største nedtur i porteføljen, blok-bootstrap af hele dage (blokke af fast længde,
    cirkulært), fast frø -> samme tal hver gang."""
    dag = (kontrakter[:, None] * P).sum(axis=0).astype(np.int64)
    n = len(dag)
    rng = np.random.default_rng(froe)
    antal_blokke = int(np.ceil(n / blok))
    starter = rng.integers(0, n, size=(runder, antal_blokke))
    idx = (starter[:, :, None] + np.arange(blok)[None, None, :]) % n
    serie = dag[idx.reshape(runder, -1)[:, :n]]
    kurve = np.cumsum(serie, axis=1)
    top = np.maximum.accumulate(np.concatenate([np.zeros((runder, 1), np.int64), kurve], axis=1), axis=1)[:, 1:]
    stoerste = (top - kurve).max(axis=1)
    return int(np.sort(stoerste)[int(np.ceil(0.99 * runder)) - 1])


def koer_maaned(datoer: np.ndarray, P: np.ndarray, har: np.ndarray, strategier: list[Strategi],
                handelsdage: np.ndarray, as_of: np.datetime64, regler: dict = None, regel=eksempel_regel):
    """datoer: dagene i P (sorteret). P[i, d] = øre pr. kontrakt; har[i, d] = findes tallet.
    handelsdage: kalenderens handelsdage (til fuldstændigheds-tjekket)."""
    regler = dict(STANDARD_REGLER if regler is None else regler)
    # 1. ingen fremtidsviden
    brug = datoer <= as_of
    datoer, P, har = datoer[brug], P[:, brug], har[:, brug]
    forslag, aktive = [], []
    for i, s in enumerate(strategier):
        # 2. fuldstændighed siden frys 2
        skal = handelsdage[(handelsdage >= s.start) & (handelsdage <= as_of)]
        dage_s = datoer[har[i] & (datoer >= s.start)]
        if s.status != "PENSIONERET" and not np.array_equal(np.sort(dage_s), skal):
            raise KraeverDig(f"{s.sid}: {len(skal) - len(dage_s)} dag(e) mangler eller er i overskud før {as_of}")
        p = P[i, har[i] & (datoer >= s.start)].astype(np.int64)
        # 3.-4.
        nt = noegletal(p, s)
        handling, grund = regel(nt, s)
        forslag.append({"sid": s.sid, "handling": handling, "grund": grund, "noegletal": nt, "kontrakter": 0})
        if handling in ("BEHOLD", "GENOPTAG", "OPTAG"):
            aktive.append(i)
    # 5. størrelse: kontrakter = gulv(f x kapital / risikomål)
    K = regler["kapital"]
    f = min(regler["risiko_pr_strategi"], regler["samlet_risiko"] / max(len(aktive), 1))
    kontrakter = np.zeros(len(strategier), dtype=np.int64)
    for i in aktive:
        kontrakter[i] = int(K * f) // strategier[i].risikomaal
    # 6. lofter pr. marked og retning som andel af risikobudgettet
    #    (risikobudget = antal aktive strategier x f x kapital; fast, så det ikke skrumper under nedskæringen)
    budget = len(aktive) * int(K * f)
    for noegle, loft in (("marked", regler["loft_pr_marked"]), ("retning", regler["loft_pr_retning"])):
        for vaerdi in sorted({getattr(strategier[i], noegle) for i in aktive}):
            gruppe = [i for i in aktive if getattr(strategier[i], noegle) == vaerdi]
            risiko = sum(int(kontrakter[i]) * strategier[i].risikomaal for i in gruppe)
            graense = int(budget * loft)
            if risiko > graense:
                for i in gruppe:
                    kontrakter[i] = (int(kontrakter[i]) * graense) // risiko
    # 7. samlet nedturs-loft (sammenhæng mellem strategier kommer med via de fælles dage)
    graense = int(K * regler["loft_samlet_nedtur99"])
    Pfuld = np.where(har, P, 0).astype(np.int64)
    for _ in range(30):
        if kontrakter.sum() == 0:
            break
        dd99 = portefoelje_nedtur99(Pfuld, kontrakter, regler["mc_runder"], regler["mc_blok_dage"], regler["mc_froe"])
        if dd99 <= graense:
            break
        ny = (kontrakter * graense) // dd99
        kontrakter = np.where(ny == kontrakter, np.maximum(kontrakter - 1, 0), ny)
    else:
        raise KraeverDig("samlet nedturs-loft kunne ikke overholdes")
    for i, f in enumerate(forslag):
        f["kontrakter"] = int(kontrakter[i])
    # 8. fingeraftryk
    h = hashlib.sha256()
    h.update(np.ascontiguousarray(P).tobytes()); h.update(np.ascontiguousarray(har).tobytes())
    h.update(json.dumps(regler, sort_keys=True).encode()); h.update(str(as_of).encode())
    h.update(json.dumps(forslag, sort_keys=True).encode())
    return forslag, h.hexdigest()
