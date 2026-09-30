"""Forsøg 7 (K1): Hvilket værn virker mod falske edges fra skæve resultater (lille target, stort stop)?

Spørgsmål: Forsøg 6b viste, at en strategi uden edge, med mange små gevinster og få store tab
(target 4 / stop 12 ticks), når t >= 4 6-11 gange oftere end normalfordelingen siger. Hjælper
(a) stabilitets-kravet B5 (positiv i >= 12 af 20 kvartaler), (b) en bootstrap-t-test på dage,
(c) at kræve flere dage?
Opsætning: 300 handelsdage, én handel pr. dag, ingen edge. 3 mio. gentagelser; de falske med
t >= 4 samles og testes med (a) og (b). Bootstrap-t: træk dagene med tilbagelægning 1.999 gange,
regn t* = (gennemsnit* - gennemsnit) / se*, og kræv at t ligger over 99,997 %-fraktilen... det er
for dyrt, så vi bruger den tilsvarende bootstrap-p-værdi og kræver p <= 1/1999 (strengeste mulige).
"""
import numpy as np

RNG = np.random.default_rng(77)
DAYS = 300
REPS = 3_000_000
CHUNK = 100_000
B = 1999


def draw(shape):
    win = RNG.random(shape) < 0.75
    return np.where(win, 4.0, -12.0) + RNG.normal(0, 1.0, shape)


def main():
    fakes = []
    for _ in range(REPS // CHUNK):
        x = draw((CHUNK, DAYS))
        t = x.mean(axis=1) / (x.std(axis=1, ddof=1) / np.sqrt(DAYS))
        fakes.extend(x[t >= 4.0])
    fakes = np.array(fakes)
    n = len(fakes)
    print(f"Forsøg 7: {n} falske med t >= 4 ud af {REPS:,} ({n / REPS:.4%}; normal siger 0,0032 %)")

    # (a) B5-lignende: del i 20 "kvartaler" á 15 dage, kræv >= 12 positive og >= 4 af 5 "år" positive
    q = fakes.reshape(n, 20, 15).sum(axis=2)
    y = fakes.reshape(n, 5, 60).sum(axis=2)
    b5 = ((q > 0).sum(axis=1) >= 12) & ((y > 0).sum(axis=1) >= 4)
    print(f"  (a) består også stabilitets-kravet B5: {b5.mean():.0%} af de falske")

    # (b) bootstrap-t
    passed_boot = 0
    for row in fakes:
        m, s = row.mean(), row.std(ddof=1)
        t_obs = m / (s / np.sqrt(DAYS))
        idx = RNG.integers(0, DAYS, (B, DAYS))
        bs = row[idx]
        t_star = (bs.mean(axis=1) - m) / (bs.std(axis=1, ddof=1) / np.sqrt(DAYS))
        p = (1 + (t_star >= t_obs).sum()) / (B + 1)
        passed_boot += p <= 1 / (B + 1) + 1e-12
    print(f"  (b) består også bootstrap-t (ingen af {B} bootstrap-t over det observerede): "
          f"{passed_boot / n:.0%} af de falske")
    print("  (Til sammenligning: for normalfordelte dage ville næsten alle falske med t>=4 også bestå b.)")


if __name__ == "__main__":
    main()
