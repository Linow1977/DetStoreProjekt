# 60 kritiske spørgsmål — Event Study og RawSignal-Analyse (RSA)

Første udgave 1. oktober 2026. **Opdateret 4. oktober 2026**, så det passer til,
hvor RSA-processen er nu.

Bygget på:
- Thomas' samling fra Claude Chat (`EventStudy_RawSignal_samling_med_datoer.txt`, status 1. okt)
- `main` i repoet (seneste commit 24. sep: RawSignal Creature)
- **arbejdsgrene, der ikke er flettet ind i `main`:**
  - `claude/new-session-y6p43z`: konsulentrapport v1-v3 (28. sep)
  - `claude/cool-einstein-4wxv9m`: konsulentopgaver, plateau-spørgsmål (28. sep)
  - `claude/dreamy-lamport-eztlk0`: konsulentgruppens rapport, laboratoriet K1-K3, VIDENSLOG-kategorien "RSA" (29.-30. sep)
  - `claude/detstorprojekt-sporgeskema-doqabk`: Thomas' svar på DetStoreProjekt-skemaet (1. okt)

Det, der er sket på serveren efter 1. oktober, er ikke med, fordi det ikke ligger i repoet.

**Status på hvert spørgsmål:**
- **Åben:** ikke besluttet nogen steder.
- **Bekræft:** der ligger en anbefaling eller beslutning, som skal bekræftes eller rettes.
- **Modstrid:** to kilder siger noget forskelligt, og det skal afgøres.
- **Ny:** nyt hul, fundet ved opdateringen 4. okt.

Spørgsmål 51-60 er skrevet fra en dataanalytikers og kvants synsvinkel og handler
om selve dataanalysen.

## Pipeline-kortet (positioner)

| Pos | Trin |
|---|---|
| P0 | Hele processen / arbejdsmåde |
| P1 | TradingDB: prisdata |
| P2 | RawSignal Maker (Creature): signalkode |
| P3 | Kørsel: backtest, indlæsning og kontrol af data |
| P4 | RSA: Event Study (måling, udgangspunkt, retning, statistik) |
| P5 | RSA: plateau og gate |
| P6 | Periodeopdeling: test / generalprøve / OOS / embargo |
| P7 | Code Creater, Edge-Finder/Cruncher, exit |

## Tidslinjen i korte træk (tid = udvikling)

- **10.–11. aug:** idé, fagnavn, plateau-princip, panelet.
- **13. sep:** signal-definitionen låses (overgang + varighed).
- **22.–24. sep:** Creature bygges og testes (det eneste i `main`).
- **24.–27. sep:** RSA-tabeller, look-ahead-fejl, retningsregel, RawSignal123 = Fail-kandidat.
- **28. sep:** konsulentrapport v1-v3, plateau-trappen PL1-PL7, Det Runde Bords afgørelser.
- **29. sep:** fokus flyttet fra filtre til analyse (MACD-sporet droppet); konsulentgruppens
  rapport og laboratoriet; periodeopdeling 2020-2024 / 2025 / 2026.
- **1. okt:** Thomas besvarer DetStoreProjekt-skemaet (300 spørgsmål).

---

## P0 — Hele processen og arbejdsmåden

**1. Skal de fire arbejdsgrene flettes ind i `main`, før der bygges mere RSA?**
Position P0 · Dato: 28. sep–1. okt · Status: Ny
Konsulentrapporterne, laboratoriet, VIDENSLOG-kategorien "RSA" og dine skemasvar ligger
på grene, som ingen ny session ser automatisk. Uden én fælles sandhed bygger den lokale
session og cloud-sessionen på forskellige grundlag.

**2. Hvad er status på serveren lige nu?**
Position P0/P4 · Dato: 27. sep → 4. okt · Status: Åben
De 9 tabeller i `rawsignal_analyse` og kørslerne af RawSignal123, 002 og 169 findes kun på
serveren. Er der kørt eller bygget mere siden 29. sep? Skal der laves en kort statuslog fra
den lokale session, der pushes til repoet?

**3. Er RawSignal123, 002 og 169 gamle eller nye filternumre?**
Position P0/P4 · Dato: 24. sep (omnummerering) mod 24.–27. sep (kørsler) · Status: Åben
Kørslerne lå samme dage som omnummereringen. "RawSignal002 (625 kombinationer)" ligner det
nye filter 1 (AvgTrueRange, 625 kombinationer).

**4. Regelfilen: kun du godkender nye versioner, og alt køres forfra ved ændring?**
Position P0/P4 · Dato: 29. sep (K2-14 punkt 9) · Status: Bekræft
Rapporten foreslår, at alle grænser står i én regelfil med versionsnummer. Skal hver
resultatrække i RSA stemples med regelfil-version, kode-version og RunID?

**5. Hvordan holdes styr på beslutninger, der blev taget efter at have set data?**
Position P0/P4 · Dato: 24.→27. sep · Status: Åben
Retningsreglen blev ændret, efter at RawSignal123's resultater på 2019-2023 var set, og den
periode overlapper testperioden. Skal der føres en log over, hvilke metodevalg der er
truffet efter at have set hvilke data, så de tælles med som forsøg?

## P1 — Prisdata

**6. Hvilken tidszone og hvilken tidsstempling bruger signalfilen og prisdata?**
Position P1 · Dato: 1. okt (dit svar 63: "ikke relevant") mod 29. sep (rapportens beslutning 4) · Status: Modstrid
Signalerne joines med 1-minuts priser. TradeStation stempler en bar med dens sluttid. Hvis
de to kilder bruger forskellig tidszone eller stempling, kigges der ind i fremtiden ved hver
join, og dagsgrænsen "midnat til midnat" flytter sig. Rapporten sætter tidszone og session
som en af dine fem første beslutninger.

**7. Rulleregel og justering: stemmer de 1-minuts priser med TradeStations kontinuerlige kontrakt?**
Position P1 · Dato: 24.–25. sep og 1. okt (svar 62) · Status: Åben
99,98 % ens tidspunkter siger intet om ens priser. Er OHLC tjekket omkring rulledatoerne,
og hvad er de 0,02 %?

**8. Er 2025 og 2026 låst, så programmerne ikke kan læse dem?**
Position P1/P6 · Dato: 29. sep · Status: Bekræft
Programmerne logger på som superbrugeren `postgres`, så ingen lås virker. Rapporten anbefaler
egne roller pr. program. Er det besluttet, og ligger 2025-data i databasen endnu?

**9. Opvarmning pr. datastrøm: hvor tidligt skal kørslerne starte for de 52 filtre med Data3?**
Position P1/P2 · Dato: 29. sep (kvalitetskontrollen F-3) · Status: Åben
Max Bars Back = 1000 bars skal dækkes for både Data2 og den større Data3. Det kan flytte
starten et eller flere år tilbage og skal måles i prøvekørslen.

**10. Hvordan håndteres negative og ekstreme priser i dataene?**
Position P1/P4 · Dato: 24.–25. sep · Status: Ny
Olie handlede til −37 $ den 20. april 2020. Med additiv bagudjustering kan ældre priser blive
meget små eller negative, så procent-afkast mister mening. Skal den dag og rulledagene
markeres eller udelukkes?

## P2 — RawSignal Maker

**11. Vejen for de op til 196 filtre med regnefejlen: kør først de 184 sikre?**
Position P2 · Dato: 29. sep (din første beslutning i rapportens 4.6) · Status: Bekræft
MACD-sporet er droppet. Betyder det, at de 196 er droppet, eller kun udskudt? Rapporten
anbefaler at køre de 184 sikre filtre først (184 × 12 = 2.208 kørsler).

**12. Skal signalerne efterprøves i Python bar for bar mod en uafhængig beregning?**
Position P2/P3 · Dato: 28. sep (åben tråd) · Status: Åben
"Forskellige signalrækker" beviser ikke rigtige tal, for forkerte tal kan også være
forskellige. Skal TA-Lib eller egen kode bruges som facit på en stikprøve?

**13. Fast filter-ID med fingeraftryk?**
Position P2 · Dato: 29. sep (K3-18 punkt 7) · Status: Bekræft
`filter_case_id` er et løbenummer, der allerede er flyttet én gang. Et fingeraftryk af
formlen sikrer, at et resultat altid peger på præcis den formel, der lavede det.

## P3 — Kørsel og indlæsning

**14. Er hullet med bar-længden lukket, før den fulde kørsel?**
Position P3 · Dato: 28.–29. sep · Status: Åben
`indlaes_csv.py` sletter hele `rawsignal<nr>`-tabellen, og RunID indeholder hverken
bar-længde eller marked. Kører samme filter på 12 bar-længder, overlever kun den sidste.

**15. Er prøvekørslen lavet: 3-5 filtre × 12 bar-længder, inkl. RawSignal069?**
Position P3 · Dato: 29. sep (K2-14 punkt 6) · Status: Åben
Den giver de tal, der mangler for at planlægge: kørselstid pr. backtest, filstørrelse og
opvarmning.

**16. Hvem kører selve backtesten, der giver RSA sine signaler?**
Position P3 · Dato: 27. sep mod 28. sep og 1. okt (svar 123) · Status: Modstrid
Den 27. kørte EdgeFinder backtesten før RSA. Den 28. ligger Edge-Finder efter Code Creater.
Den 1. okt svarede du, at workspace-indstillinger "ikke er Edge-Finders opgave". Hvilket
program henter signalerne ud af TradeStation?

## P4 — RSA: målingen

**17. Er "tidligst minuttet efter signal-barens lukning" brugt i alle RSA-tabeller?**
Position P4 · Dato: 25. sep (`mae_mfe` rettet) og 29. sep (konsulenterne enige) · Status: Bekræft
Look-ahead-fejlen blev rettet i `mae_mfe`. Er samme regel brugt i `prisefter`,
`fordeling_horisont` og `varighed_bevaegelse`, og findes der en automatisk test, der fanger
det?

**18. Hvilke højst 3 horisonter, og er de låst, før data ses?**
Position P4 · Dato: 24. sep (3/5/10/15 bars) mod 29. sep (K1-P 2: højst 3) og 1. okt (svar 114: ved ikke) · Status: Åben
Hver ekstra horisont er et ekstra forsøg. Skal horisonten måles i bars eller i minutter, så
bar-længderne kan sammenlignes?

**19. Tabellen `varighed_bevaegelse`: slettes den, eller mærkes den "kun beskrivende"?**
Position P4 · Dato: 29. sep (afgjort: AntalBars må aldrig vælge signaler) · Status: Bekræft
Varigheden kendes først, når signalet slukker. Tabellen må derfor aldrig indgå i dommen.

**20. Klumpning: hører optælling pr. handelsdag til i RSA eller i Edge-Finder/CC?**
Position P4 · Dato: 29. sep (rapporten: RSA) mod 1. okt (svar 120: Edge-Finder/CC) · Status: Modstrid
Tæller RSA signaler i stedet for dage, bliver t-tallene 1,4-4,6 gange for store (forsøg f1).
Så dømmer RSA på oppustede tal, uanset hvad Edge-Finder gør bagefter.

**21. Omkostningsmargin: 2 × eller 3 × omkostningen, og allerede i RSA?**
Position P4 · Dato: 29. sep (rapporten: 2 ×) mod 1. okt (svar 159: 3 ×, svar 128: Pharos) · Status: Modstrid
Er grænsen 2 × eller 3 × omkostningen? Og skal den gælde allerede i RSA, eller først hos
Pharos? Hvilken tick-værdi, kommission og slippage bruges for CL?

**22. Overskud i forhold til samme klokkeslæt?**
Position P4 · Dato: 24.–27. sep (ikke besluttet) og 29. sep (K1-P 15) · Status: Bekræft
Forsøg f11: med morgen-opdrift i markedet gav rå tal 12 % falske med t > 2. Målt som overskud
over det, der normalt sker på samme klokkeslæt, var det 1 %. Skal det være standard?

**23. Minimum pr. celle: 150 handelsdage og 300 signaler?**
Position P4/P5 · Dato: 27. sep (åben) og 29. sep (rapportens del 1, E) · Status: Bekræft
RawSignal123 blev kaldt "Fail", før tærsklen var besluttet. Er den dom foreløbig?

**24. Ekstreme dage: hvordan fanges et resultat, der bæres af få dage?**
Position P4 · Dato: 1. okt (svar 161: år for år) og 29. sep (forsøg f6/f7) · Status: Åben
Skæve dagsresultater kan få ren støj til at nå t ≥ 4 op til 115 gange oftere end forventet (ved mild skævhed 2-14 gange), og
stabilitetskravet B5 fanger dem ikke. Rapporten foreslår lokkeduer med samme stop/target.
Er år for år nok?

## P4 — RSA: udgangspunktet

**25. Lokkeduer i stedet for tilfældige tidspunkter: bekræftet?**
Position P4 · Dato: 11. aug (panelet) mod 29. sep (rapporten, forsøg f1/f10) · Status: Bekræft
Tilfældige tidspunkter lod 9,6 % falske igennem i stedet for 1 %. Lokkeduer flytter hele
signalserien 4-26 kalenderuger. Hvor mange runder (20-50)?

**26. Hvad skiller en stabil edge fra stabil tilfældighed?**
Position P4/P5 · Dato: 27. sep (udgangspunkt ikke blokerende) og 29. sep (4.3 nr. 9) · Status: Åben
Den nye værdi-stabilitetstest på de 8 naboer koster ingen ægte edges, men fjerner heller ingen
falske. Hvis udgangspunktet ikke er blokerende, hvad stopper så et filter, der stabilt gør det
samme som markedet?

**27. Retningen: findes den på testdata og låses ved frys 1?**
Position P4 · Dato: 27. sep (retningsregel) og 29. sep (familie = filter × retning) · Status: Bekræft
Den 27. sep blev udgangspunktet både brugt til at finde retning og kaldt "ikke blokerende".
Rapporten gør filter × retning til én familie. Gælder 4-5-år-reglen stadig?

## P4 — RSA: statistik

**28. Hvor mange forsøg laves der: "én backtest pr. workspace" eller 1,8-6 mio. celler?**
Position P4 · Dato: 1. okt (svar 152) mod 28.–29. sep (rapporterne) · Status: Modstrid
Antallet af forsøg bestemmer, hvor hårdt kravet skal være (t ≈ 4,65 ved millioner). En
backtest med 625 kombinationer × 2 retninger × 3 horisonter er 3.750 forsøg, ikke ét.

**29. Grænse for falske fund (FDR) 10 %, og hvad betyder "under 5 % består"?**
Position P4 · Dato: 29. sep (K1-P 3) og 1. okt (svar 134) · Status: Bekræft
5 % af 1,8 mio. celler er 90.000. Er dine 5 % pr. filter, pr. celle eller pr. familie?

**30. Hvad skal år for år bruges til, når det næsten ikke fanger falske?**
Position P4 · Dato: 27. sep (4-5 af 5 år) og 29. sep (forsøg f9) · Status: Åben
Falske med t ≥ 4 består stabilitetskravet B5 i 92 % af tilfældene. Det er t-kravet, der gør
arbejdet. Er år for år en dom, eller kun en advarsel? Og bedste år højst 40 % eller 50 %?

**31. Regimer: er panelets krav om opdeling efter markedsregime bevidst droppet?**
Position P4 · Dato: 11. aug (panelets punkt 2) mod 1. okt (svar 122: nej) · Status: Modstrid
Volatilitets-opdelingen blev udskudt 24. sep, og du svarede nej til markedstyper. Er
kalenderår nu det eneste regime-tjek?

**32. Accepterer du, at maskinen kun kan finde meget stærke edges på ét marked?**
Position P4 · Dato: 28. sep (rapport v3) · Status: Ny
Med 5 års data kan der ærligt kun findes edges med årlig Sharpe på ca. 2,3-2,5 pr. marked, men
ca. 1,6 på 6 markeder. Skal flere markeder ind tidligt, eller accepteres grænsen?

## P5 — Plateau og gate

**33. Farvegrænserne i PL1-PL7: låses de, før 002 og 169 ses?**
Position P5 · Dato: 28. sep (åbent punkt) · Status: Åben
Hvorfor tillader PL6 20 % røde felter, mens PL2 og PL4 kræver 0 %? Sættes grænserne efter
at have set resultaterne, kan man ubevidst vælge dem, så det ønskede filter består.

**34. Er PL2 som minimum meningsfuldt, når nabo-celler næsten er ens?**
Position P5 · Dato: 28. sep og 29. sep (forsøg f3/f10/f12) · Status: Ny
Rigtige filtre har en nabo-korrelation på ca. 0,93. Ved den korrelation når ren støj PL1 i ca.
35 % af gitrene. Ægte smalle edges (3 celler) når sjældent PL5. Skal plateau-niveauet styre
prioritering, mens t-kravet styrer dommen?

**35. Kontrol for identiske celler på alle filtre?**
Position P5 · Dato: 29. sep (forsøg f13) · Status: Bekræft
Et gitter ramt af regnefejlen når automatisk PL7. Ved overlap ≥ 0,99 erklæres gitteret
ugyldigt.

**36. Hvad er plateau for filtre med kun N1, med decimaltal eller uden parametre (76 filtre)?**
Position P5 · Dato: 28. sep · Status: Åben
3×3 til 9×9 kræver to akser. RawSignal123 havde kun N1.

**37. Skal nabo-afstanden måles i procent i stedet for trin?**
Position P5 · Dato: 11. aug / 28. sep · Status: Åben
Et trin på 1 i en periode på 3 er en stor ændring, i en periode på 200 næsten ingen.

**38. Kun plateauets midte går videre: bekræftet?**
Position P5 · Dato: 28. sep og 29. sep (forsøg f8) · Status: Bekræft
Midten holdt bedre i OOS end cellen med højest t (81 % mod 76 % ved bredde 5). Hvad hvis
midten ligger på kanten af gitteret?

**39. Endeligt dødt, også ved en bevist maskinfejl?**
Position P5 · Dato: 17. sep og 28. sep (Det Runde Bord) og 29. sep (4.3 nr. 4) · Status: Åben
Look-ahead-fejlen den 25. sep viser, at metoden kan fejle. Rapporten: kun med dit ja, kun på
data efter 2026 og med ny embargo. Accepterer du den undtagelse?

## P6 — Periodeopdeling

**40. Tolerance i 2025: z = 1,28, z = 1,0 eller fast 20 %?**
Position P6 · Dato: 29. sep (beslutningsark 6) · Status: Bekræft
z = 1,28 beholder ca. 80 % af de ægte edges og 26 % af de falske. Fast 20 % beholder ca. 55 % af
de ægte og 6 % af de falske. Hvilken fejl er værst for dig: at miste ægte eller at beholde falske?

**41. OOS-længden: 1 år (2025) eller 1-2 år?**
Position P6 · Dato: 29. sep (2025) mod 1. okt (svar 153/168: 1-2 år efter mindst 3-5 års test) · Status: Modstrid
Ét års OOS er meget kort for en dagshandels-edge. Hvilken regel gælder?

**42. Generalprøve: 2020-2023 → 2024 med 16 opsætninger skrevet ned på forhånd?**
Position P6 · Dato: 29. sep (K1-P 5) · Status: Bekræft
Den afprøver hele maskinen én gang, før det ægte prøveår bruges.

**43. Skal RawSignal123 køres om på 2020-2024?**
Position P6 · Dato: 24.–27. sep (2019-2023) mod 29. sep (testdata 2020-2024) · Status: Åben
Ellers er den første dom ikke lavet på samme grundlag som de næste.

**44. Hvordan undgår du selv at se 2025-2026 i TradeStation-charts?**
Position P6 · Dato: 29. sep (K3-18 punkt 17) · Status: Ny
Rapporten: ingen grafer fra 2025-2026, før porten åbnes. Men et almindeligt chart i
TradeStation viser alt til i dag. Hvordan låses det i praksis?

**45. 2026-embargoen: fast slutdato, buffer og hvad med sene familier?**
Position P6 · Dato: 29. sep · Status: Åben
Året er ikke slut. Rapporten foreslår 1-2 ugers buffer mellem både 2024/2025 og 2025/2026, og at
sene familier venter på data efter 2026. Erstatter 2026 de 6 måneders inkubation?

## P7 — Efter RSA

**46. Hvilken exit bruger Code Creater, og hvordan undgås en ny optimering på testdata?**
Position P7 · Dato: 28. sep og 29. sep (opgavens åbne punkt 7) · Status: Åben
Exit vælges kun på 2020-2024, fra et plateau af gode exits. 2026 bliver den eneste rene prøve
af hele strategien. Er det accepteret?

**47. Én position ad gangen og forsigtige fyldregler?**
Position P7 · Dato: 29. sep (K2-14 punkt 1 og 4) · Status: Bekræft
RSA måler alle signaler, men en strategi kan kun have én position. Det ændrer, hvilke signaler
der reelt handles.

**48. Fredags-reglen: tæller signaler lige før fredagslukket?**
Position P4/P7 · Dato: 29. sep · Status: Åben
En "10 bars"-måling fredag eftermiddag kan ende mandag, hvis den ikke stoppes ved lukning.

**49. Skal RSA-resultater genberegnes på MultiCharts-data før brug hos prop-firmaer?**
Position P7 · Dato: 1. okt (svar 64: TS og MC giver ikke samme bars) · Status: Ny
Når bars er forskellige, er signalerne også forskellige.

**50. Skal RSA kalibreres på ægte CL-priser med en plantet edge?**
Position P4/P5 · Dato: 29. sep (laboratoriet brugte kun opdigtede data) · Status: Ny
Laboratoriet viser, at metoderne virker på opdigtede data. Et kunstigt filter med en kendt,
lille edge plantet i rigtige CL-priser og et rent lokkedue-filter viser, at hele kæden finder
det ene og afviser det andet på de rigtige data.

---

## Ekstra: dataanalyse set med en kvants øjne (51-60)

**51. Hvordan ser fordelingen af "pris efter" ud?**
Position P4 · Dato: 24. sep (målingerne) og 29. sep (forsøg f6) · Status: Ny
Er der lavet histogram, skævhed og kurtosis (hvor tunge halerne er) af afkastet efter signal
pr. horisont, pr. år og for alle bars? t-tallet forudsætter en nogenlunde pæn fordeling.
Venstreskæve fordelinger narrer t op til 115 gange. Uden et kig på fordelingen ved man ikke,
om t-testen er gyldig for CL.

**52. Skal afkast måles i volatilitets-enheder i stedet for dollars?**
Position P4 · Dato: 24.–25. sep (additiv justering) · Status: Ny
CL's dagsudsving gik fra ca. 1 $ (2019) til over 10 $ (2020 og 2022). Et dollar-gennemsnit
domineres af de urolige perioder. Afkast divideret med ATR eller realiseret volatilitet ved
signalet gør årene sammenlignelige. Skal begge vises, og hvilken dømmes der på?

**53. Hvilken metode giver standardfejlen, når horisonterne overlapper?**
Position P4 · Dato: 29. sep (f1 og PF2) · Status: Ny
Dags-klyngede standardfejl, Newey-West (en rettelse for afkast, der hænger sammen over tid)
eller block bootstrap (genudtræk af hele blokke af dage)? Hvilken blokstørrelse? Valget
ændrer t-tallet, så det skal stå i regelfilen.

**54. Hvad er den kalibrerede tærskel T\* for CL efter lokkeduerne?**
Position P4 · Dato: 28.–29. sep · Status: Ny
Teorien siger t ≈ 4,65 ved millioner af forsøg. Men nabo-cellerne hænger sammen (korrelation
ca. 0,93), så det effektive antal uafhængige forsøg er langt lavere. Skal T\* sættes empirisk
fra lokkeduerne på de rigtige CL-data, og hvor mange lokkeduer skal der til for et stabilt tal?

**55. Skal hele forfaldskurven vises (alpha decay)?**
Position P4 · Dato: 10. aug (fagbegreber) og 29. sep (højst 3 horisonter) · Status: Ny
Dommen sker på højst 3 låste horisonter. Men kurven af gennemsnitligt afkast fra 1 til 60 bars
efter signalet viser, hvornår edgen topper og dør. Den kan være det bedste grundlag for
tids-exit. Skal den vises som beskrivelse, uden at den indgår i dommen?

**56. Skal kendte begivenheder markeres i dataene?**
Position P4 · Dato: 1. okt (svar 71: andre data ved ikke) · Status: Ny
CL har den ugentlige lagerrapport onsdag 10:30 New York-tid, rulledage og helligdage med kort
handel. Klumper signalerne sig omkring dem, kan en "edge" bare være en kalendereffekt. Skal de
dage markeres og vises som egne celler, selvom systemet kun bruger prisdata?

**57. Hvor ens er de 380 filtres signaler indbyrdes?**
Position P4/P5 · Dato: 29. sep (tvilling-grænse 0,8) · Status: Ny
Mange filtre bygger på de samme indikatorer og tænder på de samme tidspunkter. Overlap mellem
filtrenes signaldage (Jaccard-tal) viser, hvor mange reelt forskellige familier der er. Måles
tvilling-grænsen på signaltidspunkter eller på afkast?

**58. Findes der en datakvalitetsrapport, før RSA kører?**
Position P1 · Dato: 1. okt (svar 61, 66, 72, 75: ved ikke) · Status: Ny
Antal manglende minutter pr. dag og pr. år, bars med nul volumen, prisspring og dubletter.
Huller i 1-minuts data giver forkerte "pris efter"-tal, der ligner edge eller skjuler den.

**59. Hvad er den mindste edge, RSA overhovedet kan opdage?**
Position P4 · Dato: 28. sep (rapport v3) · Status: Ny
En styrkeberegning (power): med ca. 1.250 handelsdage, CL's typiske udsving og t ≥ 4,65, hvor
mange ticks pr. signal skal edgen mindst være? Er det tal større end realistiske edges, er det
bedre at ændre designet (flere markeder, samle bar-længder) end at køre 2.208 backtests.

**60. Skal plateauet være en statistisk model i stedet for farvetælling?**
Position P5 · Dato: 28. sep (PL1-PL7) · Status: Ny
I stedet for at dømme hver celle for sig og tælle grønne felter kan man estimere edgen med
"shrinkage" (hvor hver celles tal trækkes mod gennemsnittet af naboerne og bar-længderne).
Det giver ét tal med usikkerhed pr. område og bruger naboernes information direkte. Skal det
afprøves i laboratoriet mod PL-trappen?

---

## De vigtigste at tage først (min vurdering)

1. **Nr. 1 og 2:** én fælles sandhed og status fra serveren.
2. **Modstridene: nr. 20, 21, 28 og 41.** De ændrer selve dommen i RSA.
3. **Nr. 14 og 8:** bar-længde-hullet og superbrugeren skal lukkes før den fulde kørsel.
4. **Nr. 59 og 32:** kan maskinen overhovedet se de edges, vi leder efter?
5. **Nr. 50:** kalibrering med en plantet edge i ægte CL-data.
