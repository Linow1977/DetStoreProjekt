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
4. Prisdata
5. TradingServer (database, bibliotek, lager)
6. TML-Server (backtest, analyse, selektering)
7. EdgeFinder (event-studie)
8. EdgeCruncher
9. Statistik og beskyttelse mod selvbedrag
10. Fra enkelt-strategi til portefølje
11. Handel i virkeligheden (execution)
12. Risikostyring
13. Drift, overvågning og fejl
14. TradeStation og MultiCharts
15. Automatisering og "fuldautomatisk"
16. Arbejdsmåde, dokumentation og Claude
17. Sikkerhed, backup og hardware
18. Prioritering og næste skridt

---

## 1. Mål, vision og succes

1. Hvad betyder "hedge-fond" helt konkret for dig: kun egne penge, eller på
   et tidspunkt også andres penge?
   Svar:

2. Hvornår er projektet en succes? Beskriv det i tal (fx afkast pr. år,
   største tilladte tab, antal strategier i drift).
   Svar:

3. Hvilket afkast pr. år sigter du efter, og hvor stort et fald fra top til
   bund (drawdown) kan du leve med, før du stopper?
   Svar:

4. Når du siger "på niveau med verdens bedste" — hvilke fonde eller hvilke
   tal sammenligner du med?
   Svar:

5. Hvad er den vigtigste ting, projektet skal kunne om 6 måneder? Om 1 år?
   Om 3 år?
   Svar:

6. Hvornår skal den første strategi handle med rigtige penge? Er der en
   dato eller en betingelse?
   Svar:

7. Hvad er "daytrading" for dig: skal alle handler være lukket ved dagens
   slutning, eller må en position stå natten over?
   Svar:

8. Hvad er den største risiko for, at projektet ikke lykkes, som du ser det
   i dag?
   Svar:

9. Hvad vil du aldrig gå på kompromis med (fx kvalitet, sikkerhed, egen
   kontrol)?
   Svar:

10. Hvad vil du gerne have, at systemet kan, som du ikke tror, andre private
    tradere har?
    Svar:

11. Hvornår vil du stoppe projektet eller ændre retning? Findes der en
    "exit-regel" for selve projektet?
    Svar:

12. Skal systemet kun finde strategier, eller skal det også selv beslutte,
    hvilke der handles, og selv sætte dem i drift?
    Svar:

## 2. Rammer: tid, penge, folk og regler

13. Hvor mange timer om ugen bruger du på projektet i dag, og hvor mange
    kan du bruge fremover?
    Svar:

14. Hvor meget kapital er afsat til handel, når systemet er klar?
    Svar:

15. Hvor meget må projektet koste pr. måned i software, data, servere og
    abonnementer?
    Svar:

16. Er der andre personer involveret nu eller senere (partner, programmør,
    revisor, advokat)?
    Svar:

17. Hvis du er væk i en måned, hvem holder så øje med systemet og de åbne
    handler?
    Svar:

18. Skal handlen ske som privatperson eller gennem et selskab? Er det
    afklaret med en revisor, hvordan gevinster og tab beskattes?
    Svar:

19. Har du undersøgt, hvilke regler (fx Finanstilsynet) der gælder, hvis du
    senere vil forvalte andres penge?
    Svar:

20. Hvilken broker (mægler) skal handlerne gå gennem? Er det besluttet?
    Svar:

21. Er der krav fra brokeren om minimumskapital, margin (sikkerhedsstillelse)
    eller særlige kontotyper for futures?
    Svar:

22. Hvad er din erfaring med at handle futures manuelt? Hvilke markeder og
    hvor længe?
    Svar:

23. Hvilke af dine tidligere strategier eller erfaringer skal systemet bygge
    videre på, og hvilke skal glemmes?
    Svar:

24. Hvor meget af beslutningerne vil du selv tage, og hvor meget må Claude
    beslutte uden at spørge?
    Svar:

## 3. Markeder og instrumenter

25. Præcis hvilke futures-markeder skal systemet handle (fx ES, NQ, CL, GC)?
    Svar:

26. Skal alle strategier virke på alle markeder, eller må en strategi kun
    virke på ét marked?
    Svar:

27. Skal der kunne handles micro-kontrakter (små kontrakter), så positionen
    kan gøres mindre?
    Svar:

28. Hvilke tidspunkter på døgnet må systemet handle: kun den normale
    børstid, eller også natten (elektronisk handel)?
    Svar:

29. Hvordan håndteres dage med vigtige nyheder (fx renteudmelding,
    jobtal)? Skal systemet holde pause?
    Svar:

30. Hvordan håndteres helligdage, halve handelsdage og lukkede børser?
    Svar:

31. Hvordan skifter systemet fra én kontrakt til den næste, når en
    futures-kontrakt udløber (rollover)?
    Svar:

32. Hvilke tidsrammer skal der arbejdes med? I dag nævnes fire workspaces
    (5,10,60 / 10,20,60 / 5,30,120 / 5,10,120). Er det den endelige liste,
    og hvorfor netop dem?
    Svar:

33. Hvad betyder de tre tal i hvert workspace helt præcist (Data1, Data2,
    Data3), og hvad bruges hver af dem til?
    Svar:

34. Skal systemet kunne bruge data fra ét marked til at handle et andet
    (fx renter til at handle aktieindeks)?
    Svar:

35. Er der markeder, du bevidst vil holde dig fra, og hvorfor?
    Svar:

36. Hvor mange markeder skal handles samtidig, når systemet er i fuld drift?
    Svar:

## 4. Prisdata

37. Hvor kommer prisdataene fra i dag? Kun TradeStation, eller også andre
    kilder?
    Svar:

38. Hvor mange års historik findes der for hvert marked, og er det nok?
    Svar:

39. Hvordan kontrolleres dataene for fejl (huller, dubletter, forkerte
    priser, spring)?
    Svar:

40. Bruges "continuous contracts" (sammensatte kontrakter over flere udløb)?
    Hvis ja: hvordan er de sat sammen (justeret eller ikke justeret)?
    Svar:

41. Hvilken tidszone gemmes tiderne i, og hvordan håndteres sommer- og
    vintertid?
    Svar:

42. Er det sikkert, at TradeStation og MultiCharts giver præcis de samme
    bars (prisstænger) for samme marked og tidsramme?
    Svar:

43. Skal prisdata også gemmes i TradingDB, eller kun ligge i TradeStation?
    Svar:

44. Hvad sker der, hvis dataleverandøren retter historiske data bagefter?
    Opdager systemet det?
    Svar:

45. Skal der bruges tick-data eller kun minut-bars? Hvornår er minut-bars
    ikke præcise nok?
    Svar:

46. Hvordan sikres det, at en backtest kun bruger data, der rent faktisk
    var kendt på det tidspunkt (ingen "look-ahead" = snyd med fremtidige
    data)?
    Svar:

47. Hvor mange data skal gemmes til side, som aldrig bruges under udvikling
    (out-of-sample), men kun til den endelige kontrol?
    Svar:

48. Hvem "ejer" beslutningen om, hvilke dataperioder der må bruges til hvad
    — og står det skrevet ned?
    Svar:

49. Skal der bruges andre data end pris og volumen (fx volatilitetsindeks,
    kalender, sæson)? Eller holdes det strengt til prisdata?
    Svar:

## 5. TradingServer (database, bibliotek, lager)

50. Hvad er den fulde liste over tabeller i TradingDB i dag, og hvad bruges
    hver til?
    Svar:

51. Findes der en tegning eller beskrivelse af, hvordan tabellerne hænger
    sammen? Hvis ikke — skal der laves en?
    Svar:

52. Hvordan tages der backup af TradingDB? Hvor ofte, hvor ligger den, og er
    en gendannelse nogensinde blevet afprøvet?
    Svar:

53. Hvad er forskellen på "Database", "Bibliotek" og "Lager" i
    TradingServer? Hvad hører til hvilken?
    Svar:

54. Hvor skal resultatfilerne fra backtests ligge, og hvor længe skal de gemmes?
    Svar:

55. Hvor meget diskplads forventes der at blive brugt, når alle backtests
    for alle workspaces og markeder er kørt?
    Svar:

56. Hvordan navngives mapper og filer, så man om 2 år stadig kan finde ud
    af, hvad der er hvad?
    Svar:

57. Skal hver kørsel have et unikt kørselsnummer, så man altid kan spore et
    resultat tilbage til præcis de data og den kode, der lavede det?
    Svar:

58. Hvad sker der i databasen, når en regel eller et program ændres? Skal
    gamle resultater slettes, markeres som forældede eller beholdes?
    Svar:

59. Hvem må skrive i databasen: kun programmerne, eller også dig manuelt?
    Svar:

60. Hvordan undgås det, at to programmer skriver i samme tabel samtidig og
    ødelægger data for hinanden?
    Svar:

61. Skal den lokale Claude-session og cloud-sessionen på et tidspunkt kunne
    se databasen på samme måde (fx via et udtræk, der lægges i git)?
    Svar:

## 6. TML-Server (backtest, analyse, selektering)

62. Hvad er TML-Serveren fysisk: en separat computer, en virtuel maskine
    eller samme maskine som TradingServer?
    Svar:

63. Hvilke programmer kører på TML-Serveren (TradeStation, MultiCharts,
    Python, andet)?
    Svar:

64. Hvordan sendes arbejde mellem TradingServer og TML-Server (filer,
    database, netværksmappe)?
    Svar:

65. Hvor mange backtests kan køres samtidig, og hvad er flaskehalsen:
    computerkraft, TradeStation-licenser eller tid?
    Svar:

66. Hvor lang tid tager én backtest i dag? Hvor lang tid
    vil alle tage samlet?
    Svar:

67. Hvad betyder "Selektering" konkret: hvem eller hvad vælger, og efter
    hvilke regler?
    Svar:

68. Hvilke analyser skal ligge på TML-Serveren, og hvilke skal ligge i
    Python et andet sted?
    Svar:

69. Hvad sker der, hvis TML-Serveren går ned midt i en lang kørsel? Kan
    den fortsætte, hvor den slap?
    Svar:

70. Skal TML-Serveren kunne styres, mens du ikke er ved computeren (fx
    over fjernskrivebord eller telefon)?
    Svar:

71. Skal der være adskillelse mellem maskinen, der udvikler strategier, og
    maskinen, der handler med rigtige penge?
    Svar:

72. Hvordan holdes programversioner ens på de to servere?
    Svar:

## 7. EdgeFinder (event-studie)

73. Forklar med dine egne ord, hvad EdgeFinder skal finde. Hvad er en
    "edge" for dig?
    Svar:

74. Hvad er et event-studie i dette projekt: hvad måles der efter hvert
    signal (fx prisbevægelse efter 5, 10, 30 bars)?
    Svar:

75. Hvilke tidshorisonter efter et signal skal måles?
    Svar:

76. Hvad sammenlignes signalets resultat med? Med tilfældige tidspunkter,
    med markedet generelt, eller med noget andet?
    Svar:

77. Hvornår er et resultat "Passed"? Hvilke tal skal være opfyldt?
    Svar:

78. Hvornår er det "Failed"? Og skal "næsten bestået" være en tredje
    kategori?
    Svar:

79. Hvor mange hændelser skal der mindst være i en test, før resultatet
    kan bruges?
    Svar:

80. Skal EdgeFinder se på både køb- og salgsretning for hvert signal?
    Svar:

81. Hvordan håndteres signaler, der ligger tæt efter hinanden og derfor
    måler den samme prisbevægelse flere gange?
    Svar:

82. Skal resultatet deles op i perioder (fx år for år) for at se, om edgen
    er stabil over tid?
    Svar:

83. Skal resultatet deles op efter markedstype (stigende, faldende,
    sidelæns, rolig, urolig)?
    Svar:

84. Hvilke workspace-indstillinger skal EdgeFinder sætte i TradeStation, og
    hvor er de beskrevet?
    Svar:

85. Hvad skal ske, hvis backtest-data i mappen er ufuldstændige eller
    forkerte ("stop process og meld fejl")? Hvem får beskeden, og hvordan?
    Svar:

86. Hvilke resultater skal "journalføres", og i hvilken tabel?
    Svar:

87. Skal EdgeFinder skrives i Python? Findes der allerede noget
     analysekode, der skal genbruges?
     Svar:

88. Hvem bestemmer rækkefølgen, tingene testes i i EdgeFinder, og er der
     en prioritering?
     Svar:

## 8. EdgeCruncher

89. Hvad skal EdgeCruncher gøre? Beskriv det, som du forestiller dig det,
     selvom det ikke er færdigt.
     Svar:

90. Hvad får EdgeCruncher ind (kun "Passed" fra EdgeFinder?), og hvad
     sender den videre?
     Svar:

91. Skal EdgeCruncher kombinere flere signaler til én strategi? Hvor mange
     må der højst kombineres?
     Svar:

92. Hvor kommer indgang, udgang, stop-loss og gevinstmål ind i billedet?
     Er det EdgeCruncher eller et senere trin?
     Svar:

93. Hvad er det næste trin efter EdgeCruncher? Findes der et navn og en
     idé for det endnu?
     Svar:

94. Hvordan undgår EdgeCruncher at finde tilfældige kombinationer, der kun
     ser gode ud, fordi der er prøvet så mange?
     Svar:

95. Hvor mange kombinationer forventer du, at EdgeCruncher skal prøve?
     Tusinder, millioner?
     Svar:

96. Hvor lang tid må EdgeCruncher bruge pr. kørsel?
     Svar:

97. Hvordan vil du selv kunne se og forstå, hvorfor EdgeCruncher har valgt
     det, den har valgt?
     Svar:

98. "Data1, når den senere bliver mindre end Data2 (entry-finpudsning)" —
     hvor og hvornår hører det til?
     Svar:

## 9. Statistik og beskyttelse mod selvbedrag

99. Hvordan tages der højde for, at der testes tusindvis af signaler, så
     nogle vil se gode ud af ren tilfældighed (multiple testing)?
     Svar:

100. Tælles det, hvor mange forsøg der i alt er lavet, før en strategi blev
     fundet? Det er nødvendigt for at vurdere, hvor meget held der er med.
     Svar:

101. Hvilken metode skal bruges til out-of-sample-test (walk-forward,
     fast opdeling, andet)?
     Svar:

102. Må out-of-sample-data nogensinde bruges igen, efter de er set første
     gang? Hvad er reglen?
     Svar:

103. Hvordan testes, om en strategi er robust, når parametrene ændres en
     smule (fx 20 i stedet for 21)?
     Svar:

104. Skal strategier testes på andre markeder end dem, de blev fundet på,
     som ekstra kontrol?
     Svar:

105. Skal der laves "Monte Carlo"-test (tilfældig blanding af handlerne for
     at se, hvor slemt det kunne være gået)?
     Svar:

106. Hvilke nøgletal skal hver strategi vurderes på (fx Sharpe, profit
     factor, gennemsnitlig handel, max drawdown)? Og hvilket er det
     vigtigste?
     Svar:

107. Hvad er den mindste gennemsnitlige gevinst pr. handel, der kan
     overleve kurtage og slippage?
     Svar:

108. Skal der være et fast sæt af "kontrolsignaler" (tilfældige signaler),
     som alle resultater sammenlignes med?
     Svar:

109. Hvordan opdages det, hvis en resultatperiode domineres af én
     enkelt ekstrem dag eller hændelse?
     Svar:

110. Hvem eller hvad skal "angribe" en strategi, før den godkendes — Det
     Runde Bord, et fast testprogram eller begge dele?
     Svar:

111. Skal Det Runde Bord have et fast verdikt og en score (fx Go / No-go /
     Juster og 0–10)? Det står som ikke besluttet.
     Svar:

112. Hvordan dokumenteres alle forkastede idéer, så de ikke testes igen ved
     en fejl?
     Svar:

## 10. Fra enkelt-strategi til portefølje

113. Hvor mange strategier skal køre samtidig, når systemet er i fuld drift?
     Svar:

114. Hvordan måles det, om to strategier i virkeligheden gør det samme
     (for høj sammenhæng/korrelation)?
     Svar:

115. Hvordan fordeles kapitalen mellem strategierne: lige meget, efter
     risiko, eller efter noget andet?
     Svar:

116. Hvor ofte skal porteføljen gennemgås og ændres?
     Svar:

117. Hvad er reglen for at tage en strategi ud af drift? (Fx et bestemt tab,
     en bestemt periode med dårlige resultater.)
     Svar:

118. Hvad er reglen for at sætte en ny strategi i drift? Skal den først køre
     på papir (simuleret) i en periode?
     Svar:

119. Hvor lang en papirhandels-periode skal der være, og hvad skal den vise?
     Svar:

120. Skal strategier kunne slukkes midlertidigt, fx i perioder med meget uro
     i markedet?
     Svar:

121. Hvordan håndteres det, når to strategier vil handle modsat hinanden i
     samme marked på samme tid?
     Svar:

122. Hvordan vil du se et samlet overblik over hele porteføljen hver dag?
     Svar:

## 11. Handel i virkeligheden (execution)

123. Hvilket program skal sende ordrerne til markedet: TradeStation,
     MultiCharts eller et eget program?
     Svar:

124. Hvilke ordretyper skal bruges (markedsordre, limitordre, stopordre)?
     Svar:

125. Hvor meget slippage (forskel på forventet og faktisk pris) og kurtage
     regnes der med i backtests i dag? Er tallene målt eller gættet?
     Svar:

126. Hvordan sammenlignes de rigtige handler med backtesten bagefter, så
     forskelle opdages hurtigt?
     Svar:

127. Hvor store positioner kan de valgte markeder tåle, før dine egne
     ordrer flytter prisen?
     Svar:

128. Hvad sker der, hvis en ordre kun bliver delvist udført?
     Svar:

129. Hvad sker der, hvis internetforbindelsen eller strømmen forsvinder,
     mens der er en åben position?
     Svar:

130. Skal der ligge en stop-ordre hos brokeren hele tiden (så den virker,
     selvom din computer er slukket)?
     Svar:

131. Hvordan sikres det, at systemet ikke sender den samme ordre to gange
     ved en fejl?
     Svar:

132. Skal der være en "nødknap", der lukker alle positioner med ét tryk?
     Hvem må trykke på den?
     Svar:

133. Hvordan testes selve ordresystemet, før rigtige penge er på spil?
     Svar:

134. Beregnes backtests på bar-lukning, mens den rigtige handel sker midt i
     en bar? Er forskellen undersøgt?
     Svar:

## 12. Risikostyring

135. Hvor meget må tabes på én handel, i procent af kontoen?
     Svar:

136. Hvor meget må tabes på én dag, før systemet stopper for resten af
     dagen?
     Svar:

137. Hvor meget må tabes i en måned, før alt stoppes og gennemgås?
     Svar:

138. Hvor stor en samlet position må der højst være åben i ét marked og i
     alle markeder tilsammen?
     Svar:

139. Hvordan beregnes positionsstørrelsen: fast antal kontrakter, efter
     volatilitet eller efter noget andet?
     Svar:

140. Hvad gør systemet ved et pludseligt kæmpe prisfald (flash crash) eller
     et markedsstop?
     Svar:

141. Hvordan beskyttes systemet mod en programfejl, der fx køber 100
     kontrakter i stedet for 1?
     Svar:

142. Findes der en liste over de værste historiske markedsdage, som alle
     strategier skal testes igennem (stresstest)?
     Svar:

143. Hvem overvåger risikoen: et program, dig, eller begge?
     Svar:

144. Hvordan håndteres margin-krav, der pludselig stiger fra brokeren?
     Svar:

145. Må systemet øge positionerne efter en god periode, og i så fald efter
     hvilken regel?
     Svar:

146. Hvad er dit personlige smertepunkt: hvor stort et tab kan du se på
     uden at gribe ind manuelt?
     Svar:

## 13. Drift, overvågning og fejl

147. Hvordan får du besked, hvis noget går galt (mail, sms, telefon-besked)?
     Svar:

148. Hvilke fejl skal stoppe alt med det samme, og hvilke må bare
     registreres og samles op senere?
     Svar:

149. Skal der være én samlet fejllog for hele projektet, eller én pr.
     delprojekt?
     Svar:

150. Hvordan tjekkes det hver dag, at alle dele kører (data kommer ind,
     programmer svarer, databasen er i orden)?
     Svar:

151. Hvad gør du, hvis TradeStation opdateres og en automatisering holder op
     med at virke?
     Svar:

152. Skal der være en fast rutine efter hver handelsdag (gennemgang,
     afstemning mod brokeren)?
     Svar:

153. Hvordan genstartes hele systemet fra bunden efter et nedbrud, og står
     det skrevet ned?
     Svar:

154. Reglen "ved fejl: ret, ryd op og kør forfra" — gælder den også for
     EdgeFinder, EdgeCruncher og live-handel?
     Svar:

## 14. TradeStation og MultiCharts

155. Hvorfor skal systemet også laves til MultiCharts? Hvad er gevinsten?
     Svar:

156. Hvornår skal MultiCharts-delen starte: når hele kæden virker i
     TradeStation, eller tidligere?
     Svar:

157. Skal resultaterne fra TradeStation og MultiCharts sammenlignes, så de
     kontrollerer hinanden?
     Svar:

158. Hvad gør vi, hvis de to platforme giver forskellige resultater for samme
     test?
     Svar:

159. Er der risiko for at blive for afhængig af TradeStation (pris, licens,
     at de ændrer programmet)? Hvad er plan B?
     Svar:

160. Skal der på sigt laves en egen backtest-motor i Python, så man ikke er
     afhængig af UI-automatisering af TradeStation?
     Svar:

161. Hvilke begrænsninger i EasyLanguage har vi mødt, som kunne tale for at
     flytte dele af beregningerne ud af TradeStation?
     Svar:

## 15. Automatisering og "fuldautomatisk"

162. Hvad betyder "fuldautomatisk" for dig? Hvilke trin må ALDRIG ske uden
     din godkendelse?
     Svar:

163. Hvilke trin i kæden kræver i dag, at du sidder ved computeren?
     Svar:

164. Hvordan startes kæden: af dig, på et fast tidspunkt, eller af sig selv,
     når der kommer noget nyt?
     Svar:

165. Skal der være én "dirigent", der styrer alle trin, fx EdgeFinder
     og EdgeCruncher i rækkefølge, eller kører de hver for sig?
     Svar:

166. Hvordan ved det næste trin, at det forrige trin er færdigt og godkendt?
     Svar:

167. Hvilken rolle skal Claude have, når systemet kører: udvikler, kontrollant,
     analytiker, eller slet ingen i den daglige drift?
     Svar:

## 16. Arbejdsmåde, dokumentation og Claude

168. Der er mange dokumenter, der delvist modsiger hinanden (NOTER,
     BYGGEVEJLEDNING, NOTAT, OPGAVEBESKRIVELSE, BESLUTNINGSLOG). Skal der laves
     én "sandhed" pr. delprojekt, som altid er opdateret?
     Svar:

169. Skal der være en fast oversigt (et "kort") over hele projektet, som
     viser alle delprojekter, deres status og hvordan de hænger sammen?
     Svar:

170. Filnavnet `Task_RawSignal_Creature_EdgeFinder_opgave.md` ligger i roden.
     Skal procesbeskrivelserne have deres egen fast plads (fx én mappe pr.
     delprojekt)?
     Svar:

171. Kategorien "TradingApp" står i VIDENSLOG uden poster. Hvad er TradingApp,
     og er den stadig en del af projektet?
     Svar:

172. Hvordan skal lokal Claude og cloud-Claude dele arbejdet mellem sig? Hvad
     skal hver især lave?
     Svar:

173. Hvordan får cloud-Claude viden om databasens aktuelle indhold, når den
     ikke kan se den?
     Svar:

174. Hvordan vil du helst have, at Claude stiller spørgsmål: ét ad gangen,
     samlet i en liste, eller i et skema som dette?
     Svar:

175. Er der fejl eller misforståelser i samarbejdet med Claude indtil nu,
     som skal skrives ind i VIDENSLOG, så de ikke sker igen?
     Svar:

176. Hvordan skal FriSnak-optagelser gemmes, så idéerne ikke går tabt
     (fx en fast mappe med dato)?
     Svar:

177. Hvordan skal en idé fra FriSnak blive til en opgave: hvem skriver den
     om til en plan, og hvem godkender den?
     Svar:

## 17. Sikkerhed, backup og hardware

178. Hvor ligger koden, databasen og dataene fysisk, og hvad sker der ved
     brand, tyveri eller en død harddisk?
     Svar:

179. Er der en kopi af alt vigtigt uden for huset (fx i skyen)?
     Svar:

180. Hvordan beskyttes adgangskoder til broker, database og servere? Står
     nogen af dem i filer, der kommer i git?
     Svar:

181. Hvem har adgang til fjernskrivebordet på serverne, og er det sikret med
     mere end en adgangskode?
     Svar:

182. Har serverne nødstrøm (UPS), og hvor længe kan de køre uden strøm?
     Svar:

183. Er GitHub-projektet privat, og skal det forblive det?
     Svar:

## 18. Prioritering og næste skridt

184. Hvis du kun kunne vælge ét hul fra dette skema at lukke den næste måned,
     hvilket skulle det være?
     Svar:

185. Hvilke spørgsmål i skemaet vil du have diskuteret ved Det Runde Bord?
     Svar:

186. Hvilke emner mangler helt i dette skema?
     Svar:

187. Hvad er den næste konkrete opgave, du vil give til Claude, når skemaet
     er besvaret?
     Svar:
