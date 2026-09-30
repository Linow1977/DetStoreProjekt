"""Forsøg 8 (K1): Hvilken celle skal repræsentere et plateau i OOS — midten af gruppen eller cellen
med højest t? (del1 B.3 siger: midten.)
Opsætning: som forsøg 5 (sigma 2,0, T* 4, PL3, grøn uden 50 %-krav). 600 ægte bakker (bredde 3 og 5,
top-t 5). For hver fundet gruppe sammenlignes to repræsentanter: (a) nærmest gruppens midte,
(b) højeste t. Måles: sand edge i repræsentanten, IS-t, og andel der holder i OOS (K1 z=1,28)."""
import numpy as np
import plateau
from plateau import GRID, noise_grids, plateau_level
from scipy.ndimage import label
RNG = np.random.default_rng(8)
plateau.RELATIVE_GREEN = 0.0
S = np.sqrt(5.0)
rr, cc = np.mgrid[0:GRID, 0:GRID]
for width in [3.0, 5.0]:
    res = {"midte": [], "højeste t": []}
    for _ in range(600):
        r0, c0 = RNG.integers(6, GRID - 6, 2)
        truth = 5 * np.exp(-((rr - r0) ** 2 + (cc - c0) ** 2) / (2 * width ** 2))
        g = truth + noise_grids(RNG, 1, 2.0)[0]
        passed = np.zeros((GRID, GRID), bool)
        for r, c in np.argwhere(g >= 4.0):
            if plateau_level(g, r, c) >= 3:
                passed[r, c] = True
        lab, n = label(passed)
        for k in range(1, n + 1):
            cells = np.argwhere(lab == k)
            d = ((cells - cells.mean(axis=0)) ** 2).sum(axis=1)
            for name, p in [("midte", tuple(cells[np.argmin(d)])),
                            ("højeste t", tuple(cells[np.argmax(g[tuple(cells.T)])]))]:
                th, x = truth[p], g[p]
                y = th + S * RNG.standard_normal(2000)
                hold = np.mean((y > 0) & (y >= x - 1.28 * S))
                res[name].append((th, x, hold))
    print(f"bredde {width:.0f}, top-t 5:")
    for name, v in res.items():
        a = np.array(v)
        print(f"   {name:>10}: sand edge {a[:,0].mean():.2f}, IS-t {a[:,1].mean():.2f}, "
              f"oppustning {a[:,1].mean()-a[:,0].mean():.2f}, holder i OOS {a[:,2].mean():.1%}  (n={len(a)})")
