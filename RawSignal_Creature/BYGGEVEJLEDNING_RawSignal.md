# Byggevejledning: sådan laves en RawSignal-fil

Skrevet 23. september 2026, efter at have bygget og afprøvet filer for seks
forskellige filtertyper i TradeStation.

Dette dokument beskriver, hvad der skal til for at bygge en RawSignal-fil der
virker — ikke bare kompilerer. Der er forskel, og den forskel kostede en hel
dag at finde ud af.

`NOTER.md` er den korte tekniske huskeliste. Dette er den udførlige
gennemgang: hvad der blev bygget, hvad der gik galt, og hvorfor reglerne er,
som de er.

---

## 1. Hvad en RawSignal-fil skal gøre

Registrere to ting, og intet andet:

- **hvornår** et filter tænder
- **hvor mange bars** det er tændt

Hver gang filteret slukker, skrives én linje i en CSV-fil. Ikke andet. Ingen
handelslogik, ingen analyse — den sker bagefter i Python.

En vigtig konsekvens: **linjen skrives først, når filteret slukker.** Er
filteret stadig tændt på den allersidste bar i dataene, bliver den sidste
periode aldrig skrevet. Det er højst én manglende linje pr. variant, men det
skal man vide, når tallene tælles op.

---

## 2. Først: læs formlen, ikke databasekolonnerne

Dette er den vigtigste enkeltregel, og den er nem at overtræde.

Tabellen `filter_case` har kolonner for både N1 og N2. **Man kan ikke slutte
ud fra dem, hvilke parametre formlen bruger.** Nogle formler bruger kun
`Filter1_N2` og slet ikke `Filter1_N1`, selvom begge sæt kolonner har
værdier. Andre har tomme N1-kolonner og bruger kun N2.

Formlens tekst er facit. Søg efter `Filter1_N1` og `Filter1_N2` i teksten.

Målt på alle 381 rækker fordeler det sig sådan:

| Formlen bruger | Antal filtre |
|---|---|
| Både N1 og N2 | 128 |
| Kun N1 | 114 |
| Kun N2 | 62 |
| Ingen parametre | 77 |

Derudover:

- **52 filtre bruger `DataFilter_B`** — en anden datastrøm. Ingen bruger
  `DataFilter_C`.
- **8 filtre har decimaltal** i N2 (skridt på 0,25). Resten er hele tal.
- **Ingen** filtre bruger mere end to parametre.
- **Ingen** formler er tomme.
- Største værdi i hele tabellen er 25 for både N1 og N2.

---

## 3. De fire strukturer

Hvilke Input, løkker og arrays filen skal have, afgøres alene af hvilke
parametre formlen bruger.

### Ingen parametre (77 filtre)

Ingen løkke. Almindelige variabler i stedet for arrays. Følg mønstret i
`RawSignalTest_2.el`.

```
Var:
	int    Filter1( 0 ),
	int    Filter1_Forrige( 0 ),
	int    SignalBars( 0 ),
	string StartTekst( "" );
```

### Kun én parameter (114 + 62 filtre)

Én `While`-løkke, ét sæt Fra/Til/Step-inputs, éndimensionelt array.

```
Arrays:
	int    Filter1[25]( 0 ),
	...
	N1 = N1_Fra;
	While N1 <= N1_Til
		Begin
		...
		N1 = N1 + N1_Step;
		End;
```

Bruger formlen kun N2, hedder variablen `N2` — ikke `N1`. Og CSV-filen får
en `N2`-kolonne, ikke en `N1`-kolonne.

### Begge parametre (128 filtre)

To indlejrede `While`-løkker, todimensionelt array. Følg `RawSignalTest_1.el`.

```
Arrays:
	int    Filter1[25,25]( 0 ),
```

### Decimaltal (8 filtre) — den eneste tilladte afvigelse

Et array kan ikke slås op med 1,25. Derfor deles parameteren i to:

```
Var:
	double N2_Vaerdi( 0 ),     // selve tallet, bruges i formlen
	int    N2_Indeks( 0 ),     // 1, 2, 3 ... bruges til arrayet

	N2_Vaerdi = N2_Fra;
	N2_Indeks = 1;
	While N2_Vaerdi <= N2_Til
		Begin
		... Filter1[N2_Indeks] ...
		N2_Vaerdi = N2_Vaerdi + N2_Step;
		N2_Indeks = N2_Indeks + 1;
		End;
```

Inputtene skal være `double` i stedet for `int`, og værdien skrives med to
decimaler i CSV-filen: `NumToStr( N2_Vaerdi, 2 )`.

**Denne opdeling må kun bruges i de 8 filtre, der faktisk har decimaltal.**
De øvrige 373 skal følge skabelonen nøjagtigt, hvor `N1` er både værdi og
indeks. Afvigelser fra skabelonen har tidligere kostet timer.

---

## 4. Skabelonens faste dele

Alle filer har samme opbygning i samme rækkefølge.

### Input

```
Input:
	int    DataFilter_A( 2 ),
	int    DataFilter_B( 3 ),      // KUN hvis formlen bruger den
	int    N1_Fra( 1 ),
	int    N1_Til( 25 ),
	int    N1_Step( 1 );
```

`DataFilter_A` er altid **2**, `DataFilter_B` altid **3**. Tallene henviser
til data-nummeret på chartet, ikke til minutter.

**Bruger filteret `DataFilter_B`, skal chartet have mindst tre
datastrømme.** Har det kun to, kan strategien ikke køre.

Der er **ingen** `Mappe`- eller `RawSignalNavn`-Input. Filnavnet skrives
direkte i koden — se punkt 5.

### Array-størrelse

Altid 25, uanset hvad det enkelte filter bruger. Begrundelsen: 25 er den
største `_end`-værdi i hele tabellen, så Fra/Til/Step kan senere hæves uden
at ramme en for lille grænse. Skriv størrelsen som kommentar ved
deklarationen.

Går et Fra/Til/Step ud over 25 trin, **skal** arrayet hæves i koden. Det
følger ikke automatisk med.

### Once-blokken

```
	Once
		Begin
		FileDelete( "C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\RawSignal069.csv" );
		Print( File("...samme sti..."), "RunID,N1,N2,Starttid,AntalBars" );
		End;
```

`FileDelete` først, så gentagne beregninger af chartet ikke dubler linjerne.

### Tidsstempel

Beregnes én gang pr. bar, uden for løkken — ikke inde i den:

```
	BarTekst = FormatDate( "yyyy-MM-dd", ELDateToDateTime( Date of data(DataFilter_A) ) )
	         + " "
	         + FormatTime( "HH:mm", ELTimeToDateTime( Time of data(DataFilter_A) ) );
```

### Tænder / fortsætter / slukker

Identisk i alle filer. Rækkefølgen betyder noget, og `Filter1_Forrige`
opdateres til sidst:

```
	// TÆNDER
	If Filter1[...] = 1 and Filter1_Forrige[...] = 0 Then
		Begin
		StartTekst[...] = BarTekst;
		SignalBars[...] = 1;
		End;

	// FORTSÆTTER
	If Filter1[...] = 1 and Filter1_Forrige[...] = 1 Then
		SignalBars[...] = SignalBars[...] + 1;

	// SLUKKER — linjen skrives her
	If Filter1[...] = 0 and Filter1_Forrige[...] = 1 Then
		Begin
		Print( File("..."), ... );
		SignalBars[...] = 0;
		End;

	Filter1_Forrige[...] = Filter1[...];
```

---

## 5. Filnavne og CSV-format

### Print(File(...)) — ikke FileAppend

`Print(File("..."))` kræver et **fast, bogstaveligt filnavn i
anførselstegn**. En variabel giver compile-fejlen `File name expected here`.

`FileAppend` kan tage en variabel, men blev droppet 19. september: den åbner
og lukker filen for hver eneste linje og var for langsom på 625
kombinationer. **FileAppend må ikke bruges.**

Konsekvensen er, at filnavnet skrives ordret ind i koden — tre steder:
`FileDelete`, overskriftsrækken, og linjen der skrives ved slukning. Alle tre
skal være ens.

### Stier

```
.EL-filer:   C:\TradingDB_Folder\FilterFolder\RawSignal.EL\
CSV-output:  C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\
```

`C:\RawSignal_2026_TS\` var det oprindelige forslag og er **forladt**.

### CSV-kolonner

Kun de kolonner, filteret faktisk bruger:

| Filteret bruger | Overskriftsrække |
|---|---|
| Ingen parametre | `RunID,N1,Starttid,AntalBars` (N1 skrives altid som 1) |
| Kun N1 | `RunID,N1,Starttid,AntalBars` |
| Kun N2 | `RunID,N2,Starttid,AntalBars` |
| Begge | `RunID,N1,N2,Starttid,AntalBars` |

At filtre uden parametre alligevel skriver en `N1`-kolonne med værdien 1 er
et valg fra `RawSignalTest_2`: så har alle filer samme format og kan læses af
Python på samme måde.

### RunID skal være identisk med filnavnet

`RunID` i hver linje skal være præcis det samme som CSV-filens navn uden
mappe og endelse. Så kan en løsreven fil altid spores tilbage til det signal,
der lavede den.

Dette blev overtrådt én gang undervejs: en fil skrev til
`RawSignal069_MedPlot.csv` men satte `RawSignal069` som RunID. Tjek altid, at
de to stemmer.

---

## 6. Max Bars Back — regnes ud pr. filter

`Max Bars Back` skal dække den længste beregning i formlen ved de højeste
parameterværdier. Sættes den for lavt, **begynder strategien slet ikke at
regne** — og så oprettes CSV-filen aldrig, ikke engang med overskriftsrække.

Det er et godt diagnostisk tegn: **ingen CSV-fil overhovedet betyder som
regel Max Bars Back, ikke en kodefejl.** Overskriftsrækken skrives i
`Once`-blokken, før filteret vurderes, så findes filen ikke, er koden aldrig
kommet i gang.

Eksempler fra de byggede filer:

| Filter | Længste beregning | Anbefalet |
|---|---|---|
| `RawSignal069` | MACD 25·2·12 = 600, +9 | mindst 650 |
| `RawSignal020` | DMI 25·10 = 250 | mindst 300 |
| `RawSignal266` | Average over 25 | mindst 50 |
| `RawSignal126` | dagens åbningskurs | Auto Detect |

Auto Detect virker, men er ikke bekræftet pålidelig i alle tilfælde. Et
filter, der ikke vil køre, bør tjekkes manuelt for netop dette.

---

## 7. Det alvorlige problem: seriefunktioner i en løkke

### Hvad der sker

Indbyggede funktioner som `MACD`, `RSI`, `StandardDev`, `Average`, `DMIplus`,
`DMIminus`, `ChaikinMoneyFlow` og `AvgTrueRange` husker deres egen forrige
værdi for at kunne regne den næste. **Den hukommelse hører til kodelinjen —
ikke til parameterværdien.**

Kaldes samme linje 625 gange på én bar med 625 forskellige længder, deler
alle kombinationerne den samme hukommelse. Resultatet bliver forkert, og der
kommer **ingen fejlmeddelelse**.

### Det er målt, ikke formodet

`RawSignal069` blev kørt som rigtig backtest den 23. september. Resultat:

- CSV-filen fyldte **114 MB** med knap **3 millioner linjer**
- 200.000 linjer blev analyseret, svarende til 8.000 signal-hændelser
- **N2 gjorde forskel i nul ud af 8.000 hændelser**
- **N1=1 og N1=25 gav nøjagtig de samme 480 signaler**

Filen indeholder altså 480 rigtige signaler, gentaget 625 gange. Hele
parametersøgningen er værdiløs for dette filter.

Det er matematisk umuligt, at en MACD med langsom længde 4 og en med længde
600 giver samme signal på samme bar. Tallene er forkerte.

### Advarslen ved Verify kan IKKE bruges til at finde de ramte

Dette er vigtigt, og det er nyt:

| Fil | Bruger seriefunktion i løkke | Advarsler ved Verify |
|---|---|---|
| `RawSignal069` | MACD ×3 | **3** |
| `RawSignal020` | DMIplus, DMIminus | **2** |
| `RawSignal266` | Average | **0** |
| `RawSignal004_Test` | ChaikinMoneyFlow | **0** |

`RawSignal266` og `004_Test` har nøjagtig samme problem som 069 — TradeStation
siger bare ingenting. **Fravær af advarsel betyder ikke, at filen er i
orden.** Advarslen skal derfor stå i *hver* fils hoved, uanset hvad
compileren siger.

### Hvilke filtre er upåvirkede

Filtre uden seriefunktion. De bruger kun almindelige kursreferencer som
`Open`, `Close`, `High`, `Low`, `OpenD`, `CloseD`, `TrueRange`, `AbsValue`.
Dem gælder problemet ikke for, og deres parametersøgning er gyldig.

185 af de 381 filtre indeholder ingen af de kendte seriefunktioner.

### Kendte veje videre — ikke besluttet

1. **Håndregnet matematik.** Egen hukommelse pr. kombination i arrays i
   stedet for de indbyggede funktioner. Eneste kendte løsning. Findes i
   git-commit `12120a8`. Skal bygges særskilt for hver funktionstype.
2. **Én kørsel pr. parametersæt.** Behold de indbyggede funktioner, men lad
   hver backtest køre med ét fast parametersæt via Inputs i stedet for en
   løkke. Så er der kun ét kald pr. kodelinje. Prisen er mange kørsler.
3. **Begynd med de 77 filtre uden parametre.** De er upåvirkede.

---

## 8. Verify beviser ikke, at filen virker

Dette kostede en runde. `0 error(s)` i TradeStation Development Environment
betyder kun, at koden kan oversættes. Det siger intet om, at:

- CSV-filen bliver oprettet
- tallene er rigtige
- beregningstiden er acceptabel

Alle fem første filer gav `0 error(s)` ved Verify. Først da backtesten blev
kørt, viste det sig, at 069's tal var ubrugelige, og at 020 slet ikke
skrev nogen fil.

**Verify er en portvagt, ikke et bevis.** En fil er først i orden, når
backtesten er kørt og CSV-filen er set efter.

---

## 9. Datamængde

`RawSignal069` producerede 114 MB fra ét filter. Gange 381 bliver det til
mange gigabyte. Det bør indgå i planlægningen — både diskplads og den tid,
Python skal bruge på at læse det.

En stor del af de 114 MB er ren gentagelse (625 kopier af samme 480
signaler). Løses seriefunktions-problemet, falder mængden formentlig
betydeligt — men for filtre hvor parametrene *rent faktisk* gør en forskel,
vil filerne være store.

Et praktisk greb ved test: hæv `N1_Step` og `N2_Step` til fx 5. Så regnes
5×5 = 25 kombinationer i stedet for 625 — 25 gange hurtigere. Det kræver
ingen ændring i koden, kun i felterne før kørslen.

---

## 10. Plot: at se signalet på chartet

En **strategi kan ikke tegne** i EasyLanguage. `Plot` findes kun i Indicator-
og ShowMe-studier.

**Brug ShowMe, ikke Indicator.** En Indicator forbinder sine punkter med en
linje, så man får én lang streg hen over chartet. En ShowMe sætter
enkeltprikker og forbinder ikke.

En ShowMe kan godt både tegne og skrive CSV-filen, så alt ligger i én fil:

```
	If <filteret> Then
		Vis_Taendt = 1
	Else
		Vis_Taendt = 0;

	If Vis_Taendt = 1 Then
		Plot1( Low of data(DataFilter_A), "Taendt" );
```

Der sættes en prik på **hver** bar, filteret er tændt — ikke kun den første.
Så kan begge dele aflæses direkte:

- `Starttid` = den første prik i en sammenhængende række
- `AntalBars` = antal prikker i rækken

### To ting der gør den brugbar

**`SkrivCSV`-kontakten.** TradeStation genberegner hele studiet, hver gang et
hvilket som helst Input ændres — også det, der vælger hvilken parameter der
vises. Med CSV-skrivning slået til betyder det, at filen slettes og skrives
forfra, hver gang man bare vil flytte en prik. Derfor:

```
	int    SkrivCSV( 0 ),      // 0 = kun prikker, 1 = skriv også CSV
```

Sæt til 1, lad den skrive filen én gang, sæt tilbage til 0.

**Plottet regnes uden for løkken.** Med ét fast parametersæt kaldes MACD kun
én gang pr. kodelinje, og seriefunktions-fejlen opstår ikke. **Prikkerne
viser altså det rigtige signal, mens CSV-filen kan være forkert.** Det gør
den til et direkte måleinstrument: skift parameteren, se prikkerne flytte
sig, og slå de samme værdier op i CSV-filen. Står den stille, er fejlen
bekræftet — synligt på chartet.

---

## 11. Ting der ikke må laves om

- **Formlen fra databasen skal ind ordret.** Kun `Filter1_N1` og
  `Filter1_N2` udskiftes med løkkevariablerne. Formlen må ikke "rettes" eller
  forbedres — heller ikke selvom den kalder den samme funktion tre gange med
  identiske argumenter, eller producerer dubletter.
- **`Optimize` må ikke bruges.** TradeStation kører optimeringspas parallelt,
  og de deler samme fil. Kun det første pas kan åbne den; resten fejler med
  `OpenFileException` / `WriteFileException`. Derfor løkken og almindelig
  backtest i stedet.
- **CSV-filen skal være lukket i Excel** under kørsel. En åben fil blokerer
  skrivningen og giver samme fil-fejl.

---

## 12. Praktiske detaljer der koster tid at genopdage

**Danske bogstaver virker.** æ, ø og å i kommentarer kompilerer fint.
Skabelonfilerne bruger dem, og de skal bevares.

**Filnavnet står tre steder** i hver fil. Bruges en fil som udgangspunkt for
en anden, skal alle tre rettes — ellers skriver to filtre til samme CSV.

**Strateginavne skal være unikke.** Forsøges en strategi oprettet med et navn,
der allerede findes i TradeStation, ender programmet i en uforudsigelig
tilstand. Slå altid op i tabellen `rawsignal` i TradingDB først, og spring
over hvis navnet allerede er kørt.

**Tabellen `rawsignal`** ligger i `TradingDB` → skema `public`:

| Kolonne | Indhold |
|---|---|
| `rawsignal_name` | fx `RawSignal069` — primærnøgle, sikrer unikke navne |
| `dev_date` | byggedato, hele sekunder |
| `signal_path` | hvor `.el`-filen ligger |
| `verification` | `OK` eller `FEJLET` |
| `note` | fejl- eller advarselstekst fra Output-panelet |

---

## 13. Status pr. 23. september 2026

**Bygget og verificeret** (0 fejl ved Verify), én pr. strukturtype:

| Fil | Type | Advarsler | Backtest |
|---|---|---|---|
| `RawSignal069` | N1+N2, MACD | 3 | Kørt — tal ubrugelige |
| `RawSignal126` | Ingen parametre | 0 | Kørt — virker |
| `RawSignal020` | Kun N1, DMI | 2 | Ingen CSV, formentlig Max Bars Back |
| `RawSignal174` | Kun N2, ingen seriefunktion | 0 | Ikke rapporteret |
| `RawSignal266` | `DataFilter_B` + N1, Average | 0 | Ikke rapporteret |
| `RawSignal069_MedPlot` | ShowMe med plot + CSV | — | Virker |
| `RawSignal332_MedPlot` | Decimaltal, kun N2, to datastrømme | — | Ikke afprøvet |

**Ikke afklaret:**

- Hvilken vej for de 304 parametriserede filtre, jf. punkt 7.
- De 381 filer, der blev genereret maskinelt, følger ikke skabelonen: de
  bruger værdi/indeks-opdelingen i alle filer i stedet for kun i de 8 med
  decimaltal. De skal bygges om, før de kan bruges.
- `RawSignal020` skrev ingen CSV-fil. Skal køres igen med Max Bars Back på
  mindst 300.
