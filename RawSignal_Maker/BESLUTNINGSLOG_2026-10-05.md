# Beslutningslog — RawSignal-projektet, 5. oktober 2026

Opsummering af dagens arbejde på den lokale Claude Code-session på
DataServer. **Er andre dokumenter uenige med denne log, gælder denne log.**
Det gælder også `BESLUTNINGSLOG_2026-09-24.md`, hvad angår filternumre.

## Resultat

- `filter_case` er sammenlignet med de originale EdgeFinder-filer og bygget op
  på ny. Den har nu **312 filtre, nummereret 1–312 uden huller** (før: 380).
- Alt gammelt testdata er slettet, så RawSignal-kørslerne starter forfra.
- Parringslisten `RawSignal_EdgeFinder_parring.xlsx` (skrivebordet på
  DataServer) viser for hvert RawSignal-nummer den eller de EdgeFinder-filer,
  formlen kommer fra, begge formler, seriefunktion og hvad der er rettet.

## Originalerne

De originale filtre ligger i
`OneDrive\RD-Python\EdgeFinder_Easylanguage_Filer\EdgeFinder_Files\EdgeFinder_Files\`
som `@EdgeFinder_F1.txt` … `@EdgeFinder_F250.txt`. Hver fil har én
Long-betingelse og én Short-betingelse. **EdgeFinder-filerne er facit.** En
RawSignal skal give præcis samme handelsbetingelse som sin original.

Numrene i `filter_case` fulgte ikke filnumrene (fra fil 17 og frem var de
forskudt), så sammenligningen blev lavet på selve formlen, ikke på nummeret.

## Thomas' regler for filter_case

| Regel | Hvorfor |
|---|---|
| Er Long og Short forskellige i originalen, laves to RawSignal-filtre. Er de ens, laves ét. | Hver betingelse skal testes for sig. |
| Bruger formlen kun én parameter, hedder den altid `Filter1_N1`, aldrig `Filter1_N2`. | N står for nummer. Er der kun ét, er det nummer 1. |
| Står den samme formel flere gange, beholdes kun én. | Samme formel giver samme resultat. |
| Numrene går 1, 2, 3 … uden huller, sorteret efter EdgeFinder-filnummer. | Så filtre af samme type ligger samlet (Volatility, Trend, Pullback, Price Action, Volume, Tick, Session, Unger). |
| Filtre uden original beholdes. | CCI-filtrene med `highest/lowest` og `TrueRange A > Average(TrueRange A) × N2` kan give en edge, vi ikke kendte. |

## Rettelser i forhold til originalen

| Nyt nr. | Gammelt nr. | Original | Rettelse |
|---|---|---|---|
| 212 | 162, 164 | F158, F159/F160 | `<` rettet til `>`. Rettet 164 blev ens med 163 og er slettet som dublet. |
| 230, 231 | 181, 182 | F177, F178 | Manglende parentes sat ind: `a × (max − min)` i stedet for `(a × max) − min` |
| 41, 42 | 309, 310 | F33 | `Open[1]` rettet til `Close[1]` |
| 247, 248 | 203, 204 | F197, F198 | Originalen har to uafhængige parametre. RawSignal brugte N1 begge steder. N2 tilføjet (1–25, trin 1). |
| 53 filtre | — | — | Kun én parameter: `Filter1_N2` omdøbt til `Filter1_N1`, og intervallet flyttet med. |

Kolonnen "Rettelse" i parringslisten viser, hvilke filtre der er rettet.

Antal: 68 dubletter slettet, 58 filtre rettet. Alle betingelser i de 250
originaler findes nu som RawSignal. Kun 7 filtre er uden original (6 CCI og
TrueRange A `>`).

## Ændringer i TradingDB

| Hvad | Beslutning |
|---|---|
| `filter_case` | Indholdet erstattet med de 312 nye filtre. `gammel_case` beholdt som historik. `rawsignal_faerdig` er tom for alle. Sikkerhedskopi af de 380 gamle: `filter_case_backup_20261005`. |
| `rawsignal.rawsignal002`, `002_test`, `030`, `123`, `169` | Slettet. |
| `public.rawsignal`, `public.rawsignal_kontrol` | Tømt. |
| `rawsignal.tidslog`, `rawsignal.rs_tf_runtime` | Tømt (kun testmålinger af RawSignal002-Test). |
| `rawsignal_analyse.*` | Rækker for RawSignal002, 123 og 169 slettet. `udgangspunkt` og "Alle bars"-rækkerne i `startpris_forskel` er beholdt, fordi de kun bygger på prisdata. |
| Filer i `C:\TradingDB_Folder\FilterFolder` | `.el`, `.txt` og `.csv` for 002, 030, 123 og 169 slettet. Thomas sletter strategierne i TradeStation. |

Kørt af `Nulstil_filter_case.bat` (skrivebordet) med
`C:\TradingDB_Folder\Nulstil_filter_case_20261005.sql`, i én transaktion.

## Nye numre for de målte filtre

**OBS numre:** Alle filternumre i dokumenter fra før 5. oktober er GAMLE
numre. De kan ikke regnes om med en formel; slå op i parringslisten eller
sammenlign formlen med `filter_case_backup_20261005`.

| Filter | Gammelt nr. (24-09) | Nyt nr. | Målt for seriefunktions-fejlen |
|---|---|---|---|
| AvgTrueRange | 1 | 1 | Virker |
| Average (gamle RawSignal266) | 265 | 24 | Virker sandsynligvis |
| DMI | 30 | 50 | Ramt |
| MACD (gamle RawSignal069) | 68 | 78 | Ramt |
| CloseD | 123 | 175 | Virker |
| Highest | 169 | 218 | Ikke målt for fejlen |

`MAALT_STATUS` i `Program/generer.py` er rettet til de nye numre.

## Næste skridt

- Seriefunktions-fejlen skal testes: RawSignal-filen og den tilhørende
  EdgeFinder-fil køres begge, og resultaterne sammenlignes, for at se om
  fejlen er i begge. Parringslisten bruges til at finde parrene.
