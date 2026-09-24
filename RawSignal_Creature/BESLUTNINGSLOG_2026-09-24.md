# Beslutningslog — RawSignal-projektet, 24. september 2026

Opsummering af dagens arbejde på den lokale Claude Code-session på
DataServer. Den er skrevet, så en ny session (menneske eller Claude) kan fortsætte
uden at have været med. **Er andre dokumenter uenige med denne log, gælder
denne log.** Det gælder også OPGAVEBESKRIVELSE_RawSignal.md fra samme morgen.

Programmet ligger nu i `RawSignal_Creature/Program/` (kopi af
`C:\TradingDB_Folder\RawSignal_Creature\` på DataServer). Se dens README.md.

## Resultat

- RawSignal Creature er bygget, renset og testet (trin A og B i
  OPGAVEBESKRIVELSE_RawSignal.md).
- 13 filtre gik hele vejen igennem: bygget, verificeret (Pass) og skrevet i tabellerne.
  - 1, 7, 11, 20, 68, 112, 173, 189, 261, 265, 275, 314 og 379.
  - De dækker ingen parametre, kun N1, kun N2, begge, decimaltal, DataFilter_B, dagsværdier og seriefunktioner.
- Alt fra testene er slettet igen ved dagens slutning:
  - filer
  - rækker i `rawsignal` og `rawsignal_kontrol`
  - markeringer i `filter_case`
  - strategier i TradeStation

  Næste kørsel starter på filter 1.

## Ændringer i TradingDB

| Hvad | Beslutning |
|---|---|
| `rawsignal` og `rawsignal_kontrol` | Samme 7 kolonner i samme rækkefølge: `dev_date, rawsignal_kontrol_name, rawsignal_kontrol_path, verification, rawsignal_name, rawsignal_path, note`. Primærnøgle: strateginavn i `rawsignal`, ShowMe-navn i `rawsignal_kontrol`. `verification` er `Pass` eller `Fail`. |
| `filter_case` nr. 1 (`True;`) | Slettet. Den er ikke et filter (altid tændt = ét signal i hele testen). Alle andre filtre er rykket ét nummer ned og hedder nu 1–380. Sikkerhedskopi: tabellen `filter_case_backup_20260924`. |
| `filter_case.rawsignal_faerdig` | Ny kolonne (timestamp). Sættes, når begge filer er godkendt. Tom betyder ikke lavet endnu. Programmet kører uden nummer det laveste filter, der ikke er færdigt, så nye filtre tages med af sig selv. |
| Signaldata | Én tabel pr. filter i et eget schema: `rawsignal.rawsignal<nr>`, med kolonnerne `runid, n1, n2, starttid, antalbars, afsluttet`. Thomas valgte det for overskuelighedens skyld (først var det én fælles tabel). |

**OBS numre:** Alle henvisninger i ældre dokumenter til filternumre er de
GAMLE numre. Gamle 069 (MACD) er nu 68, gamle 266 er nu 265, og gamle 113
(gårsdagens testformel) er nu 112. Der gælder altid: nyt nr. = gammelt nr. − 1.

## Filerne pr. filter

| Fil | Type | Mappe |
|---|---|---|
| `RawSignal<nr>` | Strategi, skriver CSV | `C:\TradingDB_Folder\FilterFolder\RawSignal.EL\` + `.txt` i `RawSignal.TXT\` |
| `RawSignal<nr>_Kontrol` | ShowMe, tegner kun | `C:\TradingDB_Folder\FilterFolder\RawSignal_Kontrol.EL\` + `.txt` i `RawSignal_Kontrol.TXT\` |

- `<nr>` = `filter_case_id` med tre cifre (RawSignal007).
- ShowMe: kun Plot1, dvs. en prik hvor filteret tænder (ingen Plot2).
- Advarslen om hukommelsesproblemet står kun i filer, hvor en seriefunktion
  kaldes i en løkke. Den oplyser kun status: målt og ramt, målt og virker, eller
  ikke målt.
- `DataFilter_A( 2 )` og `DataFilter_B( 3 )` står som Inputs.
- Strategien stopper med en fejl (RaiseRunTimeError), hvis Data1 ikke har
  samme tidsramme som Data2. Data1 kan ikke rettes af koden, kun i chartet.
- **Max Bars Back står på 1000 som standard** i TradeStation (besluttet af
  Thomas samme aften). Programmet regner behovet ud ved de højeste
  parameterværdier og skriver det i filens hoved:
  - Over 1000: bygningen stopper. Det gælder ingen filtre i dag. Højeste
    behov er 609 (filter 68, MACD).
  - Kan ikke regnes helt ud: filen bygges alligevel, og hovedet siger, at
    1000 antages at være nok. Det gælder 36 filtre (CCI 18,
    ChaikinMoneyFlow 8, længden i Highest/Lowest 4, CountIf, PercentR,
    SquareRoot og Pivot*).
  - `OpenSession`/`HighSession`/`LowSession`/`CloseSession` tæller i
    sessioner ligesom `CloseD` tæller i dage og påvirker ikke Max Bars Back.
  - Alle 380 filtre kan nu bygges. Om morgenen stoppede 74 på ukendte
    funktioner.

## CSV-formatet (besluttet i RawSignal_CSV-format.docx)

```
RunID,N1,N2,Starttid,AntalBars,Afsluttet
RawSignal001,5,12,2021-10-22 16:00,4,1
```

- **Én linje pr. signal**, ikke én pr. tændt bar. Formatet med én linje pr. bar
  blev prøvet og droppet. Det gav omkring 21 mio. linjer pr. filter og ville
  fylde 0,8–1,6 TB for alle filtre.
- Kun de parametre, formlen bruger, får en kolonne. Uden parametre skrives
  `N1 = 1`.
- `Afsluttet = 0` betyder, at signalet stadig var tændt på chartets sidste
  bar. Så er `AntalBars` ikke færdigt. Linjen skrives kun én gang, også hvis
  chartet får nye bars live. (Ændrer beslutningen om, at det sidste signal
  ikke skrives. Thomas skal bruge dataene til analyse.)
- CSV læses ind i TradingDB med `python indlaes_csv.py <nr>`. De gamle linjer
  slettes først, og en fil med forkert RunID afvises. Indlæsning af flere
  filer på én gang venter, til det bliver aktuelt.

Målt: det nye filter 1 (AvgTrueRange, N1+N2) gav 939.816 signaler på 620
kombinationer med forskellige signalrækker. De 5 manglende kombinationer er
netop dem, hvor 3·N1 = 5·N2, så filteret aldrig kan være sandt. AvgTrueRange
ser altså ikke ud til at være ramt af hukommelsesproblemet.

## Automationen i TDE — det, der tog tid at finde ud af

- **Ingen tastetryk.** Simulerede tastetryk (Ctrl+Alt+S, F3) fejler, når
  fjernskrivebordet er minimeret. TDE's menukommandoer sendes i stedet
  direkte som `WM_COMMAND`. Numrene er læst fra `TSResourceDllEng.dll`:

  | Kommando | Nummer |
  |---|---|
  | New Strategy | 10576 |
  | New ShowMe | 10569 |
  | Open | 57601 |
  | Verify | 10602 |

- Dialogen "New ShowMe" har vinduesklassen `TS_IDD_INDICREATE`.
  "New Strategy" har `TS_IDD_COMMONCREATE`. Felterne har samme id'er.
- Knapper klikkes med `PostMessage`. `SendMessage` hænger, når TDE viser en
  fejlboks midt i klikket, fx "The name ... is already being used".
- Findes navnet allerede i TradeStation, åbnes den eksisterende og
  overskrives. Open-dialogen åbner kun den linje, der er **markeret i
  listen**, og det virker ikke at skrive navnet.
- Vinduestitlen er `... - <navn> : Strategy` eller `... : ShowMe` med `*`, så
  længe dokumentet ikke er gemt.
- Verify godkendes kun ved præcis "0 error(s)". Den første udgave godkendte
  ved en fejl også "10 error(s)".
- Er der ikke kontakt til TDE, lukkes den og åbnes igen, højst én gang pr.
  filter. Spørger TDE "Gem ændringer?", svares der Nej. En TDE, der er lukket
  med magt, startede nemlig i en tilstand, hvor Verify ikke virkede.
- TSDev.exe skal startes med sin egen mappe som arbejdsmappe. Ellers låser
  den programmappen.

## Arbejdsmåde (aftalt med Thomas)

- **Opstår der en fejl, rettes den, der ryddes op, og processen køres forfra.**
  Et halvt resultat lappes aldrig.
- Der skrives kun i databasen, når BÅDE strategi og ShowMe er godkendt. Så
  markeres filteret færdigt i samme transaktion.
- Thomas kan ikke indsætte tekst i Claude Code-prompten. Kommandoer, han selv
  skal køre, lægges som en .bat-fil på skrivebordet.

## Ikke gjort / åbne punkter

- BYGGEVEJLEDNING_RawSignal.md og NOTER.md er ikke skrevet om. Hvor de er
  uenige med denne log, gælder denne log.
- Scripts i `RawSignal_Creature/Automation/` er forældede og erstattet af
  `RawSignal_Creature/Program/`.
- Max Bars Back kan læres de sidste funktioner (CCI m.fl.), så de 36 filtre
  også får et udregnet behov. Det er ikke nødvendigt for at bygge dem.
- Dagsfunktionerne (`CloseD`, `HighD` osv.) giver TradeStation-advarslen om
  seriefunktioner i en løkke, men står ikke på programmets liste over
  seriefunktioner. Thomas har besluttet ikke at tilføje dem.
- Hvilken vej filtre ramt af hukommelsesproblemet (fx MACD) skal tage, er
  stadig ikke besluttet.
