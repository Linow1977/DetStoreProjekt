# Beslutningslog — RawSignal-projektet, 22. september 2026

Opsummering af dagens afklaringer, skrevet så en ny session (menneske eller
Claude) kan samle op uden at have været med. Se `BESLUTNINGSLOG_2026-09-18.md`
for baggrunden fra dagen før.

## Udgangspunkt

Denne cloud-session har kun adgang til GitHub-projektet `DetStoreProjekt` —
ikke til TradingDB, TradeStation eller Thomas' maskine. Selve generering af
de 381 `.el`-filer og byggeriet af automationsprogrammet skal ske på den
lokale Claude Code-session. Dagens arbejde her har været at afklare og
dokumentere beslutninger, ikke at bygge kode.

## Navngivning af CSV-output — det gamle problem er løst udefra

Beslutningen fra 19. september om at droppe `FileAppend` (for langsom på
625 kombinationer) genåbnede spørgsmålet om, hvordan CSV-filnavnet skulle
bygges uden en dynamisk streng i koden. Tre løsninger blev lagt frem —
ingen af dem blev valgt. I stedet:

- Der laves **kun én universal `.el`-fil pr. filter** (ikke fire varianter
  pr. workspace).
- **Det separate EdgeFinder-programmet** står for at navngive den færdige
  CSV-fil og flytte den til den rigtige mappe, efter kørslen. Det er ikke
  længere `.el`-filens eget ansvar.
- Hvilken skrivemetode selve `.el`-koden bruger internt (`Print(File(...))`
  med fast navn, eller en simplere `FileAppend`) er stadig ikke besluttet —
  men det er ikke længere kritisk, da EdgeFinder alligevel omdøber/flytter
  filen bagefter.

**Følgevirkning:** `RawSignalTest_1.el` og `RawSignalTest_2.el` bruger
stadig den gamle, dynamiske `FileAppend`-metode og skal bygges om, når
skabelonen opdateres.

## RawSignal-Creature: automationsprogrammet er nu fuldt beskrevet

En ny fil, `OPGAVEBESKRIVELSE_Automation.md`, beskriver programmet der skal
lægge `.el`-filer ind i TradeStation, verificere dem, og logge resultatet.
Centrale beslutninger:

- **Programmet hedder RawSignal-Creature** og styres fra sin egen fane i
  **TradingApp.bat** — ikke et separat vindue.
- Fanens betjeningselementer: Kør, maskine/server-valg (hvilken computer
  automationen kører på — IKKE et valg mellem TradeStation/Multicharts),
  "Fra filter nummer" (med visning af nye filer der mangler at blive
  kørt), kontrolfunktion til/fra, antal filer mellem kontrolpunkter,
  Pause, og en Live Log.
- **Fuldt automatisk:** intet manuelt arbejde, medmindre kontrolfunktionen
  er slået til.
- **Fejlhåndtering:** stopper aldrig hele kørslen på grund af én fejlende
  fil — noterer og fortsætter.
- **Indledende testkørsel** på en lille, blandet gruppe filtertyper (ingen
  parametre / én / to parametre / seriefunktion), før fuld kørsel på alle
  filer.
- **TradeStation-blok bygges først.** Multicharts er en selvstændig,
  separat blok, der tilføjes senere — de to platforme deler intet
  automations-logik (helt forskellig opbygning, betjening og kodesprog).

### TradingDB: ny tabel `RawSignal_Case`

Automationsprogrammet får læse- og skriveadgang til TradingDB:
- **Læser** `Filter_Case` (kilden til selve filtrene — uændret).
- **Skriver** til en ny tabel, **`RawSignal_Case`**, med felterne
  `RawSignal-Name`, `Dev. date`, `File Path`, `Verification`, `Note`.

Denne tabel bruges også til at afgøre, hvilke filer der er "nye" og mangler
at blive kørt.

### Vigtigt teknisk fund: TradeStation Development Environment har ingen API

Et opklarende spørgsmål blev stillet om, hvorvidt TradeStations officielle
Web API kunne bruges til at styre automationen. Svaret, undersøgt og
bekræftet:

- **TradeStation Development Environment (TDE)** — hvor EasyLanguage
  skrives og Verify trykkes — er en ren lokal editor uden internetforbindelse
  og uden nogen officiel API.
- **TradeStations Web API** er et helt separat system, kun til handel
  (kurser, konto, ordrer, streaming-data). Det har ingen bro til TDE.
- Den eneste kommunikationsvej mellem de to ("Command Line Commands") går
  fra EasyLanguage-koden *til* TradeStation — ikke omvendt.

**Konklusion:** automationsprogrammet kan ikke bygges på et API. Det skal
være **ren UI-automatisering** (simuleret tastatur/museklik), der
efterligner den bekræftede manuelle arbejdsgang i TSDev.exe:
`Ctrl+Alt+S` → navngiv → indsæt tekst → `F3` (Verify) → `Alt+C` (Luk).
Resultatet aflæses fra Output-panelet (`0 error(s), 0 warning(s)` ved
succes, ellers fejltekst med Technique/Line/Type) og status-ordet
"VERIFIED".

**Filhentning:** automationsprogrammet henter selv `.el`-filerne fra git —
ingen manuel levering nødvendig.

## Filoversigt, opdateret

| Fil | Formål | Status |
|---|---|---|
| `OPGAVEBESKRIVELSE_Automation.md` | Fuld spec til automationsprogrammet (RawSignal-Creature, TradeStation-blok) | Færdig, ingen åbne spørgsmål tilbage |
| `NOTER.md` | Levende teknisk referencedokument | Opdateret med navngivnings-afklaring, ny DB-tabel, TSDev.exe-arbejdsgang, API-afklaring |
| `ARBEJDSBESKRIVELSE_RawSignal.md` | Spec til generering af de 381 `.el`-filer | Opdateret til den nye navngivningsmodel, henviser til automations-filen |
| `BESLUTNINGSLOG_2026-09-18.md` | Gårsdagens beslutningslog | Uændret |
| `BESLUTNINGSLOG_2026-09-22.md` | Denne fil | Øjebliksbillede af dagens arbejde |

## Hvad der IKKE er lavet endnu

- De 381 `.el`-filer er stadig ikke genereret.
- `RawSignalTest_1.el`/`RawSignalTest_2.el` er ikke bygget om til den nye
  navngivningsmodel endnu.
- Automationsprogrammet er beskrevet, men ikke bygget.
- Tabellen `RawSignal_Case` er ikke oprettet i TradingDB endnu.
- Multicharts-blokken er ikke en del af det, der bygges nu.
