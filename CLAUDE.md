# CLAUDE.md — Sådan skal Claude Code arbejde i alle projekter

## Om Thomas
Thomas er ikke programmer. Al forklaring skal være i almindeligt sprog, uden at antage kendskab til kode eller tekniske begreber. 
Thomas er ikke programmør så spørgsmål og svar skal forklares så et barn kan forstå det.

## Arbejdsregler (gælder altid)
- Tænk før der skrives kode — planlæg først, byg bagefter
- Spørg ved usikkerhed — gæt aldrig på hvad Thomas mener
- Lav kirurgiske ændringer — rør ikke ved kode der ikke er relateret til den aktuelle opgave
- Kommuniker på dansk

## Kodestandard
- Skriv koden så en professionel programmør kan læse og overtage den uden forklaring.
- Fast, ensartet struktur på tværs af alle filer (samme opbygning, samme navngivningsmønster for filer/funktioner/variabler)
- Klare kommentarer der forklarer *hvorfor*, ikke kun *hvad*
- Følg almindelige branche-konventioner for det sprog der bruges
- Undgå "smarte" eller kompakte genveje, der er svære at læse — klarhed vinder over kortfattethed
- Del store opgaver op i mindre, veldefinerede filer/funktioner frem for én stor blok kode

## Før en opgave startes
- Læs den vedhæftede/uploadede plan-fil grundigt, før noget bygges
- Hvis planen er uklar eller mangler noget vigtigt, spørg Thomas først
- **Tjek `VIDENSLOG.md` for relevant viden om det, der skal arbejdes med**
  (og evt. delprojektets egen `NOTER.md`), før arbejdet går i gang — så
  tidligere fejl og beslutninger ikke gentages. Dette er den anden halvdel
  af selv-forbedringen: viden skal både skrives ned og slås op igen.

## Før en opgave afsluttes
- Test at det virker, før det kaldes "færdigt" — vis testen til Thomas
- Forklar i almindeligt sprog hvad der er lavet
- Nævn eksplicit hvis noget er udeladt eller ikke kunne løses som planlagt

## Hvis noget går ud over opgavens rammer
- Stop og spørg først — udvid ikke omfanget på egen hånd

## Videnslog (gælder alle sessioner, lokal og cloud)
- `VIDENSLOG.md` i roden af projektet er den centrale hukommelse for vigtig
  viden — tekniske fælder, beslutninger og hvorfor, markeds-/strategi-
  indsigt, åbne tråde.
- **Læs den, før en opgave startes** (se "Før en opgave startes" ovenfor) —
  ikke kun bagefter. Uden det led er filen bare en logbog, ikke noget der
  gør fremtidige sessioner bedre.
- Når en opgave afsluttes og der er lært noget vigtigt undervejs, tilføj en
  kort post under den relevante kategori i `VIDENSLOG.md` (se filens egen
  "Sådan bruges filen"-afsnit for format).
- Findes kategorien (delprojektet) ikke endnu, opret den selv — men sig det
  tydeligt til Thomas i samme omgang.
- Detaljerede tekniske noter hører til i det enkelte delprojekts egen mappe;
  i Videnslog skrives kun det korte, tværgående resumé.

## Mål
- skabe fundamentet for en privat daytrading hedge-fund bygget op omkring et fuldautomatisk strategiudviklingssystem baseret på teknisk analyse og prisdata
## Ambitionsniveau 
- skal ligge på niveau med nogle af verdens bedste hedge-fonde inden for samme type

## Selv-forbedring — afgørende for at nå ambitionsniveauet
Ambitionsniveauet ovenfor nås ikke ved at gøre det samme igen og igen. Både
Claude Code og chat skal **hele tiden blive bedre** til det, der arbejdes
med — det skal have stort, vedvarende fokus, ikke være en engangsting.

Det dækker to ting, ikke kun én:
1. **Faglig viden** — det vi lærer om trading, data, EasyLanguage,
   arkitektur osv. Håndteres af `VIDENSLOG.md` (se afsnittet "Videnslog"
   ovenfor): læses før en opgave startes, opdateres efter.
2. **Arbejdsmåde** — hvordan selve arbejdet gribes an. Gik noget langsomt?
   Blev noget misforstået, som et bedre spørgsmål kunne have fanget
   tidligere? Var en antagelse forkert? Den slags læring hører også til i
   `VIDENSLOG.md`, under den tværgående kategori
   "DetStoreProjekt (tværgående/generelt)" — ikke kun fagligt indhold om
   selve trading-systemet, men også om hvordan Claude arbejder bedre med
   Thomas og med projektet.
