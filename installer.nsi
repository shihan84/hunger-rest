; HUNGER Restaurant Billing System - Professional GUI Installer
; NSIS Script for creating a professional Windows installer

!define APP_NAME "HUNGER Restaurant Billing System"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "HUNGER Solutions"
!define APP_URL "https://github.com/shihan84/hunger-rest"
!define APP_EXECUTABLE "main.py"
!define APP_ICON "restaurant_billing\assets\icon.ico"

; Modern UI
!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"
!include "WinVer.nsh"

; General settings
Name "${APP_NAME}"
OutFile "HUNGER-Restaurant-Billing-Setup.exe"
InstallDir "$PROGRAMFILES64\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "InstallDir"
RequestExecutionLevel admin
ShowInstDetails show
ShowUninstDetails show

; Version information
VIProductVersion "${APP_VERSION}.0"
VIAddVersionKey "ProductName" "${APP_NAME}"
VIAddVersionKey "ProductVersion" "${APP_VERSION}"
VIAddVersionKey "CompanyName" "${APP_PUBLISHER}"
VIAddVersionKey "FileVersion" "${APP_VERSION}"
VIAddVersionKey "FileDescription" "${APP_NAME} Installer"

; Interface settings
!define MUI_ABORTWARNING
!define MUI_ICON "${APP_ICON}"
!define MUI_UNICON "${APP_ICON}"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_BITMAP "restaurant_billing\assets\header.bmp"
!define MUI_WELCOMEFINISHPAGE_BITMAP "restaurant_billing\assets\welcome.bmp"
!define MUI_UNWELCOMEFINISHPAGE_BITMAP "restaurant_billing\assets\welcome.bmp"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installer sections
Section "Desktop Application" SecDesktop
    SectionIn RO  ; Read-only (always selected)
    
    SetOutPath "$INSTDIR"
    
    ; Copy application files
    File /r "restaurant_billing"
    File "main.py"
    File "requirements.txt"
    File "README.md"
    File "LICENSE.txt"
    
    ; Create desktop shortcut
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "python" "$INSTDIR\${APP_EXECUTABLE}" "" "$INSTDIR\${APP_ICON}" 0
    
    ; Create start menu shortcuts
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "python" "$INSTDIR\${APP_EXECUTABLE}" "" "$INSTDIR\${APP_ICON}" 0
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe" 0
    
    ; Create launcher script
    FileOpen $0 "$INSTDIR\start_desktop.bat" w
    FileWrite $0 "@echo off$\r$\n"
    FileWrite $0 "cd /d $\"$INSTDIR$\"$\r$\n"
    FileWrite $0 "python main.py$\r$\n"
    FileWrite $0 "pause$\r$\n"
    FileClose $0
    
    ; Write registry keys
    WriteRegStr HKLM "Software\${APP_NAME}" "InstallDir" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayIcon" "$INSTDIR\${APP_ICON}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Python Runtime" SecPython
    ; Check if Python is installed
    nsExec::ExecToStack 'python --version'
    Pop $0
    Pop $1
    
    ${If} $0 != 0
        DetailPrint "Python not found, downloading Python 3.11.7..."
        
        ; Download Python installer
        inetc::get "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe" "$TEMP\python-installer.exe"
        Pop $0
        
        ${If} $0 == "OK"
            DetailPrint "Installing Python 3.11.7..."
            ExecWait '"$TEMP\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_test=0'
            Delete "$TEMP\python-installer.exe"
        ${Else}
            MessageBox MB_OK "Failed to download Python installer. Please install Python manually from python.org"
        ${EndIf}
    ${Else}
        DetailPrint "Python is already installed: $1"
    ${EndIf}
SectionEnd

Section "Git for Windows" SecGit
    ; Check if Git is installed
    nsExec::ExecToStack 'git --version'
    Pop $0
    Pop $1
    
    ${If} $0 != 0
        DetailPrint "Git not found, downloading Git for Windows..."
        
        ; Download Git installer
        inetc::get "https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe" "$TEMP\git-installer.exe"
        Pop $0
        
        ${If} $0 == "OK"
            DetailPrint "Installing Git for Windows..."
            ExecWait '"$TEMP\git-installer.exe" /SILENT /NORESTART'
            Delete "$TEMP\git-installer.exe"
        ${Else}
            MessageBox MB_OK "Failed to download Git installer. Please install Git manually from git-scm.com"
        ${EndIf}
    ${Else}
        DetailPrint "Git is already installed: $1"
    ${EndIf}
SectionEnd

Section "Install Dependencies" SecDependencies
    SetOutPath "$INSTDIR"
    
    DetailPrint "Installing Python dependencies..."
    nsExec::ExecToStack 'python -m pip install -r requirements.txt --quiet --disable-pip-version-check'
    Pop $0
    Pop $1
    
    ${If} $0 == 0
        DetailPrint "Dependencies installed successfully"
    ${Else}
        DetailPrint "Warning: Some dependencies may not have installed correctly"
    ${EndIf}
SectionEnd

Section "Initialize Database" SecDatabase
    SetOutPath "$INSTDIR"
    
    DetailPrint "Initializing database..."
    nsExec::ExecToStack 'python -c "from restaurant_billing.db import init_db; init_db(); print(\"Database initialized successfully\")"'
    Pop $0
    Pop $1
    
    ${If} $0 == 0
        DetailPrint "Database initialized successfully"
    ${Else}
        DetailPrint "Warning: Database initialization may have failed"
    ${EndIf}
SectionEnd

; Section descriptions
LangString DESC_SecDesktop ${LANG_ENGLISH} "Core desktop billing application with all features"
LangString DESC_SecPython ${LANG_ENGLISH} "Python 3.11.7 runtime (required for the application)"
LangString DESC_SecGit ${LANG_ENGLISH} "Git for Windows (required for updates and version control)"
LangString DESC_SecDependencies ${LANG_ENGLISH} "Python packages and dependencies"
LangString DESC_SecDatabase ${LANG_ENGLISH} "Initialize SQLite database with default data"

!insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecPython} $(DESC_SecPython)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecGit} $(DESC_SecGit)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDependencies} $(DESC_SecDependencies)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDatabase} $(DESC_SecDatabase)
!insertmacro MUI_FUNCTION_DESCRIPTION_END

; Uninstaller
Section "Uninstall"
    ; Remove files
    RMDir /r "$INSTDIR"
    
    ; Remove shortcuts
    Delete "$DESKTOP\${APP_NAME}.lnk"
    RMDir /r "$SMPROGRAMS\${APP_NAME}"
    
    ; Remove registry keys
    DeleteRegKey HKLM "Software\${APP_NAME}"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
SectionEnd

; Functions
Function .onInit
    ; Check Windows version
    ${IfNot} ${AtLeastWin7}
        MessageBox MB_OK "This application requires Windows 7 or later."
        Quit
    ${EndIf}
    
    ; Check if already installed
    ReadRegStr $R0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString"
    StrCmp $R0 "" done
    
    MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION \
    "${APP_NAME} is already installed. $\n$\nClick OK to remove the previous version or Cancel to cancel this upgrade." \
    IDOK uninst
    Abort
    
    uninst:
        ClearErrors
        ExecWait '$R0 _?=$INSTDIR'
        
        IfErrors no_remove_uninstaller done
        no_remove_uninstaller:
    
    done:
FunctionEnd

Function .onInstSuccess
    MessageBox MB_YESNO "Installation completed successfully!$\n$\nWould you like to launch ${APP_NAME} now?" IDYES launch IDNO skip
    launch:
        Exec "python $\"$INSTDIR\${APP_EXECUTABLE}$\""
    skip:
FunctionEnd
