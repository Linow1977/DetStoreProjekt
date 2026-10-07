# Udtrækning af 4 tilfældige testfiltre til RSA (7. oktober 2026)

Thomas' ønske: fire tilfældige filtre til RSA-testfasen.
- 2 filtre, der kun bruger `Filter1_N1`
- 2 filtre, der bruger både `Filter1_N1` og `Filter1_N2`

Hele listen over de 380 filtre ligger kun i TradingDB (`filter_case`), ikke i
repoet. Udtrækningen skal derfor køres af den lokale session på serveren.

## Regler for udtrækningen

- **Formlens tekst afgør, hvilke parametre filteret bruger** (kolonnerne
  `filter1_n1_*`/`filter1_n2_*` kan være udfyldt, uden at formlen bruger dem;
  se `RawSignal_Creature/BYGGEVEJLEDNING_RawSignal.md` afsnit 2).
- "Kun N1" = `Filter1_N1` står i formlen, og `Filter1_N2` gør ikke.
- "N1 og N2" = begge står i formlen.
- Udtrækningen bruger et fast frø (`setseed`), så den giver samme 4 filtre,
  hver gang den køres. Det gør den efterprøvelig.
- Filtre med de 8 seriefunktioner, der er ramt af eller ikke målt for
  regnefejlen (MACD, RSI, StandardDev, XAverage, DMIplus, DMIminus, ADX,
  ChaikinMoneyFlow), udelades. Ellers kan en RSA-test fejle på grund af
  regnefejlen og ikke på grund af metoden. Average og AvgTrueRange er målt og
  virker og må gerne komme med. (Udelukkelsen afventer Thomas' ja.)

## SQL (kun læsning, ændrer intet)

Køres i én og samme forbindelse, så frøet gælder for udtrækningen.

```sql
-- Fast frø: samme udtrækning hver gang.
select setseed(0.20261007);

with kandidater as (
    select filter_case_id,
           filtere,
           case
               when filtere ilike '%Filter1\_N1%' and filtere not ilike '%Filter1\_N2%' then 'kun N1'
               when filtere ilike '%Filter1\_N1%' and filtere ilike '%Filter1\_N2%'     then 'N1 og N2'
           end as gruppe
    from filter_case
    -- Seriefunktioner, der er ramt af eller ikke målt for regnefejlen, udelades.
    where filtere !~* '\m(MACD|RSI|StandardDev|XAverage|DMIplus|DMIminus|ADX|ChaikinMoneyFlow)\s*\('
),
trukket as (
    select filter_case_id,
           filtere,
           gruppe,
           row_number() over (partition by gruppe order by random()) as nr
    from kandidater
    where gruppe is not null
)
select gruppe, filter_case_id, filtere
from trukket
where nr <= 2
order by gruppe, filter_case_id;
```

SQL'en er ikke afprøvet mod TradingDB fra cloud-sessionen (ingen adgang).
Den lokale session skal vise resultatet til Thomas, før filtrene bruges.

## Resultat

*(Udfyldes af den lokale session: de 4 filter-numre, formler og antal
kombinationer.)*
