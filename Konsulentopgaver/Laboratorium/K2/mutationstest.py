"""mutationstest.py -- Fanger testene fejl? Vi indsætter bevidst 4 typiske fejl én ad gangen og kører testene.
Hver fejl SKAL få mindst én test til at fejle. KUN OPDIGTEDE DATA."""
import unittest
import numpy as np
import rsa_proto as rp
import exitmotor as em
import test_rsa_proto as tr

def koer():
    suite = unittest.defaultTestLoader.loadTestsFromModule(tr)
    res = unittest.TextTestRunner(stream=open("/dev/null", "w"), verbosity=0).run(suite)
    return len(res.failures) + len(res.errors), res.testsRun

orig_bars, orig_ev, orig_gitter, orig_celle = rp.byg_bars, rp.event_motor, em.exit_gitter, rp.celle_tal

def bars_aabning_stempel(md, kal, n):            # FEJL 1: stempler bar med ÅBNINGStid i stedet for lukketid
    b = orig_bars(md, kal, n); b.stempel = b.stempel - n; return b
def event_indgang_signalbar(md, st, h, *a, **k):   # FEJL 2: indgang på signalbarens egen luk (1 minut for tidligt)
    ev = orig_ev(md, st, h, *a, **k)
    i = np.clip(ev.indgang_idx - 1, 0, None)
    ev.brutto = ev.brutto + (md.aabn[ev.indgang_idx].astype(np.int64) - md.luk[i].astype(np.int64)) * 0 \
        + (md.aabn[ev.indgang_idx].astype(np.int64) - md.aabn[i].astype(np.int64))
    return ev
def gitter_target_foerst(md, e, s, S, T):         # FEJL 3: target først ved samme minut (TradeStations antagelse)
    import numpy as np
    res, sm = orig_gitter(md, e, s, S, T)
    return np.where(sm, np.asarray(T)[None, :] + 0 * res, res), sm
def celle_naiv(c, d, x, n):                        # FEJL 4: t regnet som om hvert signal var uafhængigt
    r = orig_celle(c, d, x, n); r["se"] = r["m"] / r["t_naiv"]; r["t"] = r["t_naiv"]; return r

for navn, modul, attr, fejl in [("bar stemplet med åbningstid", rp, "byg_bars", bars_aabning_stempel),
                                ("indgang ét minut for tidligt", rp, "event_motor", event_indgang_signalbar),
                                ("target først ved samme minut", em, "exit_gitter", gitter_target_foerst),
                                ("naiv t (ingen dag-klynger)", rp, "celle_tal", celle_naiv)]:
    gammel = getattr(modul, attr); setattr(modul, attr, fejl)
    n_fejl, n = koer()
    setattr(modul, attr, gammel)
    print(f"Indsat fejl: {navn:32s} -> {n_fejl} af {n} tests fejler {'(FANGET)' if n_fejl else '(IKKE FANGET!)'}")
n_fejl, n = koer()
print(f"Uden indsatte fejl: {n_fejl} af {n} tests fejler")
