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

6. Hvornår skal den første strategi handle med rigtige penge? Er der en dato
   eller en betingelse?
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

13. Hvordan skal man kunne se, om projektet bevæger sig i den rigtige
    retning måned for måned (delmål)?
    Svar:

14. Er målet at slå et bestemt indeks, eller at tjene penge uanset om
    markedet går op eller ned?
    Svar:

15. Hvad er vigtigst for dig: højt afkast, jævnt afkast eller lav risiko?
    Sæt dem i rækkefølge.
    Svar:

16. Hvad skal der til, for at du stoler nok på systemet til at lade det
    handle, uden at du kigger med?
    Svar:

17. Er der en tidsfrist, hvor projektet skal kunne betale for sig selv?
    Svar:

## 2. Rammer: tid, penge, folk og regler

18. Hvor mange timer om ugen bruger du på projektet i dag, og hvor mange kan
    du bruge fremover?
    Svar:

19. Hvor meget kapital er afsat til handel, når systemet er klar?
    Svar:

20. Hvor meget må projektet koste pr. måned i software, data, servere og
    abonnementer?
    Svar:

21. Er der andre personer involveret nu eller senere (partner, programmør,
    revisor, advokat)?
    Svar:

22. Hvis du er væk i en måned, hvem holder så øje med systemet og de åbne
    handler?
    Svar:

23. Skal handlen ske som privatperson eller gennem et selskab? Er det
    afklaret med en revisor, hvordan gevinster og tab beskattes?
    Svar:

24. Har du undersøgt, hvilke regler (fx Finanstilsynet) der gælder, hvis du
    senere vil forvalte andres penge?
    Svar:

25. Hvilken broker (mægler) skal handlerne gå gennem? Er det besluttet?
    Svar:

26. Er der krav fra brokeren om minimumskapital, margin
    (sikkerhedsstillelse) eller særlige kontotyper for futures?
    Svar:

27. Hvad er din erfaring med at handle futures manuelt? Hvilke markeder og
    hvor længe?
    Svar:

28. Hvilke af dine tidligere strategier eller erfaringer skal systemet bygge
    videre på, og hvilke skal glemmes?
    Svar:

29. Hvor meget af beslutningerne vil du selv tage, og hvor meget må Claude
    beslutte uden at spørge?
    Svar:

30. Hvor meget af din egen formue er du parat til at sætte på spil i alt?
    Svar:

31. Hvad sker der med projektet og kontoen, hvis du bliver syg i længere
    tid?
    Svar:

32. Hvilke dele af arbejdet vil du gerne have hjælp fra et menneske til (fx
    revisor eller programmør)?
    Svar:

33. Har brokeren regler for automatisk handel (fx krav om at godkende et
    handelsprogram)?
    Svar:

## 3. Markeder og instrumenter

34. Præcis hvilke futures-markeder skal systemet handle (fx ES, NQ, CL, GC)?
    Svar:

35. Skal alle strategier virke på alle markeder, eller må en strategi kun
    virke på ét marked?
    Svar:

36. Skal der kunne handles micro-kontrakter (små kontrakter), så positionen
    kan gøres mindre?
    Svar:

37. Hvilke tidspunkter på døgnet må systemet handle: kun den normale
    børstid, eller også natten (elektronisk handel)?
    Svar:

38. Hvordan håndteres dage med vigtige nyheder (fx renteudmelding, jobtal)?
    Skal systemet holde pause?
    Svar:

39. Hvordan håndteres helligdage, halve handelsdage og lukkede børser?
    Svar:

40. Hvordan skifter systemet fra én kontrakt til den næste, når en
    futures-kontrakt udløber (rollover)?
    Svar:

41. Hvilke tidsrammer skal der arbejdes med? I dag nævnes fire workspaces
    (5,10,60 / 10,20,60 / 5,30,120 / 5,10,120). Er det den endelige liste,
    og hvorfor netop dem?
    Svar:

42. Hvad betyder de tre tal i hvert workspace helt præcist (Data1, Data2,
    Data3), og hvad bruges hver af dem til?
    Svar:

43. Skal systemet kunne bruge data fra ét marked til at handle et andet (fx
    renter til at handle aktieindeks)?
    Svar:

44. Er der markeder, du bevidst vil holde dig fra, og hvorfor?
    Svar:

45. Hvor mange markeder skal handles samtidig, når systemet er i fuld drift?
    Svar:

46. Hvor stor en daglig omsætning (likviditet = hvor let man kan købe og
    sælge) skal et marked mindst have for at være med?
    Svar:

47. Hvordan kommer nye markeder på listen senere, og efter hvilke regler?
    Svar:

48. Skal strategierne handle i begge retninger (købe og sælge først), eller
    kun den ene vej?
    Svar:

49. Hvordan håndteres det, at markederne opfører sig forskelligt, når Asien,
    Europa og USA har åbent?
    Svar:

50. Skal der tages højde for mønstre, der følger årstiden (fx energimarkeder
    om vinteren)?
    Svar:

## 4. Markedsforståelse og strategityper

51. Hvilken slags markedsadfærd tror du mest på: trend (prisen fortsætter),
    tilbagevenden (prisen vender tilbage), udbrud eller noget andet?
    Svar:

52. Hvorfor skulle der overhovedet være en edge i teknisk analyse på
    futures? Hvem er det, der taber de penge, systemet skal vinde?
    Svar:

53. Hvilke markedsforhold tror du, systemet vil have sværest ved?
    Svar:

54. Må systemet bruge volumen og open interest (antal åbne kontrakter),
    eller kun prisen?
    Svar:

55. Hvor hurtigt tror du, en edge forsvinder, når den først er fundet?
    Svar:

56. Skal systemet lede efter edges, der virker på tværs af markeder, eller
    edges, der kun gælder ét marked?
    Svar:

57. Hvad har du lært af andre systematiske tradere eller bøger, som skal
    bygges ind i systemet?
    Svar:

58. Hvilke idéer har du testet før, som ikke virkede, og hvorfor tror du, de
    ikke virkede?
    Svar:

## 5. Prisdata

59. Hvor kommer prisdataene fra i dag? Kun TradeStation, eller også andre
    kilder?
    Svar:

60. Hvor mange års historik findes der for hvert marked, og er det nok?
    Svar:

61. Hvordan kontrolleres dataene for fejl (huller, dubletter, forkerte
    priser, spring)?
    Svar:

62. Bruges "continuous contracts" (sammensatte kontrakter over flere udløb)?
    Hvis ja: hvordan er de sat sammen (justeret eller ikke justeret)?
    Svar:

63. Hvilken tidszone gemmes tiderne i, og hvordan håndteres sommer- og
    vintertid?
    Svar:

64. Er det sikkert, at TradeStation og MultiCharts giver præcis de samme
    bars (prisstænger) for samme marked og tidsramme?
    Svar:

65. Skal prisdata også gemmes i TradingDB, eller kun ligge i TradeStation?
    Svar:

66. Hvad sker der, hvis dataleverandøren retter historiske data bagefter?
    Opdager systemet det?
    Svar:

67. Skal der bruges tick-data eller kun minut-bars? Hvornår er minut-bars
    ikke præcise nok?
    Svar:

68. Hvordan sikres det, at en backtest kun bruger data, der rent faktisk var
    kendt på det tidspunkt (ingen "look-ahead" = snyd med fremtidige data)?
    Svar:

69. Hvor mange data skal gemmes til side, som aldrig bruges under udvikling
    (out-of-sample), men kun til den endelige kontrol?
    Svar:

70. Hvem "ejer" beslutningen om, hvilke dataperioder der må bruges til hvad
    — og står det skrevet ned?
    Svar:

71. Skal der bruges andre data end pris og volumen (fx volatilitetsindeks,
    kalender, sæson)? Eller holdes det strengt til prisdata?
    Svar:

72. Hvordan gemmes de rå data, så de aldrig kan ændres ved en fejl (fx en
    skrivebeskyttet kopi)?
    Svar:

73. Hvilken tidsramme er den mindste, der skal bruges, og hvorfor?
    Svar:

74. Hvordan håndteres bars med meget lidt handel (fx om natten)?
    Svar:

75. Skal der hver dag være en kort data-rapport, der viser, om de nye data
    er kommet rigtigt ind?
    Svar:

76. Hvordan sikres det, at alle backtests bruger præcis samme udgave af
    dataene, så de kan sammenlignes?
    Svar:

77. Hvad koster bedre data fra en separat dataleverandør, og er det pengene
    værd?
    Svar:

## 6. TradingServer (database, bibliotek, lager)

78. Hvad er den fulde liste over tabeller i TradingDB i dag, og hvad bruges
    hver til?
    Svar:

79. Findes der en tegning eller beskrivelse af, hvordan tabellerne hænger
    sammen? Hvis ikke — skal der laves en?
    Svar:

80. Hvordan tages der backup af TradingDB? Hvor ofte, hvor ligger den, og er
    en gendannelse nogensinde blevet afprøvet?
    Svar:

81. Hvad er forskellen på "Database", "Bibliotek" og "Lager" i
    TradingServer? Hvad hører til hvilken?
    Svar:

82. Hvor skal resultatfilerne fra backtests ligge, og hvor længe skal de
    gemmes?
    Svar:

83. Hvor meget diskplads forventes der at blive brugt, når alle backtests
    for alle workspaces og markeder er kørt?
    Svar:

84. Hvordan navngives mapper og filer, så man om 2 år stadig kan finde ud
    af, hvad der er hvad?
    Svar:

85. Skal hver kørsel have et unikt kørselsnummer, så man altid kan spore et
    resultat tilbage til præcis de data og den kode, der lavede det?
    Svar:

86. Hvad sker der i databasen, når en regel eller et program ændres? Skal
    gamle resultater slettes, markeres som forældede eller beholdes?
    Svar:

87. Hvem må skrive i databasen: kun programmerne, eller også dig manuelt?
    Svar:

88. Hvordan undgås det, at to programmer skriver i samme tabel samtidig og
    ødelægger data for hinanden?
    Svar:

89. Skal den lokale Claude-session og cloud-sessionen på et tidspunkt kunne
    se databasen på samme måde (fx via et udtræk, der lægges i git)?
    Svar:

90. Skal der være en testdatabase ved siden af den rigtige, så nye
    programmer kan afprøves uden risiko?
    Svar:

91. Hvordan skal databasen klare det, når der kommer millioner af
    resultatrækker?
    Svar:

92. Hvilke spørgsmål vil du selv kunne stille databasen uden hjælp (fx "vis
    alle, der har bestået")?
    Svar:

93. Skal der være et enkelt skærmbillede (en app), hvor du kan se indholdet
    uden at skrive kode?
    Svar:

94. Hvad er reglen for navne på tabeller og kolonner (små eller store
    bogstaver, dansk eller engelsk)?
    Svar:

95. Hvordan registreres det, hvilken programudgave der lavede hver række i
    databasen?
    Svar:

## 7. TML-Server (backtest, analyse, selektering)

96. Hvad er TML-Serveren fysisk: en separat computer, en virtuel maskine
    eller samme maskine som TradingServer?
    Svar:

97. Hvilke programmer kører på TML-Serveren (TradeStation, MultiCharts,
    Python, andet)?
    Svar:

98. Hvordan sendes arbejde mellem TradingServer og TML-Server (filer,
    database, netværksmappe)?
    Svar:

99. Hvor mange backtests kan køres samtidig, og hvad er flaskehalsen:
    computerkraft, TradeStation-licenser eller tid?
    Svar:

100. Hvor lang tid tager én backtest i dag? Hvor lang tid vil alle tage
     samlet?
     Svar:

101. Hvad betyder "Selektering" konkret: hvem eller hvad vælger, og efter
     hvilke regler?
     Svar:

102. Hvilke analyser skal ligge på TML-Serveren, og hvilke skal ligge i
     Python et andet sted?
     Svar:

103. Hvad sker der, hvis TML-Serveren går ned midt i en lang kørsel? Kan den
     fortsætte, hvor den slap?
     Svar:

104. Skal TML-Serveren kunne styres, mens du ikke er ved computeren (fx over
     fjernskrivebord eller telefon)?
     Svar:

105. Skal der være adskillelse mellem maskinen, der udvikler strategier, og
     maskinen, der handler med rigtige penge?
     Svar:

106. Hvordan holdes programversioner ens på de to servere?
     Svar:

107. Hvor mange TradeStation-installationer og -licenser er der, og kan der
     købes flere?
     Svar:

108. Kan backtests køre om natten uden opsyn? Hvad forhindrer det i dag?
     Svar:

109. Hvordan fordeles arbejdet, hvis der kommer flere TML-maskiner?
     Svar:

110. Hvordan sikres det, at en backtest giver præcis samme resultat, hvis
     den køres igen?
     Svar:

111. Hvor gemmes backtest-indstillingerne (kurtage, slippage, handelstider),
     så de ikke ændres ved et uheld?
     Svar:

## 8. EdgeFinder (event-studie)

112. Forklar med dine egne ord, hvad EdgeFinder skal finde. Hvad er en
     "edge" for dig?
     Svar:

113. Hvad er et event-studie i dette projekt: hvad måles der efter hvert
     signal (fx prisbevægelse efter 5, 10, 30 bars)?
     Svar:

114. Hvilke tidshorisonter efter et signal skal måles?
     Svar:

115. Hvad sammenlignes signalets resultat med? Med tilfældige tidspunkter,
     med markedet generelt, eller med noget andet?
     Svar:

116. Hvornår er et resultat "Passed"? Hvilke tal skal være opfyldt?
     Svar:

117. Hvornår er det "Failed"? Og skal "næsten bestået" være en tredje
     kategori?
     Svar:

118. Hvor mange hændelser skal der mindst være i en test, før resultatet kan
     bruges?
     Svar:

119. Skal EdgeFinder se på både køb- og salgsretning for hvert signal?
     Svar:

120. Hvordan håndteres signaler, der ligger tæt efter hinanden og derfor
     måler den samme prisbevægelse flere gange?
     Svar:

121. Skal resultatet deles op i perioder (fx år for år) for at se, om edgen
     er stabil over tid?
     Svar:

122. Skal resultatet deles op efter markedstype (stigende, faldende,
     sidelæns, rolig, urolig)?
     Svar:

123. Hvilke workspace-indstillinger skal EdgeFinder sætte i TradeStation, og
     hvor er de beskrevet?
     Svar:

124. Hvad skal ske, hvis backtest-data i mappen er ufuldstændige eller
     forkerte ("stop process og meld fejl")? Hvem får beskeden, og hvordan?
     Svar:

125. Hvilke resultater skal "journalføres", og i hvilken tabel?
     Svar:

126. Skal EdgeFinder skrives i Python? Findes der allerede noget
     analysekode, der skal genbruges?
     Svar:

127. Hvem bestemmer rækkefølgen, tingene testes i i EdgeFinder, og er der en
     prioritering?
     Svar:

128. Hvordan måles det, om en edge er stor nok til at betyde noget i kroner
     og øre, og ikke kun i statistikken?
     Svar:

129. Skal EdgeFinder allerede regne kurtage og slippage med i event-studiet?
     Svar:

130. Hvad gør EdgeFinder med et resultat, der er godt på én tidsramme og
     dårligt på en anden?
     Svar:

131. Skal samme test køres på alle fire workspaces, og hvordan vægtes
     resultaterne mod hinanden?
     Svar:

132. Hvordan vælges indstillingerne for selve event-studiet (fx hvor længe
     der måles), uden at de også bliver tilpasset til at se godt ud?
     Svar:

133. Skal EdgeFinder kunne køre igen af sig selv, når der kommer nye data?
     Svar:

134. Hvor mange tests forventer du vil bestå? Og hvad gør vi, hvis næsten
     ingen eller næsten alle består?
     Svar:

## 9. EdgeCruncher

135. Hvad skal EdgeCruncher gøre? Beskriv det, som du forestiller dig det,
     selvom det ikke er færdigt.
     Svar:

136. Hvad får EdgeCruncher ind (kun "Passed" fra EdgeFinder?), og hvad
     sender den videre?
     Svar:

137. Skal EdgeCruncher kombinere flere signaler til én strategi? Hvor mange
     må der højst kombineres?
     Svar:

138. Hvor kommer indgang, udgang, stop-loss og gevinstmål ind i billedet? Er
     det EdgeCruncher eller et senere trin?
     Svar:

139. Hvad er det næste trin efter EdgeCruncher? Findes der et navn og en idé
     for det endnu?
     Svar:

140. Hvordan undgår EdgeCruncher at finde tilfældige kombinationer, der kun
     ser gode ud, fordi der er prøvet så mange?
     Svar:

141. Hvor mange kombinationer forventer du, at EdgeCruncher skal prøve?
     Tusinder, millioner?
     Svar:

142. Hvor lang tid må EdgeCruncher bruge pr. kørsel?
     Svar:

143. Hvordan vil du selv kunne se og forstå, hvorfor EdgeCruncher har valgt
     det, den har valgt?
     Svar:

144. "Data1, når den senere bliver mindre end Data2 (entry-finpudsning)" —
     hvor og hvornår hører det til?
     Svar:

145. Skal EdgeCruncher arbejde i Python, i TradeStation eller i begge?
     Svar:

146. Skal EdgeCruncher tage højde for, at markedet ændrer sig over tid (fx
     ved at teste de nyeste data for sig)?
     Svar:

147. Hvilke slags udgange skal prøves (efter tid, stop, gevinstmål, modsat
     signal)?
     Svar:

148. Skal strategierne fra EdgeCruncher være så enkle som muligt? Hvor mange
     regler må en strategi højst have?
     Svar:

149. Hvordan gemmes EdgeCrunchers resultater, så de kan sammenlignes med
     senere kørsler?
     Svar:

150. Hvornår er en strategi fra EdgeCruncher "færdig" og klar til næste
     trin?
     Svar:

## 10. Statistik og beskyttelse mod selvbedrag

151. Hvordan tages der højde for, at der testes tusindvis af signaler, så
     nogle vil se gode ud af ren tilfældighed (multiple testing)?
     Svar:

152. Tælles det, hvor mange forsøg der i alt er lavet, før en strategi blev
     fundet? Det er nødvendigt for at vurdere, hvor meget held der er med.
     Svar:

153. Hvilken metode skal bruges til out-of-sample-test (walk-forward, fast
     opdeling, andet)?
     Svar:

154. Må out-of-sample-data nogensinde bruges igen, efter de er set første
     gang? Hvad er reglen?
     Svar:

155. Hvordan testes, om en strategi er robust, når parametrene ændres en
     smule (fx 20 i stedet for 21)?
     Svar:

156. Skal strategier testes på andre markeder end dem, de blev fundet på,
     som ekstra kontrol?
     Svar:

157. Skal der laves "Monte Carlo"-test (tilfældig blanding af handlerne for
     at se, hvor slemt det kunne være gået)?
     Svar:

158. Hvilke nøgletal skal hver strategi vurderes på (fx Sharpe, profit
     factor, gennemsnitlig handel, max drawdown)? Og hvilket er det
     vigtigste?
     Svar:

159. Hvad er den mindste gennemsnitlige gevinst pr. handel, der kan overleve
     kurtage og slippage?
     Svar:

160. Skal der være et fast sæt af "kontrolsignaler" (tilfældige signaler),
     som alle resultater sammenlignes med?
     Svar:

161. Hvordan opdages det, hvis en resultatperiode domineres af én enkelt
     ekstrem dag eller hændelse?
     Svar:

162. Hvem eller hvad skal "angribe" en strategi, før den godkendes — Det
     Runde Bord, et fast testprogram eller begge dele?
     Svar:

163. Skal Det Runde Bord have et fast verdikt og en score (fx Go / No-go /
     Juster og 0–10)? Det står som ikke besluttet.
     Svar:

164. Hvordan dokumenteres alle forkastede idéer, så de ikke testes igen ved
     en fejl?
     Svar:

165. Hvor sikre skal vi være (signifikansniveau), før noget kaldes en edge?
     Svar:

166. Skal der rettes for antallet af tests med en fast metode (fx "Deflated
     Sharpe Ratio")? Hvem vælger metoden?
     Svar:

167. Hvordan undgås det, at man kigger på resultaterne og justerer, til det
     ser godt ud (skjult overtilpasning)?
     Svar:

168. Hvor lang skal en out-of-sample-periode være, før den tæller?
     Svar:

169. Skal systemet testes på "falske" data (fx tilfældigt blandede priser)
     for at se, om det også finder edge i ren støj?
     Svar:

170. Hvordan opdages fejl med fremtidige data (look-ahead) automatisk i
     koden?
     Svar:

171. Hvordan vurderes en strategi med få handler og stor gevinst mod en med
     mange handler og lille gevinst?
     Svar:

## 11. Fra enkelt-strategi til portefølje

172. Hvor mange strategier skal køre samtidig, når systemet er i fuld drift?
     Svar:

173. Hvordan måles det, om to strategier i virkeligheden gør det samme (for
     høj sammenhæng/korrelation)?
     Svar:

174. Hvordan fordeles kapitalen mellem strategierne: lige meget, efter
     risiko, eller efter noget andet?
     Svar:

175. Hvor ofte skal porteføljen gennemgås og ændres?
     Svar:

176. Hvad er reglen for at tage en strategi ud af drift? (Fx et bestemt tab,
     en bestemt periode med dårlige resultater.)
     Svar:

177. Hvad er reglen for at sætte en ny strategi i drift? Skal den først køre
     på papir (simuleret) i en periode?
     Svar:

178. Hvor lang en papirhandels-periode skal der være, og hvad skal den vise?
     Svar:

179. Skal strategier kunne slukkes midlertidigt, fx i perioder med meget uro
     i markedet?
     Svar:

180. Hvordan håndteres det, når to strategier vil handle modsat hinanden i
     samme marked på samme tid?
     Svar:

181. Hvordan vil du se et samlet overblik over hele porteføljen hver dag?
     Svar:

182. Skal der være et loft for, hvor stor en del af den samlede risiko én
     strategi må stå for?
     Svar:

183. Skal porteføljen have strategier med forskellige tidshorisonter for at
     sprede risikoen?
     Svar:

184. Hvordan testes hele porteføljen samlet bagud i tid, og ikke kun
     strategierne hver for sig?
     Svar:

185. Hvor mange strategier skal ligge i reserve, klar til at erstatte dem,
     der tages ud?
     Svar:

186. Hvad gør du, hvis alle strategier taber på samme tid?
     Svar:

187. Skal porteføljen tilpasse sig uro i markedet (fx mindre positioner, når
     det er uroligt)?
     Svar:

## 12. Handel i virkeligheden (execution)

188. Hvilket program skal sende ordrerne til markedet: TradeStation,
     MultiCharts eller et eget program?
     Svar:

189. Hvilke ordretyper skal bruges (markedsordre, limitordre, stopordre)?
     Svar:

190. Hvor meget slippage (forskel på forventet og faktisk pris) og kurtage
     regnes der med i backtests i dag? Er tallene målt eller gættet?
     Svar:

191. Hvordan sammenlignes de rigtige handler med backtesten bagefter, så
     forskelle opdages hurtigt?
     Svar:

192. Hvor store positioner kan de valgte markeder tåle, før dine egne ordrer
     flytter prisen?
     Svar:

193. Hvad sker der, hvis en ordre kun bliver delvist udført?
     Svar:

194. Hvad sker der, hvis internetforbindelsen eller strømmen forsvinder,
     mens der er en åben position?
     Svar:

195. Skal der ligge en stop-ordre hos brokeren hele tiden (så den virker,
     selvom din computer er slukket)?
     Svar:

196. Hvordan sikres det, at systemet ikke sender den samme ordre to gange
     ved en fejl?
     Svar:

197. Skal der være en "nødknap", der lukker alle positioner med ét tryk?
     Hvem må trykke på den?
     Svar:

198. Hvordan testes selve ordresystemet, før rigtige penge er på spil?
     Svar:

199. Beregnes backtests på bar-lukning, mens den rigtige handel sker midt i
     en bar? Er forskellen undersøgt?
     Svar:

200. Hvordan måles slippage i den rigtige handel, og hvor gemmes målingerne?
     Svar:

201. Hvad er reglen, hvis en ordre ikke bliver udført inden for en bestemt
     tid?
     Svar:

202. Skal systemet undgå at handle i de første og sidste minutter af
     handelsdagen?
     Svar:

203. Hvad gør systemet, hvis brokerens system er nede eller afviser ordrer?
     Svar:

204. Hvordan tjekkes det hver dag, at positionerne i systemet og hos
     brokeren er de samme?
     Svar:

## 13. Risikostyring

205. Hvor meget må tabes på én handel, i procent af kontoen?
     Svar:

206. Hvor meget må tabes på én dag, før systemet stopper for resten af
     dagen?
     Svar:

207. Hvor meget må tabes i en måned, før alt stoppes og gennemgås?
     Svar:

208. Hvor stor en samlet position må der højst være åben i ét marked og i
     alle markeder tilsammen?
     Svar:

209. Hvordan beregnes positionsstørrelsen: fast antal kontrakter, efter
     volatilitet eller efter noget andet?
     Svar:

210. Hvad gør systemet ved et pludseligt kæmpe prisfald (flash crash) eller
     et markedsstop?
     Svar:

211. Hvordan beskyttes systemet mod en programfejl, der fx køber 100
     kontrakter i stedet for 1?
     Svar:

212. Findes der en liste over de værste historiske markedsdage, som alle
     strategier skal testes igennem (stresstest)?
     Svar:

213. Hvem overvåger risikoen: et program, dig, eller begge?
     Svar:

214. Hvordan håndteres margin-krav, der pludselig stiger fra brokeren?
     Svar:

215. Må systemet øge positionerne efter en god periode, og i så fald efter
     hvilken regel?
     Svar:

216. Hvad er dit personlige smertepunkt: hvor stort et tab kan du se på uden
     at gribe ind manuelt?
     Svar:

217. Hvornår må systemet starte igen, efter at det har stoppet på grund af
     et dagstab?
     Svar:

218. Hvordan håndteres risikoen ved positioner over weekenden, hvis de
     nogensinde tillades?
     Svar:

219. Må systemet selv ændre risikogrænserne, eller må kun du?
     Svar:

220. Hvordan skrives alle ændringer af risikogrænser ned, så man kan se,
     hvem der ændrede hvad og hvornår?
     Svar:

221. Hvordan håndteres valutarisiko, hvis kontoen er i kroner og handlen
     sker i dollars?
     Svar:

## 14. Drift, overvågning og fejl

222. Hvordan får du besked, hvis noget går galt (mail, sms, telefon-besked)?
     Svar:

223. Hvilke fejl skal stoppe alt med det samme, og hvilke må bare
     registreres og samles op senere?
     Svar:

224. Skal der være én samlet fejllog for hele projektet, eller én pr.
     delprojekt?
     Svar:

225. Hvordan tjekkes det hver dag, at alle dele kører (data kommer ind,
     programmer svarer, databasen er i orden)?
     Svar:

226. Hvad gør du, hvis TradeStation opdateres og en automatisering holder op
     med at virke?
     Svar:

227. Skal der være en fast rutine efter hver handelsdag (gennemgang,
     afstemning mod brokeren)?
     Svar:

228. Hvordan genstartes hele systemet fra bunden efter et nedbrud, og står
     det skrevet ned?
     Svar:

229. Reglen "ved fejl: ret, ryd op og kør forfra" — gælder den også for
     EdgeFinder, EdgeCruncher og live-handel?
     Svar:

230. Skal der komme en daglig statusrapport, også når alt går godt?
     Svar:

231. Hvordan testes det, at alarmerne rent faktisk virker (fx en prøvealarm
     hver uge)?
     Svar:

232. Hvordan undgås det, at Windows-opdateringer genstarter maskinen midt i
     en kørsel?
     Svar:

233. Hvad sker der, hvis du ikke svarer på en alarm inden for en bestemt
     tid?
     Svar:

234. Skal der føres en log over alle alvorlige fejl, med årsag og løsning?
     Svar:

## 15. TradeStation og MultiCharts

235. Hvorfor skal systemet også laves til MultiCharts? Hvad er gevinsten?
     Svar:

236. Hvornår skal MultiCharts-delen starte: når hele kæden virker i
     TradeStation, eller tidligere?
     Svar:

237. Skal resultaterne fra TradeStation og MultiCharts sammenlignes, så de
     kontrollerer hinanden?
     Svar:

238. Hvad gør vi, hvis de to platforme giver forskellige resultater for
     samme test?
     Svar:

239. Er der risiko for at blive for afhængig af TradeStation (pris, licens,
     at de ændrer programmet)? Hvad er plan B?
     Svar:

240. Skal der på sigt laves en egen backtest-motor i Python, så man ikke er
     afhængig af UI-automatisering af TradeStation?
     Svar:

241. Hvilke begrænsninger i EasyLanguage har vi mødt, som kunne tale for at
     flytte dele af beregningerne ud af TradeStation?
     Svar:

242. Hvilken udgave af TradeStation bruges, og hvornår må den opdateres?
     Svar:

243. Skal MultiCharts bruge sin egen dataleverandør eller de samme data som
     TradeStation?
     Svar:

244. Findes der ting, vi bruger i TradeStation, som slet ikke findes i
     MultiCharts?
     Svar:

245. Hvis TradeStation ændrer priser eller lukker, hvor hurtigt kan vi så
     flytte?
     Svar:

## 16. Automatisering og "fuldautomatisk"

246. Hvad betyder "fuldautomatisk" for dig? Hvilke trin må ALDRIG ske uden
     din godkendelse?
     Svar:

247. Hvilke trin i kæden kræver i dag, at du sidder ved computeren?
     Svar:

248. Hvordan startes kæden: af dig, på et fast tidspunkt, eller af sig selv,
     når der kommer noget nyt?
     Svar:

249. Skal der være én "dirigent", der styrer alle trin, fx EdgeFinder og
     EdgeCruncher i rækkefølge, eller kører de hver for sig?
     Svar:

250. Hvordan ved det næste trin, at det forrige trin er færdigt og godkendt?
     Svar:

251. Hvilken rolle skal Claude have, når systemet kører: udvikler,
     kontrollant, analytiker, eller slet ingen i den daglige drift?
     Svar:

252. Hvordan kan du stoppe hele kæden med ét tryk, hvis noget ser forkert
     ud?
     Svar:

253. Hvordan ser du, hvor langt kæden er nået lige nu (fx en statusside)?
     Svar:

254. Må systemet selv rette fejl, eller skal det altid stoppe og spørge?
     Svar:

255. Skal systemet selv foreslå nye ting at teste ud fra tidligere
     resultater?
     Svar:

256. Hvordan undgås det, at automatikken skjuler fejl, som et menneske ville
     have set?
     Svar:

## 17. Arbejdsmåde, dokumentation og Claude

257. Der er mange dokumenter, der delvist modsiger hinanden (NOTER,
     BYGGEVEJLEDNING, NOTAT, OPGAVEBESKRIVELSE, BESLUTNINGSLOG). Skal der
     laves én "sandhed" pr. delprojekt, som altid er opdateret?
     Svar:

258. Skal der være en fast oversigt (et "kort") over hele projektet, som
     viser alle delprojekter, deres status og hvordan de hænger sammen?
     Svar:

259. Filnavnet `Task_RawSignal_Creature_EdgeFinder_opgave.md` ligger i
     roden. Skal procesbeskrivelserne have deres egen fast plads (fx én
     mappe pr. delprojekt)?
     Svar:

260. Kategorien "TradingApp" står i VIDENSLOG uden poster. Hvad er
     TradingApp, og er den stadig en del af projektet?
     Svar:

261. Hvordan skal lokal Claude og cloud-Claude dele arbejdet mellem sig?
     Hvad skal hver især lave?
     Svar:

262. Hvordan får cloud-Claude viden om databasens aktuelle indhold, når den
     ikke kan se den?
     Svar:

263. Hvordan vil du helst have, at Claude stiller spørgsmål: ét ad gangen,
     samlet i en liste, eller i et skema som dette?
     Svar:

264. Er der fejl eller misforståelser i samarbejdet med Claude indtil nu,
     som skal skrives ind i VIDENSLOG, så de ikke sker igen?
     Svar:

265. Hvordan skal FriSnak-optagelser gemmes, så idéerne ikke går tabt (fx en
     fast mappe med dato)?
     Svar:

266. Hvordan skal en idé fra FriSnak blive til en opgave: hvem skriver den
     om til en plan, og hvem godkender den?
     Svar:

267. Hvor ofte skal VIDENSLOG gennemgås og ryddes op, så gammel viden ikke
     vildleder?
     Svar:

268. Skal alle programmer have faste automatiske afprøvninger (tests), der
     køres før hver ændring?
     Svar:

269. Hvordan sikres det, at den lokale session altid har den nyeste udgave
     fra GitHub?
     Svar:

270. Hvilke opgaver giver du helst til den lokale Claude, og hvilke til
     cloud-Claude?
     Svar:

271. Skal der være en fast skabelon for opgavebeskrivelser, så Claude ikke
     misforstår dem?
     Svar:

## 18. Sikkerhed, backup og hardware

272. Hvor ligger koden, databasen og dataene fysisk, og hvad sker der ved
     brand, tyveri eller en død harddisk?
     Svar:

273. Er der en kopi af alt vigtigt uden for huset (fx i skyen)?
     Svar:

274. Hvordan beskyttes adgangskoder til broker, database og servere? Står
     nogen af dem i filer, der kommer i git?
     Svar:

275. Hvem har adgang til fjernskrivebordet på serverne, og er det sikret med
     mere end en adgangskode?
     Svar:

276. Har serverne nødstrøm (UPS), og hvor længe kan de køre uden strøm?
     Svar:

277. Er GitHub-projektet privat, og skal det forblive det?
     Svar:

278. Hvordan beskyttes serverne mod virus og hackere?
     Svar:

279. Hvor lang tid tager det at bygge en server op igen fra bunden, og står
     det skrevet ned?
     Svar:

280. Findes der en liste over alle programmer og licenser, og hvornår de
     udløber?
     Svar:

281. Hvad sker der, hvis din GitHub-konto eller din mail bliver hacket?
     Svar:

## 19. Læring og forbedring over tid

282. Hvordan skal systemet lære af de strategier, der fejler i den rigtige
     handel?
     Svar:

283. Hvor ofte skal hele kæden gennemgås for at se, om metoderne stadig er
     de bedste?
     Svar:

284. Hvordan måles det, om selve udviklingssystemet bliver bedre over tid
     (fx flere holdbare strategier pr. måned)?
     Svar:

285. Hvad skal der ske med strategier, der holder op med at virke: slettes,
     gemmes eller undersøges?
     Svar:

286. Skal der laves en fast gennemgang efter hver måned eller hvert kvartal?
     Svar:

287. Hvordan sikres det, at nye idéer fra FriSnak bliver vurderet og ikke
     glemt?
     Svar:

288. Skal Det Runde Bord være et fast trin i processen, fx før en strategi
     handler med rigtige penge?
     Svar:

## 20. Rapportering og nøgletal

289. Hvilke 5 tal vil du gerne se hver morgen?
     Svar:

290. Hvilke tal vil du se hver uge og hver måned?
     Svar:

291. Hvordan skal rapporterne se ud: tal, diagrammer, tekst eller en
     blanding?
     Svar:

292. Hvor skal rapporterne vises: på mail, i en app eller på telefonen?
     Svar:

293. Skal der være en rapport, der kan vises til en bank, en revisor eller
     en investor?
     Svar:

294. Hvordan skal rapporterne sammenligne de rigtige resultater med det,
     backtesten lovede?
     Svar:

## 21. Prioritering og næste skridt

295. Hvis du kun kunne vælge ét hul fra dette skema at lukke den næste
     måned, hvilket skulle det være?
     Svar:

296. Hvilke spørgsmål i skemaet vil du have diskuteret ved Det Runde Bord?
     Svar:

297. Hvilke emner mangler helt i dette skema?
     Svar:

298. Hvad er den næste konkrete opgave, du vil give til Claude, når skemaet
     er besvaret?
     Svar:

299. Hvilke tre ting i projektet er du mest usikker på lige nu?
     Svar:

300. Er der noget, der allerede er bygget, som bør laves om, før der bygges
     videre ovenpå?
     Svar:
