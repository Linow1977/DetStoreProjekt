# Åbne spørgsmål fra spørgeskemaet

Udtrukket 1. oktober 2026 fra Thomas' svar i `SPORGESKEMA_DetStoreProjekt.md`.
Numrene passer til spørgeskemaet.

## Ved ikke endnu (95 spørgsmål)

### 1. Mål, vision og succes

- **3.** Hvilket afkast pr. år sigter du efter, og hvor stort et fald fra top til bund (drawdown) kan du leve med, før du stopper?
- **11.** Hvornår vil du stoppe projektet eller ændre retning? Findes der en "exit-regel" for selve projektet?

### 2. Rammer: tid, penge, folk og regler

- **19.** Hvor meget kapital er afsat til handel, når systemet er klar?
- **20.** Hvor meget må projektet koste pr. måned i software, data, servere og abonnementer?

### 3. Markeder og instrumenter

- **39.** Hvordan håndteres helligdage, halve handelsdage og lukkede børser?
- **43.** Skal systemet kunne bruge data fra ét marked til at handle et andet (fx renter til at handle aktieindeks)?
- **44.** Er der markeder, du bevidst vil holde dig fra, og hvorfor?
- **46.** Hvor stor en daglig omsætning (likviditet = hvor let man kan købe og sælge) skal et marked mindst have for at være med?

### 4. Markedsforståelse og strategityper

- **56.** Skal systemet lede efter edges, der virker på tværs af markeder, eller edges, der kun gælder ét marked?

### 5. Prisdata

- **61.** Hvordan kontrolleres dataene for fejl (huller, dubletter, forkerte priser, spring)?
- **66.** Hvad sker der, hvis dataleverandøren retter historiske data bagefter? Opdager systemet det?
- **71.** Skal der bruges andre data end pris og volumen (fx volatilitetsindeks, kalender, sæson)? Eller holdes det strengt til prisdata?
- **72.** Hvordan gemmes de rå data, så de aldrig kan ændres ved en fejl (fx en skrivebeskyttet kopi)?
- **73.** Hvilken tidsramme er den mindste, der skal bruges, og hvorfor?
- **74.** Hvordan håndteres bars med meget lidt handel (fx om natten)?
- **75.** Skal der hver dag være en kort data-rapport, der viser, om de nye data er kommet rigtigt ind?
- **77.** Hvad koster bedre data fra en separat dataleverandør, og er det pengene værd?

### 6. TradingServer (database, bibliotek, lager)

- **78.** Hvad er den fulde liste over tabeller i TradingDB i dag, og hvad bruges hver til?
- **81.** Hvad er forskellen på "Database", "Bibliotek" og "Lager" i TradingServer? Hvad hører til hvilken?
- **86.** Hvad sker der i databasen, når en regel eller et program ændres? Skal gamle resultater slettes, markeres som forældede eller beholdes?
- **88.** Hvordan undgås det, at to programmer skriver i samme tabel samtidig og ødelægger data for hinanden?
- **90.** Skal der være en testdatabase ved siden af den rigtige, så nye programmer kan afprøves uden risiko?
- **91.** Hvordan skal databasen klare det, når der kommer millioner af resultatrækker?
- **92.** Hvilke spørgsmål vil du selv kunne stille databasen uden hjælp (fx "vis alle, der har bestået")?
- **94.** Hvad er reglen for navne på tabeller og kolonner (små eller store bogstaver, dansk eller engelsk)?
- **95.** Hvordan registreres det, hvilken programudgave der lavede hver række i databasen?

### 7. TML-Server (backtest, analyse, selektering)

- **98.** Hvordan sendes arbejde mellem TradingServer og TML-Server (filer, database, netværksmappe)?
- **99.** Hvor mange backtests kan køres samtidig, og hvad er flaskehalsen: computerkraft, TradeStation-licenser eller tid?
- **100.** Hvor lang tid tager én backtest i dag? Hvor lang tid vil alle tage samlet?
- **102.** Hvilke analyser skal ligge på TML-Serveren, og hvilke skal ligge i Python et andet sted?
- **103.** Hvad sker der, hvis TML-Serveren går ned midt i en lang kørsel? Kan den fortsætte, hvor den slap?
- **111.** Hvor gemmes backtest-indstillingerne (kurtage, slippage, handelstider), så de ikke ændres ved et uheld?

### 8. EdgeFinder (event-studie)

- **114.** Hvilke tidshorisonter efter et signal skal måles?
- **129.** Skal EdgeFinder allerede regne kurtage og slippage med i event-studiet?
- **130.** Hvad gør EdgeFinder med et resultat, der er godt på én tidsramme og dårligt på en anden?

### 9. EdgeCruncher

- **137.** Skal EdgeCruncher kombinere flere signaler til én strategi? Hvor mange må der højst kombineres?
- **144.** "Data1, når den senere bliver mindre end Data2 (entry-finpudsning)" — hvor og hvornår hører det til?
- **145.** Skal EdgeCruncher arbejde i Python, i TradeStation eller i begge?
- **147.** Hvilke slags udgange skal prøves (efter tid, stop, gevinstmål, modsat signal)?

### 10. Statistik og beskyttelse mod selvbedrag

- **151.** Hvordan tages der højde for, at der testes tusindvis af signaler, så nogle vil se gode ud af ren tilfældighed (multiple testing)?
- **156.** Skal strategier testes på andre markeder end dem, de blev fundet på, som ekstra kontrol?
- **160.** Skal der være et fast sæt af "kontrolsignaler" (tilfældige signaler), som alle resultater sammenlignes med?
- **164.** Hvordan dokumenteres alle forkastede idéer, så de ikke testes igen ved en fejl?
- **165.** Hvor sikre skal vi være (signifikansniveau), før noget kaldes en edge?
- **166.** Skal der rettes for antallet af tests med en fast metode (fx "Deflated Sharpe Ratio")? Hvem vælger metoden?
- **169.** Skal systemet testes på "falske" data (fx tilfældigt blandede priser) for at se, om det også finder edge i ren støj?
- **170.** Hvordan opdages fejl med fremtidige data (look-ahead) automatisk i koden?
- **171.** Hvordan vurderes en strategi med få handler og stor gevinst mod en med mange handler og lille gevinst?

### 11. Fra enkelt-strategi til portefølje

- **174.** Hvordan fordeles kapitalen mellem strategierne: lige meget, efter risiko, eller efter noget andet?
- **180.** Hvordan håndteres det, når to strategier vil handle modsat hinanden i samme marked på samme tid?
- **181.** Hvordan vil du se et samlet overblik over hele porteføljen hver dag?
- **184.** Hvordan testes hele porteføljen samlet bagud i tid, og ikke kun strategierne hver for sig?
- **187.** Skal porteføljen tilpasse sig uro i markedet (fx mindre positioner, når det er uroligt)?

### 12. Handel i virkeligheden (execution)

- **190.** Hvor meget slippage (forskel på forventet og faktisk pris) og kurtage regnes der med i backtests i dag? Er tallene målt eller gættet?
- **191.** Hvordan sammenlignes de rigtige handler med backtesten bagefter, så forskelle opdages hurtigt?
- **195.** Skal der ligge en stop-ordre hos brokeren hele tiden (så den virker, selvom din computer er slukket)?
- **196.** Hvordan sikres det, at systemet ikke sender den samme ordre to gange ved en fejl?
- **198.** Hvordan testes selve ordresystemet, før rigtige penge er på spil?
- **200.** Hvordan måles slippage i den rigtige handel, og hvor gemmes målingerne?
- **201.** Hvad er reglen, hvis en ordre ikke bliver udført inden for en bestemt tid?
- **203.** Hvad gør systemet, hvis brokerens system er nede eller afviser ordrer?
- **204.** Hvordan tjekkes det hver dag, at positionerne i systemet og hos brokeren er de samme?

### 13. Risikostyring

- **206.** Hvor meget må tabes på én dag, før systemet stopper for resten af dagen?
- **207.** Hvor meget må tabes i en måned, før alt stoppes og gennemgås?
- **210.** Hvad gør systemet ved et pludseligt kæmpe prisfald (flash crash) eller et markedsstop?
- **211.** Hvordan beskyttes systemet mod en programfejl, der fx køber 100 kontrakter i stedet for 1?
- **214.** Hvordan håndteres margin-krav, der pludselig stiger fra brokeren?
- **220.** Hvordan skrives alle ændringer af risikogrænser ned, så man kan se, hvem der ændrede hvad og hvornår?

### 14. Drift, overvågning og fejl

- **223.** Hvilke fejl skal stoppe alt med det samme, og hvilke må bare registreres og samles op senere?
- **226.** Hvad gør du, hvis TradeStation opdateres og en automatisering holder op med at virke?
- **227.** Skal der være en fast rutine efter hver handelsdag (gennemgang, afstemning mod brokeren)?
- **231.** Hvordan testes det, at alarmerne rent faktisk virker (fx en prøvealarm hver uge)?
- **232.** Hvordan undgås det, at Windows-opdateringer genstarter maskinen midt i en kørsel?
- **233.** Hvad sker der, hvis du ikke svarer på en alarm inden for en bestemt tid?

### 15. TradeStation og MultiCharts

- **241.** Hvilke begrænsninger i EasyLanguage har vi mødt, som kunne tale for at flytte dele af beregningerne ud af TradeStation?
- **244.** Findes der ting, vi bruger i TradeStation, som slet ikke findes i MultiCharts?

### 16. Automatisering og "fuldautomatisk"

- **249.** Skal der være én "dirigent", der styrer alle trin, fx EdgeFinder og EdgeCruncher i rækkefølge, eller kører de hver for sig?
- **256.** Hvordan undgås det, at automatikken skjuler fejl, som et menneske ville have set?

### 17. Arbejdsmåde, dokumentation og Claude

- **261.** Hvordan skal lokal Claude og cloud-Claude dele arbejdet mellem sig? Hvad skal hver især lave?
- **262.** Hvordan får cloud-Claude viden om databasens aktuelle indhold, når den ikke kan se den?
- **263.** Hvordan vil du helst have, at Claude stiller spørgsmål: ét ad gangen, samlet i en liste, eller i et skema som dette?
- **264.** Er der fejl eller misforståelser i samarbejdet med Claude indtil nu, som skal skrives ind i VIDENSLOG, så de ikke sker igen?
- **267.** Hvor ofte skal VIDENSLOG gennemgås og ryddes op, så gammel viden ikke vildleder?
- **268.** Skal alle programmer have faste automatiske afprøvninger (tests), der køres før hver ændring?
- **269.** Hvordan sikres det, at den lokale session altid har den nyeste udgave fra GitHub?
- **270.** Hvilke opgaver giver du helst til den lokale Claude, og hvilke til cloud-Claude?

### 18. Sikkerhed, backup og hardware

- **279.** Hvor lang tid tager det at bygge en server op igen fra bunden, og står det skrevet ned?
- **281.** Hvad sker der, hvis din GitHub-konto eller din mail bliver hacket?

### 19. Læring og forbedring over tid

- **282.** Hvordan skal systemet lære af de strategier, der fejler i den rigtige handel?
- **283.** Hvor ofte skal hele kæden gennemgås for at se, om metoderne stadig er de bedste?
- **287.** Hvordan sikres det, at nye idéer fra FriSnak bliver vurderet og ikke glemt?

### 20. Rapportering og nøgletal

- **294.** Hvordan skal rapporterne sammenligne de rigtige resultater med det, backtesten lovede?

### 21. Prioritering og næste skridt

- **296.** Hvilke spørgsmål i skemaet vil du have diskuteret ved Det Runde Bord?
- **297.** Hvilke emner mangler helt i dette skema?
- **300.** Er der noget, der allerede er bygget, som bør laves om, før der bygges videre ovenpå?

## Ikke relevant (12 spørgsmål)

### 2. Rammer: tid, penge, folk og regler

- **27.** Hvad er din erfaring med at handle futures manuelt? Hvilke markeder og hvor længe?
- **28.** Hvilke af dine tidligere strategier eller erfaringer skal systemet bygge videre på, og hvilke skal glemmes?
- **33.** Har brokeren regler for automatisk handel (fx krav om at godkende et handelsprogram)?

### 3. Markeder og instrumenter

- **34.** Præcis hvilke futures-markeder skal systemet handle (fx ES, NQ, CL, GC)?

### 4. Markedsforståelse og strategityper

- **51.** Hvilken slags markedsadfærd tror du mest på: trend (prisen fortsætter), tilbagevenden (prisen vender tilbage), udbrud eller noget andet?
- **52.** Hvorfor skulle der overhovedet være en edge i teknisk analyse på futures? Hvem er det, der taber de penge, systemet skal vinde?
- **53.** Hvilke markedsforhold tror du, systemet vil have sværest ved?
- **54.** Må systemet bruge volumen og open interest (antal åbne kontrakter), eller kun prisen?
- **57.** Hvad har du lært af andre systematiske tradere eller bøger, som skal bygges ind i systemet?
- **58.** Hvilke idéer har du testet før, som ikke virkede, og hvorfor tror du, de ikke virkede?

### 5. Prisdata

- **63.** Hvilken tidszone gemmes tiderne i, og hvordan håndteres sommer- og vintertid?

### 12. Handel i virkeligheden (execution)

- **192.** Hvor store positioner kan de valgte markeder tåle, før dine egne ordrer flytter prisen?
