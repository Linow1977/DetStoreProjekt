"""Forsøg 14 (K1): Et mildere krav om værdi-stabilitet (Thomas' beslutning: RSA TESTER værdi-stabilitet).
Kravet: i den inderste ring (3x3 omkring midten) skal alle naboer have netto >= R x midtens netto.
Prøvet R = 0 (intet krav), 0,25 og 0,5. Grøn ellers = t >= 2. Samme model som forsøg 12
(nabo-korr. ca. 0,94, T* = 4, PL3, ægte bakker med top-t 5, bredde 3 og 5)."""
import numpy as np, plateau
from plateau import GRID, noise_grids, plateau_level
from scipy.ndimage import label
plateau.RELATIVE_GREEN = 0.0
RNG = np.random.default_rng(14)
rr, cc = np.mgrid[0:GRID, 0:GRID]
def ok_inner(g, r, c, R):
    if R == 0: return True
    win = g[max(r-1,0):r+2, max(c-1,0):c+2]
    return bool((win >= R * g[r, c]).all())
def groups(g, R, truth=None):
    passed = np.zeros((GRID, GRID), bool)
    for r, c in np.argwhere(g >= 4.0):
        if plateau_level(g, r, c) >= 3 and ok_inner(g, r, c, R):
            if truth is None or truth[r, c] >= 1: passed[r, c] = True
    return label(passed)[1]
dec = noise_grids(RNG, 29000, 2.0)
for R in [0.0, 0.25, 0.5]:
    fal = sum(groups(g, R) for g in dec) / 10
    out = []
    for width in [3.0, 5.0]:
        f = 0
        for _ in range(300):
            r0, c0 = RNG.integers(6, GRID - 6, 2)
            truth = 5 * np.exp(-((rr - r0) ** 2 + (cc - c0) ** 2) / (2 * width ** 2))
            g = truth + noise_grids(RNG, 1, 2.0)[0]
            f += groups(g, R, truth) > 0
        out.append(f"bredde {width:.0f}: {f/300:.0%}")
    print(f"R = {R}: falske grupper pr. 1,8 mio. = {fal:.1f}; ægte fundet: " + ", ".join(out))
