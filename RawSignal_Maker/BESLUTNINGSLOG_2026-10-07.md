# Beslutningslog — RawSignal-projektet, 6.–7. oktober 2026

Opsummering af arbejdet 6. oktober (eftermiddag/aften) og 7. oktober 2026 på
den lokale Claude Code-session på DataServer. **Er andre dokumenter uenige med
denne log, gælder denne log.** Filternumre i denne log er de nye numre fra
7. oktober, medmindre andet står.

## Resultat

- **Alle filtre er bygget og verificeret i TDE** (kun Verify, ingen backtest).
  440 af 445 blev godkendt i første forsøg, og de 5 fejlede er rettet eller kørt
  igen (se nedenfor).
- **Seriefunktions-advarslen var falsk alarm.** 24 filtre fra alle ikke-målte
  grupper er backtestet og målt. Ingen er ramt. Omskrivningen af MACD og DMI
  virker.
- `filter_case` har nu **447 filtre, nummereret 1–447 uden huller**. To nye
  TSI-filtre (grænse 1.4) ligger som 373–374, lige efter de andre TSI-filtre.
- Programmet genstarter TDE for hver 100 filtre, lukker TradeStations
  nedbrudsrapport og lægger TDE i nederste højre hjørne.
- Alt testdata er slettet igen ("rent bord").

## Kørslen af alle filtre i TDE (6. oktober, 16:37–19:50)

| Filter (nyt nr.) | Fejl | Rettelse |
|---|---|---|
| 359, 360 | `')' expected` – `of data(...)` stod efter MinList/MaxList/AbsValue | `of data(...)` flyttet ind til hver pris, fx `MinList(Close[N1] of data(A), Open[N1] of data(A))` |
| 371, 372 | `More inputs expected` – TSI fik kun 2 tal | `TSI(Close, Filter1_N1, 5 * Filter1_N2)`. Grænsen 1.6 er fastlagt af skaberen og bevares |
| (400) | Ingen fejl i formlen: TDE gik ned midt i kørslen | Kørt igen → godkendt |

Alle rettede formler er godkendt i TDE, før de blev skrevet i `filter_case`.

**TDE bliver langsommere for hvert filter:** 16 sek pr. filter ved filter 1,
20 sek ved ca. 62, 25 sek ved ca. 169, 30 sek ved ca. 267 og 42 sek lige før
nedbruddet ved filter 400. Efter genstart: 16 sek igen. Derfor genstarter
programmet nu TDE for hver 100 filtre (`tde_styring.GENSTART_EFTER`).

118 filtre fik Verify-advarslen *"A series function should not be called more
than once with a given set of parameters"*. Den er gemt i
`public.rawsignal.note`, men betyder ikke, at tallene er forkerte (se næste
afsnit).

## Måling af seriefunktionerne (6.–7. oktober)

Ét filter fra hver gruppe, der ikke var målt, backtestet på CL 60-60-120
(2007–09). For hver kombination af N1/N2 er signalrækken sammenlignet med de
andre. Fejlen ville give *præcis* samme signaler i (næsten) alle kombinationer,
som MACD gjorde før omskrivningen.

| Filter | Gruppe | Resultat |
|---|---|---|
| 332 / 333 / 434 | LowD / HighD / OpenD | Virker – alle 25 forskellige |
| 286 | High/LowSession | Virker – jævnt faldende antal signaler med N1 |
| 282 | Open/CloseSession | Virker, men tænder aldrig: CL åbnede aldrig over 1 % under forrige lukkekurs i 2007–09 (største: 0,91 %) |
| 137 / 138 | Highest / Lowest | Virker – 607/625 og 606/606 forskellige |
| 334 | HighestBar/LowestBar | Virker – 576/600 |
| 318 | CountIf | Virker – halveres for hvert trin i N1 |
| 363 | Momentum | Virker – 25/25 |
| 60 | CCI | Virker – 625/625 |
| 93 | PercentR | Virker – 25/25 |
| 191 | PivotLowVS | Virker – stiger med N1 og flader ud fra N1 = 8 (naturligt) |
| 189 | PivotHigh/LowVSBar | Virker – jævnt faldende med N1 |
| 381 | BollingerBand | Virker – 193/223 kombinationer med signaler |
| 379 | RateOfChange | Virker – 25/25 |
| 369 | MACD (omskrevet) | Virker – 600/600 |
| 50 | DMI (omskrevet) | Virker – 625/625 |
| 52 | ADX (omskrevet) | Virker – 405/440 |
| 58 / 313 | XAverage / XAverage(...)[1] (omskrevet) | Virker – 620/620 og 25/25 |
| 377 | RSI(CloseD(0), N1) | Virker – 548/589 |
| 87 | CountIf(RSI(...)) | Virker – 125/125 |
| 85 | Average(ChaikinMoneyFlow(...)) | Virker – 625/625, men tog 2 t 43 min |

Resultatet står også i filernes hoved (`generer.MAALT_STATUS`).

**Bifund:**
- Filter 87–88: N2 kan højst være 5 (tælling over 5 bars). Thomas har rettet
  N2 til 1–5.
- Filter 85 er meget tungt at regne (2 t 43 min mod normalt 2–5 min). Filtre
  med en seriefunktion inde i Average bliver flaskehalse i den store kørsel.
- Session-filtrene får et falsk signal på chartets første bar (30-04-2007,
  før forrige sessions værdier findes). Det ligger uden for analyseperioden.

## Omnummerering 7. oktober

| Filter | Før | Efter |
|---|---|---|
| 1–372 | uændret | uændret |
| Nye TSI > 1.4 / < 1.4 | (446 / 447) | **373 / 374** |
| Alle tidligere 373–445 | 373–445 | **375–447** (+2) |

Alpha-filtrene er nu 307–447. Sikkerhedskopi før omnummereringen:
`filter_case_backup_20261007`. Strategier i TradeStation med de gamle numre
skal slettes, før der bygges forfra.

## Programændringer

- `tde_styring.find_eller_aabn()`: lukker TradeStations nedbrudsrapport
  (`TSCrashReport.exe`, svarer til "Don't Send"), før TDE åbnes igen, og
  lægger TDE i nederste højre fjerdedel af skærmen.
- `tde_styring.genstart_efter_mange()`: genstarter TDE for hver 100 filtre.
  Tælleren står i `log\tde_taeller.txt` sammen med TDE's proces-id.
- `generer.MAALT_STATUS`: 24 nye målinger.
- `Desktop\Nulstil_testdata.bat` sletter nu alle signaltabeller i schema
  `rawsignal`, uanset nummer.

## Næste skridt

- Thomas sletter RawSignal-strategier og -ShowMe'er i TDE.
- Byg alle 447 filtre og kør backtesten.
- Workspaces bruger kun 2007–09 (test). Den rigtige kørsel er 6 år.
