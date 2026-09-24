# RawSignal Creature - laver ét filter fra filter_case til en RawSignal.
#
# Brug:  python rawsignal_creature.py [filter_case_id]
#        Uden nummer køres det næste filter, der ikke er færdigt.
#
# De fire trin (OPGAVEBESKRIVELSE_RawSignal.md):
#   1. Filteret hentes i TradingDB (filter_case)
#   2. Omskrives til strategi RawSignal<nr> og ShowMe RawSignal<nr>_Kontrol
#   3. Begge verificeres i TDE (TradeStation Development Environment)
#   4. Resultatet skrives i rawsignal og rawsignal_kontrol, og filteret
#      markeres som færdigt i filter_case
#
# Findes navnet allerede i en af tabellerne, springes filteret over. Det
# forhindrer, at TDE forsøger at oprette en strategi, der findes i forvejen.
#
# Går noget galt, stopper programmet uden at skrive i databasen. Fejlen
# rettes, det der blev lavet ryddes op, og filteret køres forfra.

import os
import sys

import database
import generer
import tde_styring
from faelles import (EL_MAPPE_KONTROL, EL_MAPPE_STRATEGI, TXT_MAPPE_KONTROL,
                     TXT_MAPPE_STRATEGI, forbind, log)
from formel import ByggeFejl


def gem_fil(sti, tekst):
    # UTF-8 med BOM, så æ, ø og å vises rigtigt i alle Windows-programmer.
    with open(sti, "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(tekst)


def verificer_begge(a, sti_s, sti_k):
    """Verificerer strategi og ShowMe i TDE.

    Afbrydes verificeringen (ingen kontakt til TDE), genstartes TDE, og begge
    verificeres forfra. Det sker højst én gang. Returnerer to par
    (resultat, note), eller None, hvis TDE ikke kunne åbnes.
    """
    forbindelse = tde_styring.find_eller_aabn()
    if forbindelse is None:
        return None
    for forsoeg in (1, 2):
        strategi = tde_styring.verificer(forbindelse, sti_s, "Strategy")
        log(f"{a['navn']}: {strategi[0]}  {strategi[1]}")
        if strategi[0] == "Afbrudt":
            kontrol = ("Afbrudt", "Ikke kørt, fordi strategien blev afbrudt.")
        else:
            kontrol = tde_styring.verificer(forbindelse, sti_k, "ShowMe")
            log(f"{a['kontrol_navn']}: {kontrol[0]}  {kontrol[1]}")

        afbrudt = "Afbrudt" in (strategi[0], kontrol[0])
        if not afbrudt or forsoeg == 2:
            return strategi, kontrol
        forbindelse = tde_styring.genstart(forbindelse)
        if forbindelse is None:
            return None
        log(f"{a['navn']}: TDE er genstartet - verificerer forfra.")


def koer_filter(db, filter_case_id):
    """Hele forløbet for ét filter. Returnerer 0 ved succes eller overspring, ellers 1."""
    # ---- 1. Hent filteret ----
    raekke = database.hent_filter(db, filter_case_id)
    if raekke is None:
        log(f"Filter {filter_case_id}: findes ikke i filter_case.")
        return 1

    # ---- 2. Byg begge filer (gemmes først, når alt er kontrolleret) ----
    try:
        a, strategi, kontrol = generer.byg_filer(raekke)
    except ByggeFejl as e:
        log(f"STOP: {e}")
        return 1

    if database.findes_allerede(db, a["navn"], a["kontrol_navn"]):
        log(f"{a['navn']}: SPRUNGET OVER - navnet findes allerede i rawsignal eller rawsignal_kontrol.")
        return 0

    sti_s = os.path.join(EL_MAPPE_STRATEGI, a["navn"] + ".el")
    sti_k = os.path.join(EL_MAPPE_KONTROL, a["kontrol_navn"] + ".el")
    gem_fil(sti_s, strategi)
    gem_fil(sti_k, kontrol)
    gem_fil(os.path.join(TXT_MAPPE_STRATEGI, a["navn"] + ".txt"), strategi)
    gem_fil(os.path.join(TXT_MAPPE_KONTROL, a["kontrol_navn"] + ".txt"), kontrol)
    log(f"{a['navn']}: filer gemt (.el og .txt): {sti_s} og {sti_k}")

    # ---- 3. Verificer i TDE ----
    resultater = verificer_begge(a, sti_s, sti_k)
    if resultater is None:
        log("STOP: TDE (TSDev.exe) kunne ikke åbnes.")
        return 1
    res_s, res_k = resultater
    if res_s[0] != "Pass":
        log(f"STOP: {a['navn']} blev ikke godkendt. Intet skrevet i databasen.")
        return 1
    if res_k[0] != "Pass":
        log(f"STOP: {a['kontrol_navn']} blev ikke godkendt. Intet skrevet i databasen.")
        return 1

    # ---- 4. Skriv i tabellerne og markér som færdig ----
    # Kun når begge filer er godkendt. Ellers ville filteret blive sprunget
    # over næste gang, før fejlen er løst.
    database.gem_resultat(db, filter_case_id, a, sti_s, sti_k, res_s, res_k)
    log(f"{a['navn']}: skrevet i rawsignal ({res_s[0]}) og rawsignal_kontrol ({res_k[0]}), "
        "og markeret som færdig i filter_case.")
    return 0


def main():
    if len(sys.argv) > 2 or (len(sys.argv) == 2 and not sys.argv[1].isdigit()):
        print("Brug: python rawsignal_creature.py [filter_case_id]")
        print("      Uden nummer køres det næste filter, der ikke er færdigt.")
        return 2

    db = forbind()
    try:
        if len(sys.argv) == 2:
            filter_case_id = int(sys.argv[1])
        else:
            filter_case_id = database.naeste_filter(db)
            if filter_case_id is None:
                log("Alle filtre i filter_case er færdige - intet at køre.")
                return 0
            log(f"Næste filter, der ikke er færdigt: {filter_case_id}")
        return koer_filter(db, filter_case_id)
    finally:
        db.close()


if __name__ == "__main__":
    sys.exit(main())
