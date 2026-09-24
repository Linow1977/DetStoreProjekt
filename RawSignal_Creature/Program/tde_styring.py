# Styring af TradeStation Development Environment (TDE, TSDev.exe).
#
# Selve arbejdet i TDE (opret, indsæt kode, Verify, luk) sker i
# tde\verify-one.ps1. Her findes, åbnes og genstartes TDE, og scriptet kaldes.

import ctypes
import json
import os
import subprocess
import time

from faelles import PROGRAM_MAPPE, log

TSDEV = r"C:\Program Files (x86)\TradeStation 10.0\Program\TSDev.exe"
VERIFY_SCRIPT = os.path.join(PROGRAM_MAPPE, "tde", "verify-one.ps1")
# TDE er et 32-bit program, og verify-scriptet skal køre som 32-bit.
POWERSHELL_32 = r"C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe"

WM_CLOSE = 0x0010
BM_CLICK = 0x00F5
IDNO = 7


def find():
    """(vindue, proces-id) for TDE. None, hvis TDE ikke kører."""
    ud = subprocess.run(
        ["powershell", "-NoProfile", "-Command",
         "Get-Process TSDev -ErrorAction SilentlyContinue | "
         "Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1 | "
         "ForEach-Object { \"$($_.MainWindowHandle) $($_.Id)\" }"],
        capture_output=True, text=True).stdout.strip()
    if not ud:
        return None
    vindue, pid = ud.split()
    return int(vindue), int(pid)


def find_eller_aabn():
    """Finder TDE. Kører den ikke, åbnes den, og der ventes op til 90
    sekunder på vinduet. None, hvis det ikke lykkes."""
    tde = find()
    if tde is not None:
        return tde
    log("TDE kører ikke - åbner den.")
    # Startes fra sin egen mappe - ellers holder TDE programmappen låst,
    # så længe den kører.
    subprocess.Popen([TSDEV], cwd=os.path.dirname(TSDEV))
    # TDE viser først et midlertidigt vindue og derefter det rigtige. Der
    # ventes, til samme vindue har stået i 5 sekunder.
    forrige, stabil = None, 0
    for _ in range(90):
        time.sleep(1)
        tde = find()
        stabil = stabil + 1 if (tde is not None and tde == forrige) else 0
        forrige = tde
        if stabil >= 5:
            return tde
    return None


def _svar_nej_til_gem(pid):
    """Klikker "Nej" i TDE's "Gem ændringer?"-boks, hvis den er åben.

    Et afbrudt forsøg efterlader et ugemt dokument, og så spørger TDE ved
    lukning. Uden svar må TDE lukkes med magt, og en TDE lukket med magt
    har vist sig at kunne starte i en tilstand, hvor Verify ikke virker.
    Dokumentet laves alligevel forfra, så intet går tabt ved at svare nej.
    """
    user32 = ctypes.windll.user32
    fundne = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_void_p, ctypes.c_void_p)
    def hvert_vindue(h, _):
        vpid = ctypes.c_ulong()
        user32.GetWindowThreadProcessId(ctypes.c_void_p(h), ctypes.byref(vpid))
        klasse = ctypes.create_unicode_buffer(64)
        user32.GetClassNameW(ctypes.c_void_p(h), klasse, 64)
        if vpid.value == pid and klasse.value == "#32770" and user32.IsWindowVisible(ctypes.c_void_p(h)):
            fundne.append(h)
        return True

    user32.EnumWindows(hvert_vindue, None)
    for boks in fundne:
        nej = user32.GetDlgItem(ctypes.c_void_p(boks), IDNO)
        if nej:
            user32.PostMessageW(ctypes.c_void_p(nej), BM_CLICK, 0, 0)
            log("TDE spurgte om at gemme - svarede Nej.")


def genstart(tde):
    """Lukker TDE og åbner den igen. Bruges, når der ikke er kontakt til TDE.
    TDE bedes først om at lukke pænt, og spørger den om at gemme, svares der
    Nej. Er den ikke lukket efter 30 sekunder, lukkes den med magt."""
    vindue, pid = tde
    log("Ingen kontakt til TDE - lukker og åbner den igen.")
    ctypes.windll.user32.PostMessageW(vindue, WM_CLOSE, 0, 0)
    for _ in range(30):
        time.sleep(1)
        if find() is None:
            break
        _svar_nej_til_gem(pid)
    else:
        log("TDE lukkede ikke af sig selv - lukkes med magt.")
        subprocess.run(["taskkill", "/PID", str(pid), "/F"], capture_output=True)
        time.sleep(3)
    return find_eller_aabn()


def verificer(tde, sti, filtype):
    """Opretter filen i TDE og kører Verify. filtype er "Strategy" eller "ShowMe".

    Returnerer (resultat, note):
      Pass     - 0 fejl
      Fail     - koden har fejl; note er TDE's fejltekst
      Afbrudt  - automationen kunne ikke gennemføres (ingen kontakt til TDE)
    """
    vindue, pid = tde
    ud = subprocess.run(
        [POWERSHELL_32, "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", VERIFY_SCRIPT,
         "-MainHwnd", str(vindue), "-ProcId", str(pid), "-ElPath", sti, "-Type", filtype],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    for linje in ud.stdout.splitlines():
        if linje.strip().startswith("{"):
            svar = json.loads(linje)
            fil = os.path.basename(sti)
            if svar.get("Overskrevet"):
                log(f"{fil}: fandtes i TradeStation - koden er overskrevet med den nye.")
            if svar.get("Lukket") is False:
                log(f"{fil}: ADVARSEL - dokumentet blev ikke lukket i TDE.")
            return svar["Resultat"], svar.get("Note") or ""
    return "Afbrudt", f"Uventet svar fra verify-scriptet: {ud.stdout} {ud.stderr}".strip()
