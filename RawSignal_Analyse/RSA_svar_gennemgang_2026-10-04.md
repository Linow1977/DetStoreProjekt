# Gennemgang af Thomas' svar på RSA-skemaet (4. oktober 2026)

Svarene står ordret i `SPOERGSMAAL_EventStudy_RSA_2026-10-01.md`. Her er de
samlet: hvad der nu er besluttet, hvad der stadig er uklart, og hvor en
dataanalytiker/kvant ser en risiko.

Status: 42 svar, 18 "Ved ikke endnu".

## 1. Beslutninger (som Thomas har svaret)

| Emne | Beslutning | Spm. |
|---|---|---|
| Testdata nu | Alt, der er kørt indtil nu, er test. Når testfasen er slut, slettes det, og der køres forfra på frisk data. Testfasen er ikke færdig (rettet af Thomas, se afsnit 5). | 2, 3, 43 |
| Periodekæde | RSA: 5 år IN + 1 år OOS. Edge-Finder: RSA's IN + OOS bruges som IN + 1 nyt år OOS. Edge-Cruncher: Edge-Finders IN + OOS som IN + 1 nyt år OOS. | 5 |
| OOS-længde | 1 år. | 41 |
| Tid | Alt kører i børsens tid (exchange time), hvor kontrakten handles. | 6 |
| Låste år | 2025 og 2026 hentes hver for sig, ligger hvert sit sted, og kun det modul, der skal bruge dem, får adgang. | 8, 44 |
| Ekstreme priser | Bruges som de er (også −37 $ i april 2020). | 10 |
| Omkostninger | Bruges først i Edge-Finder. RSA leder kun efter retning og stabilitet. | 21 |
| Retning | Findes på testdata og låses ved frys 1. | 27 |
| Regimer | Panelets krav om opdeling efter markedsregime er bevidst droppet. | 31 |
| Grænse for edge-størrelse | Accepteres for nu (kun meget stærke edges på ét marked). | 32 |
| Plateau-farver | Grænserne er fastsat af Thomas og angiver nabo-stabilitet. PL2 er stadig minimum. | 33, 34 |
| Plateau for 1-akse-filtre | 3, 5, 7 eller 9 nabo-værdier. | 36 |
| Identiske celler | Ingen særskilt kontrol. Fejl skal vise sig i OOS. | 35 |
| Uafhængig Python-kontrol | Ikke før det er bevist nødvendigt. | 12 |
| Fast filter-ID | Ja (formodentlig). | 13 |
| Afkast-enhed | Dollars. | 52 |
| Kendte begivenheder (EIA, rulledage) | Markeres ikke. | 56 |
| Exit og fredags-regel | Afgøres af Edge-Finder. | 46, 48 |
| Lokkeduer / tilfældige tidspunkter | Begge testes og evalueres over tid. | 25 |
| Tolerance i OOS | "10 % falske er okay". | 40 |
| Bar-længde-hullet, prøvekørsel, hvem kører backtest | "Det er fikset" (på serveren, ikke i repoet). | 14, 15, 16 |
| Datakvalitetsrapport, mindste opdagelige edge | Tages, hvis det bliver aktuelt. | 58, 59 |
| MultiCharts-data, plantet edge i CL | Skal testes. | 49, 50 |

## 2. Svar, der skal afklares (opfølgning)

| Spm. | Svar | Hvorfor uklart |
|---|---|---|
| 28 | "ja" | Spørgsmålet var enten/eller: "én backtest pr. workspace" eller 1,8-6 mio. celler. "ja" afgør det ikke. |
| 20 | Klumpning "kan angive signalets styrke … ellers er det kun signalet på et givet tidspunkt, der gælder" | Spørgsmålet handlede om, hvor sikkert målingen er, ikke om signalets styrke (se risiko A). |
| 19 | "er den ikke retningsangivende" | Varigheden kendes først, når signalet slukker. Den kan derfor ikke angive retning på det tidspunkt, hvor man skal handle. Skal den stadig bruges som beskrivelse? |
| 38 | "fantastisk spørgsmål" | Ikke besvaret: går kun plateauets midte videre, og hvad hvis midten ligger på kanten? |
| 23 | "kun test" | Er 150 dage / 300 signaler et testtal, der skal afprøves, eller er tærsklen droppet? |
| 40 | "10 % falske er okay" | Det svarer til FDR 10 % (spm. 29, "ved ikke"). Men tolerancen i OOS (z = 1,28 / z = 1,0 / 20 %) er et andet tal. Skal vi vælge den OOS-regel, der i laboratoriet kommer tættest på 10 %? |
| 33 | Grænserne er "fastsat af mig" | Tallene står ikke i repoet. De skal ind i regelfilen, før RSA kører for alvor. |
| 4, 9, 13 | "det må vi nok heller", "tror vi har løst det", "ja det tror jeg" | Formodentlig ja, men skal bekræftes. |
| 14-16 | "det er fikset" | Rettelserne er lavet på serveren. De bør lægges i repoet, så cloud-sessionen ser dem. |

## 3. Risici set med en kvants øjne

**A. Klumpning gør RSA's dom for optimistisk (spm. 20, 24, 30).**
Når RSA tæller hvert signal som én måling, ser resultatet 1,4-4,6 gange mere
sikkert ud, end det er (forsøg f1). Det handler ikke om signalets styrke, men
om, hvor meget man kan stole på målingen. Svaret "tid vil sortere falske fra"
(spm. 30) holder kun, hvis der er tid nok: hvert OOS-år kan kun bruges én
gang, og hvis RSA lader mange falske igennem, bruger de OOS-året op og
fylder Edge-Finder. Forslag: RSA tæller stadig signaler, men regner
usikkerheden pr. handelsdag. Det koster én linje i beregningen og ændrer ikke
signal-definitionen.

**B. Periodekæden bruger et nyt år pr. trin (spm. 5).**
RSA: IN 2020-2024, OOS 2025. Edge-Finder: IN 2020-2025, OOS 2026.
Edge-Cruncher: IN 2020-2026, OOS 2027. Det betyder:
- 2026 bliver OOS for Edge-Finder og kan ikke samtidig være embargo (beslutningen 29. sep).
- Edge-Cruncher skal bruge 2027 som OOS. Det år er ikke slut før januar 2028,
  så det passer ikke med første rigtige handel i foråret 2027.
- Dagens dato er 4. okt 2026, så 2026 er heller ikke slut.
Skal kæden afklares, før Edge-Finder bygges?

**C. Dollars og år-for-år-sammenligning (spm. 52, 24).**
CL svingede ca. 10 gange mere i 2020 og 2022 end i 2019. Når afkast måles i
dollars, vil år-for-år-afvigelsen (5-20 %-båndene fra 27. sep) især måle,
hvor uroligt året var, ikke om edgen er stabil. Dollars kan sagtens være
dommen, men en vol-justeret kolonne ved siden af gør år-for-år-tallet
meningsfuldt.

**D. Ingen kontrol for identiske celler (spm. 35).**
Et gitter ramt af regnefejlen når automatisk PL7 og får dermed højeste
prioritet. Signalerne i det er rigtige for én indstilling, så det kan godt
bestå OOS, men plateauet (robustheden) er falsk, og filteret går videre som
"robust", uden at være det. Kontrollen er én beregning af overlap mellem
fjerne celler og koster ingen OOS-data.

## 4. Stadig åbent ("Ved ikke endnu")

1, 7, 11, 17, 18, 22, 26, 29, 37, 39, 42, 47, 51, 53, 54, 55, 57, 60.

De vigtigste blandt dem, før RSA kører for alvor:
- **17:** entry tidligst minuttet efter signal-barens lukning i alle tabeller (look-ahead).
- **18:** de højst 3 horisonter, låst før data ses.
- **29:** FDR-grænsen (hænger sammen med "10 % falske er okay").
- **11:** vejen for de op til 196 filtre med regnefejlen.

## 5. Opfølgning med Thomas (samme dag)

**Rettelser og nye beslutninger:**
- Testen er **ikke** færdig. Testdata slettes først, når testfasen er slut.
- **Periodekæden (erstatter 2020-2024 / 2025 / 2026-embargo fra 29. sep):**

  | Trin | IN | OOS |
  |---|---|---|
  | RSA | 2019-2023 | 2024 |
  | Edge-Finder | 2019-2024 | 2025 |
  | Edge-Cruncher | 2019-2025 | 2026 |

  Hvert OOS-år skal være låst for alle trin før det. 2026 er først komplet i
  januar 2027.
- **38:** Kun plateauets midte går videre. Ligger midten på kanten af gitteret,
  tages den også med. Skal programmeres.
- **40:** Tolerancen i OOS sættes til 15 % (fast grænse, ikke z-værdi;
  til bekræftelse). Laboratoriet (f2) gav for fast 10 % / 20 % at ca. 45-55 %
  af ægte edges blev smidt ud, så 15 % ligger midt imellem.
- **33:** Farvegrænserne i PL1-PL7 er ikke defineret endnu.
- **20:** Der skal tælles dage med signal. En dag med mange signaler kan
  senere bruges til at finde en bedre statistisk indgang.
- **52:** Der laves en kolonne for udsving (volatilitet) ved siden af dollars.
- **35:** Ingen kontrol for ens felter. Det, der sendes videre med fejl, fejler senere.

**Stadig åbent:** 28 (forklares igen), 17, 18 og 29 (uddybes), 11 (plan for
de 7 ikke-målte seriefunktioner), 33 (farvegrænser).

**Fakta om 11:** Programmets liste (`Program/formel.py`) har 10
seriefunktioner. Average og AvgTrueRange er målt og virker, MACD er målt og
ramt. Ikke målt: RSI, StandardDev, XAverage, DMIplus, DMIminus, ADX og
ChaikinMoneyFlow.

## 6. Anden opfølgning med Thomas (samme dag)

- **17 (besluttet):** RSA skal bruge næste bars åbning, regnet ud fra Data2's
  bar-længde, som tidligste pris efter et signal. Gælder alle RSA-tabeller.
- **18 (besluttet):** Måletidspunkterne skal være samme tid for alle
  bar-længder (fx minutter), ikke samme antal bars. De tre tider er ikke valgt.
- **20:** Flere signalserier på én dag kan give flere handler på én dag.
  Optælling pr. dag gælder kun for, hvor sikker målingen er, ikke for antal handler.
- **Ny idé (Thomas):** "Signalet har været tændt i k bars → gå ind" testes i
  Edge-Finder og lægges senere ind i Edge-Cruncher.
- **11:** MACD og de 7 ikke-målte seriefunktioner (RSI, StandardDev,
  XAverage, DMIplus, DMIminus, ADX, ChaikinMoneyFlow) skal undersøges. Thomas
  foreslår at teste på ny testdata ("2007-2029"; formodentlig 2007-2018, til
  bekræftelse), så hverken IN- eller OOS-årene bruges.
- **Stadig åbent:** 28 (forklares igen), 29 (Thomas spørger: hvordan kan held
  bestå OOS?), 40 (15 %-grænsen forklares nærmere), 33 (farvegrænser).

## 7. Tredje opfølgning (5. oktober)

- **"Gå ind, når signalet har været tændt i k bars"** er en selvstændig test
  for sig.
- **Måletidspunkter (18):** Alle tider skal testes, ikke kun 3. Hver tid tæller
  som ekstra forsøg (hænger sammen med 28).
- **11:** Testperioden for regnefejlen er **2007-2009** (ikke 2007-2018).
  Alle 8 funktioner (MACD + de 7 ikke-målte) testes på "40-40-80"
  (formodentlig Data1 = 40, Data2 = 40, Data3 = 80 minutter; til bekræftelse).
  Claude skal ikke skrive opgaven.
- **40:** Thomas har bedt om forklaring af reglen "efter hvor meget året normalt
  svinger" (konsulentrapporten del 1, D.2) før valget mellem den og 15 %.
- **40-40-80 bekræftet:** Data1 = 40, Data2 = 40, Data3 = 80 minutter.
- **40 (OOS-tolerance):** Thomas spurgte, hvad en fast grænse på 40 % giver.
  Laboratoriets forsøg 2 er kørt igen med 15/30/40/50 %, se
  `Laboratorium/f2_resultat_2026-10-05.txt`. Ikke besluttet endnu.
- **40 (besluttet 5. okt):** OOS-tolerancen er en **fast grænse på 40 %**
  (erstatter 15 %). Et filter består prøveåret, hvis resultatet er mindst
  60 % af resultatet i IN-perioden. Begrundelse: i forsøg 2b smider 40 % ca.
  21 % af de ægte ud og lukker ca. 13 % af de falske igennem; de falske kan
  fanges i de næste prøveår (2025, 2026), mens en kasseret ægte edge er tabt.
