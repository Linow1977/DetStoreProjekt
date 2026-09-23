# Notat til BYGGEVEJLEDNING_RawSignal.md

23. september 2026. Ja, vejledningen har brug for rettelser. Punkterne herunder er ordnet efter
vejledningens egne afsnit. Dette notat er ikke en ny vejledning. Det er en liste over, hvad der skal
rettes eller tilføjes. Den fulde beskrivelse står i `OPGAVEBESKRIVELSE_RawSignal.md`.

## Fejl der skal rettes

**Punkt 7, "det er målt":**
- Antal signaler i RawSignal069 står som 480. Hele filen er målt: 4.918 signaler pr. kombination, og
  alle 625 kombinationer er identiske (4.918 x 625 = 3.073.750 linjer). Konklusionen (parametersøgningen
  er værdiløs for 069) holder. Skriv fremover, om et tal kommer fra hele filen eller fra et udsnit.
- Tabellen med advarsler ved Verify påstår, at `RawSignal266` har "nøjagtig samme problem som 069".
  Det er modbevist: alle 25 N1-værdier giver forskellige signaler (528 til 1.453 pr. N1). Ret 266 til
  "målt, virker sandsynligvis". `RawSignal004_Test` og `RawSignal020` er ikke målt, og det skal stå.
- `Average` står på listen over funktioner med hukommelsesproblem. Tag den ud, indtil en kontrolkørsel
  (én kombination alene mod samme kombination i løkken) har afgjort det.
- Sætningen om, at fravær af advarsel ikke betyder, at en fil er i orden, kan blive stående, men kun to
  løkke-filer er målt. Det er for lidt til at sige noget sikkert om advarslerne.

**Punkt 13, status:**
- `RawSignal266` er kørt og giver forskellige signaler pr. N1 (ikke længere "ikke rapporteret").
- `RawSignal069_MedPlot` og `RawSignal332_MedPlot` udgår (se punkt 10 herunder).

## Ændringer der følger af nye beslutninger

**Punkt 1 (hvad en RawSignal-fil skal gøre):**
- `AntalBars` tælles i Data2-bars. I dag er Data1 og Data2 lige store, så den nuværende kode tæller
  rigtigt. Bliver Data1 senere mindre, tæller den forkert. Strategien skal mindst stoppe med en fejl
  i det tilfælde.
- Et signal, der stadig er tændt ved slutningen, ignoreres bevidst. Formuleringen "højst én manglende
  linje" er en beskrivelse, ikke en beslutning. Skriv, at det er besluttet.

**Punkt 5 (filnavne og CSV):**
- Filen flyttes af næste trin (EdgeFinder / RawSignal-Analysis) og skal være flyttet, før samme filter
  køres igen. `FileDelete` sletter ellers den gamle fil uden fejlmelding.
- `RunID` er filterets navn, ikke kørslen. Kørslen står kun i mappenavnet.

**Punkt 10 (plot) skal skrives om:**
- Nu står, at en ShowMe både tegner og skriver CSV, med en `SkrivCSV`-kontakt og en prik på hver sand
  bar. Det gælder ikke længere.
- Nu: der laves en separat `_Kontrol`-ShowMe pr. filter, som KUN tegner. Ingen CSV, ingen `FileDelete`.
- Plot1 er aktiveringen (falsk til sand). Fortsættelsen er valgfri i Plot2.
- `RawSignal069_MedPlot` og `RawSignal069ShowMe.csv` var en engangsting og er ikke en del af systemet.

**Punkt 12 (tabeller):**
- Tilføj den nye tabel `RawSignal_Kontrol` (PostgreSQL: `rawsignal_kontrol`) til `_Kontrol`-filerne,
  med samme kolonner som `rawsignal`. Strategifilerne bruger stadig `rawsignal`.
- Navne skal være unikke for begge filtyper, og programmet skal slå op i tabellen først.

**Nyt afsnit: to filer pr. filter:**
- Programmet laver en strategi og en `_Kontrol`-ShowMe ud fra samme række i `Filter_Case`. Kun
  `Filter_Case` ændres, filerne rettes aldrig i hånden, og formelteksten skal være ordret ens.
- ShowMe'en åbnes i TDE med Alt+Ctrl+M.

## Ting der ikke skal ændres

- Punkt 3 og 4 (strukturerne og skabelonen).
- Punkt 6 (Max Bars Back) og punkt 8 (Verify er ikke bevis).
- Punkt 11 (formlen ind ordret, Optimize må ikke bruges, CSV lukket i Excel).
- Værdi/plads-opdelingen må stadig kun bruges i de 8 filtre med decimaltal.

## Skal Thomas afgøre først

Vejledningen bør ikke skrives færdig på disse punkter, før de er afgjort:
- Hvilken vej de 304 parametriserede filtre skal tage (punkt 7).
- Hvilken mappe `_Kontrol`-filerne ligger i.
- Om tabellen til strategifilen skal omdøbes.
