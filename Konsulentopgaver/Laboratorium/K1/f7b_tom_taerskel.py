"""Forsøg 7b (K1): Hvor højt skal t-kravet være for en skæv strategi (target 4 / stop 12) uden edge,
for at få samme falske-rate som t >= 4 giver ved normalfordelte dage (0,0032 %)?
Det er præcis det, en lokkedue-kørsel med samme exits ville finde. 3 mio. gentagelser pr. række."""
import numpy as np
from scipy import stats
RNG = np.random.default_rng(78)
for days in [150, 300, 1250]:
    reps, chunk = (3_000_000, 100_000) if days < 1000 else (1_000_000, 20_000)
    top = []
    for _ in range(reps // chunk):
        win = RNG.random((chunk, days)) < 0.75
        x = np.where(win, 4.0, -12.0) + RNG.normal(0, 1.0, (chunk, days))
        t = x.mean(axis=1) / (x.std(axis=1, ddof=1) / np.sqrt(days))
        top.extend(t[t >= 3.5])
    top = np.sort(np.array(top))[::-1]
    k = int(round(stats.norm.sf(4) * reps))
    print(f"dage {days:>5}: tærskel med samme falske-rate som normal t>=4: t >= {top[k-1]:.2f}  (bygget på {k} overskridelser)")
