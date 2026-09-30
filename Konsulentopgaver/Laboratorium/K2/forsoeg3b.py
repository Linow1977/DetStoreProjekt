"""forsoeg3b.py -- F3/F3b/F8b gentaget med en MIDLERTIDIG plantet edge (ingen varig drift i prisserien).
Adskiller ægte 'smitte' via fælles signaler fra en generel opadgående drift. KUN OPDIGTEDE DATA."""
import numpy as np
from scipy import ndimage
import rsa_proto as rp
from forsoeg import BAR, HORISONT, N1, N2, celle_resultater, skriv, us_helligdage
from forsoeg2 import plant_delvis

kal = rp.lav_kalender("2020-01-01", "2024-12-31", helligdage=us_helligdage())
md = rp.lav_minutdata(kal, seed=21, sigma=2.0, uro_klumper=True, mangler=0.002)
bars = rp.byg_bars(md, kal, BAR)
sig = rp.lav_signaler(bars, N1, N2)
r0, ev = celle_resultater(md, sig, HORISONT)
region = (sig.n1_idx >= 9) & (sig.n1_idx <= 15) & (sig.n2_idx >= 9) & (sig.n2_idx <= 15)
inde = np.zeros((25, 25), bool); inde[9:16, 9:16] = True
rng = np.random.default_rng(0)
st = rng.choice(md.stempel[:-200], 20000)
for andel in (0.2, 0.5, 1.0):
    mdp = plant_delvis(md, ev.indgang_idx[region & ev.gyldig], andel, seed=3, midlertidig=True)
    e2 = rp.event_motor(mdp, st, HORISONT); drift = e2.brutto[e2.gyldig].mean()
    r, _ = celle_resultater(mdp, sig, HORISONT)
    d = r["m"] - r0["m"]
    NOK = (r["dage"] >= 150) & (r["n"] >= 300)
    pl = rp.plateau_gitter(r["m"], r["t"], NOK)
    b = (r["t"] >= 4) & (pl >= 3)
    lab, ng = ndimage.label(b)
    rep = "-"
    if ng:
        g = np.bincount(lab.ravel())[1:].argmax() + 1
        idx = np.argwhere(lab == g); midt = idx.mean(axis=0)
        rep = tuple(int(v) for v in idx[np.argmin(((idx - midt) ** 2).sum(axis=1))])
        hoejest_t = tuple(int(v) for v in idx[np.argmax(r["t"][lab == g])])
    skriv(f"F3c andel {andel:.1f} (midlertidig): ubetinget drift {drift:+.2f} ticks/60 min; stigning i netto/signal inde "
          f"{np.median(d[inde]):.2f}, uden for {np.median(d[~inde]):.2f}; t midte {r['t'][12,12]:.1f}; "
          f"t>=4 & PL>=3: inde {int(b[inde].sum())}/49, uden for {int(b[~inde].sum())}/576, grupper {ng}; "
          f"repræsentant {rep}" + (f", højeste t {hoejest_t}" if ng else ""))

# Stærkere midlertidige edges: læg +1/-1 ind k gange (k ticks pr. signal), stadig uden varig drift
for k in (2, 4):
    mdp = md
    for j in range(k):
        mdp = plant_delvis(mdp, ev.indgang_idx[region & ev.gyldig], 1.0, seed=10 + j, midlertidig=True)
    e2 = rp.event_motor(mdp, st, HORISONT); drift = e2.brutto[e2.gyldig].mean()
    r, _ = celle_resultater(mdp, sig, HORISONT)
    d = r["m"] - r0["m"]
    NOK = (r["dage"] >= 150) & (r["n"] >= 300)
    pl = rp.plateau_gitter(r["m"], r["t"], NOK)
    b = (r["t"] >= 4) & (pl >= 3)
    lab, ng = ndimage.label(b)
    rep = hoejest_t = "-"
    if ng:
        g = np.bincount(lab.ravel())[1:].argmax() + 1
        idx = np.argwhere(lab == g); midt = idx.mean(axis=0)
        rep = tuple(int(v) for v in idx[np.argmin(((idx - midt) ** 2).sum(axis=1))])
        hoejest_t = tuple(int(v) for v in idx[np.argmax(r["t"][lab == g])])
    skriv(f"F3c k={k} ticks (midlertidig): drift {drift:+.2f}; stigning inde {np.median(d[inde]):.2f}, uden for {np.median(d[~inde]):.2f}; "
          f"t midte {r['t'][12,12]:.1f}; midte PL{pl[12,12]}; t>=4 & PL>=3: inde {int(b[inde].sum())}/49, uden for {int(b[~inde].sum())}/576, "
          f"grupper {ng}; største gruppes repræsentant {rep}, højeste t {hoejest_t}")
