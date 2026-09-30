"""Forsøg 6 (K1): Holder t-tallets "hale" med få signaldage og tykhalede/skæve dagsresultater?

Spørgsmål: Porten bruger t >= ca. 4. Normalfordelingen siger, at ren støj kun når t >= 4 i
0,003 % af tilfældene. Men dagsresultater i handel er tykhalede (sjældne store dage) og kan være
skæve. Er halen tykkere, bliver der flere falske vindere end regnestykket i del1 C.1 siger, og
det er vigtigt for minimum-antallet af dage (B2: 150).
Opsætning: D uafhængige dagsresultater med middelværdi 0 fra fire fordelinger; t = gennemsnit /
(spredning / sqrt(D)). 2 mio. gentagelser pr. række. (Lokkeduerne ville fange dette automatisk;
forsøget viser, hvor meget det betyder.)
"""
import numpy as np
from scipy import stats

RNG = np.random.default_rng(5)
REPS = 2_000_000
CHUNK = 100_000


def draw(kind, shape):
    if kind == "normal":
        return RNG.standard_normal(shape)
    if kind == "tykhalet (t3)":
        return RNG.standard_t(3, shape)
    if kind == "skæv højre (gevinst-hale)":
        x = RNG.lognormal(0, 1, shape)
        return x - np.exp(0.5)
    if kind == "skæv venstre (tabs-hale)":
        x = RNG.lognormal(0, 1, shape)
        return -(x - np.exp(0.5))
    raise ValueError(kind)


def main():
    kinds = ["normal", "tykhalet (t3)", "skæv højre (gevinst-hale)", "skæv venstre (tabs-hale)"]
    print("Forsøg 6: andel af ren støj med t >= 3 og t >= 4 (ensidet)")
    print(f"  Normalfordelingen siger: t>=3: {stats.norm.sf(3):.4%}, t>=4: {stats.norm.sf(4):.5%}")
    print(f"{'fordeling':>28} {'dage':>6} | {'t>=3':>9} {'t>=4':>10} | {'t>=4 ift. normal':>16}")
    for kind in kinds:
        for days in [150, 300, 1250]:
            n3 = n4 = 0
            for _ in range(REPS // CHUNK):
                x = draw(kind, (CHUNK, days))
                t = x.mean(axis=1) / (x.std(axis=1, ddof=1) / np.sqrt(days))
                n3 += (t >= 3).sum()
                n4 += (t >= 4).sum()
            p3, p4 = n3 / REPS, n4 / REPS
            print(f"{kind:>28} {days:>6} | {p3:>9.4%} {p4:>10.5%} | {p4 / stats.norm.sf(4):>15.1f}x")


if __name__ == "__main__":
    main()
