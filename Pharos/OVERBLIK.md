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

## Hvad der ikke findes endnu

- Ingen kode til Pharos ud over prototypen på opdigtede data.
- Ingen beslutning om udkastets åbne punkter.
- Incubator, som Pharos skal hente strategier fra, er heller ikke bygget.
- Grenene med udkastet og spørgeskemaet er ikke flettet ind i `main`.
