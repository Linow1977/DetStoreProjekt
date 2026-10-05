"""Udvidelse af konsulentgruppens forsøg 2 (K1), 5. okt 2026: faste grænser 15, 30, 40 og 50 % tilføjet, N = 100.000.
Original: Konsulentopgaver/Laboratorium/K1/f2_oos_regel.py på grenen claude/dreamy-lamport-eztlk0.
"""
"""Forsøg 2 (K1): Hvor tit smider OOS-reglen en ægte edge væk, og hvor tit slipper en falsk igennem?

Sammenligner tre regler for "holder i OOS":
  A) fast 10 %:   OOS-netto >= 0,90 x IS-netto
  B) fast 20 %:   OOS-netto >= 0,80 x IS-netto
  C) K1-reglen:   OOS-netto > 0  OG  OOS-netto >= IS-netto - 1,28 x S_aar
     hvor S_aar er ESTIMERET fra 20 kvartalstal (spredning / sqrt(4)), som i del1 afsnit D.

Model (opdigtet): en celle har en sand gennemsnitsbevægelse mu pr. kvartal. Hvert kvartal
måles mu + støj (sd = sigma_q). IS = gennemsnit af 20 kvartaler (2020-2024), OOS = gennemsnit
af 4 kvartaler (2025). Enheder: sigma_q sat så IS-t = sand t (uden udvælgelse).

Del 1: ægte, uændret edge, uden udvælgelse (ren støj-effekt).
Del 2: med udvælgelse ("vinderens forbandelse"): en population af celler, hvor kun dem med
       IS-t >= tærskel går videre. Ægte har sand t = 4 eller 5; falske har sand t = 0.
Del 3: "regimeskift": kvartalsstøj større end dagsstøjen tilsiger (edge svinger mellem kvartaler).
"""
import numpy as np

RNG = np.random.default_rng(7)
Z = 1.28
N = 100_000


def measure(true_t, n, extra_quarter_sd=0.0):
    """Returnerer IS-gennemsnit, OOS-gennemsnit og estimeret S_aar for n celler."""
    # Vælg enheder: IS-standardfejl = 1  => kvartals-sd = sqrt(20)
    sd_q = np.sqrt(20.0)
    mu = np.broadcast_to(np.asarray(true_t, dtype=float), (n,))
    quarter_shift = RNG.normal(0, extra_quarter_sd, (n, 24)) if extra_quarter_sd > 0 else 0.0
    quarters = mu[:, None] + quarter_shift + RNG.normal(0, sd_q, (n, 24))
    is_q, oos_q = quarters[:, :20], quarters[:, 20:]
    is_mean = is_q.mean(axis=1)
    oos_mean = oos_q.mean(axis=1)
    s_year_quarters = is_q.std(axis=1, ddof=1) / 2.0
    s_year_clean = np.sqrt(5.0)  # dag-klynget SE (=1) x sqrt(5)
    s_year = np.maximum(s_year_quarters, s_year_clean)
    return is_mean, oos_mean, s_year


def rules(is_mean, oos_mean, s_year):
    return {
        "fast 10%": oos_mean >= 0.90 * is_mean,
        "fast 15%": oos_mean >= 0.85 * is_mean,
        "fast 20%": oos_mean >= 0.80 * is_mean,
        "fast 30%": oos_mean >= 0.70 * is_mean,
        "fast 40%": oos_mean >= 0.60 * is_mean,
        "fast 50%": oos_mean >= 0.50 * is_mean,
        "K1 z=1,28": (oos_mean > 0) & (oos_mean >= is_mean - Z * s_year),
        "K1 z=1,0": (oos_mean > 0) & (oos_mean >= is_mean - 1.0 * s_year),
        "kun >0": oos_mean > 0,
    }


def main():
    print("Del 1: ÆGTE, uændret edge, ingen udvælgelse. Andel SMIDT UD af ren støj:")
    header = f"{'sand t (5 år)':>14} | " + " | ".join(f"{k:>10}" for k in rules(*measure(1, 10)))
    print(header)
    for t in [3, 4, 5, 6, 8]:
        r = rules(*measure(t, N))
        print(f"{t:>14} | " + " | ".join(f"{1 - v.mean():>10.1%}" for v in r.values()))

    print("\nDel 2: MED udvælgelse (kun IS-t >= tærskel går til OOS).")
    print("Andel ægte smidt ud / andel falske der slipper igennem:")
    for threshold in [4.0, 4.5]:
        for true_t in [4, 5]:
            is_r, oos_r, s_r = measure(true_t, N)
            keep_r = is_r >= threshold
            is_f, oos_f, s_f = measure(0, 20 * N)
            keep_f = is_f >= threshold
            rr = rules(is_r[keep_r], oos_r[keep_r], s_r[keep_r])
            rf = rules(is_f[keep_f], oos_f[keep_f], s_f[keep_f])
            print(f"  tærskel {threshold}, ægte sand t={true_t} (ægte valgt: {keep_r.mean():.0%}; "
                  f"falske valgt: {keep_f.sum()} af {20 * N:,}):")
            for k in rr:
                print(f"     {k:>10}: ægte smidt ud {1 - rr[k].mean():6.1%} | falske igennem {rf[k].mean():6.1%}")

    print("\nDel 3: edge svinger mellem kvartaler (ekstra kvartals-sd = 2 x den rene).")
    is_r, oos_r, s_r = measure(5, N, extra_quarter_sd=2 * np.sqrt(20))
    r = rules(is_r, oos_r, s_r)
    ratio = np.median(s_r / np.sqrt(5.0))
    print(f"  median S_aar(kvartal) / S_aar(ren) = {ratio:.2f}  (>1,5 => mærkes 'ustabil')")
    for k, v in r.items():
        print(f"     {k:>10}: ægte smidt ud {1 - v.mean():6.1%}")


if __name__ == "__main__":
    main()
