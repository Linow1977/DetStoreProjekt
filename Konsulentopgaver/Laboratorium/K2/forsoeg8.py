"""forsoeg8.py -- F13 (= T11i): skæv exit-profil på ren støj. Hvor tit når t >= 3 / >= 4, og hvad er skævheden?
Tilfældige indgange (ingen edge) med target 4 / stop 12 ticks, tidsgrænse 120 min. KUN OPDIGTEDE DATA."""
import numpy as np
from scipy import stats
import rsa_proto as rp
import exitmotor as em
from forsoeg import skriv, us_helligdage

kal = rp.lav_kalender("2020-01-01", "2024-12-31", helligdage=us_helligdage())
md = rp.lav_minutdata(kal, seed=51, sigma=2.0, uro_klumper=True)
sidste = np.searchsorted(md.dag, md.dag, side="right") - 1
rng = np.random.default_rng(3)
for (S, T) in ((12, 4), (8, 8)):
    ts, skaev = [], []
    for strategi in range(150):
        e = np.sort(rng.choice(len(md.luk) - 500, 1500, replace=False))
        res = np.array([em.exit_gitter(md, i, min(i + 119, sidste[i]), [S], [T])[0][0, 0] for i in e])
        r = rp.celle_tal(np.zeros(len(e), dtype=np.int64), md.dag[e], res.astype(float), 1)
        ts.append(r["t"][0]); skaev.append(stats.skew(res))
    ts = np.array(ts)
    skriv(f"F13 stop {S} / target {T}: 150 tilfældige 'strategier' a 1.500 handler på støj: t middel {ts.mean():+.2f}, spredning {ts.std():.2f}, "
          f"andel t>=3: {np.mean(ts>=3):.3f}, t>=4: {np.mean(ts>=4):.3f} (normalfordeling: 0,0013 / 0,00003); skævhed middel {np.mean(skaev):+.2f}")
