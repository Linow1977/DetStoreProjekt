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
```

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
| `max_bars_back.py` | Regner Max Bars Back ud til filernes hoved |
| `generer.py` | Bygger teksten til strategi og ShowMe |
| `tde_styring.py` | Finder, åbner og genstarter TDE og kalder verify-scriptet |
| `tde\verify-one.ps1` | Opretter én fil i TDE, indsætter koden, kører Verify, lukker |
| `tde\tsdev-lib.ps1` | Læser Output-panelet i TDE |
| `indlaes_csv.py` | Læser en CSV-fil ind i `rawsignal.rawsignal<nr>` |
| `log\rawsignal_creature.log` | Alt, programmet har gjort |

## Regler, koden bygger på

- Formlen fra `filter_case` sættes ind ordret. Kun `Filter1_N1`/`Filter1_N2`
  udskiftes, og det kontrolleres, at formlen er ens i begge filer.
- Kan noget ikke bygges sikkert (fx ukendt funktion i Max Bars Back), stopper
  programmet hellere end at gætte.
- Der skrives kun i databasen, når BEGGE filer er godkendt i TDE. Så
  markeres filteret færdigt i `filter_case.rawsignal_faerdig` i samme
  transaktion.
- Går noget galt, ryddes det op, og filteret køres forfra.
- TDE styres uden tastetryk: menukommandoerne sendes direkte til vinduet.
  Det virker også, når fjernskrivebordet er minimeret.
- Er der ikke kontakt til TDE, lukkes den og åbnes igen, og filteret
  verificeres forfra (højst én gang).

## Kendte begrænsninger

- Seriefunktioner (MACD m.fl.) i en løkke kan give forkerte tal uden fejl.
  Filens hoved viser, om filteret er målt.
- Max Bars Back kender endnu ikke alle funktioner i `filter_case`.
- Programmet kører ét filter ad gangen.
