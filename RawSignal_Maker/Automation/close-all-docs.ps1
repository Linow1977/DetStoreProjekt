param([Parameter(Mandatory=$true)][int]$MainHwnd, [int]$Max = 20)

Add-Type -AssemblyName System.Windows.Forms
. "$PSScriptRoot\focus-lib.ps1"

Add-Type -TypeDefinition @"
using System; using System.Text; using System.Runtime.InteropServices; using System.Collections.Generic;
public class Doc {
  [DllImport("user32.dll")] public static extern bool EnumChildWindows(IntPtr h, EnumProc cb, IntPtr l);
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetClassNameW(IntPtr h, StringBuilder s, int m);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowTextW(IntPtr h, StringBuilder s, int m);
  public static string T(IntPtr h){var s=new StringBuilder(512);GetWindowTextW(h,s,512);return s.ToString();}
  public static string C(IntPtr h){var s=new StringBuilder(256);GetClassNameW(h,s,256);return s.ToString();}
  public static List<string> Open(IntPtr main){
    var r=new List<string>(); IntPtr mdi=IntPtr.Zero;
    EnumChildWindows(main,(h,l)=>{ if(C(h)=="MDIClient"){mdi=h;return false;} return true;},IntPtr.Zero);
    if(mdi==IntPtr.Zero) return r;
    EnumChildWindows(mdi,(h,l)=>{ string t=T(h); if(t.Length>0) r.Add(t); return true;},IntPtr.Zero);
    return r;}
}
"@

$main = [IntPtr]$MainHwnd
$origFg = [Fg]::GetForegroundWindow()

$docs = [Doc]::Open($main)
Write-Output "Aabne dokumenter foer: $($docs.Count)"
$docs | ForEach-Object { Write-Output "  $_" }

if ($docs.Count -eq 0) { Write-Output "Intet at lukke."; exit 0 }

if (-not [Fg]::ForceForeground($main)) {
  Write-Output "AFBRUDT: kunne ikke faa TSDev i forgrunden."
  exit 1
}

$n = 0
while ($n -lt $Max) {
  $before = [Doc]::Open($main).Count
  if ($before -eq 0) { break }
  [System.Windows.Forms.SendKeys]::SendWait("%c")
  Start-Sleep -Milliseconds 800
  $after = [Doc]::Open($main).Count
  Write-Output "  Alt+C: $before -> $after"
  if ($after -ge $before) { Write-Output "  (lukkede ikke - stopper for ikke at sende flere tastetryk i blinde)"; break }
  $n++
}

[Fg]::ForceForeground($origFg) | Out-Null

$rest = [Doc]::Open($main)
Write-Output ""
Write-Output "Aabne dokumenter efter: $($rest.Count)"
$rest | ForEach-Object { Write-Output "  $_" }
Write-Output "Fokus tilbage til: '$([Fg]::Text([Fg]::GetForegroundWindow()))'"
