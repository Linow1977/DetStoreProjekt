"""forsoeg7.py -- F12 (= test T11c): en edge, der kun findes i 2020-2021, skal afvises af tid-stabilitet (K1's B5),
mens samme edge over hele perioden skal bestå B5. KUN OPDIGTEDE DATA."""
import numpy as np
import rsa_proto as rp
from forsoeg import BAR, HORISONT, N1, N2, skriv, us_helligdage
from forsoeg2 import plant_delvis

def b5(md, kal, sig, celle_nr):
    """K1 B5 for én celle: netto > 0 i >= 4 af 5 år og >= 12 af 20 kvartaler; bedste år <= 40 % af nettogevinsten."""
    ev = rp.event_motor(md, sig.starttid, HORISONT)
    c = sig.n1_idx.astype(np.int64) * 25 + sig.n2_idx
    v = ev.gyldig & (c == celle_nr)
    dato = kal.handelsdage[ev.dag[v]]
    aar = dato.astype("datetime64[Y]").astype(int) + 1970
    kvt = (aar - 2020) * 4 + (dato.astype("datetime64[M]").astype(int) % 12) // 3
    x = ev.brutto[v].astype(np.int64)
    pr_aar = np.array([x[aar == a].sum() for a in range(2020, 2025)])
    pr_kvt = np.array([x[kvt == q].sum() for q in range(20)])
    total = x.sum()
    bedste_andel = pr_aar.max() / total if total > 0 else np.inf
    ok = (np.sum(pr_aar > 0) >= 4) and (np.sum(pr_kvt > 0) >= 12) and (bedste_andel <= 0.40)
    return ok, np.sum(pr_aar > 0), np.sum(pr_kvt > 0), bedste_andel, total / v.sum()

kal = rp.lav_kalender("2020-01-01", "2024-12-31", helligdage=us_helligdage())
md = rp.lav_minutdata(kal, seed=21, sigma=2.0, uro_klumper=True, mangler=0.002)
bars = rp.byg_bars(md, kal, BAR)
sig = rp.lav_signaler(bars, N1, N2)
ev = rp.event_motor(md, sig.starttid, HORISONT)
region = (sig.n1_idx >= 9) & (sig.n1_idx <= 15) & (sig.n2_idx >= 9) & (sig.n2_idx <= 15) & ev.gyldig
foer_2022 = kal.handelsdage[ev.dag] < np.datetime64("2022-01-01")
for navn, maske in (("edge HELE perioden", region), ("edge KUN 2020-2021", region & foer_2022)):
    mdp = plant_delvis(md, ev.indgang_idx[maske], 1.0, seed=7)
    ok, a, q, andel, m = b5(mdp, kal, sig, 12 * 25 + 12)
    skriv(f"F12 {navn:20s}: celle (12,12) netto/signal {m:.2f} ticks; positive år {a}/5, positive kvartaler {q}/20, "
          f"bedste år = {andel:.0%} af gevinsten -> B5 {'BESTÅET' if ok else 'AFVIST'}")
