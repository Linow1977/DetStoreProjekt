# Verificerer EEN .el-fil i TradeStation Development Environment.
#
# Arbejdsgang (den manuelt bekraeftede, jf. OPGAVEBESKRIVELSE_Automation.md):
#   New Strategy / New ShowMe -> navngiv -> indsaet tekst -> Verify (F3)
#   -> laes Output-panelet -> luk dokumentet
#
# Resultatet er Pass eller Fail (samme ord som i tabellerne rawsignal og
# rawsignal_kontrol). Kan selve automationen ikke gennemfoeres, er
# resultatet Afbrudt - saa er filen IKKE verificeret, og der skal ikke
# skrives noget i databasen.
#
# Der bruges INGEN tastetryk. TDE's menukommandoer sendes direkte til
# vinduet som WM_COMMAND (numrene er laest fra TDE's egne menuer), og navn
# og kode saettes med Windows-beskeder. Derfor virker det ogsaa, naar
# fjernskrivebordet er minimeret, og det tager ikke fokus fra brugeren.
# (Tastetryk fejlede 24-09-2026, naar fjernskrivebordet var minimeret.)
#
# Findes navnet allerede i TradeStation, aabnes den eksisterende, og koden
# overskrives med den nye (Overskrevet = true i svaret).
#
# Svaret er een linje JSON: Resultat, Note, Lukket, Overskrevet.
#
# SKAL koeres fra 32-bit PowerShell - TSDev er en 32-bit proces.

param(
  [Parameter(Mandatory=$true)][int]$MainHwnd,
  [Parameter(Mandatory=$true)][int]$ProcId,
  [Parameter(Mandatory=$true)][string]$ElPath,
  [Parameter(Mandatory=$true)][ValidateSet("Strategy","ShowMe")][string]$Type,
  [int]$VerifyTimeoutSec = 60
)

$ErrorActionPreference = "Stop"
. "$PSScriptRoot\tsdev-lib.ps1"

Add-Type -TypeDefinition @"
using System; using System.Text; using System.Runtime.InteropServices; using System.Collections.Generic;
public class Ui {
  [DllImport("user32.dll")] public static extern bool EnumWindows(EnumProc cb, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr h, EnumProc cb, IntPtr l);
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetClassNameW(IntPtr h, StringBuilder s, int m);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowTextW(IntPtr h, StringBuilder s, int m);
  [DllImport("user32.dll")] public static extern int GetDlgCtrlID(IntPtr h);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll")] public static extern bool IsWindow(IntPtr h);
  [DllImport("user32.dll", CharSet=CharSet.Unicode, EntryPoint="SendMessageW")]
  public static extern IntPtr SetTextMsg(IntPtr h, uint m, IntPtr w, string l);
  [DllImport("user32.dll")] public static extern IntPtr SendMessage(IntPtr h, uint m, IntPtr w, IntPtr l);
  [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint m, IntPtr w, IntPtr l);

  public const uint WM_SETTEXT = 0x000C;
  public const uint WM_COMMAND = 0x0111;
  public const uint CB_SETCURSEL = 0x014E;
  public const uint WM_GETTEXTLENGTH = 0x000E;
  public const uint BM_CLICK = 0x00F5;
  public const uint WM_CLOSE = 0x0010;

  // TDE's menukommandoer (fra File-menuen i TSResourceDllEng.dll)
  public const int CMD_NEW_STRATEGY = 10576;
  public const int CMD_NEW_SHOWME   = 10569;
  public const int CMD_OPEN         = 57601;
  public const int CMD_VERIFY       = 10602;

  // PostMessage i stedet for SendMessage: kommandoen aabner en dialog,
  // og SendMessage ville vente, til dialogen lukkes.
  public static void Kommando(IntPtr main, int cmd) { PostMessage(main, WM_COMMAND, (IntPtr)cmd, IntPtr.Zero); }

  public static string T(IntPtr h){var s=new StringBuilder(512);GetWindowTextW(h,s,512);return s.ToString();}
  public static string C(IntPtr h){var s=new StringBuilder(256);GetClassNameW(h,s,256);return s.ToString();}

  // Foerste synlige topniveau-vindue i processen med den givne vinduesklasse.
  public static IntPtr TopByClass(uint want, string cls) {
    IntPtr found = IntPtr.Zero;
    EnumWindows((h,l)=>{ uint p; GetWindowThreadProcessId(h,out p);
      if(p==want && IsWindowVisible(h) && C(h)==cls){ found=h; return false; }
      return true; }, IntPtr.Zero);
    return found;
  }
  // Underordnet vindue med et bestemt kontrol-id.
  public static IntPtr ChildById(IntPtr root, int id) {
    IntPtr found = IntPtr.Zero;
    EnumChildWindows(root,(h,l)=>{ if(GetDlgCtrlID(h)==id){ found=h; return false; } return true; }, IntPtr.Zero);
    return found;
  }
  // Underordnet vindue hvis klassenavn starter med et bestemt praefiks.
  public static IntPtr ChildByClassPrefix(IntPtr root, string prefix) {
    IntPtr found = IntPtr.Zero;
    EnumChildWindows(root,(h,l)=>{ if(C(h).StartsWith(prefix)){ found=h; return false; } return true; }, IntPtr.Zero);
    return found;
  }
  // Teksten i en fejlboks (dens Static-felter samlet).
  public static string StaticTekst(IntPtr boks) {
    var sb = new StringBuilder();
    EnumChildWindows(boks,(h,l)=>{ if(C(h)=="Static") sb.Append(T(h).Replace((char)13,(char)32).Replace((char)10,(char)32)).Append((char)32); return true; }, IntPtr.Zero);
    return sb.ToString().Trim();
  }
  // Det aktive dokumentvindue (MDI-barn med en titel).
  public static IntPtr ActiveDoc(IntPtr main) {
    IntPtr mdi = IntPtr.Zero;
    EnumChildWindows(main,(h,l)=>{ if(C(h)=="MDIClient"){ mdi=h; return false; } return true; }, IntPtr.Zero);
    if(mdi==IntPtr.Zero) return IntPtr.Zero;
    IntPtr doc = IntPtr.Zero;
    EnumChildWindows(mdi,(h,l)=>{ if(T(h).Length>0){ doc=h; return false; } return true; }, IntPtr.Zero);
    return doc;
  }
}
"@

# Automationen kunne ikke gennemfoeres. Filen er IKKE verificeret.
function Fail($msg) {
  [pscustomobject]@{ Resultat = "Afbrudt"; Note = $msg } | ConvertTo-Json -Compress
  exit 1
}

# Knapper klikkes med PostMessage, som ikke venter paa svar. SendMessage ville
# haenge, hvis TDE viser en fejlboks midt i klikket (fx "navnet findes").
function Klik($knap) {
  [Ui]::PostMessage($knap, [Ui]::BM_CLICK, [IntPtr]::Zero, [IntPtr]::Zero) | Out-Null
}

# Venter paa, at dialogen lukker. Dukker en fejlboks fra TDE op imens, laeses
# dens tekst, boksen lukkes med OK, og teksten returneres. "" = ingen fejlboks.
function Vent-Paa-Lukning($dialog, $sekunder) {
  $deadline = (Get-Date).AddSeconds($sekunder)
  while ([Ui]::IsWindow($dialog) -and (Get-Date) -lt $deadline) {
    Start-Sleep -Milliseconds 300
    $boks = [Ui]::TopByClass([uint32]$ProcId, "#32770")
    if ($boks -ne [IntPtr]::Zero) {
      $tekst = [Ui]::StaticTekst($boks)
      Klik ([Ui]::ChildById($boks, 1))
      return $tekst
    }
  }
  return ""
}

# Kommando og dialog afhaenger af filtypen. Felterne i dialogen (navn, OK,
# Cancel) har de samme id'er i begge.
if ($Type -eq "Strategy") { $nyKommando = [Ui]::CMD_NEW_STRATEGY; $dlgNavn = "New Strategy"; $dlgKlasse = "TS_IDD_COMMONCREATE" }
else                      { $nyKommando = [Ui]::CMD_NEW_SHOWME;   $dlgNavn = "New ShowMe";   $dlgKlasse = "TS_IDD_INDICREATE" }

# Navnet i TradeStation er filnavnet uden .el, fx RawSignal007
$StratName = [System.IO.Path]::GetFileNameWithoutExtension($ElPath)
$script:Overskrevet = $false
if (-not (Test-Path $ElPath)) { Fail "Filen findes ikke: $ElPath" }
$code = Get-Content -Raw -Encoding UTF8 $ElPath

$main = [IntPtr]$MainHwnd
if (-not [Ui]::IsWindow($main)) { Fail "TSDev-vinduet findes ikke (handle $MainHwnd)." }

$lv = [TsDev]::FindOutputList($main)
if ($lv -eq [IntPtr]::Zero) { Fail "Fandt ikke Output-panelet." }

# ---- 1. Ny strategi/ShowMe: menukommandoen sendes direkte ----
[Ui]::Kommando($main, $nyKommando)
$dlg = [IntPtr]::Zero
$deadline = (Get-Date).AddSeconds(15)
do {
  Start-Sleep -Milliseconds 300
  $dlg = [Ui]::TopByClass([uint32]$ProcId, $dlgKlasse)
} while ($dlg -eq [IntPtr]::Zero -and (Get-Date) -lt $deadline)
if ($dlg -eq [IntPtr]::Zero) { Fail "Dialogen '$dlgNavn' kom ikke frem." }

# ---- 2. Navngiv og tryk OK (ingen fokus noedvendig) ----
$nameEdit = [Ui]::ChildById($dlg, 10515)
$okBtn    = [Ui]::ChildById($dlg, 1)
if ($nameEdit -eq [IntPtr]::Zero -or $okBtn -eq [IntPtr]::Zero) { Fail "Fandt ikke navnefelt/OK-knap i dialogen." }

[Ui]::SetTextMsg($nameEdit, [Ui]::WM_SETTEXT, [IntPtr]::Zero, $StratName) | Out-Null
Start-Sleep -Milliseconds 300
Klik $okBtn

$fejlboks = Vent-Paa-Lukning $dlg 15
if ([Ui]::IsWindow($dlg)) {
  # Luk dialogen med Cancel, saa TSDev ikke efterlades med en aaben dialog.
  Start-Sleep -Milliseconds 300
  Klik ([Ui]::ChildById($dlg, 2))
  Start-Sleep -Milliseconds 500
  # Kun "navnet er i brug" betyder, at der skal overskrives. Alt andet er en fejl.
  if ($fejlboks -notmatch "already being used") {
    Fail "Dialogen '$dlgNavn' lukkede ikke. TDE sagde: '$fejlboks'"
  }
  $script:Overskrevet = $true
}

# ---- 2b. Navnet findes allerede: aabn den eksisterende og overskriv koden ----
# Filerne laves altid forfra ud fra filter_case, saa den gamle kode i
# TradeStation erstattes helt af den nye.
if ($script:Overskrevet) {
  # Typen i "Select Study Type"-listen: ShowMe = 6, Strategy = 7.
  $typeNr = $(if ($Type -eq "Strategy") { 7 } else { 6 })
  [Ui]::Kommando($main, [Ui]::CMD_OPEN)
  $odlg = [IntPtr]::Zero
  $deadline = (Get-Date).AddSeconds(15)
  do {
    Start-Sleep -Milliseconds 300
    $odlg = [Ui]::TopByClass([uint32]$ProcId, "TS_IDD_OPENDLG")
  } while ($odlg -eq [IntPtr]::Zero -and (Get-Date) -lt $deadline)
  if ($odlg -eq [IntPtr]::Zero) { Fail "Navnet findes i TradeStation, og Open-dialogen kom ikke frem." }

  $typeListe = [Ui]::ChildById($odlg, 572)
  $filListe  = [Ui]::ChildById($odlg, 580)
  $openBtn   = [Ui]::ChildById($odlg, 1)
  [Ui]::SendMessage($typeListe, [Ui]::CB_SETCURSEL, [IntPtr]$typeNr, [IntPtr]::Zero) | Out-Null
  # Fortael dialogen at typen er skiftet (CBN_SELCHANGE = 1), saa listen opdateres.
  [Ui]::SendMessage($odlg, [Ui]::WM_COMMAND, [IntPtr]((1 -shl 16) -bor 572), $typeListe) | Out-Null
  Start-Sleep -Milliseconds 800

  # Dialogen aabner kun det, der er markeret i listen - navnet skal vaelges der.
  $raekke = [TsDev]::FindRow($filListe, $StratName)
  if ($raekke -lt 0) {
    Klik ([Ui]::ChildById($odlg, 2))
    Fail "Navnet findes i TradeStation, men staar ikke i Open-listen under $Type."
  }
  [TsDev]::SelectRow($filListe, $raekke) | Out-Null
  Start-Sleep -Milliseconds 300
  Klik $openBtn

  $fejlboks = Vent-Paa-Lukning $odlg 15
  if ([Ui]::IsWindow($odlg)) {
    Start-Sleep -Milliseconds 300
    Klik ([Ui]::ChildById($odlg, 2))
    Fail "Navnet findes i TradeStation, men den eksisterende kunne ikke aabnes. TDE sagde: '$fejlboks'"
  }
}

# ---- 3. Bekraeft at det rigtige dokument er aktivt ----
# Titlen er fx "TradeStation Development Environment - RawSignal007 : Strategy",
# med * til sidst, saa laenge dokumentet ikke er gemt. Navn og type tjekkes
# begge, saa RawSignal007 ikke forveksles med RawSignal007_Kontrol.
Start-Sleep -Milliseconds 800
$title = [Ui]::T($main)
$forventet = " - " + [regex]::Escape($StratName) + " : " + $Type + "\*?$"
if ($title -notmatch $forventet) { Fail "Forkert dokument aktivt efter oprettelse. Titel: '$title'" }

$doc = [Ui]::ActiveDoc($main)
if ($doc -eq [IntPtr]::Zero) { Fail "Fandt ikke dokumentvinduet." }
$editor = [Ui]::ChildByClassPrefix($doc, "BCGPEditCtrl")
if ($editor -eq [IntPtr]::Zero) { Fail "Fandt ikke editoren i dokumentvinduet." }

# ---- 4. Indsaet koden (ingen fokus, ingen udklipsholder) ----
[Ui]::SetTextMsg($editor, [Ui]::WM_SETTEXT, [IntPtr]::Zero, $code) | Out-Null
Start-Sleep -Milliseconds 500
$len = [int][Ui]::SendMessage($editor, [Ui]::WM_GETTEXTLENGTH, [IntPtr]::Zero, [IntPtr]::Zero)
if ($len -lt ($code.Length * 0.9)) { Fail "Koden blev ikke indsat korrekt (editoren har $len tegn, forventede ca. $($code.Length))." }

# ---- 5. Verify: menukommandoen sendes direkte ----
# Panelet toemmes foerst, saa vi med sikkerhed laeser DENNE fils resultat
# og ikke den forriges.
[TsDev]::Clear($lv)
Start-Sleep -Milliseconds 200

[Ui]::Kommando($main, [Ui]::CMD_VERIFY)

# TradeStation afslutter altid med en opsummeringslinje "N error(s), M
# warning(s)". Den - ikke antallet af linjer - er tegnet paa at Verify er faerdig.
$deadline = (Get-Date).AddSeconds($VerifyTimeoutSec)
$text = ""
do {
  Start-Sleep -Milliseconds 400
  if ([TsDev]::RowCount($lv) -gt 0) {
    $all = [TsDev]::ReadAll($lv)
    $lines = @()
    foreach ($r in $all) { $lines += (($r | Where-Object { $_ -ne "" }) -join "  |  ").Trim() }
    $text = $lines -join " ;; "
  }
} while ($text -notmatch "error\(s\)" -and (Get-Date) -lt $deadline)

if ($text -notmatch "error\(s\)") {
  Fail "Verify gav ingen opsummeringslinje inden for $VerifyTimeoutSec sekunder. Panelet indeholdt: '$text'"
}

# ---- 6. Aflaes resultatet ----
# Praecis "0 error(s)" - ikke fx "10 error(s)", som ogsaa indeholder teksten.
$ok = $text -match "(^|[^0-9])0 error\(s\)"

# ---- 7. Luk dokumentet igen ----
# Uden det ophober der sig hundredvis af aabne dokumenter i TSDev. Vinduet
# faar en luk-besked direkte. Verify har gemt filen, saa der spoerges ikke.
[Ui]::PostMessage($doc, [Ui]::WM_CLOSE, [IntPtr]::Zero, [IntPtr]::Zero) | Out-Null
$deadline = (Get-Date).AddSeconds(10)
do {
  Start-Sleep -Milliseconds 400
  $closed = -not [Ui]::IsWindow($doc)
} while (-not $closed -and (Get-Date) -lt $deadline)

[pscustomobject]@{
  Resultat    = $(if ($ok) { "Pass" } else { "Fail" })
  Note        = $text
  Lukket      = $closed
  Overskrevet = [bool]$script:Overskrevet
} | ConvertTo-Json -Compress
