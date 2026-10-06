# RawSignal Creature

Laver filtrene i TradingDB-tabellen `filter_case` om til RawSignal-filer til
TradeStation, verificerer dem automatisk i TradeStation Development
Environment (TDE) og holder styr på, hvilke der er færdige.

Beslutningerne bag står i repoet `DetStoreProjekt/RawSignal_Creature`
(OPGAVEBESKRIVELSE, BYGGEVEJLEDNING) og i `RawSignal_CSV-format.docx`.

## Sådan bruges det

```
python rawsignal_creature.py          # næste filter, der ikke er færdigt
python rawsignal_creature.py 265      # et bestemt filter
python indlaes_csv.py 265             # læs CSV ind i TradingDB efter backtesten
python rs_ts_cyklus.py RawSignal002 CL 1   # kør backtesten i TradeStation, se nedenfor
python rs_ts_kaede.py --vent RawSignal002 CL 1 2 3   # flere timeframes efter hinanden
```

### Backtest i TradeStation: `rs_ts_cyklus.py`

Kører én hel cyklus for én strategi på ét instrument og én timeframe:
åbn workspace → indsæt strategi → vent på beregningen → luk workspace (uden at
gemme) → indlæs CSV i `rawsignal.<strategi>` (én tabel pr. filter; kolonnerne
instrument_id og timeframe_id viser, hvor linjen hører til). Hvert trin skrives i
`rawsignal.tidslog`, og gennemsnittet pr. filter/instrument/timeframe i
`rawsignal.rs_tf_runtime`. Instrumentet skal stå i `public.rs_instrumenter`,
timeframen i `public.timeframes`. Workspace-navnet bygges som
`CL-5-5-10-2007-09 Test` (foreløbig regel) eller gives som 4. argument.

TradeStation styres via kommandolinjen (Ctrl+C, `.O`, `.IST`, `.C`). Det
kræver et aktivt skrivebord: forlad serveren med
`Forlad_server_uden_at_stoppe.bat` på skrivebordet, ikke ved at lukke eller
minimere fjernskrivebordet.

`rs_ts_kaede.py` kører flere timeframes efter hinanden. Fejler en cyklus,
lukkes workspacet, og kæden springer videre. Går TradeStation ned (både
ORPlat og orchart kontrolleres, også mens der ventes på beregningen),
stopper kæden helt, og en halv CSV-fil indlæses aldrig. Med `--vent` starter
kæden først, når sessionen er flyttet med `.bat`-filen, plus 1 minut:
skærmskiftet midt i en beregning fik TradeStation til at gå ned 02-10-2026.

For hvert filter laves to filer:

| Fil | Type | Gør | Mappe |
|---|---|---|---|
| `RawSignal<nr>` | Strategi | Skriver én CSV-linje pr. signal | `FilterFolder\RawSignal.EL` (+ `.TXT`) |
| `RawSignal<nr>_Kontrol` | ShowMe | Tegner, hvor filteret tænder | `FilterFolder\RawSignal_Kontrol.EL` (+ `.TXT`) |

`<nr>` er `filter_case_id` med tre cifre. CSV-filen skrives af strategien til
`FilterFolder\RawSignal.CSV` med kolonnerne
`RunID,N1,N2,Starttid,AntalBars,Afsluttet`.

## Filerne

| Fil | Indhold |
|---|---|
| `rawsignal_creature.py` | Hovedprogrammet: de fire trin for ét filter |
| `faelles.py` | Mapper, log og forbindelse til TradingDB |
| `database.py` | Læsning og skrivning i `filter_case`, `rawsignal`, `rawsignal_kontrol` |
| `formel.py` | Læser formlen: parametre, decimaltal, DataFilter_B, seriefunktioner |
| `max_bars_back.py` | Tjekker, at Max Bars Back (1000) er nok, og skriver det i filernes hoved |
| `generer.py` | Bygger teksten til strategi og ShowMe |
| `tde_styring.py` | Finder, åbner og genstarter TDE og kalder verify-scriptet |
| `tde\verify-one.ps1` | Opretter én fil i TDE, indsætter koden, kører Verify, lukker |
| `tde\tsdev-lib.ps1` | Læser Output-panelet i TDE |
| `indlaes_csv.py` | Læser en CSV-fil ind i `rawsignal.rawsignal<nr>` |
| `rs_ts_cyklus.py` | Kører backtesten i TradeStation og tager tid på hvert trin |
| `rs_ts_kaede.py` | Kører rs_ts_cyklus på flere timeframes efter hinanden |
| `log\rawsignal_creature.log` | Alt, programmet har gjort |

## Regler, koden bygger på

- Formlen fra `filter_case` sættes ind ordret. Kun `Filter1_N1`/`Filter1_N2`
  udskiftes, og det kontrolleres, at formlen er ens i begge filer.
- Kan noget ikke bygges sikkert, stopper programmet hellere end at gætte.
- Max Bars Back står på 1000 som standard i TradeStation. Programmet regner
  ud, hvor mange bars formlen skal bruge ved de højeste parameterværdier:
  over 1000 stopper bygningen; kan det ikke regnes helt ud (fx CCI, som
  programmet ikke kender endnu), bygges filen, og hovedet siger, at 1000
  antages at være nok. Dags- og sessionsfunktioner (`CloseD`,
  `OpenSession` osv.) tæller i dage/sessioner og påvirker ikke Max Bars Back.
- Der skrives kun i databasen, når BEGGE filer er godkendt i TDE. Så
  markeres filteret færdigt i `filter_case.rawsignal_faerdig` i samme
  transaktion.
- Går noget galt, ryddes det op, og filteret køres forfra.
- TDE styres uden tastetryk: menukommandoerne sendes direkte til vinduet.
  Det virker også, når fjernskrivebordet er minimeret.
- Er der ikke kontakt til TDE, lukkes den og åbnes igen, og filteret
  verificeres forfra (højst én gang).

- Seriefunktioner, der husker deres forrige værdi og er målt som ramt i en
  løkke (XAverage, RSI, MACD, DMIplus/DMIminus) eller uafklarede (ADX), står
  i `formel.UDFOLD_FUNKTIONER`. Bruger formlen en af dem, skrives filteret ud
  på én kodelinje pr. kombination med faste tal, så hver kombination får sin
  egen hukommelse - som ved en almindelig backtest. Løkken læser så kun
  resultatet. Bevist 05-10-2026: XAverage og MACD gav 100 % samme signaler som
  en uafhængig beregning fra prisdata (den gamle løkke: 0-16 %).
- `rs_ts_cyklus.py` læser CSV-filens overskrift, så filtre med kun N1 (ingen
  N2-kolonne) kan indlæses. Giver et filter 0 signaler, skrives tiden pr.
  kombination som 0.
- Beregningen regnes for færdig, når CSV-filen har stået stille i
  `STILLE_SEK` = 60 sek. Målt 06-10-2026 på de tungeste filtre (DMI, ADX,
  StandardDev, CCI, XAverage; op til 77 min på 5-5-10): længste pause mellem
  to skrivninger var 8,6 sek.

## Kendte begrænsninger

- Seriefunktioner, der ikke står i `UDFOLD_FUNKTIONER` (fx Average,
  StandardDev, AvgTrueRange, ChaikinMoneyFlow), kører stadig i løkken. De er
  målt og virker. Filens hoved viser status.
- Udfoldningen dækker kun Fra-Til fra `filter_case`. Ændres N1/N2-felterne
  under Inputs, skrives kun de kombinationer, der er udfoldet.
- Arrays har 25 pladser pr. parameter (`formel.ARRAY_STOERRELSE`). Uden
  decimaler er værdien også pladsen, så Til må højst være 25.
- Max Bars Back kan ikke regnes helt ud for alle filtre (CCI, ChaikinMoneyFlow,
  CountIf, PercentR, Pivot-funktionerne m.fl.). De bygges med 1000 som antagelse.
- Programmet kører ét filter ad gangen.
- Efter genstart af TradeStation åbner Ctrl+C ikke kommandolinjen, før den er
  åbnet én gang i hånden. Fjernskrivebordet må ikke være minimeret under
  backtesten (brug `Forlad_server_uden_at_stoppe.bat`).
