# Hjælpefunktioner til at aflæse TradeStation Development Environment (TSDev.exe).
# SKAL køres fra 32-bit PowerShell — TSDev er en 32-bit proces, og
# LVITEM-strukturen har forskellig størrelse i 32- og 64-bit.

$ErrorActionPreference = "Stop"

Add-Type -TypeDefinition @"
using System;
using System.Text;
using System.Runtime.InteropServices;
using System.Collections.Generic;

public class TsDev {
  [DllImport("user32.dll", CharSet=CharSet.Auto)]
  public static extern IntPtr SendMessage(IntPtr h, uint msg, IntPtr w, IntPtr l);
  [DllImport("user32.dll", CharSet=CharSet.Auto)]
  public static extern int GetClassName(IntPtr h, StringBuilder s, int m);
  [DllImport("user32.dll", CharSet=CharSet.Auto)]
  public static extern int GetWindowText(IntPtr h, StringBuilder s, int m);
  [DllImport("user32.dll")]
  public static extern int GetDlgCtrlID(IntPtr h);
  [DllImport("user32.dll")]
  public static extern bool EnumChildWindows(IntPtr h, EnumProc cb, IntPtr l);
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")]
  public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);

  [DllImport("kernel32.dll")]
  public static extern IntPtr OpenProcess(uint acc, bool inherit, uint pid);
  [DllImport("kernel32.dll")]
  public static extern bool CloseHandle(IntPtr h);
  [DllImport("kernel32.dll")]
  public static extern IntPtr VirtualAllocEx(IntPtr p, IntPtr addr, uint size, uint typ, uint prot);
  [DllImport("kernel32.dll")]
  public static extern bool VirtualFreeEx(IntPtr p, IntPtr addr, uint size, uint typ);
  [DllImport("kernel32.dll")]
  public static extern bool WriteProcessMemory(IntPtr p, IntPtr addr, byte[] buf, uint size, out uint written);
  [DllImport("kernel32.dll")]
  public static extern bool ReadProcessMemory(IntPtr p, IntPtr addr, byte[] buf, uint size, out uint read);

  const uint PROCESS_ALL = 0x1F0FFF;
  const uint MEM_COMMIT = 0x1000;
  const uint MEM_RESERVE = 0x2000;
  const uint MEM_RELEASE = 0x8000;
  const uint PAGE_RW = 0x04;

  const uint LVM_GETITEMCOUNT   = 0x1004;
  const uint LVM_GETITEMTEXTW   = 0x1073;
  const uint LVM_GETHEADER      = 0x101F;
  const uint HDM_GETITEMCOUNT   = 0x1200;
  const uint LVM_DELETEALLITEMS = 0x1009;

  public static int RowCount(IntPtr lv) {
    return (int)SendMessage(lv, LVM_GETITEMCOUNT, IntPtr.Zero, IntPtr.Zero);
  }

  // Toemmer Output-panelet. Noedvendigt foer hver Verify: uden det kan man
  // ikke se forskel paa "nyt resultat" og "gammelt resultat, der tilfaeldigvis
  // fylder lige saa mange linjer".
  public static void Clear(IntPtr lv) {
    SendMessage(lv, LVM_DELETEALLITEMS, IntPtr.Zero, IntPtr.Zero);
  }

  public static int ColCount(IntPtr lv) {
    IntPtr hdr = SendMessage(lv, LVM_GETHEADER, IntPtr.Zero, IntPtr.Zero);
    if (hdr == IntPtr.Zero) return 1;
    int n = (int)SendMessage(hdr, HDM_GETITEMCOUNT, IntPtr.Zero, IntPtr.Zero);
    return n < 1 ? 1 : n;
  }

  // Læser hele listen som rækker af kolonner. Kræver kryds-proces
  // hukommelse, fordi LVITEM.pszText skal pege ind i TSDev's egen proces.
  public static List<string[]> ReadAll(IntPtr lv) {
    var rows = new List<string[]>();
    uint pid; GetWindowThreadProcessId(lv, out pid);
    IntPtr proc = OpenProcess(PROCESS_ALL, false, pid);
    if (proc == IntPtr.Zero) throw new Exception("Kunne ikke åbne TSDev-processen (OpenProcess fejlede).");

    const int LVITEM_SIZE = 60;      // rigeligt til 32-bit LVITEM
    const int TEXT_OFFSET = 64;
    const int TEXT_CHARS  = 512;
    uint blockSize = TEXT_OFFSET + (TEXT_CHARS * 2);
    IntPtr remote = VirtualAllocEx(proc, IntPtr.Zero, blockSize, MEM_COMMIT | MEM_RESERVE, PAGE_RW);
    if (remote == IntPtr.Zero) { CloseHandle(proc); throw new Exception("VirtualAllocEx fejlede."); }

    try {
      int rowN = RowCount(lv);
      int colN = ColCount(lv);
      for (int r = 0; r < rowN; r++) {
        var cols = new string[colN];
        for (int c = 0; c < colN; c++) {
          byte[] item = new byte[LVITEM_SIZE];
          // 32-bit LVITEM: mask(0) iItem(4) iSubItem(8) state(12) stateMask(16)
          //                pszText(20) cchTextMax(24)
          BitConverter.GetBytes((uint)0x00000001).CopyTo(item, 0);   // LVIF_TEXT
          BitConverter.GetBytes(r).CopyTo(item, 4);
          BitConverter.GetBytes(c).CopyTo(item, 8);
          BitConverter.GetBytes((int)remote + TEXT_OFFSET).CopyTo(item, 20);
          BitConverter.GetBytes(TEXT_CHARS).CopyTo(item, 24);

          uint w;
          WriteProcessMemory(proc, remote, item, (uint)item.Length, out w);
          SendMessage(lv, LVM_GETITEMTEXTW, (IntPtr)r, remote);

          byte[] txt = new byte[TEXT_CHARS * 2];
          uint rd;
          ReadProcessMemory(proc, (IntPtr)((int)remote + TEXT_OFFSET), txt, (uint)txt.Length, out rd);
          string s = Encoding.Unicode.GetString(txt);
          int z = s.IndexOf('\0');
          if (z >= 0) s = s.Substring(0, z);
          cols[c] = s;
        }
        rows.Add(cols);
      }
    } finally {
      VirtualFreeEx(proc, remote, 0, MEM_RELEASE);
      CloseHandle(proc);
    }
    return rows;
  }

  // Finder et underordnet vindue ud fra klassenavn + kontrol-id.
  public static IntPtr FindChild(IntPtr root, string className, int ctrlId) {
    IntPtr found = IntPtr.Zero;
    EnumChildWindows(root, (h, l) => {
      var cn = new StringBuilder(256);
      GetClassName(h, cn, 256);
      if (cn.ToString() == className && GetDlgCtrlID(h) == ctrlId) { found = h; return false; }
      return true;
    }, IntPtr.Zero);
    return found;
  }

  // Output-panelets liste ligger som SysListView32 med id 15 inde i
  // BCGPControlBar'en der hedder "Output" (id 32804).
  public static IntPtr FindOutputList(IntPtr mainWin) {
    IntPtr bar = IntPtr.Zero;
    EnumChildWindows(mainWin, (h, l) => {
      var cn = new StringBuilder(256); GetClassName(h, cn, 256);
      var tx = new StringBuilder(256); GetWindowText(h, tx, 256);
      if (cn.ToString().StartsWith("BCGPControlBar") && tx.ToString() == "Output" && GetDlgCtrlID(h) == 32804) {
        bar = h; return false;
      }
      return true;
    }, IntPtr.Zero);
    if (bar == IntPtr.Zero) return IntPtr.Zero;
    return FindChild(bar, "SysListView32", 15);
  }
}
"@

function Get-TsDevOutput {
  param([int]$MainWindowHandle)
  $lv = [TsDev]::FindOutputList([IntPtr]$MainWindowHandle)
  if ($lv -eq [IntPtr]::Zero) { throw "Fandt ikke Output-listen i TSDev-vinduet." }
  $rows = [TsDev]::ReadAll($lv)
  $out = @()
  foreach ($r in $rows) { $out += ,($r) }
  return $out
}
