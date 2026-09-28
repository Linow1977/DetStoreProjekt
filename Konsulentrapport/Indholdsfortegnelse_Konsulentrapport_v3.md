---
title: "Indholdsfortegnelse"
subtitle: "Konsulentrapport, version 3: udviklingsmotoren i DetStoreProjekt (28. september 2026)"
---

*Fil: Konsulentrapport_v3_2026-09-28.docx (samme mappe). Sidetal er ikke med, fordi de afhænger af, hvordan Word viser filen. Brug overskrifterne til at søge i rapporten, eller brug navigationsruden i Word (Vis → Navigationsrude).*

# Læsevejledning

| Har du ... | Så læs |
|---|---|
| 5 minutter | Sammenfatning |
| 30 minutter | Sammenfatning + Del 4 (især 4.3 Fase 0 og 4.7 Åbne punkter) |
| Skal du træffe beslutninger | Del 4.7, derefter de afsnit, hvert punkt henviser til |
| Vil du forstå fagligheden | Del 1–3 og 1B–3B i rækkefølge |

# Indhold


## Sådan er rapporten bygget op

*Hvordan de fire dele, B-delene og bilagene hænger sammen.*


## Aftalen for runde 3

*Opdraget, kilderne, Det Runde Bords afgørelser og den overordnede agents kontrol.*


## Sammenfatning (højst en halv side)

*Hele rapporten på en halv side.*


## Del 1 – Validering (Konsulent 1: kvantitativ statistiker), version 2

*Konsulent 1 (statistiker): hvornår er en strategi "færdig", hvor mange forsøg fabrikken reelt laver, grænser regnet efter, plateau-trappen og genvækning.*

- 0\. Kort sammenfatning: de vigtigste nye fund
- 1\. Definition af "færdig strategi", version 2
- 2\. Hvad projektets filer faktisk viser (fakta, jeg bygger på)
- 3\. Det rigtige antal forsøg, trin for trin
    - 3.1 Det rå antal (N_rå)
    - 3.2 Det effektive antal (N_eff)
    - 3.3 Hvad det betyder for grænserne
- 4\. Kalibrering af grænserne med regnestykker
    - 4.1 F4: grænsen afhænger af N_eff, og N_eff skal måles
    - 4.2 F10: kan en realistisk edge overhovedet ses? (styrkeberegning)
    - 4.3 F6: walk-forward
    - 4.4 F2/F9: pengeskabet (hold-out) kan ikke bevise meget
    - 4.5 F8: stabilitet over år
    - 4.6 PBO (sandsynlighed for overfitting ved udvælgelsen)
- 5\. Svagheder led for led (opdateret)
- 6\. EdgeFinder: godkendelse punkt for punkt
- 7\. Metode for RawSignal-Analyse (opdateret)
- 8\. Plateau-trappen: tre testbare farvedefinitioner (Thomas vælger)
- 9\. AvgTrueRange-testen: hvad den beviser, og hvad den ikke beviser
- 10\. Stikprøvekontrol (metode, Konsulent 2 udfører)
- 11\. Regimeskift og genvækning fra dvale
- 12\. Angreb på mit eget første udkast
- 13\. Åbne punkter til Thomas
- Kilder

## Del 1B – Værktøjer og protokoller til validering (Konsulent 1)

*Konsulent 1: statistiske værktøjer (StepM, bootstrap, FDR, DSR, placebo) og faste arbejdsregler. Det Runde Bord regnet i tal: 2025-regler og inkubationsregler.*

- 0\. Kort: de fem vigtigste anbefalinger (BRUG NU)
- 1\. Værktøjer: otte vurderet grundigt
    - V1. statsmodels.stats.multitest – Holm, BH, BY og lokal FDR
    - V2. arch.bootstrap – blok-bootstrap og optimal bloklængde
    - V3. arch.bootstrap.StepM (Romano-Wolf) og SPA (Hansen/White)
    - V4. arch.bootstrap.MCS – Model Confidence Set
    - V5. Deflated Sharpe, PSR og MinTRL
    - V6. CSCV/PBO (sandsynlighed for overfitting ved udvælgelsen)
    - V7. Måling af N_eff med egenværdier (Nyholt, Li-Ji) og klynger
    - V8. Generator til kontrolsignaler (placebo og indplantet edge)
- 2\. Protokoller for forskningsdisciplin, så Thomas kan følge dem uden at kode
    - P1. Forhåndsregistrering ("hypotesekort")
    - P2. Forsøgsregister
    - P3. Låst pengeskab
    - P4. Blind analyse
    - P5. Kontrolsignaler i hver kørsel
    - P6. To-nøgle-reglen
- 3\. Huller fra v2, der nu er lukket
    - 3.1 Max Bars Back-testen (1000 mod 2000) eller opvarmningstesten?
    - 3.2 Faste kolonner i passet (til Konsulent 3)
- 4\. Hvordan man kalibrerer grænser uden lang historik
- 5\. Det Runde Bord: konsekvenser for valideringen
    - 5.1 Hvad kan fabrikken ærligt finde med 5 år in-sample og 1 år out-of-sample?
    - 5.2 Hvordan Lag A/B/C passer med F1–F10
    - 5.3 Lag A: en statistisk regel, der ikke dræber ægte edges
    - 5.4 Regel for "2025 slides op"
    - 5.5 Inkubation: tre gennemregnede beslutningsregler (Thomas vælger)
    - 5.6 Uenighederne på bordet: faglig vurdering (står åbne)
- 6\. Nye åbne punkter til Thomas
- 7\. Kilder, jeg selv har åbnet eller læst

## Del 2 – EasyLanguage: kvalitet, EdgeCruncher og MultiCharts (Konsulent 2, runde 2)

*Konsulent 2 (EasyLanguage): tavse fejl fundet i den rigtige kode, MACD-fejlen, kontrolplanen, EdgeCruncher og MultiCharts.*

- 0\. Kort sagt – de fem vigtigste fund
- 1\. Fejlliste ud fra den rigtige kode
    - 1.1 Seriefunktion kaldt i løkke – MACD-typen
    - 1.2 Serie-indgang, der afhænger af løkken
    - 1.3 Advarselslisten er en navneliste
    - 1.4 Opvarmning af funktioner med tilbagekobling
    - 1.5 Blandede datastrømme (Data1 mod Data2)
    - 1.6 Tidsstempel = bar-slut, og kan blive læst som bar-start
    - 1.7 Filnavn, overskrivning og manglende oprindelse
    - 1.8 Decimal-løkker kan springe den sidste værdi over
    - 1.9 Verify-trinnet
    - 1.10 Mindre, men reelt
- 2\. MACD-mekanismen – hvad vi ved, og hvad vi ikke ved
    - 2.1 Fakta fra projektet (BEVIST)
    - 2.2 Den bedste forklaring (SANDSYNLIGT)
    - 2.3 Hvilke funktioner er i risiko?
    - 2.4 Robuste måder at skrive det på (mønstre, ikke kode)
- 3\. AvgTrueRange-testen – hvad beviser den?
- 4\. Kontrolplanen – konkret for dette projekt
- 5\. EdgeCruncher – holdt op mod Thomas' egen proces
- 6\. Porting til MultiCharts
- 7\. Angreb på mit eget første udkast
- 8\. Nye åbne punkter til Thomas

## Del 2B – Værktøjer, teknikker og EdgeFinder-protokol (Konsulent 2, runde 3)

*Konsulent 2: TA-Lib som facit, testteknikker, formel-parser og den godkendte EdgeFinder-protokol (afsnit 4).*

- 0\. Kort: de fem vigtigste anbefalinger (BRUG NU)
- 1\. Uafhængige referenceberegninger af indikatorer
    - 1.1 Hvad jeg har læst i TA-Lib
    - 1.2 Er startværdien den samme som i TradeStation?
    - 1.3 Kandidaterne vurderet
- 2\. Testteknikker for kodekvalitet
    - 2.1 Differential testing (to uafhængige udgaver sammenlignes)
    - 2.2 Golden master (snapshot) med kontrolsum
    - 2.3 Property-based testing (hypothesis)
    - 2.4 Mutationstest (plant en fejl)
    - 2.5 Statisk analyse med en rigtig parser
    - 2.6 Samlet
- 3\. Automatisering og regnemaskiner
    - 3.1 Styring af TradeStation og TDE
    - 3.2 Python-regnemaskine: færdig motor eller egen kode?
- 4\. EdgeFinder-protokol, version 3
    - 4.0 Den vigtigste følge af "rejected er endeligt"
    - 4.1 Dataperioder og låsning
    - 4.2 Trin for trin (Lag A – det låste event-studie)
    - 4.3 Lag B – begrænset søgning (kun filtre, der har bestået Lag A)
    - 4.4 Lag C – forbudt, og håndhævet teknisk
    - 4.5 Slippage efter bordets definition
    - 4.6 Filter-identitet – så et dødt filter ikke kan komme tilbage
    - 4.7 Inkubation – følger for EdgeCruncher og kodens fingeraftryk
    - 4.8 Test af selve protokollen, før den bruges
- 5\. Kilder jeg selv har åbnet og læst
- 6\. Nye åbne punkter til Thomas

## Del 3 – Data, dvale-lager og automatisering (Konsulent 3, dybde-runden)

*Konsulent 3 (data-arkitekt): databasen som den er i dag, datamængder, datamodel og dvale-lager, flere computere, drift og plug-and-play.*

- 0\. Kort sammenfatning (de 5 vigtigste nye fund)
- 1\. Kritik ud fra den rigtige kode og de rigtige tabeller
    - 1.1 Sådan ser databasen faktisk ud (læst ud af koden)
    - 1.2 Svage punkter (med fil og linje)
- 2\. Datamængder – regnet trin for trin
    - 2.1 Det eneste målte tal
    - 2.2 Rækker pr. marked og tidsramme (ét "datasæt")
    - 2.3 Bytes pr. række i PostgreSQL (dagens tabelform)
    - 2.4 Plads pr. datasæt og i alt
    - 2.5 Næste led fylder mere, hvis man ikke passer på
    - 2.6 Tid – den egentlige flaskehals
- 3\. Datamodellen for led 1–5 og vejen dertil
    - 3.1 Principper
    - 3.2 Oversigt
    - 3.3 SQL-forslag (kun forslag, ikke kørt)
    - 3.4 Migrationsvej – "ryd op og start forfra", ikke ombygning
- 4\. Fordeling over flere computere
    - 4.1 Hvad licensen tillader – ærligt: UKENDT
    - 4.2 De tre veje og hvad de koster
    - 4.3 Er TDE-fjernstyringen (WM_COMMAND) et fundament at skalere på?
    - 4.4 Kø og fejlsikring (kort, fordi princippet er uændret)
- 5\. Drift på fond-niveau – i projektets målestok
    - 5.1 Backup og gendannelse
    - 5.2 Overvågning
    - 5.3 Reproducerbarhed (at et resultat kan genskabes bit for bit)
    - 5.4 Test og produktion helt adskilt
- 6\. Plug-and-play – hvad Thomas ser og trykker på
- 7\. Vejledning i almindeligt sprog
- 8\. Angreb på mit eget første udkast
- 9\. Uenigheder (vises åbent)
- 10\. Nye åbne punkter til Thomas

## Del 3B – Værktøjer og protokoller til data, drift og automatisering (Konsulent 3, runde 3)

*Konsulent 3: Parquet/DuckDB, kø, backup, betjeningsflade og Det Runde Bords regler håndhævet i databasen.*

- 0\. Kort sagt – anbefalingerne
- 1\. Lagring af råsignaler: PostgreSQL mod Parquet/DuckDB mod TimescaleDB
    - 1.1 Hvad er det?
    - 1.2 Målt på vores egen datamængde
    - 1.3 Hvad betyder det?
    - 1.4 Vurdering
- 2\. Kø og orkestrering
- 3\. Reproducerbarhed og forsøgsregister
- 4\. Backup og drift
- 5\. Betjeningsflade (TradingApp-fanen)
- 6\. Hvad der skal stå i den versionerede metodefil (til K1 og Thomas)
- 7\. Datamodellen efter Det Runde Bord
    - 7.1 Filterets identitet (så et dødt filter ikke kommer igen)
    - 7.2 Statusser: failed og rejected
    - 7.3 Lag C håndhævet teknisk
    - 7.4 De fire datalag – én gang hver, i rækkefølge
    - 7.5 Lag B – antal tests som tal
    - 7.6 Inkubation
    - 7.7 Prisdata fra start – hvad koster det?
- 8\. Nye åbne punkter til Thomas
- 9\. Uenigheder
- 10\. Kilder, jeg selv har åbnet i denne runde
- 7.8 Tilføjet efter kritikrunden (K1 §3.2 og K2 §4.6)
- 7.9 Hvad StepM og placebo kræver af lagring

## Del 4 – Samlet overblik, version 3 (den overordnede agent)

*Den overordnede agent: samlet overblik, værktøjskassen, Fase 0, enighed/uenighed og alle åbne punkter i prioriteret rækkefølge.*

- 4.1 Hvad version 3 ændrede
- 4.2 Værktøjskassen samlet
- 4.3 Fase 0, opdateret: før den fulde kørsel analyseres
- 4.4 EdgeFinder-protokollen: status
- 4.5 Enighed og uenighed
- 4.6 Den overordnede agents egne bemærkninger
- 4.7 Samlet liste over åbne punkter til Thomas (prioriteret)

## Bilag A – Kritik fra runde 2 (dybde-runden)

*Konsulenternes kritik af hinanden i runde 2.*

- K1's kritik af udkast2/k2.md og k3.md
- K2's kritik af K1 og K3 (runde 2)
- K3 – kritik af udkast2/k1.md og udkast2/k2.md

## Bilag B – Kritik fra runde 3 (værktøjskassen)

*Konsulenternes kritik af hinanden i runde 3, herunder K1's godkendelse af EdgeFinder-protokollen.*

- K1's kritik, runde 3
- K2's kritik af K1 og K3 (runde 3)
- K3 – kritik af udkast3/k1.md og udkast3/k2.md
