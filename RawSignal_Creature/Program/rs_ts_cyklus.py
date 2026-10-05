# Kører én hel RawSignal-cyklus i TradeStation (ORPlat.exe) og tager tid på
# hvert trin:
#   1. Åbn workspace         (.O <workspace>  i kommandolinjen)
#   2. Indsæt strategi       (.IST <strategi>)
#   3. Beregning             (fra CSV-filen oprettes til den er færdigskrevet)
#   4. Luk workspace         (.C  og svar Nej til at gemme)
#   5. Indlæs CSV i TradingDB (rawsignal.<strategi>, fx rawsignal.rawsignal002_test)
# Hvert trin og hele cyklussen skrives i rawsignal.tidslog. Bagefter opdateres
# rawsignal.rs_tf_runtime med gennemsnittet af alle hele cyklusser for samme
# filter, instrument og timeframe.
#
# Brug:  python rs_ts_cyklus.py <strategi> <symbol> <timeframe_id> ["<workspace>"]
#        fx  python rs_ts_cyklus.py RawSignal002 CL 1
#            -> workspace "CL-5-5-10-2007-09 Test" (navneregel, se WORKSPACE_NAVN)
#        fx  python rs_ts_cyklus.py RawSignal002-Test CL 13 "TestData CL-10-10-120-2007-09"
# <symbol> skal stå i public.rs_instrumenter, <timeframe_id> i public.timeframes.
#
# TradeStation skal være startet og må ikke have et workspace åbent.
# Fjernskrivebordet må ikke være minimeret.

import ctypes
import ctypes.wintypes as w
import os
import subprocess
import sys
import time
from datetime import datetime

from faelles import CSV_MAPPE, forbind, log

u = ctypes.windll.user32
k = ctypes.windll.kernel32

STILLE_SEK = 120        # CSV-filen regnes for færdig, når den ikke er ændret så længe
# Foreløbig navneregel for workspaces i TradeStation (ændres senere)
WORKSPACE_NAVN = "{symbol}-{d1}-{d2}-{d3}-2007-09 Test"
MAX_BEREGNING_SEK = 6 * 3600
WM_SETTEXT, WM_GETTEXT, WM_CANCELMODE, BM_CLICK = 0x0C, 0x0D, 0x1F, 0xF5
EM_SETSEL, CB_SHOWDROPDOWN = 0xB1, 0x14F
ES_CONTINUOUS, ES_SYSTEM_REQUIRED, ES_DISPLAY_REQUIRED = 0x80000000, 0x01, 0x02
VK_RETURN, VK_SHIFT, VK_CONTROL, VK_F24 = 0x0D, 0x10, 0x11, 0x87


# ---- Vinduer ----

def _vinduer(kun_synlige=True):
    """Alle topvinduer: (hwnd, titel, klasse)."""
    ud = []

    def cb(h, _):
        if kun_synlige and not u.IsWindowVisible(h):
            return True
        t = ctypes.create_unicode_buffer(300); u.GetWindowTextW(h, t, 300)
        c = ctypes.create_unicode_buffer(100); u.GetClassNameW(h, c, 100)
        ud.append((h, t.value, c.value))
        return True
    u.EnumWindows(ctypes.WINFUNCTYPE(ctypes.c_bool, w.HWND, w.LPARAM)(cb), 0)
    return ud


def _boern(h):
    """Alle børnevinduer: (hwnd, tekst, klasse)."""
    ud = []

    def cb(b, _):
        t = ctypes.create_unicode_buffer(300); u.SendMessageW(b, WM_GETTEXT, 300, t)
        c = ctypes.create_unicode_buffer(100); u.GetClassNameW(b, c, 100)
        ud.append((b, t.value, c.value))
        return True
    u.EnumChildWindows(h, ctypes.WINFUNCTYPE(ctypes.c_bool, w.HWND, w.LPARAM)(cb), 0)
    return ud


def hovedvindue():
    for h, t, c in _vinduer():
        if c == "ORPLAT.EXE TRADESTATION":
            return h
    return None


def titel(h):
    t = ctypes.create_unicode_buffer(300); u.GetWindowTextW(h, t, 300)
    return t.value


def forgrund(h):
    """Gør h til forgrundsvindue uden Alt-tricket (det sætter TS i menu-tilstand)."""
    stop_pauseskaerm()
    cur = u.GetForegroundWindow()
    t1 = u.GetWindowThreadProcessId(cur, None); me = k.GetCurrentThreadId()
    u.AttachThreadInput(me, t1, True)
    u.BringWindowToTop(h); u.SetForegroundWindow(h)
    u.AttachThreadInput(me, t1, False)
    time.sleep(0.5)
    if u.GetForegroundWindow() != h:
        # Er intet vindue i forgrunden, nægter Windows SetForegroundWindow.
        # Et tryk på F24 (en tast uden funktion) giver programmet lov igen.
        u.keybd_event(VK_F24, 0, 0, 0); u.keybd_event(VK_F24, 0, 2, 0)
        time.sleep(0.2)
        u.SetForegroundWindow(h)
        time.sleep(0.5)
    return u.GetForegroundWindow() == h


def saet_fokus(vindue, kontrol):
    tid = u.GetWindowThreadProcessId(vindue, None); me = k.GetCurrentThreadId()
    u.AttachThreadInput(me, tid, True); u.SetFocus(kontrol); u.AttachThreadInput(me, tid, False)
    time.sleep(0.3)


def tast(vk, ctrl=False):
    if ctrl:
        u.keybd_event(VK_CONTROL, 0, 0, 0)
    u.keybd_event(vk, 0, 0, 0); u.keybd_event(vk, 0, 2, 0)
    if ctrl:
        u.keybd_event(VK_CONTROL, 0, 2, 0)


# ---- Kommandolinjen ----

def kommandolinje(hoved):
    """Finder kommandolinjen. TS skjuler den efter brug i stedet for at lukke den,
    så en skjult vises igen. Findes den ikke, åbnes den med Ctrl+C."""
    for h, t, c in _vinduer(kun_synlige=False):
        if t == "Command Line" and c == "TS_IDD_BLANKDIALOG":
            u.ShowWindow(h, 5)
            return h
    forgrund(hoved)
    tast(ord("C"), ctrl=True)
    for _ in range(30):
        time.sleep(0.3)
        for h, t, c in _vinduer():
            if t == "Command Line":
                return h
    return None


def send_kommando(hoved, tekst, forsoeg=3):
    """Prøver op til 3 gange. Lige efter et workspace er åbnet, kan TS nulstille
    kommandolinjen, mens chartet indlæses."""
    for nr in range(1, forsoeg + 1):
        try:
            return _send_kommando(hoved, tekst)
        except RuntimeError as e:
            if nr == forsoeg:
                raise
            log(f"  Forsøg {nr} mislykkedes ({e}). Prøver igen om 5 sek.")
            time.sleep(5)


def _send_kommando(hoved, tekst):
    dlg = kommandolinje(hoved)
    if not dlg:
        raise RuntimeError("Kommandolinjen kunne ikke åbnes.")
    edit = next((b for b, _, c in _boern(dlg) if c == "Edit"), None)
    if not forgrund(dlg) or not edit:
        raise RuntimeError("Kommandolinjen kunne ikke få fokus.")
    u.PostMessageW(dlg, WM_CANCELMODE, 0, 0); time.sleep(0.3)
    saet_fokus(dlg, edit)
    # Alt undtagen sidste tegn indsættes (WM_SETTEXT), og sidste tegn tastes.
    # .C reagerer kun på et rigtigt tastetryk, og tastes hele teksten, åbner
    # forslagslisten efter første tegn og tager resten af tastetrykkene.
    u.SendMessageW(u.GetParent(edit), CB_SHOWDROPDOWN, 0, 0)
    u.SendMessageW(edit, WM_SETTEXT, 0, ctypes.c_wchar_p(tekst[:-1]))
    u.SendMessageW(edit, EM_SETSEL, len(tekst) - 1, len(tekst) - 1)
    vk = u.VkKeyScanW(ord(tekst[-1]))
    if vk & 0x100:
        u.keybd_event(VK_SHIFT, 0, 0, 0)
    tast(vk & 0xFF)
    if vk & 0x100:
        u.keybd_event(VK_SHIFT, 0, 2, 0)
    # TS er langsom til at vise det tastede tegn. Vent til hele teksten står der.
    buf = ctypes.create_unicode_buffer(300)
    for _ in range(20):
        time.sleep(0.5)
        u.SendMessageW(edit, WM_GETTEXT, 300, buf)
        if buf.value == tekst:
            break
    time.sleep(0.5)
    if u.GetForegroundWindow() != dlg:
        forgrund(dlg); saet_fokus(dlg, edit)
    if buf.value != tekst or u.GetForegroundWindow() != dlg:
        raise RuntimeError(f"Kommandoen '{tekst}' kunne ikke skrives i kommandolinjen "
                           f"(feltet viste '{buf.value}', forgrund ok: {u.GetForegroundWindow() == dlg}).")
    tast(VK_RETURN)


_sidst_vaekket = 0.0


def hold_vaagen():
    """Pauseskærmen starter efter 30 min uden aktivitet, og mens den kører, kan
    TradeStation ikke få fokus (5-5-10 regner ca. 1 time). Et tryk på F24 (en
    tast uden funktion) hvert 4. minut nulstiller tælleren. Windows bedes også
    om ikke at gå i dvale."""
    global _sidst_vaekket
    if time.time() - _sidst_vaekket < 240:
        return
    k.SetThreadExecutionState(ES_CONTINUOUS | ES_SYSTEM_REQUIRED | ES_DISPLAY_REQUIRED)
    u.keybd_event(VK_F24, 0, 0, 0); u.keybd_event(VK_F24, 0, 2, 0)
    _sidst_vaekket = time.time()


def stop_pauseskaerm():
    """Lukker pauseskærmen, hvis den alligevel kører. Mens den kører, tæller
    tastetryk ikke, så den lukkes først, og derefter nulstiller F24 tælleren
    (ellers starter Windows den straks igen)."""
    global _sidst_vaekket
    ud = subprocess.run(["tasklist", "/FI", "IMAGENAME eq scrnsave.scr", "/NH"],
                        capture_output=True, text=True).stdout
    if "scrnsave.scr" in ud.lower():
        subprocess.run(["taskkill", "/IM", "scrnsave.scr", "/F"], capture_output=True)
        time.sleep(1)
        _sidst_vaekket = 0.0
        hold_vaagen()
        time.sleep(1)


def vent_paa(betingelse, sek, tekst):
    slut = time.time() + sek
    while time.time() < slut:
        hold_vaagen()
        if betingelse():
            return
        time.sleep(0.5)
    raise RuntimeError(f"Tidsgrænse: {tekst}")


def ws_aaben(hoved, workspace):
    """Sand, når workspacet står i titlen. TS kan tilføje ' (Copy)' efter
    navnet (fx efter et nedbrud), så der tjekkes ikke kun på slutningen."""
    return (" - " + workspace) in titel(hoved)


def svar_nej_til_gem(hoved, workspace, sek=20):
    """Svarer Nej, hvis TradeStation spørger om workspacet skal gemmes.
    Klikker 'No'/'Nej'-knappen, hvis den findes, ellers tastes N (som manuelt)."""
    pid = w.DWORD(); u.GetWindowThreadProcessId(hoved, ctypes.byref(pid))
    start = time.time()
    while time.time() < start + sek:
        # Titlen tjekkes først efter 3 sek: spørgsmålet kan komme lidt efter .C
        if time.time() > start + 3 and not ws_aaben(hoved, workspace):
            return "lukket uden spørgsmål"
        for h, t, c in _vinduer():
            p = w.DWORD(); u.GetWindowThreadProcessId(h, ctypes.byref(p))
            if p.value != pid.value or h == hoved or t in ("", "Command Line"):
                continue
            for b, bt, bc in _boern(h):
                if bc == "Button" and bt.replace("&", "") in ("No", "Nej"):
                    u.PostMessageW(b, BM_CLICK, 0, 0)
                    return f"klikket Nej i '{t}'"
            forgrund(h)
            tast(ord("N"))
            return f"tastet N i '{t}'"
        time.sleep(0.5)
    return "intet spørgsmål set"


# ---- Tidslog ----

def log_trin(db, strategi, workspace, trin, start, slut, note=None):
    with db.cursor() as c:
        c.execute("""insert into rawsignal.tidslog (filter, chart, trin, start, slut, note)
                     values (%s, %s, %s, %s, %s, %s)""",
                  (strategi, workspace, trin, start, slut, note))
    db.commit()
    log(f"  {trin}: {slut - start}")


# ---- Indlæsning ----

def indlaes(db, sti, tabel, instrument_id, timeframe_id):
    """CSV -> tabel. Én tabel pr. filter; instrument og timeframe står i hver linje.
    Kun de gamle linjer for samme instrument og timeframe slettes først.
    Alt i én transaktion."""
    with db.cursor() as c:
        c.execute(f"""create table if not exists {tabel} (
                          runid text not null, n1 numeric, n2 numeric,
                          starttid timestamp not null, antalbars integer not null,
                          afsluttet smallint not null,
                          instrument_id integer not null, timeframe_id integer not null)""")
        c.execute(f"create index if not exists {tabel.split('.')[1]}_inst_tf_n1_n2_starttid "
                  f"on {tabel} (instrument_id, timeframe_id, n1, n2, starttid)")
        c.execute(f"delete from {tabel} where instrument_id = %s and timeframe_id = %s",
                  (instrument_id, timeframe_id))
        c.execute("""create temp table ny (
                         runid text, n1 numeric, n2 numeric, starttid timestamp,
                         antalbars integer, afsluttet smallint) on commit drop""")
        with open(sti, encoding="utf-8-sig", newline="") as f:
            c.copy_expert("copy ny (runid, n1, n2, starttid, antalbars, afsluttet) "
                          "from stdin with (format csv, header true)", f)
        c.execute(f"""insert into {tabel} (runid, n1, n2, starttid, antalbars, afsluttet,
                                           instrument_id, timeframe_id)
                      select runid, n1, n2, starttid, antalbars, afsluttet, %s, %s from ny""",
                  (instrument_id, timeframe_id))
        antal = c.rowcount
    db.commit()
    return antal


# ---- Tidsforbrug pr. filter/instrument/timeframe ----

def opdater_runtime(db, strategi, workspace, instrument_id, timeframe_id, tabel):
    """Gennemsnit af alle hele cyklusser i tidslog for samme filter og workspace.
    Kombinationer = antal N1/N2-kombinationer med mindst ét signal."""
    with db.cursor() as c:
        c.execute(f"select count(distinct (n1, n2)) from {tabel} "
                  f"where instrument_id = %s and timeframe_id = %s", (instrument_id, timeframe_id))
        kombinationer = c.fetchone()[0]
        c.execute("""
            insert into rawsignal.rs_tf_runtime
                (filter, instrument_id, timeframe_id, kombinationer, beregning, cyklus,
                 beregning_pr_kombination, sidst_koert, note)
            select %(f)s, %(i)s, %(t)s, %(k)s,
                   make_interval(secs => round(extract(epoch from avg(slut - start) filter (where trin = 'beregning')))),
                   make_interval(secs => round(extract(epoch from avg(slut - start) filter (where trin = 'cyklus')))),
                   make_interval(secs => round(extract(epoch from avg(slut - start) filter (where trin = 'beregning')) / %(k)s, 3)),
                   date_trunc('second', now()::timestamp),
                   'Gennemsnit af ' || count(*) filter (where trin = 'cyklus') || ' hele cyklusser i tidslog.'
            from rawsignal.tidslog
            where filter = %(f)s and chart = %(w)s and trin in ('beregning', 'cyklus')
            on conflict (filter, instrument_id, timeframe_id) do update set
                kombinationer = excluded.kombinationer, beregning = excluded.beregning,
                cyklus = excluded.cyklus, beregning_pr_kombination = excluded.beregning_pr_kombination,
                sidst_koert = excluded.sidst_koert, note = excluded.note""",
                  {"f": strategi, "i": instrument_id, "t": timeframe_id, "k": kombinationer, "w": workspace})
    db.commit()


# ---- Kører TradeStation stadig? ----

class TSNede(RuntimeError):
    """TradeStation er gået ned. Kæden skal stoppe, for næste kørsel kan ikke lykkes."""


def ts_koerer(med_chart=False):
    """Hovedprogrammet (ORPlat) skal køre. Under en beregning skal chart-
    programmet (orchart) også køre: går det ned, holder CSV-filen bare op med
    at blive skrevet, og det ligner en færdig beregning. orchart starter
    først, når et chart åbnes."""
    if not hovedvindue():
        return False
    if not med_chart:
        return True
    ud = subprocess.run(["tasklist", "/FI", "IMAGENAME eq orchart.exe", "/NH"],
                        capture_output=True, text=True).stdout
    return "orchart.exe" in ud.lower()


def beregning_faerdig(sti):
    if not ts_koerer(med_chart=True):
        raise TSNede("TradeStation gik ned under beregningen. CSV-filen er ufuldstændig og indlæses ikke.")
    return time.time() - os.path.getmtime(sti) >= STILLE_SEK


# ---- Cyklus ----

# Returkoder: 0 = ok, 1 = fejl i denne cyklus, 3 = TradeStation kører ikke (stop kæden)
OK, FEJL, TS_NEDE = 0, 1, 3


def main():
    if len(sys.argv) not in (4, 5) or not sys.argv[3].isdigit():
        print('Brug: python rs_ts_cyklus.py <strategi> <symbol> <timeframe_id> ["<workspace>"]')
        return 2
    return koer_cyklus(sys.argv[1], sys.argv[2], int(sys.argv[3]),
                       sys.argv[4] if len(sys.argv) == 5 else None)


def koer_cyklus(strategi, symbol, timeframe_id, workspace=None):
    sti = os.path.join(CSV_MAPPE, strategi + ".csv")
    tabel = "rawsignal." + strategi.lower().replace("-", "_")

    db = forbind()
    with db.cursor() as c:
        c.execute("select instrument_id from public.rs_instrumenter where symbol = %s and aktiv", (symbol,))
        r = c.fetchone()
        c.execute("select data1, data2, data3 from public.timeframes where timeframe_id = %s", (timeframe_id,))
        tf = c.fetchone()
    db.rollback()
    if not r:
        log(f"STOP: {symbol} findes ikke som aktivt instrument i public.rs_instrumenter.")
        return 1
    if not tf or None in tf:
        log(f"STOP: timeframe {timeframe_id} findes ikke (helt udfyldt) i public.timeframes.")
        return 1
    instrument_id = r[0]
    d1, d2, d3 = (int(x) for x in tf)
    workspace = workspace or WORKSPACE_NAVN.format(symbol=symbol, d1=d1, d2=d2, d3=d3)

    hoved = hovedvindue()
    if not hoved:
        log("STOP: TradeStation (ORPlat.exe) kører ikke.")
        return TS_NEDE
    if " - " in titel(hoved).replace("TradeStation  - ", "", 1):
        log(f"STOP: Et workspace er allerede åbent: {titel(hoved)}")
        return 1

    log(f"Cyklus start: {strategi} på {workspace} ({symbol}, timeframe {timeframe_id} = {d1}-{d2}-{d3})")
    cyklus_start = datetime.now()
    try:
        # 1. Åbn workspace
        t0 = datetime.now()
        send_kommando(hoved, f".O {workspace}")
        vent_paa(lambda: ws_aaben(hoved, workspace), 300, "workspace åbnede ikke")
        # Chartet indlæses stadig lige efter åbningen og kan nulstille kommandolinjen
        time.sleep(20)
        log_trin(db, strategi, workspace, "aabn_workspace", t0, datetime.now(),
                 "Inkl. 20 sek ventetid på at chartet er indlæst")

        # 2. Indsæt strategi
        # Strategien sletter og genskaber CSV-filen på første bar. Oprettelsestiden
        # kan ikke bruges (Windows beholder den gamle, når en fil genskabes
        # hurtigt med samme navn), så der ses efter, hvornår filen ændres.
        t0 = datetime.now()
        send_kommando(hoved, f".IST {strategi}")
        vent_paa(lambda: os.path.exists(sti) and os.path.getmtime(sti) >= t0.timestamp(),
                 600, "strategien startede ikke (CSV-filen blev ikke genskabt)")
        startet = datetime.now()
        log_trin(db, strategi, workspace, "indsaet_strategi", t0, startet)

        # 3. Beregning: færdig, når filen ikke er ændret i STILLE_SEK
        vent_paa(lambda: beregning_faerdig(sti), MAX_BEREGNING_SEK, "beregningen blev ikke færdig")
        sidst = datetime.fromtimestamp(os.path.getmtime(sti))
        log_trin(db, strategi, workspace, "beregning", startet, sidst,
                 f"CSV første ændring -> sidst skrevet. Ventet {STILLE_SEK} sek på at filen stod stille.")

        # 4. Luk workspace uden at gemme
        t0 = datetime.now()
        send_kommando(hoved, ".C")
        svar = svar_nej_til_gem(hoved, workspace)
        vent_paa(lambda: not ws_aaben(hoved, workspace), 120, "workspace lukkede ikke")
        log_trin(db, strategi, workspace, "luk_workspace", t0, datetime.now(), svar)

        # 5. Indlæs
        t0 = datetime.now()
        antal = indlaes(db, sti, tabel, instrument_id, timeframe_id)
        log_trin(db, strategi, workspace, "indlaes", t0, datetime.now(), f"{antal} signaler -> {tabel}")

        log_trin(db, strategi, workspace, "cyklus", cyklus_start, datetime.now(), "Hele cyklussen")

        opdater_runtime(db, strategi, workspace, instrument_id, timeframe_id, tabel)
        log(f"  rs_tf_runtime opdateret for {strategi} / {symbol} / timeframe {timeframe_id}")
        return OK
    except Exception as e:
        db.rollback()
        log(f"STOP: {e}")
        return TS_NEDE if isinstance(e, TSNede) or not ts_koerer() else FEJL
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
