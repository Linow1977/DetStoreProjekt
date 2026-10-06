# Beslutningslog — RawSignal-projektet, 5.–6. oktober 2026

Opsummering af arbejdet 5. oktober (eftermiddag) og 6. oktober 2026 på den
lokale Claude Code-session på DataServer. **Er andre dokumenter uenige med
denne log, gælder denne log.** Det gælder også `BESLUTNINGSLOG_2026-10-05.md`,
hvad angår filternumre.

## Resultat

- **Seriefunktions-fejlen er løst.** Filtre med XAverage, RSI, MACD, DMI og ADX
  skrives nu ud på én kodelinje pr. kombination. Bevist mod prisdata: 100 %
  samme signaler.
- `filter_case` har nu **445 filtre, nummereret 1–445 uden huller**:
  312 fra EdgeFinder − 6 slettede (CoefTimeFrame) + 139 fra Alpha-filtrene.
- Ventetiden før en beregning regnes for færdig er sat ned fra 120 til 60 sek.
- Alt testdata er slettet igen ("rent bord"), så alle 445 filtre kan bygges
  og testes forfra.

## Seriefunktions-fejlen: årsag og løsning

**Årsag.** RawSignal-strategien kører alle kombinationer af N1/N2 i én løkke
på hver bar. Funktioner som XAverage husker deres egen forrige værdi, og
TradeStation giver hver *kodelinje* én hukommelse – ikke én pr. kombination.
Alle kombinationer delte derfor samme hukommelse. Under en almindelig
backtest eller optimering i TradeStation kører hver kombination som sin egen
backtest, og så opstår fejlen ikke. Derfor virker filtrene "under normale
forhold".

**Målt 05-10-2026** (CL 60-60-120, gamle numre i parentes for 06-10-numre):

| Funktion | Resultat i den gamle løkke |
|---|---|
| XAverage | Ramt – alle 25 kombinationer gav samme signaler |
| RSI, CountIf(RSI) | Ramt – 2 og 6 forskellige |
| MACD | Ramt – alle 625 ens |
| DMI | Ramt – 2 forskellige af 625 |
| ADX | Uafklaret – varierer, men mindre end forventet |
| ChaikinMoneyFlow, PercentR, HighD, LowD, Pivot, StandardDev, CCI | Virker |

**Løsning (Thomas valgte "løsning 1").** `formel.UDFOLD_FUNKTIONER` =
XAverage, RSI, MACD, DMIplus, DMIminus, ADX. Bruger formlen en af dem, skriver
`generer.py` formlen ud på én linje pr. kombination med faste tal, fx
`If C < xAverage(c, 2 * 1) ... Then Filter1[1] = 1 Else Filter1[1] = 0;`.
Hver linje får sin egen hukommelse. Løkken læser kun `Filter1[]`. Formlen
forbliver den originale.

**Bevis.** Testudgaver 054U (XAverage) og 078U (MACD) sammenlignet med en
uafhængig Python-beregning ud fra `public.prisdata` (60-min bars):
den nye udgave 100 % ens for alle testede N1/N2; den gamle løkke 0–16 %.
Alle 36 ramte filtre er derefter bygget og kørt: alle kombinationer gav
forskellige signaler, undtagen hvor formlen selv gør dem ens (fx
`floor(N2/2)` i MACD).

**Alternativet** – at køre de ramte filtre med TradeStations Optimize – blev
fravalgt, fordi det er meget langsommere og ikke passer ind i kæden.

## Ændringer i filter_case

| Hvad | Beslutning |
|---|---|
| Alpha-filtrene | `C:\Alpha_FIlter.txt` er Thomas' ældste originaler (1.117 cases med faste tal, 205 formel-typer). 139 nye typer tilføjet som nr. 307–445 med N1/N2 (1–25, faktor i formlen). 43 typer fandtes i forvejen, 14 var dubletter, 8 kan aldrig være sande. `Data(MyDataAF)` er skrevet som `of data(DataFilter_A)`. Se `Alpha_filter_forslag.xlsx` (skrivebordet). |
| Filter 67–72 (gl. nr.) | **Slettet.** `CoefTimeFrame` findes ikke i TradeStation, på nettet eller i nogen fil på serveren. Ingen original. |
| Omnummerering | Alle numre fra 73 rykket 6 ned (73 → 67 … 451 → 445). |
| MACD 67–78 | N2 = 2–24, trin 2 (før 1–25). `maxlist(2, floor(N2/2))` gav kun 11 forskellige værdier. N2 = 2 og 4 giver stadig det samme. |
| CountIf 87–88 | N2 = 1–5 (før 1–25). `CountIf(..., 5) >= N2` kan aldrig nå over 5. |
| 30, 31, 38, 39, 129, 130 | `Close > Highest(Close, N)` kunne aldrig være sand (den nuværende bar er med). Rettet til `Highest(...)[1]` / `Lowest(...)[1]` – sammenlign med de foregående bars. Fejlen var også i EdgeFinder-originalen. |
| Alpha 418–421, 428–429 | Blandede dags- og bar-værdier (`highD(1) > low[2]`). Rettet til dagsværdier: `lowD(...)`, `closeD(...)`. |

Sikkerhedskopier: `filter_case_backup_20261005_alpha` (før Alpha),
`_20261006` (før N2-ændring), `_20261006b` (før omnummerering),
`_20261006c` (før formelrettelser).

## Rettelser i programmet

| Fil | Ændring |
|---|---|
| `formel.py` | `UDFOLD_FUNKTIONER` og feltet `udfold` i analysen. |
| `generer.py` | `parameter_trin`, `udfoldede_linjer`; ny tekst i filens hoved; `MAALT_STATUS` med nye numre. |
| `rs_ts_cyklus.py` | Indlæsning læser CSV-overskriften (filtre med kun N1 har ingen N2-kolonne). 0 signaler gav "division by zero" – nu 0. `STILLE_SEK` 120 → 60. |

## Ventetiden (STILLE_SEK)

Programmet regner beregningen for færdig, når CSV-filen har stået stille i
`STILLE_SEK`. Målt 06-10-2026 med en måler, der så på filen hvert kvarte
sekund: den længste pause mellem to skrivninger midt i en beregning.

| Filter (06-10-nr.) | Tidsramme | Beregning | Længste pause |
|---|---|---|---|
| 48 DMI | 60-60-120 | 6 min | 8,0 sek |
| 50 DMI | 60-60-120 | 6 min | 4,8 sek |
| 14 StandardDev | 60-60-120 | 4 min | 1,3 sek |
| 52 ADX | 60-60-120 | 3 min | 8,6 sek |
| 58 XAverage | 60-60-120 | 30 sek | 0,8 sek |
| 61 CCI | 60-60-120 | 3 min | 5,8 sek |
| 50 DMI | 5-5-10 | 77 min | 7,6 sek |
| 14 StandardDev | 5-5-10 | 50 min | 1,3 sek |
| 61 CCI | 5-5-10 | 44 min | 6,0 sek |

Pausen vokser ikke med beregningstiden. Thomas besluttede **60 sek** (ca. 7×
margen). Sparer ca. 1 min pr. cyklus.

**Overslag** for alle 445 filtre på CL 60-60-120: ca. 20 timer
(ca. 2½ min fast pr. filter + beregning; 625-kombinationsfiltre ca. 6 min).

## Lært om TradeStation-styringen

- Efter genstart af TradeStation åbner Ctrl+C ikke kommandolinjen, før den
  er åbnet én gang i hånden.
- Minimeret fjernskrivebord giver "Kommandolinjen kunne ikke få fokus".
- Slettes strategierne i TradeStation, skal markeringen i `rawsignal`,
  `rawsignal_kontrol` og `filter_case.rawsignal_faerdig` også fjernes, ellers
  springer programmet dem over.

## "Rent bord"

Thomas' udtryk for, at alt er sat tilbage til udgangspunktet, klar til at
teste igen: ingen signaltabeller, `tidslog`, `rs_tf_runtime`, `rawsignal` og
`rawsignal_kontrol` tomme, ingen filtre markeret færdige, FilterFolder-mapperne
tomme, ingen RawSignal-strategier i TradeStation. `filter_case`,
sikkerhedskopier, `rawsignal_analyse`, prisdata og programmet bliver stående.
Status 06-10-2026: rent bord.

## Nye numre (06-10) for målte filtre

| Filter | Nr. 05-10 | Nr. 06-10 |
|---|---|---|
| MACD-gruppen | 73–84 | 67–78 |
| RSI | 85–88 | 79–82 |
| ChaikinMoneyFlow | 89–92 | 83–86 |
| CountIf(RSI) | 93–94 | 87–88 |
| RSI (Close[1]) | 95–98 | 89–92 |
| PercentR | 99–100 | 93–94 |
| CloseD (målt) | 175 | 169 |
| HighD / LowD | 179 / 180 | 173 / 174 |
| Pivot | 195 / 196 | 189 / 190 |

Under 67 er numrene uændrede. Parringslisten `RawSignal_EdgeFinder_parring.xlsx`
har en ny kolonne A med numrene fra 06-10.

## Næste skridt

- Byg og test alle 445 filtre på CL 60-60-120 (Alpha-filtrene er aldrig
  verificeret i TradeStation).
- Workspaces bruger kun 2007–09 (test). Den rigtige kørsel er 6 år.
