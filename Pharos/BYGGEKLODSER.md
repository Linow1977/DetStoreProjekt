# Pharos — gratis byggeklodser

Liste over færdige, gratis byggeklodser, som Pharos kan låne i stedet for at
skrive alt selv. Samlet 2026-10-12 ud fra undersøgelsen
`reports/Alternativer til Titan for futures.md`; detaljer og kilder står i
`research_notes/Alternativer til Titan for futures/byg_selv_og_praksis.md`.

**Intet er installeret eller valgt endnu.** Listen er et udgangspunkt, ikke en
beslutning.

## Hvor findes de

- **PyPI** (pypi.org) er "app-butikken" for programmeringssproget Python.
  RawSignal-programmerne er allerede skrevet i Python, så serveren kan hente en
  byggeklods med én kommando, fx `pip install ffn`.
- Selve koden ligger åbent på **GitHub**, så alle kan se, hvordan der regnes.

## Anbefalede byggeklodser

Versioner og licenser er tjekket på PyPI 2026-10-12.

| Byggeklods | Hvad den gør for Pharos | Version (dato) | Licens | Hvor |
|---|---|---|---|---|
| **ffn** | Nøgletal pr. strategi (gevinst, nedture, Sharpe), lige risikofordeling, klynger af ens strategier, test for overtilpasning | 1.4.1 (2026-10-10) | MIT | [pypi.org/project/ffn](https://pypi.org/project/ffn/) |
| **quantstats** | Nøgletal og færdige rapporter; Monte Carlo for nedturens dybde (se fælden nedenfor) | 0.0.86 (2026-09-27) | Apache-2.0 | [pypi.org/project/quantstats](https://pypi.org/project/quantstats/) |
| **Riskfolio-Lib** | Porteføljer, risikoparitet, risikomål baseret på nedture | 7.4.0 (2026-10-04) | BSD-3 | [pypi.org/project/Riskfolio-Lib](https://pypi.org/project/Riskfolio-Lib/) |
| **skfolio** | Samme område som Riskfolio-Lib; alternativ | 1.8.5 (2026-10-12) | BSD-3 | [pypi.org/project/skfolio](https://pypi.org/project/skfolio/) |
| **arch** | Blok-bootstrap (Monte Carlo, der bevarer sammenhængen mellem nabodage) til forventningsbåndene | 8.0.0 (2025-10-21) | NCSA (BSD-lignende) | [pypi.org/project/arch](https://pypi.org/project/arch/) |
| **Grafana** | Grafer og alarmer direkte på PostgreSQL-databasen, "altid tændt"-overblik | — | AGPL-3.0 | [grafana.com](https://grafana.com/) |
| **Streamlit** | Hurtig side med knapper, fx Godkend/Afvis af månedslisten | 1.65.0 (2026-10-02) | Apache-2.0 | [pypi.org/project/streamlit](https://pypi.org/project/streamlit/) |
| **Dash** | Som Streamlit, mere kontrol over udseendet | 4.4.1 | MIT | [pypi.org/project/dash](https://pypi.org/project/dash/) |
| **Healthchecks.io** | "Jeg lever"-tjeneste: alarm, når handelscomputeren holder op med at melde sig | — | Tjeneste på nettet (gratis udgave findes; priser ikke tjekket) | [healthchecks.io](https://healthchecks.io/) |

Mulig opdeling (researchernes vurdering): Grafana til den daglige vagt og
alarmer; Streamlit eller Dash til månedslisten med Godkend/Afvis.

## Godt at vide

- **Licenser:** MIT, Apache og BSD må bruges frit, også kommercielt. Grafana
  (AGPL) er fint til intern brug; kun hvis man ændrer i Grafana selv og giver
  den til andre over nettet, skal ændringerne deles.
- **Futures:** ingen af byggeklodserne er lavet til futures. De regner med
  procentafkast, så Pharos selv skal omregne kontrakter, tick-værdier og dollars.
- **Fælde i quantstats:** dens Monte Carlo blander kun rækkefølgen af de samme
  dage. Den kan vise, hvor dyb en nedtur kan blive, men ikke hvordan året ender.
  Brug `arch` til det.

## Undgå

| Pakke | Hvorfor |
|---|---|
| empyrical | Ikke opdateret siden 2020 |
| pyfolio | Ikke opdateret siden 2019 |
| recombinator | Ikke opdateret siden 2022 |
| empyrical-reloaded, pyfolio-reloaded | Virker, men ingen ny udgave siden 2025-06; kun hvis en funktion ikke findes andre steder |

(vectorbt er ikke på listen, fordi Pharos ikke skal backteste. Dens licens
forbyder kun at sælge et produkt, der primært er vectorbt; intern brug er fint.)
