# Lista os titulos das janelas visiveis de todos os processos kicad.exe.
Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices; using System.Collections.Generic;
public class W {
  public delegate bool P(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] public static extern bool EnumWindows(P f, IntPtr l);
  [DllImport("user32.dll")] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint p);
  [DllImport("user32.dll")] public static extern bool IsWindowVisible(IntPtr h);
  public static List<string> T(uint pid) {
    var r = new List<string>();
    EnumWindows((h, l) => { uint p; GetWindowThreadProcessId(h, out p);
      if (p == pid && IsWindowVisible(h)) { var s = new StringBuilder(512); GetWindowText(h, s, 512); if (s.Length > 0) r.Add(s.ToString()); }
      return true; }, IntPtr.Zero);
    return r; } }
"@
# Sai com codigo 1 se alguma janela for do projecto EBM2_V5: uma cadeia "guarda && escrita" tem de parar.
# (23-09-2026: a guarda so listava; uma copia de backups correu com a folha 06 aberta e por salvar.)
$t = @(foreach ($p in Get-Process kicad, eeschema, pcbnew -ErrorAction SilentlyContinue) { [W]::T([uint32]$p.Id) })
$t
if ($t | Where-Object { $_ -match "EBM2_V5" }) { Write-Output "GUARDA: projecto EBM2_V5 aberto no KiCad"; exit 1 }
exit 0
