"""Forsøg 6b (K1): Samme som forsøg 6, men med MILDERE skævhed og med en typisk exit-profil.

Spørgsmål: Forsøg 6 brugte meget skæve dage (skævhed ca. -6). Hvor meget betyder mild skævhed,
og hvad med den skævhed, som et lille target og et stort stop giver (mange små gevinster,
få store tab)?
Fordelinger (alle med middelværdi 0 = ingen edge):
 - lognormal sigma 0,5, spejlet (skævhed ca. -1,8)
 - lognormal sigma 0,25, spejlet (skævhed ca. -0,8)
 - "target 4 / stop 12 ticks": hver dag én handel, gevinst +4 med sandsynlighed 0,75, tab -12
   med sandsynlighed 0,25 (middelværdi 0), plus lidt normal støj.
Samtidig afprøves et simpelt værn: kræv også, at t holder, når man bruger en bootstrap-t-tærskel
(her vist som andelen, der består BÅDE t>=4 og en fortegnstest på dage (andel positive dage)).
"""
import numpy as np
from scipy import stats

RNG = np.random.default_rng(6)
REPS = 400_000
CHUNK = 50_000


def draw(kind, shape):
    if kind.startswith("lognormal"):
        s = float(kind.split()[1])
        x = RNG.lognormal(0, s, shape)
        return -(x - np.exp(0.5 * s * s))
    if kind == "target4/stop12":
        win = RNG.random(shape) < 0.75
        return np.where(win, 4.0, -12.0) + RNG.normal(0, 1.0, shape)
    raise ValueError(kind)


def main():
    print(f"Forsøg 6b: mild skævhed. Normal: t>=4 i {stats.norm.sf(4):.5%}")
    print(f"{'fordeling':>18} {'skævhed':>8} {'dage':>6} | {'t>=3':>8} {'t>=4':>9} {'ift. normal':>11}")
    for kind in ["lognormal 0.25", "lognormal 0.5", "target4/stop12"]:
        sample = draw(kind, 2_000_000)
        skew = stats.skew(sample)
        for days in [150, 300, 1250]:
            n3 = n4 = 0
            reps = REPS if days < 1000 else REPS // 4
            for _ in range(reps // CHUNK):
                x = draw(kind, (CHUNK, days))
                t = x.mean(axis=1) / (x.std(axis=1, ddof=1) / np.sqrt(days))
                n3 += (t >= 3).sum()
                n4 += (t >= 4).sum()
            p3, p4 = n3 / reps, n4 / reps
            print(f"{kind:>18} {skew:>8.2f} {days:>6} | {p3:>8.3%} {p4:>9.4%} {p4 / stats.norm.sf(4):>10.1f}x")


if __name__ == "__main__":
    main()
