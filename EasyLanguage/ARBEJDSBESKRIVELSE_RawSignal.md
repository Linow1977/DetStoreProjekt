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
   - Byg `KoerselsID` = `RawSignalNavn + "__" + BarInterval-tal for data1,
     data2, data3, adskilt med "_" + "__" + kørselsmåned (yyyy_MM)`.
   - Byg `FilNavn` = `Mappe + KoerselsID + ".csv"`.
   - `FileDelete(FilNavn)`.
   - `FileAppend(FilNavn, "RunID,N1,N2,Starttid,AntalBars" + NewLine)` — kun
     de kolonner der er relevante for filteret (spring `N2` over, hvis
     formlen ikke bruger den; spring både `N1` og `N2` over, hvis ingen af
     dem bruges).

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

6. **Skriv linjen med `FileAppend`** ved slukning, samme format som i
   eksemplerne, kun med de kolonner der er relevante for netop dette filter.

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
  `filter_case_id`) og lægges i `EasyLanguage/RawSignal/` i dette
  git-projekt, så de kan følges i versionsstyring.
- CSV-output ved kørsel går til `C:\RawSignal_2026_TS\`, som allerede findes.

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

Det ønskede forløb, fil for fil:
1. Programmet lægger én `.el`-fil ind i TradeStation (som Analysis
   Technique/Strategy).
2. Det trykker Verify (eller tilsvarende).
3. Det læser resultatet — kompileret uden fejl, eller fejlbesked.
4. Ved succes: gå til næste fil. Ved fejl: notér filnavn og fejltekst, gå
   videre — stop ikke hele kørslen på grund af én fejlende fil, medmindre
   andet besluttes (se åbent spørgsmål nedenfor).
5. Til sidst: en samlet rapport — hvor mange verificerede, hvor mange
   fejlede, og med hvilken fejl.

### Åbne spørgsmål — SKAL afklares, før dette bygges

Disse er ikke besvaret endnu. Gæt ikke på svarene — spørg Thomas, eller
undersøg og rapportér tilbage før noget bygges:

1. **Findes der en kommandolinje- eller API-adgang til TradeStation**
   (fx til at åbne/kompilere en EasyLanguage-fil uden den grafiske flade)?
   Det ville gøre automationen markant mere robust end at simulere
   museklik og tastatur, som knækker ved uventede dialogbokse eller hvis et
   vindue flytter sig. Undersøg TradeStations dokumentation og installerede
   værktøjer for dette, før der bygges på ren UI-automatisering.

2. **Adfærd ved fejl:** skal programmet stoppe helt ved første fejlende
   fil, eller notere fejlen og fortsætte til næste? (Anbefalingen ovenfor er
   "fortsæt og saml op", men det er ikke besluttet endnu.)

3. **Hvordan når filerne frem til Thomas' maskine?** Ligger den lokale
   Claude Code-session i det samme git-projekt (`DetStoreProjekt`), hentet
   ned med `git pull`, eller et andet sted på serveren uden forbindelse til
   GitHub? Det afgør, om automationsprogrammet selv skal hente filerne fra
   GitHub, eller om de allerede ligger lokalt.

## Ikke en del af denne opgave

- Ingen ændringer af `filtere`-formlerne.
- Ingen kørsel af backtests — det gør Thomas selv i TradeStation.
- Ingen ændring af `TradingDB`.
- Ingen håndregnet erstatning for MACD/RSI/StandardDev/DMI/ChaikinMoneyFlow
  m.fl. — risikoen er accepteret og dokumenteret, ikke løst, jf. `NOTER.md`.
