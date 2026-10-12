# Andrea Ungers metode til inkubation, aktivering, overvågning og deaktivering af strategier (Titan)

> **Vigtigt forbehold om kilderne (læs først).** Netværkspolitikken i dette miljø blokerede direkte hentning af ungeracademy.com, substack og ilgiornale.it (WebFetch og curl fejlede: "ENOTFOUND" / proxy 403). **Alt indhold nedenfor stammer derfor fra søgemaskinens uddrag og resuméer af de citerede sider, ikke fra en fuld læsning af selve siderne.** Citater i anførselstegn er gengivet sådan som søgeværktøjet returnerede dem fra kilden. De bør verificeres mod originalsiderne, før de bruges som endelige regler. Det gælder især tallene i "Puzzle Reassembled" og i benzin-eksemplet (se nedenfor). Næsten alle kilder er Unger Academys egne blog- og videotransskriptioner, altså markedsføringsmateriale fra Unger selv.
>
> Søgeord i hele noten: "Titan" = Ungers egen MATLAB-baserede software til porteføljestyring, som kun hans elever har adgang til. Den har intet at gøre med fintech-firmaet Titan.

## 1. Hvordan definerer Unger inkubation, og hvad skal en strategi igennem, før den går live?

### Takeaway
For Unger er "inkubation" ikke en fast prøveperiode efter udviklingen. Det er en **tilstand**, som en strategi er i, når den ikke handles med rigtige penge, mens dens equity stadig følges hver dag. Titan tester hver måned, om strategiens nyere out-of-sample-resultater er gode nok til at den kan "vågne op". Strategier, der ikke består testen, "bliver i inkubation". Jeg har ikke fundet en offentliggjort minimumslængde for inkubationen (fx "X måneder").

### Cited Findings
- Titans input er den daglige P&L for **alle** strategier, både de aktive og dem i inkubation. Udvælgelsen gennemgås én gang om måneden — [Unger Academy: The Puzzle Reassembled](https://ungeracademy.com/blog/the-puzzle-reassembled)
- Udvælgelsesreglen (Ungers egen beskrivelse, gengivet via søgeresumé): man sammenligner et længere tilbageblik på ca. **12–18 perioder (måneder)** med et kortere på ca. **3–6 måneder**. "Both shall be positive and the shorter term must also show an average monthly profit higher than the longer term." Strategier, der består, handles den kommende måned. "All those which fail will stay in incubation." — [Unger Academy: The Puzzle Reassembled](https://ungeracademy.com/blog/the-puzzle-reassembled)
- Selve parametrene (risikoprocent og længden på tilbageblikket) vælges ved at backteste hele kurven af strategier. Titan blev bygget til den tunge beregning — [Unger Academy: The Puzzle Reassembled](https://ungeracademy.com/blog/the-puzzle-reassembled)
- Første trin i at vælge strategier til live er et filter på strategiernes equity-linjer, og der bruges kun out-of-sample-data: "The first part of system selection is a filter on the equity lines, all out-of-sample, of the systems." — [Unger Academy: Effective Portfolio Management](https://ungeracademy.com/blog/effective-portfolio-management-how-to-choose-the-best-strategies-for-live-trading)
- Unger beskriver i en video systemer, som han holdt i "live incubation" (handlet live, men uden rigtige penge). Først efter at de havde klaret sig godt i den periode, satte han dem live med rigtige penge. Kilden er et sekundært resumé, og videoen blev ikke identificeret præcist — [Algo Advantage ep. 038 (resumé)](https://algoadvantage.substack.com/p/038-andrea-unger-672-returns-sure)
- Under udviklingen bruger han in-sample/out-of-sample-opdeling og stabilitetstest af parametrene (små ændringer omkring de valgte værdier) frem for klassisk walk-forward-optimering. Kilden er et sekundært resumé — [Algo Advantage ep. 038](https://algoadvantage.substack.com/p/038-andrea-unger-672-returns-sure)

### Inferences
- Ungers model er en **rotationsmodel**. Hele biblioteket af strategier (ca. 300) bliver ved med at producere "papir-equity" hver dag, og hver måned afgør en momentum-agtig regel på strategiernes egen equity, hvem der handles. Inkubation og "deaktivering" er altså samme tilstand. En ny strategi og en strategi, der er slået fra, behandles ens.
- Reglen "kort > lang, og begge positive" virker som et krav om, at strategien både skal tjene penge på lang sigt og være i en god periode lige nu (momentum i strategiens egen equity).
- En ny strategi kan tidligst blive aktiveret, når den har så meget out-of-sample-historik, at det lange tilbageblik kan beregnes (ca. 12–18 måneder). Det er **min fortolkning**, ikke noget Unger har skrevet.

### Gaps
- Jeg har ikke fundet en offentliggjort minimumsperiode for inkubation eller et minimumsantal handler for nye strategier.
- Det står ikke klart, om tilbageblikket måles i måneder eller i en anden periode. Kilden skriver "perioder", men i forbindelse med en månedlig gennemgang.
- Artiklen "The Puzzle Reassembled" er ifølge søgeværktøjet ca. 9 år gammel. Den nuværende version af Titan kan bruge andre regler.
- Titan del 1-artiklen (rotation, grundlogik) kunne ikke hentes.

## 2. Regler for at slå strategier til og fra live

### Takeaway
Unger har offentligt beskrevet tre slags filtre på equity-linjen, som Titan bruger: **(a) out-of-sample-performance** (fx reglen med kort og langt gennemsnit ovenfor), **(b) standardafvigelse** (strategier, der ligger mere end n standardafvigelser over eller under deres eget gennemsnit, filtreres fra), og **(c) equity-top** (kun strategier, der har lavet en ny top i equity inden for en given periode, fx det seneste år, er aktive). Han bruger også "pause og genaktivér ved første nye equity-top" som et eksempel på håndtering af en enkelt strategi i drawdown. Jeg har ikke fundet en Unger-regel af typen "sluk ved X % af historisk max drawdown".

### Cited Findings
- Tre måder at filtrere på: "analyze the out-of-sample performance, use the standard deviation, and use the equity peak as a filter" — [Unger Academy: Portfolio Management – How to Choose the Strategies to Trade](https://ungeracademy.com/posts/portfolio-management-how-to-choose-the-strategies-to-trade)
- Standardafvigelsesfiltret handler om systemer, der ligger "above or below n deviations from their average value". Equity-top-filtret aktiverer kun "the systems that are able to reach this value [an equity peak] in a given period of time" — [Unger Academy: Portfolio Management](https://ungeracademy.com/posts/portfolio-management-how-to-choose-the-strategies-to-trade)
- I transskriptionen af "Effective Portfolio Management" beskrives et filter, der frasorterer systemer, som klarer sig "either too well or too poorly relative to a moving average". Der nævnes også et equity-top-filter, som kun bruger systemer, der har haft en equity-top inden for det seneste år. Ifølge Unger har det sidste fungeret godt i hans backtests — [Unger Academy: Effective Portfolio Management](https://ungeracademy.com/blog/effective-portfolio-management-how-to-choose-the-best-strategies-for-live-trading)
- Titan filtrerer strategier og sætter dem automatisk på pause eller stopper dem, når de ikke klarer sig som forventet. En filtreret og en ufiltreret samlet equity sammenlignes. Den ufiltrerede tjener mere, men "the drawdown in that case is quite excessive" — [Unger Academy: Titan – The Software to Automatically Manage Trading Systems (part 2)](https://ungeracademy.com/blog/titan-the-software-to-automatically-manage-trading-systems-or-part-2)
- I et andet Titan-eksempel tjener den filtrerede tilgang ca. **$36.800 fra 2018**, mens det ufiltrerede resultat er negativt, fordi nogle systemer, der blev kodet i slutningen af 2018, klarede sig dårligt. Unger indrømmer, at den filtrerede drawdown var "very pronounced – even more in absolute value" end den ufiltrerede, men "much shorter", fordi den filtrerede equity var tilbage på en top — [Unger Academy: How to filter Drawdowns](https://ungeracademy.com/blog/how-to-filter-drawdowns)
- Eksempel med én strategi (benzin/RBOB), der var i tab i næsten 2 år. Tre scenarier blev sammenlignet: (1) altid aktiv, (2) kasseret efter **6 måneder i træk med tab eller sidelæns bevægelse**, (3) sat på pause efter de samme 6 måneder og **genaktiveret ved den første nye equity-top**. Strategien nåede en ny equity-top i marts 2022 og kunne genaktiveres fra april 2022 — [Unger Academy: Trading Strategies in Drawdown?](https://ungeracademy.com/blog/trading-strategies-in-drawdown-here-s-what-to-do-and-what-not-to-do-to-avoid-costly-mistakes)
- **Kilderne er uenige om tallene i benzin-eksemplet.** Det ene søgeresumé giver: altid aktiv ≈ $100.000 profit / ≈ $32.000 max DD, pause+genaktivering ≈ $55.000 / ≈ $20.000, kasseret ≈ $80.000 / $20.000. Det andet resumé citerer transskriptionen sådan: "Case 1 would have generated a profit of $55,000, with a maximum drawdown of about $20,000. Case 2, which is the compromise between the two in this case, would have generated a profit of $80,000 and a maximum drawdown of $20,000", og nummereringen af scenarierne er inkonsistent. **Det kan altså ikke fastslås, hvilket tal der hører til hvilket scenarie.** Det sikre er: at slå strategien fra/på pause sænkede max DD fra ca. $32k til ca. $20k og kostede profit sammenlignet med "altid aktiv" — [Unger Academy: Trading Strategies in Drawdown?](https://ungeracademy.com/blog/trading-strategies-in-drawdown-here-s-what-to-do-and-what-not-to-do-to-avoid-costly-mistakes)
- Samme artikel advarer om, at for mange filtre giver risiko for overfitting (overoptimering) — [Unger Academy: Trading Strategies in Drawdown?](https://ungeracademy.com/blog/trading-strategies-in-drawdown-here-s-what-to-do-and-what-not-to-do-to-avoid-costly-mistakes)
- Historisk max drawdown omtales som "an indication of what might be the ultimate limit beyond which we should not go further with our system". Det er en tommelfingerregel og ikke en formel Titan-regel — [Unger Academy: How to Figure Out If a Strategy Will Work…](https://ungeracademy.com/blog/how-to-figure-out-if-a-strategy-will-work-before-investing-your-money-in-it)
- I episode 016 af Better System Trader beskrives den afgørende færdighed som at kunne skelne mellem, at en strategis edge har ændret sig, og at den bare er i en normal drawdown. Episoden nævner også, at Unger selv på et tidspunkt var i **47–48 % drawdown** (personlig konto/konkurrence), tæt på margin-grænsen — [Better System Trader 016](https://bettersystemtrader.com/016-andrea-unger/)
- Unger advarer i "When To Stop Trading" om, at tradere efter en dårlig periode holder op med at respektere deres egne risikogrænser ("feel no pain after a certain threshold"). Artiklen handler om psykologi og giver ingen numerisk regel — [Unger Academy: When To Stop Trading](https://ungeracademy.com/blog/when-to-stop-trading)

### Inferences
- Ungers "sluk"-logik er **relativ og periodisk** (månedlig gennemgang af equity-momentum, afvigelse fra gennemsnit og nye toppe) frem for **absolut** (fx "sluk ved 1,5× historisk max DD"). En strategi bliver slukket, fordi den ikke længere opfylder aktiveringskriterierne ved næste månedsskifte, og der er ikke en særskilt stop-regel.
- Standardafvigelsesfiltret (som også frasorterer strategier, der klarer sig "for godt") minder om en mean-reversion-tanke: en strategi, der er langt over sit gennemsnit, forventes at falde tilbage. Det er **min fortolkning**. Unger forklarer ikke rationalet i de uddrag, der var tilgængelige.
- Ungers eget materiale viser tydeligt prisen ved det: filtrene sænker drawdown, men kan også koste profit og nogle gange give en større absolut drawdown. Han sælger det som en afvejning, ikke som en gratis gevinst.

### Gaps
- Jeg har ikke fundet konkrete værdier for "n" i standardafvigelsesfiltret, længden på glidende gennemsnit eller præcise vinduer for equity-toppen (ud over "seneste år").
- Jeg har ikke fundet regler baseret på antallet af tabende handler i træk.
- Jeg har ikke fundet Unger-regler af typen "equity under sit glidende gennemsnit = sluk", ud over formuleringen "relative to a moving average" (søgningen fandt kun generiske kilder om equity-curve trading, ikke Ungers egne).
- Søgeresultatet "Trade smaller if you're down 10%… reduce your position by 20%" blev tilskrevet Unger via en Better System Trader-artikel ([5 tips to accepting painful drawdowns](https://bettersystemtrader.com/5-tips-to-accepting-drawdowns/)). Det kunne ikke verificeres, at citatet faktisk er Ungers. **Bør ikke bruges uden kontrol.**

## 3. Hvilke målinger overvåger han for live strategier, og hvor ofte?

### Takeaway
Titans eneste rå input er **daglig P&L pr. strategi**. Ud fra den beregnes momentum i equity (gennemsnitlig månedlig profit over kort og langt vindue), afvigelse fra gennemsnittet, om der er en ny equity-top, værste dag og max drawdown. Selve beslutningerne træffes **månedligt**: hver måned giver Titan en liste over strategier og antal kontrakter til den kommende måned.

### Cited Findings
- "Every month, from my software Titan, I get a list of the strategies that will go live on the coming month." — [Unger Academy: What about My Trading Infrastructure?](https://ungeracademy.com/blog/my-trading-infrastructure)
- Output fra Titan: "the list of strategies to trade during next period and the number of contracts for each of them". Input: daglig P&L for hver strategi — [Unger Academy: The Puzzle Reassembled](https://ungeracademy.com/blog/the-puzzle-reassembled)
- Måling til position sizing: hver strategis **værste dag** bruges som "Worst Case Scenario" — [Unger Academy: The Puzzle Reassembled](https://ungeracademy.com/blog/the-puzzle-reassembled)
- Et tredjepartsresumé siger, at Titan (og et andet værktøj, Zeus) "systematically rank strategies by recent performance momentum, applying strict performance criteria". Begge er bygget i MATLAB — [Algo Advantage ep. 038](https://algoadvantage.substack.com/p/038-andrea-unger-672-returns-sure)
- Live-resultater sammenlignes løbende med backtest-forventningen (sekundært resumé) — [Better System Trader 016](https://bettersystemtrader.com/016-andrea-unger/)

### Inferences
- Rytmen er altså: data opdateres dagligt, og beslutninger træffes månedligt. Inden for måneden ændres der ikke på porteføljen ud fra Titan (min fortolkning; der står intet i kilderne om ændringer midt i måneden).

### Gaps
- Jeg har ikke fundet noget om overvågning inden for måneden (fx nødstop, hvis en strategi taber X på en uge).
- Jeg har ikke fundet noget om, at Unger offentligt måler slippage eller afvigelser i udførelsen som kriterium for at slukke en strategi.

## 4. Porteføljeallokering, korrelation og antal strategier

### Takeaway
Unger kører en meget bred portefølje på **ca. 300 strategier** på tværs af markeder, tidshorisonter og tilgange (trend/mean reversion). Det er kun en delmængde, der handles live i en given måned. Sizing sker ud fra hver strategis **værste dag** og en valgt risikoprocent, og den kan nedjusteres for **max drawdown** og **korrelation**. Kapital og korrelation tjekkes efter equity-filtret. Flere strategier på samme marked betyder færre kontrakter pr. strategi.

### Cited Findings
- Portefølje på "about 300 strategies on different markets with different approaches", som er svær at styre uden automatisering — [Unger Academy: Titan part 2](https://ungeracademy.com/blog/titan-the-software-to-automatically-manage-trading-systems-or-part-2) / [Unger Academy: My Trading Infrastructure](https://ungeracademy.com/blog/my-trading-infrastructure)
- Kontrakter = valgt risikoprocent divideret med strategiens værste dag. Tallet kan "be reduced further for the max drawdown of each strategy and correlations among systems" — [Unger Academy: The Puzzle Reassembled](https://ungeracademy.com/blog/the-puzzle-reassembled)
- Rækkefølge: først equity-filter (out-of-sample), derefter "a check is then made on the available capital… And this step is done simultaneously with a check on the correlation of the various systems". Det anbefales at starte med "unlimited capital" og først bagefter lægge kapital- og risikogrænser på ud fra drawdown eller worst case-perioder — [Unger Academy: Effective Portfolio Management](https://ungeracademy.com/blog/effective-portfolio-management-how-to-choose-the-best-strategies-for-live-trading)
- Kriterierne for at vælge strategier til næste periode beskrives som "equity, capital, correlation" — [Unger Academy: Effective Portfolio Management](https://ungeracademy.com/blog/effective-portfolio-management-how-to-choose-the-best-strategies-for-live-trading)
- Diversificering på tværs af tilgange, tidshorisonter og underliggende aktiver. Budget- og IT-begrænsninger kan forhindre, at man kører mange strategier samtidig — [Unger Academy: Portfolio Management](https://ungeracademy.com/posts/portfolio-management-how-to-choose-the-strategies-to-trade)
- Den værst tænkelige porteføljedrawdown er "the sum of all Drawdowns, but that event is highly uncommon" — [Unger Academy: How to Best Manage your Trading Systems' Portfolio](https://ungeracademy.com/blog/how-to-best-manage-your-trading-systems-portfolio)
- Han sænker størrelsen pr. system, når flere systemer handler samme marked (Better System Trader 016, emnet "controlling risk when trading multiple strategies") — [Better System Trader 016](https://bettersystemtrader.com/016-andrea-unger/)

### Inferences
- Det kendte offentlige materiale nævner ikke en fast øvre grænse for antallet af aktive strategier eller en korrelationsgrænse (fx "ρ < 0,5"). Korrelationen ser ud til at blive brugt til at **nedjustere størrelsen** frem for som et hårdt filter. Det er min fortolkning ud fra formuleringen "can be reduced further…".
- Summen af alle drawdowns som absolut worst case giver en enkel og konservativ øvre grænse for kapitalbehovet.

### Gaps
- Jeg har ikke fundet nogen numerisk risikoprocent pr. strategi eller for porteføljen. Kilden siger udtrykkeligt, at artiklen ikke angiver en.
- Jeg har ikke fundet præcise metoder til korrelation (daglig eller månedlig P&L, vindue, grænseværdi).
- Det er ikke oplyst, hvor mange af de ca. 300 strategier der typisk er aktive i en måned.

## 5. "Strategier i dvale" (hibernation), der kan genoplives

### Takeaway
Unger bruger ikke ordet "hibernation" i de kilder, jeg kunne finde. Ideen er dog helt central i hans metode: en strategi, der er slukket, bliver ikke slettet. Den går tilbage i **"incubation"/standby**, hvor dens papir-equity følges videre, og den bliver **automatisk genaktiveret**, når den igen opfylder filtrene, typisk ved en **ny equity-top**.

### Cited Findings
- Strategier, der ikke består den månedlige test, "will stay in incubation". De følges altså videre og kan bestå senere — [Unger Academy: The Puzzle Reassembled](https://ungeracademy.com/blog/the-puzzle-reassembled)
- Titan "pause[s] or stop[s]" strategier, der ikke klarer sig. Et eksempel viser genaktivering efter en ny equity-top — [Unger Academy: Titan part 2](https://ungeracademy.com/blog/titan-the-software-to-automatically-manage-trading-systems-or-part-2)
- Benzin-eksemplet: pause efter 6 måneder med tab eller sidelæns bevægelse, genaktivering ved første nye equity-top (marts 2022, så live fra april) — [Unger Academy: Trading Strategies in Drawdown?](https://ungeracademy.com/blog/trading-strategies-in-drawdown-here-s-what-to-do-and-what-not-to-do-to-avoid-costly-mistakes)
- Modsat påstand fra en tredjepart: strategier med "significant performance degradation are systematically retired rather than hastily 'patched'", og konceptet bliver enten genudviklet eller pensioneret helt — [Algo Advantage ep. 038](https://algoadvantage.substack.com/p/038-andrea-unger-672-returns-sure). **Bemærk:** et andet resumé med samme ordlyd stammer fra smtp.bardenay.com ("Andrea Unger's Systematic Trading: A Deep Dive"), som er en kilde af lav kvalitet og muligvis automatisk genereret. Den er ikke brugt som selvstændig kilde.

### Inferences
- Der ser ud til at være to niveauer: (1) **midlertidig pause** (inkubation/standby, automatisk genoplivning via Titan) for strategier, der bare er i en dårlig periode, og (2) **endelig pensionering eller genudvikling** for strategier, hvis koncept ikke længere virker. Grænsen mellem de to er ikke offentligt kvantificeret. Det er min sammenstilling af kilderne og ikke en formulering fra Unger.

### Gaps
- Jeg har ikke fundet noget om, hvornår en strategi i inkubation slettes helt (fx efter X år uden ny top).

## 6. Offentliggjorte konkrete tal (samlet oversigt)

### Takeaway
Der er få tal, der direkte er tilskrevet Unger. De fleste af dem stammer fra én artikel ("The Puzzle Reassembled") og ét eksempel (benzin). Ingen af dem bør bruges, før de er verificeret mod originalsiden.

### Cited Findings
- Langt tilbageblik **12–18**, kort tilbageblik **3–6** (måneder/perioder). Begge skal være > 0, og den gennemsnitlige månedlige profit på kort sigt skal være større end på lang sigt — [The Puzzle Reassembled](https://ungeracademy.com/blog/the-puzzle-reassembled)
- Gennemgang og rebalancering **hver måned** — [My Trading Infrastructure](https://ungeracademy.com/blog/my-trading-infrastructure)
- Equity-top inden for **det seneste år** som aktiveringsfilter — [Effective Portfolio Management](https://ungeracademy.com/blog/effective-portfolio-management-how-to-choose-the-best-strategies-for-live-trading)
- Pause efter **6 måneder i træk** med tab eller sidelæns bevægelse, genaktivering ved **første nye equity-top** (eksempel, ikke en generel regel) — [Trading Strategies in Drawdown?](https://ungeracademy.com/blog/trading-strategies-in-drawdown-here-s-what-to-do-and-what-not-to-do-to-avoid-costly-mistakes)
- Sizing: risikoprocent divideret med **værste dag** og nedjusteret for max DD og korrelation (ingen procentsats er oplyst) — [The Puzzle Reassembled](https://ungeracademy.com/blog/the-puzzle-reassembled)
- Ca. **300 strategier** i biblioteket — [Titan part 2](https://ungeracademy.com/blog/titan-the-software-to-automatically-manage-trading-systems-or-part-2)

### Inferences
- Til vores eget system: en enkel og dokumenteret startopskrift i Ungers ånd vil være: daglig P&L for alle strategier (både live og i inkubation) → månedlig gennemgang → aktivér, hvis gennemsnittet over 12 mdr. er > 0, gennemsnittet over 3 mdr. er > 0 og gennemsnittet over 3 mdr. er større end over 12 mdr. (eller hvis der har været en ny equity-top inden for 12 mdr.) → sizing ud fra værste dag → nedjustering for korrelation og max DD. **Det er en fortolkning og en sammenstilling, ikke Ungers præcise opskrift.** Parametrene bør vælges ved at backteste selve udvælgelsesreglen, ligesom Unger selv gør, og med opmærksomhed på overfitting.

### Gaps
- Jeg har ikke fundet tal for: minimumslængde på inkubation, minimumsantal handler, "n" i standardafvigelsesfiltret, risikoprocent, korrelationsgrænse, maksimalt antal aktive strategier eller en absolut stopgrænse i forhold til historisk max DD.
- Kurser og bøger ("The Unger Method", "The Successful Trader's Guide to Money Management", "Portfolio Secrets"-kurset) kunne ikke læses. Det er sandsynligvis dér, de præcise regler findes.
