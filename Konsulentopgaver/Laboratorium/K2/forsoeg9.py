"""forsoeg9.py -- F14: fanger 'identiske celler'-kontrollen et gitter, hvor seriefunktions-fejlen har gjort alle
celler ens (eller én parameter virkningsløs)? Og hvad sker der med plateau-trappen, hvis kontrollen mangler?
KUN OPDIGTEDE DATA."""
import numpy as np
import rsa_proto as rp
from forsoeg import BAR, HORISONT, N1, N2, celle_resultater, skriv, us_helligdage
from forsoeg2 import plant_delvis

kal = rp.lav_kalender("2020-01-01", "2024-12-31", helligdage=us_helligdage())
md = rp.lav_minutdata(kal, seed=21, sigma=2.0, uro_klumper=True, mangler=0.002)
bars = rp.byg_bars(md, kal, BAR)
sig = rp.lav_signaler(bars, N1, N2)
def kopier(sig, maske_kilde, hvordan):
    """Byg et 'fejlramt' gitter: 'alle' = cellen (12,12)'s signaler i alle 625 celler;
    'n2' = N2 gør ingen forskel (hver N1-række får signalerne fra N2-indeks 12)."""
    ud = {k: [] for k in ("n1", "n2", "t", "ab", "af")}
    for i in range(25):
        for j in range(25):
            ki, kj = (12, 12) if hvordan == "alle" else (i, 12)
            m = (sig.n1_idx == ki) & (sig.n2_idx == kj)
            ud["n1"].append(np.full(m.sum(), i, np.int16)); ud["n2"].append(np.full(m.sum(), j, np.int16))
            ud["t"].append(sig.starttid[m]); ud["ab"].append(sig.antal_bars[m]); ud["af"].append(sig.afsluttet[m])
    return rp.Signaler(*(np.concatenate(ud[k]) for k in ("n1", "n2", "t", "ab", "af")))
ev = rp.event_motor(md, sig.starttid, HORISONT)
for navn, s in (("gyldigt filter", sig), ("fejl: alle celler ens", kopier(sig, None, "alle")),
                ("fejl: N2 virker ikke", kopier(sig, None, "n2"))):
    k = rp.gitter_kontrol(s)
    # plant en lille, drift-fri edge efter signalerne i cellen (12,12) og se, hvad plateau-trappen siger
    s12 = (sig.n1_idx == 12) & (sig.n2_idx == 12) & ev.gyldig
    mdp = plant_delvis(md, ev.indgang_idx[s12], 1.0, seed=5, midlertidig=True)
    mdp = plant_delvis(mdp, ev.indgang_idx[s12], 1.0, seed=6, midlertidig=True)
    r, _ = celle_resultater(mdp, s, HORISONT)
    NOK = (r["dage"] >= 150) & (r["n"] >= 300)
    pl = rp.plateau_gitter(r["m"], r["t"], NOK)
    skriv(f"F14 {navn:22s}: helt ens nabo-par langs N1 {k['ens_langs_n1']:.2f}, langs N2 {k['ens_langs_n2']:.2f}; "
          f"forskellige signal-lister {k['forskellige_lister']}/{k['celler']}; fjerne celler min. lighed {k['fjerne_min_lighed']:.2f}; dom: {rp.gitter_dom(k) or 'gyldigt'}; "
          f"med 2 ticks plantet i (12,12): midten PL{pl[12,12]}, celler med PL7: {int((pl==7).sum())}")
