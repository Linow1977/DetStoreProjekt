---
title: "Konsulentrapport: udviklingsmotoren i DetStoreProjekt"
subtitle: "Fælles rapport fra konsulentgruppen – råd til Thomas, ikke beslutninger"
date: "28. september 2026"
---

# Aftalen fra den fælles planlægning

1. Konsulent 1 skriver definitionen af "færdig strategi" som det FØRSTE i sit udkast. Konsulent 2 og 3 bygger på en foreløbig version og markerer tydeligt, hvor de afhænger af den.
2. Klare grænser: Konsulent 1 designer og godkender metoder, men bygger intet. Konsulent 2 bygger og kvalitetssikrer EasyLanguage-delen (filtre, EdgeCruncher, MultiCharts). Konsulent 3 bygger data-, lager- og automatiseringsdelen. Der er to steder, hvor de overlapper. Ved stikprøverne af filtre bestemmer K1 metoden, og K2 udfører den. Ved strategiens "pas" bestemmer K1, HVAD der står i det, og K3 HVORDAN det gemmes.
3. Alle skriver på enkelt dansk, forklarer fagord første gang og sætter [Rapport], [Net: kilde] eller [Antagelse: hvorfor] på hver væsentlig påstand. Ingen afgør Thomas' åbne punkter. De samles i én liste.
4. Uenighed skjules ikke. Den skrives åbent og samles i del 4.

*Om arbejdsformen:* Den fælles planlægning var ikke en samtale, hvor alle talte på samme tid. Den overordnede agent skrev aftalen ud fra opgaven, og alle konsulenter fik den med fra start. Den egentlige samtale foregik skriftligt i runde 2. Her læste hver konsulent de to andres udkast, godkendte eller afviste deres metoder, skrev sine uenigheder ned og rettede sit eget udkast. Kommentarerne står i bilaget. Gruppen brugte cirka 10 af de 20 minutter.

# Sammenfatning (højst en halv side)

**Hovedbudskab:** Motoren kan godt komme til at producere strategier, man kan stole på. Men i dag mangler den tre ting. Den har ingen skrevet regel for, hvornår en strategi er "færdig". Den tæller ikke, hvor mange ting der er afprøvet. Og den har intet sikkert sted at gemme færdige strategier. Det vigtigste tal i rapporten er dette: Hvis ingen af de ca. 380 filtre har en ægte fordel, vil omkring 19 af dem alligevel se "gode" ud af ren tilfældighed. Med flere indstillinger pr. filter bliver det til hundreder eller tusinder (del 1).

**De tre konsulenter er enige om:**

- **"Færdig strategi" = 10 prøver (F1–F10).** Den vigtigste er "pengeskabet". Det er et stykke data, som ingen må se, før strategien til sidst testes på det én gang. Dumper strategien der, bliver den smidt ud (del 1).
- **Nogle billige ting bør gøres, FØR den fulde kørsel af de 380 filtre startes.** Filtrene skal have faste navne, der aldrig skifter nummer. Hver fil skal mærkes med den kodeversion, der lavede den. Og alle filtre skal gennemgås automatisk for tavse fejl af MACD-typen. Datadelingen skal også låses. Det koster lidt nu og kan spare en hel omgang "ryd op og start forfra" senere (del 1, 2 og 3).
- **MACD-fejlen er sandsynligvis ikke den eneste af sin slags.** Andre indbyggede udregninger, der husker deres sidste resultat, kan fejle på samme måde. Et filter, der kan være ramt, må godt bygges. Men det må ikke godkendes som færdigt, før det er kontrolleret mod en uafhængig beregning (del 1 og 2).
- **Tungt regnearbejde flyttes fra TradeStation til Python.** TradeStation laver kun signaler og handler. Det gør fabrikken hurtigere og gør det lettere at flytte til MultiCharts senere. Til gengæld skal Python's tal tjekkes mod TradeStation (del 2 og 3).
- **Databasen bliver midten af det hele.** Den holder en fælles opgaveliste, som mange computere kan tage opgaver fra. Og den har et dvale-lager, man kun kan lægge ting i. Intet bliver rettet eller slettet der (del 3).

**Største ubekendte:** Vi ved ikke, om TradeStation må være logget ind på flere computere samtidig. Det afgør, om fabrikken kan fordeles over flere maskiner. Thomas skal spørge TradeStation (del 3 og 4).

**Forbehold:** Intet er kontrolleret mod den rigtige kode eller database, fordi gruppen ikke havde adgang. Alle tal og grænser er forslag. Intet i rapporten er et løfte om afkast. Handel indebærer risiko for tab.


# Del 1 – Validering (Konsulent 1: kvantitativ statistiker)

*Udkast. Jeg designer og godkender metoder; jeg bygger intet og afgør ikke Thomas' åbne punkter.*

Mærker: [Rapport] = står i statusrapporten. [Net: kilde] = fra internettet. [Antagelse: hvorfor] = min egen vurdering.

**Tre fagord først:**
- **Overfitting** (overtilpasning): en regel er "syet" så tæt til gamle data, at den fanger tilfældig støj i stedet for noget ægte. Den ser flot ud bagud og virker ikke fremad.
- **Multiple testing** (mange forsøg): Hvis man slår plat og krone med 380 mønter, vil nogle af dem slå "krone" mange gange i træk af ren tilfældighed. Jo flere filtre man tester, desto flere tilfældige "vindere" dukker op.
- **p-værdi**: sandsynligheden for at se et resultat så godt som det, man fandt, *hvis der i virkeligheden intet er*. p = 0,05 betyder "1 ud af 20 rene tilfældigheder ser lige så gode ud".

---

## 1. Definition af "færdig strategi" (foreløbig version – K2 og K3 bygger på den)

En strategi må først lægges i dvale, når **alle** punkter nedenfor er bestået og skrevet ind i strategiens "pas" (K3 bestemmer, *hvordan* passet gemmes; her står *hvad* der skal stå i det). Ét dumpet punkt = ikke færdig. [Antagelse: listen er min faglige vurdering bygget på de kilder, der er nævnt i afsnit 3.]

| # | Test | Krav (foreløbigt – tallene er forslag, Thomas bekræfter) |
|---|------|------------------|
| F1 | **Teknisk rent signal** | Filteret er genereret af RawSignal Creature uden fejl, *og* stikprøvekontrolleret mod en uafhængig beregning (afsnit 6). Filtre med MACD-risiko eller usikker Max Bars Back er enten kontrolleret eller udelukket. Samme filter kørt to gange giver præcis samme tal (K2's "dobbeltkørsel"). |
| F2 | **Låst datadeling før første test** | Data er delt i tre dele *før* noget testes: udviklingsdata, valideringsdata og et "pengeskab" (hold-out) sidst i tiden, som ingen har set. Delingsdatoerne står i passet. |
| F3 | **Alle forsøg er talt** | Passet oplyser, hvor mange varianter (filtre × parametre × markeder × tidsrammer × retning) der i alt er prøvet i den runde, strategien kom fra. Uden dette tal kan resten ikke regnes. |
| F4 | **Overlever straf for mange forsøg** | Resultatet er stadig signifikant efter korrektion for antal forsøg (Deflated Sharpe ≥ 0,95 og/eller med i en false discovery rate-liste på 5–10 %, se afsnit 3). |
| F5 | **Plateau** | Signalet virker i et sammenhængende område af nabo-indstillinger, ikke kun i én "top". Mindst det plateau-niveau, Thomas vælger (afsnit 5 – ikke afgjort). |
| F6 | **Walk-forward** | Bestået i walk-forward-test (forklaret i afsnit 4) med fast, på forhånd skrevet opskrift. Flertallet af vinduerne er positive efter omkostninger. |
| F7 | **Omkostninger og slippage** | Edge overlever realistiske handelsomkostninger og slippage (prisforskel ved udførelse), gerne også med dobbelt omkostning som stresstest. |
| F8 | **Stabilitet over tid og markedstyper** | Ingen enkelt periode (fx ét år) eller få handler står for hovedparten af gevinsten. Resultatet holder i både rolige og urolige perioder. |
| F9 | **Pengeskabet åbnes én gang** | Til sidst testes strategien én gang på hold-out-data. Dumper den, kasseres den – den må ikke justeres og testes igen (så bliver pengeskabet "brugt"). |
| F10 | **Nok handler** | Et minimum antal handler (forslag: mindst 100–200 i udviklingsdata og mindst 30 i hold-out). [Antagelse: tommelfingerregel; for få handler giver ingen sikker statistik.] |

**Passet skal mindst indeholde:** filter-ID *og* filter-version (fordi numrene har flyttet sig [Rapport]), parametre, markeder/tidsramme, datadelings-datoer, antal forsøg (F3), resultatet af F4–F10 med tal, plateau-niveau, kendte risici (MACD/Max Bars Back), største tab (drawdown), den brugte omkostningsmodel, om pengeskabet er åbnet (ja/nej + dato), dato og kodeversion. Så kan en strategi genvurderes, når den vækkes.

Vigtigt: "Færdig" betyder "vi har ikke kunnet afvise den med de tests, vi har". Det er aldrig et løfte om fremtidig gevinst.

---

## 2. Svagheder i det nuværende set-up – hvor kan tilfældigheder slippe igennem?

**RawSignal Creature**
- Kun afprøvet på 13 filtre, og de er slettet igen [Rapport]. Teknisk korrekt kode (den kompilerer) betyder ikke, at tallene er rigtige. En fil kan være "fejlfri" og stadig regne forkert. [Antagelse: kompilering tjekker grammatik, ikke regnestykket.]
- **MACD-fejlen** [Rapport]: statistisk er det værste ved den, at den er *stille*. Forkerte tal er ikke bare støj – de kan skabe mønstre, der ikke findes, eller skjule dem, der gør. Hvis fejlen afhænger af rækkefølgen af kald, kan den ovenikøbet give "look-ahead"-lignende effekter eller ændre sig mellem kørsler. Risikoen er "accepteret" for hele kørslen og kun noteret i filerne [Rapport] – det er fint til at bygge, men **ikke** til at godkende. Mit forslag: ethvert filter med MACD (eller anden funktion på samme "mistænkt"-liste) må ikke passere F1, før det er kontrolleret mod en uafhængig beregning. Andre indbyggede funktioner med "hukommelse" (fx gennemsnit med udglatning, som også gemmer tidligere værdier) bør mistænkes for samme type fejl – K2 vurderer hvilke. [Antagelse: fejlen skyldes ifølge rapporten intern hukommelse, og det deler andre udglattede indikatorer.]
- **Max Bars Back for 36 filtre** [Rapport]: Er 1000 bjælker for lidt, starter beregningen for tidligt med "halvfærdige" tal (især ved udglattede indikatorer, der skal "varme op"). Det giver systematisk forkerte signaler i begyndelsen af data – og det rammer netop de første perioder, som ofte er udviklingsdata. Statistisk: en ukendt fejl i 36 af 380 filtre (ca. 9,5 %) er for meget til at ignorere. Forslag: køre de 36 filtre med fx 1000 og 2000 bjælker og sammenligne signalerne på de sidste, fælles bjælker. Er de identiske → antagelsen holder. Er de forskellige → filteret markeres.
- Filternumre har ændret sig [Rapport] → risiko for at resultater sættes på forkert filter. Brug et fast ID, der aldrig genbruges.

**RawSignal-Analyse** (findes kun som rolle [Rapport])
- Største risiko: at metoden først bliver skrevet *efter* man har set resultaterne. Så kan man (ubevidst) vælge den metode, der får flest filtre til at se gode ud. Metoden skal skrives og låses før fuld kørsel analyseres. [Antagelse: kendt fælde, "forking paths".]
- Plateau-analysen er ikke defineret (se afsnit 5).

**EdgeFinder** ("ikke helt udformet" [Rapport])
- Event-studier kan snyde, hvis signaler overlapper i tid (samme bevægelse tælles mange gange), hvis man bruger fremtidig information, eller hvis man ikke har en tilfældig sammenligningsgruppe. Se krav i afsnit 4.

**EdgeCruncher** (kun et navn [Rapport])
- Hvis EdgeCruncher optimerer parametre/kombinerer signaler, er det her, flest skjulte forsøg opstår. Alle forsøg skal tælles (F3). K2 designer den; jeg kræver blot, at den logger antal forsøg og aldrig rører pengeskabs-data.

**Dvale-lager** (findes ikke)
- Hvis kun "vinderne" gemmes, glemmer man, hvor mange der blev prøvet – og kan ikke længere regne korrektionen. Derfor skal også taberne/antallet gemmes (mindst som tal).
- Når en strategi vækkes måske år senere, skal den testes igen på de nye data siden dvale. Dvale er ikke en godkendelse, der holder for evigt. [Antagelse: markeder skifter adfærd, som rapporten selv nævner.]

**Tværgående**
- Samme data bruges af alle led. Hver gang et menneske eller en AI kigger på et resultat og ændrer noget, er det et ekstra forsøg. Det skal tælles med.
- Fejlprincippet "ryd op og start forfra" [Rapport] er statistisk godt – det forhindrer lappede, halvgamle resultater.

---

## 3. Multiple testing med ~380 filtre – regnestykket

**Enkelt eksempel.** Antag at *ingen* af de 380 filtre har en ægte edge. Vi tester hvert med den almindelige grænse p < 0,05.

- Forventet antal tilfældige "vindere" = 380 × 0,05 = **19 filtre**.
- Sandsynligheden for mindst én falsk vinder = 1 − 0,95^380 ≈ **99,99999 %** (næsten sikkert).

Men 380 er kun begyndelsen. Hvert filter testes typisk med flere indstillinger, markeder og retninger:

| Antal forsøg | Tilfældige "vindere" ved p<0,05 | Hvor god ser den *bedste* tilfældige ud? (t-værdi*) |
|---|---|---|
| 380 | 19 | ca. 3,0 |
| 3.800 (×10 varianter) | 190 | ca. 3,6 |
| 76.000 (×200 varianter) | 3.800 | ca. 4,3 |

*t-værdi: hvor mange "standardafvigelser" resultatet ligger over nul; 2 regnes normalt som "signifikant". Tallet er beregnet med den formel for "forventet bedste ud af N tilfældige", som bruges i Deflated Sharpe-artiklen [Net: Bailey & López de Prado, "The Deflated Sharpe Ratio", https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551]. Forudsætter uafhængige forsøg; i praksis er filtre korrelerede, så det reelle tal er lidt lavere – men retningen er den samme. [Antagelse: forenkling.]

**Pointen for et barn:** Med 380 filtre vil det bedste rene held-filter se lige så godt ud, som en forsker før i tiden ville kalde "meget stærkt bevis". Harvey, Liu og Zhu nåede frem til, at en ny opdagelse bør have t > 3 i stedet for 2, netop pga. mange forsøg [Net: Harvey, Liu & Zhu (2016), "...and the Cross-Section of Expected Returns", Review of Financial Studies; resumé: https://foxholm.com/q/research/harvey-liu-zhu-cross-section/]. Med vores antal forsøg er selv 3 for lavt.

**Bonferroni** (den strengeste simple korrektion: del 0,05 med antal forsøg): ved 380 forsøg skal p < 0,00013 (t ≈ 3,8). Den er sikker men så streng, at ægte edges også smides ud.

**Min foreslåede metode (lag på lag):**
1. **Tæl alle forsøg** (F3). Uden tælling kan intet korrigeres.
2. **False discovery rate (FDR)** med Benjamini–Hochberg i RawSignal-Analyse: i stedet for at kræve "ingen fejl overhovedet" styrer man, at *højst fx 10 % af de filtre, man lader gå videre, er tilfældige*. Passende som grovsortering, fordi den er mindre streng end Bonferroni [Net: Benjamini & Hochberg (1995), JRSS B, https://academic.oup.com/jrsssb/article/57/1/289/7035855].
3. **Deflated Sharpe Ratio (DSR)** i den endelige godkendelse: Sharpe-tallet (afkast pr. risiko) "tages ned" for antal forsøg, datalængde og skæve afkast. Krav: DSR ≥ 0,95 [Net: Bailey & López de Prado, link ovenfor].
4. **Data-snooping-test af den bedste** (White's Reality Check eller Hansen's SPA): tester om den bedste af alle modeller er bedre end tilfældighed, når man tager højde for, at man valgte den bedste [Net: White (2000), "A Reality Check for Data Snooping", Econometrica, https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0262.00152].
5. **Probability of Backtest Overfitting (PBO)** via CSCV: data deles i mange stykker, og man måler, hvor tit "vinderen" i én halvdel ender under middel i den anden halvdel. Høj PBO = udvælgelsen er overfitting [Net: Bailey, Borwein, López de Prado & Zhu, "The Probability of Backtest Overfitting", https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253]. Forslag: PBO under ca. 0,2–0,3 (Thomas vælger).
6. **Kendt-tilfældige kontrol-signaler** (se afsnit 5): kør fx 100 bevidst tilfældige signaler gennem hele linjen. Slipper for mange igennem, er linjen for blød. Det er den mest direkte og forståelige test af hele fabrikken. [Antagelse: standard "placebo"-idé.]
7. **Pengeskab** (F9) som sidste, enkelte test.

---

## 4. Metode for RawSignal-Analyse og godkendelseskrav til EdgeFinder

### 4a. RawSignal-Analyse (grovsortering – billig og hurtig)
Formål: smide det åbenlyst tilfældige/ubrugelige ud, *før* der bruges tid på det. Kun på udviklingsdata.

1. **Sundhedstjek af signalet:** antal signaler, fordeling over tid, huller, signaler i første 1000 bjælker (Max Bars Back), identiske signaler mellem filtre (dubletter tæller ikke som "flere beviser").
2. **Rå fremadrettet effekt:** for hvert signal måles prisbevægelsen efter N bjælker (fx 1, 5, 10, 20) sammenlignet med *tilfældige tidspunkter* i samme marked og samme tid på dagen. Uden omkostninger endnu.
3. **Stabilitet over tid:** del udviklingsdata i fx 4–8 lige store perioder; hvor stor en andel peger samme vej?
4. **Plateau-kort:** effekten beregnes på et gitter af nabo-parametre (se afsnit 5).
5. **FDR-sortering** (afsnit 3) på hele listen. Kun filtre på FDR-listen + med plateau-niveau ≥ Thomas' tærskel går videre.
6. **Log alt**, også dem der dumper.

### 4b. Godkendelseskrav til EdgeFinder (event-studie)
*Event-studie* = man kigger på hvad prisen gør lige efter hver gang, signalet "tænder", og sammenligner med hvad den normalt gør. Jeg godkender EdgeFinder-metoden, når den opfylder:

- E1 **Ingen fremtidsinformation:** signal beregnes kun med data til og med signalbjælken; handel tidligst på næste bjælke.
- E2 **Retfærdig sammenligning:** "normal" udvikling måles på tilfældige/ikke-signal tidspunkter med samme tid på dagen og samme volatilitet (udsving).
- E3 **Overlap håndteres:** signaler tæt på hinanden tælles ikke som uafhængige; brug fx blok-bootstrap (gentaget udtrækning af hele tidsblokke) til usikkerhed.
- E4 **Omkostninger** trukket fra (F7).
- E5 **Walk-forward:** man "træner" på en periode, tester på den næste, rykker frem og gentager – så man altid tester på data, som valget ikke har set.
- E6 **Korrektion for forsøg** (DSR/FDR, afsnit 3).
- E7 **Kontrol med kendt-tilfældige signaler** giver ca. den forventede falsk-positiv-rate (fx ~5 % ved 5 %-grænse). Gør den ikke det, er metoden forkert.
- E8 **Kontrol med et kendt, indplantet signal** (syntetiske data med en lille bevidst edge) bliver fundet. Så ved vi, at metoden også kan *finde* noget.

E7 + E8 er min vigtigste godkendelsestest: en metode, der hverken giver for mange falske fund eller overser plantede fund.

---

## 5. Plateau-trappen (PL1–PL7) – hvordan Thomas kan afgøre de åbne punkter

Jeg afgør dem ikke. Jeg foreslår forsøg, der gør Thomas' valg til et spørgsmål om tal frem for mavefornemmelse. [Antagelse: al viden om trappen stammer fra opgavebeskrivelsen; definitionen er ikke vedlagt.]

**Fælles værktøj – "placebo-forsøget":** Lav fx 200 kendt-tilfældige signaler (tilfældige tidspunkter med samme hyppighed som ægte filtre) og 20 syntetiske signaler med en lille indplantet edge. Kør dem gennem plateau-analysen og se, hvilket niveau hver ender på. Så kan Thomas se, hvor "hårdt" hvert niveau reelt er.

| Åbent punkt | Hvordan Thomas kan afgøre det |
|---|---|
| **Hvad betyder grøn/grå/rød?** | Thomas skriver en præcis regel for hver farve (fx "grøn = effekt over grænse X og p under Y"). Test: i placebo-forsøget skal næsten alle celler være grå/rød; i indplantet-forsøget skal kernen være grøn. Passer det ikke, er definitionen forkert. |
| **Hvorfor 20 % rød tilladt højere oppe, men 0 % lavere?** | Kør placebo-forsøget: hvor mange tilfældige signaler når hvert niveau? Hvis et "højere" niveau lukker *flere* tilfældige igennem end et lavere, er trappen ikke en trappe. Thomas kan også skrive begrundelsen ned (fx "større felt = flere celler = rød uundgåelig i kanten"). Er begrundelsen størrelsen, kan kravet i stedet gøres afhængigt af feltets størrelse. |
| **Hvad må resten være ved "under 50 % grå"?** | Tre muligheder at vælge mellem: (a) resten skal være grøn, (b) resten må være grøn eller rød, (c) en fast grænse for rød. Placebo-forsøget viser, hvilken af dem der lukker færrest tilfældige igennem uden at smide de indplantede ud. |
| **Er de største felter et loft?** | Tjek om PL7 stadig lader nogle tilfældige signaler igennem i placebo-forsøget. Gør det, er der brug for mere (fx flere niveauer eller en ekstra test). Gør det ikke, og mister man ikke indplantede signaler, er loftet nok. Tjek også datamængde: store felter kræver mange handler pr. celle. |
| **Hvilket niveau er nok til dvale?** | Vælg det laveste niveau, hvor placebo-signalerne næsten aldrig når op (fx under 1–5 % – Thomas vælger tallet), og hvor de fleste indplantede signaler stadig når op. Det tal skrives ind i F5. |

Til Thomas: **plateau alene er ikke nok** som bevis. Et plateau kan også opstå af tilfældighed, hvis nabo-celler deler næsten samme data. Derfor er plateau ét krav blandt flere (F5), ikke hele godkendelsen. [Antagelse: nabo-parametre giver stærkt korrelerede resultater.]

---

## 6. Stikprøvekontrol af filtre mod uafhængige beregninger (metode – K2 udfører)

1. **Uafhængig beregning:** Samme filter regnes i et andet værktøj (fx Python med et kendt, åbent bibliotek eller en simpel håndskrevet formel) på *præcis samme* prisdata. Den, der skriver den uafhængige version, må ikke kigge i EasyLanguage-koden – kun i filterets beskrivelse. [Antagelse: ellers kopieres fejlen.]
2. **Udvælgelse (lagdelt stikprøve):**
   - 100 % af de "mistænkte": alle filtre med MACD, andre funktioner på mistænkt-listen og de 36 med usikker Max Bars Back.
   - Tilfældig stikprøve af resten: fx 30–40 filtre, trukket med en fast, noteret "terning" (seed), så det kan gentages. Hvis 0 fejl findes i 38 tilfældige, kan man med ca. 95 % sikkerhed sige, at under ca. 8 % af de øvrige har fejl ("3-reglen": 3/n). [Antagelse: standard tommelfingerregel.]
   - 100 % af alle filtre, der når frem til "færdig strategi".
3. **Sammenligning:** signal for signal, bjælke for bjælke, efter opvarmningsperioden. Krav: 100 % enighed om, hvornår signalet tænder (små afrundingsforskelle i indikatorværdier accepteres inden for en på forhånd fastsat tolerance).
4. **Gentagelsestest (for MACD-typen):** kør filteret alene og sammen med andre kald/parametre i samme program. Forskellige tal = fejl af eksempel A-typen.
5. **Ved fejl:** filteret markeres, fejlen logges i Videnslog, og efter projektets princip ryddes resultatet og køres forfra – ingen delvis reparation [Rapport].

---

## 7. Nye åbne punkter til Thomas

1. **Tallene i "færdig strategi"** (F4, F6, F10, PBO-grænse): skal de foreslåede grænser bruges, eller vil Thomas sætte andre?
2. **Datadeling:** Hvilke datoer skal være udvikling, validering og "pengeskab"? Skal låses *før* fuld kørsel analyseres.
3. **Hvad tæller som ét forsøg?** Tælles hvert filter, hver parameter, hvert marked? (Påvirker hele korrektionen.)
4. **Er der allerede "set" på data?** Hvis filtrene er udvalgt efter tidligere kig på de samme prisdata, er de ekstra skjulte forsøg. Hvor meget af data er "urørt"?
5. **MACD-filtre:** udelukke, kontrollere 100 %, eller bygge egen MACD-beregning? (Tilføjelse til punkt 4 i opgavens liste: statistisk anbefaler jeg, at de ikke kan godkendes uden kontrol.)
6. **De 36 filtre med usikker Max Bars Back:** skal sammenligningstesten (1000 vs. fx 2000 bjælker) køres før fuld kørsel?
7. **Placebo-forsøget:** må der laves kendt-tilfældige signaler som fast kontrol i hele linjen? De skal holdes adskilt fra produktionsdata [Rapport: test-data må ikke blandes].
8. **Genvækning:** hvilken test skal en strategi bestå, når den vækkes fra dvale (fx ny test på data siden dvale)?
9. **Hvilke markeder og tidsrammer** skal filtrene testes på? Det bestemmer antallet af forsøg.

---

**Hvad mangler i dette udkast (ærligt):** Ingen tal er afprøvet på rigtige data – vi har ingen adgang. Grænseværdierne er forslag. Konkrete formler for plateau-farver mangler, fordi trappen ikke er defineret. Jeg har ikke vurderet dataoplysninger som markeder, datakvalitet og handelstider, fordi rapporten ikke nævner dem.

**Kilder:**
- Bailey & López de Prado, "The Deflated Sharpe Ratio" – https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2460551
- Bailey, Borwein, López de Prado & Zhu, "The Probability of Backtest Overfitting" – https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2326253
- Harvey, Liu & Zhu (2016), "...and the Cross-Section of Expected Returns" (resumé) – https://foxholm.com/q/research/harvey-liu-zhu-cross-section/
- Benjamini & Hochberg (1995), "Controlling the False Discovery Rate" – https://academic.oup.com/jrsssb/article/57/1/289/7035855
- White (2000), "A Reality Check for Data Snooping" – https://onlinelibrary.wiley.com/doi/abs/10.1111/1468-0262.00152


# Del 2 – Konsulent 2: EasyLanguage-ekspert (kvalitet og bygning)

**Udkast. Skrevet på ca. 10 minutter. Intet er kontrolleret mod den rigtige kode, fordi vi ikke har adgang til den [Rapport: opgavens afsnit 1].**

Mærker: [Rapport] = står i statusrapporten. [Net: kilde] = fra internettet. [Antagelse: hvorfor] = min egen vurdering.

**Min afhængighed af Konsulent 1:** Jeg bygger på K1's definition af "færdig strategi", punkterne **F1–F10** (se del 1). Hvor jeg henviser til et bestemt punkt, står der fx **[K1: F9]**. Hvor K1 endnu ikke har fastsat et tal (tolerance, stikprøvestørrelse), står der **[Afhænger af K1]**.

---

## 1. Fejlliste – "tavse fejl" af samme type som MACD

En **tavs fejl** er en fejl, hvor programmet kører, ingen fejlmelding kommer, men tallene er forkerte. Det er de farligste, fordi en falsk edge ser præcis ud som en ægte.

### 1.1 Funktioner med hukommelse, kaldt med skiftende indstillinger (MACD-typen)
- **Hvad:** Nogle indbyggede funktioner er **"series functions"** (funktioner med hukommelse). De husker deres eget resultat fra sidste bar og bygger videre på det. MACD er bygget af eksponentielle gennemsnit (XAverage), som netop husker sidste værdi [Antagelse: almindelig kendt opbygning af MACD i EasyLanguage; ikke kontrolleret mod projektets kode]. Hvis samme kald-sted i koden bruges med skiftende længde (fx i en løkke, der prøver 12, 26, 50), bygger funktionen videre på en "hukommelse", der blev regnet med en anden længde. Resultatet er en blanding [Rapport: afsnit 7 bekræfter fejlen for MACD ved skiftende parametre] [Antagelse: forklaringen på mekanismen].
- **Hvorfor farligt:** Tallet ser plausibelt ud. Ingen fejl. Kan skabe falske signaler.
- **Hvordan opdages:** Sammenlign med en uafhængig beregning i Python (se del 2). Lav desuden en automatisk kodescanning: find alle steder, hvor en funktion med hukommelse kaldes inde i en løkke eller med en variabel længde.
- **Samme type, andre funktioner (sandsynligt):** XAverage, RSI, ADX/DMI, Stochastic (Slow), ATR i visse udgaver, ParabolicSAR, TRIX, KeltnerChannel – alle bygger på "sidste værdi" [Antagelse: de bruger udglatning, der husker sidste værdi; skal verificeres én for én].

### 1.2 Funktioner med hukommelse, kaldt betinget (kun på nogle barer)
- **Hvad:** Står funktionen inde i en `if`-sætning, bliver den måske kun regnet, når betingelsen er sand. TradeStation prøver selv at regne "series functions" på hver bar, uanset `if` [Net: MultiCharts forum "Easy language question", https://www.multicharts.com/discussion/viewtopic.php?t=5908 – beskriver at series-funktioner kan bruges betinget uden forkert værdi]. Men det gælder kun funktioner, som platformen **genkender** som series. En egen-skrevet funktion eller en "simple function" med skjult tilstand genkendes måske ikke [Antagelse: kendt faldgrube i EasyLanguage-miljøet, ikke verificeret her].
- **Farligt:** Indikatoren "springer barer over" og bliver forkert.
- **Opdages:** Kodescanning for funktionskald inde i `if`/løkker + Python-sammenligning.

### 1.3 Max Bars Back (MBB) for lille
- **Hvad:** MBB er, hvor mange barer bagud koden må kigge. Projektet har valgt 1000 som standard, og for 36 filtre kan behovet ikke beregnes – der er det en antagelse, at 1000 er nok [Rapport: afsnit 7].
- **Farligt på to måder:** (a) Er MBB for lille, stopper platformen nogle gange med fejl – det er godt, for det ses. (b) Men et eksponentielt gennemsnit med lang længde er ikke "færdigt opvarmet" efter få barer; de første værdier er upræcise uden fejl [Antagelse: matematisk egenskab ved udglatning]. (c) De første MBB barer bliver ikke handlet [Net: MultiCharts Wiki, "Advanced. How The Strategy Backtesting Engine works", https://www.multicharts.com/trading-software/index.php?title=Advanced._How_The_Strategy_Backtesting_Engine_works]. Forskellig MBB mellem filtre = forskellig testperiode = ikke sammenlignelige tal.
- **Opdages:** Kør de 36 filtre med MBB 1000 og fx 2000. Er signalerne ens efter bar 2000? Hvis ikke, er 1000 for lidt. Brug **samme** startdato for alle filtre i analysen.

### 1.4 Look-ahead (at kigge ind i fremtiden)
- **Hvad:** Koden bruger en pris, man ikke kunne kende på handelstidspunktet. Klassikere: bruge dagens `Close` til en ordre "this bar on close" og samtidig regne med dagens høj/lav; bruge data fra et højere tidsinterval (Data2, fx dagsdata) inden dagen er slut; bruge `Next Bar Open` til at beslutte noget på samme bar [Antagelse: velkendte fejltyper i backtest-litteraturen].
- **Farligt:** Giver meget flotte, helt falske resultater.
- **Opdages:** "Forskydningstest": flyt hele signalet én bar senere. Falder resultatet dramatisk, er der mistanke om look-ahead. Kodescanning efter `Data2`, `this bar on close` kombineret med indgang samme bar.

### 1.5 Sessionstider og tidszoner
- **Hvad:** Daytrading afhænger af åbning/lukning. Forkert sessionsskabelon (fx 24-timers i stedet for dagssession), sommertid/vintertid og helligdage flytter "første bar" og "sidste bar" [Antagelse: typisk kilde til fejl ved intradag-data].
- **Opdages:** Test-bar-tæller pr. dag: hvor mange barer har hver dag? Afvigende dage listes automatisk.

### 1.6 Bar-opløsning og hvad der sker inde i en bar
- **Hvad:** Et backtest kender kun åben, høj, lav, luk (OHLC) for hver bar. Rammes både stop og mål i samme bar, må platformen gætte rækkefølgen [Net: MultiCharts forum "Help understanding Intra-bar Price Movement Assumptions", https://www.multicharts.com/discussion/viewtopic.php?t=53501].
- **Opdages:** Tæl, hvor mange handler har stop og mål i samme bar. Er det mange, testes med finere data (Look-Inside-Bar / Bar Magnifier).

### 1.7 IntrabarOrderGeneration (IOG)
- **Hvad:** Med IOG slået til regnes strategien i backtest kun 4 gange pr. bar (O, H, L, C), men live på hvert tick [Net: MultiCharts forum "[FAQ] Autotrade / Backtest / Optimization", https://www.multicharts.com/discussion/viewtopic.php?t=10811]. Backtest og virkelighed kan derfor afvige.
- **Anbefaling:** Slå IOG **fra** for alle filtre i fabrikken, medmindre K1 bestemmer andet [Antagelse: enkelhed og sammenlignelighed].

### 1.8 Afrunding og tick-størrelse
- **Hvad:** Beregnede priser (fx "luk + 0,3 × ATR") lander mellem to tilladte prisniveauer. Platformen runder, men måske anderledes i TradeStation og MultiCharts. Også: sammenligning af decimaltal med `=` kan fejle [Antagelse: almindelig egenskab ved kommatal i computere].
- **Opdages:** Rund altid selv til tick-størrelse i koden; test med `>=`/`<=` i stedet for `=`.

### 1.9 Data-fejl og justerede kontrakter
- **Hvad:** Futures skifter kontrakt. "Sammenhængende" dataserier (continuous contracts) kan være pris-justerede, så gamle priser ikke er rigtige handelspriser [Antagelse: standard ved futures-data]. Hvilken data-type projektet bruger, står ikke i rapporten.
- **Opdages:** Konsulent 3's område for selve data; jeg foreslår kun at hvert filter logger datakilde + justeringstype.

### 1.10 Nummerering af filtre
- Et filter blev fjernet, og resten rykkede ét nummer [Rapport: afsnit 6]. Ikke en EasyLanguage-fejl, men en tavs fejl: gamle filer kan pege på forkert filter. **Forslag:** hver signal-fil får en fast, unik nøgle (fx et fingeraftryk af filterets regel), ikke kun et løbenummer.

---

## 2. Kontrolplan for alle ~380 filtre

Idé: Tre lag af automatiske kontroller. Intet af det kræver, at Thomas kan kode. Metoden for stikprøverne (hvor mange, hvilken tolerance) er **K1's**; jeg udfører [Aftale punkt 2].

**Lag 1 – Kodescanning (før kørsel, gratis og hurtig).** Et Python-program læser hver signal-fil og sætter flag:
- funktion med hukommelse i løkke eller med variabel længde (MACD-typen),
- funktionskald inde i `if`,
- `Data2`/højere tidsinterval,
- ordretyper der kan give look-ahead,
- IOG slået til,
- `=` på kommatal.
Resultat: en tabel med ét flag pr. filter og fejltype. Flag betyder "mistænkt", ikke "skyldig".

**Lag 2 – Uafhængig genberegning i Python (stikprøve + alle flaggede).** For hvert udvalgt filter:
1. TradeStation skriver signalets rå værdier ud (dato, tid, indikatorværdi, signal 0/1) til en fil.
2. Python regner det samme ud fra de **samme** prisdata, skrevet fra bunden ud fra lærebogsformlen (ikke kopieret fra TradeStation).
3. Sammenlign bar for bar efter opvarmning. Afvigelse over en tolerance (K1 fastsætter) = rødt.
- Omfang: **alle** filtre med flag fra Lag 1 + de 36 med usikker Max Bars Back + en tilfældig stikprøve af de øvrige [K1: F1 og K1's afsnit 6; størrelsen afhænger af K1].
- Vigtigt: Python-koden skal skrives af en anden (eller i en anden session) end den, der skrev filteret, så de ikke deler samme misforståelse [Antagelse: uafhængighed er hele pointen].

**Lag 3 – Adfærdstests (på alle filtre).**
- Forskydningstest (look-ahead, se 1.4).
- MBB-test (kør med 1000 og 2000).
- Barer pr. dag (sessionsfejl).
- "Dobbeltkørsel": kør samme filter to gange – skal give præcis samme tal (fanger tilfældigheder/tilstand der lækker).

**Hvor resultaterne gemmes:** I en **særskilt** kontroltabel eller test-database, aldrig blandet med produktionsdata [Rapport: princip i afsnit 7]. Ny tabel = databaseændring → den præcise SQL vises og godkendes først [Rapport: afsnit 6]. Hvordan den gemmes, er K3's område.

**Hvis et filter fejler:** Ingen lappeløsning. Filterets signal-fil og resultater slettes, fejlen rettes i skabelonen/generatoren, og filteret bygges forfra [Rapport: princip "ryd op og start forfra"].

### Forslag til de MACD-ramte filtre (Thomas afgør)
Mulighederne, fra mest til mindst forsigtig:
- **A. Genskriv:** Lav egne, "hukommelsesfri" udgaver (en separat instans for hver længde i stedet for ét kald-sted med skiftende længde). Byg alle ramte filtre forfra. Kontroller med Lag 2. *Min anbefaling* [Antagelse: dyrest i tid, men eneste der fjerner fejlen].
- **B. Kør, men karantæne:** Kør dem som nu (med advarsel i filen, som besluttet [Rapport: afsnit 7]), men lad ingen af dem gå videre til EdgeFinder, før de har bestået Lag 2.
- **C. Udelad:** Tag dem ud af første kørsel og tag dem op senere.
- Uanset valg: optæl først **hvor mange** filtre der er ramt (Lag 1 kan gøre det automatisk). Vi ved det ikke i dag.

---

## 3. Oplæg til EdgeCruncher (bygget fra bunden)

**Hvad er den?** EdgeCruncher er i dag kun et navn [Rapport: afsnit 9]. Mit forslag: EdgeCruncher er **leddet, der gør en bevist edge til en handelbar strategi** – med indgang, udgang, stop og omkostninger – og tester den som en rigtig strategi. EdgeFinder siger "der er noget her"; EdgeCruncher siger "sådan handler man det, og sådan ser det ud efter omkostninger" [Antagelse: navnet og kædens rækkefølge tyder på det; Thomas skal bekræfte].

**Placering i kæden:**
RawSignal Creature → RawSignal-Analyse → EdgeFinder → **EdgeCruncher** → (K1's slutkontrol) → Dvale-lager.

**Input:**
- Et signal, der har bestået EdgeFinder, med dets "plateau" af gode indstillinger.
- Marked, tidsinterval, sessionsskabelon.
- Omkostningsmodel (kurtage + glidning pr. handel) – K1/Thomas fastsætter tallene.

**Hvad den gør (skitse):**
1. Bygger en strategi-fil i EasyLanguage ud fra en fast skabelon: signal + et **lille, fast** sæt udgangsregler (fx tidsudgang ved dagens slut, fast stop, fast mål). Få valg = mindre overtilpasning [Antagelse].
2. Tester på **udviklingsdata** over hele plateauet – ikke kun det bedste punkt [K1: F2, F5]. Omkostninger inkl. stresstest med dobbelt omkostning [K1: F7].
3. Vælger indstilling ud fra **midten af plateauet**, ikke toppen, og kører walk-forward efter K1's faste opskrift [K1: F5, F6].
4. EdgeCruncher rører **aldrig** pengeskabs-data (hold-out). Den ene pengeskabs-test [K1: F9] køres af et separat trin, som EdgeCruncher ikke kan styre [Antagelse: så den, der bygger, ikke kan kigge].
5. Tæller og logger **alle** prøvede varianter [K1: F3], så K1's korrektion kan regnes [K1: F4].
6. Kører samme fil i en **uafhængig Python-genberegning** af handlerne (stikprøve), så vi ved, at platformen regner rigtigt.

**Output – et "pas" for strategien** (K1 bestemmer indholdet, K3 hvordan det gemmes [Aftale punkt 2]). Mit forslag til felter, så det kan rumme den foreløbige definition:
- unik nøgle, filter-fingeraftryk, versionsnummer af generator og skabelon,
- marked, interval, session, datakilde og datoer for træning/out-of-sample,
- valgte indstillinger + plateauets grænser,
- antal handler [K1: F10], resultat efter omkostninger [K1: F7], største tab (drawdown), fordeling over år [K1: F8],
- antal prøvede varianter [K1: F3] og resultatet af F4–F10 med tal (K1's krav til passet),
- resultat af alle kontroller fra del 2 (Lag 1–3) og om MACD-typen er ramt,
- selve strategi-filen (kildekoden) og en "kvittering" for, hvilken platform og version den er testet på,
- status: **bestået / ikke bestået / kun TradeStation-verificeret / også MultiCharts-verificeret**.

EdgeCruncher **godkender ikke selv**. Den leverer pas; K1's regler afgør, om strategien er "færdig" [Rapport/opgave: roller må ikke slås sammen].

---

## 4. Byggeplan for RawSignal-Analyse og EdgeFinder

Metoden er **K1's**. Jeg bygger kun det, K1 har godkendt [Aftale punkt 2]. Rækkefølge:

1. **Start den fulde kørsel af RawSignal Creature først?** Det er Thomas' beslutning [Rapport: afsnit 10]. Mit råd: kør Lag 1-kodescanningen på alle 380 **før** den fulde kørsel – det er billigt og kan spare en hel omgang "ryd op og start forfra" [Antagelse].
2. **Fælles dataformat:** Én fast signal-fil-udskrift fra TradeStation (dato, tid, signal, indikatorværdi, filter-nøgle, indstillinger). Alt efterfølgende arbejde foregår i Python på disse udskrifter, ikke inde i TradeStation. Det gør analysen hurtig, gentagelig og nemmere at flytte til MultiCharts [Antagelse].
3. **RawSignal-Analyse (Python):** Plateau-kort over indstillinger, farvning grøn/grå/rød efter K1's regler. Farvereglerne er **ikke afgjort** (plateau-trappen PL1–PL7) [Rapport/opgave eksempel B]. Jeg bygger derfor reglerne som en **indstillingsfil**, så de kan ændres uden at røre koden.
4. **EdgeFinder (Python):** Event-studie = man kigger på, hvad prisen gør i fx 1, 5, 20 barer **efter** hvert signal, og sammenligner med tilfældige tidspunkter. Hvor meget der allerede findes, ved vi ikke – "ikke helt udformet" [Rapport: afsnit 9]. Det er et åbent punkt for Thomas.
5. **Testdata først:** Hvert led bygges og testes på syntetiske (opdigtede) prisdata med en **kendt** indbygget edge og på rene tilfældige data uden edge. Finder EdgeFinder en edge i ren tilfældighed oftere end forventet, er noget galt [Antagelse: standard metode til at teste en test]. Testdata holdes helt adskilt fra produktion.
6. **K1 godkender** hver del, før næste bygges.

---

## 5. Plan for porting til MultiCharts (PowerLanguage)

**Fakta:** MultiCharts' sprog PowerLanguage er i stor grad kompatibelt med klassisk EasyLanguage og kan importere .ELD-filer, men **objekt-orienteret EasyLanguage (OOEL) understøttes ikke**, og nogle indbyggede funktioner opfører sig anderledes [Net: MultiCharts, "PowerLanguage is EasyLanguage-compatible", https://www.multicharts.com/features/easylanguage/] [Net: FreeIndicators, "EasyLanguage Vs PowerLanguage", https://www.freeindicators.com/guides/easylanguage-vs-powerlanguage/].

**Kendte/sandsynlige forskelle, der skal testes:**
- Indbyggede funktioner (samme navn, måske anden formel eller opvarmning) [Net: FreeIndicators, ovenfor].
- Max Bars Back: MultiCharts regner om, når MBB ændres, og første handelsbar er MBB+1 [Net: MultiCharts Wiki, Backtesting Engine, ovenfor].
- IOG i backtest: 4 beregninger pr. bar [Net: MultiCharts FAQ, ovenfor].
- Sessionsskabeloner og datafeed kan give andre barer [Net: MultiCharts Wiki, "Why Identical Charts Show Different Strategy Trading Results", https://www.multicharts.com/trading-software/index.php?title=Why_Identical_Charts_Are_Showing_Different_Strategy_Trading_Results].
- Fjernstyringen af udviklingsmiljøet (de "interne systembeskeder") [Rapport: afsnit 7] virker næsten sikkert **ikke** i MultiCharts' editor og skal bygges forfra [Antagelse: det er et andet program].
- Afrunding til tick-størrelse.

**Sådan beviser vi, at de to platforme giver samme tal:**
1. Brug **identiske** prisdata (samme fil importeret i begge – ikke to forskellige datafeeds). Ellers måler vi dataforskelle, ikke platformforskelle.
2. **Gyldne sæt:** vælg fx 20 filtre, der dækker alle funktionstyper (inkl. MACD-typen). Kør dem i begge.
3. Sammenlign **tre niveauer**: (a) indikatorværdi pr. bar, (b) signal 0/1 pr. bar, (c) handelsliste (tid, pris, resultat).
4. Kriterium: signal og handler skal være **helt ens**; indikatorværdier ens inden for en lille tolerance (K1 fastsætter).
5. Python-genberegningen fra del 2 er den "tredje dommer": hvis de to platforme er uenige, afgør Python, hvem der har ret.
6. Først når det gyldne sæt er ens, flyttes resten. Hvert pas får mærket "også MultiCharts-verificeret".

**Rækkefølge:** Portér ikke, før kæden virker i TradeStation [Rapport/opgave afsnit 3]. Men **byg allerede nu** koden, så den kun bruger klassisk EasyLanguage (ingen OOEL) og egne funktioner i stedet for platformens, hvor det er muligt. Så bliver porten langt billigere [Antagelse].

---

## 6. Nye åbne punkter til Thomas

1. Hvordan skal de MACD-ramte filtre håndteres – A (genskriv), B (karantæne) eller C (udelad)? Og vil du have en automatisk optælling af, hvor mange der er ramt, før du vælger?
2. Må Lag 1-kodescanningen køre på alle 380 filtre **før** den fulde kørsel startes?
3. Er min forståelse af EdgeCruncher rigtig ("gør en edge til en handelbar strategi med omkostninger")? Eller havde du noget andet i tankerne?
4. Hvilke handelsomkostninger (kurtage og glidning) skal bruges pr. marked?
5. Skal IntrabarOrderGeneration være slået fra i hele fabrikken?
6. Hvilken type prisdata bruges (justeret sammenhængende futures-serie eller ej), og er sessionsskabelonen fast?
7. Må signal-filer få en fast unik nøgle (fingeraftryk) ud over løbenummeret, så nummerskift ikke kan forvirre?
8. Må de 36 filtre med ukendt MBB-behov testes med både 1000 og 2000?
9. Hvem skriver Python-kontrolberegningerne, så de er uafhængige af den, der byggede filtrene?
10. Skal MultiCharts-porten bruge samme datafil som TradeStation (anbefalet), og hvilken MultiCharts-version?

---

**Hvad mangler i dette udkast:** Ingen fejl er afprøvet i praksis – listen i del 1 er kendte fejltyper, ikke fundne fejl i projektets kode. Listen over "funktioner med hukommelse" (1.1) skal verificeres én for én. Tolerance og stikprøvestørrelse venter på K1. EdgeCruncher-oplægget er et forslag, som Thomas skal bekræfte.


# Del 3 – Konsulent 3: Data- og pipeline-arkitekt

*Dvale-lager, automatisering og dataflow. Udkast skrevet på ca. 10 minutter. Alt er råd, ikke beslutninger. Al SQL nedenfor er FORSLAG, som ikke må køres, før Thomas har set og godkendt den præcise kommando.*

**Hvor jeg afhænger af Konsulent 1:** Konsulent 1 bestemmer, HVAD en "færdig strategi" skal have bestået. Hans definition hedder **F1–F10** (se del 1). Passet nedenfor er bygget til at rumme F1–F10 og det pas-indhold, K1 kræver. Steder, der stadig afhænger af tal eller valg, K1/Thomas ikke har lagt fast (fx plateau-niveau, grænser), er markeret med **[AFH. K1]**. Designet er lavet, så nye felter kan tilføjes uden at ændre tabellerne (se afsnit 3).

Fagord forklares første gang, de bruges.

---

## 1. Kritik af det eksisterende dataflow

**1a. Filternumre der skifter (det alvorligste).** Da ét filter blev fjernet fra `filter_case`, rykkede alle efterfølgende filtre ét nummer ned [Rapport]. Det betyder, at "filter 200" i et gammelt dokument ikke længere er det samme som "filter 200" i dag. For en fabrik, der skal gemme strategier i årevis og senere vække dem, er det farligt: en strategi i dvale kunne pege på det forkerte filter, uden at nogen opdager det. At det er skrevet ned i Videnslog [Rapport], er godt, men det er en papirløsning på et strukturproblem. Et nummer, der viser en *plads i en liste*, må aldrig bruges som *navn* på en ting. [Antagelse: almindelig databasepraksis; et navn skal være permanent.]

**1b. Fjernelse i stedet for markering.** At filteret blev slettet (i stedet for at blive markeret "udgået") gør, at historikken forsvinder [Antagelse: rapporten siger "fjernet", ikke "markeret"]. Hvis `rawsignal` eller senere tabeller havde peget på det, ville de pege ud i luften eller på et andet filter.

**1c. Test og produktion i samme tabeller.** De 13 testfiltre blev kørt ind i databasen og bagefter "ryddet ud" igen [Rapport]. Princippet (aldrig blande test og produktion) er rigtigt, men metoden er skrøbelig: den afhænger af, at oprydningen husker hver eneste række i hver tabel. Én glemt række er nok til at forurene produktionsdata. Adskillelsen bør ligge i *strukturen* (separat database), ikke i en manuel oprydning. [Antagelse.]

**1d. Forældet dokumentation (Noter.md).** Dele af Noter.md er forældede, og det står i selve filen [Rapport]. Når der skal køre flere maskiner automatisk, bliver det værre: en maskine, der er sat op efter en gammel note, laver "rigtige" resultater på forkerte forudsætninger. Løsning: de regler, maskinerne skal følge (fx Max Bars Back = 1000 [Rapport]), bør stå i databasen eller i én versioneret opsætningsfil, som programmet læser – ikke kun i en note, som et menneske skal huske at læse. [Antagelse.]

**1e. Ingen kodeversion på resultaterne.** Rapporten nævner ikke, at `rawsignal` gemmer hvilken version af programmet/skabelonen der lavede signal-filen [Rapport: ikke nævnt – vi ved det ikke]. Uden det kan man ikke senere sige, hvilke resultater der skal laves om, hvis en fejl findes (fx MACD-fejlen [Rapport]). Med princippet "ryd op og start forfra" [Rapport] *skal* man kunne finde præcis de rækker, der skal ryddes.

**1f. Kun ét led har en database-kontrakt.** Kun RawSignal Creature skriver i dag til databasen (`rawsignal`, `rawsignal_kontrol`) [Rapport]. De næste fire led har ingen tabeller. Der er risiko for, at hvert nyt led opfinder sin egen måde (egne CSV-filer, egne mapper), og så ender det som et rod af enkeltfiler – præcis det opgaven advarer mod.

**1g. Én maskine, ingen kø.** I dag kører alt på Thomas' ene server, styret af ét Python-program, der fjernstyrer TradeStation ved at sende Windows-beskeder (samme beskeder som et museklik) [Rapport]. Der er ingen kø (en liste af opgaver, som maskiner tager fra) og ingen måde at fordele arbejdet på.

---

## 2. Arkitekturtegning

Ideen: **databasen er midten af alt.** Hvert led henter sit arbejde fra en fælles opgave-kø i databasen og skriver sit resultat tilbage. Intet led taler direkte med et andet led. Filer (signal-filer, rapporter) gemmes i et fast fil-lager, og databasen husker hvor.

```
                   +--------------------------------------------+
                   |          TradingDB (PostgreSQL)            |
                   |                                            |
                   |  filter_case  (faste ID'er, aldrig slettet)|
                   |  koersel      (hvilken kørsel/kodeversion) |
                   |  job          (opgave-kø for alle led)     |
                   |  rawsignal / rawsignal_kontrol             |
                   |  analyse_resultat  (led 2)                 |
                   |  edge_resultat     (led 3)                 |
                   |  strategi_kandidat (led 4)                 |
                   |  dvale_strategi + dvale_pas  (led 5)       |
                   +---^-------^--------^--------^--------^-----+
                       |       |        |        |        |
      henter job /     |       |        |        |        |
      skriver resultat |       |        |        |        |
                 +-----+--+ +--+-----+ +-+------+ +-------+--+ +------------+
 filter_case --> | 1. Raw | | 2. Raw | | 3.Edge | | 4. Edge  | | 5. Dvale-  |
                 | Signal |>| Signal |>| Finder |>| Cruncher |>|   lager    |
                 |Creature| |Analyse | |        | |          | | (pas+arkiv)|
                 +---+----+ +--------+ +--------+ +----+-----+ +-----+------+
                     |                                 |             |
                     v                                 v             v
             +------------------------------------------------------------+
             |  Fil-lager (én fast mappe-struktur, kun-tilføj):           |
             |  /lager/<miljø>/<kørsel-id>/<filter-uid>/...               |
             |  Databasen gemmer sti + kontrolsum (fingeraftryk) af filen |
             +------------------------------------------------------------+

 Arbejdere (maskiner):  PC-A [TradeStation]  PC-B [TradeStation]  PC-C [ren Python]
   Hver arbejder: "giv mig næste job af en type, jeg kan klare" -> kør -> aflever.
 Overvågning: én skærm (TradingApp) der kun LÆSER fra job- og koersel-tabellerne.
```

Pilene mellem led 1–5 viser *rækkefølgen*, ikke direkte forbindelser: når et job i led 2 er færdigt, lægger det selv et nyt job i køen til led 3. [Antagelse: enkleste måde at få et stabilt dataflow på.]

**Miljøer (test vs. produktion):** To helt adskilte databaser: `TradingDB` (produktion) og `TradingDB_test` (test), og to adskilte fil-mapper. Programmet får at vide, hvilken det skal bruge, via én opsætningsfil, og skriver altid miljøets navn øverst i alle logs og på skærmen. [Antagelse: strukturel adskillelse er sikrere end oprydning, jf. 1c.] Man kunne i stedet bruge to "schemaer" (rum) i samme database – det er billigere, men en fejl i én indstilling kan stadig blande dem. Jeg anbefaler separate databaser; det er et åbent punkt til Thomas.

---

## 3. Dvale-lageret

### 3a. Principper
1. **Faste ID'er, der aldrig skifter.** Hvert filter og hver strategi får et permanent ID (en UUID – en lang tilfældig kode, der er unik i hele verden – plus et kort, menneskevenligt navn som `STR-000123`). Rækkefølgenummeret i en liste bruges aldrig som navn. [Antagelse: løser 1a.]
2. **Aldrig slette, aldrig ændre – kun tilføje.** En gemt strategi og dens pas ændres aldrig. Ny test = ny version. Udgåede ting markeres `status = 'udgaaet'`. [Antagelse: passer med "start forfra"-princippet: man laver en ny ren version i stedet for at lappe den gamle.]
3. **Alt peger bagud.** En strategi i dvale peger på præcis det filter, den kørsel, den kodeversion og det datasæt, den kom fra – så den kan genskabes og efterprøves. [Antagelse.]
4. **Filen i fil-lageret, fakta i databasen.** Selve EasyLanguage-koden og tunge rapporter ligger som filer; databasen gemmer stien og en kontrolsum (SHA-256 – et digitalt fingeraftryk, der ændrer sig, hvis ét tegn i filen ændres). Så kan man altid se, om en fil er blevet pillet ved. [Antagelse.]

### 3b. Tabeldesign – FORSLAG (må ikke køres uden godkendelse)

Først en rettelse af filter-ID'et. Jeg kender ikke `filter_case`'s kolonner [Rapport nævner dem ikke], så dette er kun en skitse:

```sql
-- FORSLAG 1: Giv hvert filter et permanent ID, der aldrig ændres.
-- Kræver først et kig på filter_case's nuværende struktur. Ikke kørt.
ALTER TABLE filter_case ADD COLUMN filter_uid UUID NOT NULL DEFAULT gen_random_uuid();
ALTER TABLE filter_case ADD CONSTRAINT filter_case_uid_unik UNIQUE (filter_uid);
ALTER TABLE filter_case ADD COLUMN status TEXT NOT NULL DEFAULT 'aktiv'
      CHECK (status IN ('aktiv','udgaaet'));
```
Bemærk: `gen_random_uuid()` er indbygget fra PostgreSQL 13 [Antagelse: fra min viden om PostgreSQL; Thomas' version kendes ikke]. Da den fulde kørsel ikke er startet [Rapport], er **nu** det billigste tidspunkt at indføre faste ID'er.

```sql
-- FORSLAG 2: Én række pr. kørsel, så alle resultater kan spores til kodeversion og data.
CREATE TABLE koersel (
    koersel_id     BIGSERIAL PRIMARY KEY,
    led            TEXT NOT NULL,          -- 'creature','analyse','edgefinder','cruncher'
    kodeversion    TEXT NOT NULL,          -- fx git-commit-kode
    opsaetning     JSONB NOT NULL,         -- fx max_bars_back=1000, platform='TradeStation'
    datasaet       TEXT NOT NULL,          -- instrument, bar-størrelse, datakilde
    periode_fra    DATE, periode_til DATE,
    status         TEXT NOT NULL DEFAULT 'igang'
                   CHECK (status IN ('igang','faerdig','kasseret')),
    startet        TIMESTAMPTZ NOT NULL DEFAULT now(),
    afsluttet      TIMESTAMPTZ
);

-- FORSLAG 3: Selve dvale-lageret. Én række pr. strategi-VERSION. Ændres aldrig.
CREATE TABLE dvale_strategi (
    strategi_uid     UUID NOT NULL,                 -- samme for alle versioner af strategien
    version          INT  NOT NULL,                 -- 1, 2, 3 ...
    kort_navn        TEXT NOT NULL,                 -- 'STR-000123'
    filter_uid       UUID NOT NULL,                 -- peger på filter_case.filter_uid
    koersel_id       BIGINT NOT NULL REFERENCES koersel(koersel_id),
    platform         TEXT NOT NULL CHECK (platform IN ('TradeStation','MultiCharts')),
    kode_sti         TEXT NOT NULL,                 -- sti i fil-lageret
    kode_sha256      TEXT NOT NULL,                 -- fingeraftryk af koden
    status           TEXT NOT NULL DEFAULT 'dvale'
                     CHECK (status IN ('dvale','vakt','udgaaet')),
    oprettet         TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (strategi_uid, version)
);

-- FORSLAG 4a: Datadelingen (K1's F2). Låses FØR første test og ændres aldrig.
-- Hver kørsel skal pege på én datadeling (tilføj kolonnen datadeling_id i koersel).
CREATE TABLE datadeling (
    datadeling_id    BIGSERIAL PRIMARY KEY,
    marked           TEXT NOT NULL,
    udvikling_fra    DATE NOT NULL, udvikling_til  DATE NOT NULL,
    validering_fra   DATE NOT NULL, validering_til DATE NOT NULL,
    pengeskab_fra    DATE NOT NULL, pengeskab_til  DATE NOT NULL,   -- hold-out, sidst i tiden
    laast            TIMESTAMPTZ NOT NULL DEFAULT now(),
    CHECK (udvikling_til < validering_fra AND validering_til < pengeskab_fra)
);
-- Ingen må rette eller slette en datadeling bagefter (rollenavn er et eksempel):
REVOKE UPDATE, DELETE ON datadeling FROM pipeline_bruger;

-- FORSLAG 4b: "Pengeskabet åbnes én gang" (K1's F9) – håndhævet af databasen selv.
-- UNIQUE på strategi_uid (ikke version): en ny version af samme strategi kan
-- IKKE få en ny chance på pengeskabet. Rækken kan hverken rettes eller slettes.
CREATE TABLE pengeskab_aabning (
    strategi_uid     UUID PRIMARY KEY,          -- én åbning pr. strategi, for altid
    version          INT  NOT NULL,
    datadeling_id    BIGINT NOT NULL REFERENCES datadeling(datadeling_id),
    antal_handler    INT  NOT NULL,             -- F10 (hold-out-delen)
    resultat         JSONB NOT NULL,
    bestaaet         BOOLEAN NOT NULL,
    aabnet           TIMESTAMPTZ NOT NULL DEFAULT now()
);
REVOKE UPDATE, DELETE ON pengeskab_aabning FROM pipeline_bruger;

-- FORSLAG 4c: Strategiens "pas". Én kolonne pr. krav F1–F10, så man kan sortere og
-- sammenligne. Tallene bag hvert krav ligger i pas_detaljer. Grænserne er [AFH. K1].
CREATE TABLE dvale_pas (
    strategi_uid        UUID NOT NULL,
    version             INT  NOT NULL,
    pas_skabelon        TEXT NOT NULL,   -- hvilken version af K1's definition, fx 'K1-F1..F10-v1'
    datadeling_id       BIGINT NOT NULL REFERENCES datadeling(datadeling_id),  -- F2
    antal_forsoeg       INT NOT NULL,    -- F3: alle prøvede varianter i runden (også fra EdgeCruncher)
    deflated_sharpe     NUMERIC,         -- F4
    fdr_niveau          NUMERIC,         -- F4
    plateau_niveau      TEXT CHECK (plateau_niveau ~ '^PL[1-7]$'),  -- F5 [AFH. Thomas]
    antal_handler_udv   INT,             -- F10 (udviklingsdata)
    f1_ok BOOLEAN NOT NULL, f2_ok BOOLEAN NOT NULL, f3_ok BOOLEAN NOT NULL,
    f4_ok BOOLEAN NOT NULL, f5_ok BOOLEAN NOT NULL, f6_ok BOOLEAN NOT NULL,
    f7_ok BOOLEAN NOT NULL, f8_ok BOOLEAN NOT NULL, f10_ok BOOLEAN NOT NULL,
    -- F9 står ikke her: den står i pengeskab_aabning og kan ikke skrives om.
    kendte_risici       TEXT[],          -- fx '{MACD,MaxBarsBack-usikker}' (K1 + K2)
    parametre           JSONB NOT NULL,  -- valgte indstillinger + plateauets grænser (K2)
    platform_verificeret TEXT[] NOT NULL,-- '{TradeStation}' eller '{TradeStation,MultiCharts}' (K2)
    pas_detaljer        JSONB NOT NULL,  -- alle tal bag F1–F10, drawdown, kontroller Lag 1–3 (K2)
    oprettet            TIMESTAMPTZ NOT NULL DEFAULT now(),
    PRIMARY KEY (strategi_uid, version),
    FOREIGN KEY (strategi_uid, version) REFERENCES dvale_strategi(strategi_uid, version)
);
REVOKE UPDATE, DELETE ON dvale_pas FROM pipeline_bruger;

-- En strategi må kun få status 'dvale', hvis F1–F8 + F10 er sande OG pengeskabet
-- er åbnet én gang og bestået. Det tjekkes i én fast VIEW, som er den ENESTE vej ind:
CREATE VIEW faerdig_strategi AS
SELECT p.* FROM dvale_pas p
JOIN pengeskab_aabning k ON k.strategi_uid = p.strategi_uid AND k.version = p.version
WHERE p.f1_ok AND p.f2_ok AND p.f3_ok AND p.f4_ok AND p.f5_ok AND p.f6_ok
  AND p.f7_ok AND p.f8_ok AND p.f10_ok AND k.bestaaet;
```

**Hvorfor databasen skal håndhæve F9:** K1's krav "pengeskabet åbnes kun én gang" er det, der lettest brydes i det stille – et menneske eller en AI justerer "bare lidt" og tester igen. En regel i en note kan glemmes; en `PRIMARY KEY` på `strategi_uid` kan ikke. Forsøg på en anden åbning giver en fejl, som vises på overvågningsskærmen. [Antagelse: en regel håndhævet af databasen er stærkere end en regel i en vejledning.] Svaghed: det forhindrer ikke, at man opretter en "ny" strategi med nyt ID for at snyde – derfor bør `antal_forsoeg` (F3) også tælle kasserede strategier fra samme filter. [AFH. K1]

**Adgangskontrol til pengeskabs-data:** K1 kræver, at ingen ser hold-out-data før til sidst. Pengeskabs-perioden bør derfor ikke kunne hentes af led 2–4. Enkleste løsning: prisdata for pengeskabs-perioden hentes kun af ét lille program ("pengeskabs-åbneren"), som samtidig skriver i `pengeskab_aabning`. [Antagelse; hvordan prisdata ligger i dag, ved vi ikke.]

Hvorfor både faste kolonner og et JSONB-felt (et felt, der kan rumme en hel struktureret "seddel")? Fordi grænserne i F1–F10 og det præcise indhold af hver test stadig kan ændre sig. Det, der skal **sammenlignes og sorteres på** (bestået/dumpet pr. F-krav, antal forsøg, DSR, plateau), er faste kolonner; tallene bag ligger i `pas_detaljer`. [Antagelse.] Kolonnen `pas_skabelon` gør, at pas skrevet efter en gammel definition ikke forveksles med nye.

### 3c. Sammenligne og hente frem
- **Sammenligne:** Ét fast "udsigtsvindue" (en VIEW – en gemt forespørgsel, der ser ud som en tabel) viser alle strategier i dvale med de vigtigste pas-tal side om side. Den kan åbnes i TradingApp eller Excel. [Antagelse.]
- **Hente frem ("vække"):** Man vælger `STR-000123 v2`. Systemet henter koden fra fil-lageret, **tjekker fingeraftrykket**, og nægter at fortsætte hvis det ikke passer. Status sættes til `vakt` (en ny hændelse logges – det gamle slettes ikke). [Antagelse.]
- **Genkontrol:** Fordi alt peger bagud (filter, kodeversion, datasæt, periode), kan en strategi køres igen på samme data, og resultatet skal ramme passet. Gør det ikke det, er noget galt – og strategien vækkes ikke. [Antagelse.]

---

## 4. Automatisering over flere computere

### 4a. Kø af jobs i databasen
Én tabel `job`, som alle maskiner henter opgaver fra. PostgreSQL har en indbygget funktion, `FOR UPDATE SKIP LOCKED`, der gør det muligt for mange maskiner at tage fra samme kø samtidig, uden at to maskiner får samme opgave, og hvor en opgave automatisk frigives, hvis maskinen går ned midt i "tag-opgaven"-trinnet [Net: "PostgreSQL FOR UPDATE SKIP LOCKED: The One-Liner Job Queue", https://www.dbpro.app/blog/postgresql-skip-locked; og officiel dokumentation "PostgreSQL: Documentation: SELECT", https://www.postgresql.org/docs/current/sql-select.html]. Så behøver vi ikke et ekstra system (fx Redis eller RabbitMQ) – enkelt er bedre.

```sql
-- FORSLAG 5: Opgave-køen. Ikke kørt.
CREATE TABLE job (
    job_id        BIGSERIAL PRIMARY KEY,
    koersel_id    BIGINT NOT NULL REFERENCES koersel(koersel_id),
    led           TEXT NOT NULL,
    filter_uid    UUID,
    kraever       TEXT NOT NULL,     -- 'tradestation' eller 'python' (hvad maskinen skal have)
    status        TEXT NOT NULL DEFAULT 'venter'
                  CHECK (status IN ('venter','koerer','faerdig','fejlet')),
    maskine       TEXT,
    forsoeg       INT NOT NULL DEFAULT 0,
    sidst_livstegn TIMESTAMPTZ,      -- maskinen melder "jeg lever" hvert minut
    fejltekst     TEXT
);

-- Sådan tager en maskine næste job (vises kun som eksempel):
-- UPDATE job SET status='koerer', maskine=:mig, forsoeg=forsoeg+1, sidst_livstegn=now()
-- WHERE job_id = (SELECT job_id FROM job
--                 WHERE status='venter' AND kraever=:min_evne
--                 ORDER BY job_id FOR UPDATE SKIP LOCKED LIMIT 1)
-- RETURNING *;
```

### 4b. Fejlsikring: ingen halve resultater
- **Alt-eller-intet:** Et job skriver sit resultat i én databasetransaktion (en pakke af ændringer, der enten gemmes helt eller slet ikke). Filer skrives først til en midlertidig mappe og flyttes først på plads, når alt er gået godt. [Antagelse: standardpraksis.]
- **Start forfra, aldrig lappe:** Går en maskine ned (intet livstegn i fx 10 min.), sættes jobbet til `fejlet`, dets midlertidige filer slettes, og et **helt nyt** forsøg lægges i køen. Et halvt færdigt job bliver aldrig "fortsat". Det følger projektets princip [Rapport].
- **Stop efter 3 fejl** på samme job: så kræver det et menneske. Det forhindrer, at en defekt fil kører i ring. [Antagelse.]
- **Hel kørsel kasseres samlet:** Findes en fejl i kode eller opsætning (fx en ny MACD-lignende fejl), markeres hele `koersel` som `kasseret`, og en ny kørsel startes fra bunden. Fordi alt er mærket med `koersel_id`, er det let at finde. [Antagelse.]

### 4c. TradeStation og flere maskiner – det svære punkt
- Fjernstyringen sker via Windows-beskeder uden API [Rapport]. Det er skrøbeligt: to programmer, der styrer den samme TradeStation på én gang, vil forstyrre hinanden. **Anbefaling: én TradeStation-instans pr. maskine og kun én arbejder pr. instans.** [Antagelse: uden API er der ingen sikker måde at køre to styringer parallelt i samme program.]
- **Advarsel om login:** Et søgeresultat angiver, at TradeStation kan installeres på flere computere, men kun være logget ind på én computer ad gangen [Net: søgeresultat-uddrag fra "Installation Instructions (TradeStation) – Trade Automation Toolbox", https://support.tradeautomationtoolbox.com/hc/en-us/articles/43583636549267-Installation-Instructions-TradeStation – siden kunne ikke åbnes og er **ikke bekræftet**]. Hvis det passer, kræver flere TradeStation-maskiner flere konti/licenser, og det kan gøre skalering dyr eller umulig. **Det skal Thomas afklare med TradeStation før der bygges.** Vi ved det ikke.
- **Del arbejdet efter evne:** Mange trin kræver slet ikke TradeStation. Når RawSignal Creature har kørt signalerne og eksporteret deres rå handler/signaler til databasen, kan RawSignal-Analyse og store dele af EdgeFinder køres som ren Python på almindelige maskiner (kolonnen `kraever`). Så er TradeStation kun flaskehals der, hvor den er uundgåelig. [Antagelse: afhænger af K2's design af EdgeFinder/EdgeCruncher.]
- MultiCharts senere: køen er platform-neutral – et job siger bare `kraever='multicharts'`. Det gør porting lettere [Antagelse]. Der findes også færdige kommercielle værktøjer til at fordele TradeStation/MultiCharts-backtests på flere maskiner (fx MultiWalk) [Net: søgeresultat "Can I run MultiWalk on multiple computers?", https://multiwalk.net/knowledge-base/can-i-run-multiwalk-on-multiple-computers/ – siden kunne ikke åbnes]; det bør overvejes før der bygges selv. Ikke undersøgt nærmere.

### 4d. Overvågning
- Én oversigt (i TradingApp): hvor mange jobs venter / kører / er færdige / fejlede, pr. led og pr. kørsel, og hvilke maskiner har sendt livstegn for nylig. Den **læser kun** – den ændrer intet. [Antagelse.]
- Rød lampe hvis: en maskine er tavs, et job har fejlet 3 gange, eller en kørsel ikke har flyttet sig i X minutter.
- Én samlet log-tabel frem for log-filer spredt ud på maskinerne. [Antagelse.]

---

## 5. Plug-and-play: sådan kører Thomas det uden kode

1. **Én opsætningsfil pr. maskine**, med kun tre linjer: miljø (test/produktion), maskinens navn, og hvad den kan (`tradestation` eller `python`). Ingen andre indstillinger på maskinen – alt andet hentes fra databasen. [Antagelse.]
2. **Én knap for at starte en maskine** ("Start arbejder"). Den tager selv jobs, til køen er tom.
3. **I TradingApp fire knapper:** "Ny kørsel" (vælg led, datasæt, periode – systemet laver alle jobs), "Se fremdrift", "Kassér kørsel og start forfra", "Vis dvale-lager".
4. **Alle database-ændringer, der ikke er rutine** (nye tabeller, sletninger), vises som tekst med knapperne "Godkend" / "Afvis", før de sker – så projektets regel overholdes også af maskinerne. Rutine-skrivninger (et job afleverer sit resultat) er godkendt én gang for alle som en del af designet [Antagelse – Thomas skal bekræfte, at det er i orden, se åbne punkter].
5. **Test først, altid:** En ny kørsel kan først startes i produktion, når den samme kodeversion har kørt grønt i testmiljøet. [Antagelse.]

---

## 6. Vejledning i almindeligt sprog

Forestil dig et stort køkken med mange kokke.

- **Databasen er tavlen på væggen.** På tavlen står alle opgaver, der skal laves. Kokkene (computerne) går hen til tavlen, tager én seddel, laver retten og hænger resultatet op. To kokke kan aldrig tage samme seddel.
- **Hver ting har et navneskilt, der aldrig skiftes.** Før fik filtrene numre efter deres plads i køen – så når én gik hjem, fik alle bagved et nyt nummer. Nu får hver sit eget navneskilt for altid.
- **Går noget galt, smider vi retten ud og laver den forfra.** Vi prøver aldrig at redde en halvbrændt ret.
- **Øvekøkkenet er et andet rum.** Det vi øver på, kommer aldrig ind i det rigtige køkken.
- **Dvale-lageret er fryseren.** En færdig strategi lægges i en æske med en mærkat (passet): hvad den er lavet af, hvornår, med hvilken opskrift, og hvilke prøver den har bestået. Æsken må aldrig åbnes og ændres. Laver man den om, bliver det en ny æske med nyt versionsnummer.
- **Når en strategi skal vækkes,** tjekker systemet først, at æsken er præcis som da den blev frosset (fingeraftrykket), og smager den igen, før den bruges.
- **Thomas trykker kun på knapper:** "Start", "Se hvordan det går", "Kassér og start forfra" og "Vis fryseren".

---

## 7. Nye åbne punkter til Thomas

1. **Faste filter-ID'er:** Skal `filter_case` have et permanent ID (og "udgået" i stedet for sletning) *før* den fulde kørsel af de 380 filtre startes? (Jeg anbefaler ja, men det er din beslutning.)
2. **Test-adskillelse:** Separat testdatabase (min anbefaling) eller separat schema i samme database?
3. **TradeStation-licens:** Hvor mange computere må være logget ind samtidig på din konto? Dette afgør, om fordeling over flere TradeStation-maskiner overhovedet er muligt, og hvad det koster. Ikke bekræftet.
4. **Rutine-skrivninger:** Er det i orden, at godkendte programmer (fx et job der afleverer sit resultat) skriver i databasen uden at spørge hver gang, når selve programmet og tabellerne er godkendt? Ellers kan automatisering ikke lade sig gøre.
5. **Kodeversion:** Gemmer `rawsignal` i dag hvilken kodeversion der lavede hver fil? Hvis ikke: skal det tilføjes før den fulde kørsel?
6. **PostgreSQL-version** på serveren (påvirker enkelte kommandoer).
7. **Fil-lager:** Hvor skal filerne bo (serverens disk, netværksdrev, backup)? Og hvordan tages backup af TradingDB i dag?
8. **Købe eller bygge:** Skal et færdigt værktøj til fordeling af backtests (fx MultiWalk) undersøges, før vi bygger selv?
9. **Pas-indhold [AFH. K1]:** Når Konsulent 1's "færdig strategi"-definition er klar, skal felterne i `dvale_pas` gennemgås og godkendes – og hvilket plateau-niveau (PL1–PL7) er nok til dvale? (Hører sammen med plateau-trappen i opgavens punkt 9.)
10. **Noter.md:** Skal de regler, maskinerne kører efter (fx Max Bars Back = 1000), flyttes fra noter til en versioneret opsætning, som programmet læser?

**Hvad der mangler i dette udkast (ærligt):** Ingen detaljeret tabel for led 2–4 (`analyse_resultat`, `edge_resultat`, `strategi_kandidat`) – de afhænger af K1's metoder og K2's EdgeCruncher-design. Ingen backup-plan. Login-begrænsningen hos TradeStation er ikke bekræftet. Intet af SQL'en er afprøvet mod den rigtige database, som jeg ikke har adgang til.


# Del 4 – Samlet overblik (den overordnede agent)

*Jeg har ikke rettet i konsulenternes dele. Nedenfor er mit overblik over, hvordan delene hænger sammen, hvor konsulenterne er enige og uenige, og hvad Thomas skal afgøre.*

## 4.1 Sådan hænger delene sammen

Alle tre dele bygger nu på den samme definition af "færdig strategi", Konsulent 1's F1–F10. Både K2 og K3 skrev deres udkast om i runde 2, så de henviser til den. Kæden ser sådan ud, når man lægger de tre dele sammen:

1. **RawSignal Creature** laver signal-filerne. Før den fulde kørsel foreslår K2 en automatisk kodegennemgang (Lag 1), og K3 foreslår faste filter-ID'er og en kodeversion på hver kørsel.
2. **RawSignal-Analyse** (bygges i Python af K2) sorterer groft efter K1's metode. Den tjekker signalernes sundhed, måler effekten mod tilfældige tidspunkter, laver plateau-kort og en false discovery rate-sortering. Plateau-farverne ligger i en indstillingsfil, så Thomas kan ændre dem uden at røre koden.
3. **EdgeFinder** (event-studie, K2 bygger) skal opfylde K1's krav E1–E8. Den vigtigste prøve er, at metoden hverken må finde for mange "edges" i rene tilfældige signaler eller overse en edge, som man selv har lagt ind.
4. **EdgeCruncher** er K2's forslag. Den gør en bevist edge til en strategi, man kan handle med: indgang, udgang, stop og omkostninger. Den tæller alle sine forsøg og rører aldrig pengeskabet.
5. **Pengeskabs-åbneren** er et lille, separat trin, som både K2 og K3 nu foreslår. Det er det eneste, der må hente pengeskabs-data (F9). Databasen sørger for, at det kun kan ske én gang pr. strategi.
6. **Dvale-lageret** (K3) er tabeller, man kun kan lægge ting i. Hver strategi har et pas og et fingeraftryk af sin kode, og der er kun én vej ind: visningen `faerdig_strategi`.

## 4.2 Hvor konsulenterne er enige

- Fuld enighed om, at en strategi ikke må kaldes "færdig", hvis den kan være ramt af MACD-typen af fejl og ikke er kontrolleret. [K1, K2]
- Fuld enighed om at tælle alle forsøg (F3) og om, at pengeskabet kun åbnes én gang af et separat trin. [K1, K2, K3 efter runde 2]
- Fuld enighed om at flytte tungt regnearbejde fra TradeStation til Python, så længe Python kontrolleres mod TradeStation. [K2, K3 – K1 har ikke indvendinger]
- Fuld enighed om én TradeStation pr. maskine og en opgaveliste i databasen. [K2, K3]
- Fuld enighed om at teste hele fabrikken med kendt-tilfældige signaler ("placebo") og signaler med en indlagt edge. Disse testdata skal holdes adskilt fra produktion. [K1, K2]
- Fuld enighed om at alt skal kunne ryddes og køres forfra pr. kørsel, aldrig lappes. [Alle – følger projektets princip]

## 4.3 Hvor konsulenterne er uenige (vist åbent)

| # | Emne | Synspunkt A | Synspunkt B | Status efter runde 2 |
|---|------|-------------|-------------|----------------------|
| U1 | **MACD-ramte filtre** | K2 anbefaler at genskrive dem (A). | K1 kan også godkende karantæne (B), men aldrig at en ramt strategi bliver "færdig" uden kontrol. | Delvis enighed. Thomas vælger mellem A, B og C. |
| U2 | **EdgeCruncher og "out-of-sample"** | K2's første udkast lod EdgeCruncher teste på out-of-sample. | K1 og K3: kun et separat trin må åbne pengeskabet. | **Løst.** K2 har rettet sit udkast. EdgeCruncher bruger kun validerings-data. |
| U3 | **Størrelse på stikprøven** | K2's første udkast: ca. 10 % af filtrene. | K1: mindst 38 tilfældige plus alle mistænkte. | I praksis løst. K2 overlader størrelsen til K1. |
| U4 | **PL1–PL7 låst i databasen** | K3's tabel tillader kun PL1–PL7. | K1: det afgør i praksis Thomas' åbne punkt om, hvor mange niveauer trappen skal have. | **Ikke løst.** K3's udkast har stadig låsen. |
| U5 | **Filter-ID** | K1: filter-ID *og* filter-version. | K3: ét permanent ID (UUID). Versionsnumre er ikke afklaret. | Ikke løst. Thomas afgør det. |
| U6 | **Hvor kontrolresultater gemmes** | K2: i en særskilt kontroltabel eller testdatabase. | K3: kontroller af rigtige filtre er produktionsdata. Kun opdigtede testsignaler hører til i testdatabasen. | Ikke løst. |
| U7 | **Hvor strenge signalerne skal være** | K1: 100 % enighed om, hvornår et signal tænder. | K2: enig, men afrunding kan give sjældne vip lige på grænsen, og der mangler en regel for det. | Åbent teknisk punkt. |
| U8 | **Købe eller bygge fordelingen** | K3: overvej færdigt værktøj (fx MultiWalk). | K2: et lukket værktøj gør det svært at bevise tællingen af forsøg (F3). | Ikke undersøgt nærmere. |

## 4.4 Den overordnede agents egne bemærkninger

- **Én ting kan ramme projektets egen regel.** K3 gør opmærksom på noget vigtigt: En fuldautomatisk fabrik skriver i databasen tusindvis af gange. Reglen siger, at hver ændring først skal vises og godkendes. Hvis reglen tages bogstaveligt, kan fabrikken ikke køre automatisk. Thomas skal derfor afgøre, om en godkendelse af selve programmet og tabellerne også dækker de almindelige resultater, som programmet skriver bagefter. [Antagelse: det er et spørgsmål om at fortolke reglen, ikke om teknik.]
- **TradeStation-login er et stop-punkt.** Hvis kontoen kun må være logget ind på én computer ad gangen, holder planen om flere TradeStation-maskiner ikke. Så skal endnu mere arbejde flyttes til Python. Det bør afklares, før der bygges på den del. [Net-oplysningen hos K3 er ikke bekræftet.]
- **Plug-and-play mod stringens.** Forslagene gør fabrikken mere sikker, men også større. Knapperne i K3's forslag (Start, Se fremdrift, Kassér, Vis dvale-lager) skal gemme hele den kompleksitet væk for Thomas. Det har ingen konsulent tegnet i detaljer endnu. [Antagelse.]
- **Rækkefølge.** Gruppen anbefaler den samme rækkefølge fra flere vinkler. Først laves de billige ting før den fulde kørsel: faste ID'er, kodeversion, låst datadeling, kodegennemgang (Lag 1) og testen af Max Bars Back med 1000 og 2000. Derefter startes den fulde kørsel, hvis Thomas beslutter det. Så bygges RawSignal-Analyse med placebo-testen. Derefter EdgeFinder og til sidst EdgeCruncher. MultiCharts kommer til sidst, men koden skal allerede nu undgå objekt-orienteret EasyLanguage. [Antagelse: samlet ud fra del 1–3.]
- **Hvad der ikke blev nået:** Der mangler tabeldesign for led 2–4, en plan for backup og en konkret definition af plateau-farverne. Den sidste mangler bevidst, fordi den er Thomas' beslutning. Ingen af de nævnte EasyLanguage-fejl er fundet i projektets egen kode. Det er kendte typer af fejl, som skal efterprøves.

## 4.5 Samlet liste over åbne punkter, som Thomas afgør

**Fra opgaven (afsnit 9):**

1. **Plateau-trappen (PL1–PL7).** Hvad betyder farverne? Hvorfor må der være op til 20 % rød på et højt niveau? Hvad må resten være, når der er under 50 % grå? Er de største felter et loft? Og hvilket niveau er nok til dvale? K1 foreslår et placebo-forsøg, så hvert punkt kan afgøres ud fra tal (del 1, afsnit 5). Hænger sammen med U4.
2. **Hvor færdig er EdgeFinder reelt?** Findes der kode eller noter ud over "ikke helt udformet"?
3. **Skal den fulde kørsel af alle filtre startes?** Og i så fald: skal de billige forberedelser i 4.4 laves først?
4. **Hvad gør vi med de MACD-ramte filtre:** A (genskriv), B (karantæne) eller C (udelad)? Og skal der først laves en automatisk optælling af, hvor mange filtre der er ramt?

**Nye punkter fra gruppen (samlet og uden dubletter):**

5. **Grænserne i "færdig strategi".** Skal K1's foreslåede tal bruges (F4, F6, F10 og grænsen for PBO)?
6. **Datadeling.** Hvilke datoer skal bruges til udvikling, validering og pengeskab? De skal låses før analysen.
7. **Hvad tæller som ét forsøg?** Hvert filter? Hver indstilling? Hvert marked? Hver udgangsregel?
8. **Er der allerede kigget på data?** Er filtrene valgt ud fra de samme prisdata? Hvor meget data er helt urørt?
9. **Markeder, tidsrammer og prisdata.** Hvilke markeder og tidsrammer skal bruges? Hvilken type futures-serie skal bruges? Og er sessionsskabelonen fast?
10. **Handelsomkostninger** (kurtage og glidning) pr. marked.
11. **De 36 filtre med usikker Max Bars Back.** Skal de testes med både 1000 og 2000 før den fulde kørsel?
12. **Placebo-signaler.** Må der laves kendt-tilfældige signaler, som bruges fast til at kontrollere hele fabrikken (i testmiljøet)?
13. **Faste filter-ID'er.** Skal de indføres før den fulde kørsel? Skal der også være et versionsnummer (U5)?
14. **Kodeversion.** Gemmer `rawsignal` i dag, hvilken kodeversion der har lavet hver fil?
15. **Adskillelse af test og produktion.** Separat testdatabase eller et separat område i samme database? Og hvor skal kontrolresultaterne ligge (U6)?
16. **De almindelige resultater.** Må godkendte programmer skrive deres resultater uden at spørge hver gang (se 4.4)?
17. **TradeStation-licens.** Hvor mange computere må være logget ind samtidig?
18. **Købe eller bygge.** Skal et færdigt værktøj som MultiWalk undersøges (U8)?
19. **EdgeCruncher.** Er K2's forståelse rigtig: at den gør en edge til en strategi, man kan handle, med omkostninger?
20. **IntrabarOrderGeneration.** Skal den være slået fra i hele fabrikken?
21. **Uafhængighed.** Hvem skriver Python-kontrollerne, så de er uafhængige af den, der byggede filtrene?
22. **Genvækning.** Hvilken prøve skal en strategi bestå, når den vækkes fra dvale?
23. **Drift.** Hvilken PostgreSQL-version bruges? Hvor skal fil-lageret ligge, og hvordan tages backup i dag?
24. **Noter.md.** Skal de regler, maskinerne følger (fx Max Bars Back = 1000), flyttes fra noterne til en opsætning med versionsnummer?
25. **MultiCharts.** Samme datafil som i TradeStation (det anbefales), og hvilken version?


# Bilag – Konsulenternes gensidige kommentarer (runde 2)

## K1's kommentar til K2 og K3

**Rettet i k1.md:** F1 kræver nu også K2's "dobbeltkørsel" (samme filter to gange = præcis samme tal). Passet har fået tre felter mere: største tab (drawdown), omkostningsmodel og "pengeskab åbnet ja/nej + dato".

### (a) Godkendelse

**K2 – kontrolplan i tre lag: GODKENDT med to krav.**
- Lag 1 (kodescanning) og Lag 3 (forskydning, Max Bars Back 1000 mod 2000, dobbeltkørsel) er godkendt. De finder tavse fejl billigt.
- Lag 2 er godkendt, men tilfældig stikprøve skal være mindst ca. 38 filtre og ikke "10 %". Signaler skal stemme 100 %. Tolerancen for indikatorværdier sættes før kørslen og skrives ned.
- Genberegneren må ikke se EasyLanguage-koden.

**K2 – EdgeCruncher: GODKENDT med én ændring.**
- Faste udgangsregler, midten af plateauet og tælling af alle varianter er godkendt.
- IKKE godkendt: at EdgeCruncher kører på "out-of-sample-perioden". Den skal bruge *valideringsdata*. Pengeskabet (hold-out) åbnes kun én gang ved K1's slutkontrol (F9).
- Hver udgangsregel og hvert stop tæller som et forsøg (F3).

**K3 – felter i strategi-passet: GODKENDT som ramme, men der mangler felter.**
- Godkendt: `pas_skabelon`, `antal_tests_i_alt`, `godkendt_af`, faste plus fleksible felter (JSONB), "kun tilføje" og genkørsel ved vækning.
- Mangler som faste felter: datoer for datadeling, Deflated Sharpe, PBO, walk-forward-resultat, omkostningsmodel, drawdown og "pengeskab åbnet".
- `korrigeret_p` alene er for lidt, fordi der bruges flere metoder. Skriv hvilken metode.
- `CHECK PL1–PL7` låser trappen på 7 niveauer. Thomas har ikke afgjort, om der kommer flere. Kontrollen skal fjernes eller gøres åben.
- Antal forsøg skal også gemmes for dem, der dumper, ikke kun for strategier i dvale.

### (b) Uenigheder (én linje hver)

1. MACD: K2 anbefaler at genskrive (A). Statistisk kan jeg også godkende karantæne (B), men aldrig at en MACD-ramt strategi bliver "færdig" uden Lag 2-kontrol.
2. K2's EdgeCruncher bruger "out-of-sample" som sin egen test. Efter min mening må kun K1's slutkontrol åbne pengeskabet.
3. K2's stikprøve på 10 % (ca. 34 filtre) er lidt for lille. Jeg foreslår mindst 38 tilfældige plus alle mistænkte.
4. K3's faste grænse PL1–PL7 i databasen afgør i praksis et åbent punkt for Thomas. Det skal være åbent.

## K2's kommentar til K1 og K3

**Rettet i k2.md:** Den foreløbige definition af "færdig strategi" er fjernet. Jeg henviser nu til K1's F1–F10: F1 i stikprøveplanen, F2/F3/F5–F10 i EdgeCruncher og passet. Nyt: EdgeCruncher rører aldrig pengeskabet, og F9-testen køres af et separat trin.

### (a) Kan det bygges?
- **F1 og stikprøverne:** Ja. De svarer til mine lag 1–3. K1's "gentagelsestest" (filteret køres alene og sammen med andre kald) kan laves i EasyLanguage og er et godt supplement [Antagelse].
- **F2, F9 (datadeling og pengeskab):** Ja. Det kræver, at *datoerne* styres uden for TradeStation (i databasen). En menneskelig klik-optimering i TradeStation kan ellers let komme til at røre pengeskabet [Antagelse].
- **F3 (tæl alle forsøg):** Kan kun lade sig gøre, hvis ALLE optimeringer køres af vores eget program. TradeStations indbyggede optimering tæller ikke forsøg for os [Antagelse].
- **F6 (walk-forward), PBO/CSCV, placebo-forsøg:** TradeStation har ikke disse værktøjer ud af boksen, og via fjernstyring bliver de meget langsomme. Jeg foreslår: TradeStation eksporterer signaler/handler én gang, og resten regnes i Python [Antagelse]. Ulempe: Python skal så genberegne handler, og det kontrolleres med stikprøver mod TradeStation.
- **K3's kø med én TradeStation pr. maskine:** Enig. Fjernstyring via Windows-beskeder kan ikke deles sikkert [Rapport + Antagelse]. Flaskehalsen bliver TradeStation-maskinerne og licensen (K3's ubekræftede loginregel). Det taler også for at flytte så meget som muligt til Python.

### (b) Uenigheder (én linje hver)
1. K1 vil ikke "acceptere" MACD-risikoen ved godkendelse. Jeg er enig og går videre: jeg anbefaler at genskrive filtrene (valg A), K1 accepterer også kontrol eller udelukkelse.
2. K1 vil have 100 % enighed om signalet. Jeg er enig, men afrunding (tick) kan give sjældne vip på grænsen, og tolerancen for det mangler.
3. K3 vil køre RawSignal-Analyse og store dele af EdgeFinder som ren Python. Jeg er enig, men så *skal* Python-genberegningen verificeres mod TradeStation, ellers flytter vi bare fejlrisikoen.
4. K3 foreslår, at MultiWalk overvejes. Jeg er uden holdning (ikke undersøgt), men et lukket værktøj gør F3-tællingen sværere at bevise.
5. K1/K3 bruger ordet "hold-out/pengeskab", mit udkast sagde "out-of-sample". Nu retter jeg mig efter K1's ord.

## Konsulent 3 – kommentar til K1 og K2

**Rettet i k3.md:** Den foreløbige definition er erstattet med henvisninger til K1's F1–F10. Der er tre nye tabelforslag: `datadeling` (F2, låst og kan ikke rettes), `pengeskab_aabning` (F9, én åbning pr. strategi håndhævet af databasen) og `faerdig_strategi` (en fast visning, der er eneste vej ind i dvale). `dvale_pas` har nu én kolonne pr. F-krav plus `antal_forsoeg` (F3), risici og platform-verificering (K2).

### (a) Passer det sammen?

- **Antal forsøg (F3):** Ja. `antal_forsoeg` er et obligatorisk felt. EdgeCruncher skal lægge sine prøvede varianter oven i tallet fra de tidligere led. Hvem der lægger sammen, er ikke aftalt. Mit forslag: databasen tæller alle jobs i samme kørsel.
- **Datadelings-datoer (F2):** Ja. Datoerne ligger i en låst tabel, som hver kørsel og hvert pas peger på. Rækkefølgen udvikling < validering < pengeskab tjekkes af databasen.
- **Pengeskabet (F9):** Ja, og databasen håndhæver det (én række pr. strategi-ID for altid). Hullet er, at man kan oprette en "ny" strategi med nyt ID. Det kræver, at F3 også tæller kasserede strategier. Den del er K1's afgørelse.
- **K2's EdgeCruncher-pas:** Alle K2's felter kan rummes: parametre og plateau-grænser, fingeraftryk, generator-version, drawdown, kontrollerne Lag 1–3, MACD-flag og status "også MultiCharts-verificeret".
- **Uklart:** K2 skriver, at EdgeCruncher "kører én gang på out-of-sample". K1 siger, at EdgeCruncher *aldrig* må røre pengeskabet. Det skal skrives ind, at K2's out-of-sample er K1's *valideringsdel* og ikke pengeskabet.

### (b) Uenigheder

1. K2 vil lade EdgeCruncher køre out-of-sample-testen selv. Jeg mener, at kun et separat "pengeskabs-åbner"-program må hente pengeskabs-data.
2. K2 foreslår kontrolresultater i "særskilt kontroltabel eller test-database". Jeg mener, at kontroller af produktionsfiltre er produktionsdata og hører i produktion. Kun opdigtede testsignaler (fx K1's placebo) hører i testdatabasen.
3. K1 kræver filter-ID *og* filter-version. Jeg foreslår et permanent UUID. Om filtre også skal have versionsnumre, er ikke afklaret mellem os.
4. Et lille punkt om status: K2's "bestået/ikke bestået" står i passet, men det er K1's regler, der skal afgøre det. Hos mig afgøres "færdig" af visningen `faerdig_strategi` og ikke af EdgeCruncher.

