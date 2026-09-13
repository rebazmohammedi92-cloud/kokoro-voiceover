; ============================================================
;  Inno Setup script for Kokoro Voiceover
;  Turns dist\KokoroVoiceover.exe (built by build_exe.bat) into a
;  proper Windows installer: Start Menu entry, optional Desktop
;  shortcut, its own icon, and a clean uninstaller.
;
;  HOW TO USE:
;  1. Run build_exe.bat first (produces dist\KokoroVoiceover.exe).
;  2. Install Inno Setup (free): https://jrsoftware.org/isinfo.php
;  3. Open this file in Inno Setup and click Compile
;     (or right-click it and choose "Compile").
;  4. The finished installer appears in the "installer_output" folder
;     as KokoroVoiceover-Setup.exe — that's the file you double-click
;     to install the app like any normal Windows program.
; ============================================================

#define MyAppName "Kokoro Voiceover"
#define MyAppVersion "1.0"
#define MyAppExeName "KokoroVoiceover.exe"

[Setup]
AppId={{9E7F6E4B-5C1D-4C3A-8F7E-6B1C2D9E0A21}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
OutputDir=installer_output
OutputBaseFilename=KokoroVoiceover-Setup
SetupIconFile=icon.ico
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch {#MyAppName} now"; Flags: nowait postinstall skipifsilent
