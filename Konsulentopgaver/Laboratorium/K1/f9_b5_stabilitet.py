"""Forsøg 9 (K1): Hvor mange ÆGTE edges smider stabilitets-kravet B5 ud, og hvor mange FALSKE fanger det?
B5 (del1): netto > 0 i >= 4 af 5 år OG >= 12 af 20 kvartaler; bedste år <= 40 % af nettogevinsten;
uden bedste kalendermåned stadig > 0.
Opsætning: 60 måneder; hver måned = sand edge + støj. Enhed: IS-standardfejl for 5 år = 1, så
månedsstøj har sd sqrt(60). Ægte: sand t = 4, 5, 6 (edge ens hele tiden). Falske: sand t = 0,
kun dem der når IS-t >= 4 (udvalgte). Også: ægte edge, der kun virker i 3 af 5 år (burde afvises)."""
import numpy as np
RNG = np.random.default_rng(9)

def b5(months):
    total = months.sum(axis=1)
    years = months.reshape(-1, 5, 12).sum(axis=2)
    quarters = months.reshape(-1, 20, 3).sum(axis=2)
    ok_years = (years > 0).sum(axis=1) >= 4
    ok_q = (quarters > 0).sum(axis=1) >= 12
    ok_best_year = years.max(axis=1) <= 0.4 * total
    ok_month = (total - months.max(axis=1)) > 0
    return ok_years & ok_q & ok_best_year & ok_month & (total > 0), dict(
        år=ok_years, kvartaler=ok_q, bedste_år=ok_best_year, uden_bedste_måned=ok_month)

def sim(mu_per_month, n):
    return mu_per_month + RNG.normal(0, np.sqrt(60), (n, 60))

print("Forsøg 9: stabilitets-kravet B5")
for t in [4, 5, 6]:
    m = sim(t, 200_000)            # sum over 60 måneder har middel 60*t/60... skaler:
    m = m / 60 * 1.0               # enhed: gennemsnit pr. måned; t = total/ (sd_total)
    ok, parts = b5(m * 60)
    print(f"  ÆGTE sand t={t}: består B5 {ok.mean():.1%}  | delkrav: " +
          ", ".join(f"{k} {v.mean():.0%}" for k, v in parts.items()))
# falske udvalgt ved IS-t >= 4
m = sim(0, 4_000_000)
t_is = m.sum(axis=1) / np.sqrt(60 * 60)
sel = m[t_is >= 4]
ok, parts = b5(sel)
print(f"  FALSKE med IS-t>=4 (n={len(sel)}): består B5 {ok.mean():.1%} | delkrav: " +
      ", ".join(f"{k} {v.mean():.0%}" for k, v in parts.items()))
# ægte edge kun i 3 af 5 år (sand t over hele perioden = 5)
mu = np.zeros(60); mu[:36] = 5 * 60 / 36
m = mu + RNG.normal(0, np.sqrt(60), (200_000, 60))
ok, parts = b5(m)
print(f"  Edge KUN i 3 af 5 år (samlet t=5): består B5 {ok.mean():.1%} (burde være lav) | " +
      ", ".join(f"{k} {v.mean():.0%}" for k, v in parts.items()))
