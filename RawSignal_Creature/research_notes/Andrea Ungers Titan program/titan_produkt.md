# Andrea Ungers "Titan" — hvad er produktet?

> Researchnoter, indsamlet 2026-10-12. **Vigtig metodebegrænsning:** Unger Academys egne domæner (ungeracademy.com, learn.ungeracademy.com, ungermethod.com) samt Substack og Google Books kunne IKKE hentes direkte fra dette miljø (DNS-fejl / proxy afviste forbindelsen pga. organisationspolitik). Alle fund nedenfor stammer derfor fra søgemaskinens uddrag af disse sider, ikke fra en fuld læsning af selve siderne. Citater er gengivet som søgeværktøjet leverede dem. Detaljer bør efterprøves på de originale sider, før de bruges som endelige fakta.

## 1. Hvad er Titan præcist, og hvem laver det?

### Takeaway
Titan er Andrea Ungers/Unger Academys **egen (proprietære) software til at styre en portefølje af trading-strategier**. Hver måned vælger den ud fra strategiernes daglige gevinst/tab, hvilke strategier der skal handles live den næste måned, og hvor mange kontrakter hver skal have. Det er altså ikke en strategiportefølje, et kursus eller en handelsplatform i sig selv, men den deles med Unger Academys elever, og der hører en kursus/vejledningsside til ("Titan (EN)").

### Cited Findings
- Unger Academys blog har et indlæg med titlen "Titan - The Software to Automatically Manage Trading Systems", og der findes også en "Part 2" (EN) samt en italiensk udgave ("Titan - Il Software per gestire i Trading Systems in modo automatico | Parte 2") — [Unger Academy blog](https://ungeracademy.com/blog/titan-the-software-to-automatically-manage-trading-systems); [Part 2](https://ungeracademy.com/blog/titan-the-software-to-automatically-manage-trading-systems-or-part-2); [IT, del 2](https://ungeracademy.com/it/blog/titan-il-software-per-gestire-i-trading-systems-in-modo-automatico-or-parte-2)
- Unger: "This is why I use a program called Titan, which is a proprietary software that I also share with my students." — [The Unger Method](https://ungermethod.com/)
- Unger Academy: "...Titan, our proprietary software we use to filter our strategies month by month." — [Unger Academy blog (søgeuddrag)](https://ungeracademy.com/blog/the-puzzle-reassembled)
- Ifølge bloggen hjælper Titan teamet med hver måned at vælge, hvilke trading-systemer der skal bruges den følgende måned — [Unger Academy blog](https://ungeracademy.com/blog/titan-the-software-to-automatically-manage-trading-systems)
- Der findes en kursus-/vejledningsside "Titan (EN)" på Unger Academys læringsplatform. Uddraget siger, at softwaren hjælper med at vælge strategier til en portefølje og foreslår antal kontrakter ud fra kapital og risikoniveau. Siden viste "you are not yet enrolled in this course" — [learn.ungeracademy.com/courses/titan-en](https://learn.ungeracademy.com/courses/titan-en/)
- En tredjepart (nyhedsbrevet The Algorithmic Advantage) beskriver, at Unger "employs two proprietary portfolio management tools (only available to his students)—Titan and Zeus—built on MATLAB for strategy selection, portfolio construction and risk management" — [algoadvantage.substack.com, afsnit 038](https://algoadvantage.substack.com/p/038-andrea-unger-672-returns-sure)

### Inferences
- Titan er udviklet internt af Unger Academy. Der er intet fund, der peger på en ekstern partner/udvikler.
- Titan er Ungers eget arbejdsværktøj, som han dernæst har gjort tilgængeligt for elever. Det er ikke en kommercielt solgt, selvstændig software-hylde-vare.

### Gaps
- **Lanceringsdato blev ikke fundet.** Ingen kilde i søgningen angiver, hvornår Titan blev lavet eller første gang udgivet. Blogindlæggenes dato kunne ikke ses, fordi siderne ikke kunne hentes.
- Ingen del 1 af blogserien blev fundet separat (kun hovedindlægget og del 2).

## 2. Hvad gør Titan? (funktioner)

### Takeaway
Det, der er dokumenteret: (a) Titan tager **daglig P&L for hver strategi** som input, (b) **filtrerer/rangerer strategier** og sætter dem, der ikke præsterer, på pause eller stopper dem, (c) giver en **månedlig liste** over strategier, der skal handles live, (d) giver **antal kontrakter** pr. strategi ud fra kapital og risiko, (e) **kører forskellige test** af filtrene og (f) kan **omsætte strategier til mikro-kontrakter**. Der er ingen kilde på live-overvågning/dashboard i realtid, inkubation som separat funktion eller direkte styring af ordrer i platformen.

### Cited Findings
- Input og output: Titan tager daglig profit og tab for hver strategi og giver "the list of strategies to trade during next period and the number" [af kontrakter]. Unger: "I do that on a monthly basis." — [The Puzzle Reassembled](https://ungeracademy.com/blog/the-puzzle-reassembled)
- "Every month, from my software Titan, I get a list of the strategies that will go live on the coming month." — [What about My Trading Infrastructure?](https://ungeracademy.com/blog/my-trading-infrastructure)
- "Titan allows you to run different kinds of tests to evaluate the performance of your strategies and stop the ones that are not producing the results you expected." — [Unger Academy, Titan-side (søgeuddrag)](https://learn.ungeracademy.com/courses/titan-en/)
- Strategier, der ikke præsterer som ønsket, kan filtreres fra, så de automatisk sættes på pause eller stoppes — [Unger Academy blog](https://ungeracademy.com/blog/titan-the-software-to-automatically-manage-trading-systems)
- Mikro-kontrakter: Titan kan dele strategier, der er bygget på hele kontrakter, op i mikro-versioner. Eksempel: en backtest, der foreslår 0,1 kontrakt i råolie, handles som én Micro Crude Oil — [Unger Academy blog (søgeuddrag)](https://ungeracademy.com/blog/titan-the-software-to-automatically-manage-trading-systems)
- Tredjepartsbeskrivelse: Titan og Zeus "systematically rank strategies by recent performance momentum, applying strict performance criteria". Månedlige gennemgange roterer strategier og erstatter dem, der underpræsterer — [algoadvantage.substack.com](https://algoadvantage.substack.com/p/038-andrea-unger-672-returns-sure)
- **Markedsføringsudsagn (egen backtest, ikke uafhængigt efterprøvet):** I del 2 sammenligner Unger ufiltrerede og Titan-filtrerede equity-kurver for ca. 360 systemer. Nettoprofit falder fra ca. 2,9 mio. $ til ca. 1,637 mio. $ med filtre, men drawdowns bliver meget mindre. På britiske pund-strategier ville man uden filter have tabt ca. 80.000 $ over tre år mod ca. 3.900 $ med Titans filtre — [Part 2](https://ungeracademy.com/blog/titan-the-software-to-automatically-manage-trading-systems-or-part-2)
- Unger har oplyst, at han kører en portefølje på ca. 300 forskellige strategier — [Unger Academy (søgeuddrag)](https://ungeracademy.com/blog/my-trading-infrastructure)
- Strategikilde: "Million Dollar Database" beskrives som en portefølje på ca. 60 strategier, der stilles til rådighed for alle Unger Academy-elever. Titan bruges til at vælge fra den hver måned. Der findes en download med "Titan's Million Dollar Database Lists" — [Unger Academy, Trader of the Year 2023](https://ungeracademy.com/blog/trader-of-the-year-rossella-wins-with-an-incredible-profit-of-82-and-a-gain-of-eur16-330); [What's new](https://learn.ungeracademy.com/whats-new/)
- En elev (Trader of the Month, juni) valgte ca. 15 strategier manuelt og skrev, at han med flere systemer må gå over til "non-manual selection through software such as Titan" — [Unger Academy blog](https://ungeracademy.com/blog/trader-of-the-month-antonio-wins-with-a-47-return-and-a-eur10-000-gain-here-s-how-he-did-it)

### Inferences
- Titan virker som et **offline beslutningsværktøj til strategirotation og positionsstørrelse**, der kører med en fast takt (månedligt). Det handler ikke selv i markedet. Brugeren slår derefter strategierne til/fra og sætter kontraktantal i sin handelsplatform. Det er en slutning ud fra beskrivelserne ("I get a list..."). Ingen kilde siger direkte, at Titan sender ordrer.
- Filtrene ser ud til at være af typen "equity curve filter"/momentum på strategiens egen nylige performance (tredjepartsbeskrivelse plus Ungers egen tale om "filters").

### Gaps
- De præcise filterregler (vinduer, tærskler, metrikker) blev ikke fundet.
- Det er ikke dokumenteret, om Titan har dashboards/rapporter ud over lister og equity-kurver.
- Ingen kilde beskriver "inkubation" (out-of-sample-prøvetid før live) som en egentlig Titan-funktion.

## 3. Platforme: TradeStation, MultiCharts osv. Selvstændig eller tilføjelse?

### Takeaway
Titan er et **selvstændigt Windows-program bygget i MATLAB**. Det kræver, at MATLAB Runtime er installeret, og ifølge Unger Academy kan det ikke køre på en VPS. Det er ikke et plug-in til en platform. Ungers egen handelsplatform er MultiCharts. Hvordan data flyttes fra platformen ind i Titan, er ikke dokumenteret i de fundne kilder.

### Cited Findings
- Titans software kræver, at "Matlab Runtime" installeres først. Unger Academys software-side siger, at programmerne kører på Windows-pc'er eller dedikerede servere og "are NOT compatible with virtual servers (VPS)" — [learn.ungeracademy.com/software-en](https://learn.ungeracademy.com/software-en/)
- Tredjepart: Titan og Zeus er "built on MATLAB" — [algoadvantage.substack.com](https://algoadvantage.substack.com/p/038-andrea-unger-672-returns-sure)
- Unger: "the trading platform in my infrastructure is MultiCharts" — [What about My Trading Infrastructure?](https://ungeracademy.com/blog/my-trading-infrastructure)
- MultiCharts er den platform, Unger brugte ved sine fire World Cup-sejre, og den bruges i de fleste Unger Academy-kurser. Mange begreber blev oprindeligt udviklet i TradeStation og siden flyttet til MultiCharts. Ca. 99 % af scripts kan flyttes uændret mellem de to — [Unger Academy, Best Systematic Trading Software](https://ungeracademy.com/blog/best-systematic-trading-software); [Metatrader or MultiCharts?](https://ungeracademy.com/blog/metatrader-or-multicharts)

### Inferences
- Da input er daglig P&L pr. strategi, er Titan sandsynligvis platformsuafhængigt i princippet, hvis man kan eksportere daglige equity/P&L-data fra MultiCharts eller TradeStation. Det er en slutning. Selve eksportformatet er ikke fundet.

### Gaps
- Importformat og arbejdsgang (fx eksport fra MultiCharts Portfolio Trader) er ikke dokumenteret i kilderne.
- Det er ukendt, om Titan understøtter TradeStation-data direkte.

## 4. Pris, licens, målgruppe og adgang

### Takeaway
Titan sælges **ikke som selvstændigt produkt**. Det er forbeholdt Unger Academy-elever og gives typisk med som en del af/bonus til de store uddannelsesprogrammer (fx "AlgoTrader Fast"). Flere Unger-kilder kalder det gratis for elever. Der er ikke fundet nogen separat pris.

### Cited Findings
- AlgoTrader Fast-programmet nævner en "TITAN license" som bonus — [Unger Academy, AlgoTrader Fast / one-year-target](https://ungeracademy.com/one-year-target)
- Titan beskrives som gratis software for Unger Academy-elever — [Unger Academy blog (søgeuddrag)](https://ungeracademy.com/blog/titan-the-software-to-automatically-manage-trading-systems)
- "only available to his students" — [algoadvantage.substack.com](https://algoadvantage.substack.com/p/038-andrea-unger-672-returns-sure)
- På ungermethod.com står "Total Value: 197 €" i nærheden af Titan-afsnittet. Det er uklart, om beløbet angår Titan eller det omgivende kursus — [The Unger Method](https://ungermethod.com/)
- Titan-kursussiden viser "not yet enrolled", hvilket tyder på, at adgang er knyttet til tilmelding — [learn.ungeracademy.com/courses/titan-en](https://learn.ungeracademy.com/courses/titan-en/)
- Versionshistorik: Unger Academys "What's new"-side nævner en Titan-opdatering til **version 5.1.1 (februar 2023)** — [What's new](https://learn.ungeracademy.com/whats-new/)
- Til sammenligning (relateret, ikke Titan): Unger Strategy Club koster €97/md. eller €997/år (Standard) og €197/md. eller €1.997/år (VIP), og klubben er "RESERVED for students who have purchased the 'One Year Target' or 'AlgoTrader Fast' programs" — [ungerclub.com](https://ungerclub.com/); [Standard](https://ungerclub.com/unger-strategy-club-standard); [VIP (IT)](https://ungerclub.it/unger-strategy-club-vip)

### Inferences
- Versionsnummer 5.x i 2023 tyder på, at Titan har eksisteret i en del år før 2023. Det er en slutning, og det er ikke en lanceringsdato.
- Den reelle "pris" er prisen for et af hovedprogrammerne (One Year Target / AlgoTrader Fast). De priser blev ikke fundet i denne søgning.

### Gaps
- Pris på One Year Target / AlgoTrader Fast blev ikke fundet.
- Det er ukendt, om licensen er tidsbegrænset eller kræver fortsat medlemskab.
- Den nyeste version pr. oktober 2026 blev ikke fundet (sidst sete datapunkt er v5.1.1, feb. 2023).

## 5. Andre produkter med lignende navne eller overlappende roller (forvekslingsrisiko)

### Takeaway
Den vigtigste forvekslingsrisiko er **TradeStation TITAN X**, TradeStations nye handelsplatform (2025/2026), som intet har med Unger at gøre. Inden for Unger-universet overlapper **Zeus** med Titan (porteføljeværktøj med korrelation). **Million Dollar Database** og **Unger Strategy Club** er strategi-kilder, ikke software.

### Cited Findings
- **Zeus (Unger Academy):** et andet proprietært porteføljeværktøj, også MATLAB-baseret, som ifølge tredjepart vurderer korrelationer og overlap mellem handler — [algoadvantage.substack.com](https://algoadvantage.substack.com/p/038-andrea-unger-672-returns-sure). Unger Academys "What's new" nævner, at Zeus blev opdateret 2025-04-22 med "standard correlation, backtest optimization and minor bugfixes" — [What's new](https://learn.ungeracademy.com/whats-new/)
- **TradeStation TITAN X:** TradeStation Securities' nye flagskibsplatform. "Coming soon"-annoncering i aug. 2025, beta i slutningen af 2025, og annonceret/lanceret 5.–6. januar 2026 (pressemeddelelsen taler stadig om beta med bredere udrulning, mens bloggen samme dag siger "has arrived"). Funktioner: multi-asset-ordreticket, 11 diagramtyper, PC og Mac — [TradeStation, Coming Soon (aug. 2025)](https://www.tradestation.com/insights/2025/08/22/titan-x-coming-soon/); [BusinessWire, 5. jan. 2026](https://www.businesswire.com/news/home/20260105805579/en/TradeStation-Securities-Introduces-TITAN-X-The-Next-Generation-Trading-Platform); [TradeStation, "TITAN X Has Arrived" (6. jan. 2026)](https://www.tradestation.com/insights/2026/01/06/titan-x-has-arrived/)
- **Million Dollar Database:** strategi-database (ca. 60 strategier) til elever. Titan bruges til at vælge fra den — [Unger Academy](https://ungeracademy.com/blog/trader-of-the-year-rossella-wins-with-an-incredible-profit-of-82-and-a-gain-of-eur16-330)
- **Unger Strategy Club:** et abonnement på strategier for elever i One Year Target / AlgoTrader Fast — [ungerclub.com](https://ungerclub.com/)
- Et søgeresultat på Google Books viste en bog "Titan" tilknyttet navnet "Andrea Unger" (2019). Den kunne ikke åbnes, og en kontrolsøgning fandt ingen sådan bog — [Google Books (ikke verificeret)](https://books.google.com/books/about/Titan.html?id=BwiixQEACAAJ)
- Ikke-relaterede "Titan"-navne i finans: Titan (investeringsapp/wealth platform), Titan Quant Research Lab, "Titan Trading Platform" på Facebook — [Contrary Research](https://research.contrary.com/company/titan); [titanquantresearchlab.com](https://www.titanquantresearchlab.com/); [Facebook](https://www.facebook.com/titantradingplatform/)

### Inferences
- Hvis nogen taler om "Titan" i forbindelse med TradeStation, menes der sandsynligvis TITAN X-platformen og ikke Ungers værktøj. Da Unger-kredsen bruger EasyLanguage-kompatible platforme, er forvekslingen reel.
- Titan (strategivalg/rotation og kontraktstørrelse ud fra egen performance) og Zeus (korrelation/overlap, porteføljesammensætning) ser ud til at supplere hinanden. Titan er ikke det samme som Zeus.
- Den mulige bog "Titan" fra 2019 er formentlig en anden forfatter eller en fejl i metadata. Det er ikke bekræftet.

### Gaps
- Zeus' præcise funktioner og lanceringsdato blev ikke fundet i primærkilder.
- Google Books-posten kunne ikke verificeres.
- Ingen uafhængige anmeldelser eller forumdiskussioner (fx Trustpilot, Elite Trader) med konkrete Titan-erfaringer blev fundet. Trustpilot-siden for Unger Academy findes, men blev ikke læst: [Trustpilot](https://www.trustpilot.com/review/ungeracademy.com)
- Ingen podcast-interviews (Better System Trader, Chat With Traders), hvor Titan omtales specifikt, blev fundet.
