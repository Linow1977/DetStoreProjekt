# RawSignal – opgavebeskrivelse

Opdateret 23. september 2026. Erstatter alle tidligere versioner.
Læs også `BYGGEVEJLEDNING_RawSignal.md` og `NOTAT_til_BYGGEVEJLEDNING_RawSignal.md`.
Er de uenige med dette dokument, følg dette dokument.

Regler for Claude Code: tænk før du bygger, gæt aldrig, spørg ved tvivl, og lav kun de ændringer,
opgaven kræver. Punkt 12 er de ting, Thomas endnu ikke har afgjort. Dem må du ikke selv afgøre.

---

## 1. Formål

RawSignal-filer registrerer kun to ting: HVORNÅR et filter tænder, og hvor mange Data2-bars det er
tændt. Ingen handelslogik, ingen analyse. De bruges kun, mens signalerne analyseres. En rigtig
handelskode skrives senere.

## 2. To filer pr. filter (besluttet af Thomas)

```
Filter_Case (databasen)   <- det eneste Thomas ændrer
        |
        v   programmet laver begge filer ud fra samme række
RawSignal069             Strategi  Skriver CSV. Bruges i rørledningen som planlagt.
RawSignal069_Kontrol     ShowMe    Tegner kun. Bruges, når Thomas selv vil se signalet.
```

- Begge filer laves, verificeres og lægges i hver sin mappe.
- Filerne rettes aldrig i hånden. Kun `Filter_Case` ændres, og programmet laver filerne forfra.
- Formelteksten skal være ordret ens i begge filer. Programmet skal tjekke det, før filerne gemmes.
- ShowMe'en åbnes i TDE med Alt+Ctrl+M, så koden kan lægges ind, navngives og verificeres.
- Navne: strategien hedder `RawSignal<nr>`, ShowMe'en `RawSignal<nr>_Kontrol`.
- Strategi- og studienavne skal være unikke i TradeStation. Slå altid op i tabellen først (punkt 3),
  og spring over, hvis navnet allerede findes.
- Versionsnummer i filnavnene (når en formel i `Filter_Case` ændres) tages først, når det bliver aktuelt.

## 3. Tabeller i TradingDB

| Fil | Tabel |
|---|---|
| Strategi `RawSignal<nr>` | `rawsignal` (findes allerede, uændret) |
| ShowMe `RawSignal<nr>_Kontrol` | `RawSignal_Kontrol` (NY, gemmes af PostgreSQL som `rawsignal_kontrol`) |

Den nye tabel har samme kolonner som `rawsignal`:

| Kolonne | Indhold |
|---|---|
| `rawsignal_name` | fx `RawSignal069_Kontrol`, primærnøgle, sikrer unikke navne |
| `dev_date` | byggedato, hele sekunder |
| `signal_path` | hvor `.el`-filen ligger |
| `verification` | `OK` eller `FEJLET` |
| `note` | fejl- eller advarselstekst fra Output-panelet |

Koblingen mellem de to filer ligger i navnet (`RawSignal069` og `RawSignal069_Kontrol`).
Skal tabellen til strategifilen omdøbes for symmetriens skyld: se punkt 12.

## 4. Signal-definition (låst)

- Signal = filteret skifter fra FALSK til SAND.
- Varighed (`AntalBars`) = antal Data2-bars filteret bliver ved med at være SAND i træk.
- Én linje pr. signal, skrevet når filteret slukker.
- "Én linje pr. sand bar" må IKKE bruges.
- Ændres definitionen, skal alle backtests køres om. Spørg Thomas først.

```
Data2-bar:  1    2    3    4    5    6    7    8
Filter:     nej  nej  JA   JA   JA   nej  JA   nej
                      ^              ^
                 Signal 1        Signal 2
                 AntalBars 3     AntalBars 1
```

## 5. AntalBars tælles i Data2-bars

- Data2 er filterets egen tidsramme (`DataFilter_A`, altid 2).
- I dag er Data1 og Data2 lige store (bekræftet af Thomas). Så tæller strategien, som kører på Data1,
  allerede rigtigt. Eksisterende filer skal ikke køres om på grund af tællingen. (069 skal køres om
  på grund af MACD-problemet, se punkt 10.)
- Senere skal Data1 bruges til at finpudse entry med mindre bars (fx 1, 2, 3 eller 5 minutter). Så
  bliver Data1 mindre end Data2, og strategien ville se ufærdige Data2-bars og tælle forkert.
- Mindstekrav: strategien stopper med en tydelig fejl, hvis Data1 og Data2 ikke er lige store.
  Fuld løsning (kun opdatering når en Data2-bar er færdig) bygges først, når Thomas beslutter det.
- Data3 er altid større end Data2. Den påvirker ikke tællingen.

## 6. Strategien (CSV)

- Filnavn og sti står ordret i koden, ens de tre steder: `FileDelete`, overskriftsrækken og linjen
  ved slukning. Python skriver dem ind, når kodefilen laves. Ingen mappe- eller filnavn-Inputs.
  `FileAppend` må ikke bruges.
- Fra/Til/Step og DataFilter-numre er Inputs.
- CSV-mappe: `C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\`
- `RunID` i hver linje = filnavnet uden mappe og endelse.
- Kør som almindelig backtest. IKKE via Optimize.
- Filnavnet på ShowMe'en (`_Kontrol`) skrives aldrig til CSV-mappen.

| Filteret bruger | Overskriftsrække |
|---|---|
| Ingen parametre | `RunID,N1,Starttid,AntalBars` (N1 er altid 1) |
| Kun N1 | `RunID,N1,Starttid,AntalBars` |
| Kun N2 | `RunID,N2,Starttid,AntalBars` |
| Begge | `RunID,N1,N2,Starttid,AntalBars` |

- Komma som skilletegn. Punktum som decimaltegn. Dato/tid: `2020-03-15 10:45`.
- Overskriftsrækken skrives én gang, i `Once`-blokken. Alle linjer har samme antal kolonner.
- Der skrives parameterens VÆRDI, aldrig dens plads i arrayet.

## 7. Efter kørslen

- Filen flyttes af næste trin (EdgeFinder / RawSignal-Analysis) ind i kørslens egen mappe.
- Filen SKAL være flyttet, før samme filter køres igen. `FileDelete` i starten sletter ellers den
  gamle fil uden fejlmelding.
- `RunID` i filen er filterets navn, ikke kørslen. Hvilken kørsel og hvilket instrument det er,
  står kun i mappenavnet. Filen må aldrig flyttes uden mappenavn.
- Før filen flyttes: tjek at den findes og har mere end overskriftsrækken.

## 8. Signal der stadig er tændt ved backtestens slutning

Ignoreres. Skrives ikke. Det er et bevidst valg og må ikke "rettes". Begrundelse: højst ét signal pr.
variant, det har ingen kendt varighed, og analysen mangler kurser efter signalet.

## 9. Kontrol-ShowMe (`_Kontrol`)

Formål: Thomas skal kunne kontrollere signalet med øjnene. Den bruges kun, når han selv sætter den på
et chart, ikke i den automatiske proces.

- Den tegner KUN. Ingen CSV, ingen `FileDelete`, intet filnavn i koden.
- Plot1 = aktiveringen: den bar, hvor filteret skifter fra falsk til sand. Skal kunne skelnes tydeligt.
- Plot2 (valgfri) = bars hvor filteret bliver ved med at være sandt, i en anden farve eller størrelse.
- `Vis_Forrige` (forrige bars status) bruges til at skille aktivering fra fortsættelse. Den opdateres
  efter plottet.
- Ét fast parametersæt vælges med `Vis_N1` og `Vis_N2`, kun for de parametre filteret bruger.
  Har filteret decimaltal, skal inputtet være `double`.
- Plottet regnes på sin egen kodelinje med faste længder, uden løkke. Ellers rammes det af
  hukommelsesproblemet (punkt 10) og kontrollerer ingenting.
- Formlen er ordret den samme som i strategien.
- Chartet skal have de samme datastrømme som strategiens kørsel (Data2, og Data3 hvis formlen bruger
  `DataFilter_B`).
- Max Bars Back skal dække den længste beregning ved de valgte værdier.
- `RawSignal069_MedPlot` og `RawSignal069ShowMe.csv` var en engangsting fra Thomas' side og bruges ikke.

Kontrol med plottet:
- Antal aktiveringer på chartet for én kombination = antal linjer i CSV-filen for samme kombination og
  samme periode. Højst 1 i forskel (punkt 8).
- Flyt `Vis_N1` og `Vis_N2` (fx fra 1,1 til 25,25). Markeringerne skal flytte sig. Står CSV-filen stille
  for de samme kombinationer, er hukommelsesfejlen bekræftet.

## 10. Kendt problem: hukommelsen i seriefunktioner

Indbyggede funktioner som MACD og DMI husker deres forrige værdi, og hukommelsen hører til kodelinjen,
ikke til parameterværdien. Kaldes samme linje i en løkke med mange parametre, deler alle kombinationer
hukommelse, og tallene bliver forkerte uden fejlmelding.

- RawSignal069 (MACD): målt. Alle 625 kombinationer har de samme 4.918 signaler. Værdiløs som den er.
- RawSignal266 (Average): målt. Alle 25 N1-værdier giver forskellige signaler (528 til 1.453 pr. N1).
  Virker altså sandsynligvis.
- RawSignal020 (DMI) og RawSignal004_Test: ikke målt. Antag intet.
- Verify beviser ikke, at en fil virker. Advarsler ved Verify er ikke et sikkert tegn hverken den ene
  eller den anden vej (kun to løkke-filer er målt).
- Hvilken vej for de 304 filtre med parametre er ikke besluttet (punkt 12).

## 11. Tests før noget kaldes færdigt (vis dem til Thomas)

1. Kør på et lille testinterval. Åbn CSV-filen i en teksteditor: én signal pr. linje, ens antal kolonner,
   korrekt datoformat, ingen tomme eller sammenklistrede linjer.
2. **Kontrolkørsel:** kør ÉN kombination alene (Fra og Til ens), og sammenlign med samme kombination i
   løkke-filen. Signalerne skal være præcis ens.
3. Kontrol-ShowMe'en (punkt 9): antal aktiveringer mod linjer i CSV.
4. Kør samme test to gange i træk: filen må ikke få dobbelt så mange linjer.
5. `RunID` er identisk med filnavnet.
6. Python kan indlæse filen uden fejl.
7. Findes ingen CSV overhovedet: tjek Max Bars Back først.
8. Begge filer: `verification` og `note` er gemt i den rigtige tabel.
9. Formelteksten er ordret ens i strategi og `_Kontrol`.

## 12. Spørg Thomas, gæt ikke

1. Skal tabellen til strategifilen forblive `rawsignal`, eller omdøbes den (fx `RawSignal_Strategi`)?
   Til Thomas har svaret: lad den være.
2. Hvilken mappe skal `_Kontrol`-filerne ligge i?
3. Hvilken vej skal de 304 filtre med parametre tage?
   Sikreste rækkefølge: start med filtre uden hukommelsesproblem.
4. De 381 maskinlavede filer bruger værdi/plads-opdelingen i alle filer. Den må kun bruges i de 8 med
   decimaltal. De øvrige skal bygges om efter skabelonen, og én fil pr. type skal afprøves, før resten laves.
5. Skal strategien kunne køre med en mindre Data1 (entry-finpudsning), eller sker det først i et senere
   trin?
