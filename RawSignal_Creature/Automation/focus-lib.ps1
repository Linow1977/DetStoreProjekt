# Staerkere fokus-funktion. Windows blokerer normalt for, at et program
# stjaeler forgrunden. AttachThreadInput binder vores traad sammen med
# vinduets traad, hvilket loefter den spaerring.

Add-Type -TypeDefinition @"
using System; using System.Text; using System.Runtime.InteropServices;
public class Fg {
  [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int cmd);
  [DllImport("user32.dll")] public static extern bool BringWindowToTop(IntPtr h);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] public static extern bool AttachThreadInput(uint from, uint to, bool attach);
  [DllImport("kernel32.dll")] public static extern uint GetCurrentThreadId();
  [DllImport("user32.dll")] public static extern IntPtr SetFocus(IntPtr h);
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowTextW(IntPtr h, StringBuilder s, int m);

  public static string Text(IntPtr h) { var sb = new StringBuilder(512); GetWindowTextW(h, sb, 512); return sb.ToString(); }

  public static bool ForceForeground(IntPtr target) {
    IntPtr fg = GetForegroundWindow();
    if (fg == target) return true;
    uint pidT, pidF;
    uint tidT = GetWindowThreadProcessId(target, out pidT);
    uint tidF = GetWindowThreadProcessId(fg, out pidF);
    uint tidMe = GetCurrentThreadId();

    AttachThreadInput(tidMe, tidT, true);
    AttachThreadInput(tidMe, tidF, true);
    try {
      ShowWindow(target, 9);          // SW_RESTORE
      BringWindowToTop(target);
      SetForegroundWindow(target);
      SetFocus(target);
    } finally {
      AttachThreadInput(tidMe, tidF, false);
      AttachThreadInput(tidMe, tidT, false);
    }
    System.Threading.Thread.Sleep(300);
    return GetForegroundWindow() == target;
  }
}
"@
