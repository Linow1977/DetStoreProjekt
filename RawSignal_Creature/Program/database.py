# Alt, RawSignal Creature læser og skriver i TradingDB (undtagen indlæsning
# af CSV, som ligger i indlaes_csv.py).
#
#   filter_case        filtrene; kolonnen rawsignal_faerdig markerer færdige
#   rawsignal          én række pr. godkendt strategi
#   rawsignal_kontrol  én række pr. godkendt ShowMe (samme kolonner)


def hent_filter(db, filter_case_id):
    """Én række fra filter_case som en ordbog. None, hvis den ikke findes."""
    with db.cursor() as c:
        c.execute("""select filter_case_id, filtere,
                            filter1_n1_start, filter1_n1_end, filter1_n1_step,
                            filter1_n2_start, filter1_n2_end, filter1_n2_step
                     from filter_case where filter_case_id = %s""", (filter_case_id,))
        r = c.fetchone()
        if r is None:
            return None
        return dict(zip([d[0] for d in c.description], r))


def naeste_filter(db):
    """Laveste filter_case_id, der endnu ikke er lavet til en RawSignal."""
    with db.cursor() as c:
        c.execute("select min(filter_case_id) from filter_case where rawsignal_faerdig is null")
        return c.fetchone()[0]


def findes_allerede(db, navn, kontrol_navn):
    """Står strategien eller ShowMe'en allerede i tabellerne?"""
    with db.cursor() as c:
        c.execute("select 1 from rawsignal where rawsignal_name = %s", (navn,))
        strategi = c.fetchone() is not None
        c.execute("select 1 from rawsignal_kontrol where rawsignal_kontrol_name = %s", (kontrol_navn,))
        kontrol = c.fetchone() is not None
    return strategi or kontrol


def gem_resultat(db, filter_case_id, a, sti_s, sti_k, strategi, kontrol):
    """Skriver begge rækker og markerer filteret som færdigt i ÉN transaktion,
    så en halv kørsel aldrig står som færdig. strategi og kontrol er
    (resultat, note) fra verificeringen."""
    for tabel, (resultat, note) in (("rawsignal", strategi), ("rawsignal_kontrol", kontrol)):
        with db.cursor() as c:
            c.execute(f"""insert into {tabel}
                            (dev_date, rawsignal_kontrol_name, rawsignal_kontrol_path,
                             verification, rawsignal_name, rawsignal_path, note)
                          values (date_trunc('second', now()), %s, %s, %s, %s, %s, %s)""",
                      (a["kontrol_navn"], sti_k, resultat, a["navn"], sti_s, note))
    with db.cursor() as c:
        c.execute("""update filter_case set rawsignal_faerdig = date_trunc('second', now())
                     where filter_case_id = %s""", (filter_case_id,))
    db.commit()
