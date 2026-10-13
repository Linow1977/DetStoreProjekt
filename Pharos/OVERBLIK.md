# Pharos — overblik over det, der findes

Samlet 2026-10-12 ud fra projektets GitHub-grene og tidligere samtaler.
Intet af Pharos er bygget endnu. Alt her er udkast, svar og forsøg.

## Hvad Pharos er

Pharos er fabrikkens sidste led og vagten over strategierne i inkubation
(dvale) og live. Pharos bygger på Andrea Ungers Titan.

Plads i kæden (fra konsulentrunden 29-09-2026):

TradingDB → RawSignal Maker → RSA → Code Creater → Edge-Finder / Edge-Cruncher
→ Incubator → **Pharos** → [Thomas godkender] → handel

## Hvad Thomas har besluttet eller svaret

Fra spørgeskemaet (01-10-2026, grenen `claude/detstorprojekt-sporgeskema-doqabk`):

- Udvælgelse, portefølje, nøgletal og live-drift ligger hos Pharos.
- **Kun Thomas aktiverer strategier.**
- Strategier, der holder op med at virke, **gemmes**; opgaven ligger ved Pharos.
- Om en edge er stor nok i kroner og øre, er en opgave for Pharos (svar 128).
  Senere præciseret (04-10): omkostningsfaktoren bruges først i Edge-Finder.
- Gennemgang efter hver måned og hvert kvartal: begge dele.
- Pharos er en af kilderne til at måle, om hele udviklingssystemet bliver bedre.
- Tal hver morgen: gårsdagens % profit, total % profit, gårsdagens antal
  handler, **gårsdagens antal strategier overgivet til Pharos**, antal aktive
  servere. Det samme pr. uge, måned og kvartal. Rapporter: en blanding af tal,
  diagrammer og tekst.

Fra FriSnak (12-10-2026): ét samlet program (UI) omkring hele processen,
måske delt i to — RSA + EDGE (fabrikken) og Pharos (vagten).

## Pharos-udkastet (konsulentrunden 29-09-2026)

Ligger i `konsulentrunden_2026-09-29/` (kopieret fra grenen
`claude/dreamy-lamport-eztlk0`). Udkastet er designet, ikke bygget, og
**intet i det er besluttet endnu.** Kort:

- **Månedsliste:** efter sidste handelsdag foreslår Pharos for hver strategi
  OPTAG, BEHOLD, PAUSE, GENOPTAG eller PENSIONER plus antal kontrakter.
  Thomas godkender listen. Pharos afgiver aldrig ordrer.
- **Daglig vagt:** tekniske fejl (ændret kode, manglende data, forkert
  position) sætter strategien på pause med det samme. Alt andet er forslag.
- **Målestok:** hver strategi måles mod det, den *lovede* ved frys 2
  (forventningsbånd fra Monte Carlo), ikke mod sidste måned.
- **Bevidst afvigelse fra Titan:** Titan vælger efter nylig gevinst
  (momentum). Udkastet starter med *samme risiko til alle* og tager kun
  momentum i brug, hvis en test på egne papirhandler viser, at det virker —
  tidligst ca. 2029-2030. Forsøg på opdigtede data viste, at momentum kun
  hjalp, når gode perioder faktisk varede ved, og ellers gav større udsving.
- **Størrelse:** f = det mindste af 0,5 % og 10 % ÷ antal strategier, målt mod
  strategiens "værste dag". Lofter: 25 % pr. marked, 60 % pr. retning, 20 % pr.
  klynge af ens strategier. Nødbremse: halvér alle størrelser ved for stor
  samlet nedtur (forslag, Thomas godkender).
- **Pension er endelig** (som "kasseret er endeligt").
- **Ærlig begrænsning:** en død strategi opdages langsomt, typisk efter ca.
  2 år, og mange slet ikke inden for 5 år. Beskyttelsen er spredning og små
  størrelser.
- **Kontrolpanel:** én side med Godkend/Afvis, en farvet linje pr. strategi
  (grøn/gul/rød/grå) med én sætning om hvorfor, alarmliste og "Vis tallene bag".
- **Tabeller (forslag):** skemaet `pharos` med dagsresultat, koersel,
  forslag, godkendelse, alarm og status_journal — kun indsæt, aldrig ret.

Åbne punkter til Thomas står i udkastets afsnit 9 (momentum ja/nej, grænser
for pause og pension, risiko pr. strategi, godkendelse af hver månedsliste,
hvem der sætter listen ind i TradeStation).

## Laboratoriet

`konsulentrunden_2026-09-29/Laboratorium/` — små forsøg på **opdigtede data**:

| Fil | Spørgsmål |
|---|---|
| `K1/f15_pharos_pause.py`, `K1/f15b_pharos_regelsaet.py` | Hvor tit rammes en god strategi af pause eller pension ved en fejl? |
| `K1/f16_momentum_mod_1N.py` | Slår Titan-agtig udvælgelse "samme risiko til alle"? |
| `K2/pharos_proto.py`, `K2/test_pharos_proto.py` | Prototype af den månedlige beregning med 8 tests |
| `K2/pharos_forsoeg.py`, `K2/pharos_blok.py` | Momentum mod "alle lige", og hvor stor blokken må være i lokkedue-testen |

Prototypens 8 tests blev kørt igen 12-10-2026: **8 af 8 bestået.**

## Titan-undersøgelsen (12-10-2026)

`reports/Andrea Ungers Titan program.md` og noterne i `research_notes/`.
Den bekræfter udkastets billede af Titan og retter to ting i det:

- Eksemplet "største nedtur fra over 400.000 til ca. 150.000 $" findes i
  Ungers italienske Titan-artikel (del 2), men **ikke med samme gevinst**:
  overskuddet faldt samtidig fra ca. 2,9 til 1,64 mio. $.
- "1 % pr. handel" kommer kun fra en tredjepart. Unger selv oplyser ingen
  procent; en elev nævner 2 % daglig risiko.

## Alternativer til Titan (12-10-2026)

`reports/Alternativer til Titan for futures.md` og noterne i
`research_notes/Alternativer til Titan for futures/`. Kort:

- Intet købeprogram gør det samme som Titan til futures med TradeStation eller
  MultiCharts. Der findes kun delløsninger (MultiWalk Trader, MultiCharts
  Portfolio Trader, QuantAnalyzer, Portfolio Analyst, Adaptrade MSA).
- Den daglige vagt skal sættes sammen af lag: platformens alarmer, et eksternt
  "jeg lever"-signal (hjerteslag) og mæglerens egne tabsgrænser.
- Forskningen støtter udkastets "samme risiko til alle" frem for momentum.
- Udfordrer udkastet på tre punkter: papir-tal fra TradeStations SIM-konto
  kan være for flotte; udkastet mangler hjerteslag, mæglergrænser og en skrevet
  nødstop-plan; flere strategier på samme marked i samme konto giver let
  forkerte positioner.
- Researchernes vurdering: byg den smalle kerne selv og lån regnestykkerne fra
  gratis biblioteker (fx ffn, Riskfolio-Lib, arch). Listen over byggeklodser
  står i `BYGGEKLODSER.md`.

## Titans skærmbilleder (12-10-2026)

`titan_skaermbilleder/` — otte billeder fra Ungers YouTube, delt af Thomas,
med beskrivelse i `BESKRIVELSE.md`. Viser Titans fire faner, otte
filterfamilier, korrelationsfilter (0,75), stop midt i perioden og
"filtreret mod ufiltreret"-test. Retter Titan-rapporten på to punkter (se
rapportens tilføjelse sidst).

## Idé fra Thomas: Pharos mod Thomas (13-10-2026, FriSnak)

Ikke besluttet. Thomas' idé, med Claudes tilføjelser markeret.

**Idéen:** Pharos laver hver måned en liste over de live-strategier i
porteføljen, der bør gå fra aktiv til inaktiv. Thomas gennemgår selv og vælger,
hvilke der skal ud og ind. Pharos laver sin *egen* liste, hvor den for hver
strategi skriver, **hvorfor** den skal ud eller ind. Begge lister gemmes, og
over tid ses det, om Pharos' valg er bedre end Thomas'. Hvis de er *meget*
bedre, kan Pharos på sigt få lov til selv at lukke og starte strategier — med
Thomas som opsyn.

**Hvordan det passer med udkastet:** Udkastets månedsliste (OPTAG, BEHOLD,
PAUSE, GENOPTAG, PENSIONER) og tabellen `forslag` er næsten det samme. Nyt er
(1) Thomas' egen liste ved siden af, (2) pointtavlen mellem de to, og (3) en
vej til, at Pharos handler selv.

**Claudes tilføjelser (til drøftelse):**
- **Tre deltagere, ikke to:** Thomas, Pharos og en tredje, der *intet ændrer*
  ("alle strategier kører videre"). Er ingen af de to bedre end "intet", er
  månedlige ind- og udskiftninger spild. Det er samme tanke som udkastets
  R0 ("alle lige").
- **Thomas skriver sin liste først.** Låses og tidsstemples, før han ser
  Pharos' liste, ellers påvirker den hans valg og sammenligningen bliver
  skæv. Gerne en kort begrundelse pr. strategi fra Thomas også — så kan det ses,
  hvilke slags begrundelser der holder, og de kan blive til regler i Pharos.
- **Spillereglerne for "bedre" skrives ned på forhånd:** hvad måles (samlet
  resultat, største nedtur, antal strategier der ud fra bagklogskab blev
  fejlsorteret), over hvor lang tid, og hvor stor forskellen skal være.
- **Det tager år at se:** der er kun 12 månedslister om året, og en død
  strategi opdages typisk først efter ca. 2 år (udkastet). En rimelig
  forventning er 3-5 år, før det kan siges med sikkerhed — samme tidshorisont
  som momentum-testen (2029-30). Hver strategi i hver måned er dog en
  afgørelse, så der er flere målinger end 12.
- **Trin på vejen mod selvstyre, ikke alt-eller-intet:** (1) kun forslag,
  (2) Pharos må selv *lukke* strategier, Thomas må nedlægge veto, (3) Pharos må
  også starte, med loft på antal ændringer pr. måned. At lukke er mindre
  risikabelt end at starte, og nødbremsen står altid.
- **Ændrer to tidligere udsagn:** udkastet siger "Pharos afgiver aldrig
  ordrer", og Thomas' svar i spørgeskemaet siger "kun Thomas aktiverer
  strategier". Begge gælder, indtil Thomas selv siger andet.

**Thomas' svar på "hvad er bedre" (13-10-2026):** Det bliver en kombination af
de enkelte strategier og porteføljen som helhed. Det gælder **nedtur, optur og
korrelation**. "Kollision" i Thomas' første svar var en tastefejl; han bekræftede
bagefter, at det dækker **tabsperioder, der falder sammen** — flere strategier
taber på samme tid, så porteføljens nedtur bliver større end summen af de
enkeltes. Det hænger sammen med udkastets loft pr. klynge af ens strategier
(20 %) og Titans korrelationsfilter (0,75).

**Åbent:** Hvem sætter ændringen ind i TradeStation
i trin 2-3? Hvor mange ændringer pr. måned må Pharos højst foretage?

## Hvad der ikke findes endnu

- Ingen kode til Pharos ud over prototypen på opdigtede data.
- Ingen beslutning om udkastets åbne punkter.
- Incubator, som Pharos skal hente strategier fra, er heller ikke bygget.
- Grenene med udkastet og spørgeskemaet er ikke flettet ind i `main`.
