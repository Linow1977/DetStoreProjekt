# Verificerer EEN .el-fil i TradeStation Development Environment.
#
# Arbejdsgang (den manuelt bekraeftede, jf. OPGAVEBESKRIVELSE_Automation.md):
#   Ctrl+Alt+S -> navngiv -> indsaet tekst -> F3 -> laes Output-panelet
#
# Fokus laanes KUN til de to tastetryk (Ctrl+Alt+S og F3) og gives straks
# tilbage. Navn og kodetekst saettes med Windows-beskeder, saa hverken
# tastaturet eller udklipsholderen bliver brugt til det.
#
# SKAL koeres fra 32-bit PowerShell - TSDev er en 32-bit proces.

param(
  [Parameter(Mandatory=$true)][int]$MainHwnd,
  [Parameter(Mandatory=$true)][int]$ProcId,
  [Parameter(Mandatory=$true)][string]$ElPath,
  [int]$VerifyTimeoutSec = 60
)

$ErrorActionPreference = "Stop"
Add-Type -AssemblyName System.Windows.Forms
. "$PSScriptRoot\focus-lib.ps1"
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

  public const uint WM_SETTEXT = 0x000C;
  public const uint WM_GETTEXTLENGTH = 0x000E;
  public const uint BM_CLICK = 0x00F5;

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

function Fail($msg) {
  [pscustomobject]@{ Fil = (Split-Path $ElPath -Leaf); Navn = $script:StratName; Resultat = "FEJLET"; Note = $msg } | ConvertTo-Json -Compress
  exit 1
}

$StratName = [System.IO.Path]::GetFileNameWithoutExtension($ElPath)
if (-not (Test-Path $ElPath)) { Fail "Filen findes ikke: $ElPath" }
$code = Get-Content -Raw -Encoding UTF8 $ElPath

$main = [IntPtr]$MainHwnd
if (-not [Ui]::IsWindow($main)) { Fail "TSDev-vinduet findes ikke (handle $MainHwnd)." }

$origFg = [Fg]::GetForegroundWindow()
$lv = [TsDev]::FindOutputList($main)
if ($lv -eq [IntPtr]::Zero) { Fail "Fandt ikke Output-panelet." }

# ---- 1. Ny strategi: Ctrl+Alt+S (kraever fokus) ----
# Tastetrykket naar ikke altid frem foerste gang - typisk naar et andet
# program lige har haft fokus. Det er forbigaaende, saa der proeves igen
# i stedet for at give op.
$dlg = [IntPtr]::Zero
for ($forsoeg = 1; $forsoeg -le 4 -and $dlg -eq [IntPtr]::Zero; $forsoeg++) {
  if (-not [Fg]::ForceForeground($main)) {
    Start-Sleep -Milliseconds 700
    continue
  }
  Start-Sleep -Milliseconds 250
  [System.Windows.Forms.SendKeys]::SendWait("^%s")

  $deadline = (Get-Date).AddSeconds(8)
  do {
    Start-Sleep -Milliseconds 300
    $dlg = [Ui]::TopByClass([uint32]$ProcId, "TS_IDD_COMMONCREATE")
  } while ($dlg -eq [IntPtr]::Zero -and (Get-Date) -lt $deadline)
}

[Fg]::ForceForeground($origFg) | Out-Null
if ($dlg -eq [IntPtr]::Zero) { Fail "Dialogen 'New Strategy' kom ikke frem efter 4 forsoeg." }

# ---- 2. Navngiv og tryk OK (ingen fokus noedvendig) ----
$nameEdit = [Ui]::ChildById($dlg, 10515)
$okBtn    = [Ui]::ChildById($dlg, 1)
if ($nameEdit -eq [IntPtr]::Zero -or $okBtn -eq [IntPtr]::Zero) { Fail "Fandt ikke navnefelt/OK-knap i dialogen." }

[Ui]::SetTextMsg($nameEdit, [Ui]::WM_SETTEXT, [IntPtr]::Zero, $StratName) | Out-Null
Start-Sleep -Milliseconds 300
[Ui]::SendMessage($okBtn, [Ui]::BM_CLICK, [IntPtr]::Zero, [IntPtr]::Zero) | Out-Null

$deadline = (Get-Date).AddSeconds(15)
do { Start-Sleep -Milliseconds 300 } while ([Ui]::IsWindow($dlg) -and (Get-Date) -lt $deadline)
if ([Ui]::IsWindow($dlg)) { Fail "Dialogen lukkede ikke efter OK (navnet er maaske allerede i brug)." }

# ---- 3. Bekraeft at det rigtige dokument er aktivt ----
Start-Sleep -Milliseconds 800
$title = [Ui]::T($main)
if ($title -notlike "*$StratName*") { Fail "Forkert dokument aktivt efter oprettelse. Titel: '$title'" }

$doc = [Ui]::ActiveDoc($main)
if ($doc -eq [IntPtr]::Zero) { Fail "Fandt ikke dokumentvinduet." }
$editor = [Ui]::ChildByClassPrefix($doc, "BCGPEditCtrl")
if ($editor -eq [IntPtr]::Zero) { Fail "Fandt ikke editoren i dokumentvinduet." }

# ---- 4. Indsaet koden (ingen fokus, ingen udklipsholder) ----
[Ui]::SetTextMsg($editor, [Ui]::WM_SETTEXT, [IntPtr]::Zero, $code) | Out-Null
Start-Sleep -Milliseconds 500
$len = [int][Ui]::SendMessage($editor, [Ui]::WM_GETTEXTLENGTH, [IntPtr]::Zero, [IntPtr]::Zero)
if ($len -lt ($code.Length * 0.9)) { Fail "Koden blev ikke indsat korrekt (editoren har $len tegn, forventede ca. $($code.Length))." }

# ---- 5. Verify: F3 (kraever fokus) ----
# Panelet toemmes foerst, saa vi med sikkerhed laeser DENNE fils resultat
# og ikke den forriges.
[TsDev]::Clear($lv)
Start-Sleep -Milliseconds 200

if (-not [Fg]::ForceForeground($main)) { Fail "Kunne ikke faa TSDev i forgrunden til Verify." }
[System.Windows.Forms.SendKeys]::SendWait("{F3}")

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

[Fg]::ForceForeground($origFg) | Out-Null

if ($text -notmatch "error\(s\)") {
  Fail "Verify gav ingen opsummeringslinje inden for $VerifyTimeoutSec sekunder. Panelet indeholdt: '$text'"
}

# ---- 6. Aflaes resultatet ----

$ok = $text -match "0 error\(s\)"

# ---- 7. Luk dokumentet igen: Alt+C ----
# Uden det ophober der sig 381 aabne dokumenter i TSDev.
$closed = $false
if ([Fg]::ForceForeground($main)) {
  [System.Windows.Forms.SendKeys]::SendWait("%c")
  $deadline = (Get-Date).AddSeconds(10)
  do {
    Start-Sleep -Milliseconds 400
    $t = [Ui]::T($main)
    $closed = ($t -notlike "*$StratName*")
  } while (-not $closed -and (Get-Date) -lt $deadline)
  [Fg]::ForceForeground($origFg) | Out-Null
}

[pscustomobject]@{
  Fil      = (Split-Path $ElPath -Leaf)
  Navn     = $StratName
  Resultat = $(if ($ok) { "OK" } else { "FEJLET" })
  Lukket   = $closed
  Note     = $text
} | ConvertTo-Json -Compress
