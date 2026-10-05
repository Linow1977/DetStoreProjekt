# Kører rs_ts_cyklus for én strategi på ét instrument og flere timeframes efter
# hinanden.
#   - Fejler en cyklus, lukkes workspacet, og kæden springer videre til næste.
#   - Går TradeStation ned, stopper kæden helt (resten kan ikke lykkes).
#   - Med --vent startes der først, når sessionen er flyttet til serveren
#     (Forlad_server_uden_at_stoppe.bat) + 1 minut. Skærmskiftet midt i en
#     beregning fik TradeStation til at gå ned 02-10-2026.
#
# Brug:  python rs_ts_kaede.py [--vent] <strategi> <symbol> <timeframe_id> [<timeframe_id> ...]
#        fx  python rs_ts_kaede.py --vent RawSignal002-Test CL 1 2 3 4 5 6 7 8 9 10 11 12

import ctypes
import sys
import time

import rs_ts_cyklus as cyklus
from faelles import log

VENT_EFTER_FLYTNING_SEK = 60


def paa_konsol():
    """Sand, når denne session er serverens egen (flyttet med tscon)."""
    k = ctypes.windll.kernel32
    min_session = ctypes.c_ulong()
    k.ProcessIdToSessionId(k.GetCurrentProcessId(), ctypes.byref(min_session))
    return min_session.value == k.WTSGetActiveConsoleSessionId()


def luk_aabent_workspace():
    """Lukker et workspace, som en fejlet cyklus har efterladt åbent."""
    h = cyklus.hovedvindue()
    if not h:
        return
    t = cyklus.titel(h)
    if " - " not in t.replace("TradeStation  - ", "", 1):
        return
    ws = t.split(" - ", 2)[-1]
    try:
        cyklus.send_kommando(h, ".C")
        log(f"  Lukket efter fejl: {ws} ({cyklus.svar_nej_til_gem(h, ws)})")
        time.sleep(3)
    except Exception as e:
        log(f"  Kunne ikke lukke {ws}: {e}")


def main():
    args = sys.argv[1:]
    vent = "--vent" in args
    args = [a for a in args if a != "--vent"]
    if len(args) < 3 or not all(a.isdigit() for a in args[2:]):
        print("Brug: python rs_ts_kaede.py [--vent] <strategi> <symbol> <timeframe_id> [<timeframe_id> ...]")
        return 2
    strategi, symbol, timeframes = args[0], args[1], [int(a) for a in args[2:]]

    if vent and not paa_konsol():
        log("Venter på, at sessionen flyttes til serveren (Forlad_server_uden_at_stoppe.bat)...")
        while not paa_konsol():
            time.sleep(5)
        log(f"Sessionen er flyttet. Venter {VENT_EFTER_FLYTNING_SEK} sek, før første kørsel.")
        time.sleep(VENT_EFTER_FLYTNING_SEK)

    log(f"Kæde start: {strategi} / {symbol} / timeframes {timeframes}")
    ok, fejl = [], []
    for nr, tf in enumerate(timeframes):
        resultat = cyklus.koer_cyklus(strategi, symbol, tf)
        if resultat == cyklus.OK:
            ok.append(tf)
        elif resultat == cyklus.TS_NEDE:
            fejl.append(tf)
            log(f"STOP: TradeStation kører ikke. Ikke kørt: {timeframes[nr + 1:]}")
            break
        else:
            fejl.append(tf)
            log(f"  Timeframe {tf} fejlede. Springer videre.")
            luk_aabent_workspace()
        time.sleep(10)

    log(f"Kæde slut. OK: {ok}. Fejlet: {fejl or 'ingen'}.")
    return 0 if not fejl else 1


if __name__ == "__main__":
    sys.exit(main())
