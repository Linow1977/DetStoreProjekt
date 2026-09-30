# Laboratoriet fra konsulentgruppen (29. september 2026)

Her ligger de små programmer, som konsulenterne brugte til at afprøve deres forslag, og det, programmerne svarede. De hører til `Rapport_konsulentgruppen_2026-09-29.docx` og `Pharos_udkast_2026-09-29.docx` i mappen ovenover.

**Vigtigt:**
- Alt er kørt på **opdigtede data**. Programmerne viser, om metoderne opfører sig som tænkt. De siger intet om, hvorvidt de rigtige filtre har en fordel.
- Intet program rører TradingDB, TradeStation eller rigtige priser.
- Dette er afprøvning og prototyper, ikke færdige værktøjer. De rigtige værktøjer skal bygges efter byggeplanen i rapportens del 2.

## Sådan køres det

```
python -m venv venv
venv/bin/pip install -r requirements.txt
cd K2
../venv/bin/python -m unittest -v test_rsa_proto test_pharos_proto
```

Hvert forsøg køres med `python <fil>.py` inde fra sin egen mappe. Resultatet skrives på skærmen og svarer til den tilhørende `*_resultat.txt` eller `resultater*.txt`. Tilfældigheden styres af faste frø (seeds), så tallene er de samme hver gang.

Enkelte forsøg hos K3 (F2, F3 og F5) laver opdigtede testdata i undermapper som `f2_ud/`. Dem skal man ikke lægge i git.

Status ved gemning: prototypen til RSA består 20 af 20 tests, og Pharos-prototypen består 8 af 8.

## K1: statistikeren (metodeafprøvning, rapportens del 1 afsnit Q)

| Fil | Hvad forsøget spørger om |
|---|---|
| `f1_klumpning.py` | Hvor meget ser resultaterne for sikre ud, når man tæller signaler i stedet for dage? (1,4-4,6 gange) |
| `f2_oos_regel.py` | Fast 10/20 % mod "støj-enheder" som grænse for, hvor meget et resultat må falde i OOS |
| `f3_plateau_stoej.py`, `plateau.py` | Hvor tit giver ren støj et plateau (PL1-PL7)? `plateau.py` er fælles hjælpekode |
| `f4_hele_tragten.py` | Hele vejen igennem: lokkeduer, FDR, plateau og OOS på ca. 1,8 mio. kandidater |
| `f5_styrke_og_oos.py` | Finder porten de ægte edges, og hvad koster grøn-reglen? |
| `f6_hale_faa_dage.py`, `f6b_mild_skaevhed.py` | Hvor tit narrer skæve dagsresultater t-tallet? |
| `f7_skaevhed_vaern.py`, `f7b_tom_taerskel.py` | Hvilket værn virker mod skæve resultater (lille target, stort stop)? |
| `f8_repraesentant.py` | Skal plateauets midte eller cellen med højest t prøves i OOS? |
| `f9_b5_stabilitet.py`, `f9b_bedste_aar.py` | Hvad fanger stabilitetskravet B5, og skal grænsen for "bedste år" være 40 eller 50 %? |
| `f10_lokkedue_realistisk.py` | Virker lokkeduerne også på et mere realistisk opdigtet marked? |
| `f11_overskud.py` | Hjælper det at måle mod det, der normalt sker på samme klokkeslæt? |
| `f12_plateau_niveauer.py` | Hvilket plateau-niveau når ægte edges af forskellig bredde? |
| `f13_identiske_celler.py` | Regnefejlen i TradeStation: ens celler ligner et perfekt plateau. Fanger kontrollen det? |
| `f14_vaerdistabilitet.py` | Et mildere krav om værdi-stabilitet (de 8 nærmeste naboer) |
| `f15_pharos_pause.py`, `f15b_pharos_regelsaet.py` | Pharos: hvor tit sættes en god strategi på pause eller pensioneres ved en fejl? |
| `f16_momentum_mod_1N.py` | Pharos: slår Titan-agtig udvælgelse efter seneste resultat "samme risiko til alle"? |

## K2: pipeline-/analyseudvikleren (prototyper, rapportens del 2 afsnit 12 og Pharos-udkastet afsnit 7)

| Fil | Indhold |
|---|---|
| `rsa_proto.py` | Prototype af RSA-kæden: bars fra 1-minuts data, event-motor, dagstal, farver, plateau, lokkeduer og kontrol af identiske celler |
| `test_rsa_proto.py` | 20 tests med kendt svar til prototypen |
| `exitmotor.py` | Prototype af Edge-Finders exit-motor (stop, target og tid, minut for minut) |
| `mutationstest.py` | Indsætter 4 fejl med vilje og tjekker, at testene fanger dem |
| `forsoeg.py` … `forsoeg9.py`, `forsoeg3b.py`, `forsoeg5b_drift.py` | Forsøg F1-F14: bl.a. fremtidsviden, nabo-celler, lokkedue-FDR, dybt-test, skæve exits og identiske celler |
| `pharos_proto.py`, `test_pharos_proto.py` | Prototype af Pharos' månedlige beregning med 8 tests |
| `pharos_forsoeg.py`, `pharos_blok.py` | PF1 (momentum mod "alle lige") og PF2 (blokstørrelse for lokkeduer) |
| `resultater*.txt` | Output fra forsøgene |

## K3: data-arkitekten (afprøvet i DuckDB, rapportens del 3 afsnit 15b)

| Fil | Hvad forsøget spørger om |
|---|---|
| `f1_stoerrelse.py` | Hvor meget fylder én million signal-linjer som CSV og som Parquet? |
| `f2_skema_og_laase.py` | Holder låsene: afvises 2025-data i testlaget, og kan OOS-porten kun åbnes én gang? |
| `f3_nedbrud_og_forfra.py` | Ryd op og kør forfra efter et nedbrud: giver det samme resultat? |
| `f4_mapper_og_glob.py` | Kan mappestrukturen uforvarende blande perioder? |
| `f5_jobkoe.py` | Jobkøens regler for flere arbejdere, der kan gå ned undervejs |
| `f6_genberegning_og_taelle.py` | Giver en ny udregning præcis samme tal? (Nej, med kommatal. Derfor bruges hele tal) |
| `f7_runde_og_tvilling.py` | Én samlet OOS-runde med skjulte tal og lås mod "tvilling"-filtre |

Roller, rettigheder og automatiske regler i en rigtig PostgreSQL er ikke afprøvet her. De skal afprøves i en tom testdatabase (køreplanens trin 2), før TradingDB ændres.
