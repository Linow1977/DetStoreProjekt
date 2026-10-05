# RSA — overblik over hvad der testes (status 5. oktober 2026)

Samlet ud fra Thomas' beslutninger i chat-samlingen (aug-sep), konsulentrapporten
(29. sep) og svarene på RSA-skemaet (4.-5. okt). Detaljer og kilder:
`RSA_svar_gennemgang_2026-10-04.md`. Testfasen er ikke færdig.

## Formål

RSA (RawSignal-Analyse) er selve Event Study'et. Den afgør, om et filters
signal har en **retning** (Long/Short) og er **stabilt** — over tid og over
nabo-indstillinger. RSA regner ikke med omkostninger og bestemmer ikke exit.

Plads i kæden: TradingDB → RawSignal Maker → **RSA** → Code Creater →
Edge-Finder / Edge-Cruncher → Incubator → Pharos.

## Det, RSA får ind

| Hvad | Indhold |
|---|---|
| Signalfil pr. filter | `RunID, N1, N2, Starttid, AntalBars, Afsluttet` — én linje pr. signal (overgang falsk → sand) |
| Prisdata | 1-minuts bars i TradingDB, børsens tid (exchange time) |
| Workspace | Fx 40-40-80 (Data1 = Data2 = 40 min, Data3 = 80 min) |
| Periode | IN 2019-2023. OOS 2024 er låst og kun tilgængelig for RSA's OOS-trin |

## Det, RSA måler

| Måling | Regel |
|---|---|
| Indgang | Åbningen af næste Data2-bar efter signal-baren (aldrig signal-barens egen pris) |
| Pris efter | Målt efter faste tider, samme tid for alle bar-længder. Alle tider testes |
| Enhed | Dollars + en kolonne for udsving (volatilitet) |
| Antal | Signaler i alt og antal dage med signal |
| Usikkerhed | Regnes pr. dag med signal (dagens signaler samles til ét tal) |
| MAE / MFE | Største modgang og medgang; vinduet starter på baren efter signal-baren |
| Varighed (AntalBars) | Kun beskrivende. Må aldrig vælge signaler (kendes først bagefter) |
| Udgangspunkt | "Alle bars". Lokkeduer og tilfældige tidspunkter testes begge |
| Ekstreme priser | Bruges som de er (fx −37 $ i april 2020) |

## Det, RSA dømmer på

**1. Retning**
- Filterets samlede resultat holdes op mod udgangspunktet, år for år.
- 4-5 af 5 år over = Long-edge. 4-5 af 5 år under = Short-edge. Ellers ingen edge.
- Retningen findes på IN-data og låses ved frys 1.

**2. Stabilitet over tid**
- Hvert af de 5 år sammenlignes (afvigelse i %). Antal signaler/dage pr. celle vises.

**3. Stabilitet over nabo-indstillinger (plateau)**
- Plateau-niveauer PL1-PL7 (3×3, 5×5, 7×7, 9×9 felter, grøn/grå/rød). PL2 er minimum.
- Filtre med kun én parameter: 3, 5, 7 eller 9 nabo-værdier.
- Kun plateauets midte går videre. Ligger midten på kanten, tages den også med
  (skal programmeres).
- Ingen særskilt kontrol for ens felter. Fejl skal vise sig senere.

**4. Prøveåret (OOS 2024)**
- Kun det, der har bestået 1-3, prøves på 2024. Én gang.
- Består, hvis resultatet i 2024 er mindst 60 % af IN-resultatet (må højst falde 40 %).
- Dumper det, er det kasseret for altid.

## Det, RSA ikke tester (hører til senere trin)

| Emne | Hvor |
|---|---|
| Omkostninger (kurtage, slippage) | Edge-Finder |
| Exit, stop, target, fredagsregel | Edge-Finder |
| "Gå ind, når signalet har været tændt i k bars" | Egen test; senere Edge-Cruncher |
| Flere signaler på én dag som bedre indgang | Edge-Finder |
| Opdeling efter markedsregime | Droppet |
| Kendte begivenheder (lagerrapport, rulledage) | Markeres ikke |

## Sideløbende test

Regnefejlen i seriefunktioner: MACD og RSI, StandardDev, XAverage, DMIplus,
DMIminus, ADX, ChaikinMoneyFlow testes på 2007-2009 med workspace 40-40-80.

## Stadig åbent

| Nr. | Spørgsmål |
|---|---|
| 18 | Hvilke tider "pris efter" måles på |
| 28 | Tælles alle resultater, så kravet strammes, jo mere der testes? |
| 29 | Hvor stor en del af det godkendte må være held (FDR)? |
| — | Hvor højt t-tallet skal være for at bestå (afhænger af 28 og 29) |
| 33 | Farvegrænserne grøn/grå/rød i PL1-PL7 |
| 23 | Minimum pr. celle (150 dage / 300 signaler er kun et testtal) |
| 22 | Overskud i forhold til samme klokkeslæt |
| 42 | Generalprøve før OOS |
