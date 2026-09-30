"""forsoeg3.py -- F8: hvor meget deler nabo-celler signaler, og hvor lander 'repræsentanten'? KUN OPDIGTEDE DATA."""
import numpy as np
from scipy import ndimage
import rsa_proto as rp
from forsoeg import BAR, HORISONT, N1, N2, celle_resultater, plant_edge, skriv, us_helligdage

kal = rp.lav_kalender("2020-01-01", "2024-12-31", helligdage=us_helligdage())
md = rp.lav_minutdata(kal, seed=21, sigma=2.0, uro_klumper=True, mangler=0.002)
bars = rp.byg_bars(md, kal, BAR)
sig = rp.lav_signaler(bars, N1, N2)
def tider(i, j):
    return set(sig.starttid[(sig.n1_idx == i) & (sig.n2_idx == j)].tolist())
skriv("=== F8a: Andel fælles signaltider mellem midten (12,12) og en nabo (Jaccard) ===")
a = tider(12, 12)
for d in (1, 2, 3, 6, 12):
    for (i, j) in ((12 + d, 12), (12, 12 + d)):
        if i < 25 and j < 25:
            b = tider(i, j)
            skriv(f"  afstand {d:2d} ({'N1' if i != 12 else 'N2'}): {len(a & b) / len(a | b):.2f}")
skriv("=== F8b: Plantet edge (x=2) kun i 7x7 omkring (12,12): hvilken celle bliver repræsentant? ===")
r0, ev = celle_resultater(md, sig, HORISONT)
region = (sig.n1_idx >= 9) & (sig.n1_idx <= 15) & (sig.n2_idx >= 9) & (sig.n2_idx <= 15)
md_p = plant_edge(md, ev.indgang_idx[region & ev.gyldig], 2, 60, seed=2)
r, _ = celle_resultater(md_p, sig, HORISONT)
NOK = (r["dage"] >= 150) & (r["n"] >= 300)
pl = rp.plateau_gitter(r["m"], r["t"], NOK)
bestaar = (r["t"] >= 4) & (pl >= 3)
lab, ng = ndimage.label(bestaar)        # side-mod-side-naboskab
skriv(f"  beståede celler: {bestaar.sum()} i {ng} sammenhængende gruppe(r)")
for g in range(1, ng + 1):
    idx = np.argwhere(lab == g)
    midt = idx.mean(axis=0)
    rep = idx[np.argmin(((idx - midt) ** 2).sum(axis=1))]
    skriv(f"  gruppe {g}: {len(idx)} celler, geometrisk midte ({midt[0]:.1f},{midt[1]:.1f}), repræsentant {tuple(rep)}; "
          f"plantet midte var (12,12); højeste t i gruppen: {tuple(idx[np.argmax(r['t'][lab == g])])}")
