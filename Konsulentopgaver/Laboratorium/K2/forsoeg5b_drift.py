"""Kontrol af F10: skaber den plantede edge en generel opadgående drift i hele prisserien?"""
import numpy as np
import rsa_proto as rp
from forsoeg import BAR, HORISONT, N1, N2, celle_resultater, us_helligdage
from forsoeg2 import plant_delvis
kal = rp.lav_kalender("2020-01-01", "2024-12-31", helligdage=us_helligdage())
for f, andel in ((0, 1.0), (8, 0.35), (1, 0.0)):
    md = rp.lav_minutdata(kal, seed=100 + f, sigma=2.0, uro_klumper=True)
    bars = rp.byg_bars(md, kal, BAR); sig = rp.lav_signaler(bars, N1, N2)
    if andel:
        r0, ev = celle_resultater(md, sig, HORISONT)
        region = (sig.n1_idx >= 9) & (sig.n1_idx <= 15) & (sig.n2_idx >= 9) & (sig.n2_idx <= 15)
        md = plant_delvis(md, ev.indgang_idx[region & ev.gyldig], andel, seed=f)
    # ubetinget 60-min bevægelse fra 5.000 tilfældige tidspunkter
    rng = np.random.default_rng(0)
    st = rng.choice(md.stempel[:-200], 20000)
    ev = rp.event_motor(md, st, HORISONT)
    x = ev.brutto[ev.gyldig]
    print(f"filter {f} (plantet andel {andel}): ubetinget 60-min bevægelse fra tilfældige tidspunkter: "
          f"{x.mean():+.2f} ticks (SE {x.std()/np.sqrt(len(x)):.2f}); samlet drift over 5 år: {int(md.luk[-1]-md.luk[0]):+d} ticks")
