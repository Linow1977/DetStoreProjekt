# Opgavebeskrivelse: Automationsprogram til verificering af RawSignal-filer

Denne beskrivelse er skrevet til den Claude Code-session, der kører på
Thomas' egen maskine ved siden af TradeStation. Læs `ARBEJDSBESKRIVELSE_RawSignal.md`
og `NOTER.md` i samme mappe først — de forklarer baggrunden for RawSignal-
projektet som helhed.

## Formål

Der findes (op til) 381 `.el`-filer, der hver skal lægges ind i TradeStation,
verificeres (kompileres), og resultatet aflæses — uden at Thomas selv skal
gøre det manuelt for hver fil. Programmet skal køre **fuldt automatisk**,
men med et indbygget kontrolpunkt, så Thomas kan holde øje undervejs uden at
overvåge hele kørslen.

## Krav til programmet

### 1. Undersøg adgangsvejen til TradeStation FØRST

Før noget bygges: undersøg om TradeStation tilbyder en kommandolinje- eller
API-adgang til at åbne/indsætte/kompilere en EasyLanguage-fil uden den
grafiske flade. Det ville gøre automationen markant mere robust end at
simulere museklik og tastatur, som knækker ved uventede dialogbokse eller
hvis et vindue flytter sig.

Rapportér tilbage hvad der findes, før byggeriet går i gang. Findes der
ingen sådan adgang, byg med UI-automatisering (styring af mus/tastatur/
vinduer), men gør det så robust som muligt (vent på bekræftede
tilstande i stedet for faste pauser, genkend fejl-dialogbokse eksplicit).

### 2. Fuldt automatisk kørsel

Programmet skal, uden at Thomas skal gøre noget undervejs:

1. Tage næste `.el`-fil fra listen.
2. Lægge den ind i TradeStation (som Analysis Technique/Strategy).
3. Trykke Verify (eller tilsvarende).
4. Læse resultatet — kompileret uden fejl, eller fejlbesked.
5. Notere resultatet i loggen (se punkt 4 nedenfor).
6. **Ved fejl: fortsæt til næste fil.** Programmet stopper ikke hele
   kørslen på grund af én fejlende fil. Fejlen skal kunne findes og rettes
   bagefter ud fra loggen.
7. Gå til næste fil, indtil alle er behandlet.

### 3. Indledende testkørsel, før alle filer køres

Inden programmet sættes til at køre alle 381 filer, skal det først afprøves
på en lille, bevidst blandet gruppe af testfiler, der dækker de forskellige
typer signaler/filtre der findes i projektet, fx:

- Et filter uden parametre (som `RawSignalTest_2.el`).
- Et filter med kun én parameter (N1 eller N2).
- Et filter med to parametre (som `RawSignalTest_1.el`).
- Et filter der bruger en indbygget seriefunktion (MACD/RSI/StandardDev/DMI/
  ChaikinMoneyFlow), for at bekræfte at advarslen i filens hoved ikke
  forstyrrer selve verificeringen.

Kør automationen på denne lille gruppe først, og bekræft at resultatet
(kompileret/fejlet) stemmer med det, Thomas allerede ved om disse filer,
før den sættes til at køre på de resterende filer i fuld skala.

### 4. Kontrolpunkt hver N. fil (valgfrit, indstilleligt)

Programmet skal have en indstilling for, hvor ofte det stopper op og venter
på Thomas, fx hver 30. fil (tallet skal kunne ændres, ikke være fastlåst
til 30). Ved et kontrolpunkt:

- Kørslen sættes på pause.
- Status vises: hvor mange filer behandlet, hvor mange OK, hvor mange
  fejlet, og hvilke.
- Thomas kan vælge: fortsæt automatisk, eller stop helt.

Denne indstilling skal også kunne slås fra, så programmet kan køre uden
afbrydelse fra start til slut, hvis Thomas ønsker det.

### 5. Log

Alt hvad programmet foretager sig, skal skrives til en logfil (ikke kun
vises på skærmen), så et forløb kan gennemgås bagefter uden at have set det
køre. Loggen skal som minimum indeholde, pr. fil:

- Filnavn.
- Tidspunkt behandlet.
- Resultat: verificeret OK, eller fejlet (med selve fejlteksten fra
  TradeStation).

Ved afslutning (eller ved et kontrolpunkt) skal der desuden skrives en
opsummering: hvor mange filer i alt, hvor mange OK, hvor mange fejlet, og en
liste over de fejlende filnavne med deres fejl.

## Ikke en del af denne opgave

- Ingen ændringer af selve `.el`-filernes indhold — programmet skal kun
  lægge dem ind og læse resultatet, ikke rette i dem.
- Ingen kørsel af backtests — kun verificering (kompilering).
- Rapportér tilbage før byggeriet går videre, hvis der undervejs opstår
  spørgsmål der ikke er svaret på her — gæt ikke.
