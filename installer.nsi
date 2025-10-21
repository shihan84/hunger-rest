; HUNGER Restaurant Billing System - Professional GUI Installer
; NSIS Script for Windows Installer

!define APP_NAME "HUNGER Restaurant Billing System"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "HUNGER Restaurant"
!define APP_URL "https://github.com/shihan84/hunger-rest"
!define APP_EXECUTABLE "main.py"
!define APP_ICON "restaurant_billing\assets\icon.ico"

; Modern UI
!include "MUI2.nsh"

; General Settings
Name "${APP_NAME}"
OutFile "HUNGER-Restaurant-Billing-Installer.exe"
InstallDir "$PROGRAMFILES\${APP_NAME}"
InstallDirRegKey HKLM "Software\${APP_NAME}" "Install_Dir"
RequestExecutionLevel admin

; Interface Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${APP_ICON}"
!define MUI_UNICON "${APP_ICON}"

; Welcome Page
!define MUI_WELCOMEPAGE_TITLE "Welcome to ${APP_NAME}"
!define MUI_WELCOMEPAGE_TEXT "This wizard will guide you through the installation of ${APP_NAME}.$\r$\n$\r$\n${APP_NAME} is a complete restaurant billing system with GST compliance, UPI integration, and user management.$\r$\n$\r$\nClick Next to continue."
!define MUI_WELCOMEPAGE_BGCOLOR 0xFFFFFF

; License Page
!define MUI_LICENSEPAGE_TEXT_TOP "Please review the license terms before installing ${APP_NAME}."
!define MUI_LICENSEPAGE_TEXT_BOTTOM "If you accept the terms of the agreement, click I Agree to continue. You must accept the agreement to install ${APP_NAME}."

; Directory Page
!define MUI_DIRECTORYPAGE_TEXT_TOP "Setup will install ${APP_NAME} in the following folder.$\r$\n$\r$\nTo install in a different folder, click Browse and select another folder.$\r$\n$\r$\nClick Next to continue."

; Instfiles Page
!define MUI_INSTFILESPAGE_FINISHHEADER_TEXT "Installation Complete"
!define MUI_INSTFILESPAGE_FINISHPAGE_TEXT "${APP_NAME} has been installed on your computer.$\r$\n$\r$\nClick Finish to close this wizard."

; Finish Page
!define MUI_FINISHPAGE_TITLE "Installation Complete"
!define MUI_FINISHPAGE_TEXT "${APP_NAME} has been installed on your computer.$\r$\n$\r$\nThe application has been installed with all necessary components including Python dependencies and database initialization.$\r$\n$\r$\nClick Finish to close this wizard."
!define MUI_FINISHPAGE_RUN "$INSTDIR\start_desktop.bat"
!define MUI_FINISHPAGE_RUN_TEXT "Launch ${APP_NAME}"
!define MUI_FINISHPAGE_LINK "Visit our website for support and updates"
!define MUI_FINISHPAGE_LINK_LOCATION "${APP_URL}"

; Pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller Pages
!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

; Languages
!insertmacro MUI_LANGUAGE "English"

; Installer Sections
Section "Main Application" SecMain
    SectionIn RO
    
    SetOutPath "$INSTDIR"
    
    ; Copy application files
    File /r "restaurant_billing"
    File "main.py"
    File "requirements.txt"
    File "README.md"
    File "LICENSE.txt"
    
    ; Create start scripts
    FileOpen $0 "$INSTDIR\start_desktop.bat" w
    FileWrite $0 "@echo off$\r$\n"
    FileWrite $0 "cd /d $\"$INSTDIR$\"$\r$\n"
    FileWrite $0 "python main.py$\r$\n"
    FileWrite $0 "pause$\r$\n"
    FileClose $0
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\Uninstall.exe"
    
    ; Registry entries
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayName" "${APP_NAME}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString" "$INSTDIR\Uninstall.exe"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "InstallLocation" "$INSTDIR"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "URLInfoAbout" "${APP_URL}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
    
    ; Create desktop shortcut
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\start_desktop.bat" "" "$INSTDIR\${APP_ICON}" 0
    
    ; Create start menu shortcuts
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\start_desktop.bat" "" "$INSTDIR\${APP_ICON}" 0
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\Uninstall.exe" 0
    
    ; Install Python dependencies
    DetailPrint "Installing Python dependencies..."
    ExecWait 'python -m pip install --upgrade pip'
    ExecWait 'python -m pip install -r "$INSTDIR\requirements.txt"'
    
    ; Initialize database
    DetailPrint "Initializing database..."
    ExecWait 'python -c "from restaurant_billing.db import init_db; init_db(); print(\"Database initialized successfully\")"'
    
    DetailPrint "Installation completed successfully!"
SectionEnd

Section "Python Runtime" SecPython
    ; Check if Python is installed
    ExecWait 'python --version' $0
    ${If} $0 != 0
        DetailPrint "Python not found. Please install Python 3.11+ from https://python.org"
        MessageBox MB_OK "Python 3.11+ is required but not found. Please install Python from https://python.org and run the installer again."
        Abort
    ${EndIf}
    
    ; Check Python version
    ExecWait 'python -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"' $0
    ${If} $0 != 0
        DetailPrint "Python version 3.11+ required. Current version may be too old."
        MessageBox MB_OK "Python 3.11+ is required. Please upgrade Python and run the installer again."
        Abort
    ${EndIf}
    
    DetailPrint "Python runtime check passed."
SectionEnd

; Uninstaller Section
Section "Uninstall"
    ; Remove files
    RMDir /r "$INSTDIR\restaurant_billing"
    Delete "$INSTDIR\main.py"
    Delete "$INSTDIR\requirements.txt"
    Delete "$INSTDIR\README.md"
    Delete "$INSTDIR\LICENSE.txt"
    Delete "$INSTDIR\start_desktop.bat"
    Delete "$INSTDIR\Uninstall.exe"
    
    ; Remove shortcuts
    Delete "$DESKTOP\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
    Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
    RMDir "$SMPROGRAMS\${APP_NAME}"
    
    ; Remove registry entries
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
    DeleteRegKey HKLM "Software\${APP_NAME}"
    
    ; Remove installation directory
    RMDir "$INSTDIR"
    
    DetailPrint "Uninstallation completed."
SectionEnd

; Installer Functions
Function .onInit
    ; Check if already installed
    ReadRegStr $R0 HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "UninstallString"
    StrCmp $R0 "" done
    
    MessageBox MB_OKCANCEL|MB_ICONEXCLAMATION "${APP_NAME} is already installed. $\n$\nClick OK to remove the previous version or Cancel to cancel this upgrade." IDOK uninst
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
        Exec "$INSTDIR\start_desktop.bat"
    skip:
FunctionEnd