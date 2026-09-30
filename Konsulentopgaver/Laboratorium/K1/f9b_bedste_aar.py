"""Forsøg 9b: grænsen for 'bedste år' (40 % mod 50 %) — ægte (t=4,5), edge kun i 3 af 5 år, og kun i 2 af 5 år."""
import numpy as np
RNG = np.random.default_rng(91)
def share_ok(mu, lim, n=200_000):
    m = mu + RNG.normal(0, np.sqrt(60), (n, 60))
    y = m.reshape(n, 5, 12).sum(axis=2); tot = y.sum(axis=1)
    return np.mean((tot > 0) & (y.max(axis=1) <= lim * tot) & ((y > 0).sum(axis=1) >= 4))
for lim in [0.4, 0.5]:
    out = []
    for name, mu in [("ægte t=4", np.full(60, 4.0)), ("ægte t=5", np.full(60, 5.0)),
                     ("kun 3 af 5 år (t=5)", np.r_[np.full(36, 5*60/36), np.zeros(24)]),
                     ("kun 2 af 5 år (t=5)", np.r_[np.full(24, 5*60/24), np.zeros(36)])]:
        out.append(f"{name}: {share_ok(mu, lim):.0%}")
    print(f"bedste år <= {lim:.0%} + >=4 af 5 år positive:  " + " | ".join(out))
