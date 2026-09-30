"""pharos_blok.py -- PF2 (kontrol_pharos fund 6): hvor stor må blokken være, når lokkeduerne blander
hver strategis måneder? Momentum (R2: top 10 efter 6 mdr.) mod alle lige (R0). Lokkedue: hver strategis
månedsrække skæres i blokke af b måneder, blokkene blandes; fordelen R2-R0 regnes igen. Testen "består",
hvis den ægte fordel er større end 95 % af lokkeduernes. KUN OPDIGTEDE DATA."""
import numpy as np
from pharos_forsoeg import verden, N_STRAT, N_MAANED, VINDUE, TOP

def fordel(M):
    x = []
    for m in range(VINDUE, N_MAANED):
        valg = np.argsort(-M[:, m - VINDUE:m].sum(axis=1), kind="stable")[:TOP]
        x.append(M[valg, m].mean() - M[:, m].mean())
    return np.mean(x)

def bland(M, b, rng):
    ud = np.empty_like(M)
    for i in range(M.shape[0]):
        blokke = [M[i, j:j + b] for j in range(0, N_MAANED, b)]
        rng.shuffle(blokke)
        ud[i] = np.concatenate(blokke)
    return ud

VERDENER, LOKKEDUER = 60, 200
for navn, med in (("ingen hukommelse (ingen fordel)", False), ("hukommelse (fordel tænder/slukker 10 %/md.)", True)):
    for b in (1, 3, 6):
        bestaar = 0
        for seed in range(VERDENER):
            M = verden(seed, med)
            rng = np.random.default_rng(500 + seed)
            aegte = fordel(M)
            lok = np.array([fordel(bland(M, b, rng)) for _ in range(LOKKEDUER)])
            bestaar += aegte > np.quantile(lok, 0.95)
        print(f"PF2 {navn:44s} blok {b} md.: momentum 'bestod' i {bestaar/VERDENER:.0%} af {VERDENER} verdener")
