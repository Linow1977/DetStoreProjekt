"""Forsøg 5 (K1): Styrke (finder porten de ægte?) og OOS-reglerne på de celler, porten faktisk vælger.

Spørgsmål:
 a) Hvor mange ægte edges finder porten (t >= 4 og PL1/PL3), afhængigt af hvor BRED edgen er i
    parameter-gitteret, og om grøn-reglen "mindst 50 % af midten" hjælper eller skader?
 b) Hvor mange falske grupper giver ren støj pr. 1,8 mio. kandidater (2.900 gitre) i de samme varianter?
 c) For de repræsentanter porten vælger: hvor tit holder ægte og falske i OOS med forskellige regler?
Opsætning: som forsøg 4 (plateau.py), nabo-korrelation sigma = 2,0 (ca. 0,94).
"""
import numpy as np
import plateau
from plateau import GRID, noise_grids, plateau_level
from scipy.ndimage import label

RNG = np.random.default_rng(99)
SIGMA = 2.0
T_STAR = 4.0
N_PLANTED = 150
N_DECOY_GRIDS = 2900 * 10  # 10 lokkedue-runder
OOS_DRAWS = 400
S_YEAR = np.sqrt(5.0)


def reps_for(grid, min_level):
    passed = np.zeros((GRID, GRID), dtype=bool)
    for r, c in np.argwhere(grid >= T_STAR):
        if plateau_level(grid, r, c) >= min_level:
            passed[r, c] = True
    if not passed.any():
        return []
    lab, n = label(passed)
    out = []
    for k in range(1, n + 1):
        cells = np.argwhere(lab == k)
        d = ((cells - cells.mean(axis=0)) ** 2).sum(axis=1)
        out.append(tuple(cells[np.argmin(d)]))
    return out


def oos_rates(x, theta):
    """x: IS t for repræsentanter, theta: sand edge. Returnerer andel, der holder, pr. regel."""
    x = np.repeat(np.asarray(x, float), OOS_DRAWS)
    th = np.repeat(np.asarray(theta, float), OOS_DRAWS)
    y = th + S_YEAR * RNG.standard_normal(len(x))
    return {
        "K1 z=1,28": np.mean((y > 0) & (y >= x - 1.28 * S_YEAR)),
        "K1 z=1,0": np.mean((y > 0) & (y >= x - 1.0 * S_YEAR)),
        "fast 10%": np.mean(y >= 0.9 * x),
        "fast 20%": np.mean(y >= 0.8 * x),
    }


def main():
    print(f"Forsøg 5: styrke og OOS. Nabo-korrelation sigma={SIGMA}, T*={T_STAR}")
    rr, cc = np.mgrid[0:GRID, 0:GRID]
    for rel in [0.5, 0.0]:
        plateau.RELATIVE_GREEN = rel
        print(f"\n--- Grøn-regel: t >= 2 {'og >= 50 % af midten' if rel else '(uden 50 %-krav)'} ---")
        # b) falske grupper i ren støj
        dec = noise_grids(RNG, N_DECOY_GRIDS, SIGMA)
        for L in [1, 3]:
            reps = [(i, r, c) for i, g in enumerate(dec) for (r, c) in reps_for(g, L)]
            per_run = len(reps) / 10
            xs = [dec[i, r, c] for i, r, c in reps]
            fr = oos_rates(xs, np.zeros(len(xs))) if xs else {}
            print(f"  PL{L}: falske grupper pr. 1,8 mio. kandidater: {per_run:.1f}; "
                  f"falske der holder i OOS: " + ", ".join(f"{k} {v:.0%}" for k, v in fr.items()))
        # a) + c) styrke
        for width in [2.0, 3.0, 5.0]:
            for A in [4, 5, 6]:
                found = {1: 0, 3: 0}
                xs3, th3 = [], []
                for _ in range(N_PLANTED):
                    r0, c0 = RNG.integers(6, GRID - 6, 2)
                    truth = A * np.exp(-((rr - r0) ** 2 + (cc - c0) ** 2) / (2 * width ** 2))
                    g = truth + noise_grids(RNG, 1, SIGMA)[0]
                    for L in [1, 3]:
                        reps = [p for p in reps_for(g, L) if truth[p] >= 1.0]
                        if reps:
                            found[L] += 1
                            if L == 3:
                                xs3.append(g[reps[0]])
                                th3.append(truth[reps[0]])
                tr = oos_rates(xs3, th3) if xs3 else {}
                print(f"  bredde {width:.0f}, top t={A}: fundet PL1 {found[1] / N_PLANTED:4.0%}, "
                      f"PL3 {found[3] / N_PLANTED:4.0%} | ægte (PL3) der holder i OOS: "
                      + ", ".join(f"{k} {v:.0%}" for k, v in tr.items()))


if __name__ == "__main__":
    main()
