"""
forsoeg2.py -- Forsøg F3b, F6 og F7 for Konsulent 2. KUN OPDIGTEDE DATA.
Kør:  <lab-venv>/bin/python forsoeg2.py > resultater2.txt
"""

import os
import tempfile
import time

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

import rsa_proto as rp
from forsoeg import BAR, HORISONT, N1, N2, celle_resultater, skriv, us_helligdage


def plant_delvis(md, indgang_idx, andel, seed, midlertidig=False):
    """+1 tick i løbet af de næste 60 minutter efter en tilfældig 'andel' af indgangene
    -> gennemsnitlig plantet edge ~ andel ticks pr. signal (brøkdele af et tick)."""
    rng = np.random.default_rng(seed)
    valgt = np.unique(indgang_idx)
    valgt = valgt[rng.random(len(valgt)) < andel]
    skub = np.zeros(len(md.luk), dtype=np.int64)
    mins = valgt + rng.integers(0, 60, len(valgt))
    mins = mins[mins < len(skub)]
    np.add.at(skub, mins, 1)
    if midlertidig:
        # tag ticket tilbage 60-120 min senere -> ingen varig drift i prisserien (ren 'timing'-edge)
        tilbage = valgt + rng.integers(60, 120, len(valgt))
        tilbage = tilbage[tilbage < len(skub)]
        np.add.at(skub, tilbage, -1)
    kum = np.cumsum(skub)
    kum_foer = np.r_[0, kum[:-1]]
    return rp.Minutdata(md.stempel, (md.aabn + kum_foer).astype(np.int32), (md.hoej + kum).astype(np.int32),
                        (md.lav + kum_foer).astype(np.int32), (md.luk + kum).astype(np.int32), md.dag, md.minut_nr)


def main():
    kal = rp.lav_kalender("2020-01-01", "2024-12-31", helligdage=us_helligdage())

    # ---------------------------------------------------------------- F3b: styrke (power)
    skriv("=== F3b: Hvor lille en edge kan kæden finde? (plantet i 7x7-området, brøkdele af et tick) ===")
    md = rp.lav_minutdata(kal, seed=21, sigma=2.0, uro_klumper=True, mangler=0.002)
    bars = rp.byg_bars(md, kal, BAR)
    sig = rp.lav_signaler(bars, N1, N2)
    r0, ev = celle_resultater(md, sig, HORISONT)
    region = (sig.n1_idx >= 9) & (sig.n1_idx <= 15) & (sig.n2_idx >= 9) & (sig.n2_idx <= 15)
    ind = ev.indgang_idx[region & ev.gyldig]
    inde = np.zeros((25, 25), bool); inde[9:16, 9:16] = True
    for andel in (0.05, 0.1, 0.2, 0.4):
        md_p = plant_delvis(md, ind, andel, seed=int(andel * 100))
        r, _ = celle_resultater(md_p, sig, HORISONT)
        d_m = r["m"] - r0["m"]
        NOK = (r["dage"] >= 150) & (r["n"] >= 300)
        pl = rp.plateau_gitter(r["m"], r["t"], NOK)
        skriv(f"andel {andel:.2f}: plantet ~{np.median(d_m[inde]):.2f} ticks/signal inde (uden for {np.median(d_m[~inde]):.2f}); "
              f"t midte {r['t'][12,12]:.1f}; midte PL{pl[12,12]}; "
              f"celler med t>=4 og PL>=3: inde {np.sum((r['t']>=4)&(pl>=3)&inde)}/49, uden for {np.sum((r['t']>=4)&(pl>=3)&~inde)}/576")

    # ---------------------------------------------------------------- F6: trenddage og pustefaktor
    skriv("\n=== F6: Trenddage (fælles dags-drift, middel 0). Hvor meget pustes t op, hvis man tæller signaler? ===")
    rng = np.random.default_rng(5)
    for trend in (0.0, 0.1, 0.3):
        mdt = rp.lav_minutdata(kal, seed=31, sigma=2.0, uro_klumper=True, dags_trend=trend)
        barst = rp.byg_bars(mdt, kal, BAR)
        sigt = rp.lav_signaler(barst, N1, N2)
        tk, tn = [], []
        for runde in range(10):                      # lokkeduer: ingen ægte forbindelse til kursen
            w = int(rng.integers(4, 27))
            ny, ok, _, _ = rp.lokkedue_forskyd(sigt.starttid, kal, barst.stempel, w, "kalenderuger")
            s2 = rp.Signaler(sigt.n1_idx[ok], sigt.n2_idx[ok], ny[ok], sigt.antal_bars[ok], sigt.afsluttet[ok])
            rl, _ = celle_resultater(mdt, s2, HORISONT)
            tk.append(rl["t"].ravel()); tn.append(rl["t_naiv"].ravel())
        tk = np.concatenate(tk); tn = np.concatenate(tn)
        skriv(f"dags-trend {trend:.1f} ticks/min: lokkedue-t dag-klynget spredning {np.nanstd(tk):.2f}, "
              f"naivt spredning {np.nanstd(tn):.2f}; andel |t|>=3: klynget {np.nanmean(np.abs(tk)>=3):.3f}, "
              f"naivt {np.nanmean(np.abs(tn)>=3):.3f}; pustefaktor median {np.nanmedian(tn/tk):.2f}")

    # ---------------------------------------------------------------- F7: Parquet
    skriv("\n=== F7: Signal-linjer som Parquet: plads og læsetid ===")
    tabel = pa.table({
        "filter_id": pa.array(np.full(len(sig.starttid), 69, dtype=np.int16)),
        "barstr": pa.array(np.full(len(sig.starttid), BAR, dtype=np.int16)),
        "n1": pa.array(sig.n1_idx), "n2": pa.array(sig.n2_idx),
        "starttid": pa.array(sig.starttid), "antal_bars": pa.array(sig.antal_bars),
        "afsluttet": pa.array(sig.afsluttet),
    })
    with tempfile.TemporaryDirectory() as d:
        for komp in ("zstd", "snappy"):
            sti = os.path.join(d, f"s_{komp}.parquet")
            t0 = time.time()
            pq.write_table(tabel, sti, compression=komp,
                           use_dictionary=["filter_id", "barstr", "n1", "n2", "afsluttet"],
                           column_encoding={"starttid": "DELTA_BINARY_PACKED"})
            t_skriv = time.time() - t0
            st = os.path.getsize(sti)
            t0 = time.time()
            pq.read_table(sti)
            t_laes = time.time() - t0
            n = len(sig.starttid)
            skriv(f"{komp}: {st/1e6:.1f} MB for {n/1e6:.2f} mio. linjer = {st/n:.2f} bytes/linje; "
                  f"skriv {t_skriv:.2f} s, læs {t_laes:.2f} s ({n/t_laes/1e6:.0f} mio. linjer/s)")
        csv_bytes = sum(len(f"RawSignal069,{a},{b},2020-03-15 10:45,{c},{e}\n")
                        for a, b, c, e in zip(sig.n1_idx[:100000], sig.n2_idx[:100000],
                                              sig.antal_bars[:100000], sig.afsluttet[:100000])) / 100000
        skriv(f"Til sammenligning: samme linje som CSV-tekst ~{csv_bytes:.0f} bytes/linje")
        skriv("NB: signalerne her er sorteret efter (N1, N2, tid) som i TradeStation-filen; det hjælper pakningen.")


if __name__ == "__main__":
    main()
