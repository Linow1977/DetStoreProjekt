"""
forsoeg.py -- Forsøg F1-F5 for Konsulent 2 (laboratoriet). KUN OPDIGTEDE DATA.
Kør:  <lab-venv>/bin/python forsoeg.py  > resultater.txt
Hvert forsøg: spørgsmål -> opsætning -> resultat (tal) -> betydning (skrives i del2_K2.md afsnit 12).
"""

import datetime as dt
import time

import numpy as np

import rsa_proto as rp

N1 = list(range(5, 30))      # 25 værdier (længde i bars)
N2 = list(range(1, 26))      # 25 værdier
BAR = 15
HORISONT = 60


def us_helligdage(aar_fra=2020, aar_til=2024):
    """Omtrentlige amerikanske børs-helligdage (nok til at teste ugedags-forskydning)."""
    ud = []
    def nte_ugedag(aar, md, ugedag, n):
        d = dt.date(aar, md, 1)
        while d.weekday() != ugedag:
            d += dt.timedelta(1)
        return d + dt.timedelta(7 * (n - 1))
    def sidste_ugedag(aar, md, ugedag):
        d = dt.date(aar, md + 1, 1) - dt.timedelta(1)
        while d.weekday() != ugedag:
            d -= dt.timedelta(1)
        return d
    paaske = {2020: dt.date(2020, 4, 10), 2021: dt.date(2021, 4, 2), 2022: dt.date(2022, 4, 15),
              2023: dt.date(2023, 4, 7), 2024: dt.date(2024, 3, 29)}   # langfredag
    for a in range(aar_fra, aar_til + 1):
        ud += [dt.date(a, 1, 1), nte_ugedag(a, 1, 0, 3), nte_ugedag(a, 2, 0, 3), paaske[a],
               sidste_ugedag(a, 5, 0), dt.date(a, 7, 4), nte_ugedag(a, 9, 0, 1),
               nte_ugedag(a, 11, 3, 4), dt.date(a, 12, 25)]
        if a >= 2022:
            ud.append(dt.date(a, 6, 19))
    return tuple(str(d) for d in ud if d.weekday() < 5)


def celle_resultater(md, sig, horisont, fejl=False, kun_lange=None, plant=None):
    ev = rp.event_motor(md, sig.starttid, horisont, fejl_indgang_paa_signalbar=fejl, bar_min=BAR)
    brug = ev.gyldig.copy()
    if kun_lange is not None:                       # BEVIDST FEJL: brug af AntalBars (fremtidsviden)
        brug &= sig.antal_bars >= kun_lange
    celle = sig.n1_idx.astype(np.int64) * 25 + sig.n2_idx
    r = rp.celle_tal(celle[brug], ev.dag[brug], ev.brutto[brug], 625)
    return {k: v.reshape(25, 25) for k, v in r.items()}, ev


def plant_edge(md, indgang_idx, x_ticks, varighed=60, seed=0):
    """Læg +x ticks ind i prisen fordelt over 'varighed' minutter efter hver indgang (hele ticks)."""
    rng = np.random.default_rng(seed)
    skub = np.zeros(len(md.luk), dtype=np.int64)
    for i in np.unique(indgang_idx):
        mins = i + np.sort(rng.choice(varighed, x_ticks, replace=False))
        mins = mins[mins < len(skub)]
        np.add.at(skub, mins, 1)
    kum = np.cumsum(skub)
    # skub[i] påvirker minut i's luk; åbningen af minut i påvirkes af alt før i
    kum_foer = np.r_[0, kum[:-1]]
    return rp.Minutdata(md.stempel, (md.aabn + kum_foer).astype(np.int32), (md.hoej + kum).astype(np.int32),
                        (md.lav + kum_foer).astype(np.int32), (md.luk + kum).astype(np.int32), md.dag, md.minut_nr)


def skriv(*a):
    print(*a, flush=True)


def main():
    t_alt = time.time()
    kal = rp.lav_kalender("2020-01-01", "2024-12-31", helligdage=us_helligdage())
    skriv(f"Kalender: {len(kal.handelsdage)} handelsdage 2020-2024 (opdigtet, uden sommertid)")

    # ------------------------------------------------------------------ F5 (del 1): tid for bars
    t0 = time.time()
    md = rp.lav_minutdata(kal, seed=21, sigma=2.0, uro_klumper=True, mangler=0.002)
    t_md = time.time() - t0
    t0 = time.time()
    alle_bars = {n: rp.byg_bars(md, kal, n) for n in range(5, 65, 5)}
    t_bars = time.time() - t0
    skriv(f"1-min bars: {len(md.stempel):,}  (lavet på {t_md:.1f} s); 12 barstørrelser bygget på {t_bars:.2f} s")
    bars = alle_bars[BAR]
    t0 = time.time()
    sig = rp.lav_signaler(bars, N1, N2)
    skriv(f"Signaler, 25x25 celler på {BAR}-min bars: {len(sig.starttid):,}  "
          f"({len(sig.starttid)/625:,.0f} pr. celle; lavet på {time.time()-t0:.1f} s)")

    # ------------------------------------------------------------------ F1: ren støj
    skriv("\n=== F1: Ren støj (tilfældig gang med klumpet uro). Hvad giver porten? ===")
    r, ev = celle_resultater(md, sig, HORISONT)
    t = r["t"][np.isfinite(r["t"])]
    tn = r["t_naiv"][np.isfinite(r["t_naiv"])]
    skriv(f"Dag-klynget t over 625 celler: middel {t.mean():+.2f}, spredning {t.std():.2f}, "
          f"andel |t|>=3: {np.mean(np.abs(t) >= 3):.3f}, største t: {t.max():.2f}")
    skriv(f"'Naivt' t (hvert signal uafhængigt): spredning {tn.std():.2f}, andel |t|>=3: {np.mean(np.abs(tn) >= 3):.3f}")
    pust = (r["t_naiv"] / r["t"])[np.isfinite(r["t"])]
    skriv(f"Pustefaktor (naivt t / dag-klynget t): median {np.median(pust):.2f}, 90%-fraktil {np.quantile(pust, .9):.2f}")
    skriv(f"Dage pr. celle: median {np.median(r['dage']):.0f}; signaler pr. celle: median {np.median(r['n']):.0f}")
    NOK = (r["dage"] >= 150) & (r["n"] >= 300)
    pl = rp.plateau_gitter(r["m"], r["t"], NOK)
    skriv(f"Plateau-niveauer på støj (lang retning): " +
          ", ".join(f"PL>={k}: {np.sum(pl >= k)}" for k in (1, 3, 5, 7)))
    pl_kort = rp.plateau_gitter(-r["m"], -r["t"], NOK)
    skriv(f"Plateau-niveauer på støj (kort retning): " +
          ", ".join(f"PL>={k}: {np.sum(pl_kort >= k)}" for k in (1, 3, 5, 7)))

    # ------------------------------------------------------------------ F2: kig ind i fremtiden
    skriv("\n=== F2: Fanger null-testen kig-ind-i-fremtiden? (samme støjdata) ===")
    rf, _ = celle_resultater(md, sig, HORISONT, fejl=True)
    tf = rf["t"][np.isfinite(rf["t"])]
    skriv(f"FEJL A (indgang på åbningen af den bar, der skabte signalet): middel t {tf.mean():+.1f}, "
          f"andel t>=3: {np.mean(tf >= 3):.3f}")
    for k in (2, 4):
        ra, _ = celle_resultater(md, sig, HORISONT, kun_lange=k)
        ta = ra["t"][np.isfinite(ra["t"])]
        skriv(f"FEJL B (kun signaler med AntalBars >= {k}, dvs. fremtidsviden): middel t {ta.mean():+.1f}, "
              f"andel t>=3: {np.mean(ta >= 3):.3f}")
    skriv("Rigtig motor (fra F1): middel t %+.2f, andel t>=3: %.3f" % (t.mean(), np.mean(t >= 3)))

    # ------------------------------------------------------------------ F3: plantet edge
    skriv("\n=== F3: Plantet edge. Finder kæden den, og kun den? ===")
    region = (sig.n1_idx >= 9) & (sig.n1_idx <= 15) & (sig.n2_idx >= 9) & (sig.n2_idx <= 15)   # 7x7, midte (12,12)
    ind = ev.indgang_idx[region & ev.gyldig]
    resultater_plant = {}
    for x in (2, 4):
        md_p = plant_edge(md, ind, x, 60, seed=x)
        rp_, ev_p = celle_resultater(md_p, sig, HORISONT)
        m0 = r["m"]
        d_m = rp_["m"] - m0                      # hvor meget cellens netto steg pga. plantningen
        inde = np.zeros((25, 25), bool); inde[9:16, 9:16] = True
        NOKp = (rp_["dage"] >= 150) & (rp_["n"] >= 300)
        plp = rp.plateau_gitter(rp_["m"], rp_["t"], NOKp)
        skriv(f"x = {x} ticks plantet pr. signal i 7x7-området (1-min støj sd ~2 ticks, 60-min sd ~{2*np.sqrt(60):.0f} ticks):")
        skriv(f"  stigning i netto pr. signal: inde i området median {np.median(d_m[inde]):.2f}, "
              f"uden for området median {np.median(d_m[~inde]):.2f} (smitter via fælles signaler)")
        skriv(f"  t i midten (12,12): {rp_['t'][12,12]:.1f}; t inde: median {np.median(rp_['t'][inde]):.1f}; "
              f"uden for: median {np.median(rp_['t'][~inde]):.1f}")
        skriv(f"  plateau: midten (12,12) når PL{plp[12,12]}; celler med PL>=3 inde {np.sum(plp[inde]>=3)}/49, "
              f"uden for {np.sum(plp[~inde]>=3)}/576")
        resultater_plant[x] = (rp_, plp)

    # ------------------------------------------------------------------ F4: lokkeduer
    skriv("\n=== F4: Lokkeduer (hele serien flyttet 4-26 kalenderuger, cirkulært) ===")
    rng = np.random.default_rng(99)
    ugedag = lambda d: (kal.handelsdage[d].astype("int64") - 4) % 7
    for metode in ("handelsdage", "kalenderuger"):
        ny, ok, d0, d1 = rp.lokkedue_forskyd(sig.starttid, kal, bars.stempel, 13, metode)
        skriv(f"  {metode:12s}: signaler beholdt {ok.mean():.3f}; ugedag ændret for {np.mean(ugedag(d0[ok]) != ugedag(d1[ok])):.3f}")
    t_lok = []
    pas_lok = {2: [], 3: [], 4: []}
    t0 = time.time()
    RUNDER = 20
    for runde in range(RUNDER):
        w = int(rng.integers(4, 27))
        ny, ok, _, _ = rp.lokkedue_forskyd(sig.starttid, kal, bars.stempel, w, "kalenderuger")
        s2 = rp.Signaler(sig.n1_idx[ok], sig.n2_idx[ok], ny[ok], sig.antal_bars[ok], sig.afsluttet[ok])
        o = np.argsort(s2.starttid, kind="stable")
        s2 = rp.Signaler(*(getattr(s2, f)[o] for f in ("n1_idx", "n2_idx", "starttid", "antal_bars", "afsluttet")))
        rl, _ = celle_resultater(md, s2, HORISONT)
        tl = rl["t"][np.isfinite(rl["t"])]
        t_lok.append(tl)
        NOKl = (rl["dage"] >= 150) & (rl["n"] >= 300)
        pll = rp.plateau_gitter(rl["m"], rl["t"], NOKl)
        for T in pas_lok:
            pas_lok[T].append(int(np.sum((rl["t"] >= T) & (pll >= 3))))
    t_runde = (time.time() - t0) / RUNDER
    alle = np.concatenate(t_lok)
    skriv(f"  {RUNDER} runder: lokkeduernes dag-klyngede t: middel {alle.mean():+.2f}, spredning {alle.std():.2f} "
          f"(skal være ~1); spredning af rundernes middel-t: {np.std([x.mean() for x in t_lok]):.2f}")
    for T in pas_lok:
        a = np.array(pas_lok[T])
        skriv(f"  Lokkeduer, der 'består' t>={T} OG PL>=3: pr. runde middel {a.mean():.1f}, "
              f"min {a.min()}, maks {a.max()}; runder med mindst én: {np.mean(a > 0):.2f}")
    for x, (rp_, plp) in resultater_plant.items():
        for T in (3, 4):
            skriv(f"  Ægte kørsel med plantet x={x}: celler der består t>={T} OG PL>=3: {int(np.sum((rp_['t'] >= T) & (plp >= 3)))}")
    skriv(f"  Tid pr. lokkedue-runde (625 celler, hele kæden inkl. plateau): {t_runde:.2f} s")

    # ------------------------------------------------------------------ F5: tid
    skriv("\n=== F5: Tid pr. trin og fremskrivning ===")
    gentag = 5
    t0 = time.time()
    for _ in range(gentag):
        ev5 = rp.event_motor(md, sig.starttid, HORISONT)
    t_ev = (time.time() - t0) / gentag
    celle = sig.n1_idx.astype(np.int64) * 25 + sig.n2_idx
    t0 = time.time()
    for _ in range(gentag):
        rp.celle_tal(celle[ev5.gyldig], ev5.dag[ev5.gyldig], ev5.brutto[ev5.gyldig], 625)
    t_ct = (time.time() - t0) / gentag
    t0 = time.time()
    rp.plateau_gitter(r["m"], r["t"], NOK)
    t_pl = time.time() - t0
    n = len(sig.starttid)
    pr_sig = (t_ev + t_ct) / n
    skriv(f"Event-motor: {t_ev:.2f} s for {n:,} signaler ({n/t_ev/1e6:.1f} mio. signaler/s, én horisont)")
    skriv(f"Celle-tal (dag-klynget): {t_ct:.2f} s ({n/t_ct/1e6:.1f} mio. signaler/s)")
    skriv(f"Plateau for ét 25x25-gitter (625 midter, ren Python-løkke): {t_pl:.2f} s")
    skriv(f"=> pr. signal pr. horisont: {pr_sig*1e9:.0f} ns (NumPy, én kerne, uden Numba)")
    for mia in (1, 5):
        tim = mia * 1e9 * 3 * pr_sig / 3600
        skriv(f"   {mia} mia. signaler x 3 horisonter: {tim:.1f} timer på én kerne ~ {tim/4:.1f} timer på 4 kerner")
    gitre = 1.8e6 / 625
    skriv(f"   1,8 mio. kandidater ~ {gitre:,.0f} gitre a 625 celler; plateau: {gitre*t_pl/3600:.1f} timer på én kerne")
    skriv(f"   Pr. lokkedue-runde: samme som én fuld kørsel; 50 runder = 50 x ovenstående")
    skriv(f"\nSamlet køretid for forsøgene: {time.time()-t_alt:.0f} s")


if __name__ == "__main__":
    main()
