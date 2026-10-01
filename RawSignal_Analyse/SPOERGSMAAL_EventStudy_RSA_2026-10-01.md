# 50 kritiske spørgsmål — Event Study og RawSignal-Analyse (RSA)

Skrevet 1. oktober 2026 ud fra:
- Thomas' samling fra Claude Chat (`EventStudy_RawSignal_samling_med_datoer.txt`, status 1. okt)
- det der ligger i repoet (seneste commit 24. sep: RawSignal Creature, beslutningslog 24. sep, VIDENSLOG)

**Formål:** at gøre analyserne, metoderne og hele processen bedre. Spørgsmålene er
bevidst kritiske. Ingen af dem er besvaret her — de skal besvares af Thomas
(evt. med Det Runde Bord eller den lokale session).

**Sådan læses de:** hvert spørgsmål har
- **Position** i pipelinen (se kortet nedenfor)
- **Dato** = hvornår det, spørgsmålet handler om, sidst blev sagt/besluttet
- en kort forklaring på, *hvorfor* det er vigtigt

## Pipeline-kortet (positioner)

| Pos | Trin | Status i repo pr. 1. okt |
|---|---|---|
| P0 | Hele processen / arbejdsmåde | VIDENSLOG har ingen poster efter 24. sep |
| P1 | TradingDB: prisdata | Ikke i repo |
| P2 | RawSignal Maker (Creature): signalkode | **I repo** (`RawSignal_Creature/Program/`) |
| P3 | EdgeFinder: kørsel af backtest, hent og tjek data | Ikke i repo (kategori i VIDENSLOG er tom) |
| P4 | RSA: Event Study (signal, udgangspunkt, retning, statistik) | **Ikke i repo** — kun i TradingDB/lokal session |
| P5 | RSA: Plateau, gate og scoring | Ikke i repo |
| P6 | Periodeopdeling: test / OOS / embargo | Ikke i repo |
| P7 | Code Creater, EdgeCruncher, stop/target | Ikke i repo |
| P8 | Strategy Incubator / Pharos | Ikke i repo |

## Tidslinjen i korte træk (tid = udvikling)

- **10.–11. aug:** idé, fagnavn, plateau-princip, panelet. Derefter ~1 måned næsten stille.
- **13. sep:** signal-definitionen låses (overgang + varighed).
- **22.–24. sep:** Creature bygges og testes (det eneste der ligger i repo).
- **24.–29. sep:** RSA-tabeller, look-ahead-fejl, retningsregel afvist og ny lavet,
  flowet tegnet om, periodeopdeling, plateau-niveauer — **meget besluttet på 6 dage,
  intet af det er i repo.**

---

## P0 — Hele processen og arbejdsmåden

**1. Hvorfor ligger intet af RSA-arbejdet (24.–29. sep) i repoet?**
Position P0/P4 · Dato: 18. sep (VIDENSLOG-reglen) mod 24.–29. sep.
VIDENSLOG siger selv (18. sep), at sessionerne *kun* deler det, der lægges i git.
I dag kan ingen anden session se RSA-koden, de 9 tabeller, look-ahead-rettelsen eller
retningsreglen. Skal der være en fast regel om, at en beslutningslog pushes samme dag?

**2. Samlingen fra 1. okt indeholder forældede punkter — hvem rydder op?**
P0 · 23. sep mod 24. sep.
Samlingen siger (23. sep), at et signal der er tændt ved slutningen *ignoreres*. Repoet
(24. sep) siger det modsatte: det *skrives* med `Afsluttet = 0`. Den seneste dato vinder
— men samlingen er ikke rettet. Hvor mange andre punkter i samlingen er forældede?

**3. Modsigelsen om Data1/Data2 står stadig som "åben" — men den er løst i koden.**
P0/P2 · 23. sep mod 24. sep.
Koden stopper med en fejl (`RaiseRunTimeError`), hvis Data1 ikke har samme tidsramme som
Data2. Er det den endelige beslutning? Så skal punktet lukkes i samlingen.

**4. Filternumrene blev flyttet ét ned den 24. sep. Er RawSignal123, 002 og 169 gamle eller nye numre?**
P0/P4 · 24. sep (omnummerering) mod 24.–27. sep (testkørsler).
Kørslerne lå samme dage som omnummereringen. Blev "RawSignal123" analyseret med det
rigtige filter? Og "RawSignal002 (625 kombinationer)" ligner det *nye* filter 1 (AvgTrueRange,
625 kombinationer) — er det samme filter under to numre?

**5. Hvor mange beslutninger blev lavet om inden for 1–5 dage?**
P0 · 22.→27.→28. sep.
Pass/Fail lå i EdgeFinder (22. sep), flyttede til RSA (27. sep), og flowet blev tegnet
om igen (28. sep). Retningsreglen holdt 2–3 dage. Er tempoet for højt i forhold til
"kvalitet over hastighed" (23. sep)? Skal en metodebeslutning ligge et døgn, før den bygges?

**6. Hvad er "version 1.0" af RSA-metoden — og hvor står den?**
P0/P4 · krav fra panelet (dato ukendt).
Panelet krævede to spor (produktion/udvikling) og regressionstest. Hvis metoden ændres
i morgen, kan man så genskabe præcis det resultat, der dømte RawSignal123 "Fail"?

**7. Bliver hver resultatrække stemplet med metodeversion, datoperiode og RunID?**
P4 · 24.–27. sep.
Uden det kan man ikke se, om to resultater i tabellerne er regnet med samme regler.

**8. Hvor meget er metoden blevet tilpasset efter at have set resultaterne på RawSignal123?**
P0/P4 · 24.→27. sep.
Retningsreglen blev ændret, *efter* man så 123's resultater på 2019–2023. Den periode
overlapper den nye testperiode (2020–2024). Hver gang metoden rettes efter at have set
data, er data ikke længere "frisk" for metoden. Hvordan holdes styr på det?

## P1 — Prisdata

**9. Prisdata er planlagt 2015–2024. Hvor er 2025 (OOS) og 2026 (embargo)?**
P1/P6 · 24. sep mod 29. sep.
Hvis OOS skal være 2025, skal 2025 findes i databasen — men hvordan sikres det, at den
er låst, så ingen (heller ikke Claude) kan læse den før tid?

**10. Bliver Crude Oil rullet på samme dag i jeres 1-minuts data som i TradeStations kontinuerlige kontrakt?**
P1 · 24.–25. sep.
99,98 % ens *tidspunkter* siger intet om ens *priser*. Er det også tjekket, at OHLC
stemmer, især omkring rulle-datoerne? Hvad skete der med de 0,02 %?

**11. Additiv back-justering: hvad gør den ved procent-tal og ved "op/ned"-tællinger?**
P1/P4 · 24.–25. sep.
Dollartal er sammenlignelige, men en bevægelse på 1 $ betyder meget mere ved olie til
20 $ (2020) end ved 120 $ (2022). Bliver resultater i perioder med lav pris undervægtet
eller overvægtet? Skal der også måles i "antal gange normal udsving" (ATR)?

**12. Hvilken tidszone og hvilken bar-stempling (åbning eller lukning) bruger prisdata vs. TradeStation?**
P1/P4 · 24.–25. sep.
TradeStation stempler en bar med dens *slut*-tid. Hvis prisdata stempler med *start*-tid,
er der et minuts kig ind i fremtiden ved hver eneste join.

**13. "Dag = midnat til midnat" — men Crude Oil-dagen starter kl. 17 Chicago-tid dagen før.**
P6/P7 · 29. sep.
Med midnat deles én handelsdag i to. Er det bevidst? Gælder det også fredags-lukningen?

## P2 — RawSignal Maker

**14. Hvad sker der med filtre, der bruger funktioner ramt af hukommelsesfejlen (fx MACD), før de når RSA?**
P2→P4 · 18. og 24. sep (stadig ikke besluttet).
Giver filteret forkerte signaler, vil RSA dømme det på forkerte data — og et dødt filter
er "endeligt dødt" (17. sep). Skal de blokeres, før de når RSA?

**15. Skal signalerne efterprøves uafhængigt i Python mod prisdata (mindst for nogle filtre)?**
P2/P3 · 22. sep (kun compilering verificeres).
I dag tjekkes kun, at koden compilerer. Ingen tjekker, at signalerne er *rigtige*.
En stikprøve-genberegning i Python ville fange både hukommelsesfejl og tidszonefejl.

**16. 36 filtre har et ikke-udregnet Max Bars Back (antaget 1000). Hvad hvis det er for lidt?**
P2 · 24. sep.
Så starter signalerne for sent eller er forkerte i starten. Er opvarmningsperioden
(2015–2019) lang nok til at dække det, og bliver de første signaler skåret fra?

## P3 — EdgeFinder (kørslen)

**17. Hvilken rækkefølge gælder: EdgeFinder før RSA (27. sep) eller RSA → Code Creater → EdgeFinder (28. sep)?**
P3 · 27. sep mod 28. sep.
Den 27. kører EdgeFinder backtesten, *før* RSA dømmer. Den 28. står EdgeFinder *efter*
Code Creater. Hvem laver så backtesten, der giver RSA sine signaler?

**18. Hvad er en "Filter journal"-status, og hvem må ændre den?**
P3 · 11. aug / dato ukendt.
Status-felt (waiting/running/failed) til parallelle maskiner er nævnt, men ikke bygget.
Hvad sker der, hvis en maskine går ned midt i en kørsel — bliver filteret hængende i "running"?

**19. 12 bar-størrelser (5–60 min) × 380 filtre × op til 625 kombinationer: hvor lang tid tager én fuld runde?**
P3 · 28. sep og 26. sep.
Er det regnet ud, før man vælger mellem "ét filter ad gangen" og "alle filtre pr. tidsgraf"?

## P4 — RSA: signalet og målingen

**20. Varigheds-buckets bruger noget, man først kender bagefter. Er det ikke look-ahead?**
P4 · 24. sep og 27. sep (`varighed_bevaegelse`).
Når signalet tænder, ved man ikke, om det bliver tændt i 3 eller 31 bars. Hvis "31+ bars
virker bedst", kan man ikke handle på det. Hvordan bruges varigheden, uden at fremtiden
lækker ind? (Look-ahead skal tjekkes ved HVER ny beregning — 27. sep.)

**21. "Pris efter X bars": måles fra signalbarens lukning eller fra næste bars åbning?**
P4 · 24. sep.
Look-ahead-fejlen blev rettet i `mae_mfe` (25. sep). Er samme regel brugt i `prisefter`
og `fordeling_horisont`? I virkeligheden kan man tidligst handle på næste bar.

**22. Er horisonten "3, 5, 10, 15 bars" i Data2-bars eller i minutter?**
P4 · 24. sep.
10 bars på 5 min = 50 min; 10 bars på 60 min = 10 timer. Skal man sammenligne
bar-størrelser, skal horisonten måske måles i tid — eller begge.

**23. Hvad sker der, når horisonten krydser en pause, natten eller weekenden?**
P4/P7 · 29. sep (fredags-reglen).
En "10 bars"-måling fredag eftermiddag kan ende mandag. Det er ikke den samme handel,
som reglen "alt lukkes fredag" tillader.

**24. Hvad tæller som én observation? (står stadig åbent)**
P4 · sep.
147.900 signaler på 25 N1-værdier lyder af meget — men nabo-N1'er tænder ofte på næsten
de samme tidspunkter. Hvor mange *uafhængige* observationer er der reelt? Det afgør,
om "50–100.000 er rigeligt" (29. sep) er sandt.

**25. Signaler tæt på hinanden overlapper i deres "pris efter"-vindue. Er det taget med i usikkerheden?**
P4 · 24. sep.
To signaler med 2 bars mellemrum og 15 bars horisont måler næsten den samme
prisbevægelse. Så ser resultatet mere sikkert ud, end det er.

**26. Bruttotal (før omkostninger): hvor stor skal en edge pr. signal være for at overleve slippage og kommission?**
P4 · 24. sep.
Er en fordel på få cent pr. signal overhovedet interessant? Skal en minimumsgrænse
(fx 1–2 ticks efter omkostninger) ind i RSA, så filtre uden chance ikke bruger tid længere fremme?

**27. Måles kun gennemsnit og "% op" — eller også median, spredning og haler?**
P4 · 24. sep.
Et gennemsnit kan drives af få ekstreme dage (fx olie under 0 $ i april 2020). Er
2020 blevet tjekket for netop det?

**28. "Information Coefficient" blev nævnt 10. aug som fagbegreb. Bruges det?**
P4 · 10. aug.
Det er en standardmåling i professionelle event studies. Hvorfor er den ikke med?

## P4 — RSA: udgangspunktet ("alle bars")

**29. "Stabilitet uanset hvad der måles" (29. sep) — en stabil *nul-edge* er også stabil. Hvad skiller en stabil edge fra stabil tilfældighed?**
P4/P5 · 29. sep mod 27. sep.
Hvis udgangspunktet ikke er blokerende (27. sep), kan et filter, der stabilt gør *præcis*
det samme som markedet, i princippet bestå plateau-testen.

**30. Retningsreglen bruger udgangspunktet til at afgøre edge — men udgangspunktet er "ikke blokerende". Hvordan hænger det sammen?**
P4 · begge 27. sep.
"Ingen edge → gem info og gå videre" lyder blokerende. Hvilken af de to regler gælder?

**31. Skal udgangspunktet matches på klokkeslæt (og ugedag, volatilitet)?**
P4 · 24.–27. sep (ikke besluttet).
Signaler tænder måske oftest ved åbningen, hvor markedet bevæger sig mest. Så sammenlignes
de med en "gennemsnitsbar", der slet ikke ligner. Det kan både skjule og opfinde en edge.

**32. Er udgangspunktet regnet på samme bar-størrelse, samme sessioner og samme periode som signalerne?**
P4 · 24.–25. sep.
Ellers sammenlignes æbler med pærer.

## P4 — RSA: retning og statistik

**33. "4–5 år ud af 5 over udgangspunktet" — sandsynligheden for det ved ren tilfældighed er ca. 19 % pr. test. Er det skarpt nok?**
P4 · 27. sep.
Med 380 filtre × hundredvis af kombinationer vil tusindvis bestå ved held. Skal der også
kræves en minimumsstørrelse på forskellen og et sikkerhedsniveau (z-score/t-test) pr. år?

**34. Multiple testing-korrektion (~400 kombinationer pr. filter) er stadig åben. Hvornår skal den på?**
P4 · dato ukendt; 27. sep (advarslen).
Reelt er tallet langt større: kombinationer × bar-størrelser × horisonter × retning ×
varighed. Er det samlede antal tests talt op? Uden det ved man ikke, hvor mange "gode"
resultater der kun er held.

**35. "Den der finder edges må aldrig være den der dømmer dem" (17. sep) — men RSA både finder retningen og dømmer. Er princippet brudt?**
P4/P5 · 17. sep mod 27.–28. sep.

**36. Er retningen den samme på alle horisonter (3, 5, 10, 15)? Hvis ikke, hvilken vinder?**
P4 · 27. sep.
Et filter kan være Long på 3 bars og Short på 15. At vælge den bedste horisont bagefter er
endnu en skjult test.

**37. "Regime" er i dag = kalenderår. Er et kalenderår et regime?**
P4 · 11. aug (panelets punkt 2) mod 24. sep (volatilitet udskudt).
Panelet krævede opdeling efter markedsregime. 2020 indeholdt både krak, negativ pris og
genopretning. Hvornår kommer volatilitets-opdelingen, og skal den være på plads, før den
første rigtige gate-dom falder?

**38. Minimum antal signaler pr. celle er ikke besluttet — men RawSignal123 er allerede kaldt "Fail".**
P4/P5 · 27. sep.
Er dommen over 123 foreløbig? Og skal der en regel om, at intet filter dømmes "endeligt dødt",
før gaten er færdigdefineret?

## P5 — Plateau, gate og scoring

**39. Hvordan virker 3×3 / 5×5 / 7×7 / 9×9-plateauet for filtre med kun N1, med decimaltal eller uden parametre?**
P5 · 28. sep.
RawSignal123 havde kun N1 (en linje, ikke et felt). Mange af de 380 filtre har slet ingen
parametre. Hvad er "plateau" for dem?

**40. Er et plateau ægte, eller kommer det bare af, at nabo-parametre tænder på de samme tidspunkter?**
P5 · 24. og 28. sep.
N1 = 12 og N1 = 13 deler måske 90 % af signalerne. Så *skal* resultaterne ligne hinanden —
og plateauet beviser intet. Skal overlappet mellem naboers signaler måles og vises?

**41. Er "nabo" lige langt væk for alle filtre?**
P5 · 11. aug / 28. sep.
Et trin på 1 i en periode på 3 er en stor ændring; et trin på 1 i en periode på 200 er
næsten ingenting. Skal nabo-afstanden være i procent i stedet for trin?

**42. Procent-afvigelse på 5/10/15/20 % — procent af hvad?**
P5 · 27. sep (ikke besluttet).
Er gennemsnittet tæt på 0, bliver procenter vilde (0,01 → 0,02 = 100 % afvigelse). Er
z-score eller forskel målt i usikkerheder ikke mere robust? (Står som åbent 27. sep.)

**43. Hvor sættes grænserne for grøn/grå/rød — og bliver de låst, *før* man ser 002 og 169?**
P5 · 28. sep.
Sættes grænserne efter at have set resultaterne, kan man (ubevidst) vælge dem, så det
filter man håber på, består.

**44. "Kun centeret sendes videre" — hvad hvis centeret ligger på kanten af det testede område?**
P5 · 28. sep.
Så ved man ikke, om plateauet fortsætter uden for gitteret. Skal det udløse en udvidet test?

**45. "Endeligt dødt" (17. sep) — gælder det også, hvis RSA-metoden senere viser sig at have haft en fejl?**
P5 · 17. sep og 25. sep (look-ahead-fejlen).
Look-ahead-fejlen viser, at metoden *kan* have fejl. Skal en metodefejl give ret til
genkørsel af alle filtre, der er dømt på den gamle version?

## P6 — Periodeopdeling

**46. Testdata er nu 2020–2024, men RawSignal123 blev kørt på 2019–2023. Skal 123 køres om?**
P6 · 24.–27. sep mod 29. sep.
Ellers er den første "dom" ikke lavet på samme grundlag som alle de næste.

**47. Én OOS-periode (2025, ét år) brugt én gang — hvad sker der, når hundredvis af filtre testes mod den samme OOS?**
P6 · 29. sep.
Så bliver OOS i praksis endnu en udvælgelse, og "brugt én gang" holder kun pr. filter, ikke
for systemet. Og 10–20 % tilladt afvigelse på ét år er stort set støj. Hvordan beskyttes OOS?

**48. 2026-embargoen: i dag er det 1. okt 2026 — året er ikke slut. Hvornår er embargoen "færdig", og hvordan er den teknisk låst?**
P6 · 29. sep og aug ("teknisk utilgængelig").
Den lokale session har fuld adgang til TradingDB. Hvad forhindrer den i at læse 2026-data?
Og afløser den de tidligere 6 måneders embargo (åbent 29. sep)?

## P7–P8 — Efter RSA

**49. Code Creater er rykket frem lige efter RSA (28. sep), men hvilken exit den bruger er ikke besluttet. Kan man skrive kode uden exit?**
P7 · 28. sep.
Og RSA har kun målt "pris efter faste horisonter" — er der en plan for, hvordan den bedste
horisont oversættes til en exit, uden at det bliver endnu en optimering på testdata?

**50. Alt testes kun på Crude Oil (28. sep). Hvornår bevises det, at RSA virker på et marked, hvor svaret er kendt?**
P0/P4/P8 · 28. sep og 10. aug (cross-market).
RawSignal123 viste, at RSA kan sige "Fail". Men den er aldrig vist at sige "Pass" til noget,
der *ved* at have en edge. Skal der laves et kunstigt testfilter med en indbygget edge
(og et rent tilfældigt filter), så man ved, at metoden finder det ene og afviser det andet?

---

## De 5 vigtigste at tage først (min vurdering)

1. **Nr. 20** — varighed som look-ahead. Kan ugyldiggøre en hel tabel.
2. **Nr. 50** — kalibrér RSA med et kendt "ja"-filter og et kendt "nej"-filter.
3. **Nr. 40 + 24** — plateau og signalantal kan være kunstigt pæne pga. overlap.
4. **Nr. 33 + 34** — 4–5 af 5 år er for svagt med så mange tests.
5. **Nr. 1** — få RSA-koden og beslutningerne fra 24.–29. sep ind i repoet.
