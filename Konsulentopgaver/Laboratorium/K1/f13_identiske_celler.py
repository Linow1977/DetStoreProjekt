"""Forsøg 13 (K1): Seriefunktions-fejlen giver ENS signaler i alle 625 celler [Repo, via Overordnet:
RawSignal069: 480 signaler gentaget 625 gange]. Hvad gør plateau-trappen med det, og kan en simpel
kontrol ("gitter ugyldigt") skelne et fejlramt gitter fra et rigtigt?
Del 1: plateau-niveau for et gitter, hvor alle celler har samme t-tal.
Del 2: overlap af signaltider (andel fælles signaler) mellem LANGT fra hinanden liggende celler
(hjørner og midter af kanterne) i (a) et rigtigt opdigtet filter fra forsøg 10 på 20 markeder og
(b) et fejlramt gitter (alle celler = samme signaler). Kontrol: gitter ugyldigt, hvis medianen af
overlap mellem fjerne celler >= 0,99 (samme grænse som B11 i del1)."""
import numpy as np, plateau
from plateau import plateau_level
import f10_lokkedue_realistisk as f10
plateau.RELATIVE_GREEN = 0.0
print("Del 1: gitter med ens t-tal i alle 625 celler")
for t in [1.5, 2.0, 3.0, 4.5]:
    g = np.full((25, 25), t, dtype=np.float32)
    print(f"  alle celler t={t}: midtens plateau-niveau = PL{plateau_level(g, 12, 12)}")
def overlap(a, b):
    a, b = set(a), set(b)
    return len(a & b) / max(1, min(len(a), len(b)))
far = [((0, 0), (24, 24)), ((0, 24), (24, 0)), ((0, 12), (24, 12)), ((12, 0), (12, 24))]
ok_real = []
for k in range(20):
    o, h, c = f10.make_market()
    starts = {}
    for i, n1 in [(0, 5), (12, 17), (24, 29)]:
        for j, n2 in [(0, 10), (12, 34), (24, 58)]:
            on = (c > f10.rolling_max_prev(h, n1)) & (c > f10.rolling_mean(c, n2))
            starts[(i, j)] = np.flatnonzero(on[1:] & ~on[:-1]) + 1
    ok_real.append(np.median([overlap(starts[a], starts[b]) for a, b in far]))
bug = np.arange(480)
ok_bug = np.median([overlap(bug, bug) for _ in far])
print("Del 2: median overlap mellem fjerne celler")
print(f"  rigtigt filter (20 markeder): min {min(ok_real):.2f}, median {np.median(ok_real):.2f}, max {max(ok_real):.2f}")
print(f"  fejlramt gitter: {ok_bug:.2f}")
print(f"  kontrol (>= 0,99 = ugyldigt, som B11): rigtige markeret ugyldige {np.mean(np.array(ok_real) >= 0.99):.0%}, fejlramt markeret: {ok_bug >= 0.99}")
