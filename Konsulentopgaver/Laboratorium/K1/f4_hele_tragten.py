"""Forsøg 4 (K1): Hele tragten i lille skala — lokkeduer + FDR + plateau + OOS-regel.

Spørgsmål: Plant et kendt antal ægte edges blandt ca. 1,8 mio. kandidater. Hvor mange ægte og
falske kommer igennem RSA-porten (t >= T* og plateau) og derefter OOS-reglen? Og passer
lokkeduernes FDR-skøn med den sande andel falske?

Opsætning (opdigtet):
- 2.900 gitre á 25x25 = 1,81 mio. kandidater. Enhed: t-tal over 5 år (IS-standardfejl = 1).
- Støj: udglattet støj med nabo-korrelation (sigma 2,0 => ca. 0,94; også 1,5 og 3,0 prøvet).
- 60 gitre har en ægte edge: en "bakke" med top A (sand t i midten) og bredde 3 celler.
  A = 3, 4, 5, 6 (15 gitre hver). Sand edge i en celle = bakkens højde der.
- Lokkeduer: 20 runder af 2.900 rene støjgitre (svarer til cirkulær forskydning: samme
  sammenhæng mellem naboer, ingen forbindelse til kursen bagefter).
- Tæller i GRUPPER (én repræsentant pr. sammenhængende plateau, del1 B.3).
- En gruppe er "ægte", hvis den sande edge i repræsentanten er >= 1 (i t-enheder).
- OOS (ét år): måling = sand edge + støj med sd sqrt(5). Regel: > 0 og >= IS - 1,28 x sqrt(5).
  Også vist: fast 20 %-regel.
Bruger plateau.py.
"""
import numpy as np
from plateau import GRID, noise_grids, plateau_level, passing_groups
from scipy.ndimage import label

RNG = np.random.default_rng(2026)
N_GRIDS = 2900
N_REAL = 60
AMPLITUDES = [3, 4, 5, 6]
WIDTH = 3.0
N_DECOY_ROUNDS = 20
T_STARS = [3.0, 3.5, 4.0, 4.5]
LEVELS = [1, 3, 5]


def bump(amplitude):
    r0, c0 = RNG.integers(6, GRID - 6, 2)
    rr, cc = np.mgrid[0:GRID, 0:GRID]
    return amplitude * np.exp(-((rr - r0) ** 2 + (cc - c0) ** 2) / (2 * WIDTH ** 2))


def cell_levels(grid, t_min):
    """Plateau-niveau for alle celler med t >= t_min (regnes én gang, bruges for alle T*)."""
    return {(int(r), int(c)): plateau_level(grid, r, c) for r, c in np.argwhere(grid >= t_min)}


def groups_from_levels(grid, levels, t_star, min_level):
    passed = np.zeros((GRID, GRID), dtype=bool)
    for (r, c), lv in levels.items():
        if grid[r, c] >= t_star and lv >= min_level:
            passed[r, c] = True
    if not passed.any():
        return []
    lab, n = label(passed)
    reps = []
    for k in range(1, n + 1):
        cells = np.argwhere(lab == k)
        d = ((cells - cells.mean(axis=0)) ** 2).sum(axis=1)
        reps.append(tuple(cells[np.argmin(d)]))
    return reps


def run(sigma):
    truth = np.zeros((N_GRIDS, GRID, GRID), dtype=np.float32)
    amps = np.zeros(N_GRIDS)
    for i in range(N_REAL):
        amps[i] = AMPLITUDES[i % len(AMPLITUDES)]
        truth[i] = bump(amps[i])
    observed = truth + noise_grids(RNG, N_GRIDS, sigma)
    t_min = min(T_STARS)
    real_levels = [cell_levels(g, t_min) for g in observed]

    decoy_counts = {(t, L): [] for t in T_STARS for L in LEVELS}
    for _ in range(N_DECOY_ROUNDS):
        dec = noise_grids(RNG, N_GRIDS, sigma)
        dec_levels = [cell_levels(g, t_min) for g in dec]
        for t in T_STARS:
            for L in LEVELS:
                decoy_counts[(t, L)].append(sum(len(groups_from_levels(g, lv, t, L))
                                                for g, lv in zip(dec, dec_levels)))

    print(f"\n=== Nabo-korrelation: sigma = {sigma} ===")
    print(f"{'T*':>4} {'PL':>3} | {'ægte':>5} {'falske':>6} {'sand FDR':>8} {'lokkedue-FDR':>12} "
          f"{'(spredning)':>11} | ægte bakker fundet A=3/4/5/6 | efter OOS K1: ægte / falske | fast 20%: ægte / falske")
    for t in T_STARS:
        for L in LEVELS:
            true_g = false_g = 0
            found_by_amp = {a: 0 for a in AMPLITUDES}
            oos = {"K1": [0, 0], "20%": [0, 0]}
            for i, (g, lv) in enumerate(zip(observed, real_levels)):
                reps = groups_from_levels(g, lv, t, L)
                amp_found = False
                for r, c in reps:
                    theta = truth[i, r, c]
                    is_true = theta >= 1.0
                    true_g += is_true
                    false_g += not is_true
                    amp_found |= is_true
                    y = theta + np.sqrt(5.0) * RNG.standard_normal()
                    x = g[r, c]
                    k1 = (y > 0) and (y >= x - 1.28 * np.sqrt(5.0))
                    f20 = y >= 0.8 * x
                    oos["K1"][0 if is_true else 1] += k1
                    oos["20%"][0 if is_true else 1] += f20
                if amp_found:
                    found_by_amp[amps[i]] += 1
            total = true_g + false_g
            dc = np.array(decoy_counts[(t, L)])
            est = dc.mean() / total if total else float("nan")
            true_fdr = false_g / total if total else float("nan")
            found = "/".join(str(found_by_amp[a]) for a in AMPLITUDES)
            print(f"{t:>4} {L:>3} | {true_g:>5} {false_g:>6} {true_fdr:>8.1%} {est:>12.1%} "
                  f"{dc.std():>11.1f} | {found:>27} (af 15 hver) | {oos['K1'][0]:>16} / {oos['K1'][1]:<6} | "
                  f"{oos['20%'][0]:>13} / {oos['20%'][1]}")


def main():
    print("Forsøg 4: hele tragten. 2.900 gitre (1,81 mio. kandidater), 60 med ægte edge.")
    for sigma in [2.0, 1.5, 3.0]:
        run(sigma)


if __name__ == "__main__":
    main()
