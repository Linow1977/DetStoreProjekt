# Koerer et bundt .el-filer gennem TradeStation og skriver resultatet i
# TradingDB, tabellen public.rawsignal.
#
# Princip (jf. OPGAVEBESKRIVELSE_Automation.md):
#  - Filer der allerede staar i rawsignal springes over. Det er ogsaa det,
#    der forhindrer forsoeg paa at oprette en strategi, hvis navn findes i
#    forvejen - den fejl efterlod tidligere TSDev i en uforudsigelig tilstand.
#  - En fejlende fil stopper ALDRIG koerslen. Den noteres og der gaas videre.
#  - Alt logges undervejs, ikke kun til sidst.

param(
  [Parameter(Mandatory=$true)][int]$MainHwnd,
  [Parameter(Mandatory=$true)][int]$ProcId,
  [string]$ElDir   = "C:\TradingDB_Folder\FilterFolder\RawSignal.EL",
  [string]$Filter  = "RawSignal[0-9][0-9][0-9].el",
  [int]$Start      = 0,        # spring de foerste N filer over
  [int]$Antal      = 0,        # 0 = alle
  [switch]$Genkoer             # medtag ogsaa filer der allerede staar i rawsignal
)

$ErrorActionPreference = "Stop"
$psql = "C:\Program Files\PostgreSQL\18\bin\psql.exe"
$ps32 = "C:\Windows\SysWOW64\WindowsPowerShell\v1.0\powershell.exe"
$here = $PSScriptRoot

function Db-Query([string]$sql) {
  $r = & $psql -h 127.0.0.1 -U postgres -d TradingDB -w -t -A -c $sql 2>&1
  if ($LASTEXITCODE -ne 0) { throw "Databasefejl: $r" }
  return $r
}

# Kendte navne i tabellen - bruges til at springe over.
$kendte = @{}
if (-not $Genkoer) {
  foreach ($n in (Db-Query "select rawsignal_name from public.rawsignal;")) {
    if ($n -and $n.Trim() -ne "") { $kendte[$n.Trim()] = $true }
  }
}
Write-Output "Allerede i rawsignal-tabellen: $($kendte.Count)"

$filer = Get-ChildItem (Join-Path $ElDir $Filter) | Sort-Object Name
if ($Start -gt 0) { $filer = $filer | Select-Object -Skip $Start }
if ($Antal -gt 0) { $filer = $filer | Select-Object -First $Antal }
Write-Output "Filer i dette bundt: $($filer.Count)"
Write-Output ""

$ok = 0; $fejl = 0; $sprunget = 0
$fejlListe = @()

foreach ($f in $filer) {
  $navn = $f.BaseName

  if ($kendte.ContainsKey($navn)) {
    $sprunget++
    Write-Output ("{0}  SPRUNGET OVER (staar allerede i rawsignal)" -f $navn)
    continue
  }

  $json = & $ps32 -NoProfile -ExecutionPolicy Bypass -File "$here\verify-one.ps1" `
            -MainHwnd $MainHwnd -ProcId $ProcId -ElPath $f.FullName 2>&1

  $res = $null
  try { $res = ($json | Where-Object { $_ -match '^\{' } | Select-Object -First 1) | ConvertFrom-Json } catch { }

  if ($null -eq $res) {
    $fejl++; $fejlListe += $navn
    Write-Output ("{0}  FEJLET (uventet svar: {1})" -f $navn, ($json -join ' '))
    continue
  }

  # Skriv resultatet i databasen. Note og sti gemmes ogsaa ved fejl.
  $note = ($res.Note -replace "'", "''")
  $sql = @"
insert into public.rawsignal (rawsignal_name, dev_date, signal_path, verification, note)
values ('$navn', now(), '$($f.FullName -replace "'","''")', '$($res.Resultat)', '$note')
on conflict (rawsignal_name) do update
  set dev_date = excluded.dev_date,
      signal_path = excluded.signal_path,
      verification = excluded.verification,
      note = excluded.note;
"@
  try { Db-Query $sql | Out-Null }
  catch { Write-Output ("{0}  ADVARSEL: kunne ikke skrives i databasen: {1}" -f $navn, $_) }

  if ($res.Resultat -eq "OK") {
    $ok++
    Write-Output ("{0}  OK      {1}" -f $navn, $res.Note)
  } else {
    $fejl++; $fejlListe += $navn
    Write-Output ("{0}  FEJLET  {1}" -f $navn, $res.Note)
  }
}

Write-Output ""
Write-Output "===== OPSUMMERING ====="
Write-Output "OK:            $ok"
Write-Output "Fejlet:        $fejl"
Write-Output "Sprunget over: $sprunget"
if ($fejlListe.Count -gt 0) {
  Write-Output "Fejlende filer: $($fejlListe -join ', ')"
}
