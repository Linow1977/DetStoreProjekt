---
title: "Konsulentrapport, version 3: udviklingsmotoren i DetStoreProjekt"
subtitle: "Dybde-runden + værktøjskassen – råd til Thomas, ikke beslutninger"
date: "28. september 2026"
---

# Sådan er rapporten bygget op

Version 3 erstatter version 1 og 2. Den består af:

- **Del 1–3 (v2, rettet):** hver konsulents dybdegående del. Den bygger på projektets egen kode og beslutninger.
- **Del 1B–3B (nyt i v3):** hver konsulents *værktøjskasse*, altså de værktøjer, protokoller og teknikker, som professionelle bruger. De er vurderet til netop dette projekt med dommen BRUG NU, SENERE eller NEJ. Thomas' afgørelser fra **Det Runde Bord** er bygget ind.
- **Del 4 (ny):** det samlede overblik, en opdateret Fase 0, enigheder og uenigheder og alle åbne punkter i prioriteret rækkefølge.
- **Bilag:** konsulenternes kritik af hinanden fra runde 2 og 3.

# Aftalen for runde 3

1. **Thomas' opdrag:** "Brug den viden I har. Skaf ekspertviden, hvor I kan. Find værktøjer, protokoller og teknikker inden for hvert felt. Løs opgaven med det I har."
2. **Kilderne:** Mange hjemmesider er blokeret fra cloud-miljøet. Konsulenterne har i stedet læst **kildekode og dokumentation** fra anerkendte open source-projekter på GitHub og PyPI. Det gælder `arch`, `statsmodels`, TA-Lib, talipp, DuckDB, PostgreSQL og en række README-filer. Mange statistiske formler er dermed bekræftet mod rigtig kode, og nogle er også prøvekørt på syntetiske data. Det, der kun er set i søgeresultater, er stadig mærket "[Net, ikke bekræftet]".
3. **Det Runde Bord:** Thomas har **afgjort** tre ting, og de er ikke genåbnet:
   - Et filter, der fejler, er endeligt dødt ("rejected").
   - Der valideres out-of-sample.
   - Der er en inkubationstid før live.

   Konsulenterne har regnet konsekvenserne igennem og bygget kravene ind.
4. **Stadig kun råd.** Ingen kode er leveret, og intet i projektet er ændret. Rollerne er de samme: K1 godkender metoder, og K2 og K3 bygger.

**Den overordnede agents kontrol:** Nøglepåstande er tjekket direkte i koden eller i kilden. Det gælder bl.a. `verify-one.ps1:277`, `indlaes_csv.py:67-72`, `faelles.py:38`, vectorbt's "Commons Clause"-licens, at Airflow ikke kører på Windows, og at StepM/SPA/MCS findes i `arch` 8.0.0. Alle holdt. K1's vigtigste regnestykker er også regnet efter.

# Sammenfatning (højst en halv side)

**1. Hvad fabrikken ærligt kan finde.** Der er 5 års in-sample (2020–2024), og fabrikken tester millioner af varianter. Med de tal kan den kun skelne edges med **årlig Sharpe på ca. 2,3–2,5 eller mere** fra held. Tester man samme regel på **6 markeder**, falder kravet til ca. **1,6**. Pooling over markeder er det stærkeste håndtag.

**2. Afgørelsen om, at et filter er endeligt dødt, har en pris, der skal håndteres.** Bruges 2025 som dom med en 5 %-grænse, bliver **36 % af de ægte, stærke edges slået ihjel for altid**. Efter ca. 20 filtre kan 2025 slet ikke bære en dom. Det bekræfter Det Runde Bord med tal. K1 giver tre regler, Thomas kan vælge imellem (R1–R3). Afgørelsen genåbnes ikke, men dens konsekvens skal styres.

**3. Værktøjskassen.** Konsulenterne har valgt færre og modne værktøjer:
- `arch` (StepM) er hovedtesten for "er det mere end held".
- TA-Lib er uafhængigt facit for indikatorerne.
- Formlerne skal læses med en rigtig parser i stedet for en navneliste.
- Råsignaler gemmes i Parquet-filer (ca. 10 gange mindre end i databasen), og PostgreSQL bruges til journal, status og pas.
- Køen er en enkel tabel i databasen, og der skal ikke være en tung orkestrator.

Tilsammen giver det **én database, én mappe og én fane**.

**4. EdgeFinder har nu en protokol,** som K1 har godkendt med ændringer. Den bygger på Det Runde Bords Lag A, B og C.

**5. Inkubationen kan afgøres som tal.** K1 giver tre gennemregnede regler: en fast test, en sekventiel test og en Bayes-regel. Thomas vælger. Det svarer på Det Runde Bords åbne spørgsmål.

**Fase 0** (del 4.3) er den samlede liste over billige forberedelser, som bør laves, før den fulde kørsel analyseres. Intet i rapporten er et løfte om afkast. Handel indebærer risiko for tab.


# Del 1 – Validering (Konsulent 1: kvantitativ statistiker), version 2

> **Rettet i runde 3 (se også del 1B, `udkast3/k1.md`):**
> - (1) Max Bars Back-testen (1000 mod 2000) udgår som selvstændig test. Den erstattes af to-starts-testen (§5, 1B §3.1).
> - (2) DSR: Kildekoden (pypbo) bruger den *målte* spredning af Sharpe på tværs af forsøg, ikke 1/√T. Tabel 3.3 er derfor en nedre grænse (1B V5). Formlen for expected_max er nu bekræftet.
> - (3) N_eff: En syntetisk måling gav ca. 3–4 effektive tests pr. parameter, ikke ca. 6. Grænserne falder lidt (1B V7).
> - (4) Datalængden er nu kendt fra Det Runde Bord: 5 år in-sample (2020–2024) og 2025 out-of-sample. Scenarierne i §4 er regnet om i 1B §5.1.
> - (5) F4 afgøres fortrinsvis med StepM (Romano-Wolf), ikke en gættet N_eff (1B V3).

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
- **Max Bars Back for de 36 filtre:** *(Rettet i runde 3: den selvstændige test 1000 mod 2000 udgår. Den beviser kun opvarmning og erstattes af to-starts-testen nedenfor.)*
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


# Del 1B – Værktøjer og protokoller til validering (Konsulent 1)

*Tilføjet midt i runden: §5 om Det Runde Bords afgørelser (5 år IS / 2025 OOS, Lag A/B/C, 2025-reglen, inkubationsregler).*

> **Rettet efter kritikrunden (runde 3):**
> - (a) Opvarmningen regnes i bars *for hver datastrøm*. En EMA(600) på 60-minutters bars kun i den normale handelstid (RTH, ca. 7 bars/dag) kræver ca. 2.070 bars, altså ca. 1,2 års forløb før 2020. På 120-minutters bars er det over 2 år. "Fra 2019" er ikke nok for højere tidsrammer.
> - (b) Lag A-minimum pr. celle = (1,28/δ)², hvor δ er den per-handel-Sharpe, der skal til for at bestå IS-grænsen. Den skal ikke tages fra en 5 %-test i hver celle.
> - (c) E2: Dommen træffes på *råt nettoafkast*, fordi det er det, der kan handles. Afkastet efter kontrolgruppen er et ekstra krav (t ≥ 2) og ikke en erstatning.
> - (d) Lag B: StepM bruges med "filteret uden kolonnen" som benchmark, ikke nul.

*Hører sammen med del 1 v2 (`udkast2/k1.md`) og erstatter den ikke. Det er stadig kun råd. Jeg godkender metoder, Konsulent 2 og 3 bygger dem, og Thomas afgør de åbne punkter. Ingen kode leveres, og intet i projektet er ændret.*

**Mærker:**
- **[Kode: pakke version, fil]:** Jeg har selv læst kildekoden, fordi jeg hentede pakken med `pip download`.
- **[Net: URL – åbnet]:** Jeg har selv læst siden.
- **[Net, ikke bekræftet]:** Jeg har kun set søgeresultatet, ikke selve siden.
- **[Regnet]:** Jeg har selv prøvet det af i scratchpad med de installerede pakker. Data er syntetiske, altså lavet med tilfældige tal, ikke Thomas' data.
- **[Antagelse]:** Min egen vurdering.
- **[Projekt]:** Det står i projektets filer.

**Dom-skala:**
- **BRUG NU:** Bør indgå, før den fulde kørsel analyseres.
- **SENERE:** Når leddet findes.
- **NEJ:** Bør ikke bruges.

---

## 0. Kort: de fem vigtigste anbefalinger (BRUG NU)

1. **Romano-Wolf StepM fra `arch` bliver hovedtesten for "er dette mere end held?".** StepM tester alle varianter på én gang og tager selv højde for, at nabovarianter ligner hinanden. Det sker via bootstrap, dvs. at man trækker blokke af data om og om igen. Så behøver vi ikke gætte på det effektive antal forsøg (N_eff) for at sætte grænsen. Prøvekørsel: 500 varianter over 1.250 dage tog 1,4 sekund [Regnet]. Hele fabrikken pr. workspace kan køres på én pc.
2. **Faste kontrolsignaler i hver kørsel.** Placebo betyder signaler flyttet tilfældigt i tid. Indplantet edge betyder syntetiske signaler med en kendt, lille edge. Det er den eneste test, der måler hele kæden, inklusive fejl vi ikke kender. Det kan bygges med numpy og `arch`.
3. **Forhåndsregistrering og forsøgsregister**, før den fulde kørsel analyseres. For hver filterfamilie skrives på forhånd, hvad der skal testes. Det gemmes med dato og et "fingeraftryk" (hash). Det er gratis og det kraftigste værktøj mod skjulte forsøg.
4. **`statsmodels` til FDR-sortering** (Benjamini–Hochberg og lokal FDR). Deflated Sharpe og MinTRL laves som en lille egen funktion, der er kontrolleret mod `pypbo`'s kildekode. `pypbo` bruges ikke direkte, fordi licensen er AGPL og pakken ikke vedligeholdes.
5. **"Blind analyse" af EdgeFinder:** Signalernes retning og filternavne skjules, indtil metoden er låst. Thomas ser kun placebo- og kontrolresultater, til han trykker "lås".

---

## 1. Værktøjer: otte vurderet grundigt

### V1. `statsmodels.stats.multitest` – Holm, BH, BY og lokal FDR
- **Hvad:** En standard-samling af rettelser for mange tests. Benjamini–Hochberg (BH) er beregnet til "uafhængige eller positivt korrelerede" tests. Benjamini–Yekutieli (BY) er til "generelle eller negativt korrelerede" [Kode: statsmodels 0.15.0, stats/multitest.py, linje 121–122 og 329–330]. Pakken har også `local_fdr`, som skønner, hvor stor en andel af alle filtre der er rene nuller.
- **Løser:** Grovsorteringen i RawSignal-Analyse (v2 §3.3 og §7, trin 5) og farvemetode B i plateauet (v2 §8).
- **Valg mellem BH og BY:** Nabovarianter er *positivt* korrelerede, fordi de tænder på de samme bars. Derfor holder BH [Antagelse: positiv afhængighed, "PRDS", er den typiske situation her]. BY er ca. ln(m) + 0,58 gange strengere. Ved m = 84.476 er det ca. **12 gange** strengere [Regnet]. BY bruges kun, hvis man vil være sikker uanset afhængighed.
- **Modenhed og licens:** BSD-3 [Kode: METADATA]. Den er brugt bredt i forskning i mange år.
- **Arbejde:** timer.
- **Risiko:** p-værdierne ind i funktionen skal være gode, dvs. lavet med blok-bootstrap (V2).
- **Dom: BRUG NU.**

### V2. `arch.bootstrap` – blok-bootstrap og optimal bloklængde
- **Hvad:** Bootstrap betyder at trække data om og om igen for at se, hvor meget et resultat svinger. Blok-bootstrap trækker hele stykker af tidsserien, så sammenhængen mellem dage bevares. Pakken har Stationary, Circular og Moving Block. `optimal_block_length` finder bloklængden efter Politis–White-metoden [Kode: arch 8.0.0, bootstrap/base.py:126–175].
- **Løser:** E3 (overlap og afhængighed, v2 §6), metode A og C i plateauet, og konfidensintervallerne.
- **Modenhed og licens:** NCSA (en tilladende licens) [Kode: METADATA]. Pakken er skrevet af Kevin Sheppard og er et kendt værktøj i finansøkonometri.
- **Arbejde:** timer. Afprøvet her [Regnet].
- **Risiko:** Bloklængden skal regnes på *daglige* resultater, ikke på bars.
- **Dom: BRUG NU.**

### V3. `arch.bootstrap.StepM` (Romano-Wolf) og `SPA` (Hansen/White)
- **Hvad:**
  - SPA svarer på spørgsmålet: "Er den *bedste* af alle varianter bedre end ingenting, når vi ved, at vi valgte den bedste?" (White 2000 og Hansen 2005 [Kode: arch 8.0.0, bootstrap/multiple_comparison.py:500–548]).
  - StepM (Romano & Wolf 2005, Econometrica 73(4) [samme fil, linje 355–400]) går videre. Den finder *alle* varianter, der er bedre end nul, og holder sandsynligheden for bare ét falsk fund (FWER) under 5 %.
  - Begge bruger bootstrap på hele tabellen på én gang. Derfor er korrelationen mellem naboer regnet med automatisk.
- **Løser:** F4 (v2 §1). Den erstatter "t ≥ 4,65 med et gættet N_eff" med en *målt* grænse. Det lukker mit største svage punkt i v2.
- **Prøvekørsel [Regnet]:** 1.250 dage (ca. 5 år) og 500 varianter, hvoraf 5 havde en ægte edge (daglig Sharpe 0,12, svarende til ca. 1,9 om året).
  - StepM fandt 4 af de 5 og ingen falske fund, på 1,4 sekund.
  - SPA gav p = 0,002.
  - Tiden vokser nogenlunde lineært med antallet af varianter. 84.476 varianter svarer groft til 4 minutter pr. workspace [Antagelse: skaleret, ikke kørt].
- **Krav til data:** en tabel med T dage × k varianter. Hver varianter får sit daglige resultat (0 på dage uden signal) efter omkostninger. Identiske rækker fjernes først (v2 §7, trin 2). Pakken forventer "tab", så resultaterne gives med minus foran.
- **Risiko:** Variantens resultat skal defineres på forhånd (retning, horisont, udgang). Ellers er det ikke alle forsøg, der er med i tabellen.
- **Dom: BRUG NU** som hovedtest i F4, pr. workspace. DSR (V5) bruges ved siden af som et skalatal i passet.

### V4. `arch.bootstrap.MCS` – Model Confidence Set
- **Hvad:** Finder den gruppe af modeller, som man ikke kan skelne fra "den bedste" (Hansen, Lunde & Nason 2011 [Kode: arch 8.0.0, multiple_comparison.py:71–110]).
- **Løser:** Et senere valg *mellem* strategier i dvale, fx når flere strategier bygger på samme filter.
- **Dom: SENERE.** Det er uden for denne opgave (risiko på tværs af strategier).

### V5. Deflated Sharpe, PSR og MinTRL
- **Hvad:**
  - PSR er sandsynligheden for, at den ægte Sharpe er over en grænse.
  - DSR er PSR, hvor grænsen er "den forventede bedste af N rene tilfældigheder".
  - MinTRL er det mindste antal observationer, der skal til for at nå en bestemt sikkerhed.
- **Formlerne er nu bekræftet i kildekoden** [Kode: pypbo (master), pypbo/pbo.py, `psr`, `dsr`, `expected_max`, `minTRL`]:
  - `expected_max(N) = (1−γ)·Φ⁻¹(1−1/N) + γ·Φ⁻¹(1−e⁻¹/N)`. Det er præcis den formel, jeg brugte i v2 §3.3. En Monte Carlo-kontrol gav 4,14 mod formlens 4,12 ved N = 30.000 [Regnet].
  - `psr`: z = (SR − SR₀)·√(T−1) / √(1 − skæv·SR + SR²·(kurtosis−1)/4).
  - `dsr`: SR₀ = **(den målte spredning af Sharpe på tværs af forsøgene)** × expected_max(N).
- **Rettelse til v2:** Jeg satte spredningen til 1/√T, fordi det er værdien under nul-hypotesen. Koden bruger den *målte* spredning på tværs af alle forsøg. Findes der ægte edges, er den målte spredning større end 1/√T, og så bliver DSR *strengere*. Min tabel i v2 er derfor en nedre grænse for kravet.
- **Om `pypbo`:** Licensen er AGPL-3.0 [Net: https://raw.githubusercontent.com/esvhd/pypbo/master/LICENSE – åbnet]. README'en skriver selv "TODO: Add test cases" og kræver "statsmodels 0.8.0" [Net: https://raw.githubusercontent.com/esvhd/pypbo/master/README.md – åbnet]. Den findes heller ikke på PyPI (`pip download pypbo` fandt ingen version).
- **Dom:** Formlerne: **BRUG NU**. De er ca. 20 linjer, som Konsulent 2/3 skriver selv og kontrollerer mod `pypbo`'s tal. Selve pakken som afhængighed: **NEJ**, fordi den er uvedligeholdt, uden tests og har AGPL-licens.

### V6. CSCV/PBO (sandsynlighed for overfitting ved udvælgelsen)
- **Hvad:** Data deles i S stykker. For hver måde at dele dem i to lige store halvdele måles, hvor "vinderen" fra den ene halvdel ender i den anden [Kode: pypbo/pbo.py, `pbo` og `pbo_core_calc`]. S = 16 giver C(16,8) = 12.870 delinger.
- **Vigtigt forbehold fra koden selv:** "Not suitable for time series with strong auto-correlation, especially when S is large", og "all N strategy configs [may] have high but similar Sharpe … PBO may appear high" [samme fil, docstring linje ca. 80–95]. Det betyder: den passer dårligt til stærkt sammenhængende tidsserier, og PBO kan se høj ud, selv når alle varianter er gode.
- **Løser:** Kontrol af hele udvælgelsesprocessen i EdgeCruncher (v2 §4.6).
- **Dom: SENERE.** Når EdgeCruncher vælger mellem varianter. Bygges selv efter samme opskrift som V5. Grænsen kalibreres med placebo, som i v2.

### V7. Måling af N_eff med egenværdier (Nyholt, Li-Ji) og klynger
- **Hvad:** Man tager korrelationsmatricen for varianternes daglige resultater og dens egenværdier λ. Egenværdier siger, hvor mange "retninger" data reelt varierer i.
  - Nyholt: M_eff = 1 + (k−1)·(1 − Var(λ)/k).
  - Li-Ji: M_eff = Σ [1(|λ|≥1) + (|λ| − ⌊|λ|⌋)].
  - Begge er bekræftet i kildekoden til R-pakken `poolr` [Net: https://raw.githubusercontent.com/ozancinar/poolR/master/R/meff.r – åbnet; licens GPL ≥ 2]. Artiklen er Li & Ji (2005), Heredity [Net, ikke bekræftet].
- **Prøvekørsel på syntetiske priser [Regnet]:** Filteret `Range > Average(TrueRange, 5·N1)` med N1 = 1–25:
  - Nabokorrelation 0,97, og korrelationen mellem N1 = 1 og N1 = 25 er 0,81.
  - **Nyholt 3,9 og Li-Ji 3,0 effektive tests** ud af 25.
  - Mit skøn i v2 var ca. 6 pr. parameter, så det var forsigtigt sat. N_eff for fabrikken er måske 2–3 gange lavere end mit midtscenarie. Grænsen falder derfor lidt, men kun "logaritmisk": fra N_eff = 30.000 til 10.000 falder Bonferroni-t fra 4,65 til ca. 4,42.
- **Grænser:** Egenværdier kan kun regnes pr. filter (højst 625 × 625). Matricen for alle 84.476 varianter ville fylde ca. 57 GB. Mellem filtre bruges klynger: `scipy` hierarkisk klyngedeling på én repræsentant pr. filter (380 × 380). Egenværdi-metoderne kan være både for milde og for strenge, afhængigt af situationen [Net, ikke bekræftet: søgeuddrag om Li-Ji]. Derfor bruges de til at *beskrive* N_eff, mens StepM (V3) *afgør*.
- **Dom: BRUG NU** til passet og DSR. Den er ikke dommer.

### V8. Generator til kontrolsignaler (placebo og indplantet edge)
- **Hvad:**
  - **Placebo:** Filterets rigtige signalrække flyttes et tilfældigt antal handelsdage frem, og det, der falder over kanten, sættes ind forrest. Mønstret (hyppighed, klumper, længder) bevares. Kun forbindelsen til prisen brydes.
  - **Indplantet edge:** En syntetisk prisserie laves ved stationary bootstrap af de rigtige afkast (V2). På de tidspunkter, hvor et syntetisk signal tænder, lægges en lille kendt edge ind, fx per-handel-Sharpe 0,05 og 0,1.
- **Løser:** E7/E8 (v2 §6), kalibrering af PL-niveauerne og PBO (v2 §8, §4.6) og en test af hele kæden.
- **Modenhed:** Det er ikke en pakke, men en teknik bygget af numpy og `arch`. Idéen er standard inden for permutationstest [Antagelse].
- **Arbejde:** 1–2 dage for Konsulent 2/3.
- **Dom: BRUG NU.** Det er det værktøj, der giver mest sikkerhed pr. times arbejde.

**Fravalgt uden grundig vurdering:** Kommercielle værktøjer (fx MLFinLab) har lukket kode og licenser, jeg ikke har kunnet læse. Det gør det umuligt at bevise tællingen af forsøg (F3). Dom: **NEJ**, indtil nogen har undersøgt dem [Antagelse].

---

## 2. Protokoller for forskningsdisciplin, så Thomas kan følge dem uden at kode

### P1. Forhåndsregistrering ("hypotesekort")
- **Hvad:** Før resultaterne ses, udfyldes et kort pr. filterfamilie. Det indeholder: event-definition, hvornår handlen starter, retning (eller "begge, tæller dobbelt"), horisonter, parametergitter (Fra/Til/Step), workspaces, omkostningsmodel og hvilken farvemetode plateauet bruger.
- **I praksis:** Konsulent 3's skærm viser kortet som felter, der udfyldes. Når Thomas trykker "Registrér", gemmes det med dato og hash. Et kort kan ikke ændres, kun erstattes af en ny version, og det tæller som et nyt forsøg.
- **Hvorfor:** Det lukker "forking paths", altså at man vælger metoden efter at have set resultatet (v2 §5). Kilde til princippet: MacCoun & Perlmutter, "Blind analysis: Hide results to seek the truth", Nature 526 (2015) [Net, ikke bekræftet].

### P2. Forsøgsregister
- Hver kørsel skriver automatisk én linje pr. variant i Konsulent 3's `fabrik.forsoeg`. Det gælder også dem, der dumper, og placebo. Tallet i passet *tælles* af databasen og skrives aldrig i hånden.
- Thomas' eneste opgave er at lade være med at slette.

### P3. Låst pengeskab
- Datoerne låses i `fabrik.datadeling`, før analysen. Prisdata efter pengeskabets startdato må kun læses af rollen `fabrik_dommer` (Konsulent 3's design).
- Thomas trykker "Åbn pengeskab" én gang pr. strategi. Skærmen minder om, at resultatet er endeligt.

### P4. Blind analyse
- **Hvad:** Mens EdgeFinder-metoden bliver færdig, vises kun (a) placebo- og indplantet-resultater og (b) resultater, hvor filternavn og retning er skjult bag en kode.
- Først når metoden er låst (P1 er udfyldt, og E7/E8 er bestået), trykker Thomas "Lås metode". Så vises de rigtige navne.
- **Hvorfor:** Man kan ikke "forelske sig" i et filter, man ikke kan se.
- **Pris:** næsten ingen, det er et skærmvalg.

### P5. Kontrolsignaler i hver kørsel
- Hver kørsel indeholder fx 200 placebo-signaler og 20 indplantede, lavet med V8. Resultaterne sammenlignes automatisk med forventningen: falsk-positiv-rate inden for 3,6–6,4 % ved 1.000 tests og 5 %-grænse (v2 §6, E7), og mindst 80 % af de indplantede fundet.
- **Stopregel:** Uden for intervallet stoppes kørslen og markeres rød. Så gælder "ret, ryd op og kør forfra" [Projekt: VIDENSLOG.md 2026-09-24].
- Placebo-signalerne har deres eget nummerområde. Deres resultater gemmes sammen med kørslen, fordi de er beviset for kørslens kvalitet (uenighed U3 med Konsulent 3 – Thomas afgør).

### P6. To-nøgle-reglen
- Den, der bygger eller vælger (EdgeFinder/EdgeCruncher), kan ikke sætte "bestået". Kun rollen `fabrik_dommer` kan, efter faste regler fra `regelsaet`.
- Det er projektets egen regel om, at roller ikke må slås sammen [Rapport/opgaven], lavet om til databaseroller.

---

## 3. Huller fra v2, der nu er lukket

### 3.1 Max Bars Back-testen (1000 mod 2000) eller opvarmningstesten?
- **Konsulent 2's indvending** er rigtig: begge kørsler starter "kolde". Funktionerne begynder at regne ved første bar efter Max Bars Back.
- **Min konklusion:** Sammenligner man signalerne på fælles bars *langt nok* efter begge starter, *er* 1000 mod 2000 i praksis en to-starts-test. Den beviser opvarmningen, ikke Max Bars Back.
- Om Max Bars Back er for lille, siger den intet. Det forventer jeg, at TradeStation selv melder som fejl ved kørsel [Antagelse: kan ikke tjekkes, tradestation.com er blokeret].
- **Beslutning om metode (min rolle):** Max Bars Back-testen som selvstændig test **udgår**. Den erstattes af **to-starts-testen** (v2 §5): kør med Max Bars Back = 1000 og med 1000 + W, hvor W er opvarmningsvinduet fra 0,1 %-reglen. Kravet er 100 % ens signaler fra bar 1000 + 2W. De 36 filtre med ukendt behov får samme test. Uenighed U2 er løst til Konsulent 2's fordel.

### 3.2 Faste kolonner i passet (til Konsulent 3)
Alt her skal være *faste kolonner*, fordi man sorterer og filtrerer på det. Resten kan ligge i `f_resultater`.

| Kolonne | Type | F-krav | Note |
|---|---|---|---|
| `praeregistrering_id` | int | P1 | Kortet, strategien er testet efter |
| `workspace_id`, `marked`, `n1`, `n2` | – | ID | |
| `retning`, `horisont`, `event_definition`, `indgang_regel` | text | E1 | |
| `opvarmning_bars` | int | F1 | Fra 0,1 %-reglen |
| `f1_kontrolstatus` | enum: ikke_kontrolleret / bestaaet / fejlet | F1 | Konsulent 2's K0–K6 |
| `hukommelsesfejl_status` | enum: maalt_ramt / maalt_ok / ikke_maalt | F1 | |
| `n_unikke_raekker_filter` | int | F3 | Efter sammenlægning af ens rækker |
| `n_raa`, `n_eff`, `n_eff_metode` | bigint, numeric, text | F3 | Metode: Li-Ji / Nyholt / klynge |
| `t_vaerdi` | numeric | F4 | Blok-bootstrap, efter omkostninger |
| `stepm_bestaaet`, `stepm_antal_modeller` | bool, int | F4 | V3 |
| `dsr`, `sr_spredning_forsoeg` | numeric | F4 | V5 (den målte spredning bruges) |
| `plateau_niveau`, `plateau_metode` | int, text (A/B/C) | F5 | |
| `wf_t`, `wf_antal_kandidater` | numeric, int | F6 | Erstatter `walkforward_andel_pos` |
| `middel_dobbelt_omk` | numeric | F7 | Skal være > 0 |
| `f8_antal_aar`, `f8_negative_aar`, `f8_stoerste_aar_andel` | int, int, numeric | F8 | |
| `antal_handler`, `antal_handler_eff`, `sr_pr_handel` | int, numeric, numeric | F10 | "eff" efter overlap |
| `pbo` | numeric | §4.6 | Når EdgeCruncher findes |
| `skaevhed`, `kurtosis`, `max_drawdown` | numeric | DSR | |
| `placebo_rate_koersel`, `indplantet_fundet_andel` | numeric | P5 | Kørslens kontrolresultat |

Konsulent 3 mangler desuden en tabel **`genvaekning`** med kolonnerne: `strategi_uid`, `dato`, `nye_handler`, `welch_t`, `bayes_p_over_omk`, `regime_ok`, `cusum_brud` og `beslutning` (v2 §11). `regelsaet` skal have talgrænserne som felter: `t_graense`, `dsr_graense`, `stepm_alpha`, `fdr_q`, `pbo_graense`, `placebo_max`, `indplantet_min`, `pengeskab_andel` og `genvaek_bayes_graense`.

---

## 4. Hvordan man kalibrerer grænser uden lang historik

Den hårde sandhed fra v2 §4.2 gælder stadig: **Det antal år, der kræves, afhænger kun af edgens årlige Sharpe og t-grænsen.** Flere handler pr. dag hjælper ikke. Det er BEVIST algebra. Professionelle kommer rundt om det på disse måder:

1. **Kalibrering med syntetiske data (V8):** Grænserne (t, PL-niveauer, PBO) sættes, så placebo-raten og andelen af fundne indplantede edges rammer målene. Det kræver ingen ekstra historik, kun regnetid. **BRUG NU.**
2. **Pooling over markeder:** Samme uændrede regel testes på M markeder, og resultaterne lægges sammen, fx som et gennemsnit af daglige resultater på tværs af markeder. Er markederne ukorrelerede, falder det antal år, der kræves, med faktoren M. Ved korrelation ρ er gevinsten M/(1 + (M−1)ρ) [Antagelse: standardformel for gennemsnit af korrelerede størrelser]. Eksempel: 6 markeder med ρ = 0,3 giver 6/2,5 = **2,4 gange** mindre krav til år. 7,5 år bliver ca. 3,1 år [Regnet]. **BRUG NU**, hvis der er data for flere markeder (åbent punkt 1).
3. **Shrinkage og empirisk Bayes:** Ingen edge tages for pålydende. `local_fdr` (V1) skønner ud fra *alle* varianters t-værdier, hvor stor en andel der er rene nuller, og giver hver variant en sandsynlighed for at være ægte. Den forventede edge, der skrives i passet, er den observerede × sandsynligheden for at være ægte × en "haircut". Det gør også genvæknings-reglen i v2 §11 (Bayes) konkret. **BRUG NU** (statsmodels), men tallene er grove, indtil N_eff er målt.
4. **Purged og embargo-krydsvalidering:** Når handler overlapper, fjernes de observationer, der deler tid med testperioden ("purge"), og der lægges et lille mellemrum ("embargo") mellem trænings- og testperioden. Metoden er beskrevet af López de Prado [Antagelse: velkendt metode, kilde ikke åbnet]. **SENERE** (EdgeCruncher og walk-forward).
5. **Færre, bedre forsøg:** En økonomisk begrundelse pr. filterfamilie, skrevet i P1, fx "volatilitetsudbrud efterfølges af fortsættelse". Retning og horisont vælges ud fra begrundelsen. Det halverer eller femdobler ikke kravet, fordi gevinsten er logaritmisk, men det fjerner de *skjulte* forsøg. **BRUG NU.**
6. **Hvad der IKKE hjælper:** kortere bars, flere signaler pr. dag og længere parametergitre. De øger enten antallet af overlappende observationer eller antallet af forsøg, ikke antallet af uafhængige år.

---

## 5. Det Runde Bord: konsekvenser for valideringen

*Kilde: [Projekt: Det Runde Bord-sammenfatning] (`runde_bord.txt`). Thomas har **afgjort** tre ting, og dem genåbner jeg ikke:*
- *Et filter, der fejler, er endeligt dødt ("rejected").*
- *Der valideres out-of-sample.*
- *Der er en inkubationstid, før strategien går live.*

*Nedenfor viser jeg, hvad det betyder i tal. Tallene er regnet i `k1_regn3.py` [Regnet].*

### 5.1 Hvad kan fabrikken ærligt finde med 5 år in-sample og 1 år out-of-sample?
**In-sample (2020–2024, 5 år).** Hvilken ægte årlig Sharpe S skal ét enkelt signal have for at blive fundet med 80 % styrke? Formlen er S = (t + 0,84)/√5:

| Grænse t | 2,0 (ét forsøg) | 3,65 (N=380) | 4,42 (N_eff≈10.000) | 4,65 (N_eff≈30.000) | 5,77 (DSR, N_eff≈30.000) |
|---|---|---|---|---|---|
| Mindste S, der kan findes | 1,27 | 2,01 | **2,35** | **2,46** | 2,96 |

**Konklusion (BEVIST som regnestykke, givet grænsen):** Med 5 år og ét marked pr. test kan fabrikken ærligt kun finde enkeltsignaler med årlig Sharpe på ca. **2,3–2,5 eller mere** efter omkostninger. Svagere, men ægte edges er ikke til at skelne fra held. Pooling over markeder med samme regel (§4.2) sænker kravet med faktoren √(M/(1+(M−1)ρ)). Ved 6 markeder og ρ = 0,3 er det √2,4 ≈ 1,55, så kravet falder fra 2,46 til ca. 1,6 [Regnet].

**Out-of-sample (2025, 1 år).** Sandsynligheden for at bestå med en grænse c for t-værdien i 2025 er Φ(S − c):

| Grænse c i 2025 | Ren held (S=0) | S=1 | S=1,5 | S=2 | S=2,5 | S=3 |
|---|---|---|---|---|---|---|
| t ≥ 0 (kun rigtigt fortegn) | 50 % | 84 % | 93 % | 98 % | 99 % | 100 % |
| t ≥ 0,5 | 31 % | 69 % | 84 % | 93 % | 98 % | 99 % |
| t ≥ 1,0 | 16 % | 50 % | 69 % | 84 % | 93 % | 98 % |
| t ≥ 1,645 (5 % ensidet) | 5 % | 26 % | 44 % | 64 % | 80 % | 91 % |

**Konklusion:** Ét år kan ikke både beskytte mod held *og* lade ægte edges passere. Hvis "rejected" er endeligt, betyder en 5 %-grænse i 2025, at **36 % af de ægte S = 2-edges bliver slået ihjel for altid**.

### 5.2 Hvordan Lag A/B/C passer med F1–F10

| Runde Bord | Min v2-ramme | Hvad der skal passe sammen |
|---|---|---|
| Lag A (fast, låst liste af opdelinger: år, volatilitet, tid på dagen, varighed) | P1 (forhåndsregistrering), F8 (stabilitet) og F5 (plateau). Plateau går på tværs af *parametre*, Lag A på tværs af *forhold*. | Lag A er en **stabilitetstest, ikke en søgning**. Den koster derfor ingen straf for mange forsøg, *hvis* kriteriet er skrevet før. Men se 5.3: kriteriet må ikke være "alle celler positive". |
| Lag B (begrænset søgning, antal logget) | F3 (N_rå, N_eff) og P2 (forsøgsregister) | Hver kolonne og hver grænse, der prøves i Lag B, er et forsøg for *det filter*. Fundet skal bestå StepM (V3) *inden for filteret* på in-sample. Almgrens krav (resultat efter omkostninger skal stige nok til at betale for de signaler, der mistes) fastsættes som tal i `regelsaet` på forhånd. |
| Lag C (forbudt) | F9 og P6 | Håndhæves teknisk: `rejected` kan ikke læses af analyseroller. |
| Fire datalag (IS / OOS 2025 / embargo / inkubation) | F2 og F9 (mit "pengeskab") | **Embargo er pengeskabet** (F9: åbnes én gang). 2025 er et valideringslag med tæller (5.4). Inkubation er et nyt lag (5.5). |
| Døde filtre slettes aldrig og er nævneren | F3 | Det er præcis mit krav. Rejected-filtrene tæller med i N_rå og N_eff. |
| Ændres Lag A, køres alt om | P1 | Enig. Den nye version tæller som en ny forsøgsrunde (N lægges sammen). |

### 5.3 Lag A: en statistisk regel, der ikke dræber ægte edges
Fordi "rejected" er endeligt, er den dyreste fejl en *ægte edge, der dør i Lag A* (Kaufmans bekymring). Regnestykket for kravet "effekten skal være positiv i alle c celler", hvor hver celle har 1/c af de 5 år [Regnet]:

| Ægte S | 3 celler | 5 celler (fx år) | 10 celler | 20 celler |
|---|---|---|---|---|
| 1,5 | 92 % | 71 % | 21 % | 1 % |
| 2,0 | 99 % | 89 % | 44 % | 3 % |
| 2,5 | 100 % | 97 % | 67 % | 11 % |

Tabellen viser sandsynligheden for, at en ægte edge overlever. "Alle celler positive" med 10 celler slår altså over halvdelen af de ægte S = 2-edges ihjel.

**Forslag til regel for Lag A (tre mulige kriterier, Thomas vælger):**
1. **Ingen celle signifikant negativ:** ensidet 5 % med Holm på tværs af cellerne i hver opdeling.
2. **"Uden den bedste celle"-test:** Effekten skal være mindst 50 % af den samlede og stadig positiv, når den bedste celle (fx 2020) tages ud. Det tester direkte Bordets bekymring "kommer det kun fra én periode?".
3. **Heterogenitetstest:** en test for, om cellernes effekter er forskellige (Cochran's Q eller interaktion i regression). Afvis kun ved p < 0,01.

**Mindste antal signaler pr. celle:** Skal en ægte per-handel-Sharpe δ vise positivt fortegn i cellen med 90 % sandsynlighed, kræves n ≥ (1,28/δ)² [Regnet]:

| δ | 0,03 | 0,05 | 0,1 | 0,15 |
|---|---|---|---|---|
| Signaler pr. celle | 1.825 | 657 | 164 | 73 |

Celler med færre signaler vurderes ikke: de er grå, ikke røde.

**Kalibrering:** Lag A-listen og kriteriet køres på indplantede edges og placebo (V8), *før* den låses. Målene er, at højst fx 10 % af de indplantede edges på den valgte S bliver slået ihjel, og at placebo bestået under fx 50 %. Lag A er ikke hovedfilteret. Det er StepM.

### 5.4 Regel for "2025 slides op"
**Problemet:** Hver gang et filter vælges eller dømmes på 2025, er 2025 et forsøg mere. Efter k filtre kræver en ærlig 5 %-grænse t ≥ Φ⁻¹(1 − 0,05/k):

| k filtre, der har rørt 2025 | 1 | 5 | 10 | **20** | 50 | 100 | 500 |
|---|---|---|---|---|---|---|---|
| t-grænse | 1,64 | 2,33 | 2,58 | **2,81** | 3,09 | 3,29 | 3,72 |
| Ægte S, der kræves for 80 % styrke på 1 år | 2,49 | 3,17 | 3,42 | **3,65** | 3,93 | 4,13 | 4,56 |

Det bekræfter Bordets "ca. 20" med tal: allerede ved 20 filtre kan 2025 kun bekræfte edges med S ≈ 3,7. Det er urealistisk.

**Tre konkrete regler (Thomas vælger, jeg afgør ikke):**
- **R1 – Tællende grænse:** 2025-grænsen er t ≥ Φ⁻¹(1 − 0,05/k), hvor k er tælleren i journalen. Den er ærlig, men 2025 bliver hurtigt ubrugelig.
- **R2 – 2025 som kasseringsport med fast, lav grænse** (fx t₂₀₂₅ ≥ 0,5). Den ændrer sig ikke med k, fordi 2025 kun må *afvise* og aldrig bruges til at *vælge den bedste*. Ren held består i 31 % af tilfældene, og en ægte S = 2 består i 93 %. Beviset kommer fra IS (StepM) + embargo + inkubation. *Det er López de Prados linje med tal.*
- **R3 – Online FDR ("alpha-investing"):** Hver dom på 2025 bruger en del af et fast α-budget, og fund giver budget tilbage. Metoden er fleksibel, men sværere at forklare [Antagelse: kendt metodefamilie (Foster & Stine; LORD), kilde ikke åbnet].

Uanset regel: tælleren k gemmes i journalen, og 2025-resultatet må aldrig bruges til at vælge parametre.

### 5.5 Inkubation: tre gennemregnede beslutningsregler (Thomas vælger)

**Fælles for alle tre** (det gælder uanset valg):
- **Frekvenstjek:** Antallet af handler skal ligge i Poisson-intervallet for backtestens hyppighed. Forventes 60 handler, er 95 %-intervallet 45–75 [Regnet]. Ligger antallet udenfor, er der en fejl i koden eller dataene, ikke en markedsændring. → Status `failed` (teknisk), ikke `rejected`.
- **Slippage-tjek:** Den gennemsnitlige faktiske slippage (signalpris minus fillpris, samme definition som i backtesten [Projekt: Det Runde Bord-sammenfatning]) må højst være den antagne + 2 standardfejl.
- **Ur-nulstilling** ved enhver ændring (Bordets krav).
- **Den hårde sandhed:** Hvor lang tid det tager at afgøre, afhænger igen kun af S. Antallet af handler pr. uge betyder intet [Regnet]. Minimum = max(tidskrav, antal handler).

**I1 – Fast stikprøve og t-test.** Når n handler er nået, testes ensidet ved α.

| Ægte S | 1,0 | 1,25 | 1,5 | 2,0 | 2,5 |
|---|---|---|---|---|---|
| År ved α = 5 %, 80 % styrke | 6,2 | 4,0 | 2,8 | 1,6 | 1,0 |
| År ved α = 20 %, 80 % styrke | 2,8 | 1,8 | 1,3 | 0,7 | 0,45 |

Ellers: under grænsen → `rejected (inkubation)`. Simpel, men lang.

**I2 – Sekventiel test (SPRT, Wald).** Efter hver handel lægges log-sandsynlighedsforholdet (log-likelihood ratio) mellem "edge = δ" og "edge = 0" til. δ er backtestens edge efter haircut. Grænserne er A = ln(0,8/0,05) = 2,77 (→ live) og B = ln(0,2/0,95) = −1,56 (→ rejected). Forventet varighed i år [Regnet: E[N] = 2((1−β)A + βB)/S²]:

| Ægte S | 1,0 | 1,25 | 1,5 | 2,0 | 2,5 | 3,0 |
|---|---|---|---|---|---|---|
| Hvis edgen er ægte (til "live") | 3,8 | 2,4 | 1,7 | 0,95 | 0,6 | 0,4 |
| Hvis edgen er død (til "rejected") | 2,7 | 1,7 | 1,2 | 0,67 | 0,43 | 0,3 |

Den er ca. 40 % hurtigere end I1 i gennemsnit og stopper af sig selv. Den skal have et **loft** (fx 2 år). Når loftet nås, kræves det, at Thomas på forhånd har skrevet "live", "rejected" eller "forlæng".

**I3 – Bayes-regel.** Start med backtestens edge (efter haircut) som forventning med usikkerhed τ. Opdatér for hver handel. Gå live, hvis P(edge > 0) ≥ 90 % efter minimumstiden. Rejected, hvis P(edge > 0) < 50 %. Ellers forlæng. Tallene afhænger stærkt af τ [Regnet, per-handel-enheder, 250 handler/år]:

| Prior (m₀, τ) | Efter | Faktisk edge = som backtest | = 0 | = −0,05 |
|---|---|---|---|---|
| Optimistisk (0,079; 0,05) | ½ år | 96 % | 92 % | 87 % |
| Optimistisk | 1 år | 98 % | 89 % | 77 % |
| Skeptisk (0,04; 0,06) | ½ år | 85 % | 71 % | 60 % |
| Skeptisk | 1 år | 91 % | 69 % | 48 % |

Tallene er P(edge > 0). **Advarsel:** Med en optimistisk prior går en død strategi live. Valget af prior er selve beslutningen. Det skal skrives ned før inkubationen og helst kalibreres på V8-data.

**Min faglige vurdering (ikke en afgørelse):** I2 med loft passer bedst til "systemet åbner for live", fordi reglen er ren mekanik. Den er i øvrigt kun realistisk for strategier med S ≳ 2. Svagere strategier kan ikke afgøres i inkubation på under ca. 2 år.

### 5.6 Uenighederne på bordet: faglig vurdering (står åbne)
- **Lag A bred eller smal (Kaufman mod López de Prado/Destroyer):** Begge har ret om hver sin fejltype. Tabel 5.3 viser, at Kaufmans risiko er reel og kan måles: hvor mange indplantede edges dræber listen? Destroyers risiko kan også måles: hvor mange placebo slipper igennem? **Uenigheden kan omsættes til to tal med V8, før listen låses.** Hvilken fejl der er dyrest, er et valg for Thomas.
- **2025 som dom eller mellemtjek:** Regnestykket i 5.4 støtter fagligt López de Prado: efter ca. 20 filtre *kan* 2025 ikke bære en dom. Kaufmans indvending om hastighed er også rigtig. Med I2 tager en S = 2-strategi ca. 1 år, ikke 3 måneder. En mulig middelvej er R2 + I2, hvor mange kandidater inkuberes parallelt, fordi de ikke konkurrerer om data. Det kræver dog infrastruktur (Konsulent 3). Uenigheden står åben.

---

## 6. Nye åbne punkter til Thomas

1. Skal **StepM (V3)** være den afgørende test i F4, med DSR som tal ved siden af? Eller omvendt?
2. **BH eller BY** i grovsorteringen? BH forudsætter positiv afhængighed. BY er ca. 12 gange strengere.
3. **Blind analyse (P4):** Vil Thomas acceptere ikke at se filternavne, før metoden er låst?
4. **Pooling (§4.2):** Findes der data for flere markeder, der kan testes med samme regel?
5. **2025-regel:** R1, R2 eller R3 (§5.4).
6. **Inkubationsregel:** I1, I2 eller I3, loft, og hvad der sker ved loftet (§5.5).
7. **Lag A-kriterium:** 1, 2 eller 3 (§5.3), mindste antal signaler pr. celle og den acceptable "false kill"-rate for indplantede edges.
8. **Antal markeder** til pooling (§4.2, §5.1). Datalængden er nu afklaret: 5 år IS + 2025.

---

## 7. Kilder, jeg selv har åbnet eller læst

- [Kode: arch 8.0.0 (hentet med pip), `arch/bootstrap/multiple_comparison.py` (SPA, StepM, MCS, RealityCheck), `arch/bootstrap/base.py` (`optimal_block_length`), METADATA (licens NCSA)]. Afprøvet [Regnet].
- [Kode: statsmodels 0.15.0 (hentet med pip), `statsmodels/stats/multitest.py`, METADATA (BSD-3)]. Afprøvet [Regnet].
- [Net: https://raw.githubusercontent.com/esvhd/pypbo/master/pypbo/pbo.py – åbnet] (PSR, DSR, expected_max, MinTRL, minBTL, PBO/CSCV).
- [Net: https://raw.githubusercontent.com/esvhd/pypbo/master/README.md – åbnet], [Net: …/LICENSE – åbnet] (AGPL-3.0).
- [Net: https://raw.githubusercontent.com/ozancinar/poolR/master/R/meff.r – åbnet] (Nyholt, Li-Ji, Gao, Galwey), [Net: …/DESCRIPTION – åbnet] (GPL ≥ 2, version 1.3-0).
- Ikke bekræftet (kun søgeuddrag): Li & Ji (2005), Heredity; MacCoun & Perlmutter (2015), Nature 526:187; Romano & Wolf (2005), Econometrica 73(4) (kun som henvisning i arch-koden); Hansen, Lunde & Nason (2011) (samme).
- Regnestykker og prøvekørsler: scratchpad `k1_regn.py` og kørsler i denne session. Alle data er syntetiske.

**Hvad mangler:** Ingen af værktøjerne er prøvet på Thomas' rigtige data. StepM's regnetid for 84.476 varianter er skaleret, ikke kørt. Li-Ji-målingen er lavet på syntetiske priser og på ét filter.


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

**Rettet i runde 3:** Efter kritikrunden er K1 enig i vej a. Der er ikke længere uenighed om dette punkt. Alle er enige om, at MACD-filtrene **ikke** må godkendes uden kontrol. Thomas afgør stadig.

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


# Del 2B – Værktøjer, teknikker og EdgeFinder-protokol (Konsulent 2, runde 3)

*Tillæg til del 2 (v2). Kun råd. Intet i projektet er ændret, og der leveres ingen kode.*

**Mærker:**
- **[Kode: pakke version, fil]** = kildekode, jeg selv har hentet og læst.
- **[Net: URL – åbnet]** = en side, jeg selv har læst.
- **[Net, ikke bekræftet]** = kun set som uddrag fra en søgemaskine.
- **[Projekt: fil]** = står i projektets egne filer.
- **[Regnet]** = jeg har selv regnet det i scratchpad.
- **[Antagelse]** = min egen vurdering.

**Domme:**
- **BRUG NU** = tag det i brug i den næste fase.
- **SENERE** = nyttigt, men ikke før noget andet er på plads.
- **NEJ** = passer ikke til projektet.

**Rettelse i v2:** I `udkast2/k2.md` §4 stod der, at "K1 accepterer b og c". Det er rettet. K1 er enig i vej a (byg MACD-filtrene om), og uenigheden er lukket.

---

## 0. Kort: de fem vigtigste anbefalinger (BRUG NU)

1. **Facit for indikatorerne skal have tre parter.** De tre er (i) TradeStations egen funktion, kørt uden løkke, (ii) en lille Python-udgave skrevet ud fra TradeStations funktionskode, som kan læses i TDE, og (iii) TA-Lib som uafhængig tredjepart. Afvigelser i startværdien håndteres med et opvarmningsvindue udregnet pr. filter. (Afsnit 1)
2. **Byg en rigtig formel-parser med lark i stedet for navnelisten** i `formel.py:22-25`. Parseren sorterer automatisk alle 380 formler i gruppe A–E fra del 2 §2.3. Det er gratis at køre og fjerner den tavse fejl, hvor funktioner mangler på listen. (Afsnit 2.5)
3. **Golden master med kontrolsum (hash) på hver CSV og på hver Python-signalfil.** Kombiner det med differential testing: TradeStation og Python skal give samme signaler. Det er kernen i F1. (Afsnit 2.1–2.2)
4. **Plant 10 kendte fejl og se, om kontrollen fanger dem** (mutationstest på den måde, projektet arbejder). En kontrol, der aldrig er set fange en fejl, er ikke bevist. (Afsnit 2.4)
5. **Filter-identitet som fingeraftryk af den normaliserede formel** (via parseren) + parametermængde + instrument + tidsramme. Det håndhæves i databasen, generatoren og EdgeFinder, så et "rejected" filter ikke kan komme tilbage (afsnit 4.6). Samtidig gælder: **ingen Lag A-dom før F1/K0–K6 er bestået**, for med Thomas' regel er en dom på forkerte tal uoprettelig (afsnit 4.0).

Også vigtigt: EdgeFinder regnes i egen, enkel Python-kode med `arch` til blok-bootstrap (afsnit 3.2).

---

## 1. Uafhængige referenceberegninger af indikatorer

### 1.1 Hvad jeg har læst i TA-Lib
TA-Lib er et gammelt og meget brugt C-bibliotek til tekniske indikatorer. Licensen er BSD-lignende: "Redistribution and use … are permitted" [Kode: TA-Lib main, `src/ta_func/ta_EMA.c`, linje 1–5]. Den findes også som Python-pakke, TA-Lib 0.8.1, der er markeret stabil [Net: https://pypi.org/pypi/TA-Lib/json – åbnet].

| Indikator | Sådan starter TA-Lib (læst i koden) | Kilde |
|---|---|---|
| **EMA** | Vægt k = 2/(L+1). Opdatering: ny = forrige + k·(pris − forrige). **Startværdien er gennemsnittet af de første L priser.** Længde 1 er en ren kopi. | [Kode: TA-Lib, `ta_EMA.c`] |
| **MACD** | To EMA'er, som hver starter med gennemsnittet af deres første priser. "The fast and slow seed windows end on the same bar." Signallinjen starter på samme måde. Regnerækkefølgen kaldes selv en "bit-exactness contract". | [Kode: TA-Lib, `ta_MACD.c` ca. linje 210–235] |
| **RSI** | Wilder-udglatning. Gennemsnitlig gevinst og tab: ny = (gammel·(L−1) + dagens)/L. Starter med et simpelt gennemsnit. Den første, "ustabile" periode regnes, men vises ikke. | [Kode: TA-Lib, `ta_RSI.c` ca. linje 175–235] |
| **DMI+/−, ADX** | Wilder-udglatning i sumform: ny = gammel − gammel/L + dagens. Starter fra 0 og samler de første L−1 bars. ADX kræver 2·L−1 bars, før der kommer et tal. | [Kode: TA-Lib, `ta_PLUS_DI.c` linje 312–446; `ta_ADX.c` linje 76] |
| **CCI** | Typisk pris (H+L+C)/3. Gennemsnitlig **absolut** afvigelse i et glidende vindue. Faktoren er 0,015. Intet med tilbagekobling. | [Kode: TA-Lib, `ta_CCI.c` linje 177–229] |

Det betyder:
- **CCI er et glidende vindue uden hukommelse**, i hvert fald hos TA-Lib. Hvis TradeStations CCI er bygget på samme måde, hører den til gruppe B (sandsynligvis sikker i løkke), ikke gruppe A. Det flytter 18 filtre fra "ukendt" mod "sandsynligvis i orden". Det skal bekræftes i TDE. [Antagelse]
- **RSI, DMI og ADX har tilbagekobling** (gruppe A) i TA-Lib. Det understøtter, at de er i fare i en løkke.

### 1.2 Er startværdien den samme som i TradeStation?
**UKENDT.** TradeStations officielle hjælp er blokeret herfra. Min antagelse er, at TradeStations XAverage starter med **den første pris**, ikke med et gennemsnit [Antagelse, ikke bekræftet]. Men TradeStations indbyggede funktioner er selv skrevet i EasyLanguage og kan åbnes i TDE. **Den lokale session kan derfor læse den præcise startregel på få minutter.** Det er det første, der skal gøres.

**Hvor meget betyder forskellen?** Jeg har regnet det på en kunstig prisserie (tilfældig gang, 5.000 bars, pris ca. 100) [Regnet: TA-Lib 0.8.1 mod EMA med start i første pris]:

| Bar | EMA(600), TA-Lib | EMA(600), start i første pris | Forskel |
|---|---|---|---|
| 599 (første TA-Lib-værdi) | 90,267 | 90,484 | 0,217 |
| 1.000 | 79,673 | 79,730 | 0,057 |
| 1.500 | 73,351 | 73,361 | 0,011 |
| 2.500 | 84,288 | 84,288 | 0,0004 |
| 4.000 | 87,953 | 87,953 | 0,0000 |

Det passer med formlen i del 2 §1.4: forskellen falder med faktoren (1−k) pr. bar. **Konklusion:** De to startregler giver praktisk talt ens tal efter ca. 2.500 bars ved længde 600. Før det kan de give forskellige signaler, når de to sider af en ulighed ligger tæt.

Jeg har også sammenlignet RSI(14) fra TA-Lib og talipp 2.7.0 på samme serie. De gav **identiske** værdier fra bar 14 [Regnet]. Selv om talipp's kode ser anderledes ud [Kode: talipp 2.7.0, `indicators/RSI.py`], giver de samme resultat her.

### 1.3 Kandidaterne vurderet

| Værktøj | Hvad det er | Licens / modenhed | Dom |
|---|---|---|---|
| **Egen lille Python-udgave skrevet efter TradeStations funktionskode** | Ca. 10 funktioner (XAverage, MACD, RSI, DMI, ADX, Average, TrueRange/ATR, StandardDev, CCI, Highest/Lowest). Hver er én side kode. Skrives ud fra den EasyLanguage-kode, man kan læse i TDE, så startreglen bliver den samme. | Vores egen | **BRUG NU som hovedfacit og som Python-regnemaskine** (K3's plan). Den er den eneste, der kan ramme TradeStation bit for bit, også i starten. |
| **TA-Lib 0.8.1** | Uafhængigt C-bibliotek | BSD-lignende, stabil, meget udbredt | **BRUG NU som tredjepart.** Fanger fejl i vores egen udgave. Sammenlign kun efter opvarmningsvinduet, fordi startreglen er anderledes. |
| **talipp 2.7.0** | Trinvis beregning: én ny bar ad gangen, ligesom TradeStation regner [Net: https://raw.githubusercontent.com/nardew/talipp/main/README.md – åbnet] | MIT, "Production/Stable" [Net: pypi talipp json – åbnet] | **SENERE.** God til at efterprøve mønster 3 (egen hukommelse pr. kombination), fordi den regner bar for bar. Ikke nødvendig nu. |
| **pandas-ta 0.4.71b0** | Stort Python-bibliotek | "Beta". Licenssiden er ikke læst. Kræver Python ≥ 3.12 [Net: pypi pandas-ta json – åbnet] | **NEJ** for nu. Beta, og licensen er ukendt. |

**Sådan håndteres forskelle i startværdien (protokol):**
1. Den lokale session læser startreglen for hver funktion i TDE og skriver den ned.
2. Vores Python-udgave bruger præcis den regel. Sammenligningen med TradeStation skal så være 100 % ens fra første signal.
3. Sammenligningen med TA-Lib sker kun efter opvarmningsvinduet: W = ln(0,001)/ln(1−k), altså 0,1 % tilbage af startfejlen. Det giver 2.073 bars ved EMA(600) og 4.142 ved Wilder(600) [Regnet, del 2 §1.4].
4. Bars med "grænsetilfælde", hvor forskellen mellem de to sider af uligheden er mindre end 1e-9 gange prisen, tælles for sig og må ikke tælle som fejl. Grænsen godkender K1.

---

## 2. Testteknikker for kodekvalitet

### 2.1 Differential testing (to uafhængige udgaver sammenlignes)
- **Hvad:** To udgaver, der er lavet uafhængigt af hinanden, skal give samme svar. Uenighed = mindst én fejl.
- **Løser:** F1 (K1), K4 i kontrolplanen og K3's facit-plan.
- **Til projektet:** Parterne er TradeStation uden løkke, Python-regnemaskinen og TA-Lib. Ved uenighed mellem TradeStation og Python afgør TA-Lib (efter opvarmning), hvem der tager fejl.
- **Pris:** Lav, når Python-regnemaskinen alligevel bygges.
- **Dom: BRUG NU.**

### 2.2 Golden master (snapshot) med kontrolsum
- **Hvad:** En godkendt CSV gemmes som "guldkopi" med en SHA-256-kontrolsum (et fingeraftryk af filen). Fremover skal den samme kørsel give præcis samme fingeraftryk.
- **Løser:** Tavse ændringer efter en opdatering af TradeStation eller generatoren, og dobbeltkørsels-tjekket i F1(b).
- **Til projektet:** En guldkopi pr. filter og workspace-type. Kontrolsummen gemmes i passet og i databasen (K3). Kan bruges både til TradeStation-CSV og Python-output. `syrupy` (MIT) findes til formålet [Net: pypi syrupy json – åbnet], men en kontrolsum i databasen er nok og enklere [Antagelse].
- **Risiko:** Filen indeholder ikke noget tidsstempel for selve kørslen, så samme kørsel giver samme fil. Men tilføjes kørsels-ID i filen (del 2 §1.7), skal det stå i en separat linje, der ikke indgår i kontrolsummen.
- **Dom: BRUG NU.**

### 2.3 Property-based testing (`hypothesis`)
- **Hvad:** Et program laver tusindvis af tilfældige, kunstige prisserier og tjekker "egenskaber", der altid skal holde.
- **Eksempler på egenskaber:**
  - Konstant pris → ATR = 0, og filtre af typen "range > ATR" tænder aldrig.
  - N2 = 1…5 i 069 giver ens signaler (dubletterne).
  - Hvis alle priser ganges med 2, ændrer RSI og CCI sig ikke.
  - Længde L = 1 → EMA = prisen.
  - Signaler må aldrig afhænge af fremtidige bars: hvis man ændrer bar t+1, må signalet på bar t ikke ændre sig. Det er en direkte test for look-ahead.
- **Licens og modenhed:** MPL-2.0, version 6.168.3 [Net: https://pypi.org/pypi/hypothesis/json – åbnet]. Meget moden.
- **Til projektet:** Kun til Python-regnemaskinen og EdgeFinder, ikke til TradeStation. Egenskaberne kan dog også køres i TradeStation ved at importere en kunstig serie som symbol, hvis TradeStation tillader det [UKENDT].
- **Dom: BRUG NU** for Python-delen. Look-ahead-egenskaben er den vigtigste.

### 2.4 Mutationstest (plant en fejl)
- **Hvad:** Man ødelægger bevidst koden (en "mutant") og ser, om testene opdager det. En test, der aldrig fanger noget, beviser intet.
- **Værktøj:** `mutmut` 3.8.0, BSD-3 [Net: pypi mutmut json – åbnet] gør det automatisk for Python-kode.
- **Til projektet, i to niveauer:**
  - (a) **Manuelt for EasyLanguage og kontrolplanen: BRUG NU.** Byg 10 bevidst forkerte udgaver af et filter:
    - forskudt én bar,
    - Data1 i stedet for Data2,
    - `>` i stedet for `>=`,
    - forkert længde (N1 mod N1+1),
    - MACD i løkke,
    - EMA-start i gennemsnit mod første pris,
    - decimaltrin 0,1,
    - FileDelete midt i kørslen,
    - manglende sidste signal,
    - forkert session.

    Kontrolplanens trin K1–K6 skal fange **alle 10**. Fanger den ikke en af dem, er kontrollen ikke god nok.
  - (b) **mutmut på Python-regnemaskinen: SENERE**, når den findes.

### 2.5 Statisk analyse med en rigtig parser
- **Hvad:** I dag findes seriefunktioner med et regulært udtryk på en navneliste [Projekt: `Program/formel.py:22-25, 105-106`]. Max Bars Back har sin egen håndskrevne parentes-løber [Projekt: `Program/max_bars_back.py:165-244`]. En parser læser formlen som et træ, præcis som en compiler.
- **Værktøjer:** `lark` 1.3.1, MIT [Net: pypi lark json – åbnet]. `pyparsing` 3.3.3, MIT [Net: pypi pyparsing json – åbnet]. lark er mest overskuelig til en lille grammatik [Antagelse].
- **Til projektet:** En grammatik for den del af EasyLanguage, der bruges i `filter_case.filtere`: funktionskald, `of data(...)`, `[n]`, `and/or`, sammenligninger og regning. Parseren giver for hver formel:
  - gruppe A–E (del 2 §2.3),
  - "indgang afhænger af N1/N2" (gruppe C),
  - "prisreference uden `of data`" (del 2 §1.5),
  - "ukendt funktion" (stop og spørg),
  - Max Bars Back og opvarmningsvindue i samme gennemløb.
- **Afgørende egenskab:** Kan en formel ikke læses, **stopper** parseren. Den gætter ikke. Det følger projektets princip "stop hellere end gæt" [Projekt: `Program/formel.py:28-29`].
- **Pris:** Ca. 1–2 dages arbejde. Test mod alle 380 formler.
- **Dom: BRUG NU.** Det er det billigste værn mod den tavse fejl i del 2 §1.3.

### 2.6 Samlet
Rækkefølgen er: parser (2.5) → facit med tre parter (1 + 2.1) → guldkopier (2.2) → plantede fejl (2.4a) → hypothesis (2.3). De første fire er nok til at gøre F1 fra K1 målbar.

---

## 3. Automatisering og regnemaskiner

### 3.1 Styring af TradeStation og TDE

| Mulighed | Vurdering | Dom |
|---|---|---|
| **WM_COMMAND, som i dag** | Virker og er testet [Projekt: `VIDENSLOG.md` 2026-09-24]. Menunumrene er interne og kan ændre sig ved en opdatering (K3). | **Behold** til Verify. Lås TradeStation-versionen. |
| **pywinauto** (BSD, 0.6.9) med `backend="uia"` (Microsoft UI Automation) | Kan finde knapper og felter efter navn i stedet for nummer [Net: https://raw.githubusercontent.com/pywinauto/pywinauto/master/README.md – åbnet]. TDE er et ældre Windows-program. Om UIA kan se dets felter, er **UKENDT**. Seneste version er gammel (0.6.9) [Net: pypi – åbnet]. | **SENERE**: kun hvis WM_COMMAND knækker. |
| **TradeStations Web API** | Projektet har selv konstateret, at den kun handler med kurser, konti og ordrer og ikke har forbindelse til TDE [Projekt: `RawSignal_Creature/NOTER.md`, "TDE har ingen API"]. Jeg har ikke fundet noget om backtest via Web API [Net, ikke bekræftet: https://developer.tradestation.com/]. | **NEJ** til backtests. |
| **EasyLanguage Optimization API** | TradeStation har objekt-klasser, som "give you tools to define and run optimization jobs using EasyLanguage" [Net, ikke bekræftet: "EasyLanguage Optimization API Developer's Guide", https://help.tradestation.com/10_00/eng/tsdevhelp/elobject/resources/pdf/easylanguage_optimization_api.pdf]. **Det kan være vejen til at køre mange backtests inde i TradeStation uden at styre skærmen.** Men optimeringer kører parallelt, og det ødelagde tidligere skrivning til filer [Projekt: `NOTER.md` punkt 2]. Om antallet af tråde kan sættes til 1, eller om resultatet kan hentes uden filer, er **UKENDT**. Det er objekt-orienteret EasyLanguage og kan ikke flyttes til MultiCharts. | **UNDERSØG NU** (lokal session, hjælpen findes i TDE). Byg ikke på det, før det er afprøvet. |
| **MultiCharts .NET** | Strategier i C#, hvor hver beregning kan have sin egen tilstand [Antagelse: fra min viden, siderne er blokeret]. | **SENERE**. Kun hvis MultiCharts vælges som regnemaskine. |

### 3.2 Python-regnemaskine: færdig motor eller egen kode?

| Værktøj | Fakta | Vurdering | Dom |
|---|---|---|---|
| **vectorbt 1.1.1** | Stabil. Kører tusindvis af indstillinger på én gang. **Licens: "Apache 2.0 with Commons Clause"**, som forbyder at "Sell" værdi, der stammer fra softwaren, også "consulting/support services" [Net: https://raw.githubusercontent.com/polakowo/vectorbt/master/LICENSE.md – åbnet] | Hurtig. Men licensen er uklar for en fond, der tjener penge på resultaterne. Det er en juridisk risiko, som ikke skal gættes [Antagelse]. Den er også en backtest-motor, ikke et event-studie. | **NEJ**, medmindre en jurist godkender licensen. |
| **backtrader 1.9.78** | GPLv3+ [Net: pypi – åbnet] | Går bar for bar i ren Python, så den er langsom ved 84.400 kombinationer [Antagelse]. GPL giver krav ved videregivelse. | **NEJ** |
| **Egen enkel kode (numpy/pandas)** | Signaler = indikator (afsnit 1) + sammenligning. Event-studie = opslag af fremtidige afkast på faste horisonter. | Et event-studie er få og klare regnestykker. Egen kode kan læses af en professionel og testes med 2.1–2.4. Ingen licensrisiko. | **BRUG NU** |
| **arch 8.0.0** (NCSA-licens) | Har `StationaryBootstrap` (Politis & Romano), `CircularBlockBootstrap` og `optimal_block_length` [Kode: arch 8.0.0, `bootstrap/base.py`]. Har også `SPA` (White/Hansen's "Reality Check"), `StepM` (Romano–Wolf) og `MCS` [Kode: arch 8.0.0, `bootstrap/multiple_comparison.py`] | Moden og præcis det, E3 kræver. SPA/StepM er standardmetoder mod "data snooping" (at finde tilfældige vindere, fordi man har prøvet mange ting). | **BRUG NU** til bootstrap. SPA/StepM: **K1 vurderer**, for det er metode. |

---

## 4. EdgeFinder-protokol, version 3

**Status: godkendt af K1 med ændringer, indarbejdet 2026-09-28** (K1's krav står i `udkast3/k1_kritik.md`). Ændringerne:
1. **Dom på råt nettoafkast (A6/A9).** Den kontrol-justerede t ≥ 2 er et ekstra krav.
2. **StepM er grænsen (A9).** Det er ikke længere en t-værdi ud fra N_eff. Metodefilen skriver, hvilken test der giver "rejected" [Thomas afgør].
3. **Walk-forward (E5) er tilføjet (nyt trin A11).**
4. **Minimum pr. celle er (1,28/δ)² (A8).**
5. **Opvarmningen regnes i bars pr. datastrøm, og charts starter senest 2017 (4.1).** Det bekræftes med en to-starts-test.
6. **Kontrolsignaler (A10):** placebo køres også gennem StepM. Højst 1 ud af 20 placebo-sæt må give fund.
7. **Slippage (4.5):** ensidet bootstrap-test mod modellen, α = 5 %, efter mindst 30 handler.
8. **Lag B (B3):** StepM med benchmark = filteret *uden* kolonnen.
9. **Identitet (4.6):** "Ligner, men er ikke ens" tæller som et forsøg i samme familie.
10. **Lag A (A8):** et af K1's tre kriterier, med Holm på tværs af de 14 celler.

Jeg er fagligt enig i alle ti punkter. Der er ingen uenighed tilbage om protokollen.


*Omskrevet efter Thomas' afgørelser fra Det Runde Bord. Tre ting er afgjort og genåbnes ikke:*
- *et filter, der fejler, er endeligt dødt ("rejected"),*
- *der valideres out-of-sample,*
- *der er inkubation før live [Projekt: Det Runde Bord-sammenfatning].*

*Det, der står som [K1], er grænser, som K1 fastsætter. Det, der står som [Thomas], er valg, som Thomas træffer.*

### 4.0 Den vigtigste følge af "rejected er endeligt"
En forkert dom kan ikke længere rettes. Derfor skifter de tavse fejl fra del 2 fra "dyre" til "**uoprettelige**":
- MACD-fejlen: alle kombinationer er ens og ligner et falsk plateau (del 2 §1.1).
- Opvarmning: indikatoren har ikke nået at glemme sin startværdi (del 2 §1.4).
- Blandede datastrømme: Data1 og Data2 blandes uden fejlmelding (del 2 §1.5).
- Tidsstemplet læses forkert, så man kigger ind i fremtiden (del 2 §1.6).

Et filter, der bliver "rejected" på grund af forkerte tal, dør for altid, og ingen opdager det. **Konsekvens:**
- **Intet filter må få en Lag A-dom, før det har bestået F1 og kontrolplanens trin K0–K6** (del 2 §4).
- Gruppe A/C/D (del 2 §2.3) står i status "venter", ikke "rejected", indtil de er bygget om.
- En teknisk fejl giver "failed" (må køres igen). Kun en analytisk dom giver "rejected" [Projekt: Det Runde Bord-sammenfatning, del 2 pkt. 1].

**Åbent punkt (genåbner ikke afgørelsen):** Hvis en teknisk fejl opdages *efter* en dom, var dommen så en analytisk dom? Eksempel: en funktion viser sig at regne forkert. Mit råd er, at hver dom gemmer, hvilken kode- og funktionsversion den blev fældet under. Så kan man i det mindste se, hvilke domme der er fældet på tal, der senere blev fundet forkerte. Hvad der så skal ske, afgør Thomas.

### 4.1 Dataperioder og låsning
| Lag | Periode | Bruges til | Må bruges |
|---|---|---|---|
| In-sample (IS) | 2020–2024 | Lag A, Lag B, EdgeCruncher | Én gang pr. filter pr. metodeversion |
| Out-of-sample (OOS) | 2025 | Første kontrol | Én gang pr. filter. Antal filtre, der har rørt 2025, tælles |
| Embargo | Låst historik, datoer [Thomas] | Anden kontrol | Én gang |
| Inkubation | Fremtidige data | Endelig test | Én gang, med uret nulstillet ved enhver ændring |

- **Signaler regnes én gang over hele historikken, og charts starter senest 2017 (rettet efter K1).** Opvarmningen regnes i **bars pr. datastrøm**, ikke i kalenderår. En EMA(600) kræver ca. 2.000 bars. Det er ca. 1,2 år på 60-minutters RTH-bars og over 2 år på 120-minutters bars (K1). "Fra 2019" var derfor for kort til de langsomme strømme.
  - Generatoren regner opvarmningen pr. filter og pr. datastrøm og skriver den i passet.
  - En **to-starts-test** bekræfter det: samme filter køres med chart-start 2016 og 2017. Signalerne fra 2020 og frem skal være identiske.
- At *regne* signaler i 2025 er ikke at "bruge" 2025. Det gør først analysen. Adgangen til resultater fra OOS og embargo skal være låst i koden, indtil filteret har status "klar til OOS" (K3 håndhæver det).
- Metodefilen skal skrives og låses (version + dato + kontrolsum), før det første filter køres [Projekt: Det Runde Bord-sammenfatning, del 4 pkt. 1]. Den skal indeholde:
  - Lag A-listen,
  - minimum signaler pr. celle,
  - plateau-grænsen,
  - horisonter,
  - retning,
  - omkostnings- og slippage-model,
  - bootstrap-indstillinger,
  - Lag B-grænser.

### 4.2 Trin for trin (Lag A – det låste event-studie)

**A1 – Input.** Filtre med F1 bestået. Signalrækker fra Python-regnemaskinen og bars fra samme TradeStation-chart. Identiske rækker slås sammen, og antallet af unikke rækker gemmes.

**A2 – Event.** En event er **tænding**: skiftet fra falsk til sand (Starttid). Events med `Afsluttet = 0` tages kun med, hvis hele horisonten er i data.

**A3 – Signalpris og indgang (E1).**
- Starttid er barens sluttid [Antagelse; bekræftes lokalt mod chartet].
- **Signalpris** = lukkekursen på signal-baren. Det er den sidste kendte pris, da beslutningen træffes.
- **Modelleret fill** (den pris, handlen antages at blive udført til) = åbningen af næste bar i samme session, plus eller minus k ticks [Thomas].
- Signal på sessionens sidste bar → eventen droppes. Der handles ikke over natten.
- Data2/Data3 på højere tidsramme: kun færdige bars (egenskabstest del 2B §2.3).

**A4 – Horisonter og retning.**
- Horisonterne fastlægges på forhånd, fx 1, 5, 10, 20 bars og "sessionens slut".
- Udgang = modelleret fill ved horisontens slut eller sessionens slut.
- Retning: begge tæller 2 i N_rå (K1), eller den fastlægges på forhånd pr. filter [Thomas].

**A5 – Afkast og omkostninger (E4).**
- Nettoafkast = (udgangs-fill − indgangs-fill) × retning − kurtage.
- Slippage gemmes **separat** efter bordets definition (afsnit 4.5), så backtest og inkubation kan sammenlignes.
- Stresstest med dobbelte omkostninger (F7).

**A6 – Kontrolgruppe (E2).**
- Kontrol-bars uden event, med samme tid-på-dagen-spand, ugedag og volatilitets-tredjedel.
- **Dommen træffes på råt nettoafkast** (A5), for det er det, der kan handles (K1). "Event − kontrol" bruges kun som et **ekstra krav**: den kontrol-justerede t skal være ≥ 2. Det viser, at effekten ikke bare er markedets almindelige bevægelse på det tidspunkt.
- Ekstra kontrol: cirkulær forskydning af signalrækken 200 gange.

**A7 – Afhængighed (E3).** Ét tal pr. handelsdag pr. variant på en **fælles tidsakse**, hvor dage uden event tæller som 0. Stationær blok-bootstrap (`arch`) med bloklængde fra `optimal_block_length`, mindst 1 dag og 10.000 gentagelser, og **samme** trukne dage for alle varianter (kravet fra StepM). Retning og horisont låses i metodefilen, ellers bliver tabellen ti gange større (k2_kritik).

**A8 – Lag A-opdelinger (den låste liste).**
- Liste [K1/Thomas låser den]: år (2020, 2021, 2022, 2023, 2024), volatilitetsniveau (3 niveauer ud fra ATR før indgang), tid på dagen (3 spand) og signalvarighed (AntalBars i 3 niveauer).
- **Råd: opdel én dimension ad gangen, ikke alle på kryds.** Regnestykke [Regnet]:
  - På kryds giver det 5 × 3 × 3 × 3 = **135 celler**.
  - Med fx 1.000 signaler i IS bliver det ca. **7 signaler pr. celle**. Det er for få til at sige noget.
  - Hver dimension for sig giver 5 + 3 + 3 + 3 = **14 celler** og ca. 200–330 signaler pr. celle.
- **Minimum signaler pr. celle – rettet efter kritikrunden:** Jeg bruger K1's regnestykke (K1 v3 §5.3): n ≥ (1,28/δ)². Det er det antal, der skal til, for at en ægte effekt viser positivt fortegn i cellen med 90 % sandsynlighed. Eksempler: δ = 0,1 giver 164, δ = 0,05 giver 657. Mit eget forslag (196 ved en styrke-test på 5 %-niveau) var for strengt, fordi en celle ikke skal *bevise* effekten, men kun *ikke modsige* den. Celler under minimum er grå, ikke røde.
- **Kriterium (godkendt af K1):** et af K1's tre kriterier, med Holm-korrektion på tværs af de 14 celler.
- **Formål:** at afsløre, om effekten kun kommer fra én periode eller én situation. **Rettet:** Mit forslag "samme fortegn i mindst 4 af 5 år" er fjernet. K1's tabel viser, at krav om "alle/næsten alle celler positive" slår mange ægte edges ihjel. Ved 10 celler overlever kun 44 % af ægte edges med Sharpe 2. Kriteriet vælges blandt K1's tre (ingen celle signifikant negativ / uden den bedste celle / heterogenitetstest) og kalibreres med placebo og indplantede edges, før det låses [K1; Thomas vælger]. Lag A er en stabilitetstest. Hovedtesten er StepM (K1).

**A9 – Dom på IS (E6) – rettet efter K1.**
- Grovsortering med FDR q = 10 %.
- **Den endelige grænse er Romano–Wolf StepM** (`arch`) på råt nettoafkast pr. dag. Alle unikke varianter i familien testes samlet (K1 V3). t ud fra N_eff og DSR vises som tal ved siden af, men afgør ikke.
- Ekstra krav: kontrol-justeret t ≥ 2 (A6), Lag A-kriteriet (A8) og plateau efter K1 §8 (Thomas vælger niveau).
- Metodefilen skriver præcist, hvilken test der giver "rejected" [Thomas afgør].
- Består filteret ikke: **rejected**, med årsag "faldt i Lag A-gaten", metodeversion og kodeversion.

**A10 – Placebo og indplantet edge (E7, E8).** Skal bestås **for hver kørsel**, før dommene i A9 må skrives:
- 1.000 tilfældige signaler (cirkulær forskydning i **hele handelsdage**) med samme hyppighed, varighed og tid-på-dagen-profil: 3,6–6,4 % må slippe igennem ved 5 %.
- **Placebo køres også gennem StepM (K1):** Placebo-sættene testes i deres **egen** StepM-familie med identiske indstillinger, ikke blandet med de ægte varianter. Højst 1 ud af 20 placebo-sæt må give fund.
- Indplantet edge på kunstige data: mindst 80 % skal findes.
- Består kørslen ikke: **hele kørslen er "failed"** (teknisk), ingen filtre får dom, der ryddes op, og der startes forfra.

**A11 – Walk-forward (E5) – nyt, krævet af K1.**
- **Alle valg i EdgeCruncher** træffes *inde i* hvert trænings-vindue i IS (2020–2024) og testes på det efterfølgende vindue. Det gælder udgangsregel, stop, mål, horisont og retning, hvis den ikke er låst. Opskriften (vindueslængde, trin, antal vinduer) skrives i metodefilen, før der regnes [K1].
- De sammensatte test-vinduer vurderes samlet efter K1's F6.
- Træffes der ingen valg (ren signal-test uden tilpasning), er walk-forward ikke nødvendig. Så er 2025 den eneste opdeling (K1's R1–R3).

### 4.3 Lag B – begrænset søgning (kun filtre, der har bestået Lag A)
- **B1.** Kun IS-data. Kun kolonner fra en forud skrevet liste over kandidat-kolonner [Thomas/K1].
- **B2.** **Hvert prøvet par (kolonne, grænse) tælles og gemmes** i databasen pr. filter, med kørsels-ID (K3).
- **B3.** Korrektion for antallet af forsøg: **StepM med benchmark = filteret *uden* kolonnen** (K1). Kolonnen godkendes kun, hvis den slår filteret uden kolonnen efter korrektion.
- **B4.** Almgrens krav [Projekt: Det Runde Bord-sammenfatning, del 4 pkt. 5]: en kolonne godkendes kun, hvis nettoresultatet efter slippage og kurtage stiger mere end en forud fastsat grænse. Det er nettoresultatet, der skal stige, ikke kun gennemsnittet pr. signal.
- **B5.** Fund prøves derefter på 2025 og så på embargo. Hver gang kun én gang.

### 4.4 Lag C – forbudt, og håndhævet teknisk
Et filter med status "rejected" kan ikke vælges af nogen analyse, genstartes af nogen maskine eller komme tilbage i en ny forklædning. Det håndhæves tre steder (afsnit 4.6): i databasen, i generatoren og i EdgeFinder.

### 4.5 Slippage efter bordets definition
Bordet: **slippage = signalpris − fillpris**, beregnet ens i backtest og inkubation [Projekt: Det Runde Bord-sammenfatning, del 3].
- **Fortegnet skifter med retningen.** Ved køb er en fill *over* signalprisen dårlig, og så bliver signalpris − fillpris negativ. Ved salg er en fill *under* signalprisen dårlig, og så bliver tallet positivt. Råd: gem den **rå værdi** (signalpris − fillpris) plus retning, og regn en afledt "ugunstig slippage i ticks" = retning × (fillpris − signalpris) / tick-størrelse, så positivt altid betyder dårligt. Ellers udligner køb og salg hinanden i et gennemsnit, og slippage ser ud til at være nul.
- **Signalpris skal defineres ens begge steder:** lukkekursen på signal-baren, som strategien selv beregner og **logger** i det øjeblik, ordren sendes.
- **Backtest:** fillpris = næste bars åbning ± modelleret k ticks. Slippage indeholder altså også springet fra luk til næste åbning. Det er korrekt, for det er en reel omkostning ved at handle på signalet.
- **Inkubation:** fillpris = den faktiske fill fra mægleren. Strategien logger signalpris, ordretidspunkt, fill-tidspunkt, fillpris, ordretype og kurtage for hver handel.
- **Afkast regnes fra fillpris**, og slippage vises ved siden af. Så tælles den ikke to gange.
- **Kontrol (K1):** Efter mindst 30 handler i inkubation laves en ensidet bootstrap-test af den ugunstige slippage mod backtestens model, α = 5 %. Er den reelle signifikant værre, er omkostningsmodellen for optimistisk, og det gælder alle filtre.

### 4.6 Filter-identitet – så et dødt filter ikke kan komme tilbage
Bordet: formel + parameterinterval + instrument + tidsramme = identitet [Projekt: Det Runde Bord-sammenfatning, del 2 pkt. 3].

**Fingeraftryk (SHA-256) af en normaliseret identitet:**
1. **Formlen** læses af parseren (del 2B §2.5) til et træ og skrives ud i en fast form:
   - samme store/små bogstaver,
   - ingen mellemrum eller kommentarer,
   - parameternavne erstattet af P1/P2,
   - tal skrevet ens (2 og 2.0 er det samme),
   - enkle omskrivninger gjort ens (`a < b` = `b > a`, `N*2` = `2*N`).
2. **Parameterinterval:** mængden af faktisk brugte værdier (Fra/Til/Step udfoldet). Så giver "1–25 step 1" og "1–25 step 2" forskellige mængder, der kan sammenlignes.
3. **Instrument:** rodsymbol + kontinuitetstype + sessionsskabelon.
4. **Tidsrammer:** interval for Data1/Data2/Data3.

**Regler, der håndhæves:**
- **Samme fingeraftryk som et rejected filter → generatoren stopper** med en ByggeFejl ("filteret er dødt"), ligesom den i dag stopper ved andre usikre forhold [Projekt: `Program/formel.py:28-29`].
- **Samme formel-træ, instrument og tidsramme, og parametermængden overlapper et rejected filter → stop.** Thomas ser listen. Det fanger "lidt ændrede tal" (fx 1–25 → 2–24).
- **Formel-træet ligner et dødt filter, men er ikke ens** (fx én funktion byttet): ikke stop, men en advarsel i journalen, og **det tæller som et forsøg i samme familie** (K1). Fuld matematisk lighed kan ikke afgøres automatisk i alle tilfælde. **UKENDT** hvor ofte det sker.
- **Tre låse:**
  - Databasen: status rejected kan ikke ændres af fabrikkens bruger. Det er K3's rollemodel.
  - Generatoren: tjekker fingeraftrykket før bygning.
  - EdgeFinder og maskinerne: vælger kun jobs, hvis fingeraftryk ikke er rejected.
- **Følge for omnummereringen:** Filternummeret er ikke identiteten. Fingeraftrykket er. Det løser også problemet med de flyttede numre [Projekt: `VIDENSLOG.md` 2026-09-24].

### 4.7 Inkubation – følger for EdgeCruncher og kodens fingeraftryk
- **EdgeCruncher skal aflevere en frossen pakke:** strategifil + alle indstillinger + fingeraftryk. Det er denne pakke, der går i OOS, embargo og inkubation. Intet må tilpasses efter IS.
- **Strategiens fingeraftryk** = SHA-256 af:
  - den normaliserede kildekode **uden kommentarer**, fordi generatoren i dag skriver byggetidspunktet ind i hovedet [Projekt: `Program/generer.py:52`], og så ville fingeraftrykket ændre sig ved hver bygning,
  - input-værdier,
  - Max Bars Back,
  - symbol og session,
  - Data1/2/3-opsætning,
  - IOG-indstilling,
  - omkostnings- og slippage-indstillinger,
  - TradeStation-build.
- **Nulstilling af uret sker teknisk:** Strategien skriver selv sine indstillinger (symbol, interval, Max Bars Back, input) i en log på første bar hver dag. Et program sammenligner med det registrerede fingeraftryk. Afvigelse → uret nulstilles automatisk, og det logges. Om EasyLanguage kan aflæse alle indstillinger (fx sessionsskabelonen), er **UKENDT**. Det, der ikke kan aflæses, skal låses i arbejdsområdet og tjekkes af K3's opsætningstjek.
- **Inkubationen måles i både tid og antal handler** [Projekt: Det Runde Bord-sammenfatning]. EdgeCruncher skal skrive det forventede antal handler pr. uge (fra IS) i passet. Så kan man på forhånd se, hvor lang inkubationen skal være for at nå K1's minimum.
- **Beslutningsreglen ved inkubationens slutning** er et åbent spørgsmål til Thomas. Den skal stå som tal, før den første strategi går ind [Projekt: Det Runde Bord-sammenfatning, del 6].

### 4.8 Test af selve protokollen, før den bruges
Placebo og indplantet edge køres på rent kunstige data, før rigtige data røres. De 10 plantede fejl (2.4a) skal alle ende som "failed", ikke "rejected". **Det er vigtigt nu:** En teknisk fejl, der fejlagtigt bliver til et "rejected", er uoprettelig.

---

## 5. Kilder jeg selv har åbnet og læst

- TA-Lib C-kode: `ta_EMA.c`, `ta_MACD.c`, `ta_RSI.c`, `ta_PLUS_DI.c`, `ta_ADX.c`, `ta_CCI.c` fra https://raw.githubusercontent.com/TA-Lib/ta-lib/main/src/ta_func/
- talipp 2.7.0 (wheel via pip download): `indicators/EMA.py`, `indicators/RSI.py`, samt README på raw.githubusercontent.com/nardew/talipp/main/README.md
- arch 8.0.0 (wheel): `bootstrap/base.py`, `bootstrap/multiple_comparison.py`
- vectorbt LICENSE.md på raw.githubusercontent.com/polakowo/vectorbt/master/LICENSE.md
- pywinauto README på raw.githubusercontent.com/pywinauto/pywinauto/master/README.md
- PyPI JSON for: talipp, pandas-ta, TA-Lib, hypothesis, mutmut, lark, pyparsing, pywinauto, vectorbt, backtrader, arch, syrupy
- Egne regnestykker: TA-Lib 0.8.1 og talipp 2.7.0 installeret i scratchpad (EMA-start og RSI-sammenligning, afsnit 1.2)

**Ikke åbnet (blokeret / kun uddrag):** TradeStation-hjælp (Optimization API, Web API) og MultiCharts .NET.

---

## 6. Nye åbne punkter til Thomas
1. Må den lokale session læse TradeStations egen kode for XAverage, RSI, DMI, ADX, CCI og StandardDev i TDE (kun læsning) og skrive startreglerne ned?
2. Skal EasyLanguage Optimization API undersøges som vej til automatiske backtests uden skærmstyring?
3. Hvad er en event: tænding (anbefalet) eller hver tændt bar?
4. Skal signaler på sessionens sidste bar droppes (ingen handel over natten)?
5. Omkostninger pr. marked: kurtage og slippage i ticks.
6. Skal retningen fastlægges på forhånd pr. filter, eller testes begge (koster en faktor 2 i forsøg)?
7. Må vectorbt overvejes, hvis en jurist godkender Commons Clause-licensen? Mit råd er nej.
8. Hvis en teknisk fejl opdages *efter* en dom: hvordan skal domme fældet på forkerte tal markeres? (Afsnit 4.0. Afgørelsen om, at rejected er endeligt, genåbnes ikke.)
9. Embargo-periodens datoer, og hvor mange bars fra før 2020 der må bruges til opvarmning.
10. Lag A-listen: skal den opdeles én dimension ad gangen (anbefalet, 14 celler) eller på kryds (135 celler)?
11. Signalpris: skal den være lukkekursen på signal-baren (anbefalet), og skal ugunstig slippage gemmes med retningsfortegn?


# Del 3 – Data, dvale-lager og automatisering (Konsulent 3, dybde-runden)

*Rettet efter Det Runde Bord (Thomas' afgørelser): `datadeling`/`pengeskab_aabning` (FORSLAG G) er erstattet af fire datalag (in-sample 2020–2024, out-of-sample 2025, embargo, inkubation), statusserne `failed` (job, må køres igen) og `rejected` (filter, endeligt, med dødsårsag), filter-identitet, Lag B-tælling, versioneret metodefil (erstatter `regelsaet`) og inkubation – se udkast3/k3.md afsnit 6–7.*

*Rettet i runde 3: `dvale_pas` har nu `n_raa`, `n_eff`, `t_vaerdi` og en samlet walk-forward-t-værdi (`wf_t_samlet`) i stedet for `walkforward_andel_pos`; kolonnerne til `analyse_kombination`, `edge_kombination` og `kandidat` er skrevet (afsnit 3.3, FORSLAG I); facit-backtest køres nu pr. workspace-type (4 × 380), ikke på ét referencedatasæt; råsignaler foreslås gemt som Parquet-filer i stedet for i PostgreSQL (se udkast3/k3.md, Del 3B) – SQL-forslag D for `fabrik.signal` er derfor kun reserve.*

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
-- FORSLAG I: tabellerne for led 2–4. Én række pr. forsøg; dumpede rækker bliver stående (K1).
-- Nøglen er den samme overalt: kørsel × filter × kombination (n1_idx, n2_idx).
CREATE TABLE fabrik.analyse_kombination (          -- led 2, RawSignal-Analyse
    koersel_id    bigint NOT NULL REFERENCES fabrik.koersel,
    filter_uid    uuid NOT NULL, filter_version int NOT NULL,
    n1_idx smallint NOT NULL, n2_idx smallint NOT NULL,
    datadel       text NOT NULL CHECK (datadel IN ('udvikling','validering')),  -- aldrig 'pengeskab'
    antal_signaler int NOT NULL,                  -- efter opvarmningsvinduet
    antal_aabne   int NOT NULL,                   -- afsluttet = false
    gns_antalbars numeric, median_antalbars numeric,
    signaler_pr_aar numeric,
    kopi_af       smallint[],                     -- K2: kombinationer med identisk signalrække (MACD-typen)
    plateau_farve text,                           -- 'groen'/'graa'/'roed' efter regelsaet; NULL = ikke afgjort
    regelsaet_id  int REFERENCES fabrik.regelsaet,
    signal_fil_sha256 text NOT NULL,              -- fingeraftryk af den Parquet-fil, tallene kom fra
    PRIMARY KEY (koersel_id, filter_uid, filter_version, n1_idx, n2_idx, datadel)
);

CREATE TABLE fabrik.edge_kombination (             -- led 3, EdgeFinder (event-studie)
    koersel_id    bigint NOT NULL REFERENCES fabrik.koersel,
    filter_uid    uuid NOT NULL, filter_version int NOT NULL,
    n1_idx smallint NOT NULL, n2_idx smallint NOT NULL,
    datadel       text NOT NULL CHECK (datadel IN ('udvikling','validering')),
    retning       smallint NOT NULL CHECK (retning IN (1,-1)),   -- køb / salg
    horisont      text NOT NULL,                  -- fx '1','5','10','20' bars eller 'dagsslut'
    indgang       text NOT NULL,                  -- K2 1.6: fx 'naeste_bar_aabning'
    antal_events  int NOT NULL,
    n_uafhaengig  numeric,                        -- K1: effektivt n efter overlap (blok-bootstrap)
    gns_afkast    numeric, spredning numeric,
    t_vaerdi      numeric, p_vaerdi numeric,
    omk_model     jsonb,                          -- NULL = før omkostninger
    bestaaet_grov boolean,                        -- K1's grovsortering (FDR); NULL = ikke vurderet
    PRIMARY KEY (koersel_id, filter_uid, filter_version, n1_idx, n2_idx, datadel, retning, horisont)
);  -- høj-scenariet: 380 × 625 × 2 × 5 × 2 datadele ≈ 4,75 mio. rækker pr. datasæt ≈ 1 GB. Det er i orden.

CREATE TABLE fabrik.kandidat (                     -- led 4, EdgeCruncher (K2 designer indholdet)
    kandidat_id   bigserial PRIMARY KEY,
    koersel_id    bigint NOT NULL REFERENCES fabrik.koersel,
    filter_uid    uuid NOT NULL, filter_version int NOT NULL,
    n1_idx smallint NOT NULL, n2_idx smallint NOT NULL,   -- midten af plateauet (K2)
    plateau_graenser jsonb NOT NULL,              -- hvilke naboer der er med
    retning       smallint NOT NULL, horisont text,
    udgangsregler jsonb NOT NULL,                 -- fast lille sæt (K2); hver variant tæller i F3
    strategi_fil_sti text NOT NULL, strategi_fil_sha256 text NOT NULL,
    generator_version text NOT NULL,
    resultat_udv  jsonb NOT NULL,                 -- handler, netto, drawdown på udviklingsdata
    resultat_val  jsonb NOT NULL,                 -- samme på valideringsdata (aldrig pengeskab)
    wf_t_samlet   numeric, wf_antal_vinduer int,
    kontrol_status text NOT NULL,                 -- K2's K0–K6 samlet: 'bestaaet'/'fejlet'/'ikke_kontrolleret'
    platform_verificeret text[] NOT NULL,
    oprettet      timestamptz NOT NULL DEFAULT now()
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
    runde_id           int NOT NULL REFERENCES fabrik.forsoegsregnskab,  -- F3: hvilken forskningsrunde
    n_raa              bigint NOT NULL,     -- F3: kopieret fra regnskabet ved oprettelse (låst runde)
    n_eff              numeric NOT NULL,    -- F3/F4: MÅLT N_eff; passet kan ikke oprettes uden
    t_vaerdi           numeric NOT NULL,    -- F4: strategiens t på udviklings- + valideringsdata
    mt_metode          text NOT NULL,       -- fx 'DSR', 'BH-FDR 10%' (K1: skriv hvilken metode)
    deflated_sharpe    numeric,             -- F4 (regnet med n_eff)
    pbo                numeric,             -- Probability of Backtest Overfitting (K1)
    plateau_niveau     int,                 -- F5; betydning slås op i regelsaet (ingen fast skala)
    wf_t_samlet        numeric NOT NULL,    -- F6: samlet t-værdi over alle walk-forward-vinduers
                                            --     out-of-sample-handler (K1), ikke 'andel positive'
    wf_antal_vinduer   int NOT NULL,        -- F6: hvor mange vinduer tallet bygger på
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
- TradeStation bruges til det, kun TradeStation kan: Verify og en **facit-backtest pr. filter pr. workspace-type**. **Rettet i runde 3 efter K2's indvending:** de 4 workspaces har forskellige tidsrammer på Data2/Data3 (5,10,60 / 10,20,60 / 5,30,120 / 5,10,120) [Projekt: NOTER.md:150-151]. Hvordan TradeStation stiller bars fra forskellige tidsrammer op mod hinanden, er netop det, Python mest sandsynligt gør forkert [Antagelse]. Ét referencedatasæt beviser det ikke for de andre tre. Det giver 380 × 4 = 1.520 backtests pr. marked. For hvert *nyt* marked kører en stikprøve (fx mindst ét filter pr. gruppe A–E pr. workspace) for at vise, at markedet ikke opfører sig anderledes.
- Python regner alle andre datasæt og alle senere led. Et filter må først bruges i Python på en workspace-type, når dets Python-signaler er identiske med TradeStations facit på netop den type.
- Regnestykke med 5 min pr. backtest (antagelse, se 2.6): 1.520 × 5 min = 7.600 min ≈ 127 timer ≈ 5,3 døgn i TradeStation for det første marked. Det er stadig langt fra 40 døgn for alle datasæt, og langt fra K2's 84.400 kørsler.
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
4. **Python-vejen:** Må signalerne regnes i Python og bevises ens med TradeStation pr. workspace-type (1.520 facit-backtests pr. marked)?
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
- Kolonnerne for led 2–4 er skrevet (FORSLAG I), men indholdet af EdgeCrunchers udgangsregler og K1's præcise statistik kan ændre felterne i jsonb-kolonnerne.
- Intet SQL er afprøvet.


# Del 3B – Værktøjer og protokoller til data, drift og automatisering (Konsulent 3, runde 3)

*Råd, ikke beslutninger. Ingen kode leveres, og intet i projektet er ændret. SQL er FORSLAG og vises for Thomas før brug.*

**Mærker:**
- [Projekt: fil:linje]
- [Projekt: Det Runde Bord-sammenfatning] = Thomas' egne afgørelser fra runde_bord.txt
- [Net: URL – åbnet] = jeg har selv læst indholdet
- [Net, ikke bekræftet] = kun set som søgeuddrag
- [Kode: pakke version, fil] = kildekode, jeg selv har læst
- [Målt] = kørt af mig i scratchpad på syntetiske data
- [Antagelse: hvorfor]

**Rettet efter kritikrunden i runde 3:** afsnit 7.8 tilføjet: K1's faste pas-kolonner (hans §3.2) præcis som han opstiller dem, ny tabel `genvaekning`, K1's talgrænser som felter i metodefilen; K2's fingeraftryk (normaliseret formel-træ, udfoldet parametermængde, instrument inkl. session, tidsrammer for Data1–3) erstatter `numrange` i 7.1; status `venter` og en spærring, så ingen Lag A-dom kan falde før F1/K0–K6; lagring til StepM og placebo (7.9).

**Rettet i udkast2/k3.md (samme runde):**
- `dvale_pas` har fået N_rå, N_eff, t-værdi og en samlet walk-forward-t-værdi i stedet for "andel positive vinduer".
- Kolonnerne til `analyse_kombination`, `edge_kombination` og `kandidat` er skrevet.
- Facit-backtest køres pr. workspace-type (380 × 4 = 1.520 pr. marked), ikke på ét referencedatasæt. Det følger K2's indvending, og begrundelsen står i v2 afsnit 4.2.
- Råsignaler foreslås nu gemt som Parquet-filer (se afsnit 1). PostgreSQL-tabellen `fabrik.signal` er kun reserve.
- Datadeling og pengeskab er erstattet af de fire datalag fra Det Runde Bord (se afsnit 7 her).

---

## 0. Kort sagt – anbefalingerne

| # | Område | Anbefaling | Dom |
|---|---|---|---|
| 1 | Råsignaler | **Parquet-filer + DuckDB**. PostgreSQL beholdes til journal, status, pas og køen. | BRUG NU |
| 2 | Kø | **Egen `SKIP LOCKED`-tabel**, eller pgqueuer, hvis der skal spares kode. Ingen orkestrator. | BRUG NU |
| 3 | Forsøgsregister | **Egne tabeller** (forsøgsregnskab, filter-forløb). Ikke MLflow/DVC. | BRUG NU |
| 4 | CSV-kontrol | **pandera** + faste tjek af antal kombinationer og slutdato | BRUG NU |
| 5 | Backup | **pg_dump + Windows Opgavestyring + robocopy** af Parquet-mappen, med en månedlig gendannelsesprøve | BRUG NU |
| 6 | Betjeningsflade | **NiceGUI** som TradingApp-fane (Streamlit som nr. 2) | BRUG NU (lille) |
| 7 | Det Runde Bords regler | **Håndhæves i databasen** med statusser, fire datalag, metodeversion og inkubation (afsnit 7) | BRUG NU (før første filter) |

Grundtanken er: **mindre er mere.** Én database (PostgreSQL), én mappe med filer (Parquet), ét Python-program pr. maskine og én fane. Hvert ekstra værktøj er én ting mere, som Thomas og hans AI-assistent skal forstå, opdatere og tage backup af.

---

## 1. Lagring af råsignaler: PostgreSQL mod Parquet/DuckDB mod TimescaleDB

### 1.1 Hvad er det?
- **PostgreSQL** gemmer rækker. Hver række har et hoved på 23–24 bytes plus en pegepind på 4 bytes [Net: https://raw.githubusercontent.com/postgres/postgres/master/doc/src/sgml/storage.sgml – åbnet i runde 2]. Det er godt til små, vigtige tabeller, der ændres og tjekkes. Det er dyrt til hundreder af millioner smalle rækker.
- **Parquet** er et filformat, der gemmer én kolonne ad gangen og pakker den (komprimerer). Ens tal efter hinanden fylder næsten intet. En Parquet-fil ændres ikke, når den først er skrevet. Den passer til "kun tilføje" og "ryd op og start forfra": slet mappen og skriv igen.
- **DuckDB** er en lille database-motor, der kører inde i Python og kan læse Parquet-filer direkte med almindelig SQL. MIT-licens, version 1.5.5, "Production/Stable" [Net: https://pypi.org/pypi/duckdb/json – åbnet].
  - DuckDB læser kun de kolonner, en forespørgsel skal bruge. Filtre skubbes ned i filen, så dele af filen springes over via "zonemaps" [Net: https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/current/data/parquet/overview.md – åbnet, linje 204–206].
  - Mapper opdelt efter nøgle (fx `koersel=17/filter=F0001/`) springes helt over, når man filtrerer på nøglen [Net: …/docs/current/data/partitioning/hive_partitioning.md – åbnet, "Filter Pushdown"].
  - DuckDB kan også læse og skrive direkte i en kørende PostgreSQL med `ATTACH … (TYPE postgres)`, også i skrivebeskyttet tilstand [Net: …/docs/current/core_extensions/postgres/overview.md – åbnet, linje 13 og 38]. Journal i PostgreSQL og signaler i Parquet kan derfor bruges i samme forespørgsel.
  - Begrænsning: kun én proces kan skrive i en DuckDB-databasefil ad gangen [Net: …/docs/current/connect/concurrency.md – åbnet, linje 13–18]. Det rammer os ikke, hvis hvert job skriver sin egen Parquet-fil og ingen deler en DuckDB-fil.
- **TimescaleDB** er en udvidelse til PostgreSQL med tidsopdelte tabeller og kolonnelager. Licensen er delt: koden uden for mappen "tsl" er Apache 2.0, koden i "tsl" (bl.a. kolonnelageret) er under "Timescale License" [Net: https://raw.githubusercontent.com/timescale/timescaledb/main/LICENSE – åbnet]. Der bygges og testes til Windows [Net: https://raw.githubusercontent.com/timescale/timescaledb/main/README.md – åbnet, badges linje 376–378].

### 1.2 Målt på vores egen datamængde
Jeg lavede 36,0 mio. syntetiske signalrækker: 38 filtre × 625 kombinationer × 1.516 signaler, altså 1/10 af høj-scenariet på 360 mio. pr. datasæt. Kolonnerne var de samme som i dag plus `bar_nr`. De blev gemt og forespurgt med DuckDB 1.5.5 og PyArrow 25.0.1 på 4 kerner [Målt].

| Format | Størrelse | Bytes/række | Skalering til 360 mio. rækker (ét datasæt) |
|---|---|---|---|
| CSV (som i dag) | 1.655 MB | 46,0 | ca. 16,6 GB |
| Parquet, snappy | 432 MB | 12,0 | ca. 4,3 GB |
| **Parquet, zstd** | **345 MB** | **9,6** | **ca. 3,4 GB** |
| PostgreSQL (regnet i v2, afsnit 2.3) | – | ca. 108 | ca. 38,9 GB |

| Forespørgsel (36 mio. rækker, Parquet zstd) | Tid |
|---|---|
| Ét filter, tal pr. kombination (625 rækker ud) | 0,04 s |
| Alle filtre, tal pr. kombination (23.750 rækker ud) | 1,1 s |
| Samme læsning af CSV | 3,4 s kun for at tælle |

Skrivetid: 7,4 s for 36 mio. rækker.

**Forbehold:**
- Data er tilfældige, ikke ægte signaler. Ægte data har mere struktur og pakker sandsynligvis *bedre*, men det er ikke bevist.
- Tallet for PostgreSQL er regnet, ikke målt her, fordi jeg ikke har en PostgreSQL-server. **SANDSYNLIGT** 10 gange mindre plads og mindst lige så hurtig analyse.
- CSV-tallet (46 B/række) passer med projektets egen måling: 114 MB for ca. 3 mio. linjer, altså 38 B [Projekt: BYGGEVEJLEDNING_RawSignal.md:320].

### 1.3 Hvad betyder det?
- Høj-scenariet med 30 datasæt: ca. **100 GB i Parquet** mod ca. **1,2 TB i PostgreSQL**.
- Backup bliver let. Parquet-filer ændres aldrig, så en kopi skal kun kopiere nye filer (afsnit 4).
- "Ryd op og start forfra" = slet mappen `koersel=17/`. Ingen DELETE og ingen VACUUM.
- Thomas' overblik pr. filter bevares: hver kørsel har én fil pr. filter, `koersel=17/filter=F0001.parquet`. Det er "én tabel pr. filter", som han valgte [Projekt: BESLUTNINGSLOG_2026-09-24.md:33], men nu også pr. marked og kørsel.
- Hver fils SHA-256 (et digitalt fingeraftryk) skrives i PostgreSQL, når filen er færdig. En fil uden fingeraftryk i databasen findes ikke for systemet. Det svarer til dagens regel om, at der kun skrives i databasen, når alt er godkendt [Projekt: database.py:39-53].

### 1.4 Vurdering

| Værktøj | Løser | Modenhed/licens | Arbejde | Risiko | Dom |
|---|---|---|---|---|---|
| Parquet + DuckDB | Datamængde (v2 afsnit 2), oprydning, backup | Stabil, MIT/Apache | Lille: pyarrow skriver, duckdb læser | Filer kan slettes ved en fejl. Løses med fingeraftryk + backup | **BRUG NU** |
| PostgreSQL med skuffer | Samme | Stabil | Mellem | 10× plads, langsom oprydning | **Reserve** |
| TimescaleDB | Samme | Stabil, men delt licens | Udvidelse på serveren + opdateringer | Endnu en ting, der skal passe til PostgreSQL 18. Licensen skal læses af Thomas | **NEJ** (løser intet, Parquet ikke løser) |

---

## 2. Kø og orkestrering

**Hvad er det?** En *kø* er listen over opgaver, som maskinerne tager fra. En *orkestrator* er et større system, der styrer rækkefølge, tidsplaner, genforsøg og har egen hjemmeside til overvågning.

| Værktøj | Hvad | Windows | Licens/modenhed | Vurdering |
|---|---|---|---|---|
| **Egen `SKIP LOCKED`-tabel** (v2 afsnit 4.4) | Ca. 50 linjer Python + én tabel | Ja (ren PostgreSQL) | – | Alt er synligt i én tabel, og Thomas' AI-assistent kan læse det hele. Genforsøg, livstegn og "3 fejl → stop" skal skrives selv. |
| **pgqueuer** 1.4.0 | Python-kø i PostgreSQL: `FOR UPDATE SKIP LOCKED` og `LISTEN/NOTIFY`, så jobs vækker arbejderen med det samme; genforsøg [Net: https://raw.githubusercontent.com/janbjorge/pgqueuer/main/README.md – åbnet, linje 15–16, 141] | "OS Independent" [Net: https://pypi.org/pypi/pgqueuer/json – åbnet] | MIT, Production/Stable | Samme princip som den egne tabel, færdigskrevet. Én ekstra afhængighed. |
| **procrastinate** 3.10.0 | Python-kø i PostgreSQL 13+, med genforsøg, låse og periodiske jobs [Net: https://raw.githubusercontent.com/procrastinate-org/procrastinate/main/README.md – åbnet] | Ikke nævnt. **UKENDT** | MIT, stabil, men "looking for additional maintainers" (samme README) | Risiko for, at projektet går i stå. |
| **Prefect** 3.8.7 / **Dagster** 1.13.24 | Orkestratorer med egen server og hjemmeside [Net: pypi JSON for begge – åbnet] | Ikke bekræftet | Apache 2.0 | Kraftige, men en ekstra server, egne begreber og hyppige hovedversioner. For meget for én ejer. |
| **Airflow** 3.3.2 | Stor orkestrator | **Nej.** "Airflow currently can be run on POSIX-compliant Operating Systems … On Windows you can run it via WSL2 … only Linux-based distros as 'Production'" [Net: https://raw.githubusercontent.com/apache/airflow/main/README.md – åbnet, linje 120–125] | Apache 2.0 | Udelukket på Thomas' Windows-server. |

**Dom:**
- **BRUG NU: egen tabel.** pgqueuer er et godt alternativ, hvis den, der bygger, hellere vil bruge færdig kode. Begge bruger den samme mekanisme (`SKIP LOCKED`), så valget kan ændres senere uden nyt design.
- **NEJ til Prefect/Dagster/Airflow nu.** Kædens rækkefølge er fast (led 1 → 5). Det kan en kolonne `led` og reglen "et led starter først, når det forrige er færdigt" klare [Antagelse: orkestratorer betaler sig ved mange forskellige og skiftende arbejdsgange; her er der én].
- **TradeStation-flaskehalsen løses ikke af noget af dette** (v2 afsnit 4). Det er fjernstyringen af TradeStation, der er svær, ikke køen.

---

## 3. Reproducerbarhed og forsøgsregister

| Værktøj | Hvad | Passer det? | Dom |
|---|---|---|---|
| **MLflow** 3.16.1 (Apache 2.0) | Logger "eksperimenter": parametre, tal og filer pr. kørsel, med egen hjemmeside [Net: https://pypi.org/pypi/mlflow/json – åbnet] | Bygget til maskinlæring. README'en handler nu mest om GenAI og sporing [samme kilde]. Vores forsøg er 1,5–9,5 mio. rækker (K1 afsnit 3.1). Ét MLflow-"run" pr. forsøg er for tungt, og tallene skal alligevel ligge i PostgreSQL, så K1 kan tælle dem med SQL. | **NEJ** |
| **DVC** 3.67.1 (Apache 2.0, "Beta") | "Git for data": versionerer store filer og pipelines ved siden af git [Net: https://pypi.org/pypi/dvc/json – åbnet] | Ville versionere Parquet- og prisfiler. Men fingeraftryk i PostgreSQL + filer, der aldrig ændres, giver det samme med ét værktøj mindre. DVC er også "Beta". | **SENERE** (hvis filerne skal deles mellem flere steder) |
| **Egne tabeller** (`forsoegsregnskab`, `filter_forloeb`, `koersel`, fingeraftryk) | Alt i PostgreSQL | Dækker K1's F3 (N_rå talt, N_eff målt) og Det Runde Bords krav (afsnit 7). Én backup og ét sted at kigge. | **BRUG NU** |
| **pandera** 0.33.1 (MIT, stabil) | Regler for en tabel, fx "kolonnen må ikke være negativ" [Net: https://pypi.org/pypi/pandera/json – åbnet, README-eksempel med `DataFrameSchema` og `Check`] | Til CSV-indlæsning: typer, `AntalBars ≥ 1`, `Afsluttet ∈ {0,1}`, `RunID` = filnavn, stigende `Starttid` pr. kombination. | **BRUG NU** |
| **Great Expectations** 1.23.2 (Apache 2.0) | Stor ramme for datakvalitet med rapporter [Net: https://pypi.org/pypi/great-expectations/json – åbnet] | Kan det samme som pandera, men har egen projektstruktur og konfiguration. For meget her. | **NEJ** |

**"For kort fil" (v2 fund 1.2 I) fanges ikke af pandera alene.** Det kræver tre tjek mod det forventede:
1. Antal forskellige (N1, N2) i filen = antal kombinationer udregnet fra Fra/Til/Step, minus dem, der aldrig kan tænde. Ved filter 1 manglede præcis 5 af 625, og det kan forklares [Projekt: BESLUTNINGSLOG_2026-09-24.md:88-91].
2. Seneste `Starttid` ligger inden for få bars af datasættets slutdato.
3. Hvis filen er ens med en tidligere kørsel af samme filter, datasæt og kodeversion (samme fingeraftryk), skal den give præcis samme tal. Det er K2's "dobbeltkørsel".

Tjekkene er regler i én fast fil og køres før indlæsningen. Fejler et tjek, får jobbet status `failed` (teknisk) og køres forfra.

---

## 4. Backup og drift

Serveren er Windows: stierne er `C:\…`, og der bruges `psql.exe` fra PostgreSQL 18 [Projekt: Automation/run-batch.ps1:22; Program/faelles.py:13].

| Værktøj | Windows | Vurdering | Dom |
|---|---|---|---|
| **pg_dump** (følger med PostgreSQL) | Ja | Giver et øjebliksbillede, der hænger sammen, og blokerer ikke andet arbejde [Net: https://raw.githubusercontent.com/postgres/postgres/master/doc/src/sgml/backup.sgml – åbnet i runde 2]. Når signalerne ligger i Parquet, er databasen lille (journal, pas, status, edge-tal ≈ få GB), og en nattelig dump tager minutter [Antagelse: størrelse regnet i v2 FORSLAG I]. | **BRUG NU** |
| **pgBackRest** 2.59.2 | Ingen indbygget Windows-udgave fundet. Der er et åbent ønske om at porte den [Net, ikke bekræftet: søgeuddrag "Windows support? · Issue #2431"] | Stærkt værktøj til store databaser med løbende arkivering [Net: https://raw.githubusercontent.com/pgbackrest/pgbackrest/main/README.md – åbnet]. Kræver Linux. | **NEJ** (på denne server) |
| **Barman** 3.20.0 | Nej: klassificeret som "POSIX :: Linux / BSD / Unix", GPL-3.0 [Net: https://pypi.org/pypi/barman/json – åbnet] | Samme som pgBackRest. | **NEJ** |

**Protokollen (enkel, på Windows):**
1. **Hver nat kl. 02:13** (Windows Opgavestyring, altså den indbyggede Task Scheduler) kører en .bat-fil:
   - `pg_dump -Fc TradingDB` til en anden disk.
   - `robocopy /E` af Parquet-mappen og fil-lageret (.el/.csv) til samme disk. Filerne ændres aldrig, så kun nye kopieres.
   - Én linje i `fabrik.haendelse` med størrelse, antal filer og om det lykkedes.
2. **Hver uge** kopieres det til en disk uden for huset eller en krypteret sky-mappe. Thomas vælger (v2 åbent punkt 9).
3. **Hver måned** gendannes nattens dump automatisk i `TradingDB_test`. Rækker tælles i de vigtigste tabeller, og 10 tilfældige Parquet-filer tjekkes mod deres fingeraftryk. Resultatet skrives i `haendelse`.
4. **Overvågning:** TradingApp-fanen viser en lampe. Den er rød, hvis der ikke er en vellykket backup de seneste 26 timer, hvis den månedlige gendannelsesprøve fejlede, eller hvis disken er over 80 % fuld. Der er ikke brug for et overvågningsprogram. Lampen læser `haendelse`.
5. **Senere**, når der handles live: løbende arkivering (PITR, gendannelse til et bestemt tidspunkt) med PostgreSQL's egne værktøjer [samme backup.sgml, afsnit "Continuous Archiving"].

---

## 5. Betjeningsflade (TradingApp-fanen)

| Værktøj | Hvad | Plus | Minus | Dom |
|---|---|---|---|---|
| **NiceGUI** 3.17.1 (MIT) | Knapper, tabeller og dialoger i browseren, skrevet i Python. "Great for micro web apps, dashboards" [Net: https://pypi.org/pypi/nicegui/json – åbnet] | Normal knap-logik: et tryk kører én funktion. Let at forstå for en AI-assistent og en ikke-programmør. Kan vise live-log. | Mindre udbredt end Streamlit | **BRUG NU** |
| **Streamlit** 1.64.0 (Apache 2.0) | Dataapps i browseren [Net: https://pypi.org/pypi/streamlit/json – åbnet] | Meget udbredt, flotte tabeller og grafer | Hele siden køres forfra ved hvert klik [Antagelse: kendt Streamlit-model, ikke læst i denne runde]. Knapper, der starter lange jobs, bliver drilske. | **SENERE** (til rene oversigter) |
| **Textual** 8.2.8 (MIT) | Brugerflader i terminalen eller browseren; Windows 10 understøttet [Net: https://pypi.org/pypi/textual/json – åbnet] | Let og hurtig | Terminal-look. Thomas kan ikke indsætte tekst i prompten og bruger .bat-filer [Projekt: BESLUTNINGSLOG_2026-09-24.md:129-130], så en browserside med store knapper er mere venlig. | **NEJ** |

**Råd:**
- Fanen kun **læser** fra PostgreSQL og **lægger jobs** i køen. Den kører aldrig selv TradeStation.
- De få knapper, der ændrer noget (Lås metodefil, Kassér kørsel, Godkend SQL), viser først den præcise tekst og kræver et ekstra "Ja".
- Fanen startes af en .bat-fil på skrivebordet.

---

## 6. Hvad der skal stå i den versionerede metodefil (til K1 og Thomas)

Det Runde Bord kræver, at Lag A-listen, plateau-grænsen og minimum antal signaler pr. celle ligger i en versioneret metodefil, der skrives *før* første filter køres [Projekt: Det Runde Bord-sammenfatning, Del 4 pkt. 1]. Min `regelsaet`-tabel fra v2 bliver til denne fil:
- **Filen** ligger i git (fx `Metode/metode_v1.json`). Git holder styr på historikken.
- **Databasen** har `fabrik.metode_version` med versionsnummer, filens SHA-256, hele indholdet som jsonb og tidspunktet for låsning. Hver kørsel, hvert filter-forløb og hvert pas peger på én metodeversion.
- **Indhold** (K1 og Thomas bestemmer tallene, jeg bestemmer kun pladsen):
  - Lag A-opdelinger
  - minimum signaler pr. celle
  - plateau-trappe og dvale-grænse
  - Almgrens krav i Lag B: minimum forbedring efter omkostninger, sat på forhånd
  - omkostningsmodel
  - grænser for out-of-sample og embargo
  - inkubationsregel: minimum uger, minimum handler, krav for at gå live, og hvad der sker ellers
- Et felt, der ikke er udfyldt, betyder "ikke afgjort". Så går intet videre. Det gælder især inkubationsreglen (Det Runde Bord, Del 6).

---

## 7. Datamodellen efter Det Runde Bord

*Afgjort af Thomas og ikke genåbnet her: et filter, der fejler, er endeligt dødt; der valideres out-of-sample; der er en inkubationstid [Projekt: Det Runde Bord-sammenfatning, Del 1–3]. Nedenfor er kun datamodel og statusser. Selve handelsudførelsen er uden for opgaven.*

### 7.1 Filterets identitet (så et dødt filter ikke kommer igen)

```sql
-- FORSLAG R1: identitet = formel + parameterinterval + instrument + tidsramme
CREATE TABLE fabrik.filter_identitet (
    identitet_id    bigserial PRIMARY KEY,
    filter_uid      uuid NOT NULL, filter_version int NOT NULL,
    formel_norm     text NOT NULL,       -- formlen normaliseret: uden mellemrum, store/små bogstaver ens
    formel_norm_sha256 text NOT NULL,
    n1_interval     numrange, n2_interval numrange,   -- fx [5,125]
    instrument      text NOT NULL,       -- fx '@ES'
    workspace       text NOT NULL,       -- fx '5,10,60'
    UNIQUE (formel_norm_sha256, n1_interval, n2_interval, instrument, workspace)
);
-- Ekstra spærring: en ny identitet med SAMME normaliserede formel, instrument og workspace,
-- hvis interval OVERLAPPER et rejected filters interval, afvises (EXCLUDE-regel eller trigger).
```

**Ærlig grænse:**
- Et fingeraftryk fanger kun formler, der er ens tegn for tegn efter normalisering, samt overlappende intervaller.
- `C > Average(C,N1)` og `Close > Average(Close,N1)` betyder det samme, men ser forskellige ud. Det kræver en regel, der oversætter til en fast form (K2's klassifikation kan gøre det), eller en menneskelig kontrol. **UKENDT**, hvor tæt det kan lukkes.

### 7.2 Statusser: `failed` og `rejected`

```sql
-- FORSLAG R2: ét forløb pr. filter-identitet pr. metodeversion. Kun tilføje.
CREATE TABLE fabrik.filter_forloeb (
    forloeb_id      bigserial PRIMARY KEY,
    identitet_id    bigint NOT NULL REFERENCES fabrik.filter_identitet,
    metode_version  int NOT NULL REFERENCES fabrik.metode_version,
    status          text NOT NULL CHECK (status IN
                    ('ny','igang','bestaaet_gate','bestaaet_oos','bestaaet_embargo',
                     'inkubation','live_klar','rejected')),
    doedsaarsag     text CHECK (doedsaarsag IN ('gate','oos','embargo','inkubation')),
    antal_lagb_tests int NOT NULL DEFAULT 0,   -- Lag B: tal, talt af databasen fra fabrik.lagb_test
    opdateret       timestamptz NOT NULL DEFAULT now(),
    UNIQUE (identitet_id, metode_version),
    CHECK ((status = 'rejected') = (doedsaarsag IS NOT NULL))  -- rejected SKAL have en årsag
);

-- Teknisk fejl hører til jobbet, ikke filteret:
--   fabrik.job.status IN ('venter','koerer','faerdig','failed')  -> failed må køres igen
--   fabrik.filter_forloeb.status = 'rejected'                    -> aldrig igen
```

- **`failed`** er en egenskab ved et *job* (maskine gik ned, fil ikke skrevet, CSV-tjek fejlede). Jobbet lægges i kø igen, præcis som i v2.
- **`rejected`** er en egenskab ved *filter-forløbet*. Det er endeligt. Rækken slettes aldrig. Den er "nævneren" [Projekt: Det Runde Bord-sammenfatning, Del 2 pkt. 2].
- **Overgange håndhæves af en trigger** (en regel, som databasen selv kører ved hver ændring). Kun de lovlige skridt er mulige:
  - `ny → igang → bestaaet_gate → bestaaet_oos → bestaaet_embargo → inkubation → live_klar`
  - Fra hvert trin kan status gå til `rejected`.
  - **Fra `rejected` kan intet.**
- Programmerne har ingen `DELETE`-ret på tabellen (rollerne fra v2 afsnit 3.3).

### 7.3 Lag C håndhævet teknisk
Tre låse, så det ikke afhænger af, at nogen husker reglen:
1. **Køen:** en trigger på `fabrik.job` afviser ethvert nyt job for et filter-forløb med status `rejected`. En maskine kan derfor ikke genstarte det.
2. **Analyser:** Lag B-tabellen `fabrik.lagb_test` tillader kun rækker for forløb med status mindst `bestaaet_gate`. EdgeFinder og EdgeCruncher læser signaler gennem visninger, der udelukker `rejected`.
3. **Roller:** kun rollen `fabrik_dommer` kan sætte `rejected` eller skrive lag-domme. Rollen `fabrik_arbejder` kan ikke ændre status (v2 afsnit 3.3).

**Åbent punkt, som konflikter i bordets egen tekst:** "rejected … må aldrig hentes igen af nogen maskine" (Del 2 pkt. 1) og "ændres Lag A-listen … skal ALLE filtre køres om, også de døde" (Del 2 pkt. 5).
- Mit forslag til, hvordan begge kan holde: den gamle dom røres aldrig. Genkørslen er et *nyt* forløb under en *ny* metodeversion (derfor `UNIQUE (identitet_id, metode_version)`). Det tæller som nye forsøg.
- **Men Thomas skal afgøre, om et filter, der er dødt under metode v1 og består under v2, må leve videre.** Det afgør jeg ikke.

### 7.4 De fire datalag – én gang hver, i rækkefølge

```sql
-- FORSLAG R3: erstatter datadeling/pengeskab fra v2
CREATE TABLE fabrik.datalag (
    lag       text PRIMARY KEY CHECK (lag IN ('in_sample','out_of_sample','embargo','inkubation')),
    raekkefoelge smallint NOT NULL UNIQUE,   -- 1,2,3,4
    fra_dato  date NOT NULL,                 -- in_sample 2020-01-01, out_of_sample 2025-01-01
    til_dato  date,                          -- embargo: Thomas fastsætter; inkubation: åben (fremtid)
    laast     timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE fabrik.lag_brug (             -- hver række = "dette forløb har rørt dette lag"
    forloeb_id bigint NOT NULL REFERENCES fabrik.filter_forloeb,
    lag        text   NOT NULL REFERENCES fabrik.datalag,
    brugt      timestamptz NOT NULL DEFAULT now(),
    bestaaet   boolean NOT NULL,
    resultat   jsonb NOT NULL,
    PRIMARY KEY (forloeb_id, lag)            -- ÉN gang pr. lag pr. forløb
);
-- Trigger: en række for lag nr. k afvises, medmindre lag nr. k-1 findes for samme forløb
-- med bestaaet = true. Samme trigger sætter status (bestaaet_... eller rejected + årsag).
```

- Når pengeskabet (v2's F9) bliver til `embargo`, bliver K1's tredeling (udvikling, validering, pengeskab) til bordets fire lag: in-sample, out-of-sample, embargo og inkubation.
- **Datoerne for embargo er ikke afgjort.** Bordet siger kun "låst historik". Thomas fastsætter dem.
- **Antal filtre, der har rørt 2025** er en visning: `SELECT count(DISTINCT identitet_id) … WHERE lag = 'out_of_sample'`. Hver gang den stiger, skrives et øjebliksbillede i `haendelse` [Projekt: Det Runde Bord-sammenfatning, Del 3 og Del 4 pkt. 3].
  - Hvad der skal ske, når tallet er højt (hæve kravet eller flytte dommen), er bordets uenighed mellem López de Prado og Kaufman (Del 5). Den bliver stående. Tallet står i metodefilen.
- **Ét forbehold om `lag_brug`:** Databasen kan kun håndhæve det, der går gennem den. Et menneske eller en AI, der åbner 2025-data i Excel, registreres ikke. Derfor bør prisfilerne pr. lag ligge i hver sin mappe. Mappen for out-of-sample og embargo kan kun læses af den konto, som dommer-jobbet kører under [Antagelse: Windows-filrettigheder er den enkleste lås uden for databasen].

### 7.5 Lag B – antal tests som tal

```sql
-- FORSLAG R4
CREATE TABLE fabrik.lagb_test (
    forloeb_id  bigint NOT NULL REFERENCES fabrik.filter_forloeb,
    kolonne     text NOT NULL,              -- fx 'volatilitet_20', 'tid_paa_dagen'
    graense     text NOT NULL,              -- fx '> 1.5', '09:30-11:00'
    lag         text NOT NULL CHECK (lag = 'in_sample'),   -- Lag B KUN på in-sample
    netto_foer  numeric, netto_efter numeric,  -- efter slippage og kommission (Almgren)
    signaler_foer int, signaler_efter int,
    godkendt    boolean,                    -- efter metodefilens på forhånd satte grænse
    oprettet    timestamptz NOT NULL DEFAULT now()
);
-- filter_forloeb.antal_lagb_tests = count(*) fra denne tabel (vedligeholdes af trigger),
-- og indgår i forsøgsregnskabets N_rå.
```

### 7.6 Inkubation

```sql
-- FORSLAG R5
CREATE TABLE fabrik.inkubation (
    inkubation_id  bigserial PRIMARY KEY,
    strategi_uid   uuid NOT NULL, version int NOT NULL,
    strategi_sha256 text NOT NULL,          -- fingeraftryk af kode + parametre + udgangsregler
    metode_version int NOT NULL REFERENCES fabrik.metode_version,
    startet        timestamptz NOT NULL DEFAULT now(),
    antal_handler  int NOT NULL DEFAULT 0,  -- opdateres af trigger fra inkubation_handel
    status         text NOT NULL DEFAULT 'koerer'
                   CHECK (status IN ('koerer','nulstillet','bestaaet','rejected')),
    FOREIGN KEY (strategi_uid, version) REFERENCES fabrik.dvale_strategi
);

CREATE TABLE fabrik.inkubation_handel (
    inkubation_id bigint NOT NULL REFERENCES fabrik.inkubation,
    tid           timestamptz NOT NULL,
    retning       smallint NOT NULL,
    signalpris    numeric NOT NULL,
    fillpris      numeric NOT NULL,          -- rigtig udførelse
    slippage      numeric GENERATED ALWAYS AS (signalpris - fillpris) STORED,  -- samme definition som backtest
    kommission    numeric NOT NULL
);
```

- **"Enhver ændring nulstiller uret" håndhæves teknisk.**
  - En strategi i dvale kan ikke ændres, fordi der kun tilføjes (v2 afsnit 3.1). En ændring er altså en ny `version` med nyt `strategi_sha256`.
  - En trigger sætter den gamle inkubation til `nulstillet` og starter en ny med `startet = now()` og `antal_handler = 0`.
  - Det, der kører live-simuleringen, skal ved hver handel melde sit `strategi_sha256`. Passer det ikke med inkubationens, afvises handlen, og uret nulstilles.
- **Systemet åbner for live, ikke et menneske.** Et planlagt job (fx hver time) sætter `live_klar`, når tid, antal handler og resultat opfylder metodefilens inkubationsregel. Rollen `thomas_admin` har *ikke* ret til at sætte `live_klar`. Er reglen ikke udfyldt (bordets Del 6), bliver ingen strategi nogensinde `live_klar`.
- Inkubation og live ligger delvist uden for den oprindelige opgave. Her er kun statusser og tabeller. Hvordan ordrer sendes, er ikke designet.

### 7.7 Prisdata fra start – hvad koster det?
Lag B skal kunne køre uden nye backtests, så prisdata skal gemmes [Projekt: Det Runde Bord-sammenfatning, Del 4 pkt. 2]. Regnet trin for trin [Antagelse: futures handlet ca. 23 timer × 250 dage om året; 2020 til og med 2026 = 7 år]:

| Tidsramme | Bars pr. marked (7 år) |
|---|---|
| 5 min | 23 × 60 / 5 × 250 × 7 = 483.000 |
| 10 / 20 / 30 min | 241.500 / 120.750 / 80.500 |
| 60 / 120 min | 40.250 / 19.250 |
| **De 6 tidsrammer i de 4 workspaces i alt** | **ca. 985.000** |
| 1 min (hvis man vil kunne danne andre tidsrammer selv) | 2.415.000 |

- Med ca. 25 bytes pr. bar i Parquet (OHLCV) [Antagelse: tid + 4 priser + volumen pakket; ikke målt] bliver det **ca. 25 MB pr. marked** for de 6 tidsrammer og **ca. 60 MB** med 1-minut. I PostgreSQL med ca. 80 B/række er 1-minut ca. 190 MB.
- **Konklusion: pladsen er ubetydelig** i forhold til signalerne (3,4 GB pr. datasæt).
- **Det svære er ikke pladsen, men at eksportere de *samme* bars, som TradeStation regnede på**: samme session, samme tidszone og samme justering af kontraktskift. Derfor bør bars eksporteres fra TradeStation pr. workspace sammen med facit-backtesten og gemmes med fingeraftryk (v2 afsnit 5.3).
- En 1-minut-serie, som Python selv samler til 5, 10 … minutter, skal bevises ens med TradeStations egne bars, før den må erstatte dem. **UKENDT**, om det lykkes ved sessionsgrænser.
- Prisfilerne lægges i én mappe pr. datalag (afsnit 7.4).

---

## 8. Nye åbne punkter til Thomas

1. Må et filter, der er `rejected` under metode v1, leve videre, hvis det består under en ny metodeversion? (Konflikten i afsnit 7.3.)
2. Datoerne for embargo-laget.
3. Inkubationsreglen som tal: minimum uger, minimum handler, krav for at gå live, og hvad der sker ellers (bordets Del 6). Uden den bliver ingen strategi `live_klar`.
4. Hvor tæt skal "samme filter i ny forklædning" fanges? Kun ens formler og overlappende intervaller (afsnit 7.1), eller også en regel, der oversætter formler til en fast form?
5. Må out-of-sample- og embargo-prisdata ligge i mapper, som kun dommer-jobbet kan læse?
6. Egen kø-tabel eller pgqueuer (begge samme princip)?
7. NiceGUI til fanen?
8. Råsignaler i Parquet i stedet for PostgreSQL? Det ændrer, hvor "én tabel pr. filter" ligger (én fil pr. filter pr. kørsel).

## 9. Uenigheder
- **Mig mod bordets ordlyd:** "Aldrig hentes igen" og "kør alle om ved ny metode" kan kun begge holde, hvis genkørslen er et nyt forløb. Thomas afgør, hvad et nyt "bestået" betyder.
- **Mig mod K2 (fra v2):** Python som hovedregnemaskine. Nu med facit pr. workspace-type (K2's indvending er taget med), men stadig ikke EasyLanguage hele vejen.
- **Mig mod en mulig ønskeliste om orkestratorer:** Jeg anbefaler ingen (afsnit 2).

## 10. Kilder, jeg selv har åbnet i denne runde
- PyPI JSON: duckdb, pyarrow, procrastinate, pgqueuer, prefect, dagster, apache-airflow, mlflow, dvc, pandera, great-expectations, streamlit, nicegui, textual, barman (https://pypi.org/pypi/<pakke>/json)
- https://raw.githubusercontent.com/apache/airflow/main/README.md
- https://raw.githubusercontent.com/pgbackrest/pgbackrest/main/README.md
- https://raw.githubusercontent.com/timescale/timescaledb/main/README.md og …/LICENSE
- https://raw.githubusercontent.com/procrastinate-org/procrastinate/main/README.md
- https://raw.githubusercontent.com/janbjorge/pgqueuer/main/README.md
- https://raw.githubusercontent.com/duckdb/duckdb-web/main/docs/current/data/parquet/overview.md, …/data/partitioning/hive_partitioning.md, …/connect/concurrency.md, …/core_extensions/postgres/overview.md
- Fra runde 2: PostgreSQL storage.sgml, ddl.sgml, backup.sgml, datatype.sgml (raw GitHub)
- Egen måling: DuckDB 1.5.5 + PyArrow 25.0.1, 36 mio. syntetiske rækker (scratchpad r3/bench.py)
- Kun søgeuddrag (ikke bekræftet): pgBackRest "Windows support? · Issue #2431"

**Hvad der mangler:**
- Ingen måling på ægte signaldata og ingen PostgreSQL-måling.
- Prefect/Dagster på Windows er ikke bekræftet.
- Hvor godt "samme filter i ny forklædning" kan fanges, er ukendt.
- Selve handelsudførelsen i inkubationen er ikke designet (uden for opgaven).


---

## 7.8 Tilføjet efter kritikrunden (K1 §3.2 og K2 §4.6)

**Filter-identitet (erstatter `numrange` i FORSLAG R1, efter K2 §4.6):**
- `formel_trae_norm` (text): parserens faste form. Store/små bogstaver ens, ingen mellemrum, parametre som P1/P2, `a < b` = `b > a`.
- `param_maengde_n1` og `param_maengde_n2` (numeric[]): Fra/Til/Step *udfoldet*, sorteret.
- `instrument` (rodsymbol + kontinuitetstype + sessionsskabelon).
- `tidsrammer` (Data1/Data2/Data3).
- `identitet_sha256` = SHA-256 af de fire, UNIQUE.
- Overlap-spærringen bruger array-operatoren `&&` (overlap) på parametermængderne. Hvis formel-træ, instrument og tidsrammer er ens, og mængderne overlapper et `rejected` filter, afviser en trigger rækken, og generatoren stopper med ByggeFejl. Et træ, der ligner, men ikke er ens, giver kun en advarsel i `haendelse` (K2).

**Status `venter` og F1-spærring (K2 §4):**
- `filter_forloeb.status` får værdien `'venter'` (gruppe A/C/D, der ikke er bygget om).
- Triggeren på `lag_brug` afviser `in_sample`, medmindre filterets `f1_kontrolstatus = 'bestaaet'` (K0–K6).
- Et filter i `venter` kan derfor ikke få en Lag A-dom og kan ikke blive `rejected` på forkerte tal.
- Hver dom gemmer `git_commit` og `klassifikation_version`, så en dom, der er fældet under en senere fundet teknisk fejl, kan findes (K2's åbne punkt).

**Faste kolonner i `dvale_pas`, præcis som K1 opstiller dem i sin §3.2.** Alle tilføjes:
- `praeregistrering_id`, `workspace_id`, `marked`, `n1`, `n2`
- `retning`, `horisont`, `event_definition`, `indgang_regel`
- `opvarmning_bars`, `f1_kontrolstatus`, `hukommelsesfejl_status`
- `n_unikke_raekker_filter`, `n_raa`, `n_eff`, `n_eff_metode`, `t_vaerdi`
- `stepm_bestaaet`, `stepm_antal_modeller`, `dsr`, `sr_spredning_forsoeg`
- `plateau_niveau`, `plateau_metode`, `wf_t`, `wf_antal_kandidater`, `middel_dobbelt_omk`
- `f8_antal_aar`, `f8_negative_aar`, `f8_stoerste_aar_andel`
- `antal_handler`, `antal_handler_eff`, `sr_pr_handel`
- `pbo`, `skaevhed`, `kurtosis`, `max_drawdown`, `placebo_rate_koersel`, `indplantet_fundet_andel`

To ændringer i forhold til v2: `wf_t_samlet` hedder nu `wf_t` som hos K1, og `deflated_sharpe` hedder `dsr`. Enum-felterne (valgfelter) får CHECK-lister med K1's værdier. `plateau_niveau` forbliver et heltal uden loft (uenighed U4 er løst).

```sql
-- FORSLAG R6: genvækning (K1 v2 §11)
CREATE TABLE fabrik.genvaekning (
    strategi_uid     uuid NOT NULL,
    dato             date NOT NULL,
    nye_handler      int NOT NULL,
    welch_t          numeric,
    bayes_p_over_omk numeric,
    regime_ok        boolean,
    cusum_brud       boolean,
    beslutning       text NOT NULL CHECK (beslutning IN ('vaek','vent','udgaaet')),
    metode_version   int NOT NULL REFERENCES fabrik.metode_version,
    PRIMARY KEY (strategi_uid, dato)
);
```

**Talgrænser i metodefilen** (spejlet som kolonner i `fabrik.metode_version`, så de kan bruges i SQL):
- `t_graense`, `dsr_graense`, `stepm_alpha`, `fdr_q`, `pbo_graense`
- `placebo_max`, `indplantet_min`, `pengeskab_andel`, `genvaek_bayes_graense`
- Bordets egne felter: `lagA_min_signaler_pr_celle`, `plateau_graense`, `lagB_min_forbedring_efter_omk`, `oos_max_filtre_foer_skaerpelse`, `inkub_min_uger`, `inkub_min_handler`, `inkub_krav`, `inkub_ellers`

NULL betyder "ikke afgjort", og så går intet videre.

## 7.9 Hvad StepM og placebo kræver af lagring

- **StepM/SPA (K1 V3)** skal have en tabel med T dage × k varianter af daglige resultater efter omkostninger.
  - Regnet: in-sample 5 år ≈ 1.250 dage. Med K1's 84.476 varianter pr. workspace (efter sammenlægning af ens rækker) og float32 (4 bytes) bliver det 1.250 × 84.476 × 4 B ≈ **422 MB pr. workspace**. Uden sammenlægning (høj-scenariet 2,375 mio. varianter) bliver det ca. **11,9 GB**. Derfor skal ens rækker lægges sammen først, som K1 kræver.
  - **Råd:** Matrixen gemmes ikke fast. Den regnes igen fra Parquet-signalerne + de gemte prisbars + metodeversion. Det er deterministisk (giver hver gang samme resultat), og derfor skal kun disse gemmes: matrixens fingeraftryk, bootstrap-frø (seed), bloklængde og resultatet. En kopi i cache (fx `stepm/koersel=17/ws=1.parquet`) må gerne ligge, men den er ikke kilden.
- **Placebo (K1 V8)** er rigtige signalrækker forskudt et tilfældigt antal dage. Der skal ikke gemmes kopier af signaler. Kun `(kilde_filter, forskydning, seed)` gemmes i `fabrik.placebo`, og signalerne dannes igen efter behov. Indplantet edge: kun `(seed, edge_stoerrelse, bootstrap-parametre)`.
- **Følge for Parquet-lagringen:** næsten ingen ekstra plads. Det stiller til gengæld krav om, at prisbars gemmes fra start (afsnit 7.7) og aldrig ændres.


# Del 4 – Samlet overblik, version 3 (den overordnede agent)

*Jeg har ikke rettet i konsulenternes dele. Del 4 erstatter del 4 fra version 2. Punkter, der stadig gælder derfra, er taget med.*

## 4.1 Hvad version 3 ændrede

| Emne | Version 2 | Version 3 |
|---|---|---|
| Datalængde | Ukendt. Det vigtigste åbne spørgsmål | **5 år in-sample (2020–2024) + 2025 + embargo + inkubation** [Projekt: Det Runde Bord-sammenfatning] |
| Hvad kan findes | Formel og scenarier | **Årlig Sharpe ≳ 2,3–2,5 pr. marked. Ca. 1,6 med pooling over 6 markeder** (K1B §5.1) |
| Test for "mere end held" | t-grænse ud fra et gættet N_eff | **StepM (Romano-Wolf) fra `arch`.** Nabovarianternes lighed tages med automatisk, så N_eff ikke skal gættes (K1B V3) |
| Facit for indikatorer | "Uafhængig Python" | **Tre parter:** TradeStation uden løkke + Python efter TS' egen funktionskode + TA-Lib (K2B §1) |
| Advarselsliste | Navneliste med 10 funktioner | **Rigtig formel-parser (lark).** Sorterer alle 380 formler i gruppe A–E (K2B §2.5) |
| Råsignaler | PostgreSQL med skuffer | **Parquet + DuckDB.** 9,6 mod ca. 108 bytes pr. række, målt på syntetiske data (K3B §1) |
| EdgeFinder | Ikke godkendt. Ingen metode | **Protokol godkendt af K1 med ændringer** (K2B §4, K1's kritik runde 3) |
| Døde filtre | Ikke behandlet | **`failed` og `rejected` håndhæves i databasen.** Døde filtre er "nævneren" (K3B §7) |
| Inkubation | Ikke behandlet | **Tre gennemregnede beslutningsregler** til Thomas (K1B §5.5) |

## 4.2 Værktøjskassen samlet

Kun de anbefalede. Fravalgte værktøjer og begrundelser står i delene.

| Felt | Værktøj / protokol | Dom | Løser | Kilde læst af konsulenten |
|---|---|---|---|---|
| Statistik | `arch` StepM (+ SPA/MCS som supplement) | BRUG NU | "Er den bedste af mange bare held?" | Kildekode, `arch` 8.0.0, prøvekørt |
| Statistik | `arch` blok-bootstrap + optimal bloklængde | BRUG NU | Overlappende signaler (E3) | Kildekode |
| Statistik | `statsmodels` multipletests (Holm, BH, BY) | BRUG NU | Grovsortering og Lag A-celler | Kildekode, 0.15.0 |
| Statistik | Egen DSR/PSR/MinTRL (ca. 20 linjer) | BRUG NU | Tal i passet | Kontrolleret mod `pypbo`-kode (pakken selv fravalgt: AGPL) |
| Statistik | Placebo + indplantet edge i hver kørsel | BRUG NU | Kalibrerer Lag A, plateau, PBO og 2025-grænse | Prøvekørt |
| Disciplin | Hypotesekort, forsøgsregister, blind analyse, to-nøgle-regel (P1–P6) | BRUG NU | Skjulte forsøg og selvbedrag | Faglig standard [kilder ikke åbnet] |
| EasyLanguage | TA-Lib som tredje facit | BRUG NU | Uafhængig kontrol af indikatorer | C-kode læst (EMA, MACD, RSI, DI, ADX, CCI) |
| EasyLanguage | Formel-parser med `lark` | BRUG NU | Den ufuldstændige navneliste, gruppe A–E, filter-identitet | PyPI |
| EasyLanguage | Golden master (SHA-256) + differential testing | BRUG NU | F1: TS = Python | Faglig standard |
| EasyLanguage | 10 plantede fejl (manuel mutationstest) | BRUG NU | Beviser, at kontrollen virker | – |
| EasyLanguage | Egen enkel numpy-kode som Python-regnemaskine | BRUG NU | Signaler og afkast | vectorbt fravalgt (Commons Clause), backtrader fravalgt (GPLv3) |
| Data | Parquet + DuckDB til råsignaler | BRUG NU | Plads, fart, "slet én mappe = start forfra" | DuckDB-dokumentation på GitHub, målt |
| Data | PostgreSQL til journal, status, pas og kø | BRUG NU | Regler håndhævet af databasen | PostgreSQL-dokumentation |
| Data | Egen `SKIP LOCKED`-kø (eller pgqueuer) | BRUG NU | Fordeling over maskiner | README |
| Data | `pandera` + tjek af antal og slutdato | BRUG NU | For korte eller forkerte CSV-filer | PyPI |
| Drift | pg_dump + Opgavestyring + robocopy + månedlig gendannelsesprøve | BRUG NU | Backup | PostgreSQL-dokumentation |
| Betjening | NiceGUI-fane (Streamlit nr. 2) | BRUG NU, lille | Plug-and-play | PyPI |

**Min bemærkning:** Listen er bevidst kort. Den professionelle standard er ikke flest mulige værktøjer. Det er få, velforståede værktøjer, som kan kontrolleres. Det passer til en ejer uden kodeerfaring. Hvert værktøj, der ikke står her, er ét mindre at vedligeholde. [Antagelse]

## 4.3 Fase 0, opdateret: før den fulde kørsel analyseres

Det er råd, og Thomas beslutter. Rækkefølgen er valgt, så det billigste og mest afslørende kommer først. Nyt i v3 er markeret med ★.

| # | Hvad | Hvorfor | Hvor | Skøn | Fra |
|---|---|---|---|---|---|
| 0.1 | Fuld backup af TradingDB til en anden disk, læst tilbage i en testdatabase | Den eneste backup ligger i dag i samme database | Lokal | Timer | K3 §3.4, K3B §4 |
| 0.2 | ★ Læs TradeStations egen kode for XAverage, RSI, DMI, ADX, CCI og StandardDev i TDE (kun læsning), og notér typen (series/simple) og startreglen | Afgør gruppe A–E og hvordan startværdien er. Måske kan de 18 CCI-filtre flyttes til den sikre gruppe | Lokal, kun læsning | 1–2 timer | K2 §2.3, K2B §1.2 |
| 0.3 | ★ Formel-parser, der sorterer alle 380 filtre i gruppe A–E og læser Verify-advarslerne | Viser, hvor mange filtre der er i fare. I dag ved ingen det | Python | 1–2 dage at bygge | K2B §2.5 |
| 0.4 | Test T1 på filter 68 med Fra = Til mod en fil uden løkke | Afgør, hvordan MACD-fejlen virker | TradeStation, 2 kørsler | Under en time | K2 §2.2 |
| 0.5 | T1 pr. funktionstype (ca. 15–20) | Hvilke funktioner må blive i løkken | TradeStation | Ca. 1 dag | K2 §4 |
| 0.6 | ★ Skriv og lås **metodefilen** (version 1): Lag A-liste og -kriterium, minimum pr. celle, 2025-regel, test for "rejected" (StepM), retning og horisont, bloklængde, pakkeversioner | "Rejected er endeligt". Derfor skal reglerne ligge fast *før* første dom | Thomas + K1 | Beslutninger | K1B §5, K3B §6 |
| 0.7 | ★ Hypotesekort pr. filterfamilie (forhåndsregistrering) | Gratis og det stærkeste værn mod skjulte forsøg | Thomas | Timer | K1B P1 |
| 0.8 | Datamodel: filter-identitet (fingeraftryk), `failed`/`rejected`, fire datalag, kørsel, marked, journal med fejl og advarsler, roller i stedet for superbruger | Uden den kan kun ét marked gemmes, og Det Runde Bords regler kan ikke håndhæves | Thomas godkender SQL; bygges i test først | Dage | K3 v2 §3, K3B §7 |
| 0.9 | CSV bærer sin oprindelse (symbol, interval, session, bar-nummer) | En fil kan aldrig forveksles | Generator | Timer | K2 §1.7 |
| 0.10 | ★ Charts starter senest i 2017, og to-starts-testen køres | Lange udglatninger på 60- og 120-minutters data skal varmes op før 2020 | Lokal | Timer | K1's kritik runde 3 |
| 0.11 | ★ Eksportér og gem prisbars (IS, 2025 og embargo i separate, låste mapper) med fingeraftryk | StepM, placebo og Lag B kan så genskabes uden nye backtests. Fylder ca. 25–60 MB pr. marked | Lokal | Timer | K3B §7.7 |
| 0.12 | ★ Plant 10 kendte fejl og kontrollér, at kontrolplanen fanger dem alle | En kontrol, der aldrig har fanget en fejl, er ikke bevist | Test-miljø | 1 dag | K2B §2.4 |
| 0.13 | Spørg TradeStation skriftligt om samtidige logins | Afgør, om der kan bruges flere TradeStation-maskiner | Thomas | Én e-mail | K3 §4.1 |

**Vigtigste nye pointe (K2B §4.0):** Et filter er endeligt dødt, når det fejler. Så må **ingen Lag A-dom falde, før F1 og kontrolplanen er bestået for filteret**. En dom fældet på forkerte tal kan ellers aldrig rettes. MACD-filtrene står derfor som `venter`, ikke `rejected`. Afgørelsen genåbnes ikke. Kravet beskytter den.

## 4.4 EdgeFinder-protokollen: status

- **Skrevet af K2** (K2B §4) på grundlag af Det Runde Bords Lag A, B og C og de fire datalag.
- **Godkendt af K1 med ændringer** (bilag: K1's kritik runde 3):
  - Dommen træffes på råt nettoafkast, med kontrolgruppe-justering som ekstra krav.
  - StepM er grænsen for "rejected".
  - Walk-forward (E5) tilføjes.
  - Minimum pr. celle er (1,28/δ)².
  - Opvarmningen regnes pr. datastrøm.
  - Lag B bruger "filteret uden kolonnen" som benchmark.
- **Indarbejdet af K2:** Alle 10 ændringer er indarbejdet, og K2 er fagligt enig i dem alle. Der er ingen uenighed tilbage om protokollen. Status står øverst i K2B §4: "godkendt af K1 med ændringer, indarbejdet 2026-09-28".
- **Mangler før brug:** Thomas' valg i metodefilen (0.6) og en prøvekørsel på placebo og indplantede edges (K2B §4.8).

## 4.5 Enighed og uenighed

**Løst i runde 3:** EdgeFinder-protokollen (K2 har indarbejdet alle K1's krav). Placebo i egen StepM. Lag A-minimum (K2 følger K1). Facit pr. workspace-type (K3 følger K2). Faste pas-kolonner N_rå, N_eff, t og walk-forward-t (K3 følger K1). Max Bars Back-testen er erstattet af to-starts-testen (K1 følger K2). MACD vej a (alle).

**Står stadig åbne:**

| # | Emne | Synspunkter | Min vurdering |
|---|---|---|---|
| U1 | **Kan et filter, der er "rejected" under metode v1, leve, hvis det består under v2?** | Bordet siger både "aldrig igen" og "ved ny metode køres alle om". K3: genkørsel = et nyt forløb. K1: kun forsvarligt, hvis v2 er låst før resultaterne ses, køres på *alle* filtre, og forsøgene lægges sammen | En reel modstrid i Det Runde Bords egen tekst. **Kun Thomas kan afgøre den** |
| U2 | Placebo: samme StepM-familie som de ægte eller egen? | **Løst:** placebo køres gennem sin egen StepM med samme indstillinger. Højst 1 ud af 20 sæt må give fund (K1 og K2 enige) | – |
| U3 | Retning og horisont: låses på forhånd? | K2: skal låses, ellers bliver StepM-matrixen 10 gange større (8,4 GB). K1 har ikke taget endelig stilling | Hører til metodefilen (0.6) |
| U4 | Fingeraftryk af Parquet | K3 hasher filen. K2: filen er ikke stabil på tværs af versioner, så hash rå CSV + et indholds-fingeraftryk | K2's argument er stærkest [Antagelse] |
| U5 | Parser-version og identitet | K3: parserens version gemmes, og alle fingeraftryk regnes om ved ny version, også de døde | Bør følges, ellers kan et dødt filter "slippe ud" |
| U6 | Navnet `pengeskab_andel` | K3: omdøb til embargo, så passet følger de fire lag | Mindre punkt |
| U7 | Genvækning: system eller menneske? | K3: bordet vil have, at systemet åbner for live. Det samme bør gælde genvækning | Thomas afgør |
| U8 | Placebo: test eller produktion? Kontrolresultater? | Uændret fra v2 (K1/K2 mod K3) | Thomas fortolker reglen "test blandes ikke med produktion" |
| U9 | Automatisk skrivning i databasen | Uændret fra v2 | Thomas afgør. Ellers kan fabrikken ikke være automatisk |
| U10 | Kaufman mod López de Prado (Lag A-bredde, 2025 som dom) | K1: begge risici kan *måles* med placebo og indplantede edges, før listen låses. R2 + I2 er en mulig middelvej | Står åben efter Thomas' ønske |

## 4.6 Den overordnede agents egne bemærkninger

1. **Det vigtigste strategiske fund i hele arbejdet:** Med 5 års data pr. marked er fabrikken en maskine til at finde **få, meget stærke** edges, ikke mange svage. Ønsker Thomas mange strategier, er vejen at **teste den samme regel på flere markeder** (pooling), ikke flere filtre eller flere indstillinger. Flere forsøg *hæver* grænsen. Flere markeder *sænker* den. [BEVIST som regnestykke i K1B §5.1 og v2 §4.2]
2. **"Rejected er endeligt" + en streng 2025-dom er en dyr kombination.** Konsulenterne genåbner ikke afgørelsen, men viser prisen: 36 % af de ægte S = 2-edges dør ved en 5 %-grænse i 2025. K1's R2 lader 2025 kun *kassere* og aldrig *vælge*. Den bevarer afgørelsen og sænker prisen til ca. 7 %. Det er et valg for Thomas.
3. **Rapporten er vokset. Planen er ikke.** Trods mange sider er anbefalingen enkel: én database, én mappe med Parquet-filer, ét Python-program pr. maskine, én fane og én låst metodefil. Det meste af teksten er begrundelser.
4. **Det Runde Bords inkubation** ligger delvist uden for den oprindelige opgave ("live og rigtige penge er ikke med"). Konsulenterne har kun leveret beslutningsregler og datamodel, ikke selve handelsudførelsen.
5. **Kilderne.** Nu *bekræftet* mod kode: StepM, SPA, MCS og bootstrap (`arch`), BH/BY/Holm (`statsmodels`), TA-Lib's startregler, DuckDB og Parquet, PostgreSQL's dokumentation og licenserne for vectorbt, TimescaleDB, pypbo og Airflow. **Stadig ikke bekræftet:**
   - TradeStations regler for series functions og startværdier. Det kan løses lokalt med punkt 0.2.
   - TradeStations og MultiCharts' licenser for flere computere. Det kan løses med punkt 0.13.
   - Originalartiklerne (López de Prado, Harvey m.fl.). Formlerne er dog kontrolleret mod kode.
6. **Hvad der ikke er nået:**
   - Intet er kørt på Thomas' rigtige data.
   - Tid pr. backtest er ikke målt.
   - N_eff er kun målt på ét syntetisk filter.
   - StepM for 84.476 varianter er kun skaleret, ikke kørt.
   - Der er ingen tegnet skærm for NiceGUI-fanen.

## 4.7 Samlet liste over åbne punkter til Thomas (prioriteret)

**A. Afgør først, fordi de styrer metodefilen (Fase 0.6)**

1. **Hvor mange markeder** kan den samme regel testes på (pooling)? Det er det stærkeste håndtag (4.6.1).
2. **2025-regel:** R1 (tællende grænse), R2 (kun kassering, fast lav grænse) eller R3 (online FDR) (K1B §5.4).
3. **Test for "rejected":** StepM som den afgørende, med DSR som tal ved siden af (K1B §6.1)?
4. **Lag A:** kriterium 1, 2 eller 3, minimum pr. celle, én dimension ad gangen (14 celler) eller på kryds, og hvilken andel dræbte ægte edges der er acceptabel (K1B §5.3, K2B §6.10).
5. **Retning og horisont** låst på forhånd pr. filter? (U3)
6. **Hvad er en event:** tænding (anbefalet) eller hver tændt bar? Og hvornår starter handlen? (K2B §6.3)
7. **Modstriden i Det Runde Bord:** Må et filter, der er dødt under v1, leve under v2? (U1)
8. **Embargo-datoerne** (K3B §8.2).

**B. Afgør, før der bygges**

9. **Skal den fulde kørsel vente på Fase 0?** (opgavens punkt 9)
10. **Datamodel og roller** (0.8), og må godkendte programmer skrive automatisk? (U9)
11. **Råsignaler i Parquet** i stedet for PostgreSQL? (K3B §8.8)
12. **Må den lokale session læse TradeStations funktionskode?** (0.2)
13. **MACD-filtre:** Konsulenterne er enige om vej a (byg om). Hvilket mønster, og skal commit `12120a8` genoplives? (opgavens punkt 4)
14. **Python som regnemaskine med TradeStation som facit** pr. workspace-type?
15. **Blind analyse:** Accepterer du ikke at se filternavne, før metoden er låst? (K1B §6.3)
16. **TradeStation-licens:** send spørgsmålet (0.13).
17. **Skal EasyLanguage Optimization API undersøges** lokalt som vej til automatiske backtests? (K2B §6.2)
18. **Placebo- og kontrolresultater:** i test eller produktion? (U8)

**C. Inkubation og dvale (Det Runde Bords åbne spørgsmål)**

19. **Inkubationsregel:** I1 (fast test), I2 (sekventiel med loft) eller I3 (Bayes), loftet, og hvad der sker ved loftet (K1B §5.5).
20. **Genvækning:** af systemet eller af et menneske? (U7)
21. **Hvordan skal domme, der er fældet på forkerte tal, markeres,** hvis en teknisk fejl opdages bagefter? (K2B §6.8)

**D. Drift og dokumentation**

22. **Omkostninger pr. marked:** kurtage og slippage i ticks.
23. **Signalpris** = lukkekursen på signal-baren, og slippage gemt med retning? (K2B §6.11)
24. **Backup uden for serveren:** hvor, og hvor tit?
25. **Lås TradeStation-versionen** på fabriksmaskinen.
26. **NiceGUI** til fanen? (K3B §8.7)
27. **Opdatér dokumentationen:**
    - BYGGEVEJLEDNING: 4.918, ikke 480.
    - NOTER.md punkt 3: MACD-forklaringen.
    - RawSignal266-filhovedet: Average er målt i orden.


# Bilag A – Kritik fra runde 2 (dybde-runden)

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

# Bilag B – Kritik fra runde 3 (værktøjskassen)

## K1's kritik, runde 3

**Rettet i min udkast3/k1.md:**
- Opvarmning regnes pr. datastrøm.
- Lag A-minimum = (1,28/δ)².
- E2: dommen træffes på råt nettoafkast.
- Lag B: benchmark = filteret uden kolonnen.

### (a) K2's EdgeFinder-protokol (§4)

| Punkt | Dom | Hvad skal ændres |
|---|---|---|
| E1 (A3) | GODKENDT | – |
| E2 (A6) | ÆNDRES | "Event − kontrol" kan ikke handles. Dommen træffes på **råt nettoafkast**. Kontrol-justeret t ≥ 2 kræves som ekstra krav. |
| E3 (A7) | GODKENDT | – |
| E4 (A5) | GODKENDT | – |
| E5 | MANGLER | Walk-forward i IS for alle valg i EdgeCruncher. Ellers: 2025 er eneste opdeling (R1–R3). |
| E6 (A9) | AFVIST | Den endelige grænse er **StepM**, ikke en t-værdi ud fra N_eff. Metodefilen skal skrive, hvilken test der giver "rejected". Thomas afgør. |
| E7/E8 (A10) | GODKENDT | Placebo køres også gennem StepM. Højst 1 ud af 20 placebo-sæt må give fund. |
| Lag A, 14 celler | GODKENDT | Kriteriet er et af mine tre (1B §5.3), med Holm på tværs af de 14 celler. |
| 196 signaler | AFVIST som begrundelse | Cellerne skal kun vise fortegn, ikke bevise noget. Brug (1,28/δ)². δ = 0,1 giver 164, δ = 0,05 giver 657. |
| Opvarmning før 2020 | ÆNDRES | Regnes i bars pr. datastrøm. EMA(600) på 60-minutters RTH-bars kræver ca. 1,2 år, og 120-minutters bars over 2 år. Charts skal starte senest 2017, og to-starts-testen skal bekræfte det. |
| Slippage (4.5) | GODKENDT | Kontrol: ensidet bootstrap-test af den ugunstige slippage mod modellen, α = 5 %, efter mindst 30 handler. |
| Lag B | ÆNDRES | StepM med benchmark = filteret *uden* kolonnen. |
| Lag C og identitet | GODKENDT | "Ligner, men er ikke ens" tæller som et forsøg i samme familie. |

### (b) K3
- **Reproducerbarhed:** DuckDB summerer parallelt, så kommatal kan afvige i sidste decimal. [Antagelse] **Krav:** Nøgletal regnes i fast rækkefølge eller afrundes før hash og dom, og pakkeversionerne låses i metodefilen.
- **Forsøgstælling:** Tælleren for 2025 (`DISTINCT identitet_id`) er korrekt. Men N_rå skal tælle varianter (kombination × retning × horisont) plus Lag B-tests. En `failed`-kørsel må kun udelades af tællingen, hvis ingen har set dens resultater (P4).
- **Rejected under ny metodeversion:** Det er kun forsvarligt, hvis tre ting er opfyldt:
  - Versionen er låst, før resultater ses.
  - Den køres på **alle** filtre.
  - Forsøgene lægges sammen på tværs af versioner, og 2025-tælleren fortsætter.

  Ellers er det Lag C ad bagdøren. Thomas afgør.

### (c) Uenigheder
1. Dommen træffes på råt nettoafkast, ikke på "event − kontrol" (K2 A6).
2. StepM som grænse, ikke en t-værdi ud fra N_eff (K2 A9).
3. Minimum pr. celle regnes ud fra fortegn, ikke ud fra en 5 %-test (K2 A8).
4. "Fra 2019" er for kort til 60- og 120-minutters strømme (K2 4.1).
5. En ny metodeversion må ikke kun genkøre de døde filtre (K3 §7.3).

## K2's kritik af K1 og K3 (runde 3)

**Rettet i min udkast3/k2.md (§4.2, trin A8):** Jeg bruger nu K1's minimum pr. celle, n ≥ (1,28/δ)², i stedet for mit 196. Mit krav "samme fortegn i 4 af 5 år" er fjernet til fordel for K1's tre kriterier.

### (a) Kan det bygges?

**StepM som hovedtest (K1 V3).** StepM kræver en tabel med én kolonne pr. variant og én række pr. handelsdag på en **fælles tidsakse**. Det betyder:
- EdgeFinder skal lave *nettoafkast pr. dag pr. variant*. Dage uden event får 0, ikke "mangler".
- Alle varianter skal bootstrappes med **de samme** trukne dage.
- Identiske signalrækker slås sammen først.

Regnestykke [Regnet]:
- 84.476 varianter × 1.250 dage × 8 byte = **845 MB** pr. workspace.
- Med 2 retninger × 5 horisonter bliver det 844.760 kolonner = **8,4 GB**, og ca. 40 minutter efter K1's egen skalering. Det kan lade sig gøre, men kun hvis retning og horisont er låst i metodefilen. Ellers sprænger det hukommelsen.
- Tabellen gemmes som Parquet (K3), så den ikke skal regnes igen.

**Placebo og indplantede edges i hver kørsel (K1 V8).**
- Placebo (cirkulær forskydning i hele handelsdage) er billig og kan bygges.
- Men **indplantet edge på syntetiske priser tester kun Python-kæden**. TradeStation kan ikke køre på kunstige priser, uden at de importeres som symbol (UKENDT). TradeStation→CSV-delen dækkes stadig kun af facit og F1.
- Placebo må **ikke** indgå i samme StepM-familie som de ægte varianter. Så ændres grænsen for de ægte. De skal køres separat med identiske indstillinger.

**Lag A (K1 §5.3).** Enig. Kræver kun, at hver event bærer år, ATR før indgang, tid på dagen og AntalBars. Det findes i CSV + bars.

**Parquet/DuckDB (K3 §1).** Det passer med kæden TradeStation → CSV → pandera → Parquet.

Men **SHA-256 af en Parquet-fil er ikke stabil**: samme data kan give andre bytes ved en anden pyarrow-version, komprimering eller metadata ("created_by") [Antagelse: almindelig egenskab ved Parquet-skrivere]. Derfor to fingeraftryk:
1. Rå CSV-bytes. Det er golden master for TradeStation.
2. Et **indholds-fingeraftryk**: rækker sorteret, faste typer, hash af værdierne.

Alternativt låses pyarrow-versionen.

### (b) Fejl og huller

- **K3 §5, `UNIQUE(formel_norm_sha256, n1_interval, …)`:** En UNIQUE-regel fanger kun helt ens intervaller, ikke *overlap* (1–25 mod 2–24). Det kræver en udelukkelsesregel (PostgreSQL exclusion constraint på talintervaller) eller et tjek i generatoren. Intervallet bør gemmes som en mængde af værdier, ikke som tekst.
- **K1 V8:** Placebo skal forskydes i hele handelsdage, ellers ændres tid-på-dagen-profilen. K1 skriver "handelsdage". Det skal stå eksplicit i metodefilen.
- **K1 blind analyse:** Skjul også formlen, ellers kan filteret genkendes [Antagelse].

### (c) Uenigheder

1. Lag A-minimum: løst. Jeg følger K1.
2. Fingeraftryk: K3 hasher Parquet-filen. Jeg: hash rå CSV + et indholds-fingeraftryk, ikke kun filbytes.
3. Placebo: K1 lægger dem i hver kørsel (enig), men de skal have deres egen StepM, ikke dele familie med de ægte.
4. Retning og horisont: skal låses i metodefilen før StepM, ellers bliver k ti gange større. K1 har ikke taget stilling.
5. Filter-identitet: overlap skal håndhæves med en udelukkelsesregel eller i generatoren, ikke med UNIQUE (K3).

## K3 – kritik af udkast3/k1.md og udkast3/k2.md

**Rettet i min udkast3/k3.md (nyt afsnit 7.8–7.9):**
- K1's faste pas-kolonner (hans §3.2) er taget med præcis som opstillet.
- Ny tabel `genvaekning`.
- K1's talgrænser og bordets tal er nu felter i `metode_version`. NULL betyder "ikke afgjort", og så går intet videre.
- K2's fingeraftryk erstatter mit `numrange`: normaliseret formel-træ, udfoldede parametermængder (`numeric[]` med overlap-operator `&&`), instrument inkl. session og tidsrammer for Data1–3.
- Ny status `venter`. Databasen afviser en Lag A-dom, før `f1_kontrolstatus = 'bestaaet'`.
- Lagring til StepM og placebo er regnet ud.

### (a) Passer det sammen?

- **K2's fingeraftryk:** Ja. Hver del er en fast kolonne. SHA-256 af de fire dele er UNIQUE.
- **Overlap med dødt filter → stop:** Ja. En trigger på `filter_identitet` stopper det, og generatoren stopper med ByggeFejl. Et træ, der "ligner", giver kun en advarsel i `haendelse`, som K2 foreslår.
- **Ingen Lag A-dom før F1/K0–K6, og MACD-gruppen står som "venter":** Ja. `venter` er en status, og triggeren på `lag_brug` afviser `in_sample` uden bestået F1. Det genåbner ikke Thomas' afgørelse: `failed`/`rejected` er uændret, og `venter` betyder blot "ikke dømt endnu".
- **StepM (K1 V3):** kræver en matrix med T × k daglige resultater.
  - Regnet: 1.250 dage × 84.476 varianter × 4 B ≈ **422 MB pr. workspace**. Uden sammenlægning af ens rækker bliver det ca. **11,9 GB**.
  - Matrixen gemmes ikke fast. Den regnes igen fra Parquet-signaler + prisbars. Kun fingeraftryk, seed, bloklængde og resultat gemmes.
- **Placebo (K1 V8):** Kun `(kilde_filter, forskydning, seed)` gemmes. Signalerne dannes igen efter behov.
- **Følge for Parquet:** Næsten ingen ekstra plads. Men prisbars *skal* gemmes fra start og må aldrig ændres, ellers kan hverken StepM eller placebo genskabes.

### (b) Fejl og huller

1. **K2 §4.6:** Fingeraftrykket afhænger af parserens version. Ændres normaliseringen, skifter alle fingeraftryk, og et dødt filter kan "slippe ud". Parserens version skal gemmes, og ved en ny version skal alle fingeraftryk regnes om, også for de døde, før der bygges noget nyt.
2. **K1 V8:** Placebo-forskydningen skal ske *inden for in-sample*. Ellers bringer den 2025-data ind i in-sample, og tællingen af, hvem der har "rørt 2025", bliver forkert.
3. **K1 §3.2:** `pengeskab_andel` hører til den gamle tredeling. Med bordets fire lag bør det hedde fx `embargo_krav`. Ellers står der to modeller i samme pas.
4. **K1 V3:** "84.476 varianter ≈ 4 minutter" er skaleret, ikke kørt. Hukommelsen til bootstrap (flere kopier af en matrix på 422 MB) bør måles på serveren, før det kaldes BRUG NU.
5. **K1 (genvækning):** Hvem træffer beslutningen `vaek`? Bordet vil have, at *systemet* åbner for live. Det bør gælde genvækning på samme måde. Ikke afgjort.

### (c) Uenigheder

1. K2: parser-lighed = identitet. K3: kun sammen med en gemt parser-version og omregning af alle fingeraftryk ved ny version.
2. K1: grænsefelt `pengeskab_andel`. K3: omdøbes til embargo, så passet følger bordets fire lag.
3. K1: StepM-matrix som datagrundlag. K3: den er en genberegnet mellemvare, ikke noget, der gemmes fast.
4. Åbent for Thomas: genvækning afgøres af systemet eller af et menneske.

