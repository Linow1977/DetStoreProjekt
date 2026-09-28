---
title: "Konsulentrapport, version 2: udviklingsmotoren i DetStoreProjekt"
subtitle: "Dybde-runden – råd til Thomas, ikke beslutninger"
date: "28. september 2026"
---

# Aftalen for dybde-runden

1. Thomas fandt version 1 for overfladisk. Version 2 skal passe til målet: en fuldautomatisk strategifabrik på niveau med de bedste systematiske fonde.
2. **Nyt:** Konsulenterne har *læst* projektets egne filer. Det gælder kode, NOTER.md, beslutningslogs, Videnslog og Thomas' egen beskrivelse af EdgeFinder. Intet er ændret. Påstande herfra er mærket [Projekt: fil:linje].
3. Leverancen er stadig kun råd. Tallene er regnet efter, trin for trin. Hvert fund er markeret som **BEVIST**, **SANDSYNLIGT** eller **UKENDT**.
4. Rollerne er uændrede: K1 godkender metoder, K2 og K3 bygger. Ingen afgør Thomas' åbne punkter, og uenighed vises åbent.

**Sådan blev arbejdet lavet:**

- **Runde 1:** Hver konsulent skrev sin del om fra bunden ud fra projektets filer og angreb sit eget første udkast.
- **Runde 2:** Hver konsulent læste de to andres dele, godkendte eller afviste deres metoder og rettede derefter sin egen del. Kritikkerne står i bilaget.
- **Stikprøver:** Den overordnede agent har selv tjekket en række påstande direkte i koden. Det gælder `verify-one.ps1:277`, `generer.py:26`, `indlaes_csv.py:67-72`, `rawsignal_creature.py:97-107`, `faelles.py:38` og tallet 4.918 mod 480. Alle holdt.

**Vigtig begrænsning:** Cloud-miljøets netværk blokerede de fleste kilder, bl.a. SSRN, arXiv, Wikipedia, tradestation.com og multicharts.com. Kun PostgreSQL's dokumentation kunne åbnes, fordi den blev læst via dens kildefiler på GitHub. Alle andre internetkilder er mærket "[Net, ikke bekræftet]". Regnestykkerne afhænger ikke af kilderne, men de officielle platformsregler (series functions, licenser) skal stadig læses af nogen med adgang.

# Sammenfatning (højst en halv side)

**1. Fabrikken tester millioner af ting, ikke 380.** Hvert filter har op til 625 indstillinger. Hvis man ganger med 4 workspaces, køb/salg og flere tidshorisonter, bliver det ca. 3,4 millioner forsøg. Justeret for, at nabo-indstillinger ligner hinanden, er det "effektivt" ca. 30.000. Det bedste rene held vil derfor se ud som t ≈ 4. En ægte edge skal nå **t ≈ 4,65**, ikke 2 eller 3 (del 1).

**2. Derfor er mængden af historiske data det vigtigste spørgsmål i hele projektet.** Hvor mange års data der skal til, afhænger kun af edgens styrke og grænsen. En edge med årlig Sharpe 2 kræver ca. 7,5 års data. En edge med Sharpe 1 kræver ca. 30 år. Hvor meget intradag-data projektet har, står ingen steder (del 1, BEVIST som matematik).

**3. MACD-fejlen er værre og anderledes end antaget.** Alle 625 indstillinger giver *præcis* samme signal. Det ligner et perfekt plateau, så plateau-analysen ville belønne fejlen. TradeStations egen advarsel ignoreres i dag af kontrollen. Derudover mangler mange funktioner på advarselslisten (del 2, BEVIST i koden).

**4. Datamodellen kan i dag kun rumme ét marked pr. filter.** Den næste kørsel sletter den forrige uden fejlmelding, og intet sted står, hvilket marked tallene kom fra. Det samme grundproblem findes tre steder: filnavnet, `FileDelete` og `delete from` (del 2 og 3, BEVIST).

**5. Selve backtesten er ikke automatiseret.** Det er den reelle flaskehals. Gruppen er enig om vejen: TradeStation laver få facit-kørsler, og Python regner resten og skal bevises ens bar for bar (del 2 og 3).

**Konsulenterne er enige:** Den fulde kørsel bør først startes, når en kort række billige forberedelser er lavet ("Fase 0" i del 4). De koster timer eller dage. Springer man dem over, skal kørslen efter projektets eget princip ryddes og køres forfra.

Intet i rapporten er et løfte om afkast. Handel indebærer risiko for tab.


# Del 1 – Validering (Konsulent 1: kvantitativ statistiker), version 2

*Denne version erstatter hele den første del 1. Det er rådgivning. Jeg designer og godkender metoder, men jeg bygger dem ikke, og jeg afgør ikke Thomas' åbne punkter.*

**Mærker:**
- **[Projekt: fil]**: står i projektets egne filer. Jeg har kun læst dem, ikke ændret dem.
- **[Rapport]**: står i statusrapporten.
- **[Net, ikke bekræftet]**: En kilde, jeg fandt via søgning, men ikke kunne åbne, fordi netværket i cloud-sessionen blokerede siden (SSRN, arXiv, Oxford Academic og Wikipedia blev alle afvist). Jeg har kun set titel, forfattere og resumé i søgeresultatet. Formlerne kender jeg fra faget. Thomas bør få dem tjekket mod originalen.
- **[Regnet]**: Jeg har selv regnet det i et lille Python-regnestykke i scratchpad (`k1_regn.py`). Det er ikke leveret som kode til projektet.
- **[Antagelse: hvorfor]**: min egen vurdering.

**Hvor sikre er vi?** Hvert fund er markeret som **BEVIST** (vist med projektets egne tal eller ren matematik), **SANDSYNLIGT** (godt begrundet, men ikke målt) eller **UKENDT**.

**Ordliste. Fagordene forklaret én gang:**
- **Overfitting:** En regel er tilpasset så tæt til gamle data, at den fanger tilfældig støj. Den ser flot ud bagud og virker ikke fremad.
- **Multiple testing:** Tester man mange ting, ser nogle af dem gode ud af rent held. Det er som at slå plat og krone med mange mønter.
- **p-værdi:** Hvor sandsynligt det er at se et resultat så godt som det fundne, *hvis der i virkeligheden intet er*.
- **t-værdi:** Hvor mange "usikkerheder" resultatet ligger over nul. t = 2 betyder "cirka 2,5 % chance for held, hvis der kun er ét forsøg".
- **Sharpe (SR):** gennemsnitligt afkast delt med udsvinget i afkastet. Jo højere, jo mere stabilt tjener noget. *Per-handel-Sharpe* regnes pr. handel. *Årlig Sharpe* regnes pr. år.
- **Deflated Sharpe (DSR):** en Sharpe, hvor der er "trukket fra" for, hvor mange ting man har prøvet.
- **FWER og FDR:** FWER betyder "ingen falske fund overhovedet". FDR (false discovery rate) betyder "højst en fast andel af fundene er falske".
- **Walk-forward:** Man vælger på én periode, tester på den næste, rykker frem og gentager.
- **Styrke (power):** Hvor stor chance en test har for at *finde* en edge, der faktisk er der.
- **Event-studie:** Man måler, hvad prisen gør lige efter hver gang et signal tænder, og sammenligner med en "normal" periode.

---

## 0. Kort sammenfatning: de vigtigste nye fund

1. **Antallet af forsøg er ikke 380, men flere millioner.** Filtrene har op til 625 parameterkombinationer hver. De køres på 4 workspaces, og EdgeFinder vil prøve både køb og salg på flere tidshorisonter. Det rå antal forsøg er ca. 1,5–9,5 millioner. Det *effektive* antal, hvor man tager højde for, at naboer ligner hinanden, er sandsynligvis 3.000–300.000. **BEVIST** for det rå antal (ud fra projektets filer). **SANDSYNLIGT** for det effektive interval, som skal måles.
2. **Hvor mange års data der kræves, afhænger kun af to ting:** edgens årlige Sharpe og t-grænsen. Antallet af handler pr. år er ligegyldigt. Med en realistisk grænse (t ≈ 4,65) kræver en edge med årlig Sharpe 2 ca. **7,5 års** data. Med årlig Sharpe 1 kræves ca. **30 år**. **BEVIST** (ren matematik [Regnet]). Hvor meget data projektet har, er **UKENDT**.
3. **MACD-fejlen giver falske plateauer.** Filter 68 gav *nøjagtig de samme 4.918 signaler* for alle 625 kombinationer [Projekt: RawSignal_Creature/Program/generer.py; BESLUTNINGSLOG_2026-09-24.md]. Et felt, hvor alle celler er ens, ser ud som et perfekt plateau. Plateau-analysen vil altså *belønne* fejlen. **BEVIST**.
4. **EdgeFinder er ikke godkendt.** Den nuværende proces og filen `EdgeFinder_F5_SIGNAL.el` opfylder kun E1 delvist. E2–E8 mangler helt (afsnit 6). **BEVIST** ud fra filerne.
5. **Mit første udkast var for blødt fire steder:** kravet om "30 handler i pengeskabet", "t > 3" som bar, "380 forsøg" og en PBO-grænse uden begrundelse. De er rettet her (afsnit 12).

---

## 1. Definition af "færdig strategi", version 2

En strategi må først lægges i dvale, når **alle** punkter er bestået og skrevet ind i passet. Grænserne er nu *regnet*, ikke gættet. Hvor de afhænger af noget ukendt, står der en formel og en tabel. Thomas vælger scenariet. Konsulent 3 bestemmer, hvordan passet gemmes. Her står, hvad der skal stå i det.

| # | Test | Krav | Grundlag |
|---|---|---|---|
| F1 | **Teknisk korrekt** | (a) Signalets tænd/sluk er 100 % ens med en uafhængig genberegning, bar for bar, for stikprøven i afsnit 10. Kombinationen, der bliver til strategien, er altid med. (b) Samme kørsel to gange giver samme fil. (c) Kombinationens signalrække er *ikke* identisk med nabokombinationernes, medmindre formlen forklarer det (som dubletterne fra `floor`). | Afsnit 9–10 |
| F2 | **Data delt og låst før analyse** | Udvikling, validering og pengeskab (hold-out) er fastlagt med datoer, *før* den fulde kørsel analyseres. Pengeskabet er den seneste periode. | Afsnit 4.4 |
| F3 | **Alle forsøg talt** | Passet har både det rå antal forsøg (N_rå) og det målte effektive antal (N_eff). | Afsnit 3 |
| F4 | **Signifikant efter korrektion** | Strategiens t-værdi på udviklings- og valideringsdata skal nå grænsen for N_eff (tabel 4.1). Og DSR ≥ 0,95 beregnet med N_eff. | Afsnit 4.1 |
| F5 | **Plateau** | Det plateau-niveau, Thomas vælger. Farverne er defineret efter en af metoderne i afsnit 8, og identiske signalrækker er slået sammen først. | Afsnit 8 |
| F6 | **Walk-forward** | Alle valg (parameter, udgang, retning) træffes *inde i* hvert vindue. De sammensatte test-perioder skal samlet have t ≥ grænsen for det antal kandidater, der gik ind i walk-forward (ikke hele fabrikken). | Afsnit 4.3 |
| F7 | **Efter omkostninger** | F4 og F6 regnes efter omkostninger. Ved dobbelte omkostninger skal gennemsnittet stadig være over nul. | [Antagelse: stresstest] |
| F8 | **Stabil over tid** | Højst ét år ud af fem (eller tilsvarende andel) med negativt gennemsnit, og intet enkelt år står for over 40 % af gevinsten. | Afsnit 4.5 |
| F9 | **Pengeskabet åbnes én gang** | Én test på hold-out-data. Dumper den, kasseres strategien. Pengeskabet er en "kasseringstest", ikke et bevis (afsnit 4.4). | Afsnit 4.4 |
| F10 | **Nok handler** | Antallet af handler n skal være mindst ((t_grænse + 0,84) / SR_handel)². Det er givet ved styrkeberegningen og kan ikke sættes til et fast tal. | Afsnit 4.2 |

**Passet skal mindst indeholde:** fast filter-ID og filter-version (numrene er flyttet én gang [Projekt: BESLUTNINGSLOG_2026-09-24.md]), N1/N2, workspace (tidsrammer for data1–3), retning og horisont, datadelings-datoer, N_rå, N_eff, t-værdi, DSR, PBO, walk-forward-resultat, plateau-niveau og farvemetode, antal handler, største tab, omkostningsmodel, "pengeskab åbnet: ja/nej + dato", status på hukommelsesfejlen (målt og ramt / målt og virker / ikke målt), resultat af F1-kontrollen og kodeversion.

"Færdig" betyder: *vi har ikke kunnet afvise den*. Det er aldrig et løfte om gevinst.

---

## 2. Hvad projektets filer faktisk viser (fakta, jeg bygger på)

- **Et råt signal** er kun "hvornår filteret tænder, og hvor mange bars det er tændt". Der er ingen retning og ingen pris. CSV-formatet er én linje pr. signal: `RunID,N1,N2,Starttid,AntalBars,Afsluttet` [Projekt: BESLUTNINGSLOG_2026-09-24.md; Program/indlaes_csv.py]. **Følge:** Retning (køb/salg) og horisont vælges først i EdgeFinder. Så *det er der, de fleste forsøg bliver skabt*.
- **Parametre:** N1 og N2 gennemløbes som Fra/Til/Step, og arrays har altid 25 pladser [Projekt: OPGAVEBESKRIVELSE_RawSignal.md]. Højst 25 × 25 = 625 kombinationer pr. filter.
- **Workspaces:** fire tidsrammesæt: 5/10/60, 10/20/60, 5/30/120 og 5/10/120 [Projekt: NOTER.md, "Navngivning – afklaret 2026-09-22"].
- **Filter 1 (AvgTrueRange):** 939.816 signaler på 620 kombinationer, i snit ca. 1.516 signaler pr. kombination. 5 kombinationer kan aldrig blive sande (3·N1 = 5·N2) [Projekt: BESLUTNINGSLOG_2026-09-24.md].
- **Filter 68 (MACD, gammelt nr. 069):** "alle 625 kombinationer gav de samme 4.918 signaler" [Projekt: Program/generer.py, linje 26]. Fejlen fik alle kombinationer til at give samme svar.
- **Dubletter fra formlen:** I gamle 069 giver `maxlist(2, floor(N2/2))` kun 11 forskellige værdier for 25 N2-værdier [Projekt: RawSignal/RawSignal069.el].
- **Hukommelsesfejlen** kan ramme MACD, RSI, StandardDev, Average, DMI, ChaikinMoneyFlow, AvgTrueRange og XAverage. Risikoen er accepteret for alle filtre [Projekt: NOTER.md punkt 3; VIDENSLOG.md].
- **Modstrid i filerne:** `RawSignal266.el` (Average) skriver "Forvent at N1 heller ikke gør nogen forskel her". VIDENSLOG siger derimod, at Average (gamle 266) "virker" [Projekt: RawSignal/RawSignal266.el; VIDENSLOG.md 2026-09-24]. Filhovedet er formentlig ældre end målingen, men det er **UKENDT**, hvad der gælder.
- **Data:** Hvilket marked og hvor mange års historik der bruges, står ingen steder, jeg har læst. Eksemplet i CSV-formatet er dateret 2021-10-22. **UKENDT**. Det er det vigtigste tal, der mangler (afsnit 4).

---

## 3. Det rigtige antal forsøg, trin for trin

### 3.1 Det rå antal (N_rå)

Et "forsøg" er hver ting, man kunne have valgt som vinder. Det er ikke kun hvert filter.

| Trin | Faktor | Kilde |
|---|---|---|
| Filtre | 380 | [Projekt: BESLUTNINGSLOG_2026-09-24.md] |
| × kombinationer pr. filter (C) | 1 til 625. Snittet er **UKENDT**. Scenarier: 100 / 300 / 625 | [Projekt: OPGAVEBESKRIVELSE_RawSignal.md] |
| × workspaces | 4 | [Projekt: NOTER.md] |
| × retning (køb/salg) | 2 | [Antagelse: signalet har ingen retning, så EdgeFinder må prøve begge] |
| × horisonter i event-studiet | fx 5 (1, 5, 10, 20 bars og "til dagens slut") | [Antagelse: typisk event-studie; ikke fastlagt i projektet] |

N_rå = 380 × C × 4 × 2 × 5 [Regnet]:
- C = 100 giver **1.520.000**
- C = 300 giver **4.560.000**
- C = 625 giver **9.500.000**

**Rettet efter kritikrunden:** Fordelingen står faktisk i projektet. 128 filtre bruger N1 og N2, 114 kun N1, 62 kun N2 og 77 ingen, ud af 381 inkl. det slettede `True`-filter [Projekt: BYGGEVEJLEDNING_RawSignal.md, afsnit "Formlen bruger"]. Ved fuldt 1–25-gitter giver det 128·625 + 176·25 + 76 = **84.476 kombinationer pr. workspace** (snit C ≈ 222). N_rå ≈ 84.476 × 4 × 2 × 5 ≈ **3,4 mio.** Det er et loft, fordi Fra/Til/Step pr. filter kan være mindre. Inden for filtrene er det effektive antal ca. 128·36 + 176·6 + 76 ≈ 5.700 pr. workspace, før korrelation mellem filtre. Midtscenariet N_eff ≈ 25.000–30.000 i 3.2 holder.

**Filtre ramt af MACD-typen (Konsulent 2's gruppe A):** Hvis Konsulent 2's forklaring holder (funktionen regnes én gang pr. bar, med en N-værdi, vi ikke kender), giver de i dag **0 gyldige forsøg**, ikke 1: det fælles signal hører måske til en parameter uden for gitteret. Når de er bygget om, tæller de fuldt med igen. Derfor skal N_eff altid tælles på *unikke, kontrollerede* signalrækker.

Dertil kommer EdgeCrunchers udgangsregler og stop (hver variant ganger igen). Dertil kommer også alle tidligere "kig" på de samme data, fx da filtrene i sin tid blev valgt til `filter_case`. De kan ikke tælles, men de findes. [Antagelse]

### 3.2 Det effektive antal (N_eff)

Naboer ligner hinanden. ATR med længde 60 og 65 tænder næsten på de samme bars. De er derfor *ikke* to uafhængige forsøg. N_eff er antallet af "reelt forskellige" forsøg. Et skøn, trin for trin:

1. **Inde i ét filter:** længderne går fra ca. 5 til 125, altså en faktor 25. Signaler med længder, der ligger mindre end ca. 1,5–2 gange fra hinanden, er stærkt korrelerede [Antagelse: typisk for glidende gennemsnit]. log(25)/log(1,75) ≈ 5,8, altså ca. **6 uafhængige trin pr. parameter**. To parametre giver ca. **36**. Én parameter giver ca. 6. Filtre ramt af MACD-fejlen giver **1**.
2. **Mellem filtre:** mange filtre er varianter af de samme få ideer (volatilitet, trend, momentum). Skøn: 380 filtre svarer til ca. **50–150 uafhængige familier** [Antagelse: navnene og formlerne gentager få byggesten].
3. **Workspaces:** de deler tidsrammer, så 4 svarer til ca. **2–3**.
4. **Retning:** køb og salg på samme signal er hinandens spejlbillede. Det svarer til *én* test, der kan gå begge veje, altså en faktor **2** i p-værdien.
5. **Horisonter:** 1 og 5 bars er delvist korrelerede, så 5 svarer til ca. **2–3**.

Midtscenarie: N_eff ≈ 100 × 20 × 2,5 × 2 × 2,5 = **25.000**. Rimeligt interval: **3.000–300.000**. **SANDSYNLIGT**. Intervallet er bredt, og derfor skal N_eff **måles**, ikke gættes:

- **Metode til måling:** For hver kombination laves en daglig serie af "signalets afkast" (eller blot tændt/slukket pr. bar). Derefter beregnes korrelationen mellem alle serier. N_eff skønnes ud fra, hvor spredt korrelationsmatricens egenværdier er. Det svarer til Nyholt/Li-Ji-metoden fra genetik. Alternativt grupperes serierne i klynger, og antallet af klynger tælles, som López de Prado foreslår. [Antagelse: kendte metoder. Jeg har ikke kunnet åbne kilderne i denne session.]
- **Enklere kontrol:** Kør hele fabrikken på kendt-tilfældige signaler (afsnit 7) og se, hvor højt den bedste t-værdi bliver. Den bedste tilfældige t-værdi *er* den reelle grænse. Den er uafhængig af, hvordan N_eff skønnes. **Det er den test, jeg anbefaler mest.**

### 3.3 Hvad det betyder for grænserne

Den tabel, der følger nu, er projektets vigtigste enkelttal [Regnet]:

| N (forsøg) | Bedste rene held (forventet t) | FWER-grænse 5 % (Bonferroni, t) | DSR ≥ 0,95 kræver ca. t ≥ |
|---|---|---|---|
| 380 (det første udkast) | 2,97 | 3,65 | 4,61 |
| 3.000 | 3,56 | 4,15 | 5,20 |
| **30.000** (midtscenarie) | **4,12** | **4,65** | **5,77** |
| 300.000 | 4,62 | 5,10 | 6,27 |
| 4.560.000 (rå, C = 300) | 5,16 | 5,60 | 6,80 |

Sådan er tabellen regnet:
- **Bedste held:** den forventede største værdi af N tilfældige t-værdier = (1−γ)·Φ⁻¹(1−1/N) + γ·Φ⁻¹(1−1/(N·e)), hvor γ ≈ 0,5772. Formlen er fra Bailey & López de Prado [Net, ikke bekræftet: "The Deflated Sharpe Ratio", https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551].
- **Bonferroni:** Φ⁻¹(1 − 0,05/N).
- **DSR ≥ 0,95:** Under nul-hypotesen er usikkerheden på Sharpe ca. 1/√T. Derfor svarer DSR ≥ 0,95 til t ≥ (bedste held) + 1,645. Skæve afkast og "fede haler" hæver kravet en smule. Ved en per-handel-Sharpe på ca. 0,1 og kurtosis 20 er det under 3 % [Regnet], så det er ikke det, der betyder mest her.

**Læsning for et barn:** Hvis fabrikken prøver 30.000 reelt forskellige ting, vil den bedste *rene tilfældighed* se ud som t ≈ 4. Den gamle grænse "t > 3" [Net, ikke bekræftet: Harvey, Liu & Zhu (2016), "...and the Cross-Section of Expected Returns", Review of Financial Studies] var lavet til ca. 300 faktorer i hele forskningsverdenen. Den er for lav til en fabrik af denne størrelse.

**FDR i stedet for FWER:** Benjamini–Hochberg [Net, ikke bekræftet: Benjamini & Hochberg (1995), JRSS B, https://academic.oup.com/jrsssb/article/57/1/289/7035855] er mildere, når der *findes* mange ægte edges, og lige så streng som Bonferroni, når der næsten ingen findes. Den egner sig til grovsorteringen i RawSignal-Analyse (q = 10 %). Den endelige godkendelse (F4) bør bruge FWER/DSR, fordi hver strategi i dvale skal kunne stå alene. [Antagelse: begrundet i, at hver dvale-strategi senere bruges enkeltvis]

---

## 4. Kalibrering af grænserne med regnestykker

### 4.1 F4: grænsen afhænger af N_eff, og N_eff skal måles
Brug tabel 3.3 med det *målte* N_eff. Indtil det er målt, foreslår jeg midtscenariet: **t ≥ 4,65 og DSR ≥ 0,95**, med DSR regnet med N_eff = 30.000. Thomas vælger. [Antagelse]

### 4.2 F10: kan en realistisk edge overhovedet ses? (styrkeberegning)

En test med signifikansgrænse t_g finder en ægte edge med 80 % sandsynlighed, når:

n (antal handler) ≥ ((t_g + 0,84) / SR_handel)²

Per-handel-Sharpe hænger sammen med årlig Sharpe S og antal handler pr. år K: SR_handel = S / √K. Sætter man ind, får man:

**År med data, der kræves = ((t_g + 0,84) / S)²**. Antallet af handler pr. år går ud af regnestykket. **BEVIST** (algebra).

| t-grænse | S = 1 | S = 1,5 | S = 2 | S = 3 |
|---|---|---|---|---|
| 2,0 (naiv, ét forsøg) | 8,1 år | 3,6 år | 2,0 år | 0,9 år |
| **4,65** (N_eff ≈ 30.000, FWER) | **30 år** | **13 år** | **7,5 år** | **3,4 år** |
| 5,8 (DSR med N_eff ≈ 30.000) | 44 år | 20 år | 11 år | 4,9 år |

[Regnet]. S er edgens *ægte* årlige Sharpe for ét enkelt signal efter omkostninger.

**Hvad det betyder:**
- Er der kun 3–5 års intraday-data [Antagelse: eksemplet er fra 2021. **UKENDT**], kan fabrikken med ærlige grænser *kun* finde enkeltsignaler med årlig Sharpe omkring 2,5–3 eller mere. Svagere, men ægte edges vil ikke kunne skelnes fra held. Det er ikke en fejl i metoden. Det er det, data kan bære.
- **Tre håndtag** (Thomas vælger):
  1. **Mere historik.** Det har størst virkning.
  2. **Færre forsøg.** Fx step 5 i stedet for 1, så 625 kombinationer bliver 25, og retning og horisont fastlægges på forhånd pr. filter. Virkningen er dog kun "logaritmisk": går man fra 4,5 mio. til 30.000 forsøg, falder grænsen fra 5,6 til 4,65.
  3. **Flere markeder med samme regel.** Hvis den samme uændrede regel testes på fx 5 uafhængige markeder, lægges beviserne sammen. [Antagelse: kræver at markederne ikke er stærkt korrelerede]
- Handlerne skal være **uafhængige**. Event-studiets signaler overlapper ofte, fordi mange tænder tæt på hinanden. Så er det effektive n mindre end antallet af signaler. Det skal regnes med blok-bootstrap (afsnit 6, E3).

### 4.3 F6: walk-forward
"Flertallet af vinduer positive" fra mit første udkast er en svag test. Ved S = 0 er der 50 % chance for, at hvert vindue er positivt. Nyt krav: de sammensatte test-perioder testes samlet med en t-grænse for det antal kandidater, der *gik ind* i walk-forward. Går der fx 50 kandidater ind, er Bonferroni-grænsen t ≈ 2,9 [Regnet: Φ⁻¹(1−0,05/50)]. Walk-forward er kun ærlig, hvis *alle* valg sker inde i vinduet, også valg af retning og horisont.

### 4.4 F2/F9: pengeskabet (hold-out) kan ikke bevise meget
Hvor lang hold-out-periode skal der til for at bekræfte en edge med 80 % styrke ved 5 % ensidet? Formlen er år = ((1,645 + 0,84) / S_ægte)² [Regnet]:

| Ægte S | 0,75 | 1 | 1,5 | 2 | 3 |
|---|---|---|---|---|---|
| År i pengeskabet | 11 | 6,2 | 2,7 | 1,5 | 0,7 |

Den ægte S er typisk mindre end den, backtesten viser. En halvering er et almindeligt skøn [Antagelse: "haircut", fordi den bedste af mange altid er overvurderet]. **Følge:** Et pengeskab på 1–2 år kan *afsløre* en død strategi, men sjældent *bevise* en levende. F9 er derfor en kasseringstest. Beviset skal komme fra F4 + F6 på de ældre data. Min anbefaling: pengeskabet skal være ca. **20–30 %** af historikken og mindst 1 år. Thomas afgør.

### 4.5 F8: stabilitet over år
Ved årlig S = 2 er usikkerheden på ét års resultat ca. 1 (i Sharpe-enheder). P(et år er positivt) er så Φ(2) ≈ 0,977. P(mindst 4 af 5 år positive) er for S = 2: 0,99; for S = 1: 0,82; for S = 0: 0,19 [Regnet]. Reglen "højst ét negativt år ud af fem" smider altså sjældent en god strategi ud. Til gengæld afviser den kun ca. 81 % af rene tilfældigheder. **Den er et supplement, ikke et bevis.** 40 %-grænsen for ét års andel af gevinsten er en [Antagelse] og bør efterprøves med placebo-signaler.

### 4.6 PBO (sandsynlighed for overfitting ved udvælgelsen)
PBO er den andel af gange, hvor "vinderen" i den ene halvdel af data ender under midten i den anden halvdel [Net, ikke bekræftet: Bailey, Borwein, López de Prado & Zhu, "The Probability of Backtest Overfitting", https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253]. Rene tilfældigheder giver PBO ≈ 0,5. I første udkast skrev jeg "0,2–0,3" uden begrundelse. Nyt forslag: **grænsen kalibreres** ved at køre udvælgelsen på placebo-sæt (PBO bør være ≈ 0,5) og på sæt med indplantede edges. Grænsen sættes, så højst 5 % af placebo-sættene kommer under den. Indtil det er gjort: PBO ≤ 0,2 som foreløbig grænse. [Antagelse]

---

## 5. Svagheder led for led (opdateret)

**RawSignal Creature**
- **Hukommelsesfejlen skaber kopier, ikke støj.** Filter 68 viser, at fejlen kan få alle 625 kombinationer til at give samme signal. Statistisk betyder det: (1) plateau-analysen ser et perfekt plateau (afsnit 8), (2) forsøgstallet ser ud til at være 625, men er 1, og (3) vi ved ikke, *hvilken* parameter det fælles signal reelt svarer til. **BEVIST**.
- **Delvis fejl er farligere end total.** En funktion, der kun blandes lidt, giver *forskellige, men forkerte* signaler. Dem kan kun en uafhængig genberegning afsløre (afsnit 9). **SANDSYNLIGT**, fordi mekanismen er beskrevet [Projekt: NOTER.md punkt 3].
- **Dagsfunktioner** (`CloseD` osv.) giver TradeStations advarsel om seriefunktioner i en løkke. Men de står ikke på programmets liste, og det er besluttet ikke at tilføje dem [Projekt: BESLUTNINGSLOG_2026-09-24.md]. Statistisk betyder det, at deres filtre ikke får advarslen i passet. **Risiko: ikke målt.**
- **Max Bars Back for de 36 filtre:** Er værdien for lav, er de første bars' signaler forkerte. Det rammer altid starten af data, altså udviklingsdata. Test: Kør med 1000 og 2000, og sammenlign signalerne efter bar 2000. Er de ens, holder antagelsen.
- **Opvarmning (tilføjet efter Konsulent 2, afsnit 1.4):** Funktioner med tilbagekobling (EMA, Wilder) glemmer deres startværdi langsomt. **Min grænse: højst 0,1 % tilbageværende startvægt**, dvs. kasser k = ln(0,001)/ln(1−a) bars (EMA længde 600: ca. 2.070 bars). Begrundelse: at kassere et par tusind bars koster under 1 % af flere års data, mens en fejl rammer netop de første, måske skæve signaler. **Bevis for, at vinduet er nok:** 'to-starts-testen'. Kør filteret fra to startdatoer med mindst ét vindue imellem. Signalrækkerne skal være 100 % ens efter det seneste vindue. Er de ikke det, fordobles vinduet.
- **Data1 = Data2 håndhæves** [Projekt: BESLUTNINGSLOG_2026-09-24.md]. Det er godt, for så tælles AntalBars ens.
- **Censurering:** Et signal, der stadig er tændt ved slutningen, får `Afsluttet = 0` [Projekt: BESLUTNINGSLOG_2026-09-24.md]. Det er godt. Men den ældre fil `EdgeFinder_F5_SIGNAL.el` mangler det og taber det sidste signal.

**RawSignal-Analyse og EdgeFinder:** Metoden skal skrives og låses, før den fulde kørsel analyseres. Ellers vælges metoden (ubevidst) efter resultatet.

**EdgeCruncher:** Hver udgangsregel og hvert stop tæller som forsøg (F3). Den må ikke røre pengeskabet (min tidligere kommentar til Konsulent 2).

**Dvale:** Både taberne og antallet af forsøg skal gemmes. Ellers kan N_eff ikke regnes igen, når strategien vækkes.

---

## 6. EdgeFinder: godkendelse punkt for punkt

**Thomas' proces** [Projekt: Task_RawSignal_Creature_EdgeFinder_opgave.md]: læs journalen, åbn TradeStation, indlæs workspace og RawSignal, hent backtest-data, tjek for fejl (stop ved fejl), gem under nyt navn, analysér event-studiet og journalfør Passed/Failed. Processen er "ikke helt udformet".

**Filen** `EdgeFinder_F5_SIGNAL.el` [Projekt: RawSignal_Creature/EdgeFinder_F5_SIGNAL.el]: registrerer, hvornår `Range > AvgTrueRange(N1·5)` tænder og hvor længe, for N1 = 1–25, og skriver til `C:\Test\signals_test.csv`. Den indeholder *ingen* priser, afkast eller sammenligning. Den er altså en rå signal-optager (en tidlig udgave af RawSignal), ikke et event-studie.

| Krav | Status | Hvad mangler konkret |
|---|---|---|
| E1 Ingen fremtidsinformation | **Delvist.** Filteret bruger kun nuværende og tidligere bars. | Hvornår handlen starter, er ikke defineret. Signalet kendes først, når baren *lukker*. TradeStations tidsstempel er bar-slut [Antagelse: standard i TradeStation, ikke tjekket her]. Indgang skal derfor ske tidligst ved åbningen af næste data1-bar. Ved data2/data3 (højere tidsramme) skal det sikres, at kun *færdige* bars bruges. |
| E2 Retfærdig sammenligning | **Mangler** | En kontrolgruppe: afkast på tilfældige tidspunkter med samme tid på dagen, samme ugedag og samme volatilitetsniveau. Eller en "cirkulær forskydning" af signalrækken (samme mønster, flyttet i tid). |
| E3 Overlap og afhængighed | **Mangler** | Signaler inden for horisonten overlapper, og nabokombinationer deler signaler. Der skal bruges blok-bootstrap med blokke på mindst en handelsdag, eller én observation pr. dag. |
| E4 Omkostninger | **Mangler** | En omkostningsmodel pr. marked (kurtage + slippage i ticks). Tallene fastsætter Thomas. |
| E5 Walk-forward | **Mangler** | Se F6. |
| E6 Korrektion for forsøg | **Mangler** | "Passed/Failed" har ingen defineret grænse. Brug tabel 3.3 med N_eff og FDR til grovsortering. |
| E7 Placebo giver den forventede falsk-positiv-rate | **Mangler** | Kør f.eks. 1.000 tilfældige signaler (samme hyppighed og længde som de ægte) igennem. Ved en grænse på 5 % skal 3,6–6,4 % slippe igennem (95 %-interval ved 1.000 forsøg [Regnet: 0,05 ± 1,96·√(0,05·0,95/1000)]). |
| E8 Indplantet edge findes | **Mangler** | Syntetisk prisserie med en kendt lille edge (fx per-handel-Sharpe 0,1). Mindst 80 % af de indplantede skal findes, når datalængden efter afsnit 4.2 er nok. |

**Konklusion:** Den rå signal-optager kan **godkendes som input**, når den følger den nye skabelon (`Afsluttet`, fast RunID, ikke `C:\Test`). **EdgeFinder som proces godkendes ikke endnu.** Der mangler en skriftlig og låst beskrivelse af: indgangstidspunkt, horisonter, retning, kontrolgruppe, omkostninger, grænse og placebo/indplantet-test. Den beskrivelse skal Thomas og Konsulent 2 skrive, og jeg godkender den.

Desuden mangler projektet en skriftlig definition af, **hvad en "event" er**: tænding (starten af et signal) eller hele den tændte periode. Det ændrer både n og overlap. Thomas afgør.

---

## 7. Metode for RawSignal-Analyse (opdateret)

Kun på udviklingsdata. Rækkefølge:
1. **Sundhed:** antal signaler pr. kombination, fordeling over tid, andel `Afsluttet = 0`, og signaler i de første 1000 bars.
2. **Fjern kopier:** Kombinationer med *identisk* signalrække slås sammen til én (fx de 625 i filter 68 og floor-dubletterne i 069). Antallet af unikke rækker gemmes. Er **alle** rækker ens i et filter med seriefunktion, markeres filteret "ramt af hukommelsesfejl" og går ikke videre.
3. **Rå effekt pr. unik kombination:** fremadrettet afkast på den eller de *forud valgte* horisonter mod kontrolgruppen (E2) og t-værdi med blok-bootstrap (E3).
4. **Plateau-kort** efter en af metoderne i afsnit 8.
5. **FDR (q = 10 %)** på tværs af hele fabrikken, *efter* kopierne er fjernet.
6. **Placebo-kontrol som fast del af hver kørsel:** Hver kørsel indeholder fx 200 kendt-tilfældige signaler, gemt adskilt fra produktionsdata. Slipper for mange igennem, stoppes kørslen.
7. **Log alt**, også dem der dumper, og N_eff.

---

## 8. Plateau-trappen: tre testbare farvedefinitioner (Thomas vælger)

Fælles for alle tre:
- Identiske signalrækker slås sammen *før* farvning, så fejl og dubletter ikke skaber falske plateauer.
- Nabo-celler deler data, og derfor kan man ikke tælle "80 % grønne" som 80 % uafhængige beviser. Kravene til andelen af grøn/rød skal derfor kalibreres mod placebo-signaler, ikke sættes efter mavefornemmelse.

**Metode A: konfidensinterval mod omkostninger (enklest)**
- Grøn: den nedre grænse af cellens 90 %-interval (blok-bootstrap) for gennemsnitsafkast pr. handel ligger *over* omkostningen.
- Rød: den øvre grænse ligger *under nul*. Cellen taber med rimelig sikkerhed.
- Grå: alt andet (usikker).
- Fordel: let at forstå, og omkostninger er med. Ulempe: der er ingen korrektion for mange celler, så placebo-kalibreringen af PL-kravene er nødvendig.

**Metode B: FDR-farvning**
- t-værdien regnes pr. celle, og Benjamini–Hochberg bruges på alle celler i feltet.
- Grøn: signifikant positiv ved q = 10 %.
- Rød: signifikant *negativ* ved q = 10 %.
- Grå: resten.
- Fordel: tager højde for mange celler i feltet. Ulempe: afhænger af feltets størrelse. Store felter bliver strengere, hvilket kan være forklaringen på, at et højere niveau tillader mere rød.

**Metode C: placebo-percentiler og klynge-test (stærkest, dyrest)**
- For hver celle beregnes t-værdien for den ægte signalrække og for fx 500 cirkulært forskudte kopier. Mønstret bevares, men det flyttes i tid.
- Grøn: over 95 %-percentilen af placebo. Rød: under 5 %-percentilen. Grå: imellem.
- Derefter måles *størrelsen af den største sammenhængende grønne klynge*. Den sammenlignes med den største klynge i placebo. Det er samme idé som "cluster-based permutation tests" i hjerneforskning [Antagelse: kendt metode, kilde ikke åbnet].
- Fordel: nabo-korrelation er automatisk regnet med, og "plateau" får en p-værdi. Ulempe: 500 gange så meget regnetid.

**Hvordan Thomas kan afgøre de fem åbne punkter** (uændret princip, nu med tal):

| Punkt | Forsøg |
|---|---|
| Hvad betyder grå og rød? | Vælg A, B eller C ovenfor. |
| 20 % rød højere oppe og 0 % lavere nede? | Kør 200 placebo-signaler og 20 indplantede. Tæl for hvert niveau, hvor mange placebo der når det. Et højere niveau skal lukke *færre* placebo igennem end et lavere. Ellers er trappen ikke en trappe. |
| Resten ved "under 50 % grå"? | Prøv de tre varianter (resten grøn / resten grøn eller rød / fast rød-loft) og vælg den, der har lavest placebo-rate uden at miste over 20 % af de indplantede. |
| Er de største felter loftet? | Hvis PL7 stadig lukker over 1 % placebo igennem, mangler der et niveau eller en ekstra test. |
| Hvilket niveau er nok til dvale? | Det laveste niveau, hvor placebo-raten er ≤ den grænse, Thomas vælger (fx 1 %), og hvor mindst 80 % af de indplantede når op. |

---

## 9. AvgTrueRange-testen: hvad den beviser, og hvad den ikke beviser

**Testen** [Projekt: BESLUTNINGSLOG_2026-09-24.md; VIDENSLOG.md]: Filter 1 gav 620 forskellige signalrækker. De 5 manglende er netop dem, hvor 3·N1 = 5·N2, hvor filteret logisk aldrig kan være sandt.

**Den beviser (BEVIST):**
- At AvgTrueRange *ikke* har den totale fejl, hvor alle kombinationer bliver ens (sådan som MACD har).
- At de 5 manglende er forklaret af logikken. Det er et lille, positivt tegn på, at tallene opfører sig som forventet.

**Den beviser ikke:**
- At tallene er *rigtige*. En delvis sammenblanding af hukommelsen giver også forskellige rækker, bare forkerte. VIDENSLOG skriver det samme selv (2026-09-28).
- At *andre* funktioner (Average, RSI osv.) virker. Hver funktionstype skal testes for sig.
- At det virker på *alle* workspaces, datalængder og ved Max Bars Back-grænsen.

**Test der beviser, at tallene er rigtige** (i rækkefølge efter styrke):
1. **Uafhængig genberegning:** Eksportér de samme bars (OHLC for data1–3) fra TradeStation. Beregn filteret i Python ud fra formelteksten, *uden* at se EasyLanguage-koden. Sammenlign tændt/slukket bar for bar efter opvarmning. Krav: **100 % ens**.
2. **Løkke mod enkeltkald inde i TradeStation:** Byg for 10 udvalgte kombinationer en fil *uden løkke*, med én fast parameter pr. fil. Sammenlign med løkke-filens CSV. Det isolerer præcis den fejl, vi frygter. Det er billigt og kræver ingen ny beregningsmotor.
3. **Den håndregnede udgave** med separat hukommelse findes allerede for MACD [Projekt: BESLUTNINGSLOG_2026-09-18.md, git-commit 12120a8]. Den kan bruges som facit for filter 68.

Udvælg kombinationerne, så de dækker hjørnerne (N = 1 og N = 25), midten og tilfældigt valgte. Tag altid de kombinationer med, der ender i en strategi.

---

## 10. Stikprøvekontrol (metode, Konsulent 2 udfører)

**Tilføjet efter kritikrunden: krav til beviset for "Python = TradeStation"** (hvis Konsulent 3's Python-vej vælges):
1. Hvert filter, alle kombinationer, på et referencedatasæt, der dækker mindst ét år og både rolige og urolige perioder.
2. Samme bars: eksportfil med fingeraftryk (hash), samme session og tidszone.
3. Starttid, AntalBars og Afsluttet skal være 100 % ens efter opvarmningsvinduet. "Grænsetilfælde" (de to sider af uligheden ligger inden for 1e-9 relativt) tælles og vises. Er der flere end 1 pr. 10.000 signaler, dumper filteret.
4. Facit for gruppe A/C/D (MACD-typen) kan ikke være TradeStations løkke-fil, for den er forkert. Facit er rene enkeltkørsler uden løkke: mindst 5 kombinationer pr. filter (2 hjørner, midten, 2 tilfældige). Ved 0 fejl i ca. 650 tjek er under 0,5 % af kombinationerne forkerte med 95 % sikkerhed (3/n-reglen).
5. Mindst 20 filtre gentages på et andet marked eller en anden tidsramme.
6. Python-koden skrives uden at se EasyLanguage-koden.

- **Enheden er "kombination i filter", ikke "filter".** Fejlen kan ramme nogle kombinationer og ikke andre.
- **Pr. funktionstype** (MACD, RSI, StandardDev, Average, DMI, ChaikinMoneyFlow, AvgTrueRange, XAverage, CCI, dagsfunktioner): mindst 3 filtre × 5 kombinationer (2 hjørner, 1 midte, 2 tilfældige) testes med test 1 eller 2 i afsnit 9.
- **Filtre uden seriefunktion:** tilfældig stikprøve af 38 filtre × 2 kombinationer. Er der 0 fejl, er fejlraten under ca. 8 % med 95 % sikkerhed (1 − 0,92³⁸ ≈ 0,96 [Regnet]).
- **100 %** af de kombinationer, der bliver til en strategi (F1).
- Tilfældige valg sker med et fast, noteret seed, så de kan gentages.
- Ved fejl: stop, ret, ryd op og kør forfra [Projekt: VIDENSLOG.md 2026-09-24].

---

## 11. Regimeskift og genvækning fra dvale

**Problemet:** En strategi ligger i dvale i D år og skal vækkes. Er edgen der stadig? Et **regimeskift** er, når markedet skifter opførsel, fx fra roligt til uroligt.

**Regnestykket, der styrer alt** [Regnet]: Hvor stor chance er der for at *opdage*, at en edge er død (sand Sharpe = 0), med et ensidet 5 %-test på D års nye data (250 handler/år)?

| Backtest-per-handel-SR (efter halvering) | 0,5 år | 1 år | 2 år | 3 år |
|---|---|---|---|---|
| 0,047 (ca. årlig S = 0,75) | 13 % | 18 % | 28 % | 36 % |
| 0,095 (ca. årlig S = 1,5) | 28 % | 44 % | 68 % | 83 % |

**BEVIST:** Med 1–2 års dvale kan statistik sjældent afgøre, om en middelstærk edge lever eller er død. Genvækning kan ikke hvile på én test.

**Forslag til genvæknings-procedure** (tallene er forslag, Thomas vælger):
1. **Frosne parametre.** Strategien genkøres uændret fra passet. Den må ikke optimeres igen, for så bliver det et nyt forsøg.
2. **"Er den gået i stykker?"-test:** Welch t-test (en test, der sammenligner to gennemsnit) af per-handel-afkast *før* dvale mod *under* dvale. Ensidet, α = 5 %. Afvises "samme niveau", vækkes strategien ikke.
3. **Bayes-opdatering** (en måde at lægge ny viden oven i gammel): Start med backtestens edge, halveret. Læg de nye data oveni. Væk kun, hvis sandsynligheden for, at edgen efter omkostninger er over 0, er mindst fx 80 %. Den grænse fastsætter Thomas.
4. **Regime-tjek:** Markedets nuværende volatilitet (fx 20 dages realiseret udsving) og handelsvolumen skal ligge inden for 5.–95. percentil af det, backtesten dækkede. Ligger markedet uden for, har strategien aldrig været testet i den situation.
5. **Strukturbrud i hele serien:** En test for brud i gennemsnittet på tværs af hele perioden. En simpel udgave: CUSUM, som summerer afvigelser fra forventningen. Den kan også bruges senere i live-overvågning, men det er uden for denne opgave.
6. **Mange vækkes på én gang = nyt multiple testing.** Vækkes 20 strategier og vælges de 3 bedste, gælder korrektionen igen.

---

## 12. Angreb på mit eget første udkast

| Første udkast sagde | Hvad var forkert eller svagt |
|---|---|
| "380 filtre → 19 tilfældige vindere, bedste t ≈ 3" | Forsøgene var talt 4.000–25.000 gange for lavt. Jeg havde ikke set, at hvert filter har op til 625 kombinationer × 4 workspaces × retning × horisont. |
| "Mindst 30 handler i hold-out" | Uden styrke. 30 handler kan ikke skelne en realistisk edge fra nul (afsnit 4.4). Et fast tal var forkert. Det skal regnes ud fra formlen. |
| "100–200 handler i udviklingsdata" | Samme fejl. Kravet afhænger af SR og grænse. Ved realistiske tal kræves tusinder af handler. |
| "PBO under 0,2–0,3" | Tommelfingerregel uden grundlag. Den skal nu kalibreres med placebo. |
| "Flertallet af walk-forward-vinduer positive" | For svag. Tilfældighed giver 50 % positive. |
| "Plateau er ét krav blandt flere" | Rigtigt, men jeg overså, at hukommelsesfejlen *skaber* perfekte plateauer. Det er nu rettet med "fjern kopier først". |
| "Stikprøve af 38 filtre" | Forkert enhed. Fejlen rammer *kombinationer*, og den afhænger af *funktionstype*. |
| "Tredelt datasæt" | Jeg vidste ikke, hvor meget data der er. Med få år har man ikke råd til en tredeling med ærlig styrke. Det skal afklares først. |
| Kilderne | Jeg angav kilder, som jeg kun havde set i søgeresultater. Nu er de mærket "ikke bekræftet". |

---

## 13. Åbne punkter til Thomas

1. **Hvor mange års data og hvilke markeder** bruges? Det afgør, om fabrikken overhovedet kan finde andet end meget stærke edges (afsnit 4.2). Det vigtigste enkeltspørgsmål.
2. **Hvad er ét forsøg?** Skal step, retning og horisont fastlægges på forhånd for at få færre forsøg (afsnit 3)?
3. **Må N_eff måles** med korrelation eller placebo, før grænserne låses?
4. **Hvad er en event:** tænding eller hele den tændte periode? Hvornår starter handlen (næste bars åbning)?
5. **Farvemetode for plateau:** A, B eller C (afsnit 8), og hvilken placebo-rate er acceptabel pr. niveau?
6. **Hvor stort skal pengeskabet være**, når det kun kan kassere og ikke bevise (afsnit 4.4)?
7. **Modstriden om Average** (RawSignal266-filhovedet mod VIDENSLOG): hvad gælder?
8. **Dagsfunktionerne** (`CloseD` osv.): skal de alligevel testes med løkke mod enkeltkald?
9. **Genvækning:** Hvilken Bayes-sandsynlighed (fx 80 %) kræves, og hvor lang dvale-periode skal der være data for?
10. **Omkostningsmodel pr. marked** (ticks slippage + kurtage).
11. Uændret fra opgaven: plateau-trappen, hvor færdig EdgeFinder er, start af fuld kørsel, og MACD-filtrene. Min statistiske anbefaling om MACD: *ingen* strategi fra et filter, der er målt og ramt, kan passere F1. **Ændret efter kritikrunden:** Jeg er nu enig med Konsulent 2 i vej a (byg om). Output fra ramte filtre hører måske til en ukendt parameter og har derfor ingen statistisk værdi, heller ikke i karantæne.

---

## Kilder

Projektfiler (kun læst):
- /home/user/DetStoreProjekt/VIDENSLOG.md
- /home/user/DetStoreProjekt/Task_RawSignal_Creature_EdgeFinder_opgave.md
- /home/user/DetStoreProjekt/RawSignal_Creature/EdgeFinder_F5_SIGNAL.el
- /home/user/DetStoreProjekt/RawSignal_Creature/NOTER.md
- /home/user/DetStoreProjekt/RawSignal_Creature/BESLUTNINGSLOG_2026-09-18.md, _2026-09-24.md (09-22 kun søgt i)
- /home/user/DetStoreProjekt/RawSignal_Creature/OPGAVEBESKRIVELSE_RawSignal.md (uddrag)
- /home/user/DetStoreProjekt/RawSignal_Creature/RawSignal/RawSignal069.el og RawSignal266.el
- /home/user/DetStoreProjekt/RawSignal_Creature/Program/indlaes_csv.py (uddrag) og generer.py (søgt i)

Internet: alle kilder er **[Net, ikke bekræftet]**. Netværket blokerede at åbne siderne i denne session. Kun titler og resuméer fra søgeresultater er set:
- Bailey & López de Prado, "The Deflated Sharpe Ratio", Journal of Portfolio Management 40(5), 2014: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551
- Bailey, Borwein, López de Prado & Zhu, "The Probability of Backtest Overfitting", Journal of Computational Finance: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253
- Harvey, Liu & Zhu (2016), "...and the Cross-Section of Expected Returns", Review of Financial Studies (resumé): https://foxholm.com/q/research/harvey-liu-zhu-cross-section/
- Benjamini & Hochberg (1995), "Controlling the False Discovery Rate", JRSS B 57(1): https://academic.oup.com/jrsssb/article/57/1/289/7035855
- White (2000), "A Reality Check for Data Snooping", Econometrica 68: https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0262.00152

**Hvad mangler (ærligt):** N_eff er skønnet, ikke målt. Datalængde og marked er ukendte, så alle krav er givet som formler og scenarier. Kilderne er ikke åbnet. Jeg har ikke læst BYGGEVEJLEDNING, ARBEJDSBESKRIVELSE eller hele generer.py.


# Del 2 – EasyLanguage: kvalitet, EdgeCruncher og MultiCharts (Konsulent 2, runde 2)

*Erstatter del 2 fra første runde. Kun råd. Intet i projektet er ændret.*

**Mærker:**
- [Projekt: fil:linje] = står i projektets egne filer. Jeg har læst dem selv.
- [Rapport] = står i statusrapporten.
- [Net: kilde] = en side, jeg selv har åbnet og læst.
- [Net, ikke bekræftet] = jeg har kun set søgemaskinens uddrag, ikke selve siden.
- [Antagelse: hvorfor] = min egen vurdering.

**Sikkerhed – tre trin, der bruges i hele teksten:**
- **BEVIST**: målt i projektet eller står direkte i koden.
- **SANDSYNLIGT**: passer med alt, vi ved, men er ikke målt.
- **UKENDT**: vi ved det ikke.

**Vigtig begrænsning ved kilderne på nettet:** TradeStations og MultiCharts' officielle hjælpesider er blokeret fra dette arbejdsmiljø. Det gælder help.tradestation.com, cdn.tradestation.com og multicharts.com. Jeg har prøvet dem alle, også via et arkiv. Derfor kan jeg **ikke** levere officielle kilder, som jeg selv har åbnet. Alt, hvad jeg siger om platformenes indre virkemåde, er enten målt i projektet eller mærket [Net, ikke bekræftet]/[Antagelse]. Det er et åbent punkt: nogen med adgang skal læse de officielle sider (se afsnit 8).

**Afhængighed:** Jeg bygger på Konsulent 1's definition af "færdig strategi", punkterne F1–F10. Hvor et tal mangler fra K1, står der [Afhænger af K1].

---

## 0. Kort sagt – de fem vigtigste fund

1. **Kontrollen i TDE godkender filer, som TradeStation selv har advaret om.** TDE er TradeStations program, hvor koden skrives og tjekkes. Programmet markerer en fil som "Pass", når der står "0 error(s)", uanset hvor mange advarsler der er [Projekt: `Program/tde/verify-one.ps1:277`]. Men netop MACD-filen gav 3 advarsler af typen "A series function should not be called more than once with a given set of parameters" [Projekt: `BYGGEVEJLEDNING_RawSignal.md` afsnit 7; `BESLUTNINGSLOG_2026-09-18.md:90-93`]. Advarslen gemmes i Note-feltet, men ingen reagerer på den. **BEVIST** (koden). Advarslen er ikke nok til at fange alle ramte filer (se 2.3), men den er gratis og bør altid løfte et rødt flag.
2. **MACD-målingen passer med en bestemt forklaring.** Alle 625 kombinationer gav præcis de samme 4.918 signaler [Projekt: `NOTAT_til_BYGGEVEJLEDNING_RawSignal.md`]. Det passer ikke med "delt hukommelse, der blandes" – så ville tallene være forskellige og forkerte. Det passer med, at TradeStation regner en *series function* **én gang pr. bar** og derefter giver det samme tal tilbage ved hvert gennemløb af løkken. Det gælder uanset N1 og N2. **SANDSYNLIGT**. Følgen: parametersøgningen er ikke "støjfyldt" for disse filtre, den er **helt tom**. Og selv en løkke med kun ét parametersæt kan regne med en forkert værdi. Det kan testes billigt (afsnit 4).
3. **Faren er ikke kun "kendte seriefunktioner".** Den gælder enhver funktion, der får et **udtryk, som afhænger af løkkens N1/N2**, som sin "serie"-indgang. Et eksempel er `Average( MACD(...N1...), 9)` [Projekt: `RawSignal/RawSignal069.el`, filterformlen]. Listen, der styrer advarslen i filernes hoved, er en navneliste med 10 funktioner [Projekt: `Program/formel.py:22-25`]. Filtre med CCI (18 stk.), PercentR, Highest/Lowest-kombinationer m.fl. får derfor **ingen advarsel** [Projekt: `Program/generer.py:79`; `BESLUTNINGSLOG_2026-09-24.md:60-62`]. **BEVIST** for navnelisten, **UKENDT** om de er ramt.
4. **Opvarmning er et større problem end Max Bars Back.** Funktioner med tilbagekobling (eksponentielle gennemsnit, Wilder-udglatning) skal bruge 2–5 gange deres længde, før de har "glemt" deres startværdi. MACD med langsom længde 600 har stadig 3,6 % af startfejlen efter 1.000 bars. Ved 1 %-præcision kræver den 1.382 bars (regnestykke i 1.4). `max_bars_back.py` regner kun "længde = behov" [Projekt: `Program/max_bars_back.py:221-229`]. **BEVIST** som regnestykke. **SANDSYNLIGT** at det rammer de første signaler i hver fil.
5. **CSV-filen fortæller ikke, hvilket marked og hvilken tidsramme den kommer fra.** RunID er filterets navn [Projekt: `NOTAT_til_BYGGEVEJLEDNING_RawSignal.md`, punkt 5]. Filnavnet er fast, og `FileDelete` sletter uden varsel [Projekt: `Program/generer.py:170`]. Kører samme filter i to arbejdsområder (workspaces), eller køres det igen før flytning, overskrives data **uden fejl**. Oplysningen om arbejdsområdet findes kun i det navn, EdgeFinder giver filen bagefter [Projekt: `Task_RawSignal_Creature_EdgeFinder_opgave.md`]. **BEVIST** (koden). Risikoen er reel, fordi der er fire arbejdsområder [Projekt: `RawSignal_Creature/NOTER.md`, "Navngivning"].

---

## 1. Fejlliste ud fra den rigtige kode

Sådan virker det i dag: Generatoren `generer.py` bygger for hvert filter en strategi og en kontrol-ShowMe (et lille program, der kun tegner signalet på grafen). I strategien gennemløbes alle kombinationer af N1 og N2 med `While`-løkker **på hver bar**, og formlen står inde i løkken [Projekt: `Program/generer.py:235-256`]. ShowMe'en regner kun ét parametersæt og **uden løkke** [Projekt: `Program/generer.py:296`]. Det er vigtigt, for det giver os en færdig kontrol inde i platformen (afsnit 4).

### 1.1 Seriefunktion kaldt i løkke – MACD-typen
- **Set i koden:** `RawSignal069.el` kalder MACD tre gange i én betingelse inde i to løkker (N1, N2) [Projekt: `RawSignal/RawSignal069.el`, kroppen]. `RawSignal020.el` kalder `DMIplus( N1 * 10 )` og `DMIminus( N1 * 10 )` i en løkke [Projekt: `RawSignal/RawSignal020.el:81`].
- **Målt:** 069: alle 625 kombinationer er identiske [Projekt: NOTAT, punkt 7]. 020 "skrev slet ingen fil" [Projekt: BYGGEVEJLEDNING afsnit 8]. Årsagen er **UKENDT**. Min hypotese: hvis funktionen regnes én gang ved bar-start, er N1 = 0 på første bar (variablen starter på 0), og så er længden 0. Det er [Antagelse] og skal testes.
- **Hvorfor farligt:** Det ligner et rigtigt resultat. Det ødelægger hele plateau-analysen (K1's F5), fordi alle naboceller bliver ens og ligner et "perfekt plateau". **Det er den værst tænkelige fejl for netop denne fabrik:** den laver falske plateauer.
- **Opdages:** se afsnit 2 og 4.

### 1.2 Serie-indgang, der afhænger af løkken
- **Set i koden:** `Average( MACD(C, N1*2, ...), 9)` [Projekt: `RawSignal069.el`]. `Average` skal bruge MACD-værdien 1–8 bars tilbage. Platformen gemmer historikken for **kaldstedet** (stedet i koden, hvor funktionen kaldes), ikke for hver kombination [Antagelse: følger af samme mekanisme som 1.1].
- Derfor er `Average(Close, N1)` sandsynligvis i orden, fordi Close's historik er den samme for alle N1. Det passer med, at 266 er målt i orden [Projekt: NOTAT, punkt 7]. `Average( RSI(C, N1), N2)` eller `Highest( MACD(...N1...), N2)` er derimod sandsynligvis forkerte.
- **Opdages:** Automatisk læsning af formlen: find alle funktionskald, hvor en indgang indeholder N1/N2 **og** selv er et funktionskald eller en bar-reference.

### 1.3 Advarselslisten er en navneliste
- **Set i koden:** Kun de 10 navne i `SERIEFUNKTIONER` udløser advarslen [Projekt: `Program/formel.py:22-25`, `Program/generer.py:79`]. CCI (18 filtre), ChaikinMoneyFlow (8), PercentR, CountIf, SquareRoot og Pivot* er kendt som "ukendte" for Max Bars Back [Projekt: `BESLUTNINGSLOG_2026-09-24.md:60-62`]. Men kun ChaikinMoneyFlow står på advarselslisten.
- **Status:** Om CCI osv. er ramt, er **UKENDT**. Hvis de er ramt, står der ingen advarsel i filen, og den tavse fejl er helt tavs.

### 1.4 Opvarmning af funktioner med tilbagekobling
- **Set i koden:** Max Bars Back-behovet regnes som "største længde + indre længder" [Projekt: `Program/max_bars_back.py:221-229`]. Det er rigtigt for glidende vinduer (Average, Highest). Det er for lidt for funktioner, der husker sig selv.
- **Regnestykket, trin for trin:** Et eksponentielt gennemsnit (EMA) med længde L bruger vægten a = 2/(L+1). Efter k bars er der (1−a)^k tilbage af startfejlen. Skal der højst være 1 % tilbage, er k = ln(0,01)/ln(1−a).
  - L = 600 (MACD's langsomme længde ved N1=25, N2=25): a = 2/601 = 0,00333, og k = 4,605/0,00334 = **1.382 bars**. Efter 1.000 bars er der 0,99667^1000 = **3,6 %** tilbage.
  - Wilder-udglatning (bruges typisk i RSI/DMI) har a = 1/L. Ved L = 250 (020, N1=25) er der 0,996^1000 = **1,8 %** tilbage efter 1.000 bars. 1 % kræver **1.149 bars**.
  - (Regnet i Python i scratchpad. Hvilken udglatning TradeStation præcis bruger i RSI/DMI, er [Antagelse] – det skal læses i funktionens kode i TDE.)
- **Endnu værre, SANDSYNLIGT:** Hvis funktionen først begynder at regne ved den første bar *efter* Max Bars Back (CurrentBar = 1), giver Max Bars Back ingen opvarmning overhovedet. Så er de første ~1.400 bars signaler for lange EMA'er upræcise, uanset indstillingen [Antagelse: kendt opbygning af XAverage; ikke bekræftet mod officiel kilde].
- **Opdages / håndteres:** Den bedste løsning er et fast "opvarmningsvindue" pr. filter, udregnet af generatoren med formlen ovenfor. RawSignal-Analyse skal så kassere signaler i det vindue. Grænsen (1 % eller 0,1 %) fastsætter K1.

### 1.5 Blandede datastrømme (Data1 mod Data2)
- **Set i koden:** Nogle formler har ingen `of data(...)`: `AbsValue(Open[1] - Close[1]) > (0.1 * N2) * (High[1] - Low[1])` [Projekt: `RawSignal/RawSignal174.el:79`]. `close of data(DataFilter_A) > OpenD(0)` [Projekt: `RawSignal/RawSignal126.el:44`]. Her er `OpenD(0)` taget fra **Data1**, mens Close er fra Data2. Strategien tjekker kun, at Data1 og Data2 har samme bar-type og interval [Projekt: `Program/generer.py:166-168`]. Den tjekker ikke **symbol** eller **sessionsskabelon**.
- **Hvorfor farligt:** Har Data1 et andet symbol eller en anden session, sammenlignes æbler med pærer. Der kommer ingen fejl.
- **Status:** Om det sker i praksis, er **UKENDT**, fordi arbejdsområderne ikke er dokumenteret i projektet. Tjekket i `Once`-blokken bør udvides til symbol og session (Thomas beslutter).

### 1.6 Tidsstempel = bar-slut, og kan blive læst som bar-start
- **Set i koden:** Starttid = `Date/Time of data(DataFilter_A)` formateret som "yyyy-MM-dd HH:mm" [Projekt: `Program/generer.py:177-179`]. I TradeStation er en bars tid normalt **slut**-tidspunktet [Antagelse: almindelig TS-konvention, ikke bekræftet mod officiel side].
- **Hvorfor farligt:** Signalet kendes først, når baren lukker. Regner EdgeFinder afkastet fra barens **åbning** eller fra "Starttid" som et starttidspunkt, kigger den én bar ind i fremtiden. Det er klassisk look-ahead (at bruge noget, man ikke kunne vide på det tidspunkt), og det giver falske edges.
- **Også:** Tidszone og sommertid står ikke i filen. Sekunder mangler, men det betyder ikke noget ved minut-bars.
- **Status:** Look-ahead-risikoen er **SANDSYNLIG**, hvis det ikke er beskrevet eksplicit i EdgeFinder. Hvordan EdgeFinder læser tiden, er **UKENDT**, for den er ikke bygget. Anbefaling: skriv reglen "handel tidligst ved åbningen af næste bar" ind i EdgeFinder-metoden (K1 godkender).

### 1.7 Filnavn, overskrivning og manglende oprindelse
- **Set i koden:** Fast filnavn står fire steder, og `FileDelete` kører i `Once` [Projekt: `Program/generer.py:11-13, 170-171, 269-272`]. RunID = filterets navn. CSV'en indeholder hverken symbol, tidsramme eller kørselsdato.
- **Hvorfor farligt:** To kørsler af samme filter overskriver hinanden uden fejl. Glemmer EdgeFinder at flytte filen, slettes den gamle ved næste kørsel. NOTAT'et nævner netop dette [Projekt: NOTAT, punkt 5]. Bagefter kan man ikke se på selve filen, hvilket arbejdsområde den kom fra.
- **Anbefaling:** Lad strategien skrive symbol, BarInterval og sessionsnavn i overskriftslinjen, så filen bærer sin egen oprindelse. Det er en ændring af generatoren, så Thomas beslutter.

### 1.8 Decimal-løkker kan springe den sidste værdi over
- **Set i koden:** Decimalparametre tælles op med gentagen plus i en `While`-løkke [Projekt: `Program/generer.py:243, 253`]. Python regner derimod antal trin med præcise decimaltal [Projekt: `Program/formel.py:88`].
- **Regnet:** Med kommatal i computeren giver 0,1 + 0,1 + 0,1 = 0,30000000000000004. Det er mere end 0,3, så løkken stopper én for tidligt. Jeg har prøvet det i Python: Fra 0,1 / Til 0,3 / Step 0,1 giver **2** gennemløb, ikke 3. Fra 0,5 / Til 2,5 / Step 0,1 giver **20**, ikke 21.
- **Status i dag:** De 8 decimalfiltre bruger trin på 0,25 [Projekt: BYGGEVEJLEDNING, linje 61]. 0,25 kan gemmes præcist i computeren, så i dag er det **ufarligt (BEVIST ved regning)**. Men generatoren forhindrer ikke et trin på 0,1. Den sidste kombination vil så mangle uden fejl. Et billigt værn: generatoren afviser trin, som computeren ikke kan gemme præcist, eller løkken tælles med heltal.

### 1.9 Verify-trinnet
- **Set i koden:** "Pass" = regulært udtryk for "0 error(s)". Advarsler tæller ikke [Projekt: `Program/tde/verify-one.ps1:276-277`]. Hele panelteksten gemmes som Note.
- Verify er ikke et bevis for rigtige tal. Det står allerede i projektet [Projekt: BYGGEVEJLEDNING afsnit 8], og det er rigtigt.

### 1.10 Mindre, men reelt
- **Arrays med fast størrelse 25:** Generatoren stopper, hvis grænsen overskrides [Projekt: `Program/formel.py:93-94`]. Godt – den fejl er ikke tavs.
- **Dubletter i formlen** (fx `maxlist(2, floor(N2/2))` giver kun 11 forskellige værdier ud af 25) [Projekt: `RawSignal069.el`, "KENDT PROBLEM 3"]. Det er ikke en fejl, men det **skal** med i K1's optælling af forsøg (F3). Ellers tælles 625 forsøg, hvor der kun er 275 reelle.
- **IntrabarOrderGeneration:** Generatoren slår det ikke til, og RawSignal-filerne handler ikke. Mit punkt om det i første runde var derfor irrelevant her. Det bliver først relevant i EdgeCruncher.

---

## 2. MACD-mekanismen – hvad vi ved, og hvad vi ikke ved

### 2.1 Fakta fra projektet (BEVIST)
- Alle 625 kombinationer i 069 gav **præcis** de samme 4.918 signaler [Projekt: NOTAT, punkt 7].
- 266 (`Average(TrueRange of data B, N1)` i løkke) gav forskellige signaler for alle 25 N1 (528–1.453) [Projekt: NOTAT].
- Nyt filter 1 (AvgTrueRange, N1+N2) gav forskellige rækker for 620 kombinationer. De 5, der mangler, er netop dem, hvor formlen aldrig kan være sand [Projekt: `BESLUTNINGSLOG_2026-09-24.md:88-91`].
- TDE advarede 3 gange for 069 og 2 gange for 020, men 0 gange for 266 og 004 (ChaikinMoneyFlow) [Projekt: BYGGEVEJLEDNING afsnit 7].

### 2.2 Den bedste forklaring (SANDSYNLIGT)
TradeStation skelner mellem **simple functions** (regner kun, når de kaldes) og **series functions**. En series function husker sine egne tidligere værdier og **køres på hver bar, også hvis den står i en if-sætning** [Net, ikke bekræftet: TradeStation Help "About Functions", https://help.tradestation.com/10_00/eng/tsdevhelp/elword/el_definitions/about_functions.htm – kun søgeuddrag, siden er blokeret]. For at kunne det må platformen regne funktionen ved siden af den almindelige kodegang, én gang pr. bar og pr. kaldsted. Står kaldet i en løkke, får hvert gennemløb samme gemte resultat. Parameterværdien er den, N1/N2 havde, da platformen regnede den [Antagelse].

Det forklarer alle fire fakta:
- **MACD (series, via XAverage):** ét tal pr. bar → 625 ens rækker. ✔
- **Average og AvgTrueRange (simple, glidende vindue):** regnes ved hvert kald med den rigtige længde. Deres indgang (TrueRange, Close) afhænger ikke af N → forskellige og sandsynligvis rigtige rækker. ✔
- **TDE's advarsel** ("should not be called more than once with a given set of parameters") kommer kun, når samme series function kaldes flere gange. ✔
- 004/ChaikinMoneyFlow og 266 gav ingen advarsel. Det passer med, at de ikke er series functions – eller med, at advarslen ikke fanger alt. **UKENDT**.

**Den forklaring, projektet selv bruger** ("hukommelsen deles, og tallene blandes") [Projekt: `NOTER.md` punkt 3], ville give *forskellige, men forkerte* rækker. Målingen viser *ens* rækker. Forskellen betyder noget: med min forklaring regnes funktionen måske med N-værdier **uden for løkkens område** (fx N1 = N1_Til + Step efter løkkens sidste gennemløb). Så kan også filer med kun én kombination (Fra = Til) være forkerte. Det skal testes (afsnit 4, test T1).

### 2.3 Hvilke funktioner er i risiko?
| Gruppe | Eksempler i filtrene | Vurdering |
|---|---|---|
| A. Tilbagekoblede series functions | MACD, XAverage, sandsynligvis RSI, DMIplus/DMIminus/ADX | **Behandl som ødelagte i løkke**, indtil det modsatte er målt. 069 BEVIST, 020 mistænkt (ingen fil). |
| B. Glidende vinduer på prisdata | Average(C,N), AvgTrueRange(N), Highest/Lowest(High,N), StandardDev(C,N) | **SANDSYNLIGT i orden** (266 og ATR målt). Skal stadig bestå test T1 pr. funktionstype. |
| C. Vindue på et udtryk, der afhænger af N | Average(MACD(..N..),9), Highest(RSI(..N..),N2) | **SANDSYNLIGT forkert**, selv hvis den ydre funktion er simpel. |
| D. Ukendte | CCI, ChaikinMoneyFlow, PercentR, CountIf, Pivot* | **UKENDT**. Behandl som A, indtil T1 er bestået. |
| E. Ingen parametre (77 filtre) eller kun rene prisreferencer | `True`-lignende, OpenD, Close[1] | Ikke berørt af løkkefejlen. Men 1.5 og 1.6 gælder stadig. |

Hvilke funktioner i TradeStations bibliotek der er series eller simple, kan læses direkte i TDE: hver funktions egenskaber viser dens type [Antagelse: sådan er TDE bygget; skal bekræftes lokalt]. **Det er den hurtigste og mest sikre kilde, og den koster minutter, ikke dage.** Den lokale session bør lave en liste over alle funktioner, der bruges i de 380 formler, med deres type.

### 2.4 Robuste måder at skrive det på (mønstre, ikke kode)
1. **Ét parametersæt pr. kørsel.** Ingen løkke. N1/N2 sættes som faste inputs, og hver kombination er en ny backtest. Platformen er bygget til det, så det er den mest sikre løsning. Men: 128 filtre × 625 + 176 filtre × 25 = **84.400 kørsler** for alle parametriserede filtre. Ved 30–60 sekunder pr. kørsel [Antagelse: tiden er ikke målt] er det **700–1.400 maskintimer**. Kun realistisk for gruppe A/C/D, ikke for alle.
2. **Udrullet kode ("ét kaldsted pr. kombination").** Generatoren skriver én linje pr. kombination med faste tal i stedet for en løkke. Så har hvert kald sin egen hukommelse, som platformen er designet til [Antagelse]. 069 ville få 275 unikke kombinationer × 3 kald = 825 kaldsteder. **UKENDT:** om TDE kan kompilere så store filer, og hvor hurtigt de kører. Skal prøves på 069 først.
3. **Egen hukommelse pr. kombination i arrays ("håndregnet").** For hver kombination gemmes funktionens tilstand i et array, og den opdateres præcis én gang pr. bar. Et EMA fortsætter fx fra sin egen forrige værdi med sin egen vægt. Startværdien skal sættes på samme måde som i platformens egen funktion, ellers giver sammenligningen falske fejl. Den løsning findes allerede for MACD [Projekt: BYGGEVEJLEDNING afsnit 7, commit `12120a8` – jeg har ikke åbnet commit'en]. Den skal laves én gang pr. funktionstype (maks. ca. 10 typer), ikke pr. filter.
4. **Glidende vinduer (gruppe B) må blive i løkken**, hvis T1 bekræfter det pr. funktionstype.

5. **Python som regnemaskine med TradeStation som facit (K3's forslag, del 3 afsnit 4.2).** TradeStation kører én facit-backtest pr. filter og pr. workspace-type. Python regner alle andre datasæt. Et filter må først bruges i Python, når signalerne er identiske med facit.

**Rettet efter kritikrunden – jeg er blevet overbevist af K3:** Mønster 5 er bedre end at køre 84.400 kørsler med mønster 1. Det giver ca. 380 × 4 workspace-typer = 1.520 TradeStation-kørsler i stedet for 84.400. Det giver også K1's uafhængige genberegning gratis. Men der er to vigtige forbehold:
- **(a) Facit for gruppe A/C/D kan ikke være dagens løkke-fil**, for den er netop forkert. Facit skal laves uden løkke: mønster 1 eller 2 for 3–5 udvalgte kombinationer pr. filter.
- **(b) Python kan ikke uden videre ramme TradeStations tal** i de tilfælde, der er nævnt i `k2_kritik.md` (a):
  - sessioner og helligdage,
  - OpenD/CloseD,
  - Data1/Data2/Data3 på forskellige tidsrammer,
  - startværdien i XAverage/Wilder,
  - lukkede formler som CCI, PercentR og Pivot,
  - grænsetilfælde ved afrunding.

  Her skal facit-sammenligningen være pr. workspace-type, ikke kun ét referencedatasæt.

Min anbefaling er nu:
- mønster 5 som hovedvej,
- gruppe B må blive i løkke i TradeStation-facit (efter T1),
- gruppe A/C/D får facit via mønster 1/2 på udvalgte kombinationer,
- mønster 3 bruges kun, hvis Thomas vil beholde alt i EasyLanguage (fx af hensyn til MultiCharts).

**Thomas afgør, hvilken vej der vælges** (åbent punkt i opgaven).

---

## 3. AvgTrueRange-testen – hvad beviser den?

**Hvad den viser (BEVIST):** Parametrene når frem til funktionen i hvert gennemløb. Hvis ATR var ramt af MACD-fejlen, ville alle rækker være ens. Det sigende ved testen er, at præcis de 5 "umulige" kombinationer (3·N1 = 5·N2) mangler. Det viser, at N1 og N2 faktisk bruges forskelligt [Projekt: `BESLUTNINGSLOG_2026-09-24.md:88-91`]. Det er mere end "rækkerne er forskellige", og det er et godt tegn.

**Hvad den ikke viser:**
- at ATR-tallene er **rigtige** (rigtig definition, rigtig datastrøm, rigtig længde),
- at der ikke er en forskydning på én bar,
- at der ikke er en opvarmningsfejl (1.4).

Forkerte tal kan også være forskellige fra hinanden. Det står allerede ærligt i Videnslog [Projekt: `VIDENSLOG.md`, 2026-09-28].

**Tests, der ville bevise at tallene er rigtige (i stigende styrke):**
1. **Løkke mod enkeltkørsel (T1):** 3 kombinationer (lav, midt, høj). Løkke-filens signaler for (N1,N2) skal være *identiske* med en kørsel uden løkke med samme N1,N2. Bevis for, at løkken ikke ændrer noget.
2. **Uafhængig genberegning (T2):** Prisbarerne eksporteres fra samme chart. Python regner True Range og gennemsnittet ud fra lærebogens formel, skrevet uden at se TradeStations kode, og laver signalrækken. Kravet er, at Starttid og AntalBars er identiske for alle signaler efter opvarmning. Undtagelsen er "grænsetilfælde", hvor de to sider af uligheden ligger tættere end en lille tolerance. De tælles og vises for sig [tolerancen: Afhænger af K1].
3. **Kendte svar (T3):** Byg et kunstigt prisforløb, hvor svaret kan regnes i hånden (fx konstant spænd, så ATR = konstant). Filteret skal give præcis det forventede.

T1 beviser "løkken er uskadelig". T2 + T3 beviser "tallene er rigtige". Først når alle tre er bestået, er ATR-typen **BEVIST** i orden.

---

## 4. Kontrolplanen – konkret for dette projekt

**Princip:** Hvert filter skal have en status, som en maskine sætter: *ikke kontrolleret / bestået / fejlet*. Status gemmes adskilt fra produktionsdata [Rapport]. Hvordan og hvor den gemmes, er K3's område. Alle nye tabeller eller kolonner kræver, at Thomas først ser og godkender den præcise SQL [Rapport]. Et fejlet filter rettes ved at rydde op og bygge forfra [Projekt: `VIDENSLOG.md`, 2026-09-24].

| Trin | Hvad køres | Hvem | Bestået når | Tid (skøn) |
|---|---|---|---|---|
| **K0. Funktionstyper** | Liste over alle funktioner i de 380 formler og deres type (series/simple), aflæst i TDE | Lokal session | Alle funktioner har en type | 1–2 timer [Antagelse] |
| **K1. Klassifikation** | Python læser `filter_case.filtere` og placerer hvert filter i gruppe A–E (afsnit 2.3). Samtidig flag for: mangler `of data`, dags-/sessionsfunktion, decimaltrin, udtryk med N som serie-indgang | Python, ingen TradeStation | Hvert filter har gruppe + flag. Stikprøve på 20 filtre læst af et menneske | Minutter at køre |
| **K2. Advarsler** | Læs Note-feltet fra Verify for alle filer. Advarsler > 0 → mindst gruppe A | Python | Ingen filer med advarsel står som "i orden" | Minutter |
| **K3. T1 løkke mod enkeltkørsel** | Pr. **funktionstype** (ikke pr. filter): 1 filter, 3 kombinationer. Løkke-fil (Fra = Til) og ren enkeltfil | TradeStation | 100 % ens Starttid/AntalBars efter opvarmning | ca. 15–20 typer × 4 kørsler = 60–80 kørsler ≈ 1 dag [Antagelse: tid pr. kørsel ukendt] |
| **K4. T2 Python-genberegning** | Vælges mønster 5: alle filtre (Python *er* så regnemaskinen). Ellers: alle filtre i gruppe B + stikprøve af E. Samme prisbarer fra samme chart, pr. workspace-type | Python + eksport fra TS | Identiske signaler; grænsetilfælde under K1's grænse | Første filter: dage (eksport + formler). Derefter minutter pr. filter |
| **K5. Invarianter** | Gratis tjek på alle CSV'er: (a) samme fil to gange → samme kontrolsum (hash); (b) matematiske dubletter (fx N2 = 1–5 i 069) **skal** være ens; (c) forskellige længder **må ikke** alle være ens; (d) "umulige" kombinationer skal være tomme | Python | Alle fire holder | Minutter pr. filter |
| **K6. Oprindelse** | CSV'ens symbol/interval/session (når 1.7 er løst) stemmer med arbejdsområdet | Python | Ens | Sekunder |

**Rækkefølgen er vigtig:** K0 → K1 → K2 først, før den fulde kørsel. De koster næsten intet og fortæller, **hvor mange** filtre der er i fare. I dag ved vi det ikke [Rapport]. BYGGEVEJLEDNING tæller 185 af 381 uden kendte seriefunktioner [Projekt: afsnit 7], men den tælling bygger på den ufuldstændige navneliste.

**Hvad "bestået" giver:** K1's F1 ("teknisk rent signal") er opfyldt, når K3–K6 er bestået for filteret eller dets funktionstype.

**De MACD-ramte filtre – mulige veje (Thomas afgør):**
- a) Byg dem om med mønster 3 (eller 2) og kør dem gennem K3–K5. *Min anbefaling.*
- b) Kør dem som nu, men i karantæne. De må ikke gå videre før a).
- c) Tag dem ud af første runde.

Uenigheden med K1 er den samme som før: K1 accepterer b og c, jeg anbefaler a. Men alle er enige om, at de **ikke** må godkendes uden kontrol.

**Hvor stikprøven til Python er uafhængig:** Python-koden skrives af en anden session end den, der byggede generatoren, og kun ud fra formlen i databasen og lærebogens definition [Antagelse: ellers kopieres misforståelsen].

---

## 5. EdgeCruncher – holdt op mod Thomas' egen proces

**Hvad Thomas selv har skrevet** [Projekt: `Task_RawSignal_Creature_EdgeFinder_opgave.md`]:
- RawSignal Creature: hent filter → omskriv → verificér → journal.
- RawSignal-analyse (ikke beskrevet).
- EdgeFinder: læs journal → **gå til TradeStation, load workspace, sæt indstillinger, load RawSignal** → hent CSV, kontroller for fejl ("ved fejl, stop proces og meld fejl") → gem med navnet `RawSignal(Number_WorkSpace_RunDate)` → event-studie → Passed/Failed.
- EdgeCruncher: "ikke helt". MultiCharts bagefter.

**Hvad det betyder for mit forslag:**
- **Rettelse af mit første udkast:** Det er **EdgeFinder**, der kører backtesten i TradeStation og henter CSV'en – ikke RawSignal Creature, som kun verificerer. Kontrolplanens K4–K6 hører derfor naturligt til i EdgeFinders trin "kontroller for fejl". Det trin mangler i dag en definition af, hvad "fejl" er. K5 er et konkret bud.
- **Hvor mit forslag passer:** RawSignals er **hændelser, ikke handler** [Projekt: `NOTER.md`, "Hvad en RawSignal er"]. EdgeFinder måler, hvad prisen gør efter hændelsen. Der er altså et hul mellem "der er en edge efter hændelsen" og "en strategi med indgang, udgang og omkostninger". Det hul er den oplagte opgave for EdgeCruncher. Det passer med rækkefølgen i Thomas' fil.
- **Hvor det ikke passer, eller vi ikke ved det:** Thomas har ikke skrevet noget om EdgeCruncher. Den kan lige så vel være tænkt som et led, der **kombinerer** flere filtre (fx Filter1 AND Filter2) – filterkolonnerne hedder "Filter1_N1", hvilket antyder, at der kan komme et Filter2 [Projekt: `NOTER.md`, kolonnetabel; Antagelse]. Det er **UKENDT** og et åbent punkt.

**Forslag til EdgeCruncher (revideret, skal bekræftes af Thomas):**
- **Input:** et signal, der har bestået EdgeFinder (Passed), med sit plateau, sit arbejdsområde og sin CSV-oprindelse.
- **Opgave 1 – strategi:** Byg en rigtig TradeStation-strategi ud fra signalet med et lille, **fast** menu-kort af udgange: tidsudgang, fast stop, fast mål, udgang ved dagens slut. Indgang tidligst ved næste bars åbning (1.6). Her bliver IntrabarOrderGeneration relevant: den skal være **slået fra**, og stop/mål i samme bar skal håndteres og tælles [Antagelse].
- **Opgave 2 – kombination (kun hvis Thomas vil):** Filter1 AND Filter2. Advarsel: antallet af forsøg eksploderer. 380 × 380 par × plateauer skal alle tælles til K1's F3 og straffes i F4.
- **Samme løkkeproblem gælder her:** EdgeCruncher må ikke bygge strategier, hvor seriefunktioner kaldes i løkker. Brug mønstrene fra 2.4.
- **Rører aldrig pengeskabet** (K1's hold-out-data, F2/F9). Pengeskabs-testen køres af et separat trin, som EdgeCruncher ikke styrer.
- **Output – et pas til dvale-lageret** (K1 bestemmer indholdet, K3 hvordan det gemmes): filter-ID og version, generator-version, arbejdsområde (symbol/interval/session), parametre, plateau, opvarmningsvindue, antal forsøg (F3), resultater for F4–F10, kontrolstatus K0–K6, strategiens kildekode, og hvilken platform og version den er verificeret på (TS / TS+MC).
- **Journal:** Thomas' mønster "Passed/Failed" bruges også her. EdgeCruncher skriver "klar til K1-vurdering", aldrig "godkendt".

---

## 6. Porting til MultiCharts

**Kildesituation:** De officielle MultiCharts-sider kunne ikke åbnes herfra (blokeret). Det følgende bygger på projektets kode og på uddrag, jeg ikke har kunnet bekræfte. **Første skridt i porteringen skal være, at nogen læser MultiCharts' officielle wiki om PowerLanguage, series functions og Max Bars Back.**

**Hvad MultiCharts siger om sig selv** [Net, ikke bekræftet: MultiCharts, "PowerLanguage is EasyLanguage-compatible", https://www.multicharts.com/features/easylanguage/]: klassisk EasyLanguage virker for det meste, objekt-orienteret EasyLanguage gør ikke, og .ELD-filer kan importeres. Projektets filer er klassisk EasyLanguage uden objekter. Det er godt.

**Hvad der i projektets nuværende kode sandsynligvis IKKE virker:**
| Del | Hvorfor | Status |
|---|---|---|
| Fjernstyringen af TDE via `WM_COMMAND` 10576/10569/57601/10602 og aflæsning af Output-panelet | Numrene er læst fra `TSResourceDllEng.dll` [Projekt: `VIDENSLOG.md`, 2026-09-24; `Program/tde/verify-one.ps1:54-61`]. MultiCharts' editor (PowerLanguage Editor) er et andet program med andre menunumre og andre vinduer. | **Sikkert:** skal bygges forfra. Det svarer til hele `tde/`-mappen. |
| Vinduesfinding (`Get-Process TSDev`) | Andet procesnavn [Projekt: `Program/tde_styring.py:28`] | Skal bygges forfra |
| Resultattekst "0 error(s)" | MultiCharts' compiler skriver sin egen tekst. | **UKENDT**. Mønstret i `verify-one.ps1:277` skal skrives om. |
| `Print(File("..."))`, `FileDelete`, `FileAppend` | Findes sandsynligvis i PowerLanguage [Antagelse: del af klassisk EL]. Men filadgang, låsning og tidspunkt for lukning kan være anderledes. | **UKENDT**. Test: en fil med 625 kombinationer skal give samme linjeantal og samme kontrolsum. |
| `RaiseRunTimeError`, `FormatDate`, `FormatTime`, `ELDateToDateTime`, `LastBarOnChart`, `Once`, `BarType` | Nyere EL-ord, som ikke alle nødvendigvis findes i PowerLanguage | **UKENDT**. Opdages gratis ved at kompilere alle 380 filer. |
| `of data(DataFilter_A)` med variabelt datanummer | Kompilerer i TS | **UKENDT** i MC |
| Løkke + series function | MultiCharts kan håndtere series functions i løkker anderledes end TS | **UKENDT, og det er den vigtigste test.** En fil kan være rigtig i den ene platform og forkert i den anden. |
| Max Bars Back "Auto Detect" | MultiCharts genstarter beregningen, når MBB ændres [Net, ikke bekræftet: MultiCharts wiki om backtest-motoren]. En genstart kører `Once` og `FileDelete` igen. | Sandsynligvis ufarligt, men det dobbelte tidsforbrug skal måles. Brug fast MBB ligesom i TS. |
| Sessioner og data | MC henter sessioner og data fra sin egen QuoteManager, ikke fra TS | Data skal importeres fra **samme** kilde, ellers måles dataforskelle i stedet for platformforskelle |

**Sådan beviser vi, at de giver samme tal:**
1. **Samme data:** Én eksporteret barfil importeres i begge platforme, med samme sessionsskabelon og tidszone.
2. **Gyldent sæt:** Ca. 20 filtre, der dækker alle funktionstyper fra K0, mindst ét fra hver gruppe A–E, plus decimalfilter, to-datastrøms-filter og filter med OpenD.
3. **Tre niveauer:** (a) CSV-kontrolsum identisk; (b) hvis ikke: Starttid/AntalBars pr. signal; (c) hvis stadig ikke: indikatorværdi bar for bar (kræver en midlertidig testudgave, der skriver værdien).
4. **Dommer:** Python-genberegningen (K4) afgør, hvem der har ret, hvis platformene er uenige.
5. **Løkketest T1 gentages i MC** for hver funktionstype. Resultatet fra TS må ikke overføres.
6. Pas-mærket "TS+MC-verificeret" sættes først, når 1–5 er bestået.

**Hvis mønster 5 (Python som regnemaskine) vælges,** skrumper porteringen: MultiCharts skal kun kunne lave facit-kørslerne og ikke hele produktionen. Det er et argument for K3's forslag. **Hvad man ellers kan gøre allerede nu for at gøre porteringen billigere:** Brug mønster 3 (egen hukommelse i arrays) i stedet for platformens indbyggede series functions. Så afhænger tallene af **vores** kode og ikke af to leverandørers forskellige indre regler. Det er det stærkeste argument for mønster 3 [Antagelse].

**Mulighed at undersøge (ikke anbefalet endnu):** MultiCharts findes også i en .NET-udgave (C#), hvor hver beregning kan have sin egen tilstand på en helt almindelig måde [Antagelse: fra min viden, ikke bekræftet her]. Det kunne fjerne løkkeproblemet helt. Men det er en ny kodebase og altså ikke en portering.

---

## 7. Angreb på mit eget første udkast

| Første udkast sagde | Hvad var galt |
|---|---|
| MACD-fejlen er, at hukommelsen "blandes" ved skiftende længder | **Passer ikke med målingen.** 625 *ens* rækker peger på "regnes én gang pr. bar" (2.2). Det har betydning for, hvordan man tester og retter. |
| "TradeStation regner series functions på hver bar, også i if" – med en forumkilde | Kilden var et søgeuddrag, ikke åbnet. Påstanden var også irrelevant: problemet er løkker, ikke if-sætninger. |
| Liste over "sandsynligt ramte" funktioner, herunder Average og ATR | **Forkert for Average og ATR.** Begge er målt uden de ens rækker [Projekt: NOTAT]. Den vigtige skelnen er tilbagekobling mod glidende vindue, og serie-indgang afhængig af N (2.3). |
| Max Bars Back for lille er hovedrisikoen for de 36 filtre | Et for lille MBB giver oftest en synlig fejl. Den tavse risiko er **opvarmning** (1.4), som MBB ikke løser. |
| Forskydningstest for look-ahead | Irrelevant for RawSignal, der ikke handler. Den reelle look-ahead-risiko er, **hvordan Starttid læses** (1.6). |
| IOG skal slås fra | Allerede tilfældet. Irrelevant før EdgeCruncher. |
| "Kodescanning" som nyt Lag 1 | Generatoren scanner allerede (`formel.py`). Det nye er, **at listen er ufuldstændig** og at TDE-advarslerne ignoreres (1.3, 1.9). |
| RawSignal Creature eksporterer signalerne | Nej. Det er EdgeFinder, der kører backtesten [Projekt: Task-filen]. |
| Kontrolplan uden tal | Nu med rækkefølge, bestået-kriterier og tidsskøn (afsnit 4). |
| Generelle fejl (continuous contracts, afrunding til tick) | Ikke forkerte, men ikke forankret i projektets kode. Taget ud. Data-delen hører til K3. |

---

## 8. Nye åbne punkter til Thomas

1. **Advarsler ved Verify:** Skal en fil med "N warning(s)" > 0 markeres som mistænkt i stedet for "Pass"? (1.9)
2. **Må den lokale session lave K0-listen?** Det er typen (series/simple) for hver funktion, der bruges i de 380 formler, aflæst i TDE. Kun læsning.
3. **Skal K0–K2 køres før den fulde kørsel?** De koster minutter og fortæller, hvor mange filtre der er i fare.
4. **Test T1 på 069 med Fra = Til:** Giver en løkke med ét sæt samme tal som en fil uden løkke? Svaret afgør, om forklaringen i 2.2 holder.
5. **Hvilken vej for gruppe A/C/D:** mønster 1, 2 eller 3 (2.4)? Og skal commit `12120a8` (den håndregnede MACD) genoplives som skabelon?
6. **Opvarmningsvindue:** Skal generatoren udregne og skrive et opvarmningsvindue i hver fil, og skal signaler i vinduet kasseres? Grænsen fastsætter K1.
7. **Oprindelse i CSV'en:** Må strategien skrive symbol/interval/session i filens overskrift? (1.7)
8. **Tjek af Data1:** Skal `Once`-tjekket udvides til symbol og session? (1.5)
9. **Starttid:** Skal det skrives ind i EdgeFinder-metoden, at tiden er bar-slut, og at handel tidligst sker ved næste bars åbning? (1.6)
10. **Hvad er EdgeCruncher tænkt som:** "edge → strategi med udgange", "kombination af filtre" eller begge dele? (5)
11. **Officielle kilder:** Hvem læser TradeStations og MultiCharts' officielle hjælp om series functions og løkker? De er blokeret i skyen.
12. **Decimaltrin:** Skal generatoren afvise trin, som computeren ikke kan gemme præcist (fx 0,1)? (1.8)

---

**Hvad der mangler i denne del:**
- Ingen officielle kilder er læst, fordi de er blokeret.
- Tiden pr. backtest er ikke målt, så alle tidsskøn er antagelser.
- Commit `12120a8` er ikke åbnet.
- Min forklaring på MACD-fejlen (2.2) er den bedste, der passer med målingerne. Den er ikke bevist, før test T1 er kørt.


# Del 3 – Data, dvale-lager og automatisering (Konsulent 3, dybde-runden)

*Rettet efter kritikrunden: 4 workspaces fra NOTER.md er med i datamængden; journalen gemmer antal fejl og advarsler hver for sig plus hele panelteksten; filter-versionen har K2's funktionsgruppe A–E; opvarmningsvindue pr. filter × datasæt; forsøg tælles i et forsøgsregnskab med N_rå (talt af databasen) og N_eff (målt); placebo-signaler har eget nummerområde; signal-tabellen har plads til bar-nummer.*

*Denne del erstatter min første del 3 helt. Alt her er råd. Alle SQL-stykker er FORSLAG. Intet er kørt, og intet må køres, før Thomas har set og godkendt den præcise kommando [Projekt: VIDENSLOG.md, post 2026-09-24 "Vis ændringer i databasen …"].*

**Mærker:**
- [Projekt: fil:linje] = står i projektets filer. Jeg har selv læst dem.
- [Net: titel, URL] = en kilde, jeg selv har åbnet og læst.
- [Net, ikke bekræftet] = kun set i en søgeoversigt. Siden kunne ikke åbnes, fordi netværket her blokerer den.
- [Antagelse: hvorfor] = min egen vurdering.
- Vigtige påstande er også mærket **BEVIST**, **SANDSYNLIGT** eller **UKENDT**.

**Fagord, der bruges meget:**
- **Tabel:** et regneark inde i databasen.
- **Schema:** en mappe med tabeller i databasen.
- **Indeks:** en sorteret "telefonbog" over en tabel, så databasen finder rækker hurtigt.
- **Partition:** en tabel, der er delt i skuffer, som hver kan tømmes eller smides ud for sig.
- **Transaktion:** en pakke af ændringer, der enten gemmes helt eller slet ikke.
- **Superbruger:** en databasebruger, der må alt, også slette alt.

---

## 0. Kort sammenfatning (de 5 vigtigste nye fund)

1. **Kun ét marked kan gemmes pr. filter i dag. BEVIST i koden.**
   - Signaldata ligger i én tabel pr. filter, `rawsignal.rawsignal<nr>`.
   - Ved hver indlæsning slettes alt, der lå der før [Projekt: RawSignal_Creature/Program/indlaes_csv.py:72].
   - Tabellen har ingen kolonne for marked, tidsramme, dataperiode eller kørsel [Projekt: indlaes_csv.py:67-70].
   - CSV-filen (en tekstfil med kommaer mellem værdierne) har samme faste navn, uanset hvilket marked der er kørt [Projekt: generer.py:62].
   - Kører man filter 1 på to markeder, overskriver det andet marked det første uden at melde fejl. Man kan heller ikke se bagefter, hvilket marked tallene kom fra.
   - Fabrikken skal teste mange markeder. Derfor er dette det vigtigste at rette før den fulde kørsel.
2. **Selve backtesten er slet ikke automatiseret. BEVIST.**
   - Programmet laver og verificerer filerne (Verify = TradeStations kontrol af, at koden kan oversættes uden fejl). Det kører ikke backtesten.
   - Et menneske skal lægge strategien på et chart, køre den og vente, før `indlaes_csv.py` må startes [Projekt: indlaes_csv.py:14-15; README.md "Sådan bruges det"].
   - Med 380 filtre og flere markeder bliver det titusindvis af manuelle trin (se afsnit 2). Det er den reelle flaskehals, ikke databasen.
3. **Alle programmer kører som databasens superbruger `postgres`. BEVIST.**
   - Se [Projekt: faelles.py:38; Automation/run-batch.ps1 (psql -U postgres)].
   - En fejl i koden kan derfor slette hvad som helst.
   - Min egen første regel om "pengeskabet åbnes kun én gang" (REVOKE-kommandoer) ville ikke have virket, fordi en superbruger ikke kan begrænses på den måde.
4. **Afviste filer bliver ikke skrevet ned i databasen. BEVIST.**
   - `rawsignal`/`rawsignal_kontrol` får kun en række, når begge filer er godkendt [Projekt: rawsignal_creature.py:97-107; database.py:39-53].
   - Kolonnen `verification` kan derfor i praksis kun indeholde "Pass". Fejl står kun i en tekst-log på én maskine [Projekt: faelles.py:27-33].
   - Det strider mod Thomas' egen proces: "notere fejlen … vi samler alle fejl op senere" [Projekt: Task_RawSignal_Creature_EdgeFinder_opgave.md:4-5].
5. **Datamængden er stor, men kan styres. Regnet.**
   - Pr. marked og tidsramme bliver det 6–39 GB i PostgreSQL med dagens tabelform. Det svarer til 58–360 mio. signal-rækker.
   - Med fx 30 marked/tidsramme-kombinationer bliver det 0,2–1,2 TB.
   - 380 tabeller pr. marked holder ikke. Én tabel delt i skuffer pr. kørsel gør. Den skal have faste filter-ID'er, og der skal være visninger pr. filter, så Thomas beholder sit overblik.

---

## 1. Kritik ud fra den rigtige kode og de rigtige tabeller

### 1.1 Sådan ser databasen faktisk ud (læst ud af koden)

| Tabel | Hvad | Kilde |
|---|---|---|
| `filter_case` | Filtrene. Kolonner, der bruges: `filter_case_id, filtere, filter1_n1_start/_end/_step, filter1_n2_start/_end/_step, rawsignal_faerdig` | [Projekt: database.py:9-25] |
| `filter_case_backup_20260924` | Kopi fra før omnummereringen, i samme database | [Projekt: BESLUTNINGSLOG_2026-09-24.md:31] |
| `rawsignal` (i standard-schemaet) | Én række pr. godkendt strategi: `dev_date, rawsignal_kontrol_name, rawsignal_kontrol_path, verification, rawsignal_name, rawsignal_path, note`. Primærnøgle: strateginavn | [Projekt: BESLUTNINGSLOG_2026-09-24.md:30; database.py:43-49] |
| `rawsignal_kontrol` | Samme 7 kolonner. Primærnøgle: ShowMe-navn | samme |
| `rawsignal.rawsignal001` … `rawsignal380` | Én tabel pr. filter: `runid text, n1 numeric, n2 numeric, starttid timestamp, antalbars int, afsluttet smallint` + indeks (n1, n2, starttid) | [Projekt: indlaes_csv.py:67-71] |

Databasen er formentlig PostgreSQL 18. Det gamle script peger på `C:\Program Files\PostgreSQL\18\bin\psql.exe` [Projekt: Automation/run-batch.ps1:22]. **SANDSYNLIGT.**

### 1.2 Svage punkter (med fil og linje)

**A. Navnet på en ting er dens plads i en liste.**
- Strateginavn, CSV-navn, tabelnavn og RunID bygges alle af `filter_case_id` [Projekt: faelles.py:22-24].
- Da filter 1 blev slettet, skiftede alle andre navn [Projekt: BESLUTNINGSLOG_2026-09-24.md:31-37].
- Programmet springer et filter over, hvis navnet "findes allerede" [Projekt: rawsignal_creature.py:79-81; database.py:29-36]. Efter en ny omnummerering kan et nyt filter derfor blive sprunget over, fordi et andet, gammelt filter havde samme nummer. **BEVIST som mulighed** (logikken sammenligner kun navne).
- Dokumenterne er allerede ude af trit:
  - `generer.py` siger, at gamle 069 (nu 68) gav "de samme 4.918 signaler" i alle 625 kombinationer [Projekt: generer.py:26].
  - Byggevejledningen siger "480 signaler" [Projekt: BYGGEVEJLEDNING_RawSignal.md:318-324].
  - Mindst ét af tallene er forældet. **BEVIST uenighed.**

**B. Et filters formel har ingen version.**
- Ændrer man formlen eller Fra/Til/Step i `filter_case`, hedder filteret det samme, og de gamle signaler ligger stadig i `rawsignal.rawsignal<nr>`.
- Intet i tabellen viser, hvilken formel der gav dem [Projekt: indlaes_csv.py:67-70].
- **Her tager jeg K1's side i den gamle uenighed U5.** Et fast ID alene er ikke nok. Der skal også være en filter-version.

**C. Én tabel pr. filter uden marked og kørsel.** Se fund 1 ovenfor.
- Thomas valgte én tabel pr. filter "for overskuelighedens skyld" [Projekt: BESLUTNINGSLOG_2026-09-24.md:33]. Det er hans beslutning, og den respekteres i forslaget i afsnit 3: overblikket pr. filter beholdes som *visninger*.
- Men i dag giver valget:
  - 380 tabeller pr. marked, hvis man kopierer ideen videre.
  - Tabeller, som programmet opretter under kørslen (`create table if not exists`) [Projekt: indlaes_csv.py:67]. Det er databaseændringer, som ingen har set på forhånd, ét filter ad gangen.
  - En `delete from` på hele tabellen [Projekt: indlaes_csv.py:72]. Den er sikker i én transaktion, men sletter også data fra et andet marked.

**D. Samme navn til to forskellige ting.**
- `rawsignal` er både en tabel (journalen) og et schema (signaldata).
- `rawsignal.rawsignal001` og `rawsignal` betyder noget forskelligt. Det er let at skrive forkert i en SQL, der skal godkendes. **BEVIST** [Projekt: database.py:43 og indlaes_csv.py:23].

**E. Journalen er dobbelt og mangler det vigtige.**
- `gem_resultat` skriver præcis de samme 7 værdier i begge tabeller [Projekt: database.py:43-49]. Det er samme oplysning to steder.
- Til gengæld mangler:
  - kodeversion (git-commit)
  - TradeStation-version
  - formel-version
  - Max Bars Back-status
  - hvem/hvilken maskine
  - tid brugt
  - fejlede forsøg
- Filernes hoved beskriver Max Bars Back og hukommelsesproblemet [Projekt: README.md "Regler"], men det står kun i filen, ikke i en kolonne, man kan søge på.

**F. Superbruger overalt.** Se fund 3. Forbindelsen er fast kodet til `127.0.0.1` [Projekt: faelles.py:38]. Programmet kan altså kun køre på selve databaseserveren. En maskine nr. 2 kan ikke bruge det uden ændringer.

**G. Faste stier og én maskine.**
- `C:\TradingDB_Folder\FilterFolder` [Projekt: faelles.py:13].
- `C:\Program Files (x86)\TradeStation 10.0\…\TSDev.exe` [Projekt: tde_styring.py:14].
- `find()` tager "den første" TSDev-proces [Projekt: tde_styring.py:29]. Med to TDE'er på samme maskine vælger programmet tilfældigt. **BEVIST.**

**H. CSV-stien er skrevet ordret ind i EasyLanguage-koden fire steder** [Projekt: generer.py:11-13, 62, 170]. Det skyldes, at `Print(File(...))` kræver et fast navn [Projekt: VIDENSLOG.md, post 2026-09-18]. Konsekvenser:
- To kørsler af samme filter må aldrig ske samtidig på samme maskine.
- Test- og produktionskørsel skriver til samme fil, medmindre koden bygges med en anden sti.

**I. Ingen kontrol af, at backtesten er færdig.** `indlaes_csv.py` stoler på, at et menneske først starter den, når TradeStation er færdig [Projekt: indlaes_csv.py:14-15].
- En halvt skrevet fil bliver afvist, hvis RunID er forkert, eller hvis `copy` fejler.
- Men en fil, der blot er *kortere* end den skulle være, bliver indlæst uden fejl. **SANDSYNLIGT**: der er ingen tjek af antal kombinationer eller slutdato.

**J. Tidszone og datakilde er ikke gemt.** `starttid` er `timestamp` uden tidszone [Projekt: indlaes_csv.py:69]. Om TradeStation skriver børsens tid eller Windows' lokale tid, og hvilket symbol og hvilken tidsramme Data1/Data2/Data3 havde, står ingen steder. Data1's tidsramme kan kun sættes i chartet [Projekt: BESLUTNINGSLOG_2026-09-24.md:52-53]. **UKENDT, men en klar risiko for, at resultater ikke kan genskabes.**

**K. Backup er en kopi i samme database.** `filter_case_backup_20260924` ligger på samme disk og i samme database som originalen. Den beskytter mod en forkert SQL, men ikke mod en død disk, en fejl i databasen eller ransomware (et program, der låser filerne og kræver penge). **BEVIST** (placering), **UKENDT** om der findes anden backup.

**L. Det, der er godt, og som skal bevares.**
- Én transaktion for "begge filer godkendt + markér færdig" [Projekt: database.py:39-53].
- Indlæsning via en midlertidig tabel med RunID-tjek [Projekt: indlaes_csv.py:55-65].
- "Stop hellere end gæt" [Projekt: README.md].
- Højst én genstart af TDE [Projekt: rawsignal_creature.py:36-61].

Det er det rigtige fundament. Alt nedenfor bygger videre på det. Intet af det skal smides ud.

---

## 2. Datamængder – regnet trin for trin

### 2.1 Det eneste målte tal
- Filter 1 (AvgTrueRange, N1+N2) gav **939.816 signaler på 620 kombinationer** [Projekt: BESLUTNINGSLOG_2026-09-24.md:88-91].
- Det er 939.816 / 620 = **ca. 1.516 signaler pr. kombination**.
- Det gælder ét marked og én tidsramme, som ikke er oplyst.
- Største antal kombinationer pr. filter er 25 × 25 = **625** (arrays er altid 25) [Projekt: BYGGEVEJLEDNING_RawSignal.md:166-175].
- Hvor mange kombinationer de øvrige 379 filtre har, står i `filter_case`, som jeg ikke har adgang til. **UKENDT.** Jeg regner derfor med tre scenarier. Et filter uden parametre har 1 kombination, og et med kun N1 har højst 25. Derfor er gennemsnittet sikkert under 625.

### 2.2 Rækker pr. marked og tidsramme (ét "datasæt")

Rækker = 380 filtre × kombinationer pr. filter × 1.516 signaler pr. kombination

| Scenarie | Gns. kombinationer | Rækker |
|---|---|---|
| Lav | 100 | 380 × 100 × 1.516 = **57,6 mio.** |
| Mellem | 300 | 380 × 300 × 1.516 = **172,8 mio.** |
| Høj (loft) | 625 | 380 × 625 × 1.516 = **360,1 mio.** |

Forbehold: 1.516 signaler pr. kombination er målt på ét filter. Et filter, der tænder sjældent, giver langt færre. **Tallene er et loft-skøn, ikke en prognose.**

### 2.3 Bytes pr. række i PostgreSQL (dagens tabelform)

Fra PostgreSQL's egen dokumentation [Net: "Database Page Layout", PostgreSQL-dokumentationens kilde storage.sgml, https://raw.githubusercontent.com/postgres/postgres/master/doc/src/sgml/storage.sgml – åbnet og læst]:
- Hver række har et hoved på 23 bytes, som afrundes til 24.
- Plus en 4-byte "pegepind" på siden.
- En side er 8 KB.

Et `numeric`-tal fylder "to bytes for hver gruppe af fire cifre plus tre til otte bytes" [Net: datatype.sgml, samme kilde, https://raw.githubusercontent.com/postgres/postgres/master/doc/src/sgml/datatype.sgml – åbnet].

| Del | Bytes |
|---|---|
| Rækkehoved | 24 |
| `runid` ("rawsignal001", 12 tegn + 1) | 13 |
| `n1`, `n2` (små numeric, ca. 5 hver) | 10 |
| Udfyldning, så `timestamp` starter på et 8-tal | 1 |
| `starttid` | 8 |
| `antalbars` + `afsluttet` | 6 |
| Afrunding af rækken til 8 | 2 |
| Pegepind | 4 |
| **Tabel i alt** | **ca. 68** |
| Indeks (n1, n2, starttid): hoved 8 + data ca. 24 + pegepind 4, delt med 0,9 fyldningsgrad | **ca. 40** |
| **I alt pr. række** | **ca. 108** |

[Antagelse: typiske størrelser for små heltal i numeric. Den præcise størrelse kan måles på Thomas' server med `pg_total_relation_size` på filter 1's tabel. Det er en læsning, ikke en ændring.]

### 2.4 Plads pr. datasæt og i alt

| Scenarie | Pr. datasæt (108 B/række) | 10 datasæt | 30 datasæt |
|---|---|---|---|
| Lav | 6,2 GB | 62 GB | 187 GB |
| Mellem | 18,7 GB | 187 GB | 560 GB |
| Høj | 38,9 GB | 389 GB | 1,17 TB |

"Datasæt" betyder marked × workspace × dataperiode. **Rettet efter K1:** projektet har allerede **4 workspaces** (tidsrammer 5,10,60 / 10,20,60 / 5,30,120 / 5,10,120) [Projekt: RawSignal_Creature/NOTER.md:150-151]. Ét marked giver altså mindst 4 datasæt: lav 25 GB, mellem 75 GB, høj 156 GB. Hvor mange markeder Thomas vil have, er **UKENDT**. 10 og 30 datasæt i tabellen svarer til ca. 2,5 og 7,5 markeder.

**Hvad betyder det?**
- **Pladsen er ikke problemet.** En 2–4 TB SSD-disk er billig i forhold til projektet. [Antagelse: almindelige priser.]
- **Hastigheden og oprydningen er problemet.** At slette 360 mio. rækker med `DELETE` og derefter rydde op (VACUUM) tager lang tid og efterlader huller. Det passer dårligt med "ryd op og start forfra".
- **En slimmere række giver kun ca. 25 %.** Man kan fjerne `runid` (den er ens i hele tabellen), gemme n1/n2 som små heltal (`smallint`, med et indeks for de 8 decimal-filtre) og bruge `boolean` til `afsluttet`. Så bliver det ca. 48 + 4 bytes i tabellen og ca. 31 i indekset, altså ca. **83 B/række**. Høj-scenariet bliver 29,9 GB pr. datasæt. En forbedring, men ikke afgørende.
- **Den store gevinst er skuffer (partitioner).** PostgreSQL's dokumentation siger: *"An entire partition can be detached fairly quickly, so it may be beneficial to design the partition strategy in such a way that all data to be removed at once is located in a single partition."* Den advarer også om, at *"too many partitions can mean longer query planning times and higher memory consumption"*. Den gamle arvebaserede metode fungerer "med op til måske hundrede" dele, "ikke mange tusinde" [Net: "Table Partitioning – Best Practices", ddl.sgml, https://raw.githubusercontent.com/postgres/postgres/master/doc/src/sgml/ddl.sgml – åbnet og læst].
  - 380 filtre × 30 datasæt = 11.400 skuffer er for mange.
  - **Én skuffe pr. kørsel** (= ét datasæt) giver få skuffer. Det svarer præcis til "ryd op og start forfra": en fejlet kørsel smides ud som én skuffe.

### 2.5 Næste led fylder mere, hvis man ikke passer på
- EdgeFinder er et event-studie: for hvert signal måles prisudviklingen fx 1, 2, 5, 10 … bars frem.
- Gemmer man det pr. signal og pr. horisont med 10 horisonter, bliver 360 mio. rækker til 3,6 mia.
- **Råd: gem kun råsignalerne én gang. Gem EdgeFinder-resultater som tal pr. kombination** (gennemsnit, spredning, antal). Høj-scenariet giver 380 × 625 = 237.500 rækker pr. datasæt, altså ingenting. Detaljer pr. signal kan altid regnes igen fra råsignaler + prisdata. [Antagelse: reproducerbarhed gør genberegning billigere end lagring.]

### 2.6 Tid – den egentlige flaskehals
- Én backtest kører alle kombinationer af ét filter på ét datasæt, fordi løkken ligger i koden [Projekt: BYGGEVEJLEDNING_RawSignal.md:312].
- Antal backtests = 380 × antal datasæt. Hvor længe én tager, er **UKENDT**. Det er ikke målt i projektets filer.

| Minutter pr. backtest | 1 datasæt | 10 datasæt | 30 datasæt |
|---|---|---|---|
| 2 | 13 t | 5,3 døgn | 16 døgn |
| 5 | 32 t | 13 døgn | 40 døgn |
| 15 | 4 døgn | 40 døgn | 119 døgn |

Regnestykke, eksempel: 380 × 30 × 5 min = 57.000 min = 950 timer = 40 døgn med én maskine i døgndrift.

- **Og det er før walk-forward.** Walk-forward (at teste i flere tidsvinduer efter hinanden) ganger antallet op igen.
- **MACD-løsning "B" i byggevejledningen, én fast parameter pr. backtest** [Projekt: BYGGEVEJLEDNING_RawSignal.md:360-362], ganger backtests med op til 625: 380 × 625 = 237.500 backtests pr. datasæt. **Umuligt med én TradeStation.** Det afgør ikke Thomas' MACD-valg, men det skal med i valget.

---

## 3. Datamodellen for led 1–5 og vejen dertil

### 3.1 Principper
1. **Et fast ID + en version.** `filter_uid` ændres aldrig. `filter_version` stiger, når formel eller Fra/Til/Step ændres. En fingeraftryk-kolonne (`formel_sha256`, SHA-256 = en kode, der ændrer sig, hvis ét tegn ændrer sig) opdager ændringer, som ingen har meldt.
2. **Alt hører til en kørsel.** En kørsel = én kodeversion + ét datasæt + én opsætning. Går noget galt, kasseres kørslen og startes forfra.
3. **Kun tilføje.** Resultater rettes aldrig. Ny test = ny række.
4. **Databasen håndhæver reglerne, ikke dokumentationen.** Det kræver, at programmerne *ikke* kører som superbruger.
5. **Thomas' åbne punkter bliver data, ikke låse.** Det, han ikke har afgjort (plateau-trappen, dvale-grænsen, datadelingen), gemmes som en indstilling, han selv udfylder. Databasen må ikke gætte for ham.

### 3.2 Oversigt

```
                       ┌──────────────── TradingDB (produktion) ────────────────┐
 fabrik.filter ────────┤  filter (fast uid) ─< filter_version (formel, fingeraftryk)│
                       │  datasaet (marked, tidsramme, periode, data-fingeraftryk)│
                       │  koersel (kodeversion, TS-version, datasæt, status)     │
 Led 1 Creature ──────▶│  tde_verify   (én række pr. forsøg, også Fail)           │
 Led 1b Backtest ─────▶│  signal       (delt i skuffer pr. kørsel)               │
 Led 2 Analyse ───────▶│  analyse_kombination (tal + plateau-farve pr. komb.)    │
 Led 3 EdgeFinder ────▶│  edge_kombination    (event-tal pr. kombination)        │
 Led 4 EdgeCruncher ──▶│  kandidat + forsoeg (ALLE varianter, også dumpede)       │
 K1 slutkontrol ──────▶│  pengeskab_aabning (én gang pr. strategi)               │
 Led 5 Dvale ─────────▶│  dvale_strategi + dvale_pas                              │
                       │  regelsaet (Thomas' valg: plateau-skala, dvale-grænse …) │
                       │  job + haendelse (kø og samlet log for alle maskiner)   │
                       └──────────────────────────────────────────────────────────┘
   TradingDB_test: præcis samme tabeller, andet navn, andre filmapper, andre TS-navne
```

### 3.3 SQL-forslag (kun forslag, ikke kørt)

Skemaet hedder `fabrik`, så det ikke blandes med de eksisterende tabeller eller med schemaet `rawsignal` (jf. 1.2 D).

```sql
-- FORSLAG A: filtre med fast ID og version
CREATE SCHEMA fabrik;

CREATE TABLE fabrik.filter (
    filter_uid     uuid PRIMARY KEY DEFAULT gen_random_uuid(),  -- aldrig ændret
    kort_navn      text UNIQUE NOT NULL,     -- fx 'F0001', menneskevenligt, aldrig genbrugt
    gammelt_nr     int,                      -- filter_case_id på flyttedagen (kun til sporing)
    status         text NOT NULL DEFAULT 'aktiv' CHECK (status IN ('aktiv','udgaaet'))
);

CREATE TABLE fabrik.filter_version (
    filter_uid     uuid NOT NULL REFERENCES fabrik.filter,
    version        int  NOT NULL,
    formel         text NOT NULL,            -- ordret fra filter_case.filtere
    n1_start numeric, n1_end numeric, n1_step numeric,
    n2_start numeric, n2_end numeric, n2_step numeric,
    formel_sha256  text NOT NULL,            -- fingeraftryk af formel + intervaller
    mbb_behov      int,                      -- udregnet Max Bars Back, NULL = ukendt (de 36)
    hukommelse     text NOT NULL,            -- 'ikke_seriefunktion','maalt_ok','maalt_ramt','ikke_maalt'
    funktionsgruppe char(1) CHECK (funktionsgruppe IN ('A','B','C','D','E')),  -- K2 afsnit 2.3, sat af maskine
    klassifikation_version text,             -- hvilken version af K2's klassifikationsregel
    opvarmning_laengde int,                  -- K2 1.4: største tilbagekoblede længde (bars i DEN datastrøm)
    oprettet       timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (filter_uid, version),
    UNIQUE (filter_uid, formel_sha256)
);
```

```sql
-- FORSLAG B: datasæt og kørsel
CREATE TABLE fabrik.datasaet (
    datasaet_id    serial PRIMARY KEY,
    data1 text NOT NULL, data2 text, data3 text,   -- symbol + tidsramme pr. datastrøm, fx '@ES 5 min'
    session        text NOT NULL,                  -- sessionsskabelon
    tidszone       text NOT NULL,                  -- 'Exchange' eller 'Local' (jf. 1.2 J)
    periode_fra    date NOT NULL, periode_til date NOT NULL,
    prisdata_sha256 text                           -- fingeraftryk af eksporterede bars (afsnit 5.3)
);

CREATE TABLE fabrik.koersel (
    koersel_id     bigserial PRIMARY KEY,
    led            text NOT NULL,           -- 'creature','backtest','analyse','edgefinder','cruncher'
    datasaet_id    int REFERENCES fabrik.datasaet,
    git_commit     text NOT NULL,           -- programmets version
    ts_version     text,                    -- TradeStation-build
    regelsaet_id   int,                     -- hvilke af Thomas' regler der gjaldt
    status         text NOT NULL DEFAULT 'igang'
                   CHECK (status IN ('igang','faerdig','kasseret')),
    startet        timestamptz NOT NULL DEFAULT now(),
    afsluttet      timestamptz,
    kasseret_fordi text
);
```

```sql
-- FORSLAG C: journal for led 1 – ÉN række pr. forsøg, også de fejlede
CREATE TABLE fabrik.tde_verify (
    koersel_id     bigint NOT NULL REFERENCES fabrik.koersel,
    filter_uid     uuid NOT NULL, filter_version int NOT NULL,
    filtype        text NOT NULL CHECK (filtype IN ('Strategy','ShowMe')),
    ts_navn        text NOT NULL,           -- navnet i TradeStation (se afsnit 5.4 om test-præfiks)
    fil_sha256     text NOT NULL,
    resultat       text NOT NULL CHECK (resultat IN ('Pass','Fail','Afbrudt')),
    antal_fejl     int  NOT NULL,           -- tolket fra Output-panelet
    antal_advarsler int NOT NULL,           -- K2 1.9: i dag ignoreret af verify-one.ps1:276-277
    advarsler      text[],                  -- hver advarselslinje for sig (søgbar)
    raa_output     text NOT NULL,           -- hele panelteksten, uændret
    note           text,                    -- TDE's fejltekst
    maskine        text NOT NULL,
    tidspunkt      timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (filter_uid, filter_version) REFERENCES fabrik.filter_version
);
```

```sql
-- FORSLAG D: råsignaler, delt i skuffer pr. kørsel
CREATE TABLE fabrik.signal (
    koersel_id     bigint   NOT NULL,
    filter_nr      smallint NOT NULL,       -- lille internt nummer, slås op i fabrik.filter_nr_map
    n1_idx         smallint NOT NULL,       -- 1..25 (indeks, også for decimal-filtre)
    n2_idx         smallint NOT NULL,       -- 0 hvis ingen N2
    starttid       timestamp NOT NULL,
    antalbars      int NOT NULL,
    afsluttet      boolean NOT NULL,
    bar_nr         int                      -- CurrentBar ved start; kræver ændring af generatoren (Thomas/K2)
) PARTITION BY LIST (koersel_id);
-- Indekset skabes på hver skuffe: (filter_nr, n1_idx, n2_idx, starttid)
-- Hver kørsel får sin egen skuffe:
--   CREATE TABLE fabrik.signal_k17 PARTITION OF fabrik.signal FOR VALUES IN (17);
-- Kasseres kørsel 17:  ALTER TABLE fabrik.signal DETACH PARTITION fabrik.signal_k17;
--                      DROP TABLE fabrik.signal_k17;   (ét hurtigt, rent snit)
```

**Opvarmning (K2 afsnit 1.4) hører til filter × datasæt, ikke til filteret alene.** Vinduet måles i bars *i den datastrøm, funktionen regner på*. 1.382 bars er ca. 5 handelsdage på 5-min-data, men på 120-min-data (Data3 i to workspaces) er det flere måneder [Antagelse: ca. 11–12 bars à 120 min pr. døgn for et næsten døgnåbent futures-marked]. Derfor:

```sql
-- FORSLAG D2: opvarmningsvindue pr. filter-version og datasæt (udregnet af generatoren)
CREATE TABLE fabrik.opvarmning (
    filter_uid uuid NOT NULL, filter_version int NOT NULL,
    datasaet_id int NOT NULL REFERENCES fabrik.datasaet,
    grænse_rest numeric NOT NULL,        -- K1's grænse, fx 0,01 = 1 % startfejl tilbage
    bars       int NOT NULL,             -- udregnet efter K2's formel
    gyldig_fra timestamp NOT NULL,       -- første tidspunkt, hvor signaler må bruges
    PRIMARY KEY (filter_uid, filter_version, datasaet_id, grænse_rest)
);
```

Signaler i vinduet **slettes ikke** (kun tilføje). De sorteres fra i visningerne (`starttid >= gyldig_fra`), så en anden grænse fra K1 kan prøves uden ny backtest. `bar_nr` i CSV'en gør omregningen fra bars til tid sikker. Uden den skal databasen kende hver bars tidspunkt pr. datastrøm.

**Placebo-signaler (K1 afsnit 5, punkt 6)** skal gennem præcis samme produktionslinje. De får deres eget `filter_nr`-område (fx 9000+) og status `placebo` i `fabrik.filter`. Alle produktionsvisninger udelukker dem. Om det er "testdata blandet med produktion", afgør Thomas (se uenigheder).

Hvorfor `filter_nr smallint` i stedet for uuid her? En uuid er 16 bytes. Med 360 mio. rækker pr. datasæt er det ca. 5 GB ekstra. `filter_nr_map` (filter_nr ↔ filter_uid + version) skrives én gang pr. kørsel og ændres aldrig. [Antagelse: afvejning mellem plads og enkelhed.]

**Thomas' overblik pr. filter bevares** som visninger (en visning = en gemt forespørgsel, der ligner en tabel):

```sql
-- FORSLAG E: samme overblik som i dag, én "tabel" pr. filter, men uden 380 rigtige tabeller
CREATE VIEW rawsignal_vis.f0001 AS
SELECT d.data1 AS marked, s.* FROM fabrik.signal s
JOIN fabrik.koersel k USING (koersel_id) JOIN fabrik.datasaet d USING (datasaet_id)
JOIN fabrik.filter_nr_map m ON m.koersel_id = s.koersel_id AND m.filter_nr = s.filter_nr
JOIN fabrik.filter f ON f.filter_uid = m.filter_uid
WHERE f.kort_navn = 'F0001' AND k.status = 'faerdig';
```

```sql
-- FORSLAG F: Thomas' regler som data (løser uenighed U4 om PL1–PL7-låsen)
CREATE TABLE fabrik.regelsaet (
    regelsaet_id    serial PRIMARY KEY,
    navn            text NOT NULL,          -- fx 'Plateau-trappe udkast 1'
    plateau_niveauer int,                   -- hvor mange niveauer trappen har. NULL = ikke afgjort
    plateau_regler  jsonb,                  -- farvedefinitioner pr. niveau, skrevet af Thomas/K1
    dvale_min_niveau int,                   -- NULL = Thomas har ikke valgt. Så kommer INTET i dvale
    datadeling_id   int,                    -- se FORSLAG G
    godkendt_af_thomas timestamptz,         -- NULL = kun udkast
    oprettet        timestamptz NOT NULL DEFAULT now()
);
```

- Min første version havde `CHECK (plateau_niveau ~ '^PL[1-7]$')`. Den låste trappen på 7 niveauer og afgjorde dermed i praksis et åbent punkt for Thomas. **K1 havde ret. Låsen er fjernet.**
- Nu gemmes plateau-niveauet som et tal. Antallet af niveauer, farvereglerne og dvale-grænsen er Thomas' egne felter.
- Er de tomme, er der bare ingen strategi, der opfylder kravet. Det er et sikkert standardvalg, ikke en afgørelse.

```sql
-- FORSLAG G: datadeling (K1's F2), pengeskab (F9) og alle forsøg (F3)
CREATE TABLE fabrik.datadeling (
    datadeling_id  serial PRIMARY KEY,
    udvikling_fra date NOT NULL, udvikling_til date NOT NULL,
    validering_fra date NOT NULL, validering_til date NOT NULL,
    pengeskab_fra date NOT NULL, pengeskab_til date NOT NULL,
    laast          timestamptz NOT NULL DEFAULT now(),
    CHECK (udvikling_til < validering_fra AND validering_til < pengeskab_fra)
);

-- Rettet efter K1 afsnit 3: forsøg tælles i millioner. De gemmes IKKE som én
-- jsonb-række hver. Hver række i edge_kombination (filter × komb. × workspace ×
-- retning × horisont) ER ét forsøg, også de dumpede. Denne tabel er regnskabet,
-- som en maskine udfylder pr. forskningsrunde:
CREATE TABLE fabrik.forsoegsregnskab (
    runde_id       serial PRIMARY KEY,
    beskrivelse    text NOT NULL,           -- fx 'Runde 1: 380 filtre, @ES, 4 workspaces'
    n_raa          bigint NOT NULL,         -- talt af databasen: count(*) over runden
    n_raa_regnet   bigint NOT NULL,         -- 380 × C × 4 × 2 × 5 ud fra opsætningen; skal = n_raa
    n_eff          numeric,                 -- MÅLT af K1's metode (eget job), NULL indtil målt
    n_eff_metode   text,                    -- fx 'egenværdi (Nyholt/Li-Ji)', 'klynger', 'placebo'
    n_eff_input_sha256 text,                -- fingeraftryk af de serier, der blev målt på
    tidligere_kig  text,                    -- K1: kig, der ikke kan tælles, skrives ned i ord
    laast          timestamptz              -- sat, når runden er slut; derefter kun læsning
);

CREATE TABLE fabrik.forsoeg (              -- kun EdgeCrunchers ekstra varianter (udgange, stop)
    forsoeg_id     bigserial PRIMARY KEY,
    koersel_id     bigint NOT NULL REFERENCES fabrik.koersel,
    filter_uid     uuid NOT NULL, filter_version int NOT NULL,
    variant        jsonb NOT NULL,          -- parametre, udgangsregel, stop, marked …
    led            text NOT NULL,
    bestaaet       boolean NOT NULL
);

CREATE TABLE fabrik.pengeskab_aabning (
    strategi_uid   uuid PRIMARY KEY,        -- én åbning pr. strategi, for altid
    version        int NOT NULL,
    datadeling_id  int NOT NULL REFERENCES fabrik.datadeling,
    antal_handler  int NOT NULL,
    resultat       jsonb NOT NULL,
    bestaaet       boolean NOT NULL,
    aabnet         timestamptz NOT NULL DEFAULT now()
);
```

```sql
-- FORSLAG H: dvale-lageret med de felter, K1 manglede
CREATE TABLE fabrik.dvale_strategi (
    strategi_uid   uuid NOT NULL, version int NOT NULL,
    kort_navn      text NOT NULL,           -- 'STR-000123'
    filter_uid     uuid NOT NULL, filter_version int NOT NULL,
    koersel_id     bigint NOT NULL REFERENCES fabrik.koersel,
    platform       text NOT NULL,           -- 'TradeStation' / 'MultiCharts'
    kode_sti       text NOT NULL, kode_sha256 text NOT NULL,
    status         text NOT NULL DEFAULT 'dvale' CHECK (status IN ('dvale','vakt','udgaaet')),
    oprettet       timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (strategi_uid, version)
);

CREATE TABLE fabrik.dvale_pas (
    strategi_uid uuid NOT NULL, version int NOT NULL,
    pas_skabelon       text NOT NULL,       -- version af K1's F1–F10
    regelsaet_id       int NOT NULL REFERENCES fabrik.regelsaet,
    datadeling_id      int NOT NULL REFERENCES fabrik.datadeling,     -- F2 (datoerne slås op)
    antal_forsoeg      int NOT NULL,        -- F3, talt fra fabrik.forsoeg, ikke skrevet i hånden
    mt_metode          text NOT NULL,       -- fx 'DSR', 'BH-FDR 10%' (K1: skriv hvilken metode)
    deflated_sharpe    numeric,             -- F4
    pbo                numeric,             -- Probability of Backtest Overfitting (K1)
    plateau_niveau     int,                 -- F5; betydning slås op i regelsaet (ingen fast skala)
    walkforward_andel_pos numeric,          -- F6: andel positive vinduer
    omkostningsmodel   jsonb NOT NULL,      -- F7: kurtage + slippage brugt
    max_drawdown       numeric,             -- største fald fra top til bund
    antal_handler_udv  int,                 -- F10
    f_resultater       jsonb NOT NULL,      -- {"F1":true,...} + tallene bag
    kendte_risici      text[],              -- 'MACD', 'MBB_antaget' …
    platform_verificeret text[] NOT NULL,
    oprettet           timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (strategi_uid, version),
    FOREIGN KEY (strategi_uid, version) REFERENCES fabrik.dvale_strategi
);
-- "Pengeskab åbnet ja/nej + dato" står ikke som felt her. Det slås op i
-- pengeskab_aabning, så det ikke kan skrives forkert to steder.
```

- **Hvordan "færdig" afgøres:** én fast visning `fabrik.faerdig_strategi`. Den kræver, at alle F-krav i `f_resultater` er sande, at pengeskabet er åbnet og bestået, og at `plateau_niveau >= regelsaet.dvale_min_niveau`. Er Thomas' grænse tom (NULL), giver sammenligningen "ukendt", og ingen strategi slipper igennem. **Databasen afgør ikke noget for Thomas. Den venter på ham.**
- **Hvem må skrive hvad:** Tre roller, i stedet for superbrugeren:

| Rolle | Må |
|---|---|
| `fabrik_arbejder` | tilføje rækker i signal/analyse/edge/forsoeg/job |
| `fabrik_dommer` | skrive `pengeskab_aabning` og `dvale_pas` |
| `thomas_admin` | ændringer, der skal godkendes |

  `REVOKE UPDATE, DELETE` på pas-, pengeskabs- og datadelingstabellerne virker først, når programmerne ikke længere kører som `postgres`. Rollerne afspejler også projektets regel om, at den, der finder en edge, ikke må være den, der dømmer den.

### 3.4 Migrationsvej – "ryd op og start forfra", ikke ombygning

Det gode nyheder: **produktionskørslen er ikke startet, og alle testdata er slettet** [Projekt: BESLUTNINGSLOG_2026-09-24.md:18-24]. Der er altså intet at flytte, kun noget at bygge. Derfor er vejen:

| Trin | Hvad | Rører eksisterende? |
|---|---|---|
| 0 | Fuld backup (`pg_dump`) af TradingDB til en anden disk. Tjek at den kan læses tilbage i en tom testdatabase. | Nej |
| 1 | Opret `TradingDB_test` og de tre roller. Vis SQL, få godkendelse. | Nej |
| 2 | Opret schema `fabrik` i *test*. Kør 13-filter-testen igen dér (samme 13 som 24/9). | Nej |
| 3 | Når testen er grøn: opret `fabrik` i produktion. Kopiér `filter_case` → `fabrik.filter` + `filter_version` (én gang, med fingeraftryk). `gammelt_nr` gemmer dagens nummer. | Kun læsning af `filter_case` |
| 4 | `filter_case`, `rawsignal`, `rawsignal_kontrol` og schemaet `rawsignal` bliver liggende urørt og markeres "gammel" i Videnslog. De er tomme for produktionsdata. De slettes først, når Thomas beslutter det. | Nej |
| 5 | Programmerne ændres til at bruge `fabrik` + rolle `fabrik_arbejder`. Det er K2's og byggerens arbejde. Jeg bygger ikke. | – |
| 6 | Fuld kørsel starter, når Thomas siger go. | – |

Der er ingen trin, hvor gamle tabeller ændres "lidt". Det er bevidst: projektets regel er at starte rent forfra, ikke at lappe [Projekt: VIDENSLOG.md, post 2026-09-24 "Ved fejl …"].

---

## 4. Fordeling over flere computere

### 4.1 Hvad licensen tillader – ærligt: UKENDT
- **TradeStation:** Jeg kunne ikke åbne TradeStations egne sider. Netværket blokerer tradestation.com og help.tradestation.com.
  - En søgeoversigt nævnte "can only be logged in to one computer at a time" fra en tredjepartsside [Net, ikke bekræftet: Trade Automation Toolbox, installationsvejledning].
  - Et forum nævner brugere med flere logins under samme konto [Net, ikke bekræftet: Elite Trader, "Using two computers at once", https://www.elitetrader.com/et/threads/using-two-computers-at-once.108367/].
  - **Konklusion: vi ved det ikke.** Det skal afklares skriftligt med TradeStation, før der købes maskiner.
  - Spørgsmålet til TradeStation kan være: *"Må samme konto være logget ind i TradeStation 10 på flere computere samtidig, udelukkende til backtest uden handel? Hvis ikke: hvad koster en ekstra login/konto, og kræver hver login sit eget data-abonnement?"*
- **MultiCharts:** En søgeoversigt gengiver MultiCharts' egen FAQ: én licens på én computer ad gangen. Til en ekstra computer uden handel findes en "Backtesting Edition"-licens [Net, ikke bekræftet: MultiCharts Knowledgebase, "Do I need an additional license to run MultiCharts on another computer?", https://www.multicharts.com/support/base/do-i-need-an-additional-license-to-run-multicharts-on-another-computer/]. **SANDSYNLIGT**, men ikke læst selv.

### 4.2 De tre veje og hvad de koster

| Vej | Fordel | Ulempe |
|---|---|---|
| **1. Flere TradeStation-logins/maskiner** | Samme platform som i dag. "TradeStation er facit" bevares. | Licensen er ukendt. Hver maskine skal have en ens opsætning (version, workspace, data). Backtesten skal stadig automatiseres (fund 2), og det er det dyreste stykke. |
| **2. MultiCharts som regnemaskine** | Er på planen i forvejen [Projekt: Task_…opgave.md:21]. Har egen portfolio-backtester. En backtest-licens kan være en billigere ekstra maskine (ikke bekræftet). | Kode skal porteres og bevises ens (K2's "gyldne sæt"). Endnu en platform at automatisere. |
| **3. Python regner signalerne** | Ingen licensgrænse. Kan køre på mange kerner og maskiner. Giver samtidig K1's uafhængige kontrol (en anden beregning, der skal give samme tal). Fjerner MACD-problemet, fordi Python ikke har TradeStations delte hukommelse. | 380 formler skal oversættes. Hvert filter skal bevises ens med TradeStation (bar for bar) på et datasæt. Prisdata skal eksporteres fra TradeStation (samme bars, samme session, samme tidszone). |

**Min anbefaling (råd, ikke beslutning): en blanding.**
- TradeStation bruges til det, kun TradeStation kan: Verify og en **facit-backtest pr. filter på ét referencedatasæt**. Det giver 380 backtests i alt, ikke 380 × 30.
- Python regner alle andre datasæt og alle senere led. Et filter må først bruges i Python, når dets Python-signaler er identiske med TradeStations på referencedatasættet.
- Regnestykke med 5 min pr. backtest (antagelse, se 2.6): 380 × 5 min ≈ 32 timer i TradeStation i stedet for 40 døgn.
- Det afgør ikke K1's eller K2's metoder. Det flytter kun, *hvor* der regnes.

**UENIGHED:** K2 foreslog i runde 1 at bygge alt i EasyLanguage og portere til MultiCharts. Mit forslag flytter tyngden til Python. Det skal vises åbent.

### 4.3 Er TDE-fjernstyringen (WM_COMMAND) et fundament at skalere på?

**Nej, ikke til backtest i stor skala. Ja, til sit nuværende job.**
- Det virker og er testet. Det virker også med fjernskrivebordet minimeret. Knap-klik sker med `PostMessage`, fordi `SendMessage` hænger [Projekt: BESLUTNINGSLOG_2026-09-24.md:93-121]. **BEVIST.**
- Kommandonumrene (10576, 10569, 57601, 10602) er læst ud af `TSResourceDllEng.dll` [Projekt: VIDENSLOG.md, 2026-09-24]. Det er TradeStations interne tal, ikke en lovet grænseflade. En opdatering af TradeStation kan ændre dem uden varsel. **SANDSYNLIGT risiko.**
- Stien er låst til "TradeStation 10.0" [Projekt: tde_styring.py:14]. Programmet er 32-bit og kræver 32-bit PowerShell [Projekt: tde_styring.py:16-17].
- Der har allerede været tilstande, hvor Verify ikke virkede efter en tvungen lukning [Projekt: tde_styring.py:64-66].
- Det dækker kun Verify: 380 × 2 filer, én gang. At åbne charts, skifte symbol, køre backtest og vente på "færdig" er et langt større og mere skrøbeligt stykke UI-styring. Det findes ikke endnu.

**Råd:**
1. Lås TradeStation-versionen på fabriksmaskinen (ingen automatiske opdateringer midt i en kørsel).
2. Programmet tjekker ved start, at TradeStation-build og DLL-fingeraftryk er de kendte. Er de ikke det: stop.
3. Én TDE pr. Windows-bruger, én arbejder pr. TDE.
4. Byg ikke en stor UI-robot til backtests, før TradeStation-licensen og Python-vejen er afklaret.

### 4.4 Kø og fejlsikring (kort, fordi princippet er uændret)
- Jobs ligger i én tabel i databasen. Hver maskine tager det næste job, den kan klare, med PostgreSQL's `FOR UPDATE SKIP LOCKED`, så to maskiner aldrig får samme job [Net: "PostgreSQL FOR UPDATE SKIP LOCKED: The One-Liner Job Queue", https://www.dbpro.app/blog/postgresql-skip-locked – fra søgning i runde 1, ikke åbnet i denne runde: **ikke bekræftet**].
- Jobtyper: `TDE_VERIFY` (kræver TDE), `TS_FACIT_BACKTEST` (kræver TradeStation), `CSV_LOAD`, `PY_SIGNAL`, `ANALYSE`, `EDGEFINDER`, `CRUNCHER` (Python) og `PENGESKAB` (kun rolle `fabrik_dommer`).
- Hver maskine melder "jeg lever" hvert minut. Tavs i 10 minutter betyder, at jobbet er fejlet. Dets halve filer slettes, og det lægges i kø som et *nyt* forsøg. Efter 3 fejl stopper jobbet og venter på et menneske.
- Et fejlet job i en kørsel stopper ikke de andre filtre (Thomas' "log og fortsæt" [Projekt: OPGAVEBESKRIVELSE_Automation.md, "Krav til selve kørslen" pkt. 2]). Men en kørsel kan kun blive "færdig", når *alle* dens jobs er færdige. Ellers kasseres den.
- Databasens adresse skal flyttes fra den faste `127.0.0.1` [Projekt: faelles.py:38] til opsætningsfilen, så andre maskiner kan nå den over det lokale net.

---

## 5. Drift på fond-niveau – i projektets målestok

### 5.1 Backup og gendannelse
PostgreSQL har tre slags backup: SQL-dump, kopi af filerne og løbende arkivering [Net: "Backup and Restore", backup.sgml, https://raw.githubusercontent.com/postgres/postgres/master/doc/src/sgml/backup.sgml – åbnet]. Et `pg_dump` "represents a snapshot of the database at the time pg_dump began running" og blokerer ikke andet arbejde (samme kilde).

| Hvad | Hvordan | Hvorfor |
|---|---|---|
| Små, vigtige tabeller (filter, filter_version, datasaet, koersel, regelsaet, datadeling, forsoeg, pengeskab, dvale_*) | `pg_dump` hver nat til en anden disk + ugentligt ud af huset (krypteret) | Kan ikke genskabes. Pengeskabs-åbninger og antal forsøg er uerstattelige: et tabt forsøgstal gør K1's korrektion umulig. |
| Råsignaler (`fabrik.signal`) | Ugentligt eller efter hver færdig kørsel | Kan genskabes, men det koster dage (afsnit 2.6) |
| Fil-lager (.el, .csv, pris-eksport) | Samme nat, samme sted | Koden i dvale skal kunne hentes bit for bit |
| **Gendannelsesprøve** | Én gang om måneden: gendan nattens dump i `TradingDB_test` og tæl rækker | En backup, der aldrig er læst tilbage, er ikke bevist |

Løbende arkivering med gendannelse til et bestemt tidspunkt (PITR, samme kilde, afsnit "Continuous Archiving and Point-in-Time Recovery") er ikke nødvendig nu. Den bliver det, når der handles live. [Antagelse: data i udviklingsfasen kan tåle at miste højst ét døgn.]

### 5.2 Overvågning
- Én side, der kun læser: jobs pr. status, maskiner med livstegn, kørsler i gang, fejl i dag, fri diskplads.
- **Rød** når en maskine er tavs over 10 minutter, et job har fejlet 3 gange, disken er over 80 % fuld eller nattens backup mangler.
- Alle logs samles i én tabel `fabrik.haendelse` i stedet for tekstfiler på hver maskine (i dag: `log\rawsignal_creature.log` [Projekt: faelles.py:11]).

### 5.3 Reproducerbarhed (at et resultat kan genskabes bit for bit)
Et resultat er kun genskabeligt, hvis disse fem ting er gemt:

| Nr. | Hvad | Hvor |
|---|---|---|
| 1 | Filterets version | `formel_sha256` |
| 2 | Programmets version | `git_commit` |
| 3 | Platformens version | `ts_version` |
| 4 | Opsætningen | Max Bars Back, sessionsskabelon, tidszone |
| 5 | **Selve prisdataene** | `prisdata_sha256` |

- Nr. 5 mangler helt i dag. Leverandører retter somme tider historiske data. Så kan samme backtest give et andet svar næste år, uden at noget i koden har ændret sig. [Antagelse: almindeligt for dataleverandører. Ikke eftervist for TradeStation.]
- Råd: eksportér de bars, der bruges, én gang pr. datasæt. Gem dem som fil med fingeraftryk, og lad Python regne på netop den fil.
- **Prøve:** K2's "dobbeltkørsel" (samme filter to gange = samme tal) bør køre automatisk for et tilfældigt filter pr. kørsel. Samme fingeraftryk på resultatet er beviset.

### 5.4 Test og produktion helt adskilt
Min første udgave glemte to ting, der ikke ligger i databasen:

1. **TradeStations eget bibliotek af strategier er fælles.** En test-strategi `RawSignal001` og en produktions-`RawSignal001` er den samme ting i TradeStation. Programmet overskriver en eksisterende strategi med samme navn [Projekt: tde_styring.py:126-127]. **Råd:** test-filer får et præfiks i navnet, fx `T_RawSignal001`.
2. **CSV-stien står ordret i koden** (1.2 H). Test skal bygges med sin egen mappe, fx `C:\TradingDB_Folder_TEST\`.

Ellers:
- Separat database `TradingDB_test`.
- Opsætningsfilen på hver maskine siger "TEST" eller "PRODUKTION". Ordet står øverst på alle skærme og i alle logs.
- Et program i test-tilstand nægter at forbinde til produktionsdatabasen (tjek af databasenavn ved opstart).

---

## 6. Plug-and-play – hvad Thomas ser og trykker på

Det forudsætter en styringsflade. TradingApp er planlagt, men det er uklart, hvor meget der findes [Projekt: OPGAVEBESKRIVELSE_Automation.md beskriver en fane med Kør, Maskine-valg, Fra filter nummer, Kontrol, Pause, Live Log]. Jeg bygger videre på den fane. Thomas indsætter ikke tekst i prompten. Hans kommandoer ligger som .bat-filer på skrivebordet [Projekt: BESLUTNINGSLOG_2026-09-24.md:129-130]. Det bevares.

**Trin 1 – Start maskinerne.**
- Thomas dobbeltklikker `Start fabrik.bat` på hver maskine.
- Vinduet siger: *"PRODUKTION – maskine PC-A – kan: TradeStation – forbundet til TradingDB – klar."*

**Trin 2 – Ny kørsel.**
- I fanen trykker han **Ny kørsel** og vælger fra lister:
  - Led (fx "Råsignaler")
  - Datasæt (fx "@ES 5 min 2019–2026")
  - Hvilke filtre (alle / nye / enkelte)
- Skærmen viser: *"Dette vil lave 380 jobs. Anslået tid: ~32 timer på 1 maskine. Kodeversion a1b2c3. Regelsæt: 'Plateau udkast 1 – IKKE godkendt'."*
- Han trykker **Start**.

**Trin 3 – Følg med.**
- **Fremdrift**: en bjælke pr. kørsel med tal for færdige, i gang, venter og fejlet, plus en grøn/rød lampe pr. maskine.
- **Live Log** som i dag.

**Trin 4 – Hvis noget er rødt.**
- Skærmen skriver i almindeligt sprog, fx *"Filter F0068 fejlede 3 gange: TDE svarer ikke."*
- To knapper:
  - **Prøv igen forfra** (kun det job)
  - **Kassér hele kørslen** (alt fra kørslen smides ud som én skuffe, og kørslen kan startes på ny)
- Der er ingen knap for "ret lidt i resultatet". Det er med vilje.

**Trin 5 – Næste led.** Når råsignalerne er færdige, lyser **Start analyse** op. Det samme gælder EdgeFinder og EdgeCruncher. Man kan ikke starte et led, før det forrige er "færdig".

**Trin 6 – Godkendelser, kun Thomas.** Tre ting kræver hans tryk og viser først præcis, hvad der sker:
- **Lås datadeling** (datoerne vises og kan ikke ændres bagefter)
- **Godkend regelsæt** (plateau-trappe og dvale-grænse)
- **Godkend databaseændring** (den præcise SQL vises)

**Trin 7 – Pengeskab.** For hver kandidat viser skærmen: *"STR-000123 har bestået F1–F8 og F10. Pengeskabet kan kun åbnes ÉN gang. Åbn?"* Når der trykkes, kører K1's slutkontrol (rollen `fabrik_dommer`). Resultatet står der for altid.

**Trin 8 – Dvale.** Bestået strategier dukker selv op under **Dvale-lager**: en liste med de vigtigste pas-tal side om side, sortérbar. Knappen **Vis pas** åbner hele passet i almindeligt sprog. **Væk** henter koden, tjekker fingeraftrykket og kører den igen på samme data. Den nægter, hvis tallene ikke matcher.

---

## 7. Vejledning i almindeligt sprog

Tænk på fabrikken som et bageri.

- **Opskrifterne (filtrene)** får hver et navneskilt, der aldrig skiftes, og et versionsnummer. Ændrer man en opskrift, bliver det version 2. Version 1 forsvinder ikke.
- **Hver bagning (kørsel)** får sin egen bakke. Går en bagning galt, smides hele bakken ud, og man bager forfra. Man skraber ikke det brændte af.
- **Tavlen på væggen (databasen)** viser alle opgaver. Ovnene (computerne) tager selv den næste seddel. Ingen seddel kan tages af to ovne.
- **Øvebageriet** er et helt andet rum med egne bakker, eget navn på kagerne og egen tavle.
- **Kagedåsen (pengeskabet)** må kun åbnes én gang pr. kage. Den, der har bagt kagen, må ikke selv åbne den. Det gør smagsdommeren.
- **Fryseren (dvale-lageret)** har en mærkat på hver æske: opskrift og version, hvilken ovn, hvilket mel (prisdata), hvilke prøver den bestod, og hvor mange kager der blev prøvet i alt for at finde den.
- **Hver nat** tages en kopi af alle mærkater og opskrifter, som lægges et andet sted. Én gang om måneden prøver man at bage ud fra kopien, så man ved, at den virker.
- Thomas skal kun: trykke **Start**, kigge på lamperne, trykke **Prøv igen** eller **Kassér**, og godkende de få ting, som kun han må bestemme.

---

## 8. Angreb på mit eget første udkast

| # | Hvad jeg skrev | Hvad der var galt |
|---|---|---|
| 1 | Byggede alt på statusrapporten | Jeg kendte ikke `rawsignal.rawsignal<nr>`, den faste CSV-sti eller den manglende markeds-kolonne. Mit vigtigste fund i dag (kun ét marked kan gemmes) manglede helt. |
| 2 | `REVOKE UPDATE, DELETE` som sikring af pengeskabet | Virker ikke, fordi alt kører som superbrugeren `postgres` (faelles.py:38). Det var en falsk tryghed. |
| 3 | `CHECK (plateau_niveau ~ '^PL[1-7]$')` | Afgjorde Thomas' åbne punkt om trappens længde. K1 havde ret. Nu er Thomas' valg data i `regelsaet`. |
| 4 | Job-kø over flere TradeStation-maskiner | Tog for givet, at backtesten var automatiseret. Det er den ikke. Den dyreste del var usynlig i min tegning. |
| 5 | Test/produktion = to databaser | Glemte TradeStations fælles strategi-bibliotek og den faste CSV-sti i koden. To databaser er ikke nok. |
| 6 | Kun et UUID som filter-ID | K1 havde ret: der skal også være en version (formlen kan ændres). |
| 7 | Ingen tal for datamængde | Nu regnet: 6–39 GB pr. datasæt, 40 døgn med én maskine i et realistisk tilfælde. |
| 8 | "Overvej MultiWalk" | Ikke undersøgt. Kunne ikke åbne siden. K2's indvending (et lukket værktøj gør det svært at bevise tællingen af forsøg, F3) står stadig. Jeg trækker forslaget tilbage, indtil nogen har undersøgt det. |
| 9 | Log-oplysning om TradeStation-login | Var ikke bekræftet og er det stadig ikke. Nu skrevet som et spørgsmål til TradeStation i stedet for en halv påstand. |
| 10 | "Fire knapper" | For løst. Nu beskrevet trin for trin, bygget på den fane, Thomas selv har beskrevet. |

---

## 9. Uenigheder (vises åbent)

1. **Python som hovedregnemaskine (mig) mod EasyLanguage/MultiCharts hele vejen (K2's runde 1).** Ikke afgjort.
2. **Filter-ID (U5):** Jeg tilslutter mig nu K1: fast ID *og* version. Den uenighed er løst fra min side.
3. **PL-låsen (U4):** Løst. Låsen er fjernet.
4. **Kontrolresultater (U6):** Jeg fastholder, at kontroller af rigtige filtre er produktionsdata. Placebo-signaler hører i test.
5. **Automatisk skrivning i databasen:** Mit design kræver, at godkendte programmer skriver resultater uden at spørge hver gang (kun gennem rollen `fabrik_arbejder`, kun tilføje). Det kan kollidere med den bogstavelige læsning af projektets regel. Thomas afgør.

---

## 10. Nye åbne punkter til Thomas

1. **Markeder og tidsrammer:** Hvor mange datasæt skal fabrikken køre? Det afgør både lagerplads (0,2–1,2 TB) og tid (dage til måneder).
2. **Kun ét marked kan gemmes i dag.** Skal den fulde kørsel vente, til marked/kørsel er med i datamodellen? (Råd: ja. Beslutning: din.)
3. **TradeStation-licens:** Spørg TradeStation skriftligt om samtidige logins til backtest (spørgsmålet står i 4.1).
4. **Python-vejen:** Må signalerne regnes i Python og bevises ens med TradeStation på ét referencedatasæt?
5. **Roller i stedet for superbruger:** Må programmerne få egne, begrænsede database-brugere?
6. **Må godkendte programmer skrive resultater automatisk** (kun tilføje, gennem en begrænset rolle)?
7. **Filter-version:** Skal en ændret formel eller et ændret Fra/Til/Step give en ny version i stedet for en ændring af den gamle?
8. **Overblik pr. filter:** Er visninger pr. filter (`rawsignal_vis.f0001`) lige så gode for dig som rigtige tabeller?
9. **Backup:** Findes der i dag backup af TradingDB uden for serveren? Hvor må kopien ligge (anden disk, sky, USB-disk)?
10. **Tidszone og datakilde:** Skriver TradeStation børsens tid eller lokal tid i CSV'en? Og hvilke symboler og tidsrammer var Data1/Data2/Data3 ved filter 1-målingen?
11. **TradeStation-opdateringer:** Må versionen låses på fabriksmaskinen?
12. **Det uenige tal for MACD-filteret (4.918 mod 480 signaler):** Hvilket er rigtigt? NOTER.md og BYGGEVEJLEDNING bør rettes. Det står allerede som åbent punkt i beslutningsloggen.

---

**Hvad der mangler:**
- Tid pr. backtest er ikke målt.
- Antal kombinationer pr. filter er ikke kendt. Derfor er datamængden vist som scenarier.
- TradeStations og MultiCharts' licensregler er ikke bekræftet, fordi deres sider var blokeret for mig.
- Tabellerne for led 2–4 er kun skitseret som navne (`analyse_kombination`, `edge_kombination`, `kandidat`). Deres kolonner afhænger af K1's metoder og K2's design.
- Intet SQL er afprøvet.


# Del 4 – Samlet overblik (den overordnede agent)

*Jeg har ikke rettet i konsulenternes dele. Her samler jeg dem. Jeg viser, hvor de er enige og uenige. Jeg peger på det, der går på tværs af delene. Og jeg samler alle åbne punkter i én liste i den rækkefølge, de bør afgøres.*

## 4.1 Det store billede: tre fund, der hænger sammen

De tre konsulenter har arbejdet hver for sig og er nået frem til fund, der bygger på hinanden:

1. **Signalet kan være forkert uden at nogen opdager det** (K2). MACD-typen giver 625 ens signalrækker. Opvarmningen er for kort for lange udglatninger. Filen fortæller ikke, hvilket marked den kommer fra.
2. **Et forkert signal ser ud som et godt signal** (K1). Ens rækker ligner et perfekt plateau. Det tal for antal forsøg, som lyder rigtigt ("625"), er i virkeligheden 0 gyldige.
3. **Og dataene kan ikke spores bagud** (K3). Der er ingen kolonne for marked, kørsel eller kodeversion. Den næste kørsel sletter den forrige. Fejl bliver ikke skrevet i databasen.

Tilsammen betyder det: **Hvis den fulde kørsel startes i dag, vil fabrikken kunne producere strategier, der ser robuste ud, uden at nogen kan se, at de er falske. Og uden at nogen bagefter kan finde ud af, hvilke resultater der skal kasseres.** [Antagelse: samlet ud fra del 1–3. Hvert enkelt led er BEVIST i koden, men den samlede effekt er ikke målt.]

Den gode nyhed er, at produktionen ikke er startet, og at alle testdata er slettet [Projekt: BESLUTNINGSLOG_2026-09-24.md]. Alt kan derfor rettes ved at bygge rent, uden at reparere noget. Det passer præcis med projektets princip om at starte forfra.

## 4.2 Det strategiske spørgsmål, som alt andet afhænger af

K1's regnestykke (del 1, afsnit 4.2) er efter min vurdering det vigtigste i hele rapporten. Hvor mange års data der skal til, afhænger kun af to ting: hvor stærk edgen er (årlig Sharpe), og hvor høj grænsen er (t). Hvor mange handler der er om året, er ligegyldigt.

| Hvis projektet har ... | ... kan fabrikken ærligt finde enkeltsignaler med årlig Sharpe på mindst ca. |
|---|---|
| 3 års data | 3,2 |
| 5 års data | 2,5 |
| 10 års data | 1,7 |
| 20 års data | 1,2 |

[Regnet af den overordnede agent med K1's formel S = (4,65 + 0,84) / √år. Formlen er BEVIST som algebra. Grænsen t = 4,65 er K1's midtscenarie, ikke målt.]

**Hvad det betyder for målet:** De bedste systematiske fonde løser netop dette problem på tre måder: meget lang historik, mange markeder og færre, men bedre begrundede forsøg [Antagelse: almindelig viden i faget. Kilderne kunne ikke åbnes]. K1 nævner de samme tre håndtag. Derfor bør Thomas afgøre to ting, **før** metoderne låses:

- **Hvor meget intradag-historik** findes der pr. marked?
- **Hvor mange markeder** skal den samme regel testes på?

Svaret afgør, om fabrikken skal lede efter mange svage signaler (kræver mange markeder og lang historik) eller få stærke (så kan den nøjes med mindre).

## 4.3 Fase 0: det, konsulenterne anbefaler før den fulde kørsel

Det er samlet fra alle tre dele. Det er råd, og Thomas beslutter. Rækkefølgen er min. Den er valgt, så de billigste og mest afslørende ting kommer først.

| # | Hvad | Hvorfor | Hvem/hvor | Skøn over omfang | Fra |
|---|---|---|---|---|---|
| 0.1 | **Fuld backup af TradingDB til en anden disk, og læs den tilbage i en testdatabase** | Den eneste backup i dag ligger i samme database | Lokal session, kun læsning af produktion | Timer | K3 §3.4, §5.1 |
| 0.2 | **K0: liste over alle funktioner i de 380 formler og deres type** (series/simple, aflæst i TDE) | Afgør, hvor mange filtre der er i fare. I dag ved ingen det | Lokal session, kun læsning | 1–2 timer | K2 §2.3, §4 |
| 0.3 | **K1 + K2: automatisk gruppering af alle filtre i gruppe A–E og læsning af Verify-advarslerne** | Gratis. Viser fx, at filtre med advarsler står som "Pass" i dag | Python, ingen TradeStation | Minutter | K2 §4 |
| 0.4 | **Test T1 på filter 68 med Fra = Til** mod en fil uden løkke | Afgør, hvilken forklaring på MACD-fejlen der er rigtig. Det ændrer, hvordan ramte filtre skal bygges om | TradeStation, 2 kørsler | Under en time | K2 §2.2; K1 §9 |
| 0.5 | **T1 pr. funktionstype** (ca. 15–20 typer) | Beviser, hvilke funktioner der må blive i løkken | TradeStation | Ca. 1 dag | K2 §4 (K3) |
| 0.6 | **Tag stilling til datamodellen: marked, kørsel, filter-ID og version, journal med fejl og advarsler** | Uden det kan kun ét marked gemmes, og fejl kan ikke spores | Thomas godkender SQL; bygges i test først | Dage | K3 §3 |
| 0.7 | **Lad CSV'en bære sin oprindelse** (symbol, interval, session, bar-nummer) | Så en fil aldrig kan forveksles | Generatoren, Thomas beslutter | Timer | K2 §1.7; K3 §3.3 D |
| 0.8 | **Lås datadelingen og definitionen af "et forsøg"**, før resultater ses | Ellers vælges metoden efter resultatet (ubevidst) | Thomas | Én beslutning | K1 §3, §4.4 |
| 0.9 | **Spørg TradeStation skriftligt om samtidige logins** | Afgør, om fabrikken kan fordeles over flere TradeStation-maskiner | Thomas | Én e-mail | K3 §4.1 |

**Det er ikke med i Fase 0:** at bygge RawSignal-Analyse, EdgeFinder og EdgeCruncher. De kan først bygges ordentligt, når Fase 0 har vist, hvilke filtre der kan stoles på.

## 4.4 Hvor konsulenterne er enige

| Emne | Enighed | Del |
|---|---|---|
| Antal forsøg | Tælles i millioner. N_eff måles med korrelation eller placebo og gættes ikke | K1 §3, K3 §3.3 G |
| MACD-ramte filtre | Skal bygges om (vej a). Ingen strategi fra et ramt filter kan blive "færdig". K1 har skiftet holdning | K1 §13.11, K2 §4 |
| Python som regnemaskine | TradeStation laver facit, og Python regner resten, bevist ens bar for bar. K2 har skiftet holdning | K1 §10, K2 §2.4, K3 §4.2 |
| Facit for gruppe A/C/D | Kan ikke være dagens løkke-fil. Laves uden løkke på udvalgte kombinationer | K1 §10.4, K2 §2.4 (K3 har ikke skrevet det ind) |
| Opvarmning | Er en tavs risiko, som Max Bars Back ikke løser. K1 sætter grænsen til 0,1 % og kræver en "to-starts-test" | K1 §5, K2 §1.4, K3 §3.3 D2 |
| Pengeskabet | Åbnes én gang af et separat trin og håndhæves af databasen. Det kan kun kassere, ikke bevise | K1 §4.4, K3 §3.3 G |
| Filter-ID | Fast ID *og* version (tidligere uenighed U5 er løst) | K1 §1, K3 §1.2 B |
| PL1–PL7 | Må ikke være låst i databasen. Thomas' valg gemmes som data (tidligere U4 er løst) | K1 §8, K3 §3.3 F |
| Superbruger | Programmerne skal have begrænsede roller. K3's rolle "dommer" håndhæver reglen om, at den der finder en edge, ikke må dømme den | K3 §3.3 |
| EdgeFinder | Ikke godkendt endnu. Der mangler en skriftlig og låst metode (E1–E8) | K1 §6, K2 §5 |

## 4.5 Hvor konsulenterne stadig er uenige (vist åbent)

| # | Emne | Synspunkt A | Synspunkt B | Min vurdering |
|---|---|---|---|---|
| U1 | **Facit: ét referencedatasæt eller pr. workspace-type?** | K3: ét referencedatasæt | K2: pr. workspace-type, fordi sessioner og Data2/Data3 ikke kan antages ens. K1 kræver ét år + 20 filtre på et andet marked | K2's argument er stærkest. Forskellen i omkostning er lille (4 mod 1 facit pr. filter) [Antagelse] |
| U2 | **Max Bars Back-testen (1000 mod 2000)** | K1 beholder den som test | K2: den afslører intet, fordi begge kørsler starter "kolde". Test opvarmning i stedet | K1 har *tilføjet* opvarmningstesten, så uenigheden er næsten løst. Om MBB-testen overhovedet giver værdi, bør K1 og K2 afklare |
| U3 | **Placebo-signaler: i test eller produktion?** | K1: gemt adskilt fra produktionsdata | K3: samme linje, eget nummerområde, udelukket fra visninger. K1 (kritik): resultaterne skal gemmes med produktionskørslen | Thomas afgør. Projektets regel "test må ikke blandes med produktion" skal fortolkes |
| U4 | **Kontrolresultater** | K2: adskilt fra produktion | K3: kontroller af rigtige filtre *er* produktionsdata | Thomas afgør (samme fortolkning som U3) |
| U5 | **Walk-forward i passet** | K3's pas har "andel positive vinduer" | K1: skal være en samlet t-værdi, for tilfældighed giver 50 % positive | K1 har ret fagligt. K3 har ikke nået at rette det |
| U6 | **Faste kolonner for N_eff og t i passet** | K3: N_eff står i forsøgsregnskabet | K1: skal stå som faste kolonner i passet, så strategier kan sammenlignes | Mindre punkt. Bør rettes |
| U7 | **K2's 84.400 enkeltkørsler** | K2: som mulig vej for gruppe A/C/D | K1 og K3: kun som stikprøve (117–233 døgn på én maskine) | K2 har selv gjort Python-vejen til hovedanbefaling, så i praksis er det løst |
| U8 | **Opvarmning pr. filter eller pr. filter × datasæt** | K2: pr. filter | K3: pr. filter × datasæt, fordi bars betyder noget forskelligt i 5- og 120-minutters data | K3's argument er stærkest [Antagelse] |
| U9 | **Automatisk skrivning i databasen** | K3: godkendte programmer skal skrive resultater uden at spørge hver gang | Projektets regel: hver ændring vises og godkendes | Thomas afgør. Uden dette kan fabrikken ikke være automatisk |

**Rettelser mellem delene, som jeg har fundet:**

- K2 §4 skriver stadig "K1 accepterer b og c". Efter kritikrunden er K1 enig i vej a (K1 §13.11).
- K3 §1.2 A og åbent punkt 12 kalder "4.918 mod 480" en uafklaret modstrid. NOTAT'et retter selv 480 til 4.918 [Projekt: NOTAT_til_BYGGEVEJLEDNING_RawSignal.md:9]. Det er selve BYGGEVEJLEDNING, der ikke er opdateret.
- K3 §2.6 regner med 625 kombinationer for alle filtre (237.500 kørsler). Den rigtige fordeling (128/114/62/77 filtre) giver ca. 84.476 pr. workspace (K1 §3.1, K2 §2.4).

## 4.6 Den overordnede agents egne bemærkninger

1. **Tre konsulenter fandt uafhængigt af hinanden det samme grundproblem.** En kørsel identificeres kun ved filterets nummer. Det gælder filnavnet, `FileDelete` i EasyLanguage og `delete from` i databasen. Når tre fagområder rammer den samme fejl fra hver sin side, er det et stærkt tegn på, at den er vigtig.
2. **Projektets egen forklaring på MACD-fejlen er sandsynligvis forkert.** NOTER.md siger "hukommelsen blandes". Målingen (625 *ens* rækker) passer bedre med K2's forklaring: funktionen regnes én gang pr. bar. Det betyder noget, fordi så kan også en fil med kun ét parametersæt være forkert. Test 0.4 i Fase 0 afgør det på under en time.
3. **AvgTrueRange-testen er bedre end først antaget, men stadig ikke et bevis.** K2 påpeger, at netop de 5 "umulige" kombinationer mangler. Det viser, at parametrene når frem til funktionen. Men om tallene er *rigtige*, kræver T2/T3 (del 2 §3).
4. **Plug-and-play og stringens trækker i hver sin retning.** Rapporten foreslår mange nye kontroller. K3's trin-for-trin-skærmbilleder (del 3 §6) viser, at det godt kan skjules bag få knapper. Det kræver dog, at TradingApp bygges som et rigtigt styringsværktøj. Det er et projekt i sig selv.
5. **Kilderne.** Ingen af de faglige artikler og ingen af platformenes officielle sider kunne åbnes. Regnestykkerne står på egne ben, men tre ting *skal* bekræftes mod officielle kilder, før der bygges:
   - TradeStations regler for series functions i løkker,
   - TradeStations og MultiCharts' licensregler,
   - formlen for Deflated Sharpe.
6. **Hvad der ikke er nået:**
   - kolonnerne i tabellerne for led 2–4,
   - en målt tid pr. backtest,
   - en målt N_eff,
   - en skriftlig EdgeFinder-metode (K1 godkender, Thomas og K2 skriver),
   - en vurdering af, om commit `12120a8` (den håndregnede MACD) kan bruges som skabelon.

## 4.7 Samlet liste over åbne punkter til Thomas (i den rækkefølge, de bør afgøres)

**A. Afgør først, fordi de styrer alt andet**

1. **Hvor mange års intradag-data og hvor mange markeder** er der? (K1 §13.1, K3 §10.1) Svaret afgør, hvilke edges fabrikken overhovedet kan finde (4.2).
2. **Skal den fulde kørsel vente på Fase 0?** (4.3; opgavens punkt 9)
3. **Hvad tæller som ét forsøg?** Skal step, retning og horisont ligge fast på forhånd for at få færre forsøg? (K1 §13.2)
4. **Datadelingen:** hvilke datoer, og hvor stort skal pengeskabet være? (K1 §13.6)
5. **Må godkendte programmer skrive resultater automatisk** gennem en begrænset rolle? (U9, K3 §10.6)

**B. Afgør, før der bygges videre**

6. **MACD-ramte filtre:** Konsulenterne er nu enige om vej a (byg om). Hvilket mønster skal bruges, og skal commit `12120a8` genoplives? (K2 §8.5; opgavens punkt 4)
7. **Python som regnemaskine med TradeStation som facit?** (K3 §10.4)
8. **Facit pr. workspace-type eller ét referencedatasæt?** (U1)
9. **Datamodellen:** fast ID + version, marked og kørsel, roller i stedet for superbruger, visninger pr. filter i stedet for 380 tabeller? (K3 §10.2, 10.5, 10.7, 10.8)
10. **Verify-advarsler:** Skal "Pass med advarsel" markeres som mistænkt? (K2 §8.1)
11. **Oprindelse i CSV'en** (symbol, interval, session, bar-nummer) og et udvidet tjek af Data1? (K2 §8.7–8.8)
12. **Opvarmning:** Skal der udregnes et vindue, og skal signalerne i det kasseres? Er K1's grænse på 0,1 % i orden? (K2 §8.6)
13. **Placebo- og kontrolresultater:** Skal de ligge i test eller produktion? (U3, U4)
14. **TradeStation-licens:** Send spørgsmålet i del 3 §4.1.

**C. Afgør, når metoderne skal låses**

15. **Plateau-trappen:** farvemetode A, B eller C, placebo-rate pr. niveau, og hvilket niveau der er nok til dvale (K1 §8; opgavens punkt 9)
16. **Hvad er en event,** og hvornår starter handlen? Anbefalingen er ved åbningen af næste bar. (K1 §13.4, K2 §8.9)
17. **Hvor færdig er EdgeFinder reelt?** Konsulenterne har ikke fundet mere end en signal-optager (K1 §6; opgavens punkt 9)
18. **Hvad er EdgeCruncher tænkt som?** "Edge → strategi med udgange", "kombination af filtre" eller begge? (K2 §8.10)
19. **Grænserne i F1–F10:** t ≈ 4,65, DSR ≥ 0,95 og PBO kalibreret med placebo (K1 §1, §4)
20. **Omkostningsmodel pr. marked** (K1 §13.10)
21. **Genvækning:** Bayes-grænse (fx 80 %) og regime-tjek (K1 §11)

**D. Drift og oprydning**

22. **Backup uden for serveren:** hvor, og hvor tit? (K3 §10.9)
23. **Lås TradeStation-versionen** på fabriksmaskinen (K3 §10.11)
24. **Tidszone og symboler** for Data1–3 ved filter 1-målingen (K3 §10.10)
25. **Decimaltrin:** Skal generatoren afvise trin, som ikke kan gemmes præcist? (K2 §8.12)
26. **Dokumentation:** Opdatér BYGGEVEJLEDNING (4.918, ikke 480), NOTER.md (MACD-forklaringen) og RawSignal266-filhovedet (Average er målt i orden) (K1 §13.7)
27. **Officielle kilder:** Hvem læser TradeStations og MultiCharts' hjælp om series functions og licenser? (K2 §8.11)


# Bilag – Konsulenternes kritik af hinanden (dybde-runden)

## K1's kritik af udkast2/k2.md og k3.md

**Rettet i min k1.md:**
- Afsnit 3.1: N_rå regnet ud fra projektets fordeling (128/114/62/77): 84.476 kombinationer pr. workspace, ca. 3,4 mio. i alt.
- Filtre ramt af MACD-typen giver i dag 0 gyldige forsøg.
- Afsnit 5: grænse for opvarmning på 0,1 % og en "to-starts-test".
- Afsnit 10: krav til beviset for, at Python og TradeStation giver ens tal.
- Punkt 11: jeg går over til K2's vej a for MACD.

### (a) Godkendelse

- **K2's kontrolplan K0–K6 (afsnit 4): GODKENDT.** K0–K2 er gratis. K5's invarianter er god sanering.
- **K2's T1–T3 (afsnit 3): GODKENDT.** T1 skal bruge en ren fil uden løkke, ikke Fra = Til.
- **K2's MACD-forklaring (2.2): GODKENDT som arbejdshypotese.**  For mit tal betyder det, at de ramte filtre ikke giver 1 forsøg, men **0 gyldige**, fordi signalet måske hører til en N uden for gitteret. N_rå (loft) er uændret, når filtrene er bygget om. N_eff skal altid tælles på unikke, kontrollerede signalrækker.
- **K2's opvarmning (1.4): Grænsen er min opgave.** Den er sat til **0,1 %** tilbageværende startvægt. (EMA 600: ca. 2.070 bars). Det skal bevises med to-starts-testen: 100 % ens signaler efter vinduet.
- **K2's EdgeCruncher (5): GODKENDT.**
- **K3's regelsaet, datadeling og forsoeg-tabel (FORSLAG G/H): GODKENDT.**
- **K3's Python-vej med én facit-kørsel pr. filter (4.2): GODKENDT statistisk**, men kun med beviskravene nedenfor. Den er bedre end K2's 84.400 kørsler. Deterministiske beregninger kræver ikke, at alt køres.
- **K3's pas-felter: GODKENDT, men der mangler felter** (se b).

**Beviset for, at Python og TradeStation er "ens", skal indeholde:**
1. Alle filtre og alle kombinationer på et referencedatasæt på mindst ét år, der dækker både rolige og urolige perioder.
2. Samme bars, dokumenteret med en hash.
3. Starttid, AntalBars og Afsluttet skal være 100 % ens efter opvarmningen. Grænsetilfælde tælles, og der må højst være 1 pr. 10.000 signaler.
4. For gruppe A/C/D er facit **enkeltkørsler uden løkke**: 5 kombinationer pr. filter, ca. 650 tjek. Er der 0 fejl, er under 0,5 % af kombinationerne forkerte.
5. Mindst 20 filtre skal også stemme på et andet marked.
6. Python skrives uden at se EasyLanguage-koden.

### (b) Fejl og huller

- **K3 FORSLAG H, `walkforward_andel_pos`:** Det bygger på mit gamle, svage kriterium. Det skal erstattes af en **t-værdi for de samlede walk-forward-perioder** og antallet af kandidater (F6 v2).
- **K3's pas mangler:** N_eff (F3 kræver både rå og effektivt antal), t-værdi (F4), F8-tallene (negative år og største års andel), opvarmningsvindue, kontrolstatus K0–K6, retning, horisont, event-definition og antal unikke signalrækker. N_eff og t skal være faste kolonner.
- **K3's regelsaet** mangler de talgrænser, jeg foreslår, at Thomas vælger: t-grænse, DSR, PBO, placebo-rate, pengeskabets størrelse og Bayes-grænse for genvækning. De skal være data, ikke kode.
- **K3 mangler en tabel for genvækning.** Resultaterne af brudtest, Bayes og regime gemmes ingen steder.
- **K3's facit-kørsel (4.2):** Den løkke-baserede facit i TradeStation er selv forkert for MACD-typen. Det nævnes ikke.
- **K2 (2.4, mønster 1):** 84.400 kørsler er ikke nødvendige som bevis. En stikprøve af enkeltkørsler er nok (se ovenfor).
- **K2 (4):** "K1 accepterer b og c" er ikke længere rigtigt. Se (c).

### (c) Uenigheder

1. MACD: løst. Jeg går over til K2's vej a (byg om).
2. K2's 84.400 enkeltkørsler mod K3's facit + Python: jeg støtter K3 med beviskravene ovenfor, plus K2's enkeltkørsler som facit for gruppe A/C/D.
3. K3: placebo-signaler hører til i test. Enig for selve signalerne, men placebo-*resultaterne* bruges til at kalibrere grænserne, så de skal gemmes sammen med produktionskørslen.
4. K3's `walkforward_andel_pos` skal erstattes af en t-værdi (min egen gamle fejl).

## K2's kritik af K1 og K3 (runde 2)

**Rettet i k2.md:** Nyt mønster 5 i afsnit 2.4 (K3's plan: Python regner, TradeStation er facit) er nu min hovedanbefaling i stedet for 84.400 kørsler, med to forbehold. K4 og MultiCharts-afsnittet er tilpasset.

### (a) Kan det bygges?

**K3's facit-plan (del 3, afsnit 4.2):**
- Bedre end min: ca. 380 × 4 workspace-typer = 1.520 TradeStation-kørsler mod 84.400.
- **Men TradeStation kan ikke være facit for MACD-ramte filtre**, for løkke-filen er selv forkert. Facit for gruppe A/C/D laves uden løkke på 3–5 kombinationer pr. filter.
- **Python kan ikke uden videre genskabe:**
  - sessionsskabeloner og helligdage (hvilke bars der findes),
  - `OpenD`/`CloseD` (dagsgrænsen følger sessionen),
  - Data2/Data3 på højere tidsramme (hvornår en bar er "færdig"),
  - startværdien i XAverage og Wilder-udglatning,
  - TradeStations egne udgaver af CCI, PercentR og Pivot,
  - grænsetilfælde, hvor to tal er næsten lige store, fx `>` ved afrunding.
- Derfor: facit pr. workspace-type og **samme bars** eksporteret fra TradeStation. [Antagelse, del 2 §1.4–1.5]

**K1's krav:**
- **Millioner af forsøg:** alle kombinationer og dubletter gemmes, så N_rå og N_eff kan tælles.
- **t ≈ 4,65 og 7,5–30 års data** betyder:
  - Signalerne regnes **én gang over hele historikken**. Walk-forward, pengeskab og placebo regnes i Python uden nye TradeStation-kørsler.
  - Lang historik gør kørsler og CSV'er meget større. Endnu et argument for K3's plan. Hvor meget intradag-historik TradeStation har, er **UKENDT**.
- **Placebo-signaler** laves i Python.

**K3's datamodel:**
- Passer til koden. Fundet om `indlaes_csv.py:72` (sletter hele tabellen) og den manglende marked/tidsramme hænger direkte sammen med mit fund om `FileDelete` (del 2 afsnit 1.7). Det er samme grundfejl tre steder: **et datasæt identificeres kun ved filternummeret**. Det gælder filnavnet, `FileDelete` i EasyLanguage og `delete from` i databasen.
- `Print(File())` kræver et fast navn. Derfor skal oprindelsen (symbol, interval, session og kørsels-ID) skrives **ind i filens indhold**, og databasen skal bruge den som nøgle.

### (b) Fejl og huller

- **K1 §5, Max Bars Back:** "For lav Max Bars Back giver forkerte første bars. Test med 1000 mod 2000." Et for lavt Max Bars Back giver normalt en synlig fejl. Den tavse fejl er **opvarmning** af funktioner, der husker sig selv (del 2 §1.4). Starter beregningen først efter Max Bars Back, starter begge kørsler "kolde", og testen afslører intet. Brug i stedet opvarmningsvinduet (1.382 bars ved længde 600).
- **K1 §5, "Data1 = Data2 håndhæves":** Kun bar-type og interval tjekkes (`generer.py:166-168`), ikke symbol og session. Og 126/174 bruger Data1-priser direkte.
- **K1 §5, "delvis blandet fejl":** Målingen peger på "regnet én gang pr. bar". Delvise fejl er dog mulige i gruppe C.
- **K1 §3.2:** N_eff = 1 for MACD-filtre gælder kun før rettelse, bagefter ca. 36.
- **K3 §2.6:** "380 × 625 = 237.500 backtests" regner med 625 for alle filtre. Det rigtige tal er 128 × 625 + 176 × 25 = 84.400, og 77 filtre har ingen parametre. K3 overvurderer altså med ca. en faktor 2,8.
- **K3 §4.2:** "Python fjerner MACD-problemet" – ja, men så findes intet facit før en løsning uden løkke (se (a)).
- **K3 §1.2 A:** 4.918 er gyldigt. NOTAT'et retter selv 480 til 4.918.

### (c) Uenigheder

1. K3: ét referencedatasæt er facit. Jeg: facit pr. workspace-type, fordi sessioner og Data2/Data3 ikke kan antages ens.
2. K3: TradeStation-facit er nok. Jeg: ikke for gruppe A/C/D. Her skal facit laves uden løkke.
3. K1: test Max Bars Back med 1000 mod 2000. Jeg: test opvarmning, for Max Bars Back fanger ikke den tavse fejl.
4. K1: MACD-filtre må udelukkes. Jeg: genopbyg dem (mønster 2/3/5) – ellers mistes en hel indikatorfamilie.
5. Python som hovedregnemaskine: løst – jeg er enig med K3, med forbeholdene i (a).

## K3 – kritik af udkast2/k1.md og udkast2/k2.md

**Rettet i min k3.md:**
- 4 workspaces er nu med i datamængden. Ét marked giver 25–156 GB.
- `tde_verify` gemmer antal fejl og antal advarsler hver for sig, hver advarselslinje og hele panelteksten.
- `filter_version` har fået K2's funktionsgruppe A–E og en version af klassifikationsreglen.
- Ny tabel `opvarmning` pr. filter × datasæt.
- Nyt `forsoegsregnskab` med N_rå (talt) og N_eff (målt).
- Placebo-signaler har eget nummerområde.
- `bar_nr` er tilføjet til signaltabellen.

### (a) Passer det sammen?

**Ja, efter rettelserne.**

- **Forsøg (K1 afsnit 3):** 1,5–9,5 mio. forsøg skal ikke skrives ind én ad gangen.
  - Hver række i `edge_kombination` (filter × kombination × workspace × retning × horisont) *er* ét forsøg, også de dumpede. 9,5 mio. rækker er ca. 1–2 GB, og det er i orden.
  - **Hvem tæller:** databasen, med `count(*)` pr. forskningsrunde. Tallet skal være lig med det, K1 regner ud fra opsætningen (`n_raa_regnet`). Er de forskellige, er noget tabt, og runden kasseres.
  - N_eff sættes af et selvstændigt målejob (K1's metode). Metode og fingeraftryk af inddata gemmes med tallet. Intet tal skrives i hånden.
- **Opvarmning (K2 afsnit 1.4):** Den hører til filter × datasæt, ikke til filteret alene. Vinduet tælles i bars i den datastrøm, funktionen regner på. 1.382 bars er ca. 5 dage på 5-min-data, men måneder på 120-min-data.
  - Signaler i vinduet slettes ikke. De sorteres fra i visningerne, så K1 kan skifte grænse uden ny backtest.
- **Gruppe A–E (K2 afsnit 2.3):** Kolonne på `filter_version`, sat af maskine. Kontrolstatus K0–K6 ligger i en kontroltabel i produktion (min holdning i U6).
- **Advarsler (K2 afsnit 1.9):** Journalen gemmer `antal_fejl`, `antal_advarsler`, `advarsler[]` og `raa_output`.
  - Om "Pass med advarsel" skal regnes som mistænkt, er Thomas' valg (K2's åbne punkt 1). Databasen gemmer fakta, og en visning bruger hans regel.
- **Pas (K1 afsnit 2):** Alle K1's felter findes: N_rå, N_eff, DSR, PBO, walk-forward, farvemetode, drawdown, omkostninger, pengeskab via fremmednøgle og hukommelsesstatus.

### (b) Fejl og huller

1. **K2's 84.400 kørsler (afsnit 2.4):** Tallet gælder ét workspace.
   - Med 4 workspaces: 84.400 × 4 × 30–60 s = **2.800–5.600 maskintimer**, altså 117–233 døgn på én maskine.
   - For køen er 340.000 jobs ingenting. For UI-robotten er hver kørsel en cyklus med chart, input, vent og hent CSV. Ved 1 % fejl er det ca. 3.400 genstarter. [Antagelse]
   - K2's egen anbefaling (mønster 3 i løkke, mønster 1 kun som kontrol) giver 380 × 4 = 1.520 backtests, altså på linje med mit facit-forslag.
   - **Mønster 1 bør kun bruges i K2's T1-stikprøve (60–80 kørsler).**
2. **Opvarmning kræver bar-nummer:** CSV'en har kun `Starttid`. Omregning fra bars til tid kræver bar-kalenderen pr. datastrøm. Det er billigst at lade generatoren skrive `CurrentBar` med, sammen med K2's forslag om symbol og interval i overskriften (afsnit 1.7).
3. **K1's N_rå (afsnit 3.1)** mangler faktoren *markeder*. Med flere markeder ganges tallet igen.
4. **K1's placebo i hver kørsel (afsnit 5, punkt 6)** skal gå gennem produktionslinjen for at være en ærlig test. Men K1 skriver "gemt adskilt fra produktionsdata". Begge dele kan ikke være fuldt sande. Mit forslag: samme tabeller, eget nummerområde, udelukket fra alle produktionsvisninger.
5. **K2's klassifikation er versionsløs:** Ændres reglen for gruppe A–E, skifter filtre gruppe uden spor. Derfor gemmes `klassifikation_version`.

### (c) Uenigheder

1. K2 (mønster 1 som mulig hovedvej for A/C/D) mod K3 (kun som stikprøve, fordi 117–233 døgn og tusindvis af robotgenstarter ikke kan betale sig).
2. K1 (placebo adskilt fra produktion) mod K3 (samme linje, eget nummerområde). Thomas afgør.
3. K2 (opvarmningsvindue pr. filter) mod K3 (pr. filter × datasæt).
4. K2/K1 (kontrolstatus "adskilt fra produktionsdata") mod K3 (kontroller af rigtige filtre er produktionsdata), uændret U6.

