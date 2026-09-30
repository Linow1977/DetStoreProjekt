"""Forsøg 3 (K1): Hvor tit giver ren støj et plateau (PL1-PL7) i et 25x25-gitter?

Spørgsmål: Beviser et plateau noget, når nabo-celler deler de fleste signaler?
Opsætning: 20.000 støjgitre (ingen edge) pr. grad af nabo-sammenhæng. For hvert gitter
findes det højeste plateau-niveau, nogen celle når (farver som i del1 G.2). Desuden: hvor tit
når en celle BÅDE t >= T* og PL3 (hele RSA-kravet B3 + B6).
Scriptet bruger plateau.py.
"""
import numpy as np
from plateau import noise_grids, neighbour_correlation, plateau_level

RNG = np.random.default_rng(11)
N_GRIDS = 20_000


def max_level_per_grid(grids):
    levels = np.zeros(len(grids), dtype=int)
    for i, g in enumerate(grids):
        best = 0
        for r, c in np.argwhere(g >= 2.0):  # PL1 kræver, at midten selv er grøn
            best = max(best, plateau_level(g, r, c))
            if best == 7:
                break
        levels[i] = best
    return levels


def main():
    print("Forsøg 3: plateauer i REN STØJ (25x25-gitter, ingen edge)")
    print(f"{'sigma':>5} {'nabo-korr.':>10} | " + " ".join(f"{'>=PL' + str(k):>7}" for k in range(1, 8))
          + " | celle med t>=4 og PL3 | t>=4.5 og PL3")
    for sigma in [0.0, 0.7, 1.0, 1.5, 2.0]:
        corr = neighbour_correlation(sigma) if sigma > 0 else 0.0
        grids = noise_grids(RNG, N_GRIDS, sigma)
        lv = max_level_per_grid(grids)
        # Hele kravet: t >= T* og plateau >= PL3
        hit4 = hit45 = 0
        for g in grids:
            ok4 = ok45 = False
            for r, c in np.argwhere(g >= 4.0):
                if plateau_level(g, r, c) >= 3:
                    ok4 = True
                    if g[r, c] >= 4.5:
                        ok45 = True
            hit4 += ok4
            hit45 += ok45
        row = " ".join(f"{np.mean(lv >= k):>7.2%}" for k in range(1, 8))
        print(f"{sigma:>5.1f} {corr:>10.2f} | {row} | {hit4 / N_GRIDS:>20.3%} | {hit45 / N_GRIDS:>12.3%}")
    print("\nTal = andel af gitre, hvor mindst én celle når niveauet. Et gitter = 625 kandidater.")
    print("Omregning: 1,8 mio. kandidater svarer til ca. 2.900 gitre.")


if __name__ == "__main__":
    main()
