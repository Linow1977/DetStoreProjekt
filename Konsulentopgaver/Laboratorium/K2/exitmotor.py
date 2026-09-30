"""
exitmotor.py -- Prototype af Edge-Finders exit-motor (del2_K2.md afsnit 7.3). KUN OPDIGTEDE DATA.

Regler (lang handel; kort er spejlvendt):
- Indgang på åbningen af indgangsminuttet e. Hele minut e ligger efter indgangen.
- Stop-niveau = indgang - S. Rammes, hvis minuttets lav <= niveau.
  Åbner minuttet allerede under niveauet (gab), fyldes til åbningsprisen (dårligere).
- Target-niveau = indgang + T. Rammes kun, hvis høj >= niveau + 1 (1 tick forbi). Fyldes til niveauet.
- Rammes begge i samme minut: STOP først.
- Ellers ud på luk efter højst H minutter, dog senest sessionens sidste minut.
"""

import numpy as np


def exit_langsom(md, e, sidste, S, T):
    """Reference: minut for minut, én kombination ad gangen."""
    ind = int(md.aabn[e])
    stop_niv, tgt_niv = ind - S, ind + T
    for i in range(e, sidste + 1):
        if md.lav[i] <= stop_niv:
            fyld = int(md.aabn[i]) if md.aabn[i] <= stop_niv else stop_niv
            return fyld - ind, "stop", i
        if md.hoej[i] >= tgt_niv + 1:
            return tgt_niv - ind, "target", i
    return int(md.luk[sidste]) - ind, "tid", sidste


def exit_gitter(md, e, sidste, S_liste, T_liste):
    """Hele S x T-gitteret på én gang for én handel.
    Finder første minut, hvor hvert stop- og target-niveau rammes, og sammenligner."""
    ind = int(md.aabn[e])
    lav = md.lav[e:sidste + 1].astype(np.int64)
    hoej = md.hoej[e:sidste + 1].astype(np.int64)
    aabn = md.aabn[e:sidste + 1].astype(np.int64)
    L = len(lav)
    laveste = np.minimum.accumulate(lav)            # faldende
    hoejeste = np.maximum.accumulate(hoej)          # stigende
    S = np.asarray(S_liste); T = np.asarray(T_liste)
    # første minut hvor laveste <= ind - S  <=>  -laveste >= S - ind
    stop_i = np.searchsorted(-laveste, S - ind, side="left")          # L = aldrig
    tgt_i = np.searchsorted(hoejeste, ind + T + 1, side="left")
    stop_fyld = np.where(stop_i < L,
                         np.minimum(aabn[np.minimum(stop_i, L - 1)], ind - S) - ind, 0)
    tid_resultat = int(md.luk[sidste]) - ind
    si = stop_i[:, None]; ti = tgt_i[None, :]
    resultat = np.where((si <= ti) & (si < L), stop_fyld[:, None],
                        np.where(ti < L, T[None, :], tid_resultat))
    samme_minut = (si == ti) & (si < L)
    return resultat, samme_minut
