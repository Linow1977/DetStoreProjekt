"""Fælles hjælpekode for forsøg 3 og 4: støjgitre og plateau-trappen (K1 del1 afsnit G.2).

Et 25x25-gitter af t-tal (N1 x N2). Nabo-celler hænger sammen, fordi de deler signaler.
Det efterlignes med hvid støj, der udglattes med et gaussisk filter (bredde sigma),
og derefter skaleres, så hver celle har spredning 1 (et rigtigt regnet t-tal under nul-hypotesen).

Farver (K1 G.2), set fra en midtercelle med t-tal tc:
  grøn: t >= 2 og t >= 0,5 x tc
  rød:  t <= 0
  grå:  alt andet, også celler uden for gitteret (manglende data)
Trappen (opgaven, eksempel B):
  PL1 3x3 100 % grøn | PL2 5x5 grå < 50 %, rød 0, midte PL1 | PL3 5x5 100 % grøn
  PL4 7x7 grå < 50 %, rød 0, midte PL3 | PL5 7x7 100 % grøn
  PL6 9x9 grå < 50 %, rød < 20 %, midte PL5 | PL7 9x9 100 % grøn
"""
import numpy as np
from scipy.ndimage import gaussian_filter, label

GRID = 25
PAD = 8  # ekstra kant, så udglatningen ikke får kant-effekter


def noise_grids(rng, n, sigma):
    """n uafhængige 25x25 støjgitre med nabo-sammenhæng styret af sigma (0 = ingen)."""
    size = GRID + 2 * PAD
    white = rng.standard_normal((n, size, size)).astype(np.float32)
    if sigma > 0:
        smooth = gaussian_filter(white, sigma=(0, sigma, sigma), mode="wrap")
        smooth /= np.sqrt((gaussian_kernel_weights(sigma) ** 2).sum())
    else:
        smooth = white
    return smooth[:, PAD:PAD + GRID, PAD:PAD + GRID]


def gaussian_kernel_weights(sigma):
    """Vægtene i det 2D gaussiske filter (samme trunkering som scipy: 4 sigma)."""
    radius = int(4.0 * sigma + 0.5)
    x = np.arange(-radius, radius + 1)
    w1 = np.exp(-0.5 * (x / sigma) ** 2)
    w1 /= w1.sum()
    return np.outer(w1, w1)


def neighbour_correlation(sigma, rng=None):
    rng = rng or np.random.default_rng(0)
    g = noise_grids(rng, 2000, sigma)
    a, b = g[:, :, :-1].ravel(), g[:, :, 1:].ravel()
    return np.corrcoef(a, b)[0, 1]


RELATIVE_GREEN = 0.5  # grøn kræver t >= RELATIVE_GREEN x midtens t (0 = slået fra)


def plateau_level(grid, r, c):
    """Højeste plateau-niveau (0-7) for midtercellen (r, c) i ét gitter."""
    tc = grid[r, c]
    padded = np.full((GRID + 8, GRID + 8), np.nan, dtype=np.float32)
    padded[4:4 + GRID, 4:4 + GRID] = grid
    win = padded[r:r + 9, c:c + 9]  # 9x9 omkring midten (midten er [4,4])
    valid = ~np.isnan(win)
    green = valid & (win >= 2.0) & (win >= RELATIVE_GREEN * tc)
    red = valid & (win <= 0.0)
    grey = ~green & ~red  # inkl. manglende celler

    def box(mask, half):
        return mask[4 - half:4 + half + 1, 4 - half:4 + half + 1]

    level = 0
    if box(green, 1).all():
        level = 1
    else:
        return level
    n25 = 25
    if box(grey, 2).sum() < 0.5 * n25 and box(red, 2).sum() == 0:
        level = 2
    else:
        return level
    if box(green, 2).all():
        level = 3
    else:
        return level
    n49 = 49
    if box(grey, 3).sum() < 0.5 * n49 and box(red, 3).sum() == 0:
        level = 4
    else:
        return level
    if box(green, 3).all():
        level = 5
    else:
        return level
    n81 = 81
    if box(grey, 4).sum() < 0.5 * n81 and box(red, 4).sum() < 0.2 * n81:
        level = 6
    else:
        return level
    if box(green, 4).all():
        level = 7
    return level


def passing_groups(grid, t_star, min_level, truth=None):
    """Beståede celler (t >= T* og plateau >= min_level) samlet i sammenhængende grupper.
    Returnerer liste af (repræsentant r, c, t, niveau). Repræsentant = beståede celle nærmest
    gruppens geometriske midte (K1 del1 B.3)."""
    cand = np.argwhere(grid >= t_star)
    if len(cand) == 0:
        return []
    passed = np.zeros_like(grid, dtype=bool)
    levels = {}
    for r, c in cand:
        lv = plateau_level(grid, r, c)
        if lv >= min_level:
            passed[r, c] = True
            levels[(r, c)] = lv
    if not passed.any():
        return []
    lab, n = label(passed)
    out = []
    for k in range(1, n + 1):
        cells = np.argwhere(lab == k)
        centre = cells.mean(axis=0)
        d = ((cells - centre) ** 2).sum(axis=1)
        best = cells[np.argmin(d)]
        out.append((int(best[0]), int(best[1]), float(grid[best[0], best[1]]), levels[tuple(best)]))
    return out
