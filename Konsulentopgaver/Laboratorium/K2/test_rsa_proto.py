"""
test_rsa_proto.py -- Tests med kendt svar for prototypen (numrene følger testplanen i del2_K2.md afsnit 10).
Kør:  <lab-venv>/bin/python -m unittest -v test_rsa_proto
KUN OPDIGTEDE DATA.
"""

import unittest

import numpy as np
import statsmodels.api as sm

import rsa_proto as rp


def lille_kalender(session_laengde=12):
    """Én handelsdag med en kort session, så resultaterne kan regnes i hånden."""
    kal = rp.lav_kalender("2020-01-06", "2020-01-06")          # en mandag
    kal.session_laengde[:] = session_laengde
    return kal


def haandlavet_minutdata(kal, minutter, aabn, hoej, lav, luk):
    minutter = np.array(minutter, dtype=np.int32)
    return rp.Minutdata(
        stempel=kal.session_aabning[0] + minutter.astype(np.int64),
        aabn=np.array(aabn, dtype=np.int32), hoej=np.array(hoej, dtype=np.int32),
        lav=np.array(lav, dtype=np.int32), luk=np.array(luk, dtype=np.int32),
        dag=np.zeros(len(minutter), dtype=np.int32), minut_nr=minutter)


class T1_BarByggingHaandregnet(unittest.TestCase):
    def test_fem_minutters_bars_med_hul_og_kort_sidste_bar(self):
        kal = lille_kalender(12)
        # minut 7 mangler (ingen handel)
        mins = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
        aabn = [100, 101, 102, 103, 104, 105, 107, 108, 109, 110, 111]
        luk = [101, 102, 103, 104, 105, 106, 108, 109, 110, 111, 112]
        hoej = [x + 2 for x in luk]
        lav = [x - 2 for x in aabn]
        md = haandlavet_minutdata(kal, mins, aabn, hoej, lav, luk)
        b = rp.byg_bars(md, kal, 5)
        s0 = int(kal.session_aabning[0])
        # Bar 1: minut 1-5, stemplet +5. Bar 2: minut 6,8,9,10, stemplet +10. Bar 3 (kort): 11-12, stemplet +12.
        self.assertEqual(list(b.stempel - s0), [5, 10, 12])
        self.assertEqual(list(b.aabn), [100, 105, 110])
        self.assertEqual(list(b.hoej), [107, 112, 114])
        self.assertEqual(list(b.lav), [98, 103, 108])
        self.assertEqual(list(b.luk), [105, 110, 112])


class T2_BarByggingModReference(unittest.TestCase):
    def test_hurtig_lig_langsom_alle_12_barstoerrelser(self):
        kal = rp.lav_kalender("2020-01-06", "2020-01-10", tidlig_luk=("2020-01-09",))
        md = rp.lav_minutdata(kal, seed=3, mangler=0.03)
        for n in range(5, 65, 5):
            a = rp.byg_bars(md, kal, n)
            b = rp.byg_bars_langsomt(md, kal, n)
            for felt in ("stempel", "aabn", "hoej", "lav", "luk"):
                np.testing.assert_array_equal(getattr(a, felt), getattr(b, felt), err_msg=f"{n} min {felt}")
            # egenskaber: høj >= åbn/luk, lav <= åbn/luk
            self.assertTrue(np.all(a.hoej >= np.maximum(a.aabn, a.luk)))
            self.assertTrue(np.all(a.lav <= np.minimum(a.aabn, a.luk)))


class T3_AlignmentFangerFejl(unittest.TestCase):
    def test_en_prisfejl_og_en_manglende_bar(self):
        kal = rp.lav_kalender("2020-01-06", "2020-01-07")
        md = rp.lav_minutdata(kal, seed=4)
        vores = rp.byg_bars(md, kal, 15)
        deres = rp.byg_bars(md, kal, 15)
        deres.luk = deres.luk.copy(); deres.luk[10] += 1               # én pris ændret
        keep = np.ones(len(deres.stempel), bool); keep[50] = False     # én bar slettet
        deres = rp.Bars(*(getattr(deres, f)[keep] for f in ("stempel", "aabn", "hoej", "lav", "luk", "dag")))
        f = rp.sammenlign_bars(vores, deres)
        self.assertEqual(len(f), 2)
        self.assertEqual(sorted(x[0] for x in f), ["ekstra hos os", "pris"])


class T4_EventMotorHaandregnet(unittest.TestCase):
    def test_indgang_naeste_minut_udgang_og_afkortning(self):
        kal = lille_kalender(12)
        mins = list(range(1, 13))
        aabn = [100 + 10 * i for i in range(12)]
        luk = [a + 5 for a in aabn]
        md = haandlavet_minutdata(kal, mins, aabn, [x + 1 for x in luk], [x - 1 for x in aabn], luk)
        s0 = int(kal.session_aabning[0])
        # Signal-bar lukker i minut 5 -> indgang = åbning af minut 6 (150).
        # Horisont 3 min -> udgang = luk på minut 8 (175). Brutto = 25.
        ev = rp.event_motor(md, np.array([s0 + 5]), 3)
        self.assertTrue(ev.gyldig[0]); self.assertEqual(int(ev.brutto[0]), 25); self.assertEqual(ev.grund[0], 0)
        # Horisont 30 min fra minut 6 -> afkortes til sidste minut (luk 215). Brutto = 65, mærket 3.
        ev = rp.event_motor(md, np.array([s0 + 5]), 30)
        self.assertEqual(int(ev.brutto[0]), 65); self.assertEqual(ev.grund[0], 3)
        # Signal på sidste bar i sessionen -> ingen indgang samme session -> udeladt (ingen næste minut)
        ev = rp.event_motor(md, np.array([s0 + 12]), 3)
        self.assertFalse(ev.gyldig[0])

    def test_sessionsskift_udelades(self):
        kal = rp.lav_kalender("2020-01-06", "2020-01-07")
        md = rp.lav_minutdata(kal, seed=5)
        sidste_minut_dag0 = int(kal.session_aabning[0] + kal.session_laengde[0])
        ev = rp.event_motor(md, np.array([sidste_minut_dag0]), 15)
        self.assertFalse(ev.gyldig[0]); self.assertEqual(ev.grund[0], 1)


class T5_FremtidsSnyd(unittest.TestCase):
    def test_priser_efter_X_paavirker_ikke_signaler_foer_X(self):
        kal = rp.lav_kalender("2020-01-01", "2020-03-31")
        md = rp.lav_minutdata(kal, seed=6)
        bars = rp.byg_bars(md, kal, 15)
        sig = rp.lav_signaler(bars, range(5, 10), range(1, 6))
        X = int(md.stempel[len(md.stempel) // 2])
        ev1 = rp.event_motor(md, sig.starttid, 60)
        # byt alle priser efter X ud med tilfældigt vrøvl
        md2 = rp.Minutdata(**{k: getattr(md, k).copy() for k in md.__dataclass_fields__})
        efter = md2.stempel > X
        rng = np.random.default_rng(0)
        for f in ("aabn", "hoej", "lav", "luk"):
            getattr(md2, f)[efter] = rng.integers(0, 99999, efter.sum())
        ev2 = rp.event_motor(md2, sig.starttid, 60)
        # udgangsminuttet for hvert signal
        i_ud_stempel = sig.starttid + 1 + 60   # øvre grænse for udgangstid
        foer = ev1.gyldig & (i_ud_stempel <= X)
        self.assertGreater(foer.sum(), 100)
        np.testing.assert_array_equal(ev1.brutto[foer], ev2.brutto[foer])

    def test_fejlagtig_indgang_paa_signalbaren_giver_falsk_edge_paa_stoej(self):
        """Den bevidste fejl (indgang på den bar, der skabte signalet) skal give et tydeligt
        'edge' på ren støj. Det viser, at null-testen (T11a) fanger kig-ind-i-fremtiden."""
        kal = rp.lav_kalender("2020-01-01", "2020-12-31")
        md = rp.lav_minutdata(kal, seed=7)
        bars = rp.byg_bars(md, kal, 15)
        sig = rp.lav_signaler(bars, [10], [3])
        rigtig = rp.event_motor(md, sig.starttid, 60)
        fejl = rp.event_motor(md, sig.starttid, 60, fejl_indgang_paa_signalbar=True)
        c = np.zeros(len(sig.starttid), dtype=np.int64)
        tr = rp.celle_tal(c[rigtig.gyldig], rigtig.dag[rigtig.gyldig], rigtig.brutto[rigtig.gyldig], 1)
        tf = rp.celle_tal(c[fejl.gyldig], fejl.dag[fejl.gyldig], fejl.brutto[fejl.gyldig], 1)
        self.assertLess(abs(tr["t"][0]), 4)       # rigtig motor: ingen edge i støj
        self.assertGreater(tf["t"][0], 10)        # fejlagtig motor: kæmpe falsk edge


class T6_Datovagt(unittest.TestCase):
    def test_pris_efter_testslut_stopper_analysen(self):
        kal = rp.lav_kalender("2020-01-06", "2020-01-10")
        md = rp.lav_minutdata(kal, seed=8)
        slut = int(md.stempel[-100])
        with self.assertRaises(rp.DatoFejl):
            rp.kontroller_datograense(md, slut)

    def test_signal_hvis_horisont_passerer_testslut_udelades(self):
        kal = rp.lav_kalender("2020-01-06", "2020-01-10")
        md = rp.lav_minutdata(kal, seed=8)
        slut = int(md.stempel[-1])
        ev = rp.event_motor(md, np.array([slut - 30]), 60, test_slut_stempel=slut)
        self.assertFalse(ev.gyldig[0]); self.assertEqual(ev.grund[0], 2)


class T7_DagKlyngetSEModStatsmodels(unittest.TestCase):
    def test_samme_tal_som_statsmodels(self):
        rng = np.random.default_rng(9)
        n = 5000
        dag = np.sort(rng.integers(0, 300, n))
        dagsstoej = rng.standard_normal(300)[dag] * 3      # signaler samme dag hænger sammen
        x = np.rint(1 + dagsstoej + rng.standard_normal(n) * 5)
        vores = rp.celle_tal(np.zeros(n, dtype=np.int64), dag, x, 1)
        res = sm.OLS(x, np.ones(n)).fit(cov_type="cluster", cov_kwds={"groups": dag})
        self.assertAlmostEqual(vores["m"][0], res.params[0], places=9)
        self.assertAlmostEqual(vores["se"][0], res.bse[0], places=9)


def plateau_langsomt(M, T, NOK, r, k):
    """Uafhængig udgave til T10: regner farve celle for celle med almindelige løkker."""
    R, K = M.shape
    niveau = 0
    for nv, h, krav in rp.TRAPPE:
        g = gr = ro = 0
        for i in range(r - h, r + h + 1):
            for j in range(k - h, k + h + 1):
                inde = 0 <= i < R and 0 <= j < K
                if not inde or not NOK[i, j] or not np.isfinite(M[i, j]):
                    gr += 1
                elif M[i, j] <= 0:
                    ro += 1
                elif T[i, j] >= 2.0 and M[i, j] >= rp.ANDEL_AF_MIDTE * M[r, k]:
                    g += 1
                else:
                    gr += 1
        tot = (2 * h + 1) ** 2
        ok = (g == tot) if krav == "alle_groen" else (
            gr / tot < 0.5 and (ro == 0 if krav == "graa_under_50_roed_0" else ro / tot < 0.2))
        if not ok:
            break
        niveau = nv
    return niveau


class T10_PlateauTrappen(unittest.TestCase):
    def tomt(self):
        M = np.full((25, 25), np.nan); T = np.full((25, 25), np.nan); NOK = np.zeros((25, 25), bool)
        return M, T, NOK

    def test_groent_5x5_giver_PL4(self):
        M, T, NOK = self.tomt()
        M[10:15, 10:15] = 10; T[10:15, 10:15] = 5; NOK[10:15, 10:15] = True
        # 7x7: 25 grønne + 24 grå (49 %) + 0 røde -> PL4 opfyldt; PL5 kræver 100 % grøn -> stop
        self.assertEqual(rp.plateau_niveau(M, T, NOK, 12, 12), 4)

    def test_roed_i_7x7_ringen_giver_PL3(self):
        M, T, NOK = self.tomt()
        M[10:15, 10:15] = 10; T[10:15, 10:15] = 5; NOK[10:15, 10:15] = True
        M[9, 9] = -1; T[9, 9] = -0.5; NOK[9, 9] = True
        self.assertEqual(rp.plateau_niveau(M, T, NOK, 12, 12), 3)

    def test_nabo_under_halvdelen_af_midten_er_graa(self):
        gammel = rp.ANDEL_AF_MIDTE
        rp.ANDEL_AF_MIDTE = 0.5          # K1's GAMLE regel slået til i denne test
        self.addCleanup(setattr, rp, "ANDEL_AF_MIDTE", gammel)
        M, T, NOK = self.tomt()
        M[10:15, 10:15] = 10; T[10:15, 10:15] = 5; NOK[10:15, 10:15] = True
        M[12, 12] = 25                     # midten er meget bedre end naboerne (10 < 50 % af 25)
        self.assertEqual(rp.plateau_niveau(M, T, NOK, 12, 12), 0)
        rp.ANDEL_AF_MIDTE = 0.0          # K1's NYE regel: samme gitter er nu et plateau
        self.assertEqual(rp.plateau_niveau(M, T, NOK, 12, 12), 4)

    def test_kant_taeller_som_graa(self):
        M, T, NOK = self.tomt()
        M[0:3, 0:3] = 10; T[0:3, 0:3] = 5; NOK[0:3, 0:3] = True
        self.assertEqual(rp.plateau_niveau(M, T, NOK, 1, 1), 1)   # 3x3 grøn -> PL1; 5x5 har 16/25 grå -> ikke PL2
        self.assertEqual(rp.plateau_niveau(M, T, NOK, 0, 0), 0)   # hjørnet: 3x3 har celler uden for kanten

    def test_hurtig_lig_langsom_paa_tilfaeldige_gitre(self):
        self.addCleanup(setattr, rp, "ANDEL_AF_MIDTE", rp.ANDEL_AF_MIDTE)
        rng = np.random.default_rng(10)
        for i in range(600):
            rp.ANDEL_AF_MIDTE = 0.5 if i % 2 else 0.0      # begge regler afprøves
            M = rng.normal(2, 3, (25, 25)); T = M / rng.uniform(0.5, 2, (25, 25))
            NOK = rng.random((25, 25)) > 0.1
            r, k = rng.integers(0, 25, 2)
            if not (M[r, k] > 0):
                continue
            self.assertEqual(rp.plateau_niveau(M, T, NOK, r, k), plateau_langsomt(M, T, NOK, r, k))


class T12_LokkedueNulForskydning(unittest.TestCase):
    def test_forskydning_0_giver_de_aegte_signaler(self):
        kal = rp.lav_kalender("2020-01-01", "2020-06-30")
        md = rp.lav_minutdata(kal, seed=11)
        bars = rp.byg_bars(md, kal, 15)
        sig = rp.lav_signaler(bars, [10], [3])
        ny, ok, _, _ = rp.lokkedue_forskyd(sig.starttid, kal, bars.stempel, 0)
        self.assertTrue(np.all(ok))
        np.testing.assert_array_equal(ny, sig.starttid)

    def test_kalenderuger_bevarer_ugedag_ogsaa_med_helligdage(self):
        kal = rp.lav_kalender("2020-01-01", "2024-12-31",
                              helligdage=("2020-01-01", "2020-07-03", "2020-12-25", "2021-01-01"))
        md = rp.lav_minutdata(kal, seed=12)
        bars = rp.byg_bars(md, kal, 30)
        sig = rp.lav_signaler(bars, [10], [3])
        ugedag = lambda d: (kal.handelsdage[d].astype("int64") - 4) % 7
        ny, ok, d0, d1 = rp.lokkedue_forskyd(sig.starttid, kal, bars.stempel, 13, "kalenderuger")
        self.assertTrue(np.all(ugedag(d0[ok]) == ugedag(d1[ok])))


class T8_ExitMotor(unittest.TestCase):
    def test_hurtigt_gitter_lig_langsom_minut_for_minut(self):
        import exitmotor as em
        kal = rp.lav_kalender("2020-01-06", "2020-02-28")
        md = rp.lav_minutdata(kal, seed=13, uro_klumper=True, mangler=0.002)
        sidste = np.searchsorted(md.dag, md.dag, side="right") - 1
        rng = np.random.default_rng(13)
        S = list(range(2, 30, 3)); T = list(range(2, 30, 3))
        for e in rng.integers(0, len(md.luk) - 500, 150):
            s = min(e + 90, sidste[e])
            res, _ = em.exit_gitter(md, e, s, S, T)
            for a, Sv in enumerate(S):
                for b, Tv in enumerate(T):
                    self.assertEqual(int(res[a, b]), em.exit_langsom(md, e, s, Sv, Tv)[0])


class T18_IdentiskeCeller(unittest.TestCase):
    """Seriefunktions-fejlen kan give ENS signaler i alle celler -> ligner et perfekt plateau.
    Kontrollen skal kende forskel på et gyldigt gitter og et fejlramt."""
    def test_gyldigt_og_fejlramt_gitter(self):
        kal = rp.lav_kalender("2020-01-01", "2020-12-31")
        md = rp.lav_minutdata(kal, seed=14)
        bars = rp.byg_bars(md, kal, 15)
        sig = rp.lav_signaler(bars, range(5, 30), range(1, 26))
        k = rp.gitter_kontrol(sig)
        self.assertEqual(rp.gitter_dom(k), [])                      # gyldigt
        self.assertEqual(k["forskellige_lister"], 625)
        # fejlramt: cellen (0,0)'s signaler kopieret til alle 625 celler
        m = (sig.n1_idx == 0) & (sig.n2_idx == 0)
        n = int(m.sum())
        kopi = rp.Signaler(np.repeat(np.arange(25, dtype=np.int16), 25 * n),
                           np.tile(np.repeat(np.arange(25, dtype=np.int16), n), 25),
                           np.tile(sig.starttid[m], 625), np.tile(sig.antal_bars[m], 625),
                           np.tile(sig.afsluttet[m], 625))
        k2 = rp.gitter_kontrol(kopi)
        self.assertEqual(rp.gitter_dom(k2), ["N1", "N2"])
        self.assertEqual(k2["forskellige_lister"], 1)
        self.assertGreaterEqual(k2["fjerne_min_lighed"], 0.99)     # K1's regel slår til
        self.assertLess(k["fjerne_min_lighed"], 0.99)              # ... men ikke på det gyldige gitter


class T19_VaerdiStabilitet(unittest.TestCase):
    """K1's B6: de 8 nærmeste naboer skal have netto >= 50 % af midtens (kun inderste ring)."""
    def test_inderste_ring(self):
        M = np.full((25, 25), np.nan)
        M[9:16, 9:16] = 1.0                 # svag yderring (7x7) - må gerne være under 50 %
        M[11:14, 11:14] = 6.0               # inderste ring: 6 >= 50 % af 10
        M[12, 12] = 10.0
        self.assertTrue(rp.vaerdi_stabil(M, 12, 12))      # yderringen (1,0 = 10 %) tæller ikke
        M[11, 13] = 4.0                     # én nabo under 50 %
        self.assertFalse(rp.vaerdi_stabil(M, 12, 12))
        M[11, 13] = 5.0                     # præcis 50 % er nok
        self.assertTrue(rp.vaerdi_stabil(M, 12, 12))
        self.assertFalse(rp.vaerdi_stabil(M, 0, 0))       # hjørne: naboer uden for gitteret


if __name__ == "__main__":
    unittest.main(verbosity=2)
