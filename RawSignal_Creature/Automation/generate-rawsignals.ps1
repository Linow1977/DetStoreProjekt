# Genererer een .el-fil pr. raekke i filter_case.
#
# Struktur og regler foelger ARBEJDSBESKRIVELSE_RawSignal.md:
#  - Formlen fra databasen indsaettes uaendret; kun Filter1_N1/Filter1_N2
#    erstattes af loekkevariablerne.
#  - Kun de Input og loekker, formlen faktisk bruger, bygges.
#  - Kun de CSV-kolonner, der er relevante for filteret, skrives.
#  - Fast, bogstaveligt filnavn i hvert Print(File(...)) - ingen variabel.
#
# Hver parameter faar TO variabler: en vaerdi og et heltals-indeks.
# Det er noedvendigt, fordi 8 filtre bruger decimaltal (skridt 0,25), og
# et array ikke kan indekseres med et decimaltal. Samme struktur bruges i
# alle filer, saa de ser ens ud uanset om parameteren er hel eller decimal.

param(
  [Parameter(Mandatory=$true)][string]$JsonPath,
  [Parameter(Mandatory=$true)][string]$OutDir,
  [string]$CsvDir = "C:\TradingDB_Folder\FilterFolder\RawSignal.CSV"
)

$ErrorActionPreference = "Stop"

# Array-stoerrelsen foelger den stoerste _end-vaerdi i HELE tabellen (25),
# ikke den enkelte fils egen, saa Fra/Til/Step senere kan haeves.
$ARRAY_SIZE = 25

# Indbyggede seriefunktioner. Kaldes de i en loekke med skiftende
# parametre, kan resultatet blive forkert UDEN fejlmeddelelse - se NOTER.md
# punkt 3. Advarslen skrives i filens hoved, problemet loeses ikke.
$SERIE_FUNKTIONER = @(
  'MACD','RSI','StandardDev','Average','XAverage','DMIplus','DMIminus',
  'ChaikinMoneyFlow','AvgTrueRange','TrueRange','ADX','Momentum',
  'BollingerBand','CCI','Stochastic','WAverage','Summation'
)

$data = Get-Content -Raw -Encoding UTF8 $JsonPath | ConvertFrom-Json
New-Item -ItemType Directory -Path $OutDir -Force | Out-Null

function Er-Decimal($v) {
  if ($null -eq $v) { return $false }
  $d = [decimal]$v
  return ($d -ne [Math]::Truncate($d))
}

function Tal-Tekst($v) {
  # Skriver tal uden unoedvendige nuller: 1 i stedet for 1.00
  $d = [decimal]$v
  if ($d -eq [Math]::Truncate($d)) { return ([int]$d).ToString() }
  return $d.ToString([System.Globalization.CultureInfo]::InvariantCulture)
}

$resultat = @()

foreach ($row in $data) {

  $id      = [int]$row.filter_case_id
  $navn    = "RawSignal{0:D3}" -f $id
  $formel  = ($row.filtere).Trim()
  $formelR = $formel -replace ';\s*$', ''     # afsluttende semikolon fjernes

  $brugerN1 = $formel -imatch 'Filter1_N1'
  $brugerN2 = $formel -imatch 'Filter1_N2'
  $brugerB  = $formel -imatch 'DataFilter_B'

  # Decimal-parametre kraever double i stedet for int.
  $n1Decimal = (Er-Decimal $row.filter1_n1_start) -or (Er-Decimal $row.filter1_n1_end) -or (Er-Decimal $row.filter1_n1_step)
  $n2Decimal = (Er-Decimal $row.filter1_n2_start) -or (Er-Decimal $row.filter1_n2_end) -or (Er-Decimal $row.filter1_n2_step)

  # Formlen med loekkevariabler i stedet for parameternavne.
  $formelKode = $formelR
  $formelKode = [regex]::Replace($formelKode, 'Filter1_N1', 'N1_Vaerdi', 'IgnoreCase')
  $formelKode = [regex]::Replace($formelKode, 'Filter1_N2', 'N2_Vaerdi', 'IgnoreCase')

  $csvSti = Join-Path $CsvDir "$navn.csv"

  # Hvilke seriefunktioner optraeder i formlen?
  $fundne = @()
  foreach ($f in $SERIE_FUNKTIONER) {
    if ($formel -imatch "\b$f\s*\(") { $fundne += $f }
  }
  $fundne = $fundne | Select-Object -Unique

  # ---------- filens hoved ----------
  $h = New-Object System.Text.StringBuilder
  [void]$h.AppendLine("{")
  [void]$h.AppendLine("//***** $navn")
  [void]$h.AppendLine("// Raat signal: registrerer KUN hvornaar filteret taender, og hvor laenge")
  [void]$h.AppendLine("// det er taendt. Ingen handelslogik, ingen analyse.")
  [void]$h.AppendLine("//")
  [void]$h.AppendLine("// Kilde: TradingDB, tabellen filter_case, filter_case_id = $id")
  [void]$h.AppendLine("//")
  [void]$h.AppendLine("// Formel fra databasen (uaendret):")
  foreach ($linje in ($formel -split "`r?`n")) { [void]$h.AppendLine("//   $($linje.Trim())") }
  [void]$h.AppendLine("//")

  if ($brugerN1 -or $brugerN2) {
    $p = @(); if ($brugerN1) { $p += "Filter1_N1" }; if ($brugerN2) { $p += "Filter1_N2" }
    [void]$h.AppendLine("// Parametre som formlen bruger: $($p -join ' og ')")
  } else {
    [void]$h.AppendLine("// Formlen bruger ingen parametre - der findes kun een variant.")
  }
  if ($brugerB) {
    [void]$h.AppendLine("// Formlen bruger to datastroemme: DataFilter_A og DataFilter_B.")
  }
  [void]$h.AppendLine("//")

  if ($fundne.Count -gt 0 -and ($brugerN1 -or $brugerN2)) {
    [void]$h.AppendLine("//")
    [void]$h.AppendLine("// KENDT PROBLEM - LAES DETTE FOER TALLENE BRUGES")
    [void]$h.AppendLine("//")
    [void]$h.AppendLine("// Formlen bruger indbygget(e) seriefunktion(er): $($fundne -join ', ').")
    [void]$h.AppendLine("// Saadanne funktioner husker deres egen forrige vaerdi for at kunne regne")
    [void]$h.AppendLine("// den naeste. TradeStation gemmer den hukommelse eet sted pr. kodelinje -")
    [void]$h.AppendLine("// ikke eet sted pr. parametervaerdi. Naar funktionen kaldes her i en")
    [void]$h.AppendLine("// loekke med mange forskellige laengder, deler alle varianterne den")
    [void]$h.AppendLine("// samme hukommelse.")
    [void]$h.AppendLine("//")
    [void]$h.AppendLine("// Resultatet kan derfor vaere forkert, UDEN at der kommer nogen")
    [void]$h.AppendLine("// fejlmeddelelse. Filen kompilerer, koerer og leverer tal, der ser")
    [void]$h.AppendLine("// rigtige ud. Bemaerk: TradeStation advarer ikke konsekvent om det -")
    [void]$h.AppendLine("// nogle funktioner giver advarsel ved Verify, andre ikke. Fravaer af")
    [void]$h.AppendLine("// advarsel betyder IKKE at filen er fri for problemet.")
    [void]$h.AppendLine("//")
    [void]$h.AppendLine("// Dette er en bevidst beslutning (se NOTER.md punkt 3): risikoen")
    [void]$h.AppendLine("// accepteres for at komme videre, men tal fra parametriserede filtre")
    [void]$h.AppendLine("// boer kontrolleres, foer de laegges til grund for noget.")
    [void]$h.AppendLine("//")
  }

  [void]$h.AppendLine("//")
  [void]$h.AppendLine("// VIGTIGT: Koer som almindelig backtest - IKKE via Optimize.")
  [void]$h.AppendLine("// VIGTIGT: CSV-filen skal vaere lukket i Excel, mens der koeres.")
  [void]$h.AppendLine("// VIGTIGT: Max Bars Back saettes til Auto Detect, eller hoejt nok til")
  [void]$h.AppendLine("//          den laengste beregning i formlen.")
  if ($brugerN1 -or $brugerN2) {
    [void]$h.AppendLine("// VIGTIGT: Arrays herunder rummer $ARRAY_SIZE trin pr. parameter. Giver")
    [void]$h.AppendLine("//          Fra/Til/Step flere end $ARRAY_SIZE trin, SKAL stoerrelsen haeves.")
  }
  [void]$h.AppendLine("}")
  [void]$h.AppendLine("")

  # ---------- Input ----------
  $inputs = @("`tint    DataFilter_A( 2 )")
  if ($brugerB) { $inputs += "`tint    DataFilter_B( 3 )" }
  if ($brugerN1) {
    $t = if ($n1Decimal) { "double" } else { "int   " }
    $inputs += "`t$t N1_Fra( $(Tal-Tekst $row.filter1_n1_start) )"
    $inputs += "`t$t N1_Til( $(Tal-Tekst $row.filter1_n1_end) )"
    $inputs += "`t$t N1_Step( $(Tal-Tekst $row.filter1_n1_step) )"
  }
  if ($brugerN2) {
    $t = if ($n2Decimal) { "double" } else { "int   " }
    $inputs += "`t$t N2_Fra( $(Tal-Tekst $row.filter1_n2_start) )"
    $inputs += "`t$t N2_Til( $(Tal-Tekst $row.filter1_n2_end) )"
    $inputs += "`t$t N2_Step( $(Tal-Tekst $row.filter1_n2_step) )"
  }
  [void]$h.AppendLine("Input:")
  [void]$h.AppendLine((($inputs -join ",`r`n") + ";"))
  [void]$h.AppendLine("")

  # ---------- Arrays / Var ----------
  $dim = ""
  if ($brugerN1 -and $brugerN2) { $dim = "[$ARRAY_SIZE,$ARRAY_SIZE]" }
  elseif ($brugerN1 -or $brugerN2) { $dim = "[$ARRAY_SIZE]" }

  if ($dim -ne "") {
    [void]$h.AppendLine("// Een plads pr. trin. Indekset taelles 1, 2, 3 ... uafhaengigt af")
    [void]$h.AppendLine("// parameterens vaerdi, saa decimal-skridt ogsaa kan bruges.")
    [void]$h.AppendLine("Arrays:")
    [void]$h.AppendLine("`tint    Filter1$dim( 0 ),")
    [void]$h.AppendLine("`tint    Filter1_Forrige$dim( 0 ),")
    [void]$h.AppendLine("`tint    SignalBars$dim( 0 ),")
    [void]$h.AppendLine("`tstring StartTekst$dim( `"`" );")
    [void]$h.AppendLine("")
  }

  $vars = @()
  if ($brugerN1) {
    $t = if ($n1Decimal) { "double" } else { "int   " }
    $vars += "`t$t N1_Vaerdi( 0 )"
    $vars += "`tint    N1_Indeks( 0 )"
  }
  if ($brugerN2) {
    $t = if ($n2Decimal) { "double" } else { "int   " }
    $vars += "`t$t N2_Vaerdi( 0 )"
    $vars += "`tint    N2_Indeks( 0 )"
  }
  if ($dim -eq "") {
    $vars += "`tint    Filter1( 0 )"
    $vars += "`tint    Filter1_Forrige( 0 )"
    $vars += "`tint    SignalBars( 0 )"
    $vars += "`tstring StartTekst( `"`" )"
  }
  $vars += "`tstring BarTekst( `"`" )"
  [void]$h.AppendLine("Var:")
  [void]$h.AppendLine((($vars -join ",`r`n") + ";"))
  [void]$h.AppendLine("")

  # ---------- CSV-kolonner ----------
  $kol = @("RunID")
  if ($brugerN1) { $kol += "N1" }
  if ($brugerN2) { $kol += "N2" }
  $kol += @("Starttid","AntalBars")
  $overskrift = $kol -join ","

  [void]$h.AppendLine("")
  [void]$h.AppendLine("//----- Engangsopsaetning: nulstil filen og skriv overskriftsraekke -----//")
  [void]$h.AppendLine("")
  [void]$h.AppendLine("`tOnce")
  [void]$h.AppendLine("`t`tBegin")
  [void]$h.AppendLine("`t`tFileDelete( `"$csvSti`" );")
  [void]$h.AppendLine("`t`tPrint( File(`"$csvSti`"), `"$overskrift`" );")
  [void]$h.AppendLine("`t`tEnd;")
  [void]$h.AppendLine("")
  [void]$h.AppendLine("")
  [void]$h.AppendLine("//----- Tidsstempel for den aktuelle bar -----//")
  [void]$h.AppendLine("")
  [void]$h.AppendLine("`tBarTekst = FormatDate( `"yyyy-MM-dd`", ELDateToDateTime( Date of data(DataFilter_A) ) )")
  [void]$h.AppendLine("`t         + `" `"")
  [void]$h.AppendLine("`t         + FormatTime( `"HH:mm`", ELTimeToDateTime( Time of data(DataFilter_A) ) );")
  [void]$h.AppendLine("")
  [void]$h.AppendLine("")

  # ---------- selve kroppen ----------
  $idx = ""
  if ($brugerN1 -and $brugerN2) { $idx = "[N1_Indeks,N2_Indeks]" }
  elseif ($brugerN1) { $idx = "[N1_Indeks]" }
  elseif ($brugerN2) { $idx = "[N2_Indeks]" }

  # Vaerdierne som skrives i CSV-linjen
  $vaerdiFelter = @()
  if ($brugerN1) {
    $dec = if ($n1Decimal) { 2 } else { 0 }
    $vaerdiFelter += "`t`t`t`t     + NumToStr( N1_Vaerdi, $dec ) + `",`""
  }
  if ($brugerN2) {
    $dec = if ($n2Decimal) { 2 } else { 0 }
    $vaerdiFelter += "`t`t`t`t     + NumToStr( N2_Vaerdi, $dec ) + `",`""
  }

  $krop = New-Object System.Text.StringBuilder
  [void]$krop.AppendLine("`t`t`t// Selve filteret - formlen fra databasen, uaendret")
  [void]$krop.AppendLine("`t`t`tIf $formelKode Then")
  [void]$krop.AppendLine("`t`t`t`tFilter1$idx = 1")
  [void]$krop.AppendLine("`t`t`tElse")
  [void]$krop.AppendLine("`t`t`t`tFilter1$idx = 0;")
  [void]$krop.AppendLine("")
  [void]$krop.AppendLine("`t`t`t// TAENDER")
  [void]$krop.AppendLine("`t`t`tIf Filter1$idx = 1 and Filter1_Forrige$idx = 0 Then")
  [void]$krop.AppendLine("`t`t`t`tBegin")
  [void]$krop.AppendLine("`t`t`t`tStartTekst$idx = BarTekst;")
  [void]$krop.AppendLine("`t`t`t`tSignalBars$idx = 1;")
  [void]$krop.AppendLine("`t`t`t`tEnd;")
  [void]$krop.AppendLine("")
  [void]$krop.AppendLine("`t`t`t// FORTSAETTER")
  [void]$krop.AppendLine("`t`t`tIf Filter1$idx = 1 and Filter1_Forrige$idx = 1 Then")
  [void]$krop.AppendLine("`t`t`t`tSignalBars$idx = SignalBars$idx + 1;")
  [void]$krop.AppendLine("")
  [void]$krop.AppendLine("`t`t`t// SLUKKER - linjen skrives her")
  [void]$krop.AppendLine("`t`t`tIf Filter1$idx = 0 and Filter1_Forrige$idx = 1 Then")
  [void]$krop.AppendLine("`t`t`t`tBegin")
  [void]$krop.AppendLine("`t`t`t`tPrint( File(`"$csvSti`"),")
  [void]$krop.AppendLine("`t`t`t`t       `"$navn`" + `",`"")
  foreach ($vf in $vaerdiFelter) { [void]$krop.AppendLine($vf) }
  [void]$krop.AppendLine("`t`t`t`t     + StartTekst$idx + `",`"")
  [void]$krop.AppendLine("`t`t`t`t     + NumToStr( SignalBars$idx, 0 ) );")
  [void]$krop.AppendLine("`t`t`t`tSignalBars$idx = 0;")
  [void]$krop.AppendLine("`t`t`t`tEnd;")
  [void]$krop.AppendLine("")
  [void]$krop.AppendLine("`t`t`tFilter1_Forrige$idx = Filter1$idx;")

  $kropTekst = $krop.ToString().TrimEnd()

  if (-not $brugerN1 -and -not $brugerN2) {
    # Ingen loekke - fjern den ekstra indrykning
    [void]$h.AppendLine("//----- Filter og signal-registrering -----//")
    [void]$h.AppendLine("")
    foreach ($l in ($kropTekst -split "`r?`n")) {
      [void]$h.AppendLine(($l -replace '^\t\t\t', "`t"))
    }
  }
  else {
    [void]$h.AppendLine("//----- Alle trin gennemloebes paa hver bar -----//")
    [void]$h.AppendLine("")
    if ($brugerN1) {
      [void]$h.AppendLine("`tN1_Vaerdi = N1_Fra;")
      [void]$h.AppendLine("`tN1_Indeks = 1;")
      [void]$h.AppendLine("`tWhile N1_Vaerdi <= N1_Til")
      [void]$h.AppendLine("`t`tBegin")
      [void]$h.AppendLine("")
    }
    if ($brugerN2) {
      $pre = if ($brugerN1) { "`t`t" } else { "`t" }
      [void]$h.AppendLine("$($pre)N2_Vaerdi = N2_Fra;")
      [void]$h.AppendLine("$($pre)N2_Indeks = 1;")
      [void]$h.AppendLine("$($pre)While N2_Vaerdi <= N2_Til")
      [void]$h.AppendLine("$pre`tBegin")
      [void]$h.AppendLine("")
    }

    # Kroppen indrykkes efter hvor dybt vi er
    $dybde = 0; if ($brugerN1) { $dybde++ }; if ($brugerN2) { $dybde++ }
    foreach ($l in ($kropTekst -split "`r?`n")) {
      if ($dybde -eq 1) { [void]$h.AppendLine(($l -replace '^\t\t\t', "`t`t")) }
      else { [void]$h.AppendLine($l) }
    }
    [void]$h.AppendLine("")

    if ($brugerN2) {
      $pre = if ($brugerN1) { "`t`t" } else { "`t" }
      [void]$h.AppendLine("$pre`tN2_Vaerdi = N2_Vaerdi + N2_Step;")
      [void]$h.AppendLine("$pre`tN2_Indeks = N2_Indeks + 1;")
      [void]$h.AppendLine("$pre`tEnd;")
    }
    if ($brugerN1) {
      [void]$h.AppendLine("")
      [void]$h.AppendLine("`t`tN1_Vaerdi = N1_Vaerdi + N1_Step;")
      [void]$h.AppendLine("`t`tN1_Indeks = N1_Indeks + 1;")
      [void]$h.AppendLine("`t`tEnd;")
    }
  }

  $sti = Join-Path $OutDir "$navn.el"
  Set-Content -Path $sti -Value $h.ToString() -Encoding UTF8 -NoNewline

  $type = if ($brugerN1 -and $brugerN2) { "N1+N2" } elseif ($brugerN1) { "N1" } elseif ($brugerN2) { "N2" } else { "ingen" }
  $resultat += [pscustomobject]@{
    Id = $id; Navn = $navn; Type = $type
    Decimal = ($n1Decimal -or $n2Decimal)
    DataB = $brugerB
    Serie = ($fundne -join '/')
  }
}

Write-Output "Genereret: $($resultat.Count) filer i $OutDir"
Write-Output ""
Write-Output "Fordeling paa parametertype:"
$resultat | Group-Object Type | Sort-Object Count -Descending | ForEach-Object { "  {0,-8} {1}" -f $_.Name, $_.Count }
Write-Output ""
Write-Output "Med decimal-parametre: $(($resultat | Where-Object Decimal).Count)"
Write-Output "Med DataFilter_B:      $(($resultat | Where-Object DataB).Count)"
Write-Output "Uden seriefunktion:    $(($resultat | Where-Object { $_.Serie -eq '' }).Count)"
