"""forsoeg4.py -- F9: exit-motoren. Hurtig 'hele gitteret' = langsom minut-for-minut? Tid? KUN OPDIGTEDE DATA."""
import time
import numpy as np
import rsa_proto as rp
import exitmotor as em
from forsoeg import skriv, us_helligdage

kal = rp.lav_kalender("2020-01-01", "2020-12-31", helligdage=us_helligdage(2020, 2020))
md = rp.lav_minutdata(kal, seed=41, sigma=2.0, uro_klumper=True, mangler=0.002)
rng = np.random.default_rng(1)
H = 120
S_liste = list(range(4, 44, 4)); T_liste = list(range(4, 44, 4))       # 10 x 10 = 100 kombinationer
dag_sidste = np.searchsorted(md.dag, md.dag, side="right") - 1
def handel(e):
    return e, min(e + H - 1, dag_sidste[e])
# (a) korrekthed
N = 400
es = rng.integers(0, len(md.luk) - 2000, N)
fejl = 0; samme = 0; t_langsom = time.time()
ref = np.zeros((N, 10, 10), dtype=np.int64)
for n, e in enumerate(es):
    e, s = handel(e)
    for a, S in enumerate(S_liste):
        for b, T in enumerate(T_liste):
            ref[n, a, b] = em.exit_langsom(md, e, s, S, T)[0]
t_langsom = time.time() - t_langsom
t0 = time.time()
for n, e in enumerate(es):
    e, s = handel(e)
    res, sm = em.exit_gitter(md, e, s, S_liste, T_liste)
    fejl += int(np.sum(res != ref[n])); samme += int(sm.sum())
t_hurtig = time.time() - t0
skriv(f"F9a: {N} handler x 100 stop/target-kombinationer: afvigelser hurtig vs. langsom = {fejl}")
skriv(f"     samme-minut-tilfælde (stop valgt): {samme} af {N*100} = {samme/(N*100):.3%}")
skriv(f"     tid: langsom {t_langsom:.1f} s, hurtig {t_hurtig:.2f} s ({t_langsom/t_hurtig:.0f} x hurtigere)")
# (b) særtilfælde i hånden: gab forbi stop og samme minut
kal1 = rp.lav_kalender("2020-01-06", "2020-01-06"); kal1.session_laengde[:] = 5
mk = rp.Minutdata(kal1.session_aabning[0] + np.arange(1, 6), np.array([100, 101, 90, 95, 96], np.int32),
                  np.array([102, 103, 96, 120, 97], np.int32), np.array([99, 100, 88, 80, 95], np.int32),
                  np.array([101, 102, 95, 96, 96], np.int32), np.zeros(5, np.int32), np.arange(1, 6, dtype=np.int32))
r_gab = em.exit_langsom(mk, 0, 4, 5, 50); g_gab, _ = em.exit_gitter(mk, 0, 4, [5], [50])
skriv(f"F9b: gab forbi stop (indgang 100, stop 95, minut 3 åbner 90): langsom {r_gab[0]} ({r_gab[1]}), hurtig {int(g_gab[0,0])} -> forventet -10")
r_sm = em.exit_langsom(mk, 3, 4, 4, 10); g_sm, sm = em.exit_gitter(mk, 3, 4, [4], [10])
skriv(f"F9c: samme minut (indgang 95, stop 91, target 105; minut 4 har høj 120 og lav 80): langsom {r_sm[0]} ({r_sm[1]}), hurtig {int(g_sm[0,0])}, mærket samme-minut={bool(sm[0,0])} -> forventet -4 (stop)")
# (c) fart
M = 20000
es = rng.integers(0, len(md.luk) - 2000, M)
t0 = time.time()
for e in es:
    e, s = handel(e)
    em.exit_gitter(md, e, s, S_liste, T_liste)
dt_ = time.time() - t0
skriv(f"F9d: {M} handler x 100 kombinationer på {dt_:.1f} s = {M/dt_:,.0f} handler/s (NumPy, én kerne)")
