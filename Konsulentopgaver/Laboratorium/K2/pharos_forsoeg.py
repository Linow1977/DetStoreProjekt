"""pharos_forsoeg.py -- PF1: Er "vælg efter seneste resultat" (Titan-agtig momentum) bedre end "tag alle lige"?
Walk-forward måned for måned: udvælgelsen bruger kun data til og med sidste måned; resultatet måles i næste måned.
To opdigtede verdener: (a) ingen strategi har en fordel; (b) halvdelen har en lille fordel, som slukker
tilfældigt og tænder igen (skiftende perioder). Lokkedue: tilfældig udvælgelse af samme antal.
KUN OPDIGTEDE DATA. Kør: <lab-venv>/bin/python pharos_forsoeg.py > resultater_pharos.txt"""

import numpy as np

N_STRAT, N_MAANED, DAGE = 40, 60, 21          # 40 strategier, 5 år, 21 handelsdage pr. måned
VINDUE, TOP = 6, 10                           # rangér efter de seneste 6 måneder, vælg de 10 bedste


def verden(seed, med_fordel):
    rng = np.random.default_rng(seed)
    dag = rng.normal(0, 10_000, (N_STRAT, N_MAANED * DAGE))
    if med_fordel:
        # halvdelen har +1.000 øre/dag i "tændte" perioder; tilstand skifter med 10 % chance pr. måned
        taendt = np.zeros((N_STRAT, N_MAANED), bool); taendt[: N_STRAT // 2, 0] = True
        for m in range(1, N_MAANED):
            skift = rng.random(N_STRAT) < 0.10
            taendt[:, m] = np.where(skift, ~taendt[:, m - 1], taendt[:, m - 1])
        taendt[N_STRAT // 2:] = False
        dag += np.repeat(taendt, DAGE, axis=1) * 1_000
    return dag.reshape(N_STRAT, N_MAANED, DAGE).sum(axis=2)   # månedstal


def walk_forward(M, metode, rng):
    ud = []
    for m in range(VINDUE, N_MAANED):
        if metode == "alle":
            valg = np.arange(N_STRAT)
        elif metode == "momentum":
            valg = np.argsort(-M[:, m - VINDUE:m].sum(axis=1), kind="stable")[:TOP]
        else:                                     # lokkedue: tilfældige TOP
            valg = rng.choice(N_STRAT, TOP, replace=False)
        ud.append(M[valg, m].mean())              # lige vægt pr. valgt strategi
    x = np.array(ud)
    return x.mean(), x.std() / np.sqrt(len(x))


for navn, med in (("ingen fordel", False), ("skiftende fordel", True)):
    res = {k: [] for k in ("alle", "momentum", "lokkedue")}
    for seed in range(200):
        M = verden(seed, med)
        rng = np.random.default_rng(10_000 + seed)
        for k in res:
            res[k].append(walk_forward(M, k, rng)[0])
    s = {k: (np.mean(v), np.std(v)) for k, v in res.items()}
    bedre = np.mean(np.array(res["momentum"]) > np.array(res["alle"]))
    print(f"PF1 {navn:17s} (200 verdener): gns. næste-måneds netto pr. valgt strategi — "
          f"alle {s['alle'][0]:+,.0f} (spr. {s['alle'][1]:,.0f}), momentum {s['momentum'][0]:+,.0f} "
          f"(spr. {s['momentum'][1]:,.0f}), lokkedue {s['lokkedue'][0]:+,.0f} (spr. {s['lokkedue'][1]:,.0f}); "
          f"momentum slog 'alle' i {bedre:.0%} af verdenerne")
