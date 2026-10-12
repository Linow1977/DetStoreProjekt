"""Forsøg 15 (K1): Pharos' pause- og pensioneringsregel "målt mod forventningen".
Score efter k måneder = (faktisk sum - forventet sum) / (forventet spredning * sqrt(k)), tjekket hver måned
fra måned 3 til 60. Spørgsmål: (a) hvor tit pauses/pensioneres en strategi, der leverer PRÆCIS som lovet
(falsk alarm), og (b) hvor hurtigt opdages en strategi, hvis edge er død (gennemsnit 0 fra frysedatoen),
for forskellige forventede Sharpe-tal (gevinst i forhold til udsving, pr. år)?"""
import numpy as np
RNG = np.random.default_rng(15)
N, M = 100_000, 60
def run(sharpe_true_frac, sharpe_exp, z):
    mu = sharpe_exp / np.sqrt(12); sd = 1.0
    r = RNG.normal(mu * sharpe_true_frac, sd, (N, M))
    k = np.arange(1, M + 1)
    score = (np.cumsum(r, axis=1) - k * mu) / (sd * np.sqrt(k))
    hit = (score[:, 2:] < -z)
    ever = hit.any(axis=1)
    first = np.where(ever, hit.argmax(axis=1) + 3, np.nan)
    return ever.mean(), np.nanmedian(first) if ever.any() else np.nan
print("Falsk alarm: strategi leverer præcis som lovet (60 måneders månedlige tjek)")
for z in [2.33, 3.0]:
    p, _ = run(1.0, 1.0, z)
    print(f"  grænse {z}: andel der på et tidspunkt rammes: {p:.1%}")
print("Død edge (gennemsnit 0 fra frysedatoen): andel opdaget inden 60 mdr. og median-måned")
for s in [0.5, 1.0, 2.0, 3.0]:
    out = []
    for z in [2.33, 3.0]:
        p, m = run(0.0, s, z)
        out.append(f"grænse {z}: {p:.0%} (median måned {m:.0f})")
    print(f"  forventet Sharpe {s}: " + "; ".join(out))
