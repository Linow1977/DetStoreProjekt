"""Forsøg 12 (K1): Hvilket plateau-niveau kan ægte edges nå, afhængigt af deres bredde, og hvor mange
falske giver hvert niveau? (Grøn = t >= 2 uden 50 %-krav, som rettet efter forsøg 5.)
Opsætning: sigma 2,0 (nabo-korr. ca. 0,94), T* = 4. 300 ægte bakker pr. række (top-t 5), og 29.000
støjgitre (= 10 x 1,8 mio. kandidater) til falske grupper pr. 1,8 mio."""
import numpy as np, plateau
from plateau import GRID, noise_grids, plateau_level
from scipy.ndimage import label
plateau.RELATIVE_GREEN = 0.0
RNG = np.random.default_rng(12)
rr, cc = np.mgrid[0:GRID, 0:GRID]
def groups(g, L):
    passed = np.zeros((GRID, GRID), bool)
    for r, c in np.argwhere(g >= 4.0):
        if plateau_level(g, r, c) >= L: passed[r, c] = True
    return label(passed)[1]
dec = noise_grids(RNG, 29000, 2.0)
print("Falske grupper pr. 1,8 mio. kandidater (T*=4):",
      ", ".join(f"PL{L}: {sum(groups(g, L) for g in dec)/10:.1f}" for L in [1, 3, 5, 7]))
for width in [3.0, 5.0, 8.0]:
    found = {L: 0 for L in [1, 3, 5, 7]}
    for _ in range(300):
        r0, c0 = RNG.integers(6, GRID - 6, 2)
        truth = 5 * np.exp(-((rr - r0) ** 2 + (cc - c0) ** 2) / (2 * width ** 2))
        g = truth + noise_grids(RNG, 1, 2.0)[0]
        for L in found:
            passed = [(r, c) for r, c in np.argwhere(g >= 4.0) if truth[r, c] >= 1 and plateau_level(g, r, c) >= L]
            found[L] += bool(passed)
    print(f"Ægte edge, bredde {width:.0f} celler, top-t 5: fundet " + ", ".join(f"PL{L} {v/300:.0%}" for L, v in found.items()))
