# Beslutningslog — RawSignal-projektet, 18. september 2026

Fuld gennemgang af dagens arbejde, skrevet så en ny session (menneske eller
Claude) kan samle op uden at have været med. Kronologisk, med begrundelser —
ikke kun konklusioner.

## Hvor det startede

En eksisterende EasyLanguage-strategi, `EdgeFinder_F5_SIGNAL`, skulle
registrere hvornår et volatilitetsfilter tændte og slukkede, og skrive det
til en CSV-fil. TradeStations Events Log viste skiftevis
`OpenFileException` og `WriteFileException` på filen `signals_test.csv`.

**Root cause, fundet i flere trin:**
- Først mistanke: flere samtidige TradeStation-instanser (optimering)
  skriver til samme fil og låser hinanden ude.
- Også: filen var åben i Excel på skærmbilledet — det alene kan blokere
  skrivning.
- Et forsøg på at give hver kørsel sit eget filnavn via en variabel i
  `Print(File(FilNavn))` fejlede med compile-fejlen `File name expected
  here`. **Lærdom:** `Print(File(...))` kræver et bogstaveligt filnavn i
  anførselstegn — aldrig en variabel.
- Den egentlige årsag til de oprindelige fejl: TradeStations `Optimize`
  kører mange parameterkombinationer parallelt. De deler alle den samme
  faste fil, og kun det første pas kan åbne den.

**Løsning:** i stedet for at bruge `Optimize` til at afprøve mange
parameterkombinationer, lader strategien selv løbe alle kombinationer
igennem på hver bar, ved hjælp af arrays (én "hukommelse" pr. kombination),
og køres som én almindelig backtest. `EdgeFinder_F5_SIGNAL` blev bygget om
til dette og virker.

## RawSignal-konceptet formuleret

Undervejs definerede Thomas et generelt begreb: et **RawSignal** er en
rå, uden analyse: registrering af hvornår et filter tænder, og hvor
mange bars det er tændt. Ikke en strategi, ikke en analyse — analysen
(event-studie-metode) sker bagefter i Python. TradeStations eneste opgave
er at levere de rå events.

**Navngivningskonvention** blev fastlagt gennem flere runder:
- Format: `RawSignal(Nummer)__tidsramme1_tidsramme2_tidsramme3__år_måned`
- Alle tre tidsrammer (data1, data2, data3) skal med, fordi samme filter kan
  køres på flere TradeStation-workspaces med forskellige
  tidsramme-kombinationer, og to workspaces kan dele én tidsramme men ikke
  de andre to.
- Datoen er **hvornår backtesten køres**, ikke hvornår koden blev skrevet.
- `RunID` i selve filen er identisk med filnavnet, så en løsreven fil altid
  kan spores tilbage til den kørsel, der lavede den (bruges i journalen).

**Teknisk forhindring:** et filnavn, der skal bygges dynamisk (med
tidsrammer og dato indlejret), kan ikke bruges med `Print(File(...))`,
fordi den kræver et fast, bogstaveligt filnavn. Løsningen blev at bruge
`FileAppend(FilNavn, tekst)` i stedet, som accepterer en variabel som
filnavn. Prisen: `FileAppend` åbner og lukker filen for hver linje, der
skrives, og er derfor langsommere end `Print(File(...))`, som holder filen
åben hele kørslen. En hastighedstest af dette er bygget ind i
`RawSignalTest_1.el`, men endnu ikke kørt/rapporteret tilbage.

Tidsrammerne aflæses automatisk med `BarInterval of data(1/2/3)`, og
kørselsdatoen med `ComputerDateTime` — strategien behøver ikke få nogen af
delene fortalt, den finder dem selv.

## To testfiltre bygget, med to meget forskellige udfald

**`RawSignalTest_2`** (ingen parametre — lukkekurs under gårsdagens
dagsluk): enkel, byggede og verificerede uden problemer. Dette er
referenceeksemplet for et filter uden parametre.

**`RawSignalTest_1`** (Thomas' MACD-baserede filter, to parametre N1 og
N2): afslørede et alvorligt og generelt problem.

### Det centrale tekniske fund: indbyggede seriefunktioner i en løkke

`MACD` — og lignende indbyggede TradeStation-funktioner som `RSI`,
`StandardDev`, `Average`, `DMIplus`/`DMIminus`, `ChaikinMoneyFlow`,
`AvgTrueRange` — bygger internt på funktioner som `XAverage`, der **husker
deres egen forrige værdi** for at kunne regne den næste. Den hukommelse er
knyttet til **kodelinjen**, ikke til den specifikke parameterværdi.

Kaldes samme linje MACD 625 gange på én bar, med 625 forskellige
parameterlængder (i en løkke, for at afprøve mange kombinationer), deler
alle kombinationerne den samme interne hukommelse. Resultatet **kan blive
forkert, uden at der kommer nogen fejlmeddelelse.** TradeStation
kompilerer, kører, og leverer tal, der ser fuldstændig normale ud.

Det blev konkret bevist: da RawSignalTest_1 blev kørt, viste tal for 14
forskellige N2-værdier (12 til 25) præcis samme starttidspunkt og samme
varighed — hvilket er matematisk umuligt, når de repræsenterer gennemsnit
af meget forskellig længde. TradeStation gav samtidig selv advarslen "A
series function should not be called more than once with a given set of
parameters" ved verificering — en bekræftelse fra værktøjet selv, ikke kun
en teoretisk bekymring.

**To løsningsveje blev undersøgt:**

1. **Håndregnet matematik.** De eksponentielle gennemsnit regnes selv, med
   separat hukommelse pr. parameterkombination (arrays i stedet for
   TradeStations indbyggede funktion). Denne udgave blev bygget og virker
   uden advarsler — men er markant mere kode, og skal bygges særskilt for
   hver underliggende funktionstype (MACD, RSI, StandardDev, DMI, osv.).
   Findes i projektets historik (git-commit `12120a8`), hvis den skal
   bruges igen.

2. **Acceptere risikoen.** Brug de indbyggede funktioner direkte, som
   Thomas oprindeligt skrev dem, og dokumentér advarslen tydeligt i hver
   fils hoved i stedet for at løse den. Hurtigere at bygge i stor skala,
   men tal fra parametriserede filtre bør kontrolleres, før de bruges til
   noget vigtigt.

**Beslutning: vej 2 er valgt, og gælder for alle 381 filtre**, ikke kun
RawSignalTest_1. Dette blev besluttet efter at det stod klart, at næsten
alle 381 filtre i TradingDB bruger denne slags indbyggede funktioner —
håndregning af hver enkelt funktionstype ville være en markant større
opgave end først antaget.

### Sekundært fund: `floor`/`maxlist` skaber dubletter

`maxlist(2, floor(N2/2))` giver kun 11 forskellige værdier for 25
N2-værdier, så mange af de 625 kombinationer bliver nøjagtige dubletter af
hinanden (samme signal, forskelligt N2). Dette blev undersøgt grundigt
(bl.a. afprøvet uden `floor`, hvilket reducerede dubletterne markant), men
til sidst besluttet at **bevare Thomas' oprindelige formel uændret** i
RawSignalTest_1, inklusive dubletterne — samme princip som ovenfor: formlen
fra databasen er facit, ikke noget der skal "forbedres" undervejs.

### N1/N2 gjort til Fra/Til/Step

Oprindeligt faste `For N1 = 1 to 25`-løkker. Ændret til `While`-løkker
styret af tre separate Input pr. parameter (`N1_Fra`, `N1_Til`, `N1_Step`),
for at kunne styre skridtstørrelse (fx kun ulige tal, eller spring 2 ad
gangen for hurtigere test-kørsler) uden at ændre koden. Dette viste sig
efterfølgende at matche TradingDB's kolonnestruktur næsten identisk.

## TradingDB opdaget

Thomas viste, at der findes en Postgres-database (`TradingDB`), tabellen
`filter_case`, med **381 filtre** allerede defineret — bygget af en anden,
lokal Claude Code-session, der kører fysisk på Thomas' server (ikke via
fjernskrivebord).

**Vigtig afklaring om arkitektur:** denne session (som skriver denne log)
kører i en midlertidig sky-boks og har **kun** forbindelse til GitHub-
projektet `DetStoreProjekt`. Den kan ikke se TradingDB, ikke TradeStation,
ikke noget på Thomas' fysiske maskine. Den lokale session har omvendt
adgang til TradingDB og TradeStation, men (formentlig) ikke til denne
samtale. De to sessioner deler intet andet end det, der bevidst lægges ind
i GitHub-projektet.

**Tabellens struktur** (`filter_case`):

| Kolonne | Indhold |
|---|---|
| `filter_case_id` | Unikt løbenummer, 1-381 |
| `filter1_n1_start/end/step` | Fra/Til/Step for N1 (kan være tom) |
| `filter1_n2_start/end/step` | Fra/Til/Step for N2 (kan være tom) |
| `gammel_case` | Internt gruppenummer fra ældre system — ikke relevant |
| `filtere` | Selve filterformlen som EasyLanguage-tekst |

**Vigtig faldgrube fundet:** man kan ikke gå ud fra, hvilke parametre en
formel bruger, ud fra om databasekolonnerne er udfyldt. Nogle formler
bruger **kun** `Filter1_N2` og slet ikke `Filter1_N1`, selvom begge sæt
kolonner har værdier. Formlens tekst skal læses for at afgøre det.

Eksempler på formler set i databasen (viser variationen):
```
Average( MACD(C, Filter1_N1*2, Filter1_N1*2*maxlist(2,floor(Filter1_N2/2))), 9) < MACD(...);
RSI(Close, Filter1_N1*3) of data(DataFilter_A) > 50;
StandardDev(Close, 2*Filter1_N1, 1) > Average(StandardDev(...), 0.25*Filter1_N2);
DMIplus(Filter1_N1*10) of data(DataFilter_A) < DMIminus(Filter1_N1*10) of data(DataFilter_A);
ChaikinMoneyFlow(3*Filter1_N1) of data(DataFilter_A) > 0;
```
Fælles for de fleste: de bruger indbyggede seriefunktioner (MACD, RSI,
StandardDev, DMI, ChaikinMoneyFlow) — samme klasse funktioner som gav
problemet i RawSignalTest_1. Beslutningen om at acceptere og dokumentere
risikoen (i stedet for at håndregne) gælder derfor bredt på tværs af de 381.

## Arbejdsbeskrivelse skrevet

`ARBEJDSBESKRIVELSE_RawSignal.md` er skrevet til den lokale Claude
Code-session, med de 381 filer som mål. Den beskriver:
- Skabelonen der skal genbruges (struktur identisk med RawSignalTest_1/2)
- Reglen om at læse formlens tekst for at afgøre parameterbrug
- At formler fra databasen ikke må ændres eller "forbedres"
- At array-størrelser skal sættes efter den største værdi i hele tabellen,
  ikke kun den enkelte fils egen, så Fra/Til/Step senere kan hæves uden at
  ramme en for lille grænse
- At filerne bygges i bundter (10-20 ad gangen), ikke alle 381 på én gang,
  så en systematisk fejl opdages tidligt

## Verificering — endnu uløst

Ingen af Claude Code-sessionerne kan styre TradeStations grafiske flade for
at trykke "Verify". Det har hele dagen krævet, at Thomas selv gjorde det og
sendte screenshots tilbage.

**Besluttet:** der skal bygges et selvstændigt automationsprogram, som
lægger hver `.el`-fil ind i TradeStation, verificerer den, og rapporterer
resultatet — fil for fil, uden at Thomas skal gøre det manuelt 381 gange.
Dette var i forvejen planlagt at skulle laves.

**Ikke besluttet endnu** (skrevet som åbne spørgsmål i
`ARBEJDSBESKRIVELSE_RawSignal.md`):
1. Findes der en kommandolinje- eller API-adgang til TradeStation, eller
   skal automationen simulere museklik og tastatur (mere skrøbeligt)?
2. Skal programmet stoppe ved første fejl, eller notere og fortsætte?
3. Arbejder den lokale session i samme git-projekt som denne session
   (`DetStoreProjekt`, hentet med `git pull`), eller et andet sted uden
   GitHub-forbindelse?

## Filoversigt i projektet

| Fil | Formål | Status |
|---|---|---|
| `EdgeFinder_F5_SIGNAL.el` | Det oprindelige filter, ombygget til array-baseret enkelt-gennemløb | Virker, kørt af Thomas |
| `RawSignalTest_2.el` | Referenceeksempel: filter uden parametre, dynamisk filnavn | Virker, verificeret |
| `RawSignalTest_1.el` | Referenceeksempel: filter med to parametre (N1/N2 Fra/Til/Step), Thomas' oprindelige MACD-formel, kendt seriefunktions-risiko dokumenteret i filens hoved, tester FileAppend-hastighed | Verificeret (kompilerer), hastighedstest afventer resultat |
| `NOTER.md` | Levende teknisk referencedokument — EasyLanguage-regler, navngivning, kørselsvejledning | Løbende opdateret |
| `ARBEJDSBESKRIVELSE_RawSignal.md` | Spec til den lokale Claude Code-session for at generere de 381 filer + automationsprogram | Under udarbejdelse, åbne spørgsmål udestår |
| `BESLUTNINGSLOG_2026-09-18.md` | Denne fil | Øjebliksbillede af dagens arbejde |

## Hvad der IKKE er lavet endnu

- De 381 `.el`-filer er ikke genereret.
- Automationsprogrammet til at verificere dem er ikke bygget.
- Hastighedstesten af `FileAppend` på en stor fil er ikke kørt/rapporteret.
- De tre åbne spørgsmål ovenfor om automationsprogrammet er ikke besvaret.
