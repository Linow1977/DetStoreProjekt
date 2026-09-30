"""Forsøg 11 (K1): Hjælper det at måle OVERSKUD over den gennemsnitlige bevægelse på samme klokkeslæt?
Spørgsmål: Markedet har et fast klokkeslæts-mønster (her: opdrift i den første time) og generel opdrift.
Et filter uden edge, der tænder oftere om morgenen, ser så godt ud. Fjerner "overskud over
klokkeslæts-gennemsnittet" (del1 B.1) det? Og koster det noget, når der ER en edge?
Opsætning: som forsøg 10 (f10_lokkedue_realistisk.py), men minut-afkast får +0,02 i dagens første
60 minutter. 150 markeder. Mål: t (dag-klynget) på (a) rå bevægelse, (b) overskud. Plus en plantet
edge: efter signaler i cellerne N1 in 12..16 lægges +1,5 x (typisk 60-min sd / 10) ind i de næste 60 min
(midlertidigt; ingen varig drift)."""
import numpy as np
import f10_lokkedue_realistisk as f10
RNG = np.random.default_rng(1111)
f10.RNG = RNG
B, BPD, H = f10.BAR, f10.BARS_PER_DAY, f10.H

def make_market(morning_drift):
    log_vol = np.zeros(f10.DAYS)
    for d in range(1, f10.DAYS):
        log_vol[d] = 0.98 * log_vol[d-1] + RNG.normal(0, 0.15)
    u = np.linspace(-1, 1, f10.MIN_PER_DAY)
    shocks = RNG.standard_t(4, (f10.DAYS, f10.MIN_PER_DAY)) / np.sqrt(2.0)
    rets = 0.002 + shocks * np.exp(log_vol)[:, None] * (1 + 0.8 * u ** 2)[None, :]
    rets[:, :60] += morning_drift
    return rets

def bars(rets):
    price = 1000 + np.cumsum(rets.ravel())
    p = price.reshape(-1, B)
    opens = np.r_[1000.0, price[:-1]].reshape(-1, B)[:, 0]
    return opens, p.max(axis=1), p[:, -1]

def t_both(starts, opens, closes, baseline):
    idx = starts
    entry = idx + 1; ex = entry + H - 1
    ok = (entry // BPD == idx // BPD) & (ex // BPD == idx // BPD)
    entry, ex = entry[ok], ex[ok]
    move = closes[ex] - opens[entry]
    day = entry // BPD
    return f10.day_t(day, move), f10.day_t(day, move - baseline[entry % BPD])

res = {"rå": [], "overskud": []}
res_edge = {"rå": [], "overskud": []}
for k in range(150):
    rets = make_market(0.02)
    opens, highs, closes = bars(rets)
    # klokkeslæts-gennemsnit af 60-min bevægelse for hver bar-position
    nb = len(opens); pos = np.arange(nb) % BPD
    ent = np.arange(nb - H); ex = ent + H - 1
    same = (ex // BPD) == (ent // BPD)
    mv = closes[ex[same]] - opens[ent[same]]
    baseline = np.zeros(BPD)
    for p_ in range(BPD):
        m = pos[ent[same]] == p_
        baseline[p_] = mv[m].mean() if m.any() else 0.0
    n1, n2 = 10, 20
    on = (closes > f10.rolling_max_prev(highs, n1)) & (closes > f10.rolling_mean(closes, n2))
    starts = np.flatnonzero(on[1:] & ~on[:-1]) + 1
    starts = starts[starts < nb - H - 1]
    a, b = t_both(starts, opens, closes, baseline)
    res["rå"].append(a); res["overskud"].append(b)
    # plantet edge: +edge over de næste H bars efter hvert signal (midlertidig, fjernes igen)
    rets2 = rets.copy().ravel()
    sd60 = np.std(mv)
    add = 1.5 * sd60 / 10 / (H * B)
    for s in starts:
        m0 = (s + 1) * B
        rets2[m0:m0 + H * B] += add
        rets2[m0 + H * B:m0 + 2 * H * B] -= add
    o2, h2, c2 = bars(rets2.reshape(rets.shape))
    a, b = t_both(starts, o2, c2, baseline)
    res_edge["rå"].append(a); res_edge["overskud"].append(b)
print("Forsøg 11: morgen-opdrift i markedet, filter N1=10, N2=20, 150 markeder")
for name in ["rå", "overskud"]:
    x = np.array(res[name]); y = np.array(res_edge[name])
    print(f"  {name:>9}: UDEN edge t middel {x.mean():+.2f} (sd {x.std():.2f}), andel t>2 {np.mean(x>2):.0%} | "
          f"MED plantet edge t middel {y.mean():+.2f}, andel t>=4 {np.mean(y>=4):.0%}")
