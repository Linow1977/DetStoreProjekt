# Andrea Ungers Titan — skærmbilleder, arbejdsgang, data — og sammenlignelige overvågnings-/inkubationsværktøjer (input til "Pharos")

> **Vigtig metodenote (læs først):** Netværkspolitikken i denne session blokerede direkte hentning af ungeracademy.com, learn.ungeracademy.com, ps.ungeracademy.com, substack og proboards (proxy svarede 403 / DNS-fejl). Alle fund nedenfor stammer derfor fra søgemaskinens uddrag/resuméer af de nævnte sider, ikke fra fuld læsning af siderne. Citater er gengivet som søgemaskinen viste dem. Ingen YouTube-videoer kunne ses. Alt om Titans konkrete skærmbilleder er derfor tyndt og markeret som ubekræftet, hvor det ikke direkte står i en kilde. Næsten alle Titan-kilder er Unger Academys egne markedsføringssider.

## 1. Hvad viser Titans skærmbilleder/dashboards, og hvad er brugerens daglige/månedlige arbejdsgang?

### Takeaway
Titan er offentligt beskrevet som et **månedligt udvælgelses- og positionsstørrelsesværktøj**, ikke et realtids-dashboard: det tager daglig P&L for alle strategier ind, anvender et momentum-/equity-filter (lang og kort periode), og giver som output en liste over strategier der skal handles næste måned samt antal kontrakter pr. strategi. Det eneste dokumenterede "skærmbillede" er en sammenligning af filtreret vs. ufiltreret porteføljeequity; selve brugerfladen (tabeller, menuer) er ikke offentligt beskrevet.

### Cited Findings
- Titan beskrives på Unger Academys kursusside som "a software that allows you to choose the best strategies to add to your portfolio. Moreover, it tells you how many contracts you should trade with each strategy based on your capital and your risk level." — [Unger Academy, Titan (EN) kursus](https://learn.ungeracademy.com/courses/titan-en/); [Portfolio Secrets salgsside](https://ps.ungeracademy.com/secrets)
- Input/output: "TITAN get as inputs the daily profit/loss of all the strategies, we can be set different testing parameter"; output er de strategier der skal handles i næste periode og antal kontrakter for hver. — [Unger Academy: Effective Portfolio Management](https://ungeracademy.com/blog/effective-portfolio-management-how-to-choose-the-best-strategies-for-live-trading)
- Udvælgelsesregel (Ungers egen beskrivelse): "I look into a longer-term performance (something around 12 to 18 periods, months in my case) and a shorter term one (3 to 6 periods), both shall be positive and the shorter term must also show an average monthly profit higher than the longer term." Strategier der består er "valid to trade during the coming month, all those which fail will stay in incubation." — [Unger Academy: Effective Portfolio Management](https://ungeracademy.com/blog/effective-portfolio-management-how-to-choose-the-best-strategies-for-live-trading)
- Positionsstørrelse: "the worst day of each strategy is taken as Worst Case Scenario and used to calculate the number of contracts after deciding the percentage of risk to take", hvilket "can be further adjusted (reduced) considering the max drawdown of each strategy and correlations among systems." — [Unger Academy: Effective Portfolio Management](https://ungeracademy.com/blog/effective-portfolio-management-how-to-choose-the-best-strategies-for-live-trading)
- Titan kan "splitte" strategier på store kontrakter til micro-kontrakter (fx et backtest der foreslår 0,1 kontrakt råolie → 1 Micro Crude Oil). — [Unger Academy: Titan – The Software to Automatically Manage Trading Systems](https://ungeracademy.com/blog/titan-the-software-to-automatically-manage-trading-systems)
- Titan "allows you to run different kinds of tests to evaluate the performance of your strategies and stop the ones that are not producing the results you expected." — [Unger Academy: Titan](https://ungeracademy.com/blog/titan-the-software-to-automatically-manage-trading-systems)
- Det eneste beskrevne "skærmbillede" i video: en rød ufiltreret equity-linje vs. en blå linje med equity-baserede filtre; linjerne er out-of-sample og inkl. kommission og slippage. "The first step of system selection is a filter on the equity lines of the systems, all out-of-sample." — [Unger Academy: Effective Portfolio Management](https://ungeracademy.com/blog/effective-portfolio-management-how-to-choose-the-best-strategies-for-live-trading)
- Italiensk del 2 af Titan-videoen: Titan "consente di filtrare le strategie in modo da mettere automaticamente in pausa o stoppare quelle che non stanno performando"; i Ungers test faldt net profit fra ca. 2,9 mio. til ca. 1,64 mio. USD, mens max drawdown faldt fra over 400.000 til ca. 150.000 USD. (Leverandørens egen påstand.) — [Unger Academy IT: Titan parte 2](https://ungeracademy.com/it/blog/titan-il-software-per-gestire-i-trading-systems-in-modo-automatico-or-parte-2)
- Andet beskrevet filter: kun systemer der har ramt en ny equity-top inden for det seneste år bruges. — [Unger Academy IT: Titan parte 2](https://ungeracademy.com/it/blog/titan-il-software-per-gestire-i-trading-systems-in-modo-automatico-or-parte-2) (via søgeresumé; kan også stamme fra [How to filter Drawdowns](https://ungeracademy.com/blog/how-to-filter-drawdowns))
- Månedlig arbejdsgang (Unger selv): "Every month, from my software Titan, I get a list of the strategies that will go live on the coming month. These are the strategies that I put live on the platform." Han kører ca. 300 strategier, og "thanks to Titan, I can automate long operations and complicated algorithms, simplifying my portfolio management." — [Unger Academy: What about My Trading Infrastructure?](https://ungeracademy.com/blog/my-trading-infrastructure)
- Elev-eksempel: en "Trader of the Month" (marts 2025) kører backtests i Titan og "picks only those strategies that rank among the best, giving priority to trend-following systems with low drawdowns"; en anden elev bruger 2 % daglig risiko-indstilling og månedlig rebalancering. — [Unger Academy: Trader of the Month March 2025](https://ungeracademy.com/?p=7024)
- Advarsel fra Unger selv: flere og flere restriktive filtre kan føre til overfitting. — [Unger Academy IT: Titan parte 2](https://ungeracademy.com/it/blog/titan-il-software-per-gestire-i-trading-systems-in-modo-automatico-or-parte-2)

### Inferences
- Titans "workflow" er **månedlig**, ikke daglig: eksport af daglig P&L → kør Titan → få liste (live/inkubation) + kontrakter → slå strategier til/fra manuelt i MultiCharts. Daglig overvågning af den kørende drift ser ud til at ligge i et **separat** værktøj (Strategy Checker, se spørgsmål 2).
- Titan behandler "inkubation" som en tilstand, en strategi kan gå ind og ud af hver måned (strategier der fejler filteret "stay in incubation"), ikke kun som en fast periode før første live-dag. Det er en vigtig designbeslutning for Pharos: strategistatus er dynamisk.
- Kernevisningerne man kan udlede: (a) strategiliste med status og kontraktantal, (b) porteføljeequity filtreret vs. ufiltreret, (c) parameterpanel for testvinduer/risiko-%. Den præcise skærmopbygning er **ikke bekræftet**.

### Gaps
- Ingen offentlig beskrivelse/skærmbillede af Titans faktiske brugerflade (menuer, tabelkolonner, grafer udover equity-sammenligningen). YouTube-demoer kunne ikke ses.
- Uklart om Titan viser nøgletal pr. strategi (fx Sharpe, profit factor, korrelationsmatrix) på skærmen, eller kun bruger dem internt.
- Den præcise formel for kontraktberegning (fx risiko-% × kapital / værste dag, og hvordan DD/korrelation reducerer) er ikke offentlig.

## 2. Hvordan får Titan sine data, og sender det ordrer eller rådgiver det kun?

### Takeaway
Titan arbejder på **filer med daglig P&L pr. strategi** (eksporteret fra handelsplatformen), kører som MATLAB-baseret skrivebordsprogram, og der er **intet tegn på broker-forbindelse eller ordreafsendelse** — Unger sætter selv de udvalgte strategier live i MultiCharts. Live-drift overvåges i stedet af et særskilt produkt, "Unger Strategy Checker", der sender Telegram-alarmer.

### Cited Findings
- Input er "the daily profit/loss of all the strategies". — [Unger Academy: Effective Portfolio Management](https://ungeracademy.com/blog/effective-portfolio-management-how-to-choose-the-best-strategies-for-live-trading)
- Titan og et søsterværktøj "Zeus" er ifølge en tredjeparts podcast-opsummering "built on MATLAB for strategy selection, portfolio construction and risk management" og "only available to his students"; samme kilde nævner at equity-kurver også kan importeres i andre programmer som AmiBroker eller RealTest. — [The Algorithmic Advantage #038 (Andrea Unger)](https://algoadvantage.substack.com/p/038-andrea-unger-672-returns-sure). Unger Academys software kræver ifølge søgeresumé MATLAB Runtime installeret — [Unger Academy Software (EN)](https://learn.ungeracademy.com/software-en/). Zeus kunne **ikke** bekræftes i nogen Unger-egen kilde.
- Unger kører sin handelssoftware (MultiCharts) på en cloud-server: "the trading platform in my infrastructure is MultiCharts"; de strategier Titan udvælger er "the strategies that I put live on the platform." — [Unger Academy: My Trading Infrastructure](https://ungeracademy.com/blog/my-trading-infrastructure)
- Unger Strategy Checker: "monitors your trading station 24/7", sender beskeder via Telegram; alarmer for afbrydelse platform↔broker eller datafeed, platform-genstart, når et system går ind/ud af position, alvorlig entry-slippage og pludselig server-nedlukning. Lavet fordi "when we are away from our computers, we don't have the possibility to check if everything is going well." — [Unger Academy: Unger Strategy Checker](https://ungeracademy.com/blog/unger-strategy-checker-tm-monitor-your-live-strategies-from-your-cell-phone-wherever-and-whenever); [Strategy Checker salgsside](https://cf.ungeracademy.com/purchase-unger-investing717dcjze)
- Alternativ: Unger Academy anbefaler også fjernskrivebord (RDP) fra telefon/tablet til at se platformen direkte. — [Unger Academy: Monitor with Smartphone and RDP](https://ungeracademy.com/blog/how-to-monitor-the-performance-of-your-strategies-with-a-smartphone-tablet-and-rdp)
- Platform-side: MultiCharts kan eksportere "List of Trades" til CSV fra Portfolio Performance Report; et ønske om CSV-eksport af performance-summary er en åben feature-request (MC-677); brugere skriver egne trade-lister til fil med EasyLanguage `Print`/`FileAppend`. — [MultiCharts forum t=47515](https://www.multicharts.com/discussion/viewtopic.php?t=47515); [MultiCharts MC-677](https://www.multicharts.com/pm/public/multicharts/issues/MC-677&search_queue=3); [MultiCharts forum t=48271](https://www.multicharts.com/discussion/viewtopic.php?t=48271)

### Inferences
- Titan er et **rådgivende** værktøj (beslutningsstøtte), ikke et eksekveringsværktøj. Adskillelsen "månedlig udvælgelse (Titan)" vs. "løbende driftsovervågning/alarmer (Strategy Checker)" er en nyttig arkitekturskabelon for Pharos.
- Den præcise eksportvej (TradeStation/MultiCharts → fil → Titan) er ikke dokumenteret offentligt; sandsynligvis daglig P&L-serie pr. strategi fra performance-rapport eller en EasyLanguage-funktion der skriver til fil (**ubekræftet**).
- For projektet her (TradeStation + PostgreSQL) kan databasen erstatte Titans filbaserede input: daglig P&L pr. strategi gemmes direkte i tabeller.

### Gaps
- Filformat, kolonner og importprocedure for Titan er ikke offentlige (kun i elevmateriale).
- Uklart om Titan understøtter TradeStation-eksport direkte, eller kun MultiCharts (Unger bruger selv MultiCharts).
- Ingen bekræftelse af om Titan sammenligner live-handler med backtest (fx slippage-afvigelse) — det fremgår ikke af kilderne.

## 3. Brugerfeedback/anmeldelser — styrker, begrænsninger, klager

### Takeaway
Der findes **næsten ingen uafhængig feedback specifikt om Titan**. Anmeldelser handler om Unger Academy generelt (overvejende positive om undervisning/coaching, kritiske om sælgede add-on-strategier). Prisen/tilgængeligheden er uklar mellem kilder.

### Cited Findings
- Trustpilot: ca. 330 anmeldelser, gennemsnit ca. 4 stjerner; ros til undervisning og coaching; en 1-stjernet: "If the expectation is to be profitable long term, forget it." — [Trustpilot: Unger Academy](https://www.trustpilot.com/review/ungeracademy.com?page=3); [Trustpilot AU](https://au.trustpilot.com/review/ungeracademy.com)
- Kritisk anmelder: add-on-strategierne er dårlige out-of-sample, overoptimerede med mange justerbare inputs, og backtests uden slippage/kommission — i modstrid med kursets egen lære om curve fitting. (Én brugers påstand.) — [Trustpilot: Unger Academy](https://www.trustpilot.com/review/ungeracademy.com?page=3)
- Goodreads-læser af Ungers bog: bogen er "a marketing tool for the academy", overfladisk, men "Titan video tutorials" var nyttige. — [Goodreads: The Unger Method](https://www.goodreads.com/book/show/57357737-the-unger-method---the-winning-strategy-of-the-4-time-world-trading-cham)
- Unger Academys community-forum har et Titan-board med ca. 52 tråde og 358 indlæg (moderet af personalet; indhold ikke tilgængeligt). — [Unger Academy forum (proboards)](https://skilledacademy.proboards.com/forum)
- Pris/tilgang er modstridende: Portfolio Secrets-salgssiden siger Titan ikke er inkluderet og kan købes separat for €997 — [Portfolio Secrets](https://ps.ungeracademy.com/secrets); mens en Unger-artikel kalder Titan "un software gratuito per gli studenti di Unger Academy" — [Unger Academy IT: Titan parte 2](https://ungeracademy.com/it/blog/titan-il-software-per-gestire-i-trading-systems-in-modo-automatico-or-parte-2). (Kan afhænge af kursuspakke/tidspunkt — ubekræftet.)
- Ungers egen advarsel om overfitting af filtre (se spørgsmål 1). — [Unger Academy IT: Titan parte 2](https://ungeracademy.com/it/blog/titan-il-software-per-gestire-i-trading-systems-in-modo-automatico-or-parte-2)

### Inferences
- Afledte begrænsninger (ikke brugerrapporterede, men følger af designet): (a) MATLAB-afhængighed/lukket elevværktøj, (b) månedlig granularitet → reagerer langsomt på pludselig strategi-nedbrud mellem rebalanceringer, (c) momentum-filteret kan "piske" strategier ind og ud (whipsaw), og den filtrerede kurve i Ungers eget eksempel halverer også nettoprofitten.
- Den filtrerede-vs-ufiltreret-backtest er i sig selv udsat for den overfitting Unger advarer om; Pharos bør kunne vise robusthed af filterparametre (flere vinduer), ikke kun ét valgt filter.

### Gaps
- Ingen uafhængige tests, fora-diskussioner eller video-anmeldelser af Titan selv fundet.
- Indholdet af Titan-forumboardet (fejl, ønsker) kunne ikke læses.

## 4. Sammenlignelige værktøjer til inkubation/porteføljeovervågning og fælles funktioner

### Takeaway
Markedet deler sig i (a) **porteføljebyggere/backtest-analyse** (QuantAnalyzer Portfolio Master, TradeStation Portfolio Maestro, MultiCharts Portfolio Trader), (b) **inkubations-/OOS-værktøjer** (MultiWalk, Kevin Daveys proces og Excel Monte Carlo/sandsynlighedskegle), og (c) **live-vs-backtest-sammenligning og driftsalarmer** (QuantAnalyzer Compare Results, Algo Terminal, Unger Strategy Checker). Få værktøjer dækker alle tre; netop dét hul er Pharos' mulighed.

### Cited Findings
**Kevin Davey (proces, ikke ét produkt)**
- Inkubation: strategien kører i realtid uden (eller med minimal) rigtige penge; længde angives forskelligt: 3–6 mdr. (Daveys site), 6–9 mdr. (MultiWalk om Davey), 6–12 mdr. (tredjepart). — [MultiWalk: Incubation period](https://multiwalk.net/knowledge-base/incubation-period-in-multiwalk/); [KJ Trading: After optimization (PDF)](https://kjtradingsystems.com/WhatHappensAfterOptimization.pdf); [forex.in.rs](https://www.forex.in.rs/simple-systems-diversified/)
- Månedlig kontrol: "look at the results once a month and add those new results to your historical backtest equity curve." — [KJ Trading: After optimization (PDF)](https://kjtradingsystems.com/WhatHappensAfterOptimization.pdf)
- Daveys Excel Monte Carlo-simulator har en sandsynlighedskegle til live-overvågning: hver lukket handel tilføjes, og live-equity plottes mod indre/ydre bånd; "quitting equity point" bruges til risk-of-ruin. — [Medium: Monte Carlo Simulation and Probability Cones](https://medium.com/data-science/improving-your-algo-trading-by-using-monte-carlo-simulation-and-probability-cones-abacde033adf); [LinkedIn: Monte Carlo analysis (Kevin Davey)](https://www.linkedin.com/pulse/montecarlo-analysis-quantitative-trading-kevin-davey-hakim-tadjadit)
- Detektion af svigtende strategi: statistisk proceskontrol (fra hans aerospace-baggrund), "out of control"-kriterier defineret på forhånd — "The biggest mistake he sees traders make is not having any criteria defined until they are already in the middle of a drawdown"; sandsynlighedskegler/Monte Carlo; drawdown-baseret on/off (fx genaktivering efter halv genvinding af DD); "a really good backtest can actually be a predictor of bad performance." — [Better System Trader: 6 ways to detect a failing trading strategy](https://bettersystemtrader.com/6-ways-to-detect-a-failing-trading-strategy-with-kevin-davey/); [BST #170](https://bettersystemtrader.com/170-how-to-detect-a-failing-trading-strategy-kevin-davey/)
- Strategy Factory-kurset indeholder materiale "When to Quit a Trading Strategy" (detaljer ikke offentlige). — [Coursehuge: Strategy Factory Workshop](https://coursehuge.com/product/kevin-davey-strategy-factory-workshop-2021/)

**MultiWalk (TradeStation-baseret walkforward-framework)**
- Simuleret inkubation: OOS-perioden skjules i alle rapporter, til man er klar; når den afsløres er resultatet endeligt — "It either passed or failed incubation." MultiWalk Trader styrer strategier som samling, med inkubationsdatoer der kan overstyre projektets. Kører kun under TradeStation. — [MultiWalk: Incubation period](https://multiwalk.net/knowledge-base/incubation-period-in-multiwalk/); [MultiWalk](https://multiwalk.net/)

**StrategyQuant QuantAnalyzer**
- "Compare Results": sammenligner live-/platformresultater med backtests, overlejrer equity-kurver, batch for mange strategier. "Portfolio Master" bygger porteføljer under constraints ved at gennemgå tusindvis af kombinationer (gratis version max 4 strategier). — [QuantAnalyzer Compare Results](https://strategyquant.com/quantanalyzer/compare-results/); [QuantAnalyzer](https://strategyquant.com/quantanalyzer/); [StrategyQuant pricing](https://strategyquant.com/pricing/)
- Roadmap-ønsket "Improve monitoring of live strategies" er markeret **Refused**; brugere uploader live-tradelister manuelt. — [QuantAnalyzer roadmap](https://roadmap.strategyquant.com/projects/qa4/roadmap); [StrategyQuant forum: Analyzing live data](https://strategyquant.com/forum/topic/analizing-live-data/)
- StrategyQuants egen anbefalede arbejdsgang: live-konto → online-monitor (FX Blue/MyFxBook) → CSV-eksport → sammenlign i QuantAnalyzer. — [StrategyQuant blog: Real trading](https://strategyquant.com/blog/real-trading-compare-live-strategy-results-backtest/)

**TradeStation Portfolio Maestro / MultiCharts Portfolio Trader**
- Portfolio Maestro (købt af TradeStation fra RINA Technologies i 2010): porteføljebacktest med money management på porteføljeequity og porteføljestops. Ingen kilde bekræfter at den er udgået; hjælpesiden er fra v9.01 (gammel). — [SEC pressemeddelelse 2010](https://www.sec.gov/Archives/edgar/data/1111559/000119312510194692/dex991.htm); [TradeStation help: Portfolio Maestro feature summary](https://help.tradestation.com/09_01/tsportfolio/general/feature_summary_portfolio_maestro.htm)
- Brugerklager over Portfolio Maestro: misser handler. — [NexusFi: Portfolio Maestro misses trades](https://nexusfi.com/showthread.php?t=42990)
- MultiCharts Portfolio Trader angives (brugerindlæg, ubekræftet) som tilkøb ca. $499. — [RizeTrade: MultiCharts vs TradeStation](https://rizetrade.com/brokers/multicharts-vs-tradestation)

**Andre**
- Algo Advantage "Algo Terminal" (Interactive Brokers): "record all trades, easily compare live to back-test." — [Algo Advantage Toolbox](https://www.algoadvantage.io/toolbox/)
- QuantConnect: research-pipeline hvor out-of-sample paper trading skal ligge inden for backtestens statistiske interval. — [QuantConnect](https://www.quantconnect.com/)

### Inferences
Fælles funktioner på tværs af værktøjerne:
1. Strategi-register med status (udvikling → inkubation → live → pause/udgået).
2. Equity-kurve pr. strategi og portefølje, med backtest + inkubation/live sammenhængende (Davey: læg live oven i backtest).
3. Live-vs-backtest-sammenligning (afvigelse i P&L, slippage, antal handler).
4. Statistiske grænser defineret på forhånd: Monte Carlo-/sandsynlighedskegle, max DD-grænse, "quit point".
5. Porteføljeudvælgelse/rangering med periodisk (oftest månedlig) rebalancering.
6. Positionsstørrelse ud fra risiko-%, værste dag/DD og korrelation.
7. Korrelationsanalyse mellem strategier.
8. Driftsalarmer (forbindelse, positioner, slippage) — typisk separat værktøj.

### Gaps
- Kevin Daveys konkrete quit-tærskler (tal) er kun i hans bøger/kursus, ikke offentligt.
- Ingen kilder fundet om nyere (2025–2026) dedikerede inkubations-trackere for TradeStation-futurestradere; markedet ser tyndt ud.
- Portfolio Maestros nuværende status (aktiv/udgået) ikke bekræftet.

## 5. Hvilke funktioner er essentielle vs. nice-to-have for et in-house program som Pharos?

### Takeaway
Ud fra Titan + Davey + de øvrige værktøjer er kernen: et strategiregister med dynamisk status, daglig P&L i databasen, live/inkubation lagt oven i backtest, forudfastsatte statistiske stop-/genstartsregler, månedlig rangering + kontraktberegning, og live-vs-backtest-afvigelse. Driftsalarmer og avanceret porteføljeoptimering er næste lag.

### Cited Findings
- Titans kerne = daglig P&L ind → filter (lang/kort vindue) → liste + kontraktantal ud, månedligt. — [Unger Academy: Effective Portfolio Management](https://ungeracademy.com/blog/effective-portfolio-management-how-to-choose-the-best-strategies-for-live-trading)
- Daveys kerne = kriterier for "out of control" fastlagt **før** drawdown; månedlig opdatering af equity; sandsynlighedskegle. — [Better System Trader](https://bettersystemtrader.com/6-ways-to-detect-a-failing-trading-strategy-with-kevin-davey/); [KJ Trading PDF](https://kjtradingsystems.com/WhatHappensAfterOptimization.pdf)
- Driftsalarmer (forbindelse, positioner, slippage, server) er hos Unger et separat produkt. — [Unger Strategy Checker](https://ungeracademy.com/blog/unger-strategy-checker-tm-monitor-your-live-strategies-from-your-cell-phone-wherever-and-whenever)
- Live-overvågning er det felt StrategyQuant afviste at bygge — dvs. et reelt hul i markedet. — [QuantAnalyzer roadmap](https://roadmap.strategyquant.com/projects/qa4/roadmap)

### Inferences
**Essentielt (version 1)** — alle afledt af ovenstående, ikke direkte anbefalet af en kilde:
- Strategiregister med status og historik over statusskift (hvornår og hvorfor en strategi gik i inkubation/live/pause).
- Daglig P&L pr. strategi lagret i PostgreSQL (backtest, inkubation og live adskilt med markering).
- Equity-graf pr. strategi hvor backtest + inkubation/live hænger sammen, med tydelig skillelinje ved inkubationsstart.
- Forudfastsatte regler pr. strategi: max DD-grænse, Monte Carlo-/sandsynlighedskegle, "quit point", og evt. genstartsregel.
- Månedlig rangering/udvælgelse (Titan-lignende: lang og kort periode) med output = liste + kontraktantal.
- Positionsstørrelse ud fra risiko-% af kapital, værste dag og max DD; micro-kontrakt-konvertering.
- Live vs. backtest-sammenligning (slippage, P&L-afvigelse, antal handler).
- Rådgivende output (ingen automatiske ordrer) — som Titan.

**Nice-to-have (senere)**
- Korrelationsmatrix og korrelationsbaseret nedskalering.
- Porteføljeoptimering (QuantAnalyzer Portfolio Master-stil kombinatorik).
- Robusthedstjek af selve udvælgelsesfiltret (flere vinduer) mod overfitting.
- Driftsalarmer til telefon (Telegram e.l.) for forbindelse, positionsuoverensstemmelse, slippage.
- Simuleret inkubation (MultiWalk-stil skjult OOS) til hurtigere screening.
- Filtreret vs. ufiltreret porteføljeequity (Titans eneste dokumenterede graf).

### Gaps
- Ingen kilde giver en standardiseret "feature-liste" for sådanne programmer; opdelingen essentiel/nice-to-have er en vurdering, ikke et kildefund.
- Ingen offentlige oplysninger om hvordan professionelle CTA'er/hedgefonde bygger deres interne overvågningsværktøjer (uden for denne opgaves søgning).
