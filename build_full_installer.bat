@echo off
REM Build Full Professional Installer for HUNGER Restaurant Billing System
REM This script creates a complete installer with all dependencies

echo ========================================
echo Building Full Professional Installer
echo ========================================
echo.

REM Check if NSIS is installed
makensis /VERSION >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] NSIS found
    makensis /VERSION
) else (
    echo [ERROR] NSIS not found
    echo.
    echo Please install NSIS (Nullsoft Scriptable Install System):
    echo 1. Download from: https://nsis.sourceforge.io/Download
    echo 2. Install NSIS
    echo 3. Add NSIS to your PATH
    echo 4. Run this script again
    echo.
    pause
    exit /b 1
)

REM Create assets directory
if not exist "restaurant_billing\assets" mkdir "restaurant_billing\assets"

REM Create placeholder icon if not exists
if not exist "restaurant_billing\assets\icon.ico" (
    echo [INFO] Creating placeholder icon...
    copy nul "restaurant_billing\assets\icon.ico" >nul 2>&1
)

REM Create placeholder images if not exist
if not exist "restaurant_billing\assets\header.bmp" (
    echo [INFO] Creating placeholder header image...
    copy nul "restaurant_billing\assets\header.bmp" >nul 2>&1
)

if not exist "restaurant_billing\assets\welcome.bmp" (
    echo [INFO] Creating placeholder welcome image...
    copy nul "restaurant_billing\assets\welcome.bmp" >nul 2>&1
)

REM Create LICENSE.txt if not exists
if not exist "LICENSE.txt" (
    echo [INFO] Creating LICENSE.txt...
    echo MIT License > LICENSE.txt
    echo. >> LICENSE.txt
    echo Copyright (c) 2024 HUNGER Restaurant Billing System >> LICENSE.txt
    echo. >> LICENSE.txt
    echo Permission is hereby granted, free of charge, to any person obtaining a copy >> LICENSE.txt
    echo of this software and associated documentation files (the "Software"), to deal >> LICENSE.txt
    echo in the Software without restriction, including without limitation the rights >> LICENSE.txt
    echo to use, copy, modify, merge, publish, distribute, sublicense, and/or sell >> LICENSE.txt
    echo copies of the Software, and to permit persons to whom the Software is >> LICENSE.txt
    echo furnished to do so, subject to the following conditions: >> LICENSE.txt
    echo. >> LICENSE.txt
    echo The above copyright notice and this permission notice shall be included in all >> LICENSE.txt
    echo copies or substantial portions of the Software. >> LICENSE.txt
    echo. >> LICENSE.txt
    echo THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR >> LICENSE.txt
    echo IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, >> LICENSE.txt
    echo FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE >> LICENSE.txt
    echo AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER >> LICENSE.txt
    echo LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, >> LICENSE.txt
    echo OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE >> LICENSE.txt
    echo SOFTWARE. >> LICENSE.txt
)

REM Create full installer script
echo [INFO] Creating full installer script...
cat > installer_full.nsi << 'EOF'
; HUNGER Restaurant Billing System - Full Professional Installer
; Complete installer with all dependencies and features

!define APP_NAME "HUNGER Restaurant Billing System"
!define APP_VERSION "1.0.0"
!define APP_PUBLISHER "HUNGER Solutions"
!define APP_URL "https://github.com/shihan84/hunger-rest"
!define APP_EXECUTABLE "main.py"

; Modern UI
!include "MUI2.nsh"
!include "FileFunc.nsh"
!include "LogicLib.nsh"
!include "WinVer.nsh"

; General settings
Name "${APP_NAME}"
OutFile "HUNGER-Restaurant-Billing-Full-Setup.exe"
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
VIAddVersionKey "FileDescription" "${APP_NAME} Full Installer"

; Interface settings
!define MUI_ABORTWARNING
!define MUI_HEADERIMAGE
!define MUI_WELCOMEFINISHPAGE_BITMAP "restaurant_billing\assets\welcome.bmp"

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
    SectionIn RO
    SetOutPath "$INSTDIR"
    File /r "restaurant_billing"
    File "main.py"
    File "requirements.txt"
    File "README.md"
    File "LICENSE.txt"
    
    ; Create desktop shortcut
    CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "python" "$INSTDIR\${APP_EXECUTABLE}" "" "" 0
    
    ; Create start menu shortcuts
    CreateDirectory "$SMPROGRAMS\${APP_NAME}"
    CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "python" "$INSTDIR\${APP_EXECUTABLE}" "" "" 0
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
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "Publisher" "${APP_PUBLISHER}"
    WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "DisplayVersion" "${APP_VERSION}"
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoModify" 1
    WriteRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}" "NoRepair" 1
    
    ; Create uninstaller
    WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Python Runtime" SecPython
    nsExec::ExecToStack 'python --version'
    Pop $0
    Pop $1
    
    ${If} $0 != 0
        DetailPrint "Python not found, downloading Python 3.11.7..."
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
    nsExec::ExecToStack 'git --version'
    Pop $0
    Pop $1
    
    ${If} $0 != 0
        DetailPrint "Git not found, downloading Git for Windows..."
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
    RMDir /r "$INSTDIR"
    Delete "$DESKTOP\${APP_NAME}.lnk"
    RMDir /r "$SMPROGRAMS\${APP_NAME}"
    DeleteRegKey HKLM "Software\${APP_NAME}"
    DeleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APP_NAME}"
SectionEnd

; Functions
Function .onInit
    ${IfNot} ${AtLeastWin7}
        MessageBox MB_OK "This application requires Windows 7 or later."
        Quit
    ${EndIf}
    
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
EOF

REM Build the installer
echo [INFO] Building full installer...
makensis installer_full.nsi

if %errorLevel% == 0 (
    echo.
    echo ========================================
    echo FULL INSTALLER BUILT SUCCESSFULLY
    echo ========================================
    echo.
    echo Output: HUNGER-Restaurant-Billing-Full-Setup.exe
    echo.
    echo Features:
    echo - Professional GUI installer
    echo - Component selection
    echo - Automatic Python installation
    echo - Automatic Git installation
    echo - Desktop shortcuts
    echo - Start menu integration
    echo - Uninstaller
    echo - Registry integration
    echo - Database initialization
    echo.
    echo Ready for distribution!
) else (
    echo.
    echo ========================================
    echo BUILD FAILED
    echo ========================================
    echo.
    echo Please check the error messages above.
    echo Make sure all required files are present.
)

echo.
pause
