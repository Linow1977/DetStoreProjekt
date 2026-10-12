# Titan — skærmbilleder fra Andrea Ungers YouTube

Skærmbilleder af Titan, som Thomas har taget fra en video på Ungers
YouTube-kanal og delt 12-10-2026. Kun til intern reference. Billederne er
gengivet i lav opløsning, så tal og ord nedenfor er aflæst efter bedste evne;
de usikre er markeret med (?). Datoen for videoen kendes ikke; testperioden i
billederne går fra 01-01-2018 til 31-12-2021, så videoen er sandsynligvis fra
efteråret 2021.

Dubletter (samme skærm taget flere gange) er udeladt.

## Opbygning af programmet

Fire faner øverst: **Settings**, **Backtest**, **Strategy manager** og
**Backtest comparison**.

## 01–03: Indstillinger (Settings)

**Øverst:**
- Strategiliste (`AN_AU_FP_FULL_2020`), mappe til rapporter og til resultater,
  knappen "Check strategy list".
- Testperiode: start 01-01-2018, slut 31-12-2021. Gemte forudindstillinger
  ("preset").
- Knapper: Save settings, Save preset, **Save setting and run backtest**.

**Advanced filters settings — otte filterfamilier (faner):**
1. **Long/Short period filters** (billede 01): Periodicity "1st Sat of every
   month" (altså vurdering den første lørdag hver måned), **Long period 9**,
   **Short period 2**, begge slået til, Th 0, Min Trades 16.
2. Alternate & avg
3. Yearly Gain/DD filter
4. Titan's behavior filters
5. Avg Trade Filters
6. Std. Dev
7. Peak test filters
8. **Ranking** (billede 02): Strategy Ranking til/fra (det er uklart på
   billedet, om den står til eller fra), Analysis period 6, Ranking mode
   "descending Net Profit", Max/cat 3, Min Trades 16, Skip cat NONE.

**Advanced settings — fem faner:** Backtest, Money Management,
**Intra-period stop**, **MaxDD suspension**, **Degrade**.
- På fanen Backtest: Correlation Mode "AU formula", Corr. TH 0,750,
  TradeLMT 0,375, ShiftC 0,750, cLoops 2.

**Main settings:** Starting Capital 200.000, Daily risk 2,000 (%),
MaxDD 10,00, MaxTotalDD 99, MarginDD 2,00, Leverage 1,00.
Afkrydsning: Excel export og LoadOnlyActive er slået til; Show One,
SaveAggregEquities, SaveAllSysEquities, ForceMinCont og Read Saved er slået fra.

**Currency settings:** egen valuta EUR og faste vekselkurser
(EUR/USD 1,20, GBP/USD 1,10, USD/JPY 110 m.fl.).

Billede 03 viser også skrivebordet bag Titan med genveje til bl.a.
MultiCharts, MATLAB og "Backup_VPS".

## 04: Backtest — daglig equity-kurve

Underfaner: Strategies to trade, Performance summary, Equity Curve
(Daily/Monthly/Annual), Annual/Monthly/Daily period Analysis.

- Øverst tre kurver: **filtered** (blå), **unfiltered** (rød) og
  "filter w/ gaps" (lyseblå).
- Filtreret ender omkring 400.000 $, ufiltreret omkring 115.000 $.
- Nederst: Max Drawdown for begge. Den filtrerede når ca. −55.000 $, den
  ufiltrerede ca. −80.000 $ (aflæst).

## 05: Backtest — årlig analyse

| År | Filtreret | Ufiltreret | 1ct Profit | Forskel filtreret − ufiltreret |
|---|---|---|---|---|
| 2018 | 138.439 $ | 76.670 $ | 782.913 $ | 61.769 $ |
| 2019 | 89.074 $ | 9.382 $ | 627.504 $ | 79.692 $ |
| 2020 | 94.393 $ | 28.178 $ | 1.843.805 $ | 66.215 $ |
| 2021 | 78.889 $ | −1.396 $ | −293.042 $ | 80.285 $ |

Tallene er aflæst i lav opløsning (?). "1ct Profit" er sandsynligvis
resultatet med én kontrakt pr. strategi (?).

## 06–08: Pr. marked (filtreret mod ufiltreret)

Hvert billede har tre dele: gevinstkurve, drawdown og nederst **SysOn**,
dvs. hvor mange af markedets strategier der var slået til hver måned.
Rød = ufiltreret, blå = filtreret.

| Marked | Strategier | Gevinst ufiltr. / filtr. | Drawdown ufiltr. / filtr. | ROA ufiltr. / filtr. |
|---|---|---|---|---|
| BP (britiske pund) | 10 | −80.359 $ / −3.899 $ | −84.131 $ / −8.033 $ | −0,96 / −0,43 |
| C (majs) | 2 | 10.788 $ / 9.708 $ | −6.993 $ / −3.958 $ | 1,54 / 2,45 |
| FGBL (tysk Bund) | 16 | 77.683 $ / 101.947 $ | −86.158 $ / −29.783 $ | 0,90 / 3,42 |

## Hvad billederne lærer os (Claudes vurdering)

1. **Titan har langt flere regler end den ene, der er beskrevet offentligt.**
   Otte filterfamilier, rangering, korrelationsfilter og tre slags stop.
   Undersøgelsen fra 12-10 skrev, at der ingen offentlig regel var for at
   stoppe midt i måneden. Fanerne **Intra-period stop** og
   **MaxDD suspension** viser, at Titan har den slags. Hvordan de virker,
   ses ikke.
2. **Indstillingerne er ikke de offentlige.** Her står lang periode 9 og kort
   periode 2, mens artiklerne nævner 12–18 og 3–6. Reglerne er altså
   indstillinger, som brugeren justerer.
3. **Kernen i skærmen er "filtreret mod ufiltreret".** Titan tester hele
   tiden sin egen udvælgelsesregel mod at handle alle strategier. Det er
   samme tanke som Pharos-udkastets R0 ("alle lige") mod R1/R2.
4. **Forsigtighed med tallene:** I dette eksempel tjener den filtrerede
   portefølje *mere* end den ufiltrerede. I Ungers blog-eksempel tjente den
   *mindre*. Testperioden 2018–2021 er sandsynligvis også den periode,
   indstillingerne er valgt på, og så ser resultatet bedre ud, end det vil
   gøre fremover. Pharos-udkastet kræver derfor, at reglen testes på nye
   papirhandler.
5. **Gode idéer til Pharos' skærm:** visning pr. marked med "SysOn"-søjler,
   årstabel med filtreret/ufiltreret/forskel, og et korrelationsloft (her
   0,75 — samme størrelsesorden som udkastets 0,7).
