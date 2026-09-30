"""Forsøg 1 (K1): Hvor meget puster klumpede signaler t-tallet op?

Spørgsmål: Hvis signaler klumper sig på få dage, og signaler samme dag deler en
fælles "dagsbevægelse", hvor meget for stort bliver t-tallet, når man tæller hvert
signal som uafhængigt? Og hvad sker der med en tilfældig-kontrol, der bruger
tilfældige enkelttidspunkter (panelets forslag) i stedet for at bevare klumpningen?

Model (opdigtet, ingen edge = nul-hypotesen):
- 1.250 handelsdage (5 år).
- En dag er "aktiv" for filteret med sandsynlighed p; en aktiv dag har Poisson(m) signaler.
- Bevægelse efter signal i på dag d:  r = a_d + e_i,  hvor a_d ~ N(0, rho) er en fælles
  dagskomponent og e_i ~ N(0, 1-rho). Ingen edge: middelværdi 0.
- Naivt t: alle signaler som uafhængige.
- Dag-klynget t: signaler lagt sammen pr. dag (samme formel som K2's 5.3).
- "Tilfældige tidspunkter": samme antal signaler, men spredt jævnt over alle dage
  (ingen klumpning). Markedets dagskomponent er den samme.
Hvis t-tallet er rigtigt regnet, skal dets spredning under nul-hypotesen være ca. 1.
"""
import numpy as np

RNG = np.random.default_rng(20260929)
N_DAYS = 1250
N_SIM = 2000


def simulate(p_active, mean_per_day, rho, clustered=True):
    naive_t = np.empty(N_SIM)
    cluster_t = np.empty(N_SIM)
    for s in range(N_SIM):
        day_component = RNG.normal(0.0, np.sqrt(rho), N_DAYS)
        if clustered:
            active = RNG.random(N_DAYS) < p_active
            counts = np.where(active, RNG.poisson(mean_per_day, N_DAYS), 0)
        else:
            total = RNG.poisson(p_active * mean_per_day * N_DAYS)
            counts = np.bincount(RNG.integers(0, N_DAYS, total), minlength=N_DAYS)
        n = counts.sum()
        # Sum og kvadratsum pr. dag uden at lave hvert signal: sum af e over n_d signaler
        e_sum = RNG.normal(0.0, np.sqrt((1 - rho) * np.maximum(counts, 1))) * (counts > 0)
        day_sum = counts * day_component + e_sum
        mean = day_sum.sum() / n
        # Naiv varians: sum over signaler (r - mean)^2. Regnes eksakt via dagsdele:
        # r_i = a_d + e_i; brug simulation af e_i's kvadratsum ~ (1-rho)*chi2(n_d)
        # Eksakt: kvadratsum = (1-rho)*chi2(n_d - 1) + (sum e)^2 / n_d  (normalfordelt e)
        safe_counts = np.maximum(counts, 1)
        chi = np.where(counts > 1, RNG.chisquare(np.maximum(counts - 1, 1)), 0.0)
        e_sq = ((1 - rho) * chi + e_sum ** 2 / safe_counts) * (counts > 0)
        # sum r^2 = sum_d [n_d a_d^2 + 2 a_d e_sum_d + e_sq_d]
        sum_r2 = (counts * day_component ** 2 + 2 * day_component * e_sum + e_sq).sum()
        var_naive = (sum_r2 - n * mean ** 2) / (n - 1)
        naive_t[s] = mean / np.sqrt(var_naive / n)
        used = counts > 0
        D = used.sum()
        resid = day_sum[used] - mean * counts[used]
        se = np.sqrt(D / (D - 1) * (resid ** 2).sum()) / n
        cluster_t[s] = mean / se
    return naive_t, cluster_t


def main():
    print("Forsøg 1: klumpning. Spredning af t under 'ingen edge' (skal være ca. 1,0)")
    print(f"{'aktive dage':>11} {'sign./aktiv dag':>15} {'rho':>5} | {'naivt t':>8} {'dag-klynget t':>13} | "
          f"{'oppustning':>10} | {'andel |t|>3 naivt':>18} {'dag-klynget':>11}")
    settings = [(0.3, 10, 0.1), (0.3, 10, 0.3), (0.3, 40, 0.1), (0.3, 40, 0.3), (0.3, 40, 0.5), (0.1, 40, 0.3)]
    for p, m, rho in settings:
        nt, ct = simulate(p, m, rho, clustered=True)
        print(f"{p:>11.0%} {m:>15} {rho:>5.1f} | {nt.std():>8.2f} {ct.std():>13.2f} | {nt.std() / ct.std():>9.1f}x | "
              f"{np.mean(np.abs(nt) > 3):>18.1%} {np.mean(np.abs(ct) > 3):>11.2%}")
    print()
    print("Tilfældige tidspunkter (panelets kontrol) vs. ægte klumpet signal, rho=0.3, 30% aktive dage, 40/dag:")
    nt_c, ct_c = simulate(0.3, 40, 0.3, clustered=True)
    nt_u, ct_u = simulate(0.3, 40, 0.3, clustered=False)
    print(f"  Ægte klumpet signal (uden edge): naivt t spredning {nt_c.std():.2f}")
    print(f"  Tilfældige tidspunkter:          naivt t spredning {nt_u.std():.2f}")
    thr_uniform = np.quantile(nt_u, 0.99)
    print(f"  Tærskel sat af tilfældige tidspunkter (1% falske): t >= {thr_uniform:.2f}; "
          f"andel ægte-klumpede støjceller over den: {np.mean(nt_c >= thr_uniform):.1%} (burde være 1%)")


if __name__ == "__main__":
    main()
