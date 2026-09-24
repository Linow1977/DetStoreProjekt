# RawSignal Creature – opgavebeskrivelse

Opdateret 24. september 2026. Erstatter alle tidligere versioner.
Er andre filer uenige med dette dokument, følg dette dokument.

> **Tilføjet 24. september om aftenen:** Opgaven er udført. Beslutningerne
> fra dagen står i `BESLUTNINGSLOG_2026-09-24.md` og gælder foran dette
> dokument, hvor de er uenige. Det gælder især CSV-formatet (ny kolonne
> `Afsluttet`, sidste signal skrives), tabelkolonnerne, omnummereringen af
> `filter_case` (alle numre én ned) og svarene på de åbne punkter i afsnit 6.
> Programmet ligger i `Program/`.

---

## 1. Opgaven i fire trin

```
1. Filteret hentes i TradingDB (Filter_Case)
2. Omskrives til to filer:
     RawSignal<nr>            strategi
     RawSignal<nr>_Kontrol    ShowMe
3. Verificeres i TDE (af RawSignal Creature selv, som dagen før)
4. Info lægges i TradingDB-tabellerne:
     strategi -> rawsignal
     ShowMe   -> RawSignal_Kontrol
```

Alt andet i dette dokument er detaljer om trin 2. Det fortæller, hvad de to filer skal indeholde.

**Sådan arbejdes der:**
- Kvalitet over hastighed. Tænk før du bygger. Gæt aldrig. Spørg ved tvivl.
- Kun `Filter_Case` ændres. De genererede filer rettes aldrig i hånden. Programmet laver dem forfra.
- Lav kun de ændringer, opgaven kræver.
- Alle filer fra 22. september er slettet. Vi starter friskt.

## 2. Rækkefølge

**Trin A: tabellen `RawSignal_Kontrol`**
- Læs den faktiske struktur af `rawsignal` i databasen (kolonner, typer, primærnøgle, regler).
- Lav `RawSignal_Kontrol` som en tro kopi af strukturen, uden rækker. (PostgreSQL gemmer navnet som
  `rawsignal_kontrol`. Det er fint.)
- Vis SQL'en, før den køres. Rør ikke `rawsignal`.
- Tjek de 10 rækker i `rawsignal` og eventuelle strategier med samme navne i TDE. Programmet springer
  over, hvis et navn allerede findes, så gamle rester kan blokere. Slet intet uden Thomas' OK.
- Stop og vis resultatet.

**Trin B: programmet (kun efter trin A er godkendt)**
- Bygges og afprøves for 8 forskellige filtre, ÉT ad gangen, så fejl kan findes og rettes undervejs.
- Efter hvert filter: stop, og skriv hvad der blev lavet og hvad verificeringen gav. Vent på Thomas'
  besked, før næste filter.
- De 8 filtre skal tilsammen dække: ingen parametre, kun N1, kun N2, begge parametre, decimaltal,
  `DataFilter_B`, med seriefunktion og uden seriefunktion. Foreslå de 8 ud fra `Filter_Case`. Simpleste
  først. Thomas godkender listen.
- Programmet køres ikke på alle 381 filtre, før alle 8 er godkendt.

## 3. Tabellerne (trin 4)

| Fil | Tabel |
|---|---|
| Strategi `RawSignal<nr>` | `rawsignal` (findes, beholder sit navn) |
| ShowMe `RawSignal<nr>_Kontrol` | `RawSignal_Kontrol` (ny, samme kolonner) |

Kolonnerne (besluttet 24. september, ens i begge tabeller): `dev_date`, `rawsignal_kontrol_name`,
`rawsignal_kontrol_path`, `verification` (`Pass` eller `Fail`), `rawsignal_name`, `rawsignal_path`
og `note` (tekst fra Output-panelet). Primærnøgle: `rawsignal_name` i `rawsignal`,
`rawsignal_kontrol_name` i `rawsignal_kontrol`.

- Navne skal være unikke. Slå op i tabellen før noget oprettes, og spring over, hvis navnet findes.
- Strategi åbnes i TDE med Ctrl+Alt+S, ShowMe med Alt+Ctrl+M, som i den eksisterende automation.
- `RawSignal_Case` er ikke aktuelt. Ret gamle omtaler i NOTER, Automation og beslutningsloggen.

---

## 4. Hvad filerne skal indeholde (opslag til trin 2)

### 4.1 Signalet (gælder begge filer)

- Filteret er SAND eller FALSK på hver bar. Signal = skiftet fra FALSK til SAND.
- Varighed (`AntalBars`) = antal Data2-bars filteret bliver SAND i træk.
- Formelteksten fra `Filter_Case` sættes ind ordret. Kun `Filter1_N1` og `Filter1_N2` udskiftes.
  Formelteksten skal være ens i strategi og ShowMe. Tjek det, før filerne gemmes.
- Hvilke parametre filteret bruger, afgøres af formelteksten, ikke af databasekolonnerne.
- `DataFilter_A` er altid 2 og `DataFilter_B` altid 3. Data3 er større end Data2.

```
Data2-bar:  1    2    3    4    5    6    7    8
Filter:     nej  nej  JA   JA   JA   nej  JA   nej
                      ^              ^
                 Signal 1        Signal 2
                 AntalBars 3     AntalBars 1
```

### 4.2 Strategien `RawSignal<nr>`

- Skriver én linje pr. signal til en CSV-fil, når filteret slukker. Ikke andet. Ingen handelslogik.
- Struktur, Inputs, løkker og arrays følger BYGGEVEJLEDNING punkt 3 og 4, afhængigt af hvilke
  parametre formlen bruger. Array-størrelse altid 25.
- Værdi/plads-opdelingen (to variable) bruges KUN i de 8 filtre med decimaltal. Alle andre følger
  skabelonen, hvor N1 (eller N2) er både værdi og plads.
- `Once`-blokken sletter filen med `FileDelete` og skriver overskriftsrækken.
- Filnavn og sti står ordret i koden, ens de tre steder: `FileDelete`, overskriftsrækken og linjen,
  der skrives ved slukning. Python skriver dem ind. `Print(File(...))` skal bruges, ikke `FileAppend`.
- CSV-mappe: `C:\TradingDB_Folder\FilterFolder\RawSignal.CSV\`
- `RunID` i hver linje = filnavnet uden mappe og endelse.
- Tidsstemplet regnes én gang pr. bar, uden for løkken, med formatet `2020-03-15 10:45`.
- Et signal, der stadig er tændt ved backtestens slutning, skrives ikke. Det er et bevidst valg.
- Der skrives parameterens VÆRDI, aldrig dens plads i arrayet.
- Max Bars Back skal dække den længste beregning ved de højeste parameterværdier. Skriv den ind som
  kommentar i filens hoved.
- Kørsel: almindelig backtest, ikke Optimize.

| Filteret bruger | Overskriftsrække |
|---|---|
| Ingen parametre | `RunID,N1,Starttid,AntalBars` (N1 er altid 1) |
| Kun N1 | `RunID,N1,Starttid,AntalBars` |
| Kun N2 | `RunID,N2,Starttid,AntalBars` |
| Begge | `RunID,N1,N2,Starttid,AntalBars` |

Komma som skilletegn. Punktum som decimaltegn. Windows-linjeskift er fint.

### 4.3 ShowMe'en `RawSignal<nr>_Kontrol`

- Tegner KUN. Ingen CSV, ingen `FileDelete`, intet filnavn i koden.
- Plot1 sætter en markering på hver bar, hvor signalet aktiveres (skiftet FALSK til SAND).
- Ét fast parametersæt vælges med inputs (`Vis_N1` og/eller `Vis_N2`, kun de parametre filteret bruger).
  Har filteret decimaltal, skal inputtet være `double`.
- `Vis_Forrige` (forrige bars status) bruges til at skille aktivering fra fortsættelse. Den opdateres
  efter plottet.
- Plottet regnes på sin egen kodelinje med faste længder, uden løkke (se 4.4).
- Chartet skal have de samme datastrømme som strategien (Data2, og Data3 hvis formlen bruger
  `DataFilter_B`).
- Max Bars Back skal dække den længste beregning ved de valgte værdier.

### 4.4 Kendt problem: hukommelsen i seriefunktioner (ikke løst i dag)

Indbyggede funktioner som MACD og DMI husker deres forrige værdi, og hukommelsen hører til kodelinjen,
ikke til parameterværdien. Kaldes samme linje i en løkke med mange parametre, deler alle kombinationer
hukommelse, og tallene bliver forkerte uden fejlmelding.

- RawSignal069 (MACD) er målt: alle 625 kombinationer gav de samme 4.918 signaler.
- RawSignal266 (Average) er målt: forskellige signaler for hver N1. Virker altså sandsynligvis.
- Andre filtre er ikke målt. Antag intet.
- Verify beviser ikke, at en fil virker. Det viser kun, at den kan kompileres.
- Programmet skal bygge filtre med og uden seriefunktion på samme måde. Hvilken vej de filtre skal
  tage, hvor løkken giver forkerte tal, er ikke besluttet.
- Formelteksten må aldrig "forbedres", heller ikke selvom den kalder samme funktion flere gange.

---

## 5. Ikke en del af opgaven nu

- Hvad der sker med CSV-filen bagefter (flytning, EdgeFinder, RawSignal-Analysis).
- Hvilken vej de 304 filtre med parametre skal tage ved hukommelsesproblemet.
- Data1, når den senere bliver mindre end Data2 (entry-finpudsning i handelskode).
- Versionsnumre i filnavne, når en formel i `Filter_Case` ændres.
- Thomas' egen manuelle test og kontrol.

## 6. Åbne punkter, der skal spørges om (afgør ikke selv)

> **Besvaret 24. september:** 1. `RawSignal.EL\` og ny `RawSignal_Kontrol.EL\` (+ `.TXT`-kopier).
> 2. Kun Plot1. 3. Kun i filer med seriefunktion i en løkke. 4. Ja, strategien stopper med en
> fejl; Data1 rettes i chartet. 5. Testet på 13 filtre, se `BESLUTNINGSLOG_2026-09-24.md`.

1. Hvilke mapper skal `.el`-filerne ligge i (strategi og `_Kontrol`)? Foreslå, og vent på OK, før filer skrives.
2. Skal ShowMe'en også have Plot2 (bars hvor filteret bliver ved med at være sandt)?
3. Skal filens hoved have en advarsel om hukommelsesproblemet i alle filer, eller kun i filer med
   seriefunktion? Teksten må kun oplyse status (målt og virker, målt og ramt, ikke målt). Den må aldrig
   forudsige et resultat.
4. Skal strategien stoppe med en tydelig fejl, hvis Data1 og Data2 ikke er lige store?
5. Hvilke 8 filtre skal testes (punkt 2, trin B)?
