# Noter — RawSignal og EasyLanguage

Kort hukommelse for arbejdet med signal-eksport fra TradeStation.
Skrevet så den kan læses uden forhåndskendskab til koden.

## Hvad en RawSignal er

Et **råt signal**: basal information om hvad der sker og hvornår det opstår.
Ikke en handelsstrategi, ikke en analyse — bare registreringen af at et filter
tændte, hvornår det tændte, og hvor længe det var tændt.

Analysen (event-studie-metode) sker et andet sted, i Python.
TradeStation skal kun levere de rå events.

## Kilden: TradingDB

De 381 filtre, der skal laves, ligger i en Postgres-database (`TradingDB`),
tabellen `filter_case`. Den er kun tilgængelig fra en anden, lokal Claude
Code-session med direkte adgang til serveren — ikke fra denne session.

Relevante kolonner:

| Kolonne | Betydning |
|---|---|
| `filter_case_id` | Unikt løbenummer, 1-381. Bruges som RawSignal-nummer. |
| `filter1_n1_start/end/step` | Fra/Til/Step for N1. Kan være tom (parameter ikke brugt). |
| `filter1_n2_start/end/step` | Fra/Til/Step for N2. Kan være tom. |
| `gammel_case` | Internt gruppenummer fra et ældre system. Ikke relevant for noget her. |
| `filtere` | Selve filterformlen, som EasyLanguage-tekst, fx `MACD(C, Filter1_N1*2, ...) > 0;` |

**Vigtigt:** man kan ikke gå ud fra, hvilke parametre en formel bruger, ud fra
om kolonnerne er udfyldt. Nogle formler bruger kun `Filter1_N2` og slet ikke
`Filter1_N1`, selvom begge sæt kolonner har værdier. Formlens tekst skal
læses for at se, hvilke af `Filter1_N1`/`Filter1_N2` der rent faktisk
forekommer.

## Navngivning (gældende metode)

Filnavnet og RunID bygges af **strategien selv, ved kørsel** — ikke skrevet
ind på forhånd. Det løser to problemer på én gang: samme filter kan køres på
flere workspaces (forskellige tidsrammer) uden at overskrive hinanden, og
køredatoen kommer automatisk med.

```
Mappe:    C:\RawSignal_2026_TS\
Filnavn:  RawSignal(Nummer)__tf1_tf2_tf3__år_måned.csv
RunID:    Samme streng som filnavnet, uden mappe og uden .csv
```

Eksempel: kører `RawSignal069` på et chart med data1=5 min, data2=10 min,
data3=60 min, i september 2026:

```
C:\RawSignal_2026_TS\RawSignal069__5_10_60__2026_09.csv
```

De tre tidsrammer aflæses med `BarInterval of data(1/2/3)`. Alle tre skal med
— to forskellige workspaces kan dele samme filter-tidsramme, og så er det de
to andre tal, der adskiller dem.

Datoen kommer fra `ComputerDateTime` — computerens ur ved kørsel, ikke
hvornår koden blev skrevet.

Se `RawSignalTest_2.el` for den fungerende kode, det bygger på.

## EasyLanguage-regler vi har lært (dyrt betalte)

Disse kostede flere mislykkede forsøg at finde ud af. Læs dem, før der skrives
en ny RawSignal-fil.

1. **`Print(File("..."))` må kun have et fast filnavn i anførselstegn.**
   En variabel giver compile-fejlen `File name expected here` og dermed
   `Strategy not verified`.

   **Løsning:** brug `FileAppend(FilNavn, tekst)` i stedet. Den kan tage en
   variabel som filnavn. Prisen: den åbner og lukker filen for hver linje,
   der skrives, og er derfor langsommere end `Print(File(...))`. Det er
   accepteret, fordi det er den eneste måde at bygge filnavnet dynamisk på.

2. **Optimering kan ikke bruges, når der skrives til fil.**
   TradeStation kører optimeringspas parallelt. Kun det første pas får lov at
   åbne filen; resten fejler med `OpenFileException` / `WriteFileException`.
   Løsningen: lad strategien selv løbe alle varianter igennem på hver bar
   ved hjælp af arrays, og kør den som én almindelig backtest.

3. **Indbyggede seriefunktioner (MACD, RSI, StandardDev, Average, DMIplus,
   DMIminus, ChaikinMoneyFlow, AvgTrueRange, XAverage, m.fl.) kan give
   forkerte tal, hvis de kaldes i en løkke med skiftende parameterværdier —
   UDEN at der kommer nogen fejlmeddelelse.**

   Årsagen: de bygger internt på funktioner som `XAverage`, der husker deres
   egen forrige værdi for at kunne regne den næste. Den hukommelse er knyttet
   til kodelinjen, ikke til parameterværdien. Kaldes samme linje 625 gange på
   én bar med 625 forskellige længder, deler de hukommelsen, og resultatet
   kan blive forkert.

   **Beslutning (gælder alle 381 filtre):** vi accepterer denne risiko for at
   komme videre, i stedet for at håndregne hver funktion selv. Det betyder,
   at tal fra filtre med parametre bør kontrolleres, før de bruges til
   noget vigtigt. Advarslen skal stå skrevet i hver enkelt .EL-fils hoved,
   præcis som i `RawSignalTest_1.el`, så den der åbner filen senere kender
   forbeholdet uden at skulle kende denne samtale.

   Den sikre, håndregnede metode (separat hukommelse pr. kombination) findes
   og virker — den blev brugt og siden forladt for MACD-eksemplet. Den er
   markant mere arbejdskrævende, fordi den skal bygges særskilt for hver
   underliggende funktionstype (MACD, RSI, StandardDev, DMI, osv.). Overvej
   den, hvis et bestemt filter viser sig lovende og skal bekræftes.

4. **N1 og N2 er Fra/Til/Step, ikke faste 1-25-løkker.**
   Styres med `While`-løkker og tre Input pr. parameter
   (`N1_Fra`/`N1_Til`/`N1_Step`), så de matcher TradingDB's kolonner direkte.
   Se `RawSignalTest_1.el`.

   Arrays i koden har en fast størrelse (fx `[25,25]`), sat ved kompilering.
   Går `_Til` over den grænse, skal array-størrelsen hæves i koden — den
   følger ikke automatisk med.

5. **Max Bars Back skal sættes højt nok** til den længste beregning i koden.
   Med mange forskellige filtre og parameterområder er det upraktisk at
   regne det ud for hver af de 381 i hånden. Brug **"Auto Detect"** i
   `Format Strategies → Properties for All`, hvis TradeStation tilbyder det —
   det er endnu ikke bekræftet, at det virker pålideligt her, så et filter
   der ikke vil verificere, bør tjekkes manuelt for netop dette.

6. **CSV-filen skal være lukket i Excel**, mens TradeStation kører.
   En åben fil i Excel blokerer skrivningen og giver samme fil-fejl som ovenfor.

7. **Overskriftsrække i toppen af filen**, så Python kender kolonnenavnene.
   Skrives i et `Once`-blok sammen med `FileDelete`, så gentagne beregninger
   af chartet ikke dubler linjerne.

## Sådan køres en RawSignal-backtest

1. Luk CSV-filen i Excel.
2. Højreklik på chartet → `Format Strategies…` → marker strategien → `Format…`
3. Fanen `Inputs`: sæt faste tal i felterne (Fra/Til/Step for N1 og N2).
4. Fanen `Properties for All`: `Maximum number of bars study will reference`
   → `Auto Detect`, eller `User specified` med en tilstrækkelig høj værdi.
5. `OK` → `OK`. Backtesten kører af sig selv — der er ingen start-knap.
6. Kør igen: højreklik på chartet → `Reload Chart`.

**Rør ikke `Optimize…`** — det er den, der giver fil-fejlene.

## Kendte begrænsninger

- Er et filter stadig **tændt** på den allersidste bar i dataene, bliver den
  sidste periode ikke skrevet ud. Linjen skrives først, når filteret slukker.
  Det er højst én manglende linje pr. variant.
- `FileAppend` er ikke endnu tidsmålt på en fil med mange hundredtusind
  linjer. Testen kører i `RawSignalTest_1.el` — resultatet er ikke kendt endnu.

## Navngivning — afklaret 2026-09-22

**Beslutning 2026-09-19: `FileAppend` droppes.** Den var for langsom på
RawSignalTest_1's 625 kombinationer (åbner/lukker filen for hver skrevet
linje). Det genåbnede navngivnings-problemet, som `FileAppend` oprindeligt
løste: hvordan holdes de fire workspaces (5,10,60 / 10,20,60 / 5,30,120 /
5,10,120) adskilt, når filnavnet er en fast tekststreng i koden.

**Løsning, valgt af Thomas:** ingen af de tre oprindelige forslag bruges.
Der laves kun **én universal `.el`-fil pr. filter** (ikke fire varianter,
og ikke et manuelt indtastet filnavn). Selve navngivningen og flytningen
af den færdige CSV-fil til den rigtige mappe håndteres **eksternt, af det
separate EdgeFinder-programmet** — ikke inde i RawSignal-filens egen kode.

**Ikke endeligt afklaret:** hvilken skrivemetode `.el`-filen selv bruger
internt (`Print(File("..."))` med fast, bogstaveligt filnavn, eller
`FileAppend` med et simplere, ikke-workspace-specifikt navn) — det er ikke
længere kritisk, da EdgeFinder-programmet uanset hvad står for det endelige
navn og placering. Afklares når skabelonen i `RawSignalTest_1.el` /
`RawSignalTest_2.el` bygges om.

**Følgevirkning, ikke rettet endnu:** `RawSignalTest_1.el` og
`RawSignalTest_2.el` bruger stadig `FileAppend` med dynamisk,
workspace-baseret filnavn (den forladte metode) — de skal bygges om til
den nye, simplere model, når automationsprogrammet skal bruge dem.

- **Hastighedstest af `FileAppend`**: ikke længere relevant, da metoden droppes.
- **Filnavne under udvikling af RawSignal-Creature:** mens selve
  RawSignal-Creature-programmet (fil-generering + automation) udvikles,
  hedder testfilerne `RawSignal_(Nummer)_Test.el` — ikke det endelige
  `RawSignal###.el`.

## TradingDB — ny tabel til automations-sporing

Ud over `Filter_Case` (kilden til selve filtrene, se ovenfor) er der
besluttet en ny tabel, **`RawSignal_Case`**, som automationsprogrammet
læser og skriver til (se `OPGAVEBESKRIVELSE_Automation.md`):

| Felt | Indhold |
|---|---|
| `RawSignal-Name` | Filens navn, fx `RawSignal069` |
| `Dev. date` | Byggedato for `.el`-filen |
| `File Path` | Hvor filen ligger |
| `Verification` | Resultat af Verify i TradeStation |
| `Note` | Fx fejltekst ved en mislykket verificering |

Automationsprogrammet bruger denne tabel til at se, hvilke filer der
allerede er kørt, og hvilke der er nye og mangler at blive verificeret.

## TradeStation Development Environment — bekræftet arbejdsgang

Manuelt testet, én fil ad gangen, i `TSDev.exe`:

1. Åbn `TSDev.exe`, hvis det ikke allerede er åbent.
2. Ny strategi: `Ctrl+Alt+S`.
3. Navngiv strategien `RawSignal...` → Enter.
4. Indsæt signalteksten.
5. Verify: `F3`.
6. Luk: `Alt+C`.

Verify-resultatet vises i Output-panelet (`0 error(s), 0 warning(s)` ved
succes, ellers fejltekst med Technique/Line/Type) og i statuslinjen
("VERIFIED" ved godkendt fil). Dette er det, automationsprogrammet skal
aflæse — se `OPGAVEBESKRIVELSE_Automation.md`.

## Åbne punkter

- **Arbejdsbeskrivelse til den lokale Claude Code-session**, der skal
  generere alle 381 .EL-filer ud fra TradingDB
  (`ARBEJDSBESKRIVELSE_RawSignal.md`), skal opdateres til den nye,
  simplere navngivningsmodel (ingen dynamisk workspace-navngivning i
  koden selv).
- Automationsprogrammets krav er nu beskrevet i
  `OPGAVEBESKRIVELSE_Automation.md`, men to punkter er stadig ikke
  undersøgt: CLI/API-adgang til TradeStation, og hvordan filerne når frem
  til den maskine, der kører automationen.
