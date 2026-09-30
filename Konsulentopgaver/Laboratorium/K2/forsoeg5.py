"""
forsoeg5.py -- F10: Virker lokkedue-FDR-maskinen? KUN OPDIGTEDE DATA.
12 uafhængige opdigtede 'filtre' (hver på sin egen opdigtede prisserie, så sandheden er kendt).
3 af dem har en plantet edge i et 7x7-område; 9 er ren støj.
Vi kører porten (t >= T og PL >= P) på de ægte signaler og på 20 runder lokkeduer
og sammenligner K1's FDR-skøn (lokkeduer pr. runde / ægte beståede) med den SANDE andel falske.
Tælles både pr. celle og pr. sammenhængende gruppe (K1's repræsentant-enhed).
"""

import time

import numpy as np
from scipy import ndimage

import rsa_proto as rp
from forsoeg import BAR, HORISONT, N1, N2, celle_resultater, skriv, us_helligdage
from forsoeg2 import plant_delvis

KRAV = [(2.0, 1), (2.5, 1), (2.0, 3), (3.0, 3)]      # (T, mindste plateau-niveau)
PLANTET = {0: 1.0, 4: 0.6, 8: 0.35}                  # filter -> andel af signaler med +1 tick
import sys
MIDLERTIDIG = "--midlertidig" in sys.argv   # F10b: plantet edge uden varig drift


def dom(r):
    NOK = (r["dage"] >= 150) & (r["n"] >= 300)
    pl = rp.plateau_gitter(r["m"], r["t"], NOK)
    ud = {}
    for T, P in KRAV:
        b = (r["t"] >= T) & (pl >= P) & NOK
        _, grupper = ndimage.label(b)
        ud[(T, P)] = (int(b.sum()), int(grupper))
    return ud


def main():
    t0 = time.time()
    kal = rp.lav_kalender("2020-01-01", "2024-12-31", helligdage=us_helligdage())
    rng = np.random.default_rng(2026)
    filtre = []
    for f in range(12):
        # ingen trenddage her: ellers har "støj"-filtrene en ægte (opdigtet) momentum-edge, og sandheden bliver uklar
        md = rp.lav_minutdata(kal, seed=100 + f, sigma=2.0, uro_klumper=True)
        bars = rp.byg_bars(md, kal, BAR)
        sig = rp.lav_signaler(bars, N1, N2)
        if f in PLANTET:
            r0, ev = celle_resultater(md, sig, HORISONT)
            region = (sig.n1_idx >= 9) & (sig.n1_idx <= 15) & (sig.n2_idx >= 9) & (sig.n2_idx <= 15)
            md = plant_delvis(md, ev.indgang_idx[region & ev.gyldig], PLANTET[f], seed=f, midlertidig=MIDLERTIDIG)
        filtre.append((md, bars, sig))
    skriv(f"F10{'b (midlertidig edge, ingen drift)' if MIDLERTIDIG else ''}: 12 opdigtede filtre lavet ({time.time()-t0:.0f} s). Plantet: {PLANTET}")

    aegte = {k: np.zeros(12, dtype=int) for k in KRAV}
    aegte_g = {k: np.zeros(12, dtype=int) for k in KRAV}
    for f, (md, bars, sig) in enumerate(filtre):
        r, _ = celle_resultater(md, sig, HORISONT)
        d = dom(r)
        for k in KRAV:
            aegte[k][f], aegte_g[k][f] = d[k]
        skriv(f"  filter {f:2d} {'(plantet)' if f in PLANTET else '(støj)   '}: t midte {r['t'][12,12]:+.1f}, "
              + ", ".join(f"T>={T},PL>={P}: {d[(T,P)][0]} celler/{d[(T,P)][1]} grp" for T, P in KRAV))

    RUNDER = 20
    lok = {k: [] for k in KRAV}
    lok_g = {k: [] for k in KRAV}
    for runde in range(RUNDER):
        s_c = {k: 0 for k in KRAV}; s_g = {k: 0 for k in KRAV}
        for f, (md, bars, sig) in enumerate(filtre):
            w = int(rng.integers(4, 27))
            ny, ok, _, _ = rp.lokkedue_forskyd(sig.starttid, kal, bars.stempel, w, "kalenderuger")
            s2 = rp.Signaler(sig.n1_idx[ok], sig.n2_idx[ok], ny[ok], sig.antal_bars[ok], sig.afsluttet[ok])
            r, _ = celle_resultater(md, s2, HORISONT)
            d = dom(r)
            for k in KRAV:
                s_c[k] += d[k][0]; s_g[k] += d[k][1]
        for k in KRAV:
            lok[k].append(s_c[k]); lok_g[k].append(s_g[k])
    skriv(f"\n  Lokkeduer: {RUNDER} runder x 12 filtre ({time.time()-t0:.0f} s i alt)")
    stoej = np.array([f not in PLANTET for f in range(12)])
    for k in KRAV:
        T, P = k
        for navn, a, l in (("celler", aegte[k], lok[k]), ("grupper", aegte_g[k], lok_g[k])):
            besta = a.sum()
            falske = a[stoej].sum()
            l = np.array(l)
            fdr_sand = falske / besta if besta else float("nan")
            fdr_skoen = l.mean() / besta if besta else float("nan")
            skriv(f"  T>={T}, PL>={P}, {navn:7s}: ægte beståede {besta:4d} (heraf fra støj-filtre {falske:3d}) | "
                  f"SAND andel falske {fdr_sand:.2f} | lokkedue-skøn {fdr_skoen:.2f} "
                  f"(lokkeduer pr. runde: middel {l.mean():.1f}, spredning {l.std():.1f}, maks {l.max()})")


if __name__ == "__main__":
    main()
