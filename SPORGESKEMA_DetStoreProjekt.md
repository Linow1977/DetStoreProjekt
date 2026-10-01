# Spørgeskema — DetStoreProjekt

Oprettet 30. september 2026.

## Formål

Spørgeskemaet skal finde huller, åbne spørgsmål, udfordringer og mangler i
DetStoreProjekt. Spørgsmålene går både i dybden (detaljer i de dele, der
allerede er bygget) og i bredden (dele, der endnu ikke er beskrevet).

Spørgsmålene bygger på det, der ligger i projektet i dag: `CLAUDE.md`,
`VIDENSLOG.md`, `Task_RawSignal_Creature_EdgeFinder_opgave.md` og filerne i
`RawSignal_Creature/`.

**Uden for skemaet:** Pharos, Filter og RawSignal-filerne (de regnes som
samme ting) er bevidst udeladt. Derfor er der heller ingen spørgsmål om
RawSignal Creature, der bygger dem.

**Besvaret af Thomas 1. oktober 2026** via siden på claude.ai. Svarene er
skrevet ind her ordret. "Ved ikke endnu" betyder, at spørgsmålet stadig er
et åbent hul.

## Sådan bruges skemaet

- Skriv svaret under hvert spørgsmål efter `Svar:`.
- "Ved ikke endnu" er et fint svar. Det viser, hvor der er et hul.
- Spring gerne over og kom tilbage. Rækkefølgen er ikke vigtig.
- Svarene kan bagefter samles i `VIDENSLOG.md` og i delprojekternes egne filer.
- Fagord er forklaret kort i parentes første gang, de bruges.

## Indhold

1. Mål, vision og succes
2. Rammer: tid, penge, folk og regler
3. Markeder og instrumenter
4. Markedsforståelse og strategityper
5. Prisdata
6. TradingServer (database, bibliotek, lager)
7. TML-Server (backtest, analyse, selektering)
8. EdgeFinder (event-studie)
9. EdgeCruncher
10. Statistik og beskyttelse mod selvbedrag
11. Fra enkelt-strategi til portefølje
12. Handel i virkeligheden (execution)
13. Risikostyring
14. Drift, overvågning og fejl
15. TradeStation og MultiCharts
16. Automatisering og "fuldautomatisk"
17. Arbejdsmåde, dokumentation og Claude
18. Sikkerhed, backup og hardware
19. Læring og forbedring over tid
20. Rapportering og nøgletal
21. Prioritering og næste skridt

---

## 1. Mål, vision og succes

1. Hvad betyder "hedge-fond" helt konkret for dig: kun egne penge, eller på
   et tidspunkt også andres penge?
   Svar: inspiration for hvad målet er.
         indtil det er bevist at det virker 100% min egen penge - og så må vi hvad fremtiden bringer, men det er ikke noget vi skal bruge tid på nu.

2. Hvornår er projektet en succes? Beskriv det i tal (fx afkast pr. år,
   største tilladte tab, antal strategier i drift).
   Svar: når profit er relativ konstant og funktionelle strategi produktionen er stabil.
         ingen % afkast mål.

3. Hvilket afkast pr. år sigter du efter, og hvor stort et fald fra top til
   bund (drawdown) kan du leve med, før du stopper?
   Svar: Ved ikke endnu

4. Når du siger "på niveau med verdens bedste" — hvilke fonde eller hvilke
   tal sammenligner du med?
   Svar: Målet er et system af en seriøs karakter, der lav seriøse og stabile strategier, med stabil afkast.

5. Hvad er den vigtigste ting, projektet skal kunne om 6 måneder? Om 1 år?
   Om 3 år?
   Svar: 6 måneder. en pip-line der virker.
         1 år. Profit skabende strategier, ingen profit mål men tegn på stabil afkast.
         3 år. > 10 % afkast pr mådenede.

6. Hvornår skal den første strategi handle med rigtige penge? Er der en dato
   eller en betingelse?
   Svar: forår 2027

7. Hvad er "daytrading" for dig: skal alle handler være lukket ved dagens
   slutning, eller må en position stå natten over?
   Svar: kort handler, samme dages luk.

8. Hvad er den største risiko for, at projektet ikke lykkes, som du ser det
   i dag?
   Svar: Mig, et system der ikke bliver stabilt, kapital mangel.

9. Hvad vil du aldrig gå på kompromis med (fx kvalitet, sikkerhed, egen
   kontrol)?
   Svar: kvalitet, stabilitet.

10. Hvad vil du gerne have, at systemet kan, som du ikke tror, andre private
    tradere har?
    Svar: en stabil Edge, en stabil flydende produktil og pip-line.

11. Hvornår vil du stoppe projektet eller ændre retning? Findes der en
    "exit-regel" for selve projektet?
    Svar: Ved ikke endnu

12. Skal systemet kun finde strategier, eller skal det også selv beslutte,
    hvilke der handles, og selv sætte dem i drift?
    Svar: måske over tid.

13. Hvordan skal man kunne se, om projektet bevæger sig i den rigtige
    retning måned for måned (delmål)?
    Svar: en profil kurver der stille og roligt vokser, en stabil produktion af strategier.

14. Er målet at slå et bestemt indeks, eller at tjene penge uanset om
    markedet går op eller ned?
    Svar: lave profit når market går op og ned.

15. Hvad er vigtigst for dig: højt afkast, jævnt afkast eller lav risiko?
    Sæt dem i rækkefølge.
    Svar: lav risiko, jævnt afkast, højt afkast.

16. Hvad skal der til, for at du stoler nok på systemet til at lade det
    handle, uden at du kigger med?
    Svar: kommer ikke til at ske!

17. Er der en tidsfrist, hvor projektet skal kunne betale for sig selv?
    Svar: 2 til 3 år

## 2. Rammer: tid, penge, folk og regler

18. Hvor mange timer om ugen bruger du på projektet i dag, og hvor mange kan
    du bruge fremover?
    Svar: 6 til 12 timer pr dag.
          1 til 6 timer pr dag.

19. Hvor meget kapital er afsat til handel, når systemet er klar?
    Svar: Ved ikke endnu

20. Hvor meget må projektet koste pr. måned i software, data, servere og
    abonnementer?
    Svar: Ved ikke endnu

21. Er der andre personer involveret nu eller senere (partner, programmør,
    revisor, advokat)?
    Svar: måske sener.

22. Hvis du er væk i en måned, hvem holder så øje med systemet og de åbne
    handler?
    Svar: alt mig.

23. Skal handlen ske som privatperson eller gennem et selskab? Er det
    afklaret med en revisor, hvordan gevinster og tab beskattes?
    Svar: der er jeg ikke endnu.

24. Har du undersøgt, hvilke regler (fx Finanstilsynet) der gælder, hvis du
    senere vil forvalte andres penge?
    Svar: det til er jeg ikke kommet endnu.

25. Hvilken broker (mægler) skal handlerne gå gennem? Er det besluttet?
    Svar: ikke besluttet.

26. Er der krav fra brokeren om minimumskapital, margin
    (sikkerhedsstillelse) eller særlige kontotyper for futures?
    Svar: der er jeg ikke endnu.

27. Hvad er din erfaring med at handle futures manuelt? Hvilke markeder og
    hvor længe?
    Svar: ikke relevant.

28. Hvilke af dine tidligere strategier eller erfaringer skal systemet bygge
    videre på, og hvilke skal glemmes?
    Svar: spørgsmål ikke relevant.

29. Hvor meget af beslutningerne vil du selv tage, og hvor meget må Claude
    beslutte uden at spørge?
    Svar: intet.

30. Hvor meget af din egen formue er du parat til at sætte på spil i alt?
    Svar: det der skal til for en mand med en mellem dansk indkomst.

31. Hvad sker der med projektet og kontoen, hvis du bliver syg i længere
    tid?
    Svar: det må jeg se på til den tid.

32. Hvilke dele af arbejdet vil du gerne have hjælp fra et menneske til (fx
    revisor eller programmør)?
    Svar: der er jeg ikke kommet til endnu.

33. Har brokeren regler for automatisk handel (fx krav om at godkende et
    handelsprogram)?
    Svar: ikke relevant.

## 3. Markeder og instrumenter

34. Præcis hvilke futures-markeder skal systemet handle (fx ES, NQ, CL, GC)?
    Svar: ikke relevant.

35. Skal alle strategier virke på alle markeder, eller må en strategi kun
    virke på ét marked?
    Svar: det skal virke hvor det er skabt

36. Skal der kunne handles micro-kontrakter (små kontrakter), så positionen
    kan gøres mindre?
    Svar: ja.

37. Hvilke tidspunkter på døgnet må systemet handle: kun den normale
    børstid, eller også natten (elektronisk handel)?
    Svar: hvor det har sin edge.

38. Hvordan håndteres dage med vigtige nyheder (fx renteudmelding, jobtal)?
    Skal systemet holde pause?
    Svar: nej.

39. Hvordan håndteres helligdage, halve handelsdage og lukkede børser?
    Svar: Ved ikke endnu

40. Hvordan skifter systemet fra én kontrakt til den næste, når en
    futures-kontrakt udløber (rollover)?
    Svar: manuelt.

41. Hvilke tidsrammer skal der arbejdes med? I dag nævnes fire workspaces
    (5,10,60 / 10,20,60 / 5,30,120 / 5,10,120). Er det den endelige liste,
    og hvorfor netop dem?
    Svar: der er en liste der startes med.

42. Hvad betyder de tre tal i hvert workspace helt præcist (Data1, Data2,
    Data3), og hvad bruges hver af dem til?
    Svar: Data2 og Data3 er til søgen og beregning af edge.
          Data1 optimering af handels entry.

43. Skal systemet kunne bruge data fra ét marked til at handle et andet (fx
    renter til at handle aktieindeks)?
    Svar: Ved ikke endnu

44. Er der markeder, du bevidst vil holde dig fra, og hvorfor?
    Svar: Ved ikke endnu

45. Hvor mange markeder skal handles samtidig, når systemet er i fuld drift?
    Svar: kan der ikke svares på da det kommer an på hvilke strategier der er modne til af handle.

46. Hvor stor en daglig omsætning (likviditet = hvor let man kan købe og
    sælge) skal et marked mindst have for at være med?
    Svar: Ved ikke endnu

47. Hvordan kommer nye markeder på listen senere, og efter hvilke regler?
    Svar: nå filter kolonnerne er kørt igennem.

48. Skal strategierne handle i begge retninger (købe og sælge først), eller
    kun den ene vej?
    Svar: hver sin retning.

49. Hvordan håndteres det, at markederne opfører sig forskelligt, når Asien,
    Europa og USA har åbent?
    Svar: strategierne handler efter det markeder de handler på.

50. Skal der tages højde for mønstre, der følger årstiden (fx energimarkeder
    om vinteren)?
    Svar: nej.

## 4. Markedsforståelse og strategityper

51. Hvilken slags markedsadfærd tror du mest på: trend (prisen fortsætter),
    tilbagevenden (prisen vender tilbage), udbrud eller noget andet?
    Svar: ikke relevant.

52. Hvorfor skulle der overhovedet være en edge i teknisk analyse på
    futures? Hvem er det, der taber de penge, systemet skal vinde?
    Svar: ikke relevant.

53. Hvilke markedsforhold tror du, systemet vil have sværest ved?
    Svar: ikke relevant.

54. Må systemet bruge volumen og open interest (antal åbne kontrakter),
    eller kun prisen?
    Svar: ikke relevant.

55. Hvor hurtigt tror du, en edge forsvinder, når den først er fundet?
    Svar: kan man ikke vide.

56. Skal systemet lede efter edges, der virker på tværs af markeder, eller
    edges, der kun gælder ét marked?
    Svar: Ved ikke endnu

57. Hvad har du lært af andre systematiske tradere eller bøger, som skal
    bygges ind i systemet?
    Svar: ikke relevant.

58. Hvilke idéer har du testet før, som ikke virkede, og hvorfor tror du, de
    ikke virkede?
    Svar: ikke relevant.

## 5. Prisdata

59. Hvor kommer prisdataene fra i dag? Kun TradeStation, eller også andre
    kilder?
    Svar: Tradestation.

60. Hvor mange års historik findes der for hvert marked, og er det nok?
    Svar: vi bruger det der kan skaffes.

61. Hvordan kontrolleres dataene for fejl (huller, dubletter, forkerte
    priser, spring)?
    Svar: Ved ikke endnu

62. Bruges "continuous contracts" (sammensatte kontrakter over flere udløb)?
    Hvis ja: hvordan er de sat sammen (justeret eller ikke justeret)?
    Svar: vi bruger det den data udbyder har.

63. Hvilken tidszone gemmes tiderne i, og hvordan håndteres sommer- og
    vintertid?
    Svar: ikke relevant.

64. Er det sikkert, at TradeStation og MultiCharts giver præcis de samme
    bars (prisstænger) for samme marked og tidsramme?
    Svar: nej

65. Skal prisdata også gemmes i TradingDB, eller kun ligge i TradeStation?
    Svar: TradingDB

66. Hvad sker der, hvis dataleverandøren retter historiske data bagefter?
    Opdager systemet det?
    Svar: Ved ikke endnu

67. Skal der bruges tick-data eller kun minut-bars? Hvornår er minut-bars
    ikke præcise nok?
    Svar: kun minut, det er nok.

68. Hvordan sikres det, at en backtest kun bruger data, der rent faktisk var
    kendt på det tidspunkt (ingen "look-ahead" = snyd med fremtidige data)?
    Svar: det arbejdes  der på.

69. Hvor mange data skal gemmes til side, som aldrig bruges under udvikling
    (out-of-sample), men kun til den endelige kontrol?
    Svar: det arbejdes der på.

70. Hvem "ejer" beslutningen om, hvilke dataperioder der må bruges til hvad
    — og står det skrevet ned?
    Svar: mig.

71. Skal der bruges andre data end pris og volumen (fx volatilitetsindeks,
    kalender, sæson)? Eller holdes det strengt til prisdata?
    Svar: Ved ikke endnu

72. Hvordan gemmes de rå data, så de aldrig kan ændres ved en fejl (fx en
    skrivebeskyttet kopi)?
    Svar: Ved ikke endnu

73. Hvilken tidsramme er den mindste, der skal bruges, og hvorfor?
    Svar: Ved ikke endnu

74. Hvordan håndteres bars med meget lidt handel (fx om natten)?
    Svar: Ved ikke endnu

75. Skal der hver dag være en kort data-rapport, der viser, om de nye data
    er kommet rigtigt ind?
    Svar: Ved ikke endnu

76. Hvordan sikres det, at alle backtests bruger præcis samme udgave af
    dataene, så de kan sammenlignes?
    Svar: der vil kun være den samme data tilgængelig.

77. Hvad koster bedre data fra en separat dataleverandør, og er det pengene
    værd?
    Svar: Ved ikke endnu

## 6. TradingServer (database, bibliotek, lager)

78. Hvad er den fulde liste over tabeller i TradingDB i dag, og hvad bruges
    hver til?
    Svar: Ved ikke endnu

79. Findes der en tegning eller beskrivelse af, hvordan tabellerne hænger
    sammen? Hvis ikke — skal der laves en?
    Svar: ja det skal laves på et tidspunkt.

80. Hvordan tages der backup af TradingDB? Hvor ofte, hvor ligger den, og er
    en gendannelse nogensinde blevet afprøvet?
    Svar: TradingDB server et vist sat til SATA3

81. Hvad er forskellen på "Database", "Bibliotek" og "Lager" i
    TradingServer? Hvad hører til hvilken?
    Svar: Ved ikke endnu

82. Hvor skal resultatfilerne fra backtests ligge, og hvor længe skal de
    gemmes?
    Svar: Data Server, TradingDB.
          så lang tid der er relevant, data er guld værd.

83. Hvor meget diskplads forventes der at blive brugt, når alle backtests
    for alle workspaces og markeder er kørt?
    Svar: det der er behov for.

84. Hvordan navngives mapper og filer, så man om 2 år stadig kan finde ud
    af, hvad der er hvad?
    Svar: Mig.

85. Skal hver kørsel have et unikt kørselsnummer, så man altid kan spore et
    resultat tilbage til præcis de data og den kode, der lavede det?
    Svar: Ja.

86. Hvad sker der i databasen, når en regel eller et program ændres? Skal
    gamle resultater slettes, markeres som forældede eller beholdes?
    Svar: Ved ikke endnu

87. Hvem må skrive i databasen: kun programmerne, eller også dig manuelt?
    Svar: begge.

88. Hvordan undgås det, at to programmer skriver i samme tabel samtidig og
    ødelægger data for hinanden?
    Svar: Ved ikke endnu

89. Skal den lokale Claude-session og cloud-sessionen på et tidspunkt kunne
    se databasen på samme måde (fx via et udtræk, der lægges i git)?
    Svar: ja.

90. Skal der være en testdatabase ved siden af den rigtige, så nye
    programmer kan afprøves uden risiko?
    Svar: Ved ikke endnu

91. Hvordan skal databasen klare det, når der kommer millioner af
    resultatrækker?
    Svar: Ved ikke endnu

92. Hvilke spørgsmål vil du selv kunne stille databasen uden hjælp (fx "vis
    alle, der har bestået")?
    Svar: Ved ikke endnu

93. Skal der være et enkelt skærmbillede (en app), hvor du kan se indholdet
    uden at skrive kode?
    Svar: ja

94. Hvad er reglen for navne på tabeller og kolonner (små eller store
    bogstaver, dansk eller engelsk)?
    Svar: Ved ikke endnu

95. Hvordan registreres det, hvilken programudgave der lavede hver række i
    databasen?
    Svar: Ved ikke endnu

## 7. TML-Server (backtest, analyse, selektering)

96. Hvad er TML-Serveren fysisk: en separat computer, en virtuel maskine
    eller samme maskine som TradingServer?
    Svar: separate maskiner.

97. Hvilke programmer kører på TML-Serveren (TradeStation, MultiCharts,
    Python, andet)?
    Svar: alt der er behov for.

98. Hvordan sendes arbejde mellem TradingServer og TML-Server (filer,
    database, netværksmappe)?
    Svar: Ved ikke endnu

99. Hvor mange backtests kan køres samtidig, og hvad er flaskehalsen:
    computerkraft, TradeStation-licenser eller tid?
    Svar: Ved ikke endnu

100. Hvor lang tid tager én backtest i dag? Hvor lang tid vil alle tage
     samlet?
     Svar: Ved ikke endnu

101. Hvad betyder "Selektering" konkret: hvem eller hvad vælger, og efter
     hvilke regler?
     Svar: selektering = udvælgelse.
           der laves en rapport jeg kigger på.

102. Hvilke analyser skal ligge på TML-Serveren, og hvilke skal ligge i
     Python et andet sted?
     Svar: Ved ikke endnu

103. Hvad sker der, hvis TML-Serveren går ned midt i en lang kørsel? Kan den
     fortsætte, hvor den slap?
     Svar: Ved ikke endnu

104. Skal TML-Serveren kunne styres, mens du ikke er ved computeren (fx over
     fjernskrivebord eller telefon)?
     Svar: ja

105. Skal der være adskillelse mellem maskinen, der udvikler strategier, og
     maskinen, der handler med rigtige penge?
     Svar: ja

106. Hvordan holdes programversioner ens på de to servere?
     Svar: opsætning

107. Hvor mange TradeStation-installationer og -licenser er der, og kan der
     købes flere?
     Svar: de installationer der er behov for, de arbejder offline, opdateres en afgangen.
           indtil videre en licens.
           Ja.

108. Kan backtests køre om natten uden opsyn? Hvad forhindrer det i dag?
     Svar: Det skal køre hele tiden.

109. Hvordan fordeles arbejdet, hvis der kommer flere TML-maskiner?
     Svar: automatisk.

110. Hvordan sikres det, at en backtest giver præcis samme resultat, hvis
     den køres igen?
     Svar: kontrol

111. Hvor gemmes backtest-indstillingerne (kurtage, slippage, handelstider),
     så de ikke ændres ved et uheld?
     Svar: Ved ikke endnu

## 8. EdgeFinder (event-studie)

112. Forklar med dine egne ord, hvad EdgeFinder skal finde. Hvad er en
     "edge" for dig?
     Svar: den skal finde mulig statistisk baseret fordel ved signalet.

113. Hvad er et event-studie i dette projekt: hvad måles der efter hvert
     signal (fx prisbevægelse efter 5, 10, 30 bars)?
     Svar: hvad sker der når signalet tænder.

114. Hvilke tidshorisonter efter et signal skal måles?
     Svar: Ved ikke endnu

115. Hvad sammenlignes signalets resultat med? Med tilfældige tidspunkter,
     med markedet generelt, eller med noget andet?
     Svar: RSA, OOS og Tid

116. Hvornår er et resultat "Passed"? Hvilke tal skal være opfyldt?
     Svar: under udvikling

117. Hvornår er det "Failed"? Og skal "næsten bestået" være en tredje
     kategori?
     Svar: under udvikling

118. Hvor mange hændelser skal der mindst være i en test, før resultatet kan
     bruges?
     Svar: under udvikling

119. Skal EdgeFinder se på både køb- og salgsretning for hvert signal?
     Svar: det er en opgave der ligger ved RSA der står for signal analyse.

120. Hvordan håndteres signaler, der ligger tæt efter hinanden og derfor
     måler den samme prisbevægelse flere gange?
     Svar: der sker i Edge-Finder/CC.

121. Skal resultatet deles op i perioder (fx år for år) for at se, om edgen
     er stabil over tid?
     Svar: Ja

122. Skal resultatet deles op efter markedstype (stigende, faldende,
     sidelæns, rolig, urolig)?
     Svar: nej

123. Hvilke workspace-indstillinger skal EdgeFinder sætte i TradeStation, og
     hvor er de beskrevet?
     Svar: det er ikke Edge-Finders opgave.
           det ligger i TradingDB

124. Hvad skal ske, hvis backtest-data i mappen er ufuldstændige eller
     forkerte ("stop process og meld fejl")? Hvem får beskeden, og hvordan?
     Svar: ikke afgjort.
           mig.
           automatisk

125. Hvilke resultater skal "journalføres", og i hvilken tabel?
     Svar: det er ikke afgjort

126. Skal EdgeFinder skrives i Python? Findes der allerede noget
     analysekode, der skal genbruges?
     Svar: der arbejdes der på

127. Hvem bestemmer rækkefølgen, tingene testes i i EdgeFinder, og er der en
     prioritering?
     Svar: mig

128. Hvordan måles det, om en edge er stor nok til at betyde noget i kroner
     og øre, og ikke kun i statistikken?
     Svar: en opgave der ligger ved Pharos

129. Skal EdgeFinder allerede regne kurtage og slippage med i event-studiet?
     Svar: Ved ikke endnu

130. Hvad gør EdgeFinder med et resultat, der er godt på én tidsramme og
     dårligt på en anden?
     Svar: Ved ikke endnu

131. Skal samme test køres på alle fire workspaces, og hvordan vægtes
     resultaterne mod hinanden?
     Svar: den skal køres på alle de workspaces der er vagt på nu værende tidspunkt.

132. Hvordan vælges indstillingerne for selve event-studiet (fx hvor længe
     der måles), uden at de også bliver tilpasset til at se godt ud?
     Svar: der arbejdes der på

133. Skal EdgeFinder kunne køre igen af sig selv, når der kommer nye data?
     Svar: ja

134. Hvor mange tests forventer du vil bestå? Og hvad gør vi, hvis næsten
     ingen eller næsten alle består?
     Svar: forventer et lav antal der består, mindre end 5 %

## 9. EdgeCruncher

135. Hvad skal EdgeCruncher gøre? Beskriv det, som du forestiller dig det,
     selvom det ikke er færdigt.
     Svar: der er usikkerhed om Edge-Finder og Edge -Cruncher skal ligges sammen til en process.

136. Hvad får EdgeCruncher ind (kun "Passed" fra EdgeFinder?), og hvad
     sender den videre?
     Svar: Den få kun Pass og sender interessante kandidater videre til OOS og Pharos.

137. Skal EdgeCruncher kombinere flere signaler til én strategi? Hvor mange
     må der højst kombineres?
     Svar: Ved ikke endnu

138. Hvor kommer indgang, udgang, stop-loss og gevinstmål ind i billedet? Er
     det EdgeCruncher eller et senere trin?
     Svar: Edge-Finder

139. Hvad er det næste trin efter EdgeCruncher? Findes der et navn og en idé
     for det endnu?
     Svar: Pharos

140. Hvordan undgår EdgeCruncher at finde tilfældige kombinationer, der kun
     ser gode ud, fordi der er prøvet så mange?
     Svar: OOS

141. Hvor mange kombinationer forventer du, at EdgeCruncher skal prøve?
     Tusinder, millioner?
     Svar: 100

142. Hvor lang tid må EdgeCruncher bruge pr. kørsel?
     Svar: det der er behov for

143. Hvordan vil du selv kunne se og forstå, hvorfor EdgeCruncher har valgt
     det, den har valgt?
     Svar: Rapport og i TradingDB

144. "Data1, når den senere bliver mindre end Data2 (entry-finpudsning)" —
     hvor og hvornår hører det til?
     Svar: Ved ikke endnu

145. Skal EdgeCruncher arbejde i Python, i TradeStation eller i begge?
     Svar: Ved ikke endnu

146. Skal EdgeCruncher tage højde for, at markedet ændrer sig over tid (fx
     ved at teste de nyeste data for sig)?
     Svar: den bruges kun en gang

147. Hvilke slags udgange skal prøves (efter tid, stop, gevinstmål, modsat
     signal)?
     Svar: Ved ikke endnu

148. Skal strategierne fra EdgeCruncher være så enkle som muligt? Hvor mange
     regler må en strategi højst have?
     Svar: Ja.
           ikke definerede  endnu

149. Hvordan gemmes EdgeCrunchers resultater, så de kan sammenlignes med
     senere kørsler?
     Svar: TradingDB

150. Hvornår er en strategi fra EdgeCruncher "færdig" og klar til næste
     trin?
     Svar: nu de har været igennem OOS.

## 10. Statistik og beskyttelse mod selvbedrag

151. Hvordan tages der højde for, at der testes tusindvis af signaler, så
     nogle vil se gode ud af ren tilfældighed (multiple testing)?
     Svar: Ved ikke endnu

152. Tælles det, hvor mange forsøg der i alt er lavet, før en strategi blev
     fundet? Det er nødvendigt for at vurdere, hvor meget held der er med.
     Svar: der køres kun en backtest pr workspace.
           der sammenlines med OOS og incubatiin

153. Hvilken metode skal bruges til out-of-sample-test (walk-forward, fast
     opdeling, andet)?
     Svar: Rå data 1-2 år efter backtest periode på minimum 3-5 år

154. Må out-of-sample-data nogensinde bruges igen, efter de er set første
     gang? Hvad er reglen?
     Svar: nej

155. Hvordan testes, om en strategi er robust, når parametrene ændres en
     smule (fx 20 i stedet for 21)?
     Svar: OOS data

156. Skal strategier testes på andre markeder end dem, de blev fundet på,
     som ekstra kontrol?
     Svar: Ved ikke endnu

157. Skal der laves "Monte Carlo"-test (tilfældig blanding af handlerne for
     at se, hvor slemt det kunne være gået)?
     Svar: ja men kun til fremtid analyse

158. Hvilke nøgletal skal hver strategi vurderes på (fx Sharpe, profit
     factor, gennemsnitlig handel, max drawdown)? Og hvilket er det
     vigtigste?
     Svar: alle de klassiske ,men holdt simpelt - tid vil vise hvilke tal der vise de mest relevante tal at kigge efter.

159. Hvad er den mindste gennemsnitlige gevinst pr. handel, der kan overleve
     kurtage og slippage?
     Svar: 3 gange omkostninger pr handle

160. Skal der være et fast sæt af "kontrolsignaler" (tilfældige signaler),
     som alle resultater sammenlignes med?
     Svar: Ved ikke endnu

161. Hvordan opdages det, hvis en resultatperiode domineres af én enkelt
     ekstrem dag eller hændelse?
     Svar: år for år analyse, hvor stor er udsving

162. Hvem eller hvad skal "angribe" en strategi, før den godkendes — Det
     Runde Bord, et fast testprogram eller begge dele?
     Svar: fast testprogram.

163. Skal Det Runde Bord have et fast verdikt og en score (fx Go / No-go /
     Juster og 0–10)? Det står som ikke besluttet.
     Svar: de har intet med selve processen at gøre når det er færdigt

164. Hvordan dokumenteres alle forkastede idéer, så de ikke testes igen ved
     en fejl?
     Svar: Ved ikke endnu

165. Hvor sikre skal vi være (signifikansniveau), før noget kaldes en edge?
     Svar: Ved ikke endnu

166. Skal der rettes for antallet af tests med en fast metode (fx "Deflated
     Sharpe Ratio")? Hvem vælger metoden?
     Svar: Ved ikke endnu

167. Hvordan undgås det, at man kigger på resultaterne og justerer, til det
     ser godt ud (skjult overtilpasning)?
     Svar: en test, en OOS, der efter er det låst

168. Hvor lang skal en out-of-sample-periode være, før den tæller?
     Svar: 1-2 år

169. Skal systemet testes på "falske" data (fx tilfældigt blandede priser)
     for at se, om det også finder edge i ren støj?
     Svar: Ved ikke endnu

170. Hvordan opdages fejl med fremtidige data (look-ahead) automatisk i
     koden?
     Svar: Ved ikke endnu

171. Hvordan vurderes en strategi med få handler og stor gevinst mod en med
     mange handler og lille gevinst?
     Svar: Ved ikke endnu

## 11. Fra enkelt-strategi til portefølje

172. Hvor mange strategier skal køre samtidig, når systemet er i fuld drift?
     Svar: det der er kapital til

173. Hvordan måles det, om to strategier i virkeligheden gør det samme (for
     høj sammenhæng/korrelation)?
     Svar: en opgave der ligger i Pharos

174. Hvordan fordeles kapitalen mellem strategierne: lige meget, efter
     risiko, eller efter noget andet?
     Svar: Ved ikke endnu

175. Hvor ofte skal porteføljen gennemgås og ændres?
     Svar: opgaven ligger i Pharos, månedlig kontrol

176. Hvad er reglen for at tage en strategi ud af drift? (Fx et bestemt tab,
     en bestemt periode med dårlige resultater.)
     Svar: Pharos

177. Hvad er reglen for at sætte en ny strategi i drift? Skal den først køre
     på papir (simuleret) i en periode?
     Svar: Pharos

178. Hvor lang en papirhandels-periode skal der være, og hvad skal den vise?
     Svar: Pharos

179. Skal strategier kunne slukkes midlertidigt, fx i perioder med meget uro
     i markedet?
     Svar: Nej

180. Hvordan håndteres det, når to strategier vil handle modsat hinanden i
     samme marked på samme tid?
     Svar: Ved ikke endnu

181. Hvordan vil du se et samlet overblik over hele porteføljen hver dag?
     Svar: Ved ikke endnu

182. Skal der være et loft for, hvor stor en del af den samlede risiko én
     strategi må stå for?
     Svar: ja

183. Skal porteføljen have strategier med forskellige tidshorisonter for at
     sprede risikoen?
     Svar: Pharos, ja

184. Hvordan testes hele porteføljen samlet bagud i tid, og ikke kun
     strategierne hver for sig?
     Svar: Ved ikke endnu

185. Hvor mange strategier skal ligge i reserve, klar til at erstatte dem,
     der tages ud?
     Svar: alle

186. Hvad gør du, hvis alle strategier taber på samme tid?
     Svar: tag tabet

187. Skal porteføljen tilpasse sig uro i markedet (fx mindre positioner, når
     det er uroligt)?
     Svar: Ved ikke endnu

## 12. Handel i virkeligheden (execution)

188. Hvilket program skal sende ordrerne til markedet: TradeStation,
     MultiCharts eller et eget program?
     Svar: begge med hver sine strategier

189. Hvilke ordretyper skal bruges (markedsordre, limitordre, stopordre)?
     Svar: markedordre

190. Hvor meget slippage (forskel på forventet og faktisk pris) og kurtage
     regnes der med i backtests i dag? Er tallene målt eller gættet?
     Svar: Ved ikke endnu

191. Hvordan sammenlignes de rigtige handler med backtesten bagefter, så
     forskelle opdages hurtigt?
     Svar: Ved ikke endnu

192. Hvor store positioner kan de valgte markeder tåle, før dine egne ordrer
     flytter prisen?
     Svar: ikke relevant

193. Hvad sker der, hvis en ordre kun bliver delvist udført?
     Svar: ikke noget.

194. Hvad sker der, hvis internetforbindelsen eller strømmen forsvinder,
     mens der er en åben position?
     Svar: manuel overvågning

195. Skal der ligge en stop-ordre hos brokeren hele tiden (så den virker,
     selvom din computer er slukket)?
     Svar: Ved ikke endnu

196. Hvordan sikres det, at systemet ikke sender den samme ordre to gange
     ved en fejl?
     Svar: Ved ikke endnu

197. Skal der være en "nødknap", der lukker alle positioner med ét tryk?
     Hvem må trykke på den?
     Svar: mig

198. Hvordan testes selve ordresystemet, før rigtige penge er på spil?
     Svar: Ved ikke endnu

199. Beregnes backtests på bar-lukning, mens den rigtige handel sker midt i
     en bar? Er forskellen undersøgt?
     Svar: der er vi ikke endnu

200. Hvordan måles slippage i den rigtige handel, og hvor gemmes målingerne?
     Svar: Ved ikke endnu

201. Hvad er reglen, hvis en ordre ikke bliver udført inden for en bestemt
     tid?
     Svar: Ved ikke endnu

202. Skal systemet undgå at handle i de første og sidste minutter af
     handelsdagen?
     Svar: det vi RSA vise

203. Hvad gør systemet, hvis brokerens system er nede eller afviser ordrer?
     Svar: Ved ikke endnu

204. Hvordan tjekkes det hver dag, at positionerne i systemet og hos
     brokeren er de samme?
     Svar: Ved ikke endnu

## 13. Risikostyring

205. Hvor meget må tabes på én handel, i procent af kontoen?
     Svar: 1-2 futures kontrakter pr handler, og stoploss

206. Hvor meget må tabes på én dag, før systemet stopper for resten af
     dagen?
     Svar: Ved ikke endnu

207. Hvor meget må tabes i en måned, før alt stoppes og gennemgås?
     Svar: Ved ikke endnu

208. Hvor stor en samlet position må der højst være åben i ét marked og i
     alle markeder tilsammen?
     Svar: det er tilpasset med antal strategier i hver markede

209. Hvordan beregnes positionsstørrelsen: fast antal kontrakter, efter
     volatilitet eller efter noget andet?
     Svar: fast antal kontrakter

210. Hvad gør systemet ved et pludseligt kæmpe prisfald (flash crash) eller
     et markedsstop?
     Svar: Ved ikke endnu

211. Hvordan beskyttes systemet mod en programfejl, der fx køber 100
     kontrakter i stedet for 1?
     Svar: Ved ikke endnu

212. Findes der en liste over de værste historiske markedsdage, som alle
     strategier skal testes igennem (stresstest)?
     Svar: der er vi ikke nået til endnu

213. Hvem overvåger risikoen: et program, dig, eller begge?
     Svar: begge

214. Hvordan håndteres margin-krav, der pludselig stiger fra brokeren?
     Svar: Ved ikke endnu

215. Må systemet øge positionerne efter en god periode, og i så fald efter
     hvilken regel?
     Svar: det afgør mig og Pharos

216. Hvad er dit personlige smertepunkt: hvor stort et tab kan du se på uden
     at gribe ind manuelt?
     Svar: 10 %

217. Hvornår må systemet starte igen, efter at det har stoppet på grund af
     et dagstab?
     Svar: dagen efter

218. Hvordan håndteres risikoen ved positioner over weekenden, hvis de
     nogensinde tillades?
     Svar: alle handler stopper Fradag

219. Må systemet selv ændre risikogrænserne, eller må kun du?
     Svar: kun mig

220. Hvordan skrives alle ændringer af risikogrænser ned, så man kan se,
     hvem der ændrede hvad og hvornår?
     Svar: Ved ikke endnu

221. Hvordan håndteres valutarisiko, hvis kontoen er i kroner og handlen
     sker i dollars?
     Svar: alt er i $

## 14. Drift, overvågning og fejl

222. Hvordan får du besked, hvis noget går galt (mail, sms, telefon-besked)?
     Svar: ikke afgjort

223. Hvilke fejl skal stoppe alt med det samme, og hvilke må bare
     registreres og samles op senere?
     Svar: Ved ikke endnu

224. Skal der være én samlet fejllog for hele projektet, eller én pr.
     delprojekt?
     Svar: pr. delprojekt

225. Hvordan tjekkes det hver dag, at alle dele kører (data kommer ind,
     programmer svarer, databasen er i orden)?
     Svar: manuelt og automatisk

226. Hvad gør du, hvis TradeStation opdateres og en automatisering holder op
     med at virke?
     Svar: Ved ikke endnu

227. Skal der være en fast rutine efter hver handelsdag (gennemgang,
     afstemning mod brokeren)?
     Svar: Ved ikke endnu

228. Hvordan genstartes hele systemet fra bunden efter et nedbrud, og står
     det skrevet ned?
     Svar: manuelt

229. Reglen "ved fejl: ret, ryd op og kør forfra" — gælder den også for
     EdgeFinder, EdgeCruncher og live-handel?
     Svar: den gælder for det hele

230. Skal der komme en daglig statusrapport, også når alt går godt?
     Svar: muligvis

231. Hvordan testes det, at alarmerne rent faktisk virker (fx en prøvealarm
     hver uge)?
     Svar: Ved ikke endnu

232. Hvordan undgås det, at Windows-opdateringer genstarter maskinen midt i
     en kørsel?
     Svar: Ved ikke endnu

233. Hvad sker der, hvis du ikke svarer på en alarm inden for en bestemt
     tid?
     Svar: Ved ikke endnu

234. Skal der føres en log over alle alvorlige fejl, med årsag og løsning?
     Svar: ja helst

## 15. TradeStation og MultiCharts

235. Hvorfor skal systemet også laves til MultiCharts? Hvad er gevinsten?
     Svar: multichats skal bruges til Prop-firmaer

236. Hvornår skal MultiCharts-delen starte: når hele kæden virker i
     TradeStation, eller tidligere?
     Svar: det kommer an på hvordan arbejdet går med TradeStation udgaven

237. Skal resultaterne fra TradeStation og MultiCharts sammenlignes, så de
     kontrollerer hinanden?
     Svar: Det ligger ved Pharos
           ved samme strategier skal de måles op mod hinanden

238. Hvad gør vi, hvis de to platforme giver forskellige resultater for
     samme test?
     Svar: gem info og analysere den

239. Er der risiko for at blive for afhængig af TradeStation (pris, licens,
     at de ændrer programmet)? Hvad er plan B?
     Svar: det tager vi når det bliver aktuelt

240. Skal der på sigt laves en egen backtest-motor i Python, så man ikke er
     afhængig af UI-automatisering af TradeStation?
     Svar: muligvis

241. Hvilke begrænsninger i EasyLanguage har vi mødt, som kunne tale for at
     flytte dele af beregningerne ud af TradeStation?
     Svar: Ved ikke endnu

242. Hvilken udgave af TradeStation bruges, og hvornår må den opdateres?
     Svar: Tradestation 10
           i weekender

243. Skal MultiCharts bruge sin egen dataleverandør eller de samme data som
     TradeStation?
     Svar: Tradestation

244. Findes der ting, vi bruger i TradeStation, som slet ikke findes i
     MultiCharts?
     Svar: Ved ikke endnu

245. Hvis TradeStation ændrer priser eller lukker, hvor hurtigt kan vi så
     flytte?
     Svar: da der også bruges Multicharts er vi sikkeret for en tid

## 16. Automatisering og "fuldautomatisk"

246. Hvad betyder "fuldautomatisk" for dig? Hvilke trin må ALDRIG ske uden
     din godkendelse?
     Svar: aktivering af strategier ligger hos mig og kun hos mig, resten skal være så automatisk som muligt

247. Hvilke trin i kæden kræver i dag, at du sidder ved computeren?
     Svar: det hele, det er kun i opbygnings fasen

248. Hvordan startes kæden: af dig, på et fast tidspunkt, eller af sig selv,
     når der kommer noget nyt?
     Svar: af mig

249. Skal der være én "dirigent", der styrer alle trin, fx EdgeFinder og
     EdgeCruncher i rækkefølge, eller kører de hver for sig?
     Svar: Ved ikke endnu

250. Hvordan ved det næste trin, at det forrige trin er færdigt og godkendt?
     Svar: når det er leveret til den, der bliver automatisk givet besked

251. Hvilken rolle skal Claude have, når systemet kører: udvikler,
     kontrollant, analytiker, eller slet ingen i den daglige drift?
     Svar: helst ingen, den skal hjælpe med videre udvikling

252. Hvordan kan du stoppe hele kæden med ét tryk, hvis noget ser forkert
     ud?
     Svar: i en app

253. Hvordan ser du, hvor langt kæden er nået lige nu (fx en statusside)?
     Svar: der er vi ikke endnu

254. Må systemet selv rette fejl, eller skal det altid stoppe og spørge?
     Svar: altid spørges

255. Skal systemet selv foreslå nye ting at teste ud fra tidligere
     resultater?
     Svar: det ligger ved Pharos

256. Hvordan undgås det, at automatikken skjuler fejl, som et menneske ville
     have set?
     Svar: Ved ikke endnu

## 17. Arbejdsmåde, dokumentation og Claude

257. Der er mange dokumenter, der delvist modsiger hinanden (NOTER,
     BYGGEVEJLEDNING, NOTAT, OPGAVEBESKRIVELSE, BESLUTNINGSLOG). Skal der
     laves én "sandhed" pr. delprojekt, som altid er opdateret?
     Svar: alt er under udvikling, noget er på ide basis, noget er tanker, noget er muligvis relevant senere

258. Skal der være en fast oversigt (et "kort") over hele projektet, som
     viser alle delprojekter, deres status og hvordan de hænger sammen?
     Svar: måske

259. Filnavnet `Task_RawSignal_Creature_EdgeFinder_opgave.md` ligger i
     roden. Skal procesbeskrivelserne have deres egen fast plads (fx én
     mappe pr. delprojekt)?
     Svar: der skal laves en mappe pr delprojekt

260. Kategorien "TradingApp" står i VIDENSLOG uden poster. Hvad er
     TradingApp, og er den stadig en del af projektet?
     Svar: det skal være en app hvor alt kan styres og nogle ting skal kunne findes frem gennem appen, men der er vi ikke endnu

261. Hvordan skal lokal Claude og cloud-Claude dele arbejdet mellem sig?
     Hvad skal hver især lave?
     Svar: Ved ikke endnu

262. Hvordan får cloud-Claude viden om databasens aktuelle indhold, når den
     ikke kan se den?
     Svar: Ved ikke endnu

263. Hvordan vil du helst have, at Claude stiller spørgsmål: ét ad gangen,
     samlet i en liste, eller i et skema som dette?
     Svar: Ved ikke endnu

264. Er der fejl eller misforståelser i samarbejdet med Claude indtil nu,
     som skal skrives ind i VIDENSLOG, så de ikke sker igen?
     Svar: Ved ikke endnu

265. Hvordan skal FriSnak-optagelser gemmes, så idéerne ikke går tabt (fx en
     fast mappe med dato)?
     Svar: en fast mappe

266. Hvordan skal en idé fra FriSnak blive til en opgave: hvem skriver den
     om til en plan, og hvem godkender den?
     Svar: det styre jeg

267. Hvor ofte skal VIDENSLOG gennemgås og ryddes op, så gammel viden ikke
     vildleder?
     Svar: Ved ikke endnu

268. Skal alle programmer have faste automatiske afprøvninger (tests), der
     køres før hver ændring?
     Svar: Ved ikke endnu

269. Hvordan sikres det, at den lokale session altid har den nyeste udgave
     fra GitHub?
     Svar: Ved ikke endnu

270. Hvilke opgaver giver du helst til den lokale Claude, og hvilke til
     cloud-Claude?
     Svar: Ved ikke endnu

271. Skal der være en fast skabelon for opgavebeskrivelser, så Claude ikke
     misforstår dem?
     Svar: det er nok en god ide vi må arbejde på

## 18. Sikkerhed, backup og hardware

272. Hvor ligger koden, databasen og dataene fysisk, og hvad sker der ved
     brand, tyveri eller en død harddisk?
     Svar: der er en fysisk server det hele ligger på.
           det er fordelt på tre harddisk.
           ved brand, mister jeg alt - god point

273. Er der en kopi af alt vigtigt uden for huset (fx i skyen)?
     Svar: nej

274. Hvordan beskyttes adgangskoder til broker, database og servere? Står
     nogen af dem i filer, der kommer i git?
     Svar: det meste er det kun mig der har

275. Hvem har adgang til fjernskrivebordet på serverne, og er det sikret med
     mere end en adgangskode?
     Svar: kun mig

276. Har serverne nødstrøm (UPS), og hvor længe kan de køre uden strøm?
     Svar: nej ikke endnu

277. Er GitHub-projektet privat, og skal det forblive det?
     Svar: det skal være privat, vis det ikke er skal det ændres.

278. Hvordan beskyttes serverne mod virus og hackere?
     Svar: almindelig beskyttelse.

279. Hvor lang tid tager det at bygge en server op igen fra bunden, og står
     det skrevet ned?
     Svar: Ved ikke endnu

280. Findes der en liste over alle programmer og licenser, og hvornår de
     udløber?
     Svar: nej

281. Hvad sker der, hvis din GitHub-konto eller din mail bliver hacket?
     Svar: Ved ikke endnu

## 19. Læring og forbedring over tid

282. Hvordan skal systemet lære af de strategier, der fejler i den rigtige
     handel?
     Svar: Ved ikke endnu

283. Hvor ofte skal hele kæden gennemgås for at se, om metoderne stadig er
     de bedste?
     Svar: Ved ikke endnu

284. Hvordan måles det, om selve udviklingssystemet bliver bedre over tid
     (fx flere holdbare strategier pr. måned)?
     Svar: TradingDB
           Pharos
           Analyse

285. Hvad skal der ske med strategier, der holder op med at virke: slettes,
     gemmes eller undersøges?
     Svar: gemmes
           opgave ligger ved Pharos

286. Skal der laves en fast gennemgang efter hver måned eller hvert kvartal?
     Svar: Begge dele

287. Hvordan sikres det, at nye idéer fra FriSnak bliver vurderet og ikke
     glemt?
     Svar: Ved ikke endnu

288. Skal Det Runde Bord være et fast trin i processen, fx før en strategi
     handler med rigtige penge?
     Svar: nej

## 20. Rapportering og nøgletal

289. Hvilke 5 tal vil du gerne se hver morgen?
     Svar: gårdages dagens %profit
           Total %profit
           gårdages  antal handler.
           gårdages antal strategier der er overgivet til Pharos.
           antal server aktive

290. Hvilke tal vil du se hver uge og hver måned?
     Svar: ugens %profit
           Total %profit
           ugens antal handler.
           ugens antal strategier der er overgivet til Pharos.
           det samme for hver måned og hver kvartal

291. Hvordan skal rapporterne se ud: tal, diagrammer, tekst eller en
     blanding?
     Svar: en blanding

292. Hvor skal rapporterne vises: på mail, i en app eller på telefonen?
     Svar: app og sms

293. Skal der være en rapport, der kan vises til en bank, en revisor eller
     en investor?
     Svar: bank og investor

294. Hvordan skal rapporterne sammenligne de rigtige resultater med det,
     backtesten lovede?
     Svar: Ved ikke endnu

## 21. Prioritering og næste skridt

295. Hvis du kun kunne vælge ét hul fra dette skema at lukke den næste
     måned, hvilket skulle det være?
     Svar: RSA og EdgeFinder

296. Hvilke spørgsmål i skemaet vil du have diskuteret ved Det Runde Bord?
     Svar: Ved ikke endnu

297. Hvilke emner mangler helt i dette skema?
     Svar: Ved ikke endnu

298. Hvad er den næste konkrete opgave, du vil give til Claude, når skemaet
     er besvaret?
     Svar: giv mig en liste over, "Ved ikke endnu" "Ikke relevant"

299. Hvilke tre ting i projektet er du mest usikker på lige nu?
     Svar: RSA analyse værdiger, Cruncher og Pharos

300. Er der noget, der allerede er bygget, som bør laves om, før der bygges
     videre ovenpå?
     Svar: Ved ikke endnu
