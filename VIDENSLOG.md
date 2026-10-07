# Videnslog — DetStoreProjekt

Central hukommelse for hele projektet. Her samles den vigtige viden vi får
undervejs — tekniske fælder, beslutninger og hvorfor, indsigt om markedet
eller strategierne, og åbne tråde der ikke er lukket endnu.

Skrevet så en ny session (menneske eller Claude, lokal eller cloud) kan
læse sig ind i, hvad der allerede er lært, uden at have været med i
samtalen der førte til det.

## Sådan bruges filen

- **Én post pr. læring**, under den kategori (delprojekt) den hører til.
  Format: `### ÅÅÅÅ-MM-DD — Kort overskrift`, efterfulgt af 2-5 linjer:
  hvad vi lærte/besluttede, og hvorfor det er vigtigt.
- **Detaljerede tekniske noter og fulde beslutningslogs hører hjemme i det
  enkelte delprojekts egen mappe** (som `RawSignal_Creature/NOTER.md`).
  Her i Videnslog skrives kun det korte, tværgående resumé — med en
  henvisning til detalje-filen, hvis der findes én.
- **Nye kategorier oprettes efter behov.** Dukker der viden op om et
  delprojekt, der ikke allerede har en overskrift her, opretter Claude
  selv en ny `##`-overskrift til det — men siger det altid tydeligt til
  Thomas i samme omgang, så det kan rettes hvis kategorien er forkert.
- Vigtigst øverst i hver kategori er ikke et krav — kronologisk
  (ældste øverst) er nok, medmindre andet giver bedre overblik.

---

## DetStoreProjekt (tværgående / generelt)

Viden der gælder hele projektet, ikke kun ét delprojekt — fx overordnede
arkitektur-valg, eller hvordan de forskellige Claude-sessioner arbejder
sammen.

### 2026-09-18 — To adskilte Claude-sessioner deler kun det, der lægges i GitHub
Der findes en lokal Claude Code-session med direkte adgang til Thomas'
server (TradingDB, TradeStation). Denne (cloud-)session har kun adgang til
GitHub-projektet `DetStoreProjekt`. De to sessioner ser intet af hinandens
arbejde, ud over det der bevidst committes og pushes til dette projekt.
**Følge:** al viden der skal deles mellem sessionerne, skal ligge som
filer i git — herunder denne Videnslog.

### 2026-09-23 — Videnslog oprettet
Thomas bad om en "selv-lærende" mekanisme: et sted hvor vigtig viden fra
arbejdet med projektet samles, i stedet for at forsvinde i enkelte
chat-samtaler. Denne fil er svaret — én central log med
under-kategorier pr. delprojekt, som Claude selv udvider efter behov.

### 2026-09-24 — Ved fejl: ret, ryd op og kør forfra — lap aldrig
Da ShowMe-delen af et filter fejlede, blev den verificeret for sig, og
rækkerne blev skrevet i hånden. Thomas afviste det: "hvis der opstår en
fejl, skal processen starte forfra med problemet løst." **Følge:** stop, ret
årsagen, slet alt, hvad kørslen lavede, og kør det hele igen. Programmet er
bygget, så det aldrig skriver et halvt resultat i databasen.

### 2026-09-24 — Vis ændringer i databasen, før de laves, og tilføj intet ekstra
En tabelændring blev kørt med små tilføjelser, der ikke stod i den viste
SQL. Thomas: "du var lige hurtig nok". **Følge:** den SQL, der vises, er
præcis den, der køres. Ændres noget, vises det igen først.

### 2026-09-24 — Test før "færdig" fanger rigtige fejl
Den dybdegående test af det rensede program fandt fire fejl, som de tidligere
kørsler ikke havde vist. Den vigtigste var, at "10 error(s)" blev godkendt.
En anden var, at programmet hang, når en strategi fandtes i forvejen.
**Følge:** hver vej gennem programmet skal afprøves mindst én gang, også
fejl- og genstartsvejene.

### 2026-10-06 — "Rent bord" = alt sat tilbage til udgangspunktet
Thomas' udtryk for, at RawSignal-data er ryddet, så der kan testes igen fra en
kendt start: ingen signaltabeller, tomme log-tabeller, ingen filtre markeret
færdige, tomme FilterFolder-mapper og ingen strategier i TradeStation.
`filter_case`, sikkerhedskopier, analyse-udgangspunktet og prisdata bliver
stående. Se `RawSignal_Creature/BESLUTNINGSLOG_2026-10-06.md`.

### 2026-10-06 — Mål i stedet for at antage, også når en ændring virker lille
Ventetiden 120 → 60 sek, seriefunktions-fejlen og løsningen blev alle afgjort
ved måling (pauser i CSV-filen, sammenligning med en uafhængig beregning fra
prisdata), ikke ved vurdering. Målingen af løsningen afslørede samtidig, at
den gamle løkke kun regnede rigtigt for den første kombination.

### 2026-10-07 — En fejl må ikke kunne smitte videre i en kørsel
Ved en testkørsel af 16 backtests fejlede den første, og workspacet blev stående
åbent, så de 15 næste stoppede med det samme. Brug altid den kæde, der rydder op
efter en fejl (`rs_ts_kaede.py`), og test ét filter alene, før mange køres.

## TradingApp

*(Ingen poster endnu.)*

## RawSignal-Creature

Se `RawSignal_Creature/NOTER.md` for de fulde tekniske EasyLanguage-regler,
og `RawSignal_Creature/BESLUTNINGSLOG_2026-09-18.md` for den fulde
kronologiske gennemgang. Her kun det korte resumé.

### 2026-09-18 — Indbyggede TradeStation-funktioner kan give forkerte tal i en løkke, uden fejlmelding
Funktioner som MACD, RSI, StandardDev m.fl. husker deres forrige værdi
knyttet til kodelinjen, ikke til parameterværdien. Kaldes de i en løkke
med mange forskellige parametre, kan resultatet blive forkert uden nogen
fejlmeddelelse. **Besluttet:** risikoen accepteres for alle 381 filtre
(hurtigere end at håndregne hver funktion selv), men skal dokumenteres i
hver fils hoved. Se `NOTER.md` punkt 3 for detaljer.

### 2026-09-18 — `Print(File(...))` kræver et fast filnavn, `FileAppend` tillader en variabel
`Print(File("..."))` skal have et bogstaveligt filnavn i anførselstegn —
en variabel giver compile-fejlen `File name expected here`. `FileAppend`
kan bruge en variabel, men åbner/lukker filen for hver skrevet linje og er
derfor langsommere. Valget mellem de to hænger sammen med det åbne
navngivnings-spørgsmål, se `NOTER.md`, afsnittet "Åbne punkter".

### 2026-09-24 — RawSignal Creature bygget og testet; filter_case omnummereret
Programmet ligger i `RawSignal_Creature/Program/`. Det bygger strategi og
ShowMe pr. filter, verificerer dem i TDE og markerer filteret færdigt i
`filter_case.rawsignal_faerdig`.
- `filter_case` nr. 1 (`True;`) er slettet, og alle andre er rykket ét nummer
  ned. Det betyder, at gamle numre i ældre dokumenter er én for høje.
- CSV-formatet er én linje pr. signal: `RunID,N1,N2,Starttid,AntalBars,Afsluttet`.
- Data ligger i `rawsignal.rawsignal<nr>`.

Se `RawSignal_Creature/BESLUTNINGSLOG_2026-09-24.md`.

### 2026-09-24 — TDE skal styres med menukommandoer, ikke tastetryk
Simulerede tastetryk virker ikke, når fjernskrivebordet er minimeret.
TDE's menukommandoer kan sendes direkte som `WM_COMMAND`. Numrene står i
`TSResourceDllEng.dll`:
- New Strategy = 10576
- New ShowMe = 10569
- Open = 57601
- Verify = 10602

Knapper skal klikkes med `PostMessage`, fordi `SendMessage` hænger på TDE's
fejlbokse.

### 2026-09-24 — Max Bars Back står på 1000; ukendte funktioner stopper ikke længere
Thomas har sat Max Bars Back til 1000 som standard. Programmet stopper nu kun,
hvis et filter med sikkerhed skal bruge mere end 1000. Højeste udregnede behov
er 609 (MACD). Kan behovet ikke regnes ud, fx for CCI, bygges filen med 1000
som antagelse. Alle 380 filtre kan nu bygges.

### 2026-09-24 — AvgTrueRange i en løkke er målt og ser ud til at virke
Det nye filter 1 (AvgTrueRange, 625 kombinationer) gav forskellige
signalrækker for alle 620 kombinationer, der kan tænde. Sammen med Average
(gamle 266) er det to funktioner, der virker. MACD (gamle 069) er stadig den
eneste målte, der er ramt.

### 2026-10-05 — filter_case bygget op på ny ud fra EdgeFinder-filerne; alle numre nye
`filter_case` passede ikke med de originale EdgeFinder-filer: numrene var forskudt, 68 dubletter,
og nogle formler afveg (fx `<` i stedet for `>`, manglende parentes, `Open[1]` i stedet for `Close[1]`).
Tabellen er bygget op på ny: 312 filtre, sorteret efter EdgeFinder-filnummer, én parameter hedder
altid N1, Long/Short forskellige giver to filtre. Alt gammelt testdata er slettet. **Følge:** gamle
filternumre i ældre dokumenter kan ikke regnes om. Sammenlign altid på formlen, ikke på nummeret.
Se `RawSignal_Creature/BESLUTNINGSLOG_2026-10-05.md`.

### 2026-10-05 — Seriefunktions-fejlen løst: én kodelinje pr. kombination
Filtrene virker i en almindelig backtest, fordi hver kombination dér er sin egen
kørsel. I RawSignal-løkken deler alle kombinationer én hukommelse pr. kodelinje.
Målt ramt: XAverage, RSI, MACD, DMI (ADX uafklaret). Løsning: formlen skrives ud
på én linje pr. kombination med faste tal (`formel.UDFOLD_FUNKTIONER`). Bevist
100 % mod en uafhængig beregning fra prisdata; den gamle løkke ramte 0–16 %.
Se `RawSignal_Creature/BESLUTNINGSLOG_2026-10-06.md`.

### 2026-10-06 — CSV-filen skrives løbende: 60 sek stilhed er nok
Den længste pause mellem to skrivninger midt i en beregning var 8,6 sek, også i
en 77 minutters DMI-kørsel på 5-5-10. `STILLE_SEK` er sat fra 120 til 60 sek
og sparer ca. 1 min pr. cyklus.

### 2026-10-06 — filter_case: 445 filtre efter Alpha og oprydning
139 formel-typer fra Thomas' ældste filtre (`C:\Alpha_FIlter.txt`) er tilføjet
som 307–445. De 6 CoefTimeFrame-filtre er slettet (funktionen findes ikke), og
alle numre fra 73 er rykket 6 ned. Formler, der aldrig kan være sande (fx
`Close > Highest(Close, N)` uden `[1]`), fandtes også i originalerne og er rettet.

### 2026-10-07 — Verify-advarslen om seriefunktioner er ikke et tegn på fejl
24 filtre fra alle grupper med advarslen (D- og Session-funktioner, Highest,
CountIf, CCI, Pivot, Bollinger, seriefunktion i seriefunktion m.fl.) er
backtestet og målt: ingen er ramt. Omskrivningen af MACD/DMI/ADX/XAverage
virker. Mål ved at sammenligne signalrækken pr. kombination – ens signaler ved
høje parametre kan være naturligt (fx ingen dage med så stort udsving).
Se `RawSignal_Creature/BESLUTNINGSLOG_2026-10-07.md`.

### 2026-10-07 — TDE bliver langsommere for hvert filter og går til sidst ned
16 sek pr. filter ved filter 1, 42 sek ved filter 400, hvor TDE gik ned.
Genstart giver 16 sek igen. Programmet genstarter nu TDE for hver 100 filtre.
EasyLanguage: `of data(...)` må ikke stå efter MinList/MaxList/AbsValue (sæt det
ved hver pris), og TSI kræver 3 tal: `TSI(Close, længde1, længde2)`.

### 2026-10-07 — filter_case: 447 filtre, nye TSI som 373–374
To TSI-filtre med grænse 1.4 er lagt ind ved siden af de andre TSI; alle numre
fra 373 er rykket 2 op. Alpha-filtrene er nu 307–447.

## EdgeFinder

*(Ingen poster endnu.)*

## EdgeCruncher

*(Ingen poster endnu.)*
