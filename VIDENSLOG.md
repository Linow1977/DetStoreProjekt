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

### 2026-09-29 — Fokus flyttet fra filtre til analyse; konsulentopgave v2
Thomas: det vigtige nu er analyse af data, pipelinen, RSA, Edge-Finder/CC
og Pharos, ikke de enkelte filtre (MACD-sporet er droppet). Konsulent 2 er
skiftet fra EasyLanguage-ekspert til kvantitativ pipeline-/analyseudvikler.
EasyLanguage-arbejdet er et åbent punkt, ikke en fast rolle. Ny kæde:
TradingDB → RawSignal Maker → RSA → Code Creater → Edge-Finder/Cruncher →
Incubator → Pharos. Se `Konsulentopgaver/Opgave_til_konsulentgruppen_v2_2026-09-29.docx`.

### 2026-09-29 — Konsulentrapport v2 og Pharos-udkast færdige
Tre konsulent-agenter (statistiker, pipeline-udvikler, data-arkitekt) og en
overordnet agent skrev rapporten. Den ligger i
`Konsulentopgaver/Rapport_konsulentgruppen_2026-09-29.docx`, Pharos-udkastet
(inspireret af Andrea Ungers Titan) i `Pharos_udkast_2026-09-29.docx` og
afprøvningskoden i `Konsulentopgaver/Laboratorium/`. Hovedfund: tre huller
skal lukkes før den fulde kørsel (se RawSignal-Creature og punktet om
superbrugeren nedenfor). Thomas' beslutninger er samlet i rapportens del 4.6
og bilag A. Intet er besluttet endnu.

### 2026-09-29 — Programmerne logger på TradingDB som superbrugeren `postgres`
`Program/faelles.py` forbinder som `postgres`. En superbruger går uden om alle
rettigheder, så låse på 2025-2026-data og engangs-porten til OOS kan ikke
virke, før programmerne får egne, begrænsede roller. Skal rettes, før låsene
bygges.

### 2026-09-29 — Arbejdsmåde: uafhængig kontrol og hele VIDENSLOG
En uafhængig agent, der ikke havde skrevet noget, fandt 43 fejl i en rapport,
som tre konsulenter allerede havde angrebet hinandens dele af. Blandt dem var
to regler, der brød Thomas' egne beslutninger. **Følge:** store leverancer
skal altid gennem en frisk kontrol. Samtidig blev VIDENSLOG kun søgt i med
nøgleord, ikke læst helt, og posten om, at Average og AvgTrueRange virker i
løkken, blev overset. **Følge:** læs hele VIDENSLOG før en opgave, ikke kun
søg i den.

### 2026-09-30 — Arbejdsmåde: "let læst" betyder voksent almindeligt dansk
De første letlæste udgaver af rapporterne blev afvist som "for barnlige"
(sammenligninger med plat og krone, skabe og fodboldtrænere). Thomas vil have
**hele indholdet i samme opbygning**, voksent almindeligt dansk, fagord
forklaret, og formler, SQL og kode **ordret uændret**. **Følge:** spørg ved
"let læst" om tone og omfang, før der skrives. Kodeblokke kopieres maskinelt
fra originalen (linjenumre) i stedet for at blive skrevet af, og et script
tjekker bagefter, at alle blokke findes ordret, og at antallet af afsnit er
det samme. Resultat: `Rapport_konsulentgruppen_almdansk_2026-09-29.docx` og
`Pharos_udkast_almdansk_2026-09-29.docx` i `Konsulentopgaver/`.

## RSA (RawSignal-Analyser)

Andet led i kæden: analyserer signal-backtests for stabilitet. Metoden står i
konsulentrapportens del 1 (statistik) og del 2 (byggeplan).

### 2026-09-29 — Tæl i handelsdage, og mål tilfældighed med lokkeduer
Signaler klumper sig, så t-tal regnet pr. signal blev 1,4-4,6 gange for store
i forsøg; de skal regnes pr. handelsdag. Panelets "tilfældige tidspunkter"
lod ca. ti gange for mange falske igennem. Lokkeduer, hvor hele
signalserien flyttes 4-26 kalenderuger, gav et retvisende billede.
`AntalBars` kendes først, når signalet slukker, og må aldrig bruges til at
vælge signaler. Kun forsøg på opdigtede data, se `Konsulentopgaver/Laboratorium/K1`.

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

### 2026-09-29 — En ny barstørrelse sletter den forrige
`Program/indlaes_csv.py` kører `delete` på hele `rawsignal.rawsignal<nr>`
før indlæsning, og RunID indeholder ikke barstørrelsen. Kører samme filter
på 12 barstørrelser, overlever kun den sidste. Skal rettes (job-nummer og
barstørrelse på hver række) før den fulde kørsel.

### 2026-09-29 — Regnefejlen får et gitter til at ligne et perfekt plateau
Når en seriefunktion giver ens signaler i alle 625 celler, når plateau-trappen
automatisk PL7. RSA skal derfor have en kontrol for "identiske celler", der
markerer gitteret som ugyldigt, og den skal køres på alle filtre. 184 af 380
filtre indeholder ingen af de kendte seriefunktioner; op til 196 kan være
ramt. Det tal er et loft: Average og AvgTrueRange er målt og virker (posten
ovenfor), så det reelle antal ramte er sandsynligvis lavere. Rapporten fra
29. september bruger loftet.

## EdgeFinder

*(Ingen poster endnu.)*

## EdgeCruncher

*(Ingen poster endnu.)*
