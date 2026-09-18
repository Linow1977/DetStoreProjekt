# Noter — RawSignal og EasyLanguage

Kort hukommelse for arbejdet med signal-eksport fra TradeStation.
Skrevet så den kan læses uden forhåndskendskab til koden.

## Hvad en RawSignal er

Et **råt signal**: basal information om hvad der sker og hvornår det opstår.
Ikke en handelsstrategi, ikke en analyse — bare registreringen af at et filter
tændte, hvornår det tændte, og hvor længe det var tændt.

Analysen (event-studie-metode) sker et andet sted, i Python.
TradeStation skal kun levere de rå events.

## Navngivning (besluttet, endnu ikke bygget)

| Hvad | Format | Eksempel |
|---|---|---|
| Navn | `RawSignal(nummer)` | RawSignal07 |
| Filsti | `RawSignal(Nummer)_år_måned` | `C:\Test\RawSignal07_2026_09.csv` |
| RunID | Samme som filstiens navn | `RawSignal07_2026_09` |

- Året og måneden er **hvornår backtesten køres** — ikke hvornår koden blev skrevet.
- RunID og filnavn holdes identiske, så data og filnavn altid passer sammen.
- Ingen mellemrum og ingen æ/ø/å — det gør Python-siden nemmere.
- Navnet føres ind i journalen. Derfra kan man finde både den rigtige
  RawSignal-fil og den kode der lavede den.

### Fælde ved køredatoen

`RunID` er et Input-felt og kan rettes i TradeStation lige før kørslen.
**Filstien kan ikke** — den skal stå som fast tekst inde i koden (se reglen nedenfor).

Hvis filnavnet skal vise køredatoen, skal .EL-filen altså laves lige før den
køres. Det passer sammen med idéen om at lade en skill generere filen.

## EasyLanguage-regler vi har lært (dyrt betalte)

Disse kostede flere mislykkede forsøg at finde ud af. Læs dem, før der skrives
en ny RawSignal-fil.

1. **`File(...)` må kun have et fast filnavn i anførselstegn.**
   En variabel giver compile-fejlen `File name expected here` og dermed
   `Strategy not verified`. Filnavnet skal bages ind i koden.

2. **Optimering kan ikke bruges, når der skrives til fil.**
   TradeStation kører optimeringspas parallelt. Kun det første pas får lov at
   åbne filen; resten fejler med `OpenFileException` / `WriteFileException`.
   Løsningen: lad strategien selv løbe alle varianter igennem på hver bar
   ved hjælp af arrays, og kør den som én almindelig backtest.

3. **Max Bars Back skal sættes højt nok** til den længste beregning i koden.
   Ved ATR-længder op til 25 × 5 = 125 bars skal den være mindst 130.
   Sættes under `Format Strategies → Properties for All`.

4. **CSV-filen skal være lukket i Excel**, mens TradeStation kører.
   En åben fil i Excel blokerer skrivningen og giver samme fil-fejl som ovenfor.

5. **Overskriftsrække i toppen af filen**, så Python kender kolonnenavnene.
   Skrives i et `Once`-blok sammen med `FileDelete`, så gentagne beregninger
   af chartet ikke dubler linjerne.

## Sådan køres en RawSignal-backtest

1. Luk CSV-filen i Excel.
2. Højreklik på chartet → `Format Strategies…` → marker strategien → `Format…`
3. Fanen `Inputs`: sæt faste tal i felterne.
4. Fanen `Properties for All`: `Maximum number of bars study will reference`
   → `User specified` → mindst 130.
5. `OK` → `OK`. Backtesten kører af sig selv — der er ingen start-knap.
6. Kør igen: højreklik på chartet → `Reload Chart`.

**Rør ikke `Optimize…`** — det er den, der giver fil-fejlene.

## Kendte begrænsninger

- Er et filter stadig **tændt** på den allersidste bar i dataene, bliver den
  sidste periode ikke skrevet ud. Linjen skrives først, når filteret slukker.
  Det er højst én manglende linje pr. variant.

## Åbne punkter

- **Skill til at generere .EL-filer**: besluttet at vente, til vi har lavet
  filter nummer to. Med kun ét eksempel risikerer vi at støbe tilfældigheder
  i beton i stedet for det, der faktisk varierer.
