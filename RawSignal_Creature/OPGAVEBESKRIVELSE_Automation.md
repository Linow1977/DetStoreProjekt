# Opgavebeskrivelse: RawSignal-Creature — automationsprogram (TradeStation-blok)

Denne beskrivelse er skrevet til den Claude Code-session, der kører lokalt på
Thomas' maskine med adgang til TradeStation, TradingApp og TradingDB. Læs
`ARBEJDSBESKRIVELSE_RawSignal.md` og `NOTER.md` i samme mappe først — de
forklarer baggrunden for RawSignal-projektet som helhed.

## Formål

En del af **RawSignal-Creature**-programmet: automatisk lægge `.el`-filer
ind i TradeStation Development Environment (`TSDev.exe`), verificere dem,
og gemme resultatet i TradingDB. Styres fra en fane i **TradingApp.bat** —
ikke som et separat vindue/program.

## Databaseadgang: TradingDB

Programmet har **læse- og skriveadgang** til TradingDB:

- **Læser** fra `Filter_Case` — filtrene og deres information (samme
  tabel som RawSignal-filerne oprindeligt er bygget ud fra).
- **Skriver** til en ny tabel, **`RawSignal_Case`**, med mindst felterne:
  - `RawSignal-Name`
  - `Dev. date` (byggedato)
  - `File Path`
  - `Verification` (resultat af Verify)
  - `Note`

Programmet bruger `RawSignal_Case` til at afgøre, hvilke filer der allerede
er kørt, og hvilke der er **nye** og mangler at blive kørt (relevant for
"Fra filter nummer"-feltet i fanen, se nedenfor).

## Opbygning: TradeStation-blok nu, Multicharts-blok senere

TradeStation og Multicharts deler ikke automations-logik — forskellig
opbygning, betjening og kodesprog. Programmet bygges som selvstændige
blokke:

- **Nu:** kun TradeStation-blokken bygges.
- **Senere:** Multicharts-blokken tilføjes som en helt separat blok, uden
  at røre TradeStation-blokken. Fælles for begge blokke, når Multicharts
  kommer: samme fane, samme log-princip, samme kontrolpunkt-funktion.

## Forudsætning: den bekræftede manuelle arbejdsgang

Arbejdsgangen er testet manuelt, én fil ad gangen, i TSDev.exe:

1. Hvis TSDev.exe ikke er åben, åbn det.
2. Ny strategi: `Ctrl+Alt+S`.
3. Navngiv strategien `RawSignal...` → Enter.
4. Indsæt signalteksten.
5. Verify: `F3`.
6. Luk: `Alt+C`.

Automationen skal efterligne præcis dette forløb.

## Fanen i TradingApp — betjeningselementer

| Element | Funktion |
|---|---|
| **Kør** | Starter kørslen |
| **Maskine/server-valg** | Vælg hvilken computer/maskine TradeStation-blokken skal køre på (relevant hvis flere maskiner har TradeStation installeret) |
| **Fra filter nummer** | Start kørslen fra et bestemt filternummer — fanen viser hvilke der er **nye** (findes i `Filter_Case`, mangler i `RawSignal_Case`) |
| **Kontrolfunktion (til/fra)** | Slår kontrolpunkt-pausen til/fra |
| **Antal mellem kontrol** | Antal filer mellem hvert kontrolpunkt (fx 30) |
| **Pause** | Stopper kørslen midlertidigt, uanset kontrolfunktionen |
| **Live Log** | Viser loggen mens programmet kører, ikke kun bagefter |

## Hvordan Verify-resultatet aflæses

Efter F3 vises resultatet i **Output-panelet** nederst i TSDev.exe:
- Ved succes: `0 error(s), 0 warning(s)` i kolonnen "Description".
- Ved fejl: fejltekst, med kolonnerne Technique/Line/Type der viser hvor
  fejlen er.

Statuslinjen nederst i vinduet viser desuden **"VERIFIED"**, når filen er
godkendt. Automationen skal aflæse Output-panelets tekst og/eller
status-ordet "VERIFIED" for at afgøre succes/fejl, og skrive resultatet
ind i `RawSignal_Case.Verification` (og `.Note` ved fejl, med selve
fejlteksten).

## Krav til selve kørslen

1. **Fuldt automatisk.** Intet manuelt arbejde undervejs, medmindre
   kontrolfunktionen er aktiveret. Programmet åbner TSDev.exe (hvis ikke
   allerede åben), opretter ny strategi, navngiver den, indsætter
   signalteksten, trykker Verify, læser resultatet, lukker, og går videre
   til næste fil — for alle filer, der mangler i `RawSignal_Case`.
2. **Fejlhåndtering: stop aldrig, log og fortsæt.** Fejler én fil, noteres
   det i `RawSignal_Case` (Verification + Note) og i logfilen, og
   programmet går videre til næste. Hele kørslen stopper ikke på grund af
   én fejlende fil.
3. **Indledende testkørsel på en lille, blandet gruppe.** Før programmet
   sættes til at køre for alvor: afprøv det på et lille udsnit af
   `RawSignal_(Nummer)_Test.el`-filer (navnekonvention under udvikling),
   der dækker de forskellige filtertyper:
   - Et filter uden parametre.
   - Et filter med kun én parameter (N1 eller N2).
   - Et filter med to parametre.
   - Et filter der bruger en indbygget seriefunktion (MACD/RSI/
     StandardDev/DMI/ChaikinMoneyFlow).

   Bekræft at resultatet stemmer, før det køres i fuld skala.
4. **Log.** Alt skrives til en logfil, og vises live i fanens "Live Log" —
   ikke kun på skærmen undervejs og væk bagefter. Pr. fil: filnavn,
   tidspunkt, resultat (OK/fejlet + evt. fejltekst). Ved afslutning (og
   ved hvert kontrolpunkt): en opsummering med antal OK/fejlet og liste
   over fejlende filer.

## Stadig uafklaret — undersøg og rapportér tilbage, gæt ikke

1. **CLI/API-adgang til TradeStation.** Undersøg
   `C:\Program Files (x86)\TradeStation 10.0\Program` for værktøjer, der
   kan give en mere robust adgang til Verify-funktionen end at simulere
   museklik/tastatur og aflæse skærmen. Findes intet sådant, byg videre
   med UI-automatisering, men gør den robust (vent på bekræftede
   tilstande, genkend fejl-dialogbokse eksplicit).
2. **Hvordan filerne når frem til automationsprogrammet.** Er det samme
   git-projekt (`DetStoreProjekt`), hentet med `git pull` på Thomas'
   maskine, eller ligger de et andet sted?

## Ikke en del af denne opgave

- Multicharts-blokken (kommer som selvstændig opgave senere).
- Ændringer af `.el`-filernes indhold eller af `Filter_Case`.
- Kørsel af backtests.
- Navngivning og flytning af selve CSV-outputtet fra en kørt backtest —
  det håndteres af det separate EdgeFinder-programmet, ikke af dette
  automationsprogram.
