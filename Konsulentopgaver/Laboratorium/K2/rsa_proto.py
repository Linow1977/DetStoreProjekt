"""
rsa_proto.py -- Lille prototype af RSA-kæden (Konsulent 2, laboratoriet).

KUN OPDIGTEDE DATA. Ingen forbindelse til repo, TradingDB eller rigtige priser.

Kæden (samme rækkefølge som i del2_K2.md afsnit 4-6):
    lav_kalender -> lav_minutdata -> byg_bars -> lav_signaler (et opdigtet 2-parameter-filter)
    -> event_motor -> celle_tal (dag-klynget t) -> plateau_niveau -> lokkedue_forskyd

Konventioner (samme som i byggeplanen):
- Tid er heltal: minutter siden 1970-01-01 i børsens lokale tid (ingen sommertid i prototypen).
- Et 1-minuts bar stemplet t dækker (t-1, t]  -> tidsstemplet er LUKKETIDEN.
- Priser er heltal i ticks.
- Handelsdag D: session fra (D-1) 17:00 til D 16:00 (23 timer = 1380 minutter).
  Mandagens session starter søndag 17:00 (søndag = mandag, mærket).
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

import numpy as np

MINUTTER_PR_DAG = 1440
SESSION_START_KL = 17 * 60      # 17:00 dagen før handelsdagen
SESSION_LAENGDE = 23 * 60       # 1380 minutter


# ---------------------------------------------------------------------------
# 1. Kalender og opdigtede 1-minuts data
# ---------------------------------------------------------------------------

@dataclass
class Kalender:
    handelsdage: np.ndarray        # datetime64[D] for hver handelsdag
    session_aabning: np.ndarray    # int64 minut-tid for sessionens åbning (dagen før kl. 17)
    session_laengde: np.ndarray    # int64 antal minutter i sessionen (kortere ved tidlig lukning)


def lav_kalender(start="2020-01-01", slut="2024-12-31", helligdage=(), tidlig_luk=()):
    """Hverdage mellem start og slut, minus helligdage. tidlig_luk = dage med 3 timer kortere session."""
    dage = np.arange(np.datetime64(start), np.datetime64(slut) + 1)
    ugedag = (dage.astype("datetime64[D]").view("int64") - 4) % 7   # 0 = mandag
    dage = dage[ugedag < 5]
    if helligdage:
        dage = dage[~np.isin(dage, np.array(helligdage, dtype="datetime64[D]"))]
    epoke_dag = dage.astype("int64")
    aabning = (epoke_dag - 1) * MINUTTER_PR_DAG + SESSION_START_KL
    laengde = np.full(len(dage), SESSION_LAENGDE, dtype=np.int64)
    if tidlig_luk:
        laengde[np.isin(dage, np.array(tidlig_luk, dtype="datetime64[D]"))] = SESSION_LAENGDE - 180
    return Kalender(dage, aabning.astype(np.int64), laengde)


@dataclass
class Minutdata:
    stempel: np.ndarray     # int64 lukketid
    aabn: np.ndarray        # int32 ticks
    hoej: np.ndarray
    lav: np.ndarray
    luk: np.ndarray
    dag: np.ndarray         # int32 handelsdagens nummer (indeks i kalenderen)
    minut_nr: np.ndarray    # int32 1..sessionslængde (minutter efter åbning)


def lav_minutdata(kal: Kalender, seed=1, sigma=2.0, uro_klumper=False, mangler=0.0,
                  dags_trend=0.0) -> Minutdata:
    """Tilfældig gang i hele ticks. uro_klumper=True giver skiftende rolige/urolige dage.
    mangler = andel af minutter uden handel (fjernes; første minut i sessionen beholdes).
    dags_trend = spredning (ticks pr. minut) af en tilfældig 'trenddag'-drift, fælles for hele dagen.
    Den har middel 0 (ingen edge), men gør signaler samme dag afhængige af hinanden."""
    rng = np.random.default_rng(seed)
    n_dage = len(kal.handelsdage)
    dag = np.repeat(np.arange(n_dage, dtype=np.int32), kal.session_laengde)
    minut_nr = np.concatenate([np.arange(1, L + 1, dtype=np.int32) for L in kal.session_laengde])
    stempel = kal.session_aabning[dag] + minut_nr

    if uro_klumper:
        # log-udsving følger en langsom AR(1) fra dag til dag -> klumpet uro
        log_s = np.zeros(n_dage)
        for i in range(1, n_dage):
            log_s[i] = 0.9 * log_s[i - 1] + 0.3 * rng.standard_normal()
        s_minut = sigma * np.exp(log_s)[dag]
    else:
        s_minut = np.full(len(dag), sigma)

    drift = rng.standard_normal(n_dage)[dag] * dags_trend if dags_trend > 0 else 0.0
    skridt = np.rint(rng.standard_normal(len(dag)) * s_minut + drift).astype(np.int64)
    # nat-gab: første minut i hver session åbner et stykke fra forrige sessions luk
    foerste = minut_nr == 1
    gab = np.zeros(len(dag), dtype=np.int64)
    gab[foerste] = np.rint(rng.standard_normal(foerste.sum()) * sigma * 5).astype(np.int64)
    # luk[i] = luk[i-1] + gab[i] + skridt[i];  aabn[i] = luk[i-1] + gab[i]
    luk = 20000 + np.cumsum(skridt + gab)
    aabn = np.empty_like(luk)
    aabn[0] = 20000 + gab[0]
    aabn[1:] = luk[:-1] + gab[1:]
    ekstra_op = np.abs(np.rint(rng.standard_normal(len(luk)) * s_minut * 0.5)).astype(np.int64)
    ekstra_ned = np.abs(np.rint(rng.standard_normal(len(luk)) * s_minut * 0.5)).astype(np.int64)
    hoej = np.maximum(aabn, luk) + ekstra_op
    lav = np.minimum(aabn, luk) - ekstra_ned

    behold = np.ones(len(luk), dtype=bool)
    if mangler > 0:
        behold = (rng.random(len(luk)) >= mangler) | foerste
    return Minutdata(stempel[behold], aabn[behold].astype(np.int32), hoej[behold].astype(np.int32),
                     lav[behold].astype(np.int32), luk[behold].astype(np.int32),
                     dag[behold], minut_nr[behold])


# ---------------------------------------------------------------------------
# 2. Bar-bygning (sessions-forankret, stemplet med lukketid; afsnit 4.1)
# ---------------------------------------------------------------------------

@dataclass
class Bars:
    stempel: np.ndarray
    aabn: np.ndarray
    hoej: np.ndarray
    lav: np.ndarray
    luk: np.ndarray
    dag: np.ndarray


def byg_bars(md: Minutdata, kal: Kalender, n_min: int) -> Bars:
    """N-minuts bars fra 1-minuts bars. Bar nr. k dækker minut (k*N+1 .. (k+1)*N) efter åbning,
    stemples med åbning + (k+1)*N, dog højst sessionens luk (kort sidste bar).
    Minutter uden handel opfindes ikke; en bar findes, hvis mindst ét minut findes."""
    bar_nr = (md.minut_nr.astype(np.int64) - 1) // n_min
    noegle = md.dag.astype(np.int64) * 100000 + bar_nr
    # data er sorteret efter tid -> nøglen er stigende; find grupper
    start = np.flatnonzero(np.r_[True, noegle[1:] != noegle[:-1]])
    dag = md.dag[start]
    bar_slut_minut = np.minimum((bar_nr[start] + 1) * n_min, kal.session_laengde[dag])
    stempel = kal.session_aabning[dag] + bar_slut_minut
    return Bars(
        stempel=stempel.astype(np.int64),
        aabn=md.aabn[start],
        hoej=np.maximum.reduceat(md.hoej, start),
        lav=np.minimum.reduceat(md.lav, start),
        luk=md.luk[np.r_[start[1:] - 1, len(md.luk) - 1]],
        dag=dag,
    )


def byg_bars_langsomt(md: Minutdata, kal: Kalender, n_min: int) -> Bars:
    """Uafhængig, langsom referenceudgave (almindelig løkke) til test T1/T2."""
    grupper = {}
    for i in range(len(md.stempel)):
        d = int(md.dag[i])
        k = (int(md.minut_nr[i]) - 1) // n_min
        grupper.setdefault((d, k), []).append(i)
    ud = []
    for (d, k), idx in sorted(grupper.items()):
        slut = min((k + 1) * n_min, int(kal.session_laengde[d]))
        ud.append((int(kal.session_aabning[d]) + slut, int(md.aabn[idx[0]]),
                   max(int(md.hoej[i]) for i in idx), min(int(md.lav[i]) for i in idx),
                   int(md.luk[idx[-1]]), d))
    a = np.array(ud, dtype=np.int64)
    return Bars(a[:, 0], a[:, 1], a[:, 2], a[:, 3], a[:, 4], a[:, 5])


# ---------------------------------------------------------------------------
# 3. Et opdigtet 2-parameter-filter -> signal-linjer som fra TradeStation
# ---------------------------------------------------------------------------

@dataclass
class Signaler:
    n1_idx: np.ndarray      # 0..24 (position i parameterlisten)
    n2_idx: np.ndarray
    starttid: np.ndarray    # lukketid for den bar, hvor filteret blev SANDT
    antal_bars: np.ndarray  # hvor mange bars i træk filteret var SANDT (FREMTIDSVIDEN!)
    afsluttet: np.ndarray   # 0 = stadig tændt ved dataslut


def lav_signaler(bars: Bars, n1_vaerdier, n2_vaerdier) -> Signaler:
    """Filter: luk > glidende gennemsnit(N1)  OG  luk > luk for N2 bars siden.
    Signal = skift fra FALSK til SAND. Regnet på en sammenhængende bar-serie (som i TradeStation)."""
    luk = bars.luk.astype(np.float64)
    cs = np.r_[0.0, np.cumsum(luk)]
    ud = {k: [] for k in ("n1", "n2", "t", "ab", "af")}
    opvarmning = max(max(n1_vaerdier), max(n2_vaerdier))
    for i1, n1 in enumerate(n1_vaerdier):
        sma = np.full(len(luk), np.nan)
        sma[n1 - 1:] = (cs[n1:] - cs[:-n1]) / n1
        over_sma = luk > sma
        for i2, n2 in enumerate(n2_vaerdier):
            mom = np.zeros(len(luk), dtype=bool)
            mom[n2:] = luk[n2:] > luk[:-n2]
            sand = over_sma & mom
            sand[:opvarmning] = False
            kant = np.diff(np.r_[False, sand, False].astype(np.int8))
            start = np.flatnonzero(kant == 1)
            slut = np.flatnonzero(kant == -1)          # første bar efter SAND-perioden
            ud["n1"].append(np.full(len(start), i1, dtype=np.int16))
            ud["n2"].append(np.full(len(start), i2, dtype=np.int16))
            ud["t"].append(bars.stempel[start])
            ud["ab"].append((slut - start).astype(np.int32))
            ud["af"].append((slut < len(luk)).astype(np.int8))
    return Signaler(*(np.concatenate(ud[k]) for k in ("n1", "n2", "t", "ab", "af")))


# ---------------------------------------------------------------------------
# 4. Event-motoren (afsnit 5.2)
# ---------------------------------------------------------------------------

@dataclass
class Events:
    gyldig: np.ndarray       # bool: signalet kunne handles og måles
    grund: np.ndarray        # 0 ok, 1 sessionsskift, 2 periodeslut, 3 afkortet (stadig gyldig)
    dag: np.ndarray          # handelsdag for indgang
    brutto: np.ndarray       # ticks, lang retning
    indgang_idx: np.ndarray


def event_motor(md: Minutdata, starttid: np.ndarray, horisont_min: int,
                test_slut_stempel: int | None = None, fejl_indgang_paa_signalbar=False,
                bar_min: int = 15) -> Events:
    """Indgang = åbningen af første 1-min bar med lukketid > Starttid. Udgang = luk på minuttet,
    der slutter horisont_min efter indgang (afkortes til sessionens sidste minut).
    fejl_indgang_paa_signalbar=True er en BEVIDST FEJL til forsøget: indgang på signal-barens
    egen åbning (kigger ind i fremtiden, fordi filteret først kendes ved barens luk)."""
    n = len(md.stempel)
    i_ind = np.searchsorted(md.stempel, starttid, side="right")
    i_sig = i_ind - 1                                   # sidste minut i signal-baren
    grund = np.zeros(len(starttid), dtype=np.int8)
    ok = (i_ind < n) & (i_sig >= 0)
    i_ind_c = np.minimum(i_ind, n - 1)
    i_sig_c = np.maximum(i_sig, 0)
    sessionsskift = ok & (md.dag[i_ind_c] != md.dag[i_sig_c])
    grund[sessionsskift] = 1
    ok &= ~sessionsskift

    indgang_aabning = md.stempel[i_ind_c] - 1            # indgangsminuttets åbningstid
    maal = indgang_aabning + horisont_min
    i_ud = np.searchsorted(md.stempel, maal, side="right") - 1
    i_ud = np.clip(i_ud, 0, n - 1)
    # sidste minut i samme session; horisont ud over sessionens luk -> afkort og mærk
    dag_ind = md.dag[i_ind_c]
    sidste_i_dag = np.searchsorted(md.dag, dag_ind, side="right") - 1
    afkortet = ok & (maal > md.stempel[sidste_i_dag])
    i_ud = np.minimum(i_ud, sidste_i_dag)
    grund[afkortet] = 3
    if test_slut_stempel is not None:
        efter = ok & (maal > test_slut_stempel)
        grund[efter] = 2
        ok &= ~efter

    if fejl_indgang_paa_signalbar:
        # Finder åbningen af den bar, der SKABTE signalet (bar_min minutter før lukketiden)
        i_fejl = np.searchsorted(md.stempel, starttid - bar_min, side="right")
        indgang_pris = md.aabn[np.clip(i_fejl, 0, n - 1)].astype(np.int64)
    else:
        indgang_pris = md.aabn[i_ind_c].astype(np.int64)
    brutto = md.luk[i_ud].astype(np.int64) - indgang_pris
    return Events(ok, grund, dag_ind.astype(np.int32), brutto, i_ind_c)


# ---------------------------------------------------------------------------
# 5. Celle-tal med dag-klynget usikkerhed (afsnit 5.3)
# ---------------------------------------------------------------------------

def celle_tal(celle: np.ndarray, dag: np.ndarray, netto: np.ndarray, n_celler: int):
    """For hver celle: antal signaler, antal dage, netto pr. signal, dag-klynget SE og t.
    SE = sqrt(D/(D-1) * sum_d (S_d - m*n_d)^2) / sum n_d   (klynge = handelsdag)."""
    noegle = celle.astype(np.int64) * 10_000_000 + dag.astype(np.int64)
    orden = np.argsort(noegle, kind="stable")
    k = noegle[orden]
    x = netto[orden].astype(np.float64)
    start = np.flatnonzero(np.r_[True, k[1:] != k[:-1]])
    S_d = np.add.reduceat(x, start)
    n_d = np.diff(np.r_[start, len(k)]).astype(np.float64)
    c_d = (k[start] // 10_000_000).astype(np.int64)

    sum_S = np.bincount(c_d, S_d, n_celler)
    sum_n = np.bincount(c_d, n_d, n_celler)
    D = np.bincount(c_d, None, n_celler).astype(np.float64)
    with np.errstate(invalid="ignore", divide="ignore"):
        m = sum_S / sum_n
        rest2 = np.bincount(c_d, (S_d - m[c_d] * n_d) ** 2, n_celler)
        se = np.sqrt(D / (D - 1) * rest2) / sum_n
        t = m / se
        # "naiv" t, som om hvert signal var uafhængigt (til sammenligning / pustefaktor)
        sum_x2 = np.bincount(celle, netto.astype(np.float64) ** 2, n_celler)
        var_x = (sum_x2 - sum_n * m ** 2) / (sum_n - 1)
        t_naiv = m / np.sqrt(var_x / sum_n)
    return dict(n=sum_n, dage=D, m=m, se=se, t=t, t_naiv=t_naiv)


# ---------------------------------------------------------------------------
# 6. Farver og plateau-trappen (afsnit 5.4-5.5, K1's G.2)
# ---------------------------------------------------------------------------

GROEN, GRAA, ROED = 0, 1, 2
# K1's regel efter K1's laboratorium: grøn = nok data + netto > 0 + t >= 2 (INTET krav om "% af midten").
# Sæt til 0.5 for K1's gamle regel ("netto >= 50 % af midten").
ANDEL_AF_MIDTE = 0.0
TRAPPE = [  # (niveau, halv bredde, krav)
    (1, 1, "alle_groen"), (2, 2, "graa_under_50_roed_0"), (3, 2, "alle_groen"),
    (4, 3, "graa_under_50_roed_0"), (5, 3, "alle_groen"),
    (6, 4, "graa_under_50_roed_under_20"), (7, 4, "alle_groen"),
]


def farv_set_fra_midte(m, t, nok_data, midte_m, t_groen=2.0, andel_af_midte=None):
    """K1 G.2: grøn = nok data og m>0 og t>=2 og m >= 50 % af midten; rød = m<=0; ellers grå.
    Celler uden data (NaN) eller for lidt data = grå."""
    if andel_af_midte is None:
        andel_af_midte = ANDEL_AF_MIDTE
    farve = np.full(m.shape, GRAA, dtype=np.int8)
    har = nok_data & np.isfinite(m)
    farve[har & (m <= 0)] = ROED
    groen = har & (m > 0) & (t >= t_groen) & (m >= andel_af_midte * midte_m)
    farve[groen] = GROEN
    return farve


def plateau_niveau(M, T, NOK, r, k):
    """Højeste niveau i trappen for midten (r, k) i et gitter. Celler uden for kanten = grå."""
    R, K = M.shape
    niveau = 0
    for nv, h, krav in TRAPPE:
        felt_m = np.full((2 * h + 1, 2 * h + 1), np.nan)
        felt_t = np.full_like(felt_m, np.nan)
        felt_ok = np.zeros(felt_m.shape, dtype=bool)
        r0, r1, k0, k1 = max(r - h, 0), min(r + h + 1, R), max(k - h, 0), min(k + h + 1, K)
        felt_m[r0 - (r - h):r1 - (r - h), k0 - (k - h):k1 - (k - h)] = M[r0:r1, k0:k1]
        felt_t[r0 - (r - h):r1 - (r - h), k0 - (k - h):k1 - (k - h)] = T[r0:r1, k0:k1]
        felt_ok[r0 - (r - h):r1 - (r - h), k0 - (k - h):k1 - (k - h)] = NOK[r0:r1, k0:k1]
        f = farv_set_fra_midte(felt_m, felt_t, felt_ok, M[r, k])
        andel_graa = np.mean(f == GRAA)
        andel_roed = np.mean(f == ROED)
        if krav == "alle_groen":
            opfyldt = np.all(f == GROEN)
        elif krav == "graa_under_50_roed_0":
            opfyldt = andel_graa < 0.5 and andel_roed == 0
        else:
            opfyldt = andel_graa < 0.5 and andel_roed < 0.2
        if not opfyldt:
            break
        niveau = nv
    return niveau


def plateau_gitter(M, T, NOK):
    """Niveau for alle midter i gitteret (kun celler med m>0 kan være midte)."""
    R, K = M.shape
    ud = np.zeros((R, K), dtype=np.int8)
    for r in range(R):
        for k in range(K):
            if NOK[r, k] and np.isfinite(M[r, k]) and M[r, k] > 0:
                ud[r, k] = plateau_niveau(M, T, NOK, r, k)
    return ud


# ---------------------------------------------------------------------------
# 7. Lokkeduer: forskyd hele signalserien et helt antal uger (afsnit 6.1, K1 C.3)
# ---------------------------------------------------------------------------

def lokkedue_forskyd(starttid: np.ndarray, kal: Kalender, gyldige_stempler: np.ndarray,
                     uger: int, metode="kalenderuger"):
    """Flyt alle signaler 'uger' frem, cirkulært inden for kalenderen, med samme klokkeslæt
    målt fra sessionens åbning. Signaler, hvis nye tidspunkt ikke findes som bar-lukketid, udelades.
    metode='kalenderuger': +7*uger kalenderdage (bevarer ugedagen altid).
    metode='handelsdage' : +5*uger handelsdage (flytter ugedagen, hvis der er helligdage imellem)."""
    dag_idx = np.searchsorted(kal.session_aabning, starttid, side="right") - 1
    forskel = starttid - kal.session_aabning[dag_idx]
    n = len(kal.handelsdage)
    if metode == "handelsdage":
        ny_idx = (dag_idx + 5 * uger) % n
        ok = np.ones(len(starttid), dtype=bool)
    else:
        d0 = kal.handelsdage[0].astype("int64")
        span = (kal.handelsdage[-1].astype("int64") - d0 + 1)
        span_uger = (span // 7) * 7
        ny_dato = d0 + ((kal.handelsdage[dag_idx].astype("int64") - d0 + 7 * uger) % span_uger)
        pos = np.searchsorted(kal.handelsdage.astype("int64"), ny_dato)
        pos_c = np.minimum(pos, n - 1)
        ok = kal.handelsdage.astype("int64")[pos_c] == ny_dato
        ny_idx = pos_c
    ny = kal.session_aabning[ny_idx] + forskel
    ok &= np.isin(ny, gyldige_stempler)
    return ny, ok, dag_idx, ny_idx


# ---------------------------------------------------------------------------
# 8. Alignment og datovagt (afsnit 4.2 og 5.2 pkt. 6)
# ---------------------------------------------------------------------------

def sammenlign_bars(vores: Bars, deres: Bars):
    """Returnerer liste af forskelle: ('mangler hos os'|'ekstra hos os'|'pris', stempel)."""
    forskelle = []
    a = {int(s): i for i, s in enumerate(vores.stempel)}
    b = {int(s): i for i, s in enumerate(deres.stempel)}
    for s in sorted(set(a) | set(b)):
        if s not in a:
            forskelle.append(("mangler hos os", s))
        elif s not in b:
            forskelle.append(("ekstra hos os", s))
        else:
            i, j = a[s], b[s]
            if (vores.aabn[i], vores.hoej[i], vores.lav[i], vores.luk[i]) != \
               (deres.aabn[j], deres.hoej[j], deres.lav[j], deres.luk[j]):
                forskelle.append(("pris", s))
    return forskelle


class DatoFejl(Exception):
    pass


def kontroller_datograense(md: Minutdata, test_slut_stempel: int):
    """Hård vagt: stop, hvis der er priser efter testperiodens slut i det, analysen får."""
    if len(md.stempel) and md.stempel.max() > test_slut_stempel:
        raise DatoFejl("Pris efter testperiodens slut fundet - analysen stoppes.")


# ---------------------------------------------------------------------------
# 9. Gitter-kontrol: "identiske celler" (seriefunktions-fejlen i TradeStation-løkken)
# ---------------------------------------------------------------------------

def gitter_kontrol(sig: Signaler, n1_antal=25, n2_antal=25):
    """For hvert filter x barstørrelse: giver parametrene overhovedet forskellige signaler?
    Et fingeraftryk af hver celles signal-liste sammenlignes med nabo-cellens langs N1 og N2.
    Returnerer andelen af nabo-par, der er HELT ens, pr. akse, og antal forskellige lister i gitteret.
    (Hvis seriefunktioner deler hukommelse på tværs af løkken, bliver alle celler ens -> falsk 'perfekt plateau'.)"""
    celle = sig.n1_idx.astype(np.int64) * n2_antal + sig.n2_idx
    orden = np.lexsort((sig.starttid, celle))
    c = celle[orden]; t = sig.starttid[orden]
    start = np.flatnonzero(np.r_[True, c[1:] != c[:-1]])
    slut = np.r_[start[1:], len(c)]
    fp = {}
    for a, b in zip(start, slut):
        fp[int(c[a])] = hash(t[a:b].tobytes())
    def aks(d1, d2):
        ens = tot = 0
        for i in range(n1_antal):
            for j in range(n2_antal):
                i2, j2 = i + d1, j + d2
                if i2 < n1_antal and j2 < n2_antal:
                    a, b = fp.get(i * n2_antal + j), fp.get(i2 * n2_antal + j2)
                    if a is not None and b is not None:
                        tot += 1; ens += (a == b)
        return ens / tot if tot else float("nan")
    # K1's regel (koereplan trin 8a): ligner FJERNE celler (hjørner og kantmidter) hinanden >= 99 %?
    tider = {int(c[a]): set(t[a:b].tolist()) for a, b in zip(start, slut)}
    h1, h2, m1, m2 = n1_antal - 1, n2_antal - 1, (n1_antal - 1) // 2, (n2_antal - 1) // 2
    fjerne = [((0, 0), (h1, h2)), ((0, h2), (h1, 0)), ((0, m2), (h1, m2)), ((m1, 0), (m1, h2))]
    lighed = []
    for (i1, j1), (i2, j2) in fjerne:
        A, B = tider.get(i1 * n2_antal + j1), tider.get(i2 * n2_antal + j2)
        if A is not None and B is not None and (A or B):
            lighed.append(len(A & B) / len(A | B))
    return dict(ens_langs_n1=aks(1, 0), ens_langs_n2=aks(0, 1), forskellige_lister=len(set(fp.values())),
                celler=len(fp), fjerne_min_lighed=min(lighed) if lighed else float("nan"))


def gitter_dom(k, graense=0.5):
    """Regel (i regelfilen): er mere end 'graense' af nabo-parrene langs en akse HELT ens,
    virker den parameter ikke -> gitteret er ugyldigt for den akse (TEKNISK_FEJL, ikke 'plateau')."""
    ugyldig = []
    if k.get("fjerne_min_lighed", 0) >= 0.99:          # K1's regel: fjerne celler >= 99 % ens -> hele gitteret
        return ["N1", "N2"]
    if k["ens_langs_n1"] > graense:
        ugyldig.append("N1")
    if k["ens_langs_n2"] > graense:
        ugyldig.append("N2")
    return ugyldig


# ---------------------------------------------------------------------------
# 10. Værdi-stabilitet (K1's B6/G.2, efter kvalitetskontrollen): de 8 nærmeste naboer skal have
#     netto >= 50 % af midtens netto. Gælder KUN den inderste ring, ikke hele plateau-feltet.
# ---------------------------------------------------------------------------

def vaerdi_stabil(M, r, k, andel=0.5):
    """True, hvis alle 8 naboer omkring (r, k) findes, har data og netto >= andel * midtens netto.
    En nabo uden for gitteret eller uden data kan ikke måles -> ikke bestået (K1: kan ikke måles = ikke bestået)."""
    R, K = M.shape
    midte = M[r, k]
    if not (np.isfinite(midte) and midte > 0):
        return False
    for dr in (-1, 0, 1):
        for dk in (-1, 0, 1):
            if dr == 0 and dk == 0:
                continue
            i, j = r + dr, k + dk
            if not (0 <= i < R and 0 <= j < K) or not np.isfinite(M[i, j]) or M[i, j] < andel * midte:
                return False
    return True
