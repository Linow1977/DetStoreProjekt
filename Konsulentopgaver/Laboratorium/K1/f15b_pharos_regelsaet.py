"""Forsøg 15b (K1): HELE Pharos' regelsæt (afsnit 4.3-4.5) kørt samlet, måned for måned i 60 måneder.
Score siden frysedato = (faktisk sum - lovet sum) / (lovet spredning * sqrt(måneder)). Papir regnes videre under pause.
Varianter:
 V1 (som skrevet): pause ved score < -2,33 (fra måned 3); genoptag efter >= 3 mdr. pause hvis score > -1,28;
    pension ved score < -3,0, ELLER 12 mdr. pause i træk, ELLER 2 pauser inden for 24 mdr.
 V2: som V1, men KUN pension ved score < -3,0 (ingen 12-måneders- og 2-pause-regel).
 V3: som V1, men genoptag når score > -2,0 (lavere tærskel).
 V4: kun pension ved -3,0 og ingen pauser for dårlige resultater.
Nedturs-båndene er ikke med i modellen (kun scoren)."""
import numpy as np
RNG = np.random.default_rng(151)
N, M = 50_000, 60
def sim(frac, sharpe, variant):
    mu = sharpe / np.sqrt(12)
    r = RNG.normal(mu * frac, 1.0, (N, M))
    cs = np.cumsum(r, axis=1); k = np.arange(1, M + 1)
    score = (cs - k * mu) / np.sqrt(k)
    retired_at = np.full(N, np.nan); paused_ever = np.zeros(N, bool)
    resume_thr = -2.0 if variant == "V3" else -1.28
    for i in range(N):
        paused = False; pstart = None; pauses = []
        for t in range(2, M):
            s = score[i, t]
            if s < -3.0: retired_at[i] = t + 1; break
            if variant == "V4": continue
            if not paused:
                if s < -2.33:
                    paused = True; pstart = t; paused_ever[i] = True; pauses.append(t)
                    if variant != "V2" and len([p for p in pauses if t - p < 24]) >= 2:
                        retired_at[i] = t + 1; break
            else:
                if variant != "V2" and t - pstart >= 12: retired_at[i] = t + 1; break
                if t - pstart >= 3 and s > resume_thr: paused = False
    return np.mean(~np.isnan(retired_at)), paused_ever.mean(), np.nanmedian(retired_at)
print("GOD strategi (leverer præcis som lovet), 60 måneder:")
for v in ["V1", "V2", "V3", "V4"]:
    pr, pp, _ = sim(1.0, 1.0, v)
    print(f"  {v}: pensioneret {pr:.1%}, sat på pause mindst én gang {pp:.1%}")
print("DØD edge (gennemsnit 0 fra frysedatoen), andel pensioneret inden 60 mdr. (median måned):")
for s in [1.0, 2.0]:
    out = []
    for v in ["V1", "V2", "V3", "V4"]:
        pr, pp, med = sim(0.0, s, v)
        out.append(f"{v} {pr:.0%} ({med:.0f})")
    print(f"  lovet Sharpe {s}: " + ", ".join(out))
