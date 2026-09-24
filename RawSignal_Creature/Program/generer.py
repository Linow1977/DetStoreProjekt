# Bygger teksten til de to EasyLanguage-filer for ét filter:
#   RawSignal<nr>           strategi, skriver én CSV-linje pr. signal
#   RawSignal<nr>_Kontrol   ShowMe, tegner kun
#
# CSV-formatet (RawSignal_CSV-format.docx, 24-09-2026):
#   RunID,N1,N2,Starttid,AntalBars,Afsluttet
#   Kun de parametre, formlen bruger, får en kolonne. Uden parametre skrives
#   N1 = 1, så alle filer har samme form. Afsluttet = 0 betyder, at signalet
#   stadig var tændt på chartets sidste bar.
#
# Filnavnet på CSV-filen står ordret fire steder i strategien (FileDelete,
# overskrift, slukning og sidste bar), fordi Print(File(...)) kræver et fast
# filnavn i anførselstegn.

from datetime import datetime

import max_bars_back
from faelles import CSV_MAPPE
from formel import ARRAY_STOERRELSE, ByggeFejl, analyser, tal_tekst, udskift

# Målt status for hukommelsesproblemet. Filtre, der ikke står her, er
# ikke målt. Teksten må kun oplyse status, aldrig forudsige et resultat.
# Numrene er efter omnummereringen 24-09-2026 (filter 1 "True;" slettet,
# alle andre rykket én ned). Målingerne blev lavet under de gamle numre.
MAALT_STATUS = {
    68: "Målt og ramt (som gamle RawSignal069): alle 625 kombinationer gav de samme 4.918 signaler.",
    265: "Målt og virker sandsynligvis (som gamle RawSignal266): hver N1 gav forskellige signaler.",
}


# ---------------------------------------------------------------- fælles hoved

def hoved_faelles(a, linjer):
    """Kilde, formel og parametre - ens i strategi og ShowMe."""
    linjer.append(f"// Kilde: TradingDB, tabellen filter_case, filter_case_id = {a['id']}")
    linjer.append("//")
    linjer.append("// Formel fra databasen (uændret):")
    linjer.append(f"//   {a['raa_formel']}")
    linjer.append("//")
    if a["parametre"]:
        navne = " og ".join("Filter1_" + p["navn"] for p in a["parametre"])
        linjer.append(f"// Parametre som formlen bruger: {navne}")
    else:
        linjer.append("// Formlen bruger ingen parametre - der findes kun én variant.")
    if a["bruger_b"]:
        linjer.append("// Formlen bruger DataFilter_B. Chartet skal have mindst tre datastrømme.")


def hoved_genereret(linjer):
    """Hvornår filen er lavet, og at den aldrig må rettes i hånden."""
    linjer.append("//")
    linjer.append(f"// Genereret af RawSignal Creature {datetime.now():%Y-%m-%d %H:%M}.")
    linjer.append("// Ret ALDRIG i filen i hånden. Ret i filter_case, og lad programmet")
    linjer.append("// lave filen forfra.")


# ---------------------------------------------------------------- strategi

def byg_strategi(a):
    """Strategien RawSignal<nr>. Returnerer (tekst, formlen som den står i koden)."""
    navn = a["navn"]
    csv = CSV_MAPPE + "\\" + navn + ".csv"
    p = a["parametre"]
    formel_kode = udskift(a["formel"], {"Filter1_" + x["navn"]: x["vaerdi"] for x in p})

    L = ["{", f"//***** {navn}",
         "// Råt signal: registrerer KUN hvornår filteret tænder, og hvor længe det er",
         "// tændt. Skriver én linje i CSV-filen pr. signal. Ingen handelslogik.",
         f"// Kontrol: ShowMe'en {a['kontrol_navn']} tegner det samme signal på chartet.",
         "//"]
    hoved_faelles(a, L)
    if not p:
        L.append("// N1-kolonnen skrives alligevel (altid 1), så alle RawSignal-filer har")
        L.append("// samme format og kan læses af Python på samme måde.")
    hoved_genereret(L)

    # Advarslen hører kun til, hvor problemet kan opstå: en seriefunktion
    # kaldt i en løkke med skiftende parametre.
    if a["seriefunktioner"] and p:
        status = MAALT_STATUS.get(a["id"], "Ikke målt.")
        L += ["//", "//",
              "// KENDT PROBLEM - LÆS DETTE, FØR TALLENE BRUGES",
              "//",
              f"// Formlen bruger seriefunktion(er): {', '.join(a['seriefunktioner'])}.",
              "// Sådanne funktioner husker deres forrige værdi, og hukommelsen hører til",
              "// kodelinjen, ikke til parameterværdien. Kaldes linjen i en løkke med mange",
              "// parametre, deler alle kombinationer hukommelse, og tallene kan blive",
              "// forkerte uden fejlmelding. Verify viser ikke, om filen er ramt.",
              "//",
              f"// Status for dette filter: {status}"]

    L += ["//", "//",
          "// CSV-KOLONNER",
          "// Starttid  = baren hvor filteret tænder.",
          "// AntalBars = antal Data2-bars filteret er tændt i træk.",
          "// Afsluttet = 1, når filteret slukkede. 0, når det stadig var tændt på",
          "//             chartets sidste bar - så er AntalBars ikke færdigt.",
          "//",
          "// VIGTIGT: Kør som almindelig backtest - IKKE via Optimize.",
          "// VIGTIGT: CSV-filen skal være lukket i Excel, mens der køres.",
          "// VIGTIGT: Data1 skal have samme tidsramme som Data2. AntalBars tælles i",
          "//          Data2-bars, så ellers stopper strategien med en fejl."]
    mbb = max_bars_back.tekst(a)
    L.append(f"// VIGTIGT: Max Bars Back: {mbb[0]}")
    L += ["//          " + t for t in mbb[1:]]
    if p:
        L.append(f"// VIGTIGT: Arrays har {ARRAY_STOERRELSE} pladser pr. parameter. Giver Fra/Til/Step")
        L.append("//          flere pladser, SKAL arrayet hæves i koden.")
    L += ["}", ""]

    # Input
    inp = ["\tint    DataFilter_A( 2 )"]
    if a["bruger_b"]:
        inp.append("\tint    DataFilter_B( 3 )")
    for x in p:
        t = "double" if x["decimal"] else "int   "
        inp.append(f"\t{t} {x['navn']}_Fra( {tal_tekst(x['start'])} )")
        inp.append(f"\t{t} {x['navn']}_Til( {tal_tekst(x['slut'])} )")
        inp.append(f"\t{t} {x['navn']}_Step( {tal_tekst(x['step'])} )")
    L.append("Input:")
    L.append(",\n".join(inp) + ";")
    L.append("")

    # Arrays eller almindelige variabler
    if p:
        dim = "[" + ",".join(str(ARRAY_STOERRELSE) for _ in p) + "]"
        idx = "[" + ",".join(x["plads"] for x in p) + "]"
        L.append(f"// Én plads pr. parameterværdi, {ARRAY_STOERRELSE} pladser pr. parameter.")
        L.append("Arrays:")
        L.append(f"\tint    Filter1{dim}( 0 ),")
        L.append(f"\tint    Filter1_Forrige{dim}( 0 ),")
        L.append(f"\tint    SignalBars{dim}( 0 ),")
        L.append(f"\tstring StartTekst{dim}( \"\" );")
        L.append("")
        var = []
        for x in p:
            if x["decimal"]:
                var.append(f"\tdouble {x['vaerdi']}( 0 )")
                var.append(f"\tint    {x['plads']}( 0 )")
            else:
                var.append(f"\tint    {x['vaerdi']}( 0 )")
    else:
        idx = ""
        var = ["\tint    Filter1( 0 )",
               "\tint    Filter1_Forrige( 0 )",
               "\tint    SignalBars( 0 )",
               "\tstring StartTekst( \"\" )"]
    var.append("\tint    SlutSkrevet( 0 )")
    var.append("\tstring BarTekst( \"\" )")
    L.append("Var:")
    L.append(",\n".join(var) + ";")
    L.append("")

    # Overskrift og CSV-værdier
    kolonner = (["RunID"] + ([x["navn"] for x in p] if p else ["N1"])
                + ["Starttid", "AntalBars", "Afsluttet"])
    overskrift = ",".join(kolonner)

    L += ["",
          "//----- Engangsopsætning: tjek datastrømme, nulstil filen, skriv overskrift -----//",
          "",
          "\tOnce",
          "\t\tBegin",
          "\t\t// AntalBars tælles i Data2-bars. Har Data1 en anden tidsramme, bliver",
          "\t\t// tallene forkerte, så strategien stopper, før der skrives noget.",
          "\t\tIf BarType <> BarType of data(DataFilter_A)",
          "\t\t   or BarInterval <> BarInterval of data(DataFilter_A) Then",
          "\t\t\tRaiseRunTimeError( \"Data1 skal have samme tidsramme som Data2. Ret Data1 i chartet.\" );",
          "",
          f"\t\tFileDelete( \"{csv}\" );",
          f"\t\tPrint( File(\"{csv}\"), \"{overskrift}\" );",
          "\t\tEnd;",
          "",
          "",
          "//----- Tidsstempel for den aktuelle bar (samme for alle kombinationer) -----//",
          "",
          "\tBarTekst = FormatDate( \"yyyy-MM-dd\", ELDateToDateTime( Date of data(DataFilter_A) ) )",
          "\t         + \" \"",
          "\t         + FormatTime( \"HH:mm\", ELTimeToDateTime( Time of data(DataFilter_A) ) );",
          "", ""]

    # Selve kroppen - samme tekst uanset antal løkker, kun indrykningen skifter
    if p:
        vaerdier = [f"NumToStr( {x['vaerdi']}, {2 if x['decimal'] else 0} )" for x in p]
    else:
        vaerdier = ["\"1\""]

    def csv_linje(afsluttet):
        """CSV-linjen. Bruges både når filteret slukker og på sidste bar."""
        linjer = [f"\tPrint( File(\"{csv}\"),",
                  f"\t       \"{navn}\" + \",\""]
        linjer += [f"\t     + {v} + \",\"" for v in vaerdier]
        linjer += [f"\t     + StartTekst{idx} + \",\"",
                   f"\t     + NumToStr( SignalBars{idx}, 0 ) + \",\"",
                   f"\t     + \"{afsluttet}\" );"]
        return linjer

    krop = ["// Selve filteret - formlen fra databasen, uændret",
            f"If {formel_kode} Then",
            f"\tFilter1{idx} = 1",
            "Else",
            f"\tFilter1{idx} = 0;",
            "",
            "// TÆNDER",
            f"If Filter1{idx} = 1 and Filter1_Forrige{idx} = 0 Then",
            "\tBegin",
            f"\tStartTekst{idx} = BarTekst;",
            f"\tSignalBars{idx} = 1;",
            "\tEnd;",
            "",
            "// FORTSÆTTER",
            f"If Filter1{idx} = 1 and Filter1_Forrige{idx} = 1 Then",
            f"\tSignalBars{idx} = SignalBars{idx} + 1;",
            "",
            "// SLUKKER - linjen skrives her, Afsluttet = 1",
            f"If Filter1{idx} = 0 and Filter1_Forrige{idx} = 1 Then",
            "\tBegin"]
    krop += csv_linje(1)
    krop += [f"\tSignalBars{idx} = 0;",
             "\tEnd;",
             "",
             "// SIDSTE BAR - et signal, der stadig er tændt, skrives med Afsluttet = 0",
             f"If LastBarOnChart and SlutSkrevet = 0 and Filter1{idx} = 1 Then",
             "\tBegin"]
    krop += csv_linje(0)
    krop += ["\tEnd;",
             "",
             f"Filter1_Forrige{idx} = Filter1{idx};"]

    if not p:
        L.append("//----- Filter og signal-registrering -----//")
        L.append("")
        L += [("\t" + k) if k else "" for k in krop]
    else:
        L.append("//----- Alle kombinationer gennemløbes på hver bar -----//")
        L.append("")
        # Løkkerne åbnes udefra og ind
        for n, x in enumerate(p):
            ind = "\t" * (1 + 2 * n)
            L.append(f"{ind}{x['vaerdi']} = {x['navn']}_Fra;")
            if x["decimal"]:
                L.append(f"{ind}{x['plads']} = 1;")
            L.append(f"{ind}While {x['vaerdi']} <= {x['navn']}_Til")
            L.append(f"{ind}\tBegin")
            L.append("")
        ind = "\t" * (1 + 2 * len(p))
        L += [(ind + k) if k else "" for k in krop]
        # og lukkes indefra og ud
        for n in reversed(range(len(p))):
            x = p[n]
            ind = "\t" * (2 + 2 * n)
            L.append("")
            L.append(f"{ind}{x['vaerdi']} = {x['vaerdi']} + {x['navn']}_Step;")
            if x["decimal"]:
                L.append(f"{ind}{x['plads']} = {x['plads']} + 1;")
            L.append(f"{ind}End;")

    # Sidste bar er nu skrevet for alle kombinationer. Kommer der nye bars
    # (live-data), skrives den ikke igen.
    L += ["",
          "",
          "//----- Sidste bar er skrevet - skriv den ikke igen -----//",
          "",
          "\tIf LastBarOnChart Then",
          "\t\tSlutSkrevet = 1;"]

    tekst = "\n".join(L) + "\n"

    # Filnavnet skal stå ordret fire steder: FileDelete, overskrift,
    # slukning og sidste bar. RunID er filnavnet.
    if tekst.count(f"\"{csv}\"") != 4:
        raise ByggeFejl(f"{navn}: filnavnet står ikke præcis fire steder.")
    return tekst, formel_kode


# ---------------------------------------------------------------- ShowMe

def byg_kontrol(a):
    """ShowMe'en RawSignal<nr>_Kontrol. Returnerer (tekst, formlen som den står i koden)."""
    navn = a["kontrol_navn"]
    p = a["parametre"]
    formel_kode = udskift(a["formel"], {"Filter1_" + x["navn"]: "Vis_" + x["navn"] for x in p})

    L = ["{", f"//***** {navn}",
         f"// Kontrol-ShowMe til strategien {a['navn']}. Tegner KUN - skriver ingen fil.",
         "//",
         "// Plot1 sætter en prik på den bar, hvor filteret tænder (skiftet fra falsk",
         "// til sand). Det svarer til kolonnen Starttid i strategiens CSV-fil.",
         "//"]
    hoved_faelles(a, L)
    hoved_genereret(L)
    L.append("//")
    if p:
        navne = " og ".join("Vis_" + x["navn"] for x in p)
        L.append(f"// Ét parametersæt vises ad gangen. Vælg det med {navne} under Inputs.")
        L.append("// Formlen regnes uden løkke, så seriefunktioner regner rigtigt her.")
        L.append("//")
    mbb = max_bars_back.tekst(a)
    L += ["// VIGTIGT: Chartet skal have samme datastrømme som strategien"
          + (" (Data2 og Data3)." if a["bruger_b"] else " (Data2)."),
          f"// VIGTIGT: Max Bars Back: {mbb[0]}"]
    L += ["//          " + t for t in mbb[1:]]
    L += ["}", ""]

    inp = ["\tint    DataFilter_A( 2 )"]
    if a["bruger_b"]:
        inp.append("\tint    DataFilter_B( 3 )")
    for x in p:
        t = "double" if x["decimal"] else "int   "
        inp.append(f"\t{t} Vis_{x['navn']}( {tal_tekst(x['start'])} )")
    L.append("Input:")
    L.append(",\n".join(inp) + ";")
    L.append("")
    L += ["Var:",
          "\tint    Vis_Taendt( 0 ),",
          "\tint    Vis_Forrige( 0 );",
          "",
          "",
          "//----- Selve filteret - formlen fra databasen, uændret -----//",
          "",
          f"\tIf {formel_kode} Then",
          "\t\tVis_Taendt = 1",
          "\tElse",
          "\t\tVis_Taendt = 0;",
          "",
          "",
          "//----- Tegning: kun hvor filteret tænder -----//",
          "",
          "\tIf Vis_Taendt = 1 and Vis_Forrige = 0 Then",
          "\t\tPlot1( Low of data(DataFilter_A), \"Start\" );",
          "",
          "\t// Opdateres efter plottet, så den altid er forrige bars status.",
          "\tVis_Forrige = Vis_Taendt;",
          ""]
    return "\n".join(L), formel_kode


# ---------------------------------------------------------------- samlet

def byg_filer(raekke):
    """Returnerer analysen og teksten til begge filer. Gemmer intet."""
    a = analyser(raekke)
    strategi, formel_s = byg_strategi(a)
    kontrol, formel_k = byg_kontrol(a)

    # Formelteksten skal være ordret ens i begge filer og i databasen, når
    # parameternavnene føres tilbage.
    tilbage_s = udskift(formel_s, {x["vaerdi"]: "Filter1_" + x["navn"] for x in a["parametre"]})
    tilbage_k = udskift(formel_k, {"Vis_" + x["navn"]: "Filter1_" + x["navn"] for x in a["parametre"]})
    # Parameternavnet kan være stavet med små bogstaver i databasen, så
    # originalen skrives med samme stavning, før der sammenlignes.
    original = udskift(a["formel"], {"Filter1_" + x["navn"]: "Filter1_" + x["navn"] for x in a["parametre"]})
    if not (tilbage_s == tilbage_k == original):
        raise ByggeFejl(f"Filter {a['id']}: formelteksten er ikke ens i strategi og ShowMe.")
    return a, strategi, kontrol
