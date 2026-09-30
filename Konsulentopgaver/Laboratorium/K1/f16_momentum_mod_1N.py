"""Forsøg 16 (K1): Hjælper Titan-lignende momentum-udvælgelse af strategier?
Regel M (som beskrevet for Titan i søgeresuméer): handl en strategi næste måned, hvis summen over de
sidste 12 måneder og de sidste 3 måneder begge er > 0, og 3-måneders gennemsnittet > 12-måneders gennemsnittet.
Nulmodel 1/N: handl alle strategier med samme risiko.
To opdigtede verdener, 40 strategier, 120 måneder, månedlig Sharpe-agtig edge 0,15 (ca. 0,5 pr. år) når "tændt":
 A) edgen er konstant (ingen hukommelse fra måned til måned),
 B) edgen skifter mellem tændt og slukket i lange perioder (gennemsnit 12 måneder), altså positiv autokorrelation.
Mål: porteføljens gennemsnit pr. måned, spredning og årlig Sharpe, samt største nedtur. 2.000 gentagelser."""
import numpy as np
RNG = np.random.default_rng(16)
S, T, R = 40, 120, 2000
def world(regime):
    if not regime:
        mu = np.full((S, T), 0.15)
    else:
        on = np.zeros((S, T), bool); state = RNG.random(S) < 0.5
        for t in range(T):
            flip = RNG.random(S) < 1 / 12
            state = np.where(flip, ~state, state); on[:, t] = state
        mu = np.where(on, 0.30, 0.0)   # samme gennemsnit 0,15 over tid
    return mu + RNG.normal(0, 1, (S, T))
def evaluate(regime):
    res = {"1/N": [], "Momentum (Titan-lignende)": []}
    for _ in range(R):
        x = world(regime)
        port_all, port_m = [], []
        for t in range(12, T):
            l12 = x[:, t-12:t].mean(axis=1); l3 = x[:, t-3:t].mean(axis=1)
            sel = (l12 > 0) & (l3 > 0) & (l3 > l12)
            port_all.append(x[:, t].mean())
            port_m.append(x[sel, t].mean() if sel.any() else 0.0)
        for k, p in [("1/N", port_all), ("Momentum (Titan-lignende)", port_m)]:
            p = np.array(p); eq = np.cumsum(p)
            res[k].append((p.mean(), p.std(), p.mean() / p.std() * np.sqrt(12), (np.maximum.accumulate(eq) - eq).max()))
    for k, v in res.items():
        a = np.array(v)
        print(f"   {k:>27}: middel/md {a[:,0].mean():.3f}, Sharpe/år {a[:,2].mean():.2f}, største nedtur {a[:,3].mean():.2f}")
print("Verden A: konstant edge (ingen momentum i strategierne)"); evaluate(False)
print("Verden B: edge tænder/slukker i lange perioder (momentum findes)"); evaluate(True)
