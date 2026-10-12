"""test_pharos_proto.py -- tests med kendt svar for Pharos' beregningsmotor. KUN OPDIGTEDE DATA.
Kør: <lab-venv>/bin/python -m unittest -v test_pharos_proto"""

import unittest

import numpy as np

import pharos_proto as ph


def kalender(n=260):
    d = np.arange(np.datetime64("2026-01-05"), np.datetime64("2026-01-05") + 400)
    d = d[((d.astype("int64") - 4) % 7) < 5]
    return d[:n]


def strategi(sid, marked="ES", retning="LANG", dagstab=300_000, dagstab99=200_000, start=None):
    return ph.Strategi(sid, marked, retning, dagstab, dagstab99, forv_maaned=20_000, sd_maaned=60_000,
                       nedtur95=150_000, nedtur99=250_000, start=start)


def data(n_strat, n_dage=260, seed=1, sd=8_000):
    rng = np.random.default_rng(seed)
    P = np.rint(rng.normal(500, sd, (n_strat, n_dage))).astype(np.int64)
    return P, np.ones_like(P, dtype=bool)


class P1_IngenFremtidsviden(unittest.TestCase):
    def test_data_efter_as_of_aendrer_intet(self):
        d = kalender(); P, har = data(3)
        S = [strategi(f"S{i}", start=d[0]) for i in range(3)]
        as_of = d[150]
        f1, h1 = ph.koer_maaned(d, P, har, S, d, as_of)
        P2 = P.copy(); P2[:, 151:] = -10_000_000          # katastrofe EFTER as-of
        f2, h2 = ph.koer_maaned(d, P2, har, S, d, as_of)
        self.assertEqual(h1, h2); self.assertEqual(f1, f2)


class P2_Stoerrelse(unittest.TestCase):
    def test_fast_broekdel_af_risikomaal(self):
        d = kalender(60); P, har = data(1, 60, sd=100)
        regler = dict(ph.STANDARD_REGLER, risiko_pr_strategi=0.01, loft_pr_marked=1.0, loft_pr_retning=1.0)
        # risikomål = største af værste dagstab (300.000) og 99 %-dagstab (200.000) = 300.000
        S = [strategi("S0", dagstab=300_000, dagstab99=200_000, start=d[0])]
        f, _ = ph.koer_maaned(d, P, har, S, d, d[-1], regler)
        self.assertEqual(f[0]["kontrakter"], 3)          # 1.000.000 // 300.000
        # nu er 99 %-dagstabet størst (400.000) -> 1.000.000 // 400.000 = 2
        S = [strategi("S0", dagstab=300_000, dagstab99=400_000, start=d[0])]
        f, _ = ph.koer_maaned(d, P, har, S, d, d[-1], regler)
        self.assertEqual(f[0]["kontrakter"], 2)


class P2b_SamletRisiko(unittest.TestCase):
    def test_f_er_mindste_af_05_procent_og_10_procent_delt_med_antal(self):
        d = kalender(60); P, har = data(30, 60, sd=100)
        S = [strategi(f"S{i}", marked=f"M{i}", retning=["LANG", "KORT"][i % 2], dagstab=10_000, dagstab99=0, start=d[0])
             for i in range(30)]
        regler = dict(ph.STANDARD_REGLER, loft_pr_marked=1.0, loft_pr_retning=1.0)
        f, _ = ph.koer_maaned(d, P, har, S, d, d[-1], regler)
        # 30 strategier: f = min(0,5 %, 10 %/30 = 0,333 %) -> 333.333 øre // 10.000 = 33 kontrakter
        self.assertEqual({x["kontrakter"] for x in f}, {33})


class P3_LoftPrMarked(unittest.TestCase):
    def test_marked_over_25_procent_af_risikobudgettet_skaleres_ned(self):
        d = kalender(60); P, har = data(4, 60, sd=100)
        S = [strategi("A", "ES", "LANG", start=d[0]), strategi("B", "ES", "KORT", start=d[0]),
             strategi("C", "NQ", "LANG", start=d[0]), strategi("D", "CL", "KORT", start=d[0])]
        regler = dict(ph.STANDARD_REGLER, risiko_pr_strategi=0.01)   # loft 25 % pr. marked, 60 % pr. retning
        f, _ = ph.koer_maaned(d, P, har, S, d, d[-1], regler)
        # hver: 1.000.000 // 300.000 = 3 kontrakter = 900.000 risiko. Budget = 4 x 1.000.000 = 4.000.000.
        # ES: 1.800.000 > 25 % = 1.000.000 -> 3 x 1.000.000 // 1.800.000 = 1 hver. Retning: LANG 1+3, KORT 1+3 -> 1.200.000 < 2.400.000.
        self.assertEqual([x["kontrakter"] for x in f], [1, 1, 3, 3])


class P4_TvillingerTaellerDobbelt(unittest.TestCase):
    def test_ens_strategier_rammer_samlet_loft_uafhaengige_goer_ikke(self):
        d = kalender(); P1, har = data(1, sd=30_000, seed=3); P2, _ = data(1, sd=30_000, seed=4)
        S = [strategi("A", start=d[0], marked="ES", retning="LANG"), strategi("B", start=d[0], marked="NQ", retning="KORT")]
        regler = dict(ph.STANDARD_REGLER, risiko_pr_strategi=0.01, loft_pr_marked=1.0, loft_pr_retning=1.0, mc_runder=500)
        # find loftet ud fra de uafhængige, og sæt det lidt over deres 99 %-nedtur
        uaf = np.vstack([P1, P2]); tvil = np.vstack([P1, P1])
        k = np.array([3, 3])
        dd_uaf = ph.portefoelje_nedtur99(uaf, k, 500, 20, 1)
        dd_tvil = ph.portefoelje_nedtur99(tvil, k, 500, 20, 1)
        self.assertGreater(dd_tvil, dd_uaf * 1.2)          # tvillinger = næsten dobbelt risiko
        regler["loft_samlet_nedtur99"] = (dd_uaf * 1.05) / regler["kapital"]
        f_uaf, _ = ph.koer_maaned(d, uaf, np.ones_like(uaf, bool), S, d, d[-1], regler)
        f_tvil, _ = ph.koer_maaned(d, tvil, np.ones_like(tvil, bool), S, d, d[-1], regler)
        self.assertEqual(sum(x["kontrakter"] for x in f_uaf), 6)
        self.assertLess(sum(x["kontrakter"] for x in f_tvil), 6)


class P5_SammeTalHverGang(unittest.TestCase):
    def test_to_koersler_samme_fingeraftryk(self):
        d = kalender(); P, har = data(5)
        S = [strategi(f"S{i}", marked=["ES", "NQ", "CL"][i % 3], start=d[0]) for i in range(5)]
        a = ph.koer_maaned(d, P, har, S, d, d[-1])
        b = ph.koer_maaned(d, P.copy(), har.copy(), S, d, d[-1])
        self.assertEqual(a[1], b[1])


class P6_Fuldstaendighed(unittest.TestCase):
    def test_manglende_dag_giver_ingen_liste(self):
        d = kalender(); P, har = data(2)
        har[1, 100] = False
        S = [strategi("S0", start=d[0]), strategi("S1", start=d[0])]
        with self.assertRaises(ph.KraeverDig):
            ph.koer_maaned(d, P, har, S, d, d[-1])


class P7_PensioneretErEndeligt(unittest.TestCase):
    def test_pensioneret_kommer_ikke_igen_og_faar_0_kontrakter(self):
        d = kalender(); P, har = data(1, sd=100)
        S = [strategi("S0", start=d[0])]; S[0].status = "PENSIONERET"
        f, _ = ph.koer_maaned(d, P, har, S, d, d[-1])
        self.assertEqual(f[0]["handling"], "PENSIONERET"); self.assertEqual(f[0]["kontrakter"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
