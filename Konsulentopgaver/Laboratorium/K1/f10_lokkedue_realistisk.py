"""Forsøg 10 (K1): Virker lokkeduer (cirkulær forskydning 4-26 uger) på et mere realistisk opdigtet marked?

Spørgsmål: I et marked med skiftende uro (rolige og urolige perioder), U-formet uro over dagen,
tykke haler og en lille opdrift — og med et ægte filter, der tænder oftest i urolige perioder —
ligner lokkeduernes t-tal så de ægte signalers t-tal, når der INGEN edge er? Og hvor tæt hænger
nabo-cellerne i gitteret sammen (det tal, der afgør plateauets værdi, forsøg 3-4)?

Marked (opdigtet): 1.250 dage á 390 minutter. Dagens uro følger en langsom proces (log-AR(1),
persistens 0,98), minut-afkast er t-fordelte (df 4) og skaleres med U-form over dagen. Lille drift.
Afkast er uafhængige af fortiden => INGEN filter har en ægte edge.
Filter: 10-minutters bars. Signal = "lukker over højeste høj de sidste N1 bars" OG "luk over
gennemsnittet af de sidste N2 bars", N1 = 5..29, N2 = 10..58 (trin 2) -> 25 x 25 gitter.
Signal = skift fra FALSK til SAND. Indgang = næste bars åbning. Mål = bevægelse over 6 bars (60 min),
kun hvis inden for samme dag. Lang retning. Dag-klynget t.
Sammenligning: (A) ægte signaler på 12 uafhængige markeder (sand nul-fordeling),
(B) lokkeduer: samme signaler flyttet 4-26 hele uger cirkulært, 4 runder pr. marked.
"""
import numpy as np

RNG = np.random.default_rng(1010)
DAYS, MIN_PER_DAY, BAR = 1250, 390, 10
BARS_PER_DAY = MIN_PER_DAY // BAR
H = 6
N1S = np.arange(5, 30)
N2S = np.arange(10, 60, 2)
N_MARKETS = 200
N_DECOY = 3


def make_market():
    log_vol = np.zeros(DAYS)
    for d in range(1, DAYS):
        log_vol[d] = 0.98 * log_vol[d - 1] + RNG.normal(0, 0.15)
    day_vol = np.exp(log_vol)
    u = np.linspace(-1, 1, MIN_PER_DAY)
    intraday = 1.0 + 0.8 * u ** 2
    shocks = RNG.standard_t(4, (DAYS, MIN_PER_DAY)) / np.sqrt(2.0)
    rets = 0.002 + shocks * day_vol[:, None] * intraday[None, :]  # lille opdrift
    price = 1000 + np.cumsum(rets.ravel())
    p = price.reshape(DAYS * BARS_PER_DAY, BAR)
    opens = np.r_[1000.0, price[:-1]].reshape(DAYS * BARS_PER_DAY, BAR)[:, 0]
    return opens, p.max(axis=1), p[:, -1]


def rolling_max_prev(x, n):
    """Højeste værdi af de n FORRIGE bars (ikke den nuværende)."""
    out = np.full(len(x), np.inf)
    from numpy.lib.stride_tricks import sliding_window_view
    w = sliding_window_view(x, n).max(axis=1)  # w[i] = max(x[i..i+n-1])
    out[n:] = w[:-1]
    return out


def rolling_mean(x, n):
    c = np.cumsum(np.r_[0.0, x])
    out = np.full(len(x), np.nan)
    out[n - 1:] = (c[n:] - c[:-n]) / n
    return out


def cell_day_sums(start_bars, opens, closes, day_shift_bars=0):
    """Dagssummer af bevægelse for signaler, der starter ved start_bars (evt. flyttet)."""
    nb = len(opens)
    idx = (start_bars + day_shift_bars) % nb
    entry = idx + 1
    exit_ = entry + H - 1
    same_day = (entry // BARS_PER_DAY == idx // BARS_PER_DAY) & (exit_ // BARS_PER_DAY == idx // BARS_PER_DAY)
    entry, exit_ = entry[same_day], exit_[same_day]
    move = closes[exit_] - opens[entry]
    day = entry // BARS_PER_DAY
    return day, move


def day_t(day, move):
    if len(move) < 30:
        return np.nan
    sums = np.bincount(day, weights=move, minlength=DAYS)
    counts = np.bincount(day, minlength=DAYS)
    used = counts > 0
    n, D = counts.sum(), used.sum()
    m = sums.sum() / n
    resid = sums[used] - m * counts[used]
    se = np.sqrt(D / (D - 1) * (resid ** 2).sum()) / n
    return m / se


def main():
    real_t, decoy_t, neighbour = [], [], []
    for k in range(N_MARKETS):
        opens, highs, closes = make_market()
        brk = {n1: closes > rolling_max_prev(highs, n1) for n1 in N1S}
        sma = {n2: closes > rolling_mean(closes, n2) for n2 in N2S}
        grid_real = np.full((25, 25), np.nan)
        shifts = RNG.integers(4, 27, N_DECOY) * 5 * BARS_PER_DAY  # hele uger, samme for hele filteret
        grid_dec = np.full((N_DECOY, 25, 25), np.nan)
        for i, n1 in enumerate(N1S):
            for j, n2 in enumerate(N2S):
                on = brk[n1] & sma[n2]
                starts = np.flatnonzero(on[1:] & ~on[:-1]) + 1
                starts = starts[starts < len(opens) - H - 1]
                grid_real[i, j] = day_t(*cell_day_sums(starts, opens, closes))
                for r, s in enumerate(shifts):
                    grid_dec[r, i, j] = day_t(*cell_day_sums(starts, opens, closes, s))
        real_t.append(grid_real.ravel())
        decoy_t.append(grid_dec.ravel())
        neighbour.append(np.corrcoef(grid_real[:, :-1].ravel(), grid_real[:, 1:].ravel())[0, 1])
        neighbour.append(np.corrcoef(grid_real[:-1, :].ravel(), grid_real[1:, :].ravel())[0, 1])
        print(f"  marked {k + 1}/{N_MARKETS} færdigt", flush=True)
    grid_mean_real = np.array([np.nanmean(x) for x in real_t])
    grid_mean_dec = np.array([np.nanmean(x.reshape(N_DECOY, -1), axis=1) for x in decoy_t]).ravel()
    real_t = np.concatenate(real_t)
    decoy_t = np.concatenate(decoy_t)
    real_t, decoy_t = real_t[~np.isnan(real_t)], decoy_t[~np.isnan(decoy_t)]

    def describe(x):
        return (f"middel {x.mean():+.2f}, spredning {x.std():.2f}, |t|>2: {np.mean(np.abs(x) > 2):.1%}, "
                f"t>2: {np.mean(x > 2):.1%}, t>3: {np.mean(x > 3):.2%}")
    print("\nForsøg 10: realistisk opdigtet marked uden edge")
    print(f"  Ægte signaler (sand nul, {len(real_t)} celler):  " + describe(real_t))
    print(f"  Lokkeduer ({len(decoy_t)} celler):             " + describe(decoy_t))
    # Spredning af t mellem markeder er klumpet (hele gitteret flytter sig sammen) -> vis også gitter-middel
    print(f"  Gitter-gennemsnit af t: ægte middel {grid_mean_real.mean():+.2f} (sd {grid_mean_real.std():.2f}), "
          f"lokkeduer middel {grid_mean_dec.mean():+.2f} (sd {grid_mean_dec.std():.2f})")
    print(f"  Nabo-korrelation af t i gitteret (median over markeder/retninger): {np.median(neighbour):.2f}")
    print("  (Middel af t over 0 skyldes opdriften: lange signaler får opdriften med — både ægte og lokkeduer.)")


if __name__ == "__main__":
    main()
