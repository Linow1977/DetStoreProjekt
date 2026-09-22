# Arbejdsbeskrivelse: Generér 381 RawSignal .EL-filer fra TradingDB

Denne beskrivelse er skrevet til at blive givet som prompt til den Claude
Code-session, der har direkte adgang til `TradingDB` (Postgres) og til
TradeStations filsystem. Læs `NOTER.md` i samme mappe først — den forklarer
baggrunden og de EasyLanguage-fælder, der ligger til grund for reglerne her.

## Opgaven

For hver af de 381 rækker i tabellen `public.filter_case` skal der laves én
`.el`-fil: et "råt signal" (RawSignal), der registrerer hvornår filteret
tænder, og hvor længe det er tændt — intet andet. Ingen handelslogik, ingen
analyse. Filerne skal kunne åbnes og verificeres i TradeStation, og
efterfølgende køres som almindelige backtests, der eksporterer data til CSV.

## Kilde-data pr. række

| Kolonne | Brug |
|---|---|
| `filter_case_id` | RawSignal-nummer. Brug som `RawSignal###` med tre cifre og foranstillede nuller, fx `RawSignal007`, `RawSignal069`, `RawSignal381`. |
| `filter1_n1_start/end/step` | Fra/Til/Step for N1, hvis formlen bruger `Filter1_N1`. |
| `filter1_n2_start/end/step` | Fra/Til/Step for N2, hvis formlen bruger `Filter1_N2`. |
| `filtere` | Selve filterformlen, som EasyLanguage-udtryk, der evaluerer til sandt/falsk. |
| `gammel_case` | Ignoreres. Ikke relevant for generering eller navngivning. |

**Læs formlens tekst for at afgøre, hvilke parametre der reelt bruges.**
Kolonnerne kan være udfyldt for en parameter, der alligevel ikke optræder i
formlen. Byg kun de Input-felter og løkker, der svarer til de parametre,
formlen faktisk indeholder:

- Ingen `Filter1_N1` og ingen `Filter1_N2` i formlen → ingen løkke, én variant. Følg mønstret i `RawSignalTest_2.el`.
- Kun `Filter1_N1` (eller kun `Filter1_N2`) → én løkke, ét sæt Fra/Til/Step-inputs, ét array-index.
- Begge → to indlejrede løkker, to sæt Fra/Til/Step-inputs, to array-index. Følg mønstret i `RawSignalTest_1.el`.

## Skabelon: struktur der SKAL genbruges

Byg hver fil efter samme opskrift som `RawSignalTest_1.el` og
`RawSignalTest_2.el` i denne mappe. Ikke som inspiration — som skabelon.
Afvigelser herfra har tidligere kostet flere timers fejlsøgning:

1. **Input-blok:** `DataFilter_A` (int, standard 2), `Mappe` (string, standard
   `"C:\RawSignal_2026_TS\"`), `RawSignalNavn` (string, sat til det
   pågældende `RawSignal###`), og Fra/Til/Step-inputs for hver parameter
   formlen bruger.

2. **`Once`-blok:**
   - **Navngivning ændret 2026-09-22:** ingen dynamisk opbygning af
     filnavnet ud fra `BarInterval`/`ComputerDateTime` længere. Der laves
     kun **én universal fil** pr. filter. Navngivning og flytning af den
     færdige CSV-fil til den rigtige mappe håndteres eksternt af det
     separate **EdgeFinder-programmet** — ikke i denne kode.
   - Sæt `FilNavn` til det faste, forventede outputnavn (afklares endeligt
     når skabelonen bygges om — se `NOTER.md`, afsnittet "Navngivning —
     afklaret 2026-09-22").
   - `FileDelete(FilNavn)`.
   - Skriv overskriftsrækken, `"RunID,N1,N2,Starttid,AntalBars" + NewLine`
     — kun de kolonner der er relevante for filteret (spring `N2` over,
     hvis formlen ikke bruger den; spring både `N1` og `N2` over, hvis
     ingen af dem bruges).

3. **Løkke(r) over parametrene** med `While`, styret af Fra/Til/Step-inputs
   (ikke faste `For`-løkker) — se `RawSignalTest_1.el`.

4. **Selve filteret:** sæt `filtere`-kolonnens tekst ind uændret, med
   `Filter1_N1`/`Filter1_N2` erstattet af løkkevariablerne. Formlen skal
   IKKE omskrives eller "rettes" — heller ikke selvom den bruger en
   indbygget seriefunktion i en løkke (se advarslen i `NOTER.md`, punkt 3).
   Det er et bevidst valg, og advarslen skal med i filens hoved i stedet for
   at blive løst.

5. **Tænder/fortsætter/slukker-logik**, identisk med de to eksempelfiler:
   array pr. kombination af parametre, `Filter1[...]`, `Filter1_Forrige[...]`,
   `SignalBars[...]`, `StartTekst[...]`.

6. **Skriv linjen ved slukning** (skrivemetode — `Print(File(...))` eller
   `FileAppend` — afklares når skabelonen bygges om, se `NOTER.md`),
   samme format som i eksemplerne, kun med de kolonner der er relevante
   for netop dette filter.

7. **Filens hoved (kommentarblok)** skal indeholde:
   - Filterets `filter_case_id` og den oprindelige formel fra `filtere`.
   - Advarslen om seriefunktioner i løkker, hvis formlen bruger en (kopiér
     teksten fra `RawSignalTest_1.el`, tilpasset).
   - Hvilke parametre filteret bruger.
   - Påmindelse: kør som almindelig backtest, ikke Optimize; CSV-filen skal
     være lukket i Excel; Max Bars Back sættes til Auto Detect eller en
     tilstrækkelig værdi.

## Array-størrelse

Sæt array-dimensionerne til mindst den største `_end`-værdi, der forekommer
i hele `filter_case`-tabellen for den pågældende parameter — ikke kun den
værdi, der gælder for netop denne fil. Så kan samme Fra/Til/Step-inputs
senere sættes højere uden at ramme en for lille array-grænse. Skriv den
valgte størrelse som kommentar ved array-deklarationen.

## Filnavne og placering

- De færdige `.el`-filer navngives `RawSignal###.el` (samme nummerering som
  `filter_case_id`) og lægges i `RawSignal_Creature/RawSignal/` i dette
  git-projekt, så de kan følges i versionsstyring. Under udvikling af selve
  RawSignal-Creature-programmet hedder testfiler i stedet
  `RawSignal_(Nummer)_Test.el` — se `NOTER.md`.
- **CSV-output ved kørsel:** navngivning og flytning til den rigtige mappe
  håndteres nu af det separate EdgeFinder-programmet, ikke af koden i
  `.el`-filen selv (afklaret 2026-09-22, se `NOTER.md`). `C:\RawSignal_2026_TS\`
  var det oprindelige, forladte mappe-forslag — bekræft med Thomas, om det
  stadig er relevant, når skabelonen bygges om.

## Rækkefølge og validering

1. Byg og verificér (compile) filerne i små bundter — fx 10-20 ad gangen —
   frem for alle 381 på én gang. Kompileringsfejl skal rettes, før næste
   bundt bygges, så samme fejl ikke gentages 381 gange.
2. Byg IKKE noget der forsøger at "forbedre" en formel fra databasen. Formlen
   er facit. Opgaven er at pakke den ind i den fungerende skabelon, ikke at
   validere dens finansielle logik.
3. Når alle filer er bygget og kompilerer, meld tilbage: hvor mange filer,
   hvor mange advarsler om seriefunktioner, og om nogen formler ikke passede
   ind i 0/1/2-parameter-mønstret ovenfor (fx flere end to parametre) —
   de skal behandles særskilt, ikke gættes på.

## Automationsprogram: læg filen ind i TradeStation og verificér

Ingen af Claude Code-sessionerne kan styre TradeStations grafiske flade —
hverken denne session (cloud, ingen adgang til din maskine) eller den
lokale. Skal de 381 filer verificeres uden at Thomas selv skal åbne og
klikke Verify 381 gange, skal der bygges et selvstændigt program til det,
som kører på Thomas' maskine ved siden af TradeStation.

**Fuld opgavebeskrivelse: se `OPGAVEBESKRIVELSE_Automation.md`** i denne
mappe. Kort opsummeret er det nu besluttet:

- Programmet er en del af RawSignal-Creature og styres fra en fane i
  TradingApp.bat (Kør / maskine-valg / Fra filter nummer / kontrolfunktion
  til/fra / antal mellem kontrol / Pause / Live Log).
- **Adfærd ved fejl (afklaret):** stopper aldrig hele kørslen — noterer
  fejlen og fortsætter til næste fil.
- Resultatet skrives til en ny tabel i TradingDB, `RawSignal_Case` (navn,
  byggedato, filsti, verificeringsresultat, note), ikke kun til en logfil.
- Bygges kun til **TradeStation** i første omgang. Multicharts er en
  selvstændig, separat blok, der tilføjes senere — de to platforme deler
  ikke automations-logik.

### Adgangsvej og filhentning — begge afklaret 2026-09-22

- **Ingen CLI/API til TradeStation Development Environment.** TDE er en
  lokal editor uden internetforbindelse. TradeStations Web API findes,
  men er kun til handel (kurser, konto, ordrer) og har ingen bro til TDE.
  Automationen bygges derfor som ren UI-automatisering — se
  `OPGAVEBESKRIVELSE_Automation.md` for detaljer.
- **Filhentning:** automationsprogrammet henter selv `.el`-filerne (fra
  git) og lægger dem ind i TDE.

## Ikke en del af denne opgave

- Ingen ændringer af `filtere`-formlerne.
- Ingen kørsel af backtests — det gør Thomas selv i TradeStation.
- Ingen ændring af `filter_case`-tabellen i `TradingDB`. (Den nye tabel
  `RawSignal_Case`, som automationsprogrammet læser/skriver, hører til
  den opgave — se `OPGAVEBESKRIVELSE_Automation.md` — ikke til denne
  fil-genererings-opgave.)
- Ingen håndregnet erstatning for MACD/RSI/StandardDev/DMI/ChaikinMoneyFlow
  m.fl. — risikoen er accepteret og dokumenteret, ikke løst, jf. `NOTER.md`.
