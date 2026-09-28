# Konsulentopgaver — Udviklingsmotoren (idé → færdig strategi → dvale)

## Overordnet mål

Vi bygger en fuldautomatisk udviklingsmotor, der tager en rå idé og fører
den hele vejen frem til en **færdig, statistisk godkendt strategi**, som
lægges i et "dvale-lager" og venter på senere at blive sat i drift.

Denne opgave dækker **kun udviklingsmotoren** — fra idé til dvale. Den
dækker **ikke**: risikostyring på tværs af strategier, live-udførelse,
overvågning af rigtige penge, eller hvad der sker, når en strategi vækkes
fra dvalen. Det er bevidst udeladt og kommer senere.

## Nuværende stade (kort)

- **RawSignal Creature** — bygger og verificerer 380+ filtre i
  TradeStation (EasyLanguage). Er i gang og fungerer i store træk.
- **EdgeFinder** — skal afgøre om et signal er en ægte statistisk fordel
  (event-studie). Er **kun en løs skitse** i dag, ikke færdigdesignet.
- **EdgeCruncher** — det led der samler op efter EdgeFinder. Er **slet
  ikke designet endnu**.
- Alt kører i dag på TradeStation, fordelt over **11 TML-servere**, og
  skal senere porteres til MultiCharts.
- Data og resultater gemmes i en database (TradingDB), men der findes
  endnu intet struktureret "dvale-lager" til færdige strategier.

## De tre roller

De tre konsulenter skal arbejde sammen om ét fælles slutprodukt: en
skriftlig, konkret definition af **"færdig strategi"** — præcis hvilke
tests en strategi skal bestå, før den lægges i dvale. Det er selve
målestokken for hele projektet, og uden den ved vi ikke, hvornår vi er i
mål.

Arbejdsrækkefølge: **Rolle 1 først** (sætter målestokken), **Rolle 2
derefter**, **Rolle 3 løbende** så snart der er noget værd at skalere.

---

## Rolle 1 — Validering & "færdig strategi" (statistiker)

**Formål:** Sikre at kun ægte, robuste strategier når frem til dvale-
lageret — ikke tilfældige mønstre, der kun ser gode ud, fordi der er
testet 380+ filtre samtidig.

**Konkrete opgaver:**
- Designe selve **EdgeFinder-metoden** fra bunden (den er i dag kun en
  løs skitse: "load workspace, hent backtest-data, analysér event-
  studie" — intet mere præcist findes endnu).
- Fastlægge hvordan der korrigeres for, at mange filtre testes samtidig
  (multiple testing / data snooping), så vi ikke tror et tilfældigt
  vindende filter er en ægte fordel.
- Designe walk-forward- og robusthedstests (fx cluster-robusthed: virker
  strategien også for nabo-parametre, ikke kun det ene bedste sæt).
- Skrive den endelige, konkrete **"færdig strategi"-definition**: hvilke
  tests skal bestås, med hvilke grænseværdier, før noget lægges i dvale.
- Lave **stikprøvekontrol** af et udvalg af filtre fra RawSignal
  Creature, ved at genberegne dem uafhængigt — som en sikring af, at
  Rolle 3's arbejde ikke fejler stille (se fx den kendte fejl, hvor
  MACD i en løkke kan give forkerte tal uden fejlmelding).
- Vurdere Thomas' eksisterende "Plateau-trappe" (PL1–PL7, en
  robusthedsmåling baseret på 3x3/5x5/7x7/9x9-naboskaber med grøn/grå/
  rød) og — **efter afklaring med Thomas selv** af de uklare punkter
  (hvad grå og rød betyder, hvorfor PL6 tillader op til 20 % rød mens
  PL2 og PL4 kræver 0 %) — afgøre om og hvordan den indgår i "færdig
  strategi"-kriteriet.

**Leverance:** Et skriftligt, entydigt "færdig strategi"-dokument + en
beskrevet EdgeFinder-metode, der kan implementeres af Rolle 3.

**Afgrænsning:** Finder/udvikler ikke selv nye strategi-idéer (det er
Rolle 2) — dømmer kun.

---

## Rolle 2 — Strategi- og edge-udvikling

**Formål:** Finde og formulere kandidater til rigtige, vedvarende
fordele (edges) i prisdata — råmaterialet som Rolle 1 efterfølgende
dømmer.

**Konkrete opgaver:**
- Analysere output fra RawSignal Creature og pege på, hvilke
  filter-kombinationer der er værd at forfølge videre.
- Formulere nye idéer til filtre, entry-/exit-regler og strategi-logik,
  baseret på mønstre i data.
- Arbejde tæt sammen med Rolle 1 om at oversætte en rå idé til noget,
  der kan testes formelt — men **dømmer aldrig selv**, om resultatet er
  godt nok. Det er bevidst adskilt fra Rolle 1, så samme person ikke
  både finder og godkender sit eget arbejde.

**Leverance:** En løbende strøm af kandidat-strategier/edges, klar til
formel validering hos Rolle 1.

**Afgrænsning:** Ingen ansvar for kodning i EasyLanguage, automatisering
eller databaser — det er Rolle 3.

---

## Rolle 3 — Motor-bygger (EasyLanguage, automatisering, dvale-lager)

**Formål:** Få hele udviklingsmotoren til at køre selvstændigt, hurtigt
og fejlsikkert — uden at Thomas skal have AI- eller Python-viden for at
holde den kørende.

**Hårdt krav (kan ikke fravælges):** Dyb, praktisk EasyLanguage-
kompetence. Stille fejl her (som den kendte MACD-i-løkke-fejl, der giver
forkerte tal uden nogen fejlmelding) ødelægger alle efterfølgende
resultater usynligt. Dette skal prioriteres højst ved valg af konsulent.

**Konkrete opgaver:**
- Kvalitetssikre de 380+ filtre i RawSignal Creature for skjulte
  EasyLanguage-faldgruber.
- Færdiggøre **EdgeCruncher** (i dag helt udesignet) baseret på den
  metode Rolle 1 leverer.
- Bygge selve automatiseringen: kø og fordeling af backtests på de
  **11 TML-servere**, med fejlsikring så processen kan stoppe sig selv
  og melde fejl i stedet for at fortsætte med forkerte data (jf. den
  eksisterende regel: "ved fejl, ret, ryd op og kør forfra — lap
  aldrig").
- Designe og bygge **dvale-lageret**: hvordan en færdig, godkendt
  strategi gemmes, mærkes (fx med hvilken version af "færdig strategi"-
  kriteriet den bestod) og senere kan findes og hentes frem igen.
- Senere: porte hele kæden fra TradeStation til MultiCharts.

**Bonus (rart at have, ikke et krav):** Erfaring med server-drift/
distribuerede kørsler og databasedesign. Findes det ikke hos samme
person som EasyLanguage-kompetencen, kan det løses som tilkøbt hjælp —
men EasyLanguage-delen må ikke gå på kompromis for det.

**Leverance:** En kørende, selvstændig pipeline fra RawSignal → EdgeFinder
→ EdgeCruncher → dvale-lager, der kan skaleres på de 11 servere uden
manuel indgriben.

**Afgrænsning:** Bestemmer ikke selv, hvad der er "godt nok" — følger
Rolle 1's kriterier. Bygger ikke selv nye strategi-idéer — det er
Rolle 2.

---

## Åbent punkt (kræver Thomas, ikke konsulenterne)

Plateau-trappens (PL1–PL7) grå/rød-grænser er uafklarede og skal
bekræftes af Thomas, før de indgår i "færdig strategi"-kriteriet under
Rolle 1. Ingen af konsulenterne skal gætte sig til dette.
