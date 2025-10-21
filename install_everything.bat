@echo off
setlocal EnableExtensions EnableDelayedExpansion

echo ========================================
echo HUNGER Restaurant Billing System
echo Complete Installation for Fresh Windows
echo ========================================
echo.

REM Check if running as Administrator
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo This script requires Administrator privileges.
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo Starting complete installation...
echo This will install all required software and dependencies.
echo.

REM Create installation log
set LOG_FILE=installation_log_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt
echo Installation started at %date% %time% > "%LOG_FILE%"
echo.

REM Step 1: Install Chocolatey (Windows Package Manager)
echo [1/8] Installing Chocolatey Package Manager...
echo Installing Chocolatey... >> "%LOG_FILE%"
powershell -Command "Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))" 2>>"%LOG_FILE%"
if %errorlevel% neq 0 (
    echo Failed to install Chocolatey. Continuing with manual installation...
    echo Chocolatey installation failed >> "%LOG_FILE%"
) else (
    echo Chocolatey installed successfully!
    echo Chocolatey installed successfully >> "%LOG_FILE%"
)
echo.

REM Step 2: Install Python 3.11
echo [2/8] Installing Python 3.11...
echo Installing Python 3.11... >> "%LOG_FILE%"
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Downloading Python 3.11.7...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python-installer.exe'}" 2>>"%LOG_FILE%"
    
    if not exist python-installer.exe (
        echo Failed to download Python installer.
        echo Python download failed >> "%LOG_FILE%"
        goto :error
    )
    
    echo Installing Python 3.11.7...
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 2>>"%LOG_FILE%"
    
    REM Wait for installation
    timeout /t 30 /nobreak >nul
    
    REM Clean up
    del python-installer.exe
    
    REM Refresh PATH
    call refreshenv.cmd 2>nul || (
        echo Refreshing environment variables...
        for /f "usebackq tokens=2*" %%A in (`reg query HKCU\Environment /v PATH`) do set USERPATH=%%B
        for /f "usebackq tokens=2*" %%A in (`reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH`) do set SYSPATH=%%B
        set PATH=%SYSPATH%;%USERPATH%
    )
    
    echo Python installed successfully!
    echo Python installed successfully >> "%LOG_FILE%"
) else (
    echo Python already installed:
    python --version
    echo Python already installed >> "%LOG_FILE%"
)
echo.

REM Step 3: Install Git
echo [3/8] Installing Git for Windows...
echo Installing Git... >> "%LOG_FILE%"
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo Downloading Git for Windows...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe' -OutFile 'git-installer.exe'}" 2>>"%LOG_FILE%"
    
    if not exist git-installer.exe (
        echo Failed to download Git installer.
        echo Git download failed >> "%LOG_FILE%"
        goto :error
    )
    
    echo Installing Git...
    git-installer.exe /SILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh" 2>>"%LOG_FILE%"
    
    REM Wait for installation
    timeout /t 20 /nobreak >nul
    
    REM Clean up
    del git-installer.exe
    
    echo Git installed successfully!
    echo Git installed successfully >> "%LOG_FILE%"
) else (
    echo Git already installed:
    git --version
    echo Git already installed >> "%LOG_FILE%"
)
echo.

REM Step 4: Install Visual Studio Build Tools (for Python packages)
echo [4/8] Installing Visual Studio Build Tools...
echo Installing Visual Studio Build Tools... >> "%LOG_FILE%"
powershell -Command "& {Invoke-WebRequest -Uri 'https://aka.ms/vs/17/release/vs_buildtools.exe' -OutFile 'vs_buildtools.exe'}" 2>>"%LOG_FILE%"
if exist vs_buildtools.exe (
    echo Installing Visual Studio Build Tools (this may take a while)...
    vs_buildtools.exe --quiet --wait --add Microsoft.VisualStudio.Workload.VCTools --includeRecommended 2>>"%LOG_FILE%"
    del vs_buildtools.exe
    echo Visual Studio Build Tools installed!
    echo Visual Studio Build Tools installed >> "%LOG_FILE%"
) else (
    echo Visual Studio Build Tools download failed, continuing...
    echo Visual Studio Build Tools download failed >> "%LOG_FILE%"
)
echo.

REM Step 5: Install Node.js (for development tools)
echo [5/8] Installing Node.js...
echo Installing Node.js... >> "%LOG_FILE%"
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo Downloading Node.js...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://nodejs.org/dist/v20.10.0/node-v20.10.0-x64.msi' -OutFile 'nodejs-installer.msi'}" 2>>"%LOG_FILE%"
    
    if exist nodejs-installer.msi (
        echo Installing Node.js...
        msiexec /i nodejs-installer.msi /quiet 2>>"%LOG_FILE%"
        del nodejs-installer.msi
        echo Node.js installed successfully!
        echo Node.js installed successfully >> "%LOG_FILE%"
    ) else (
        echo Node.js download failed, continuing...
        echo Node.js download failed >> "%LOG_FILE%"
    )
) else (
    echo Node.js already installed:
    node --version
    echo Node.js already installed >> "%LOG_FILE%"
)
echo.

REM Step 6: Install Flutter (for mobile app development)
echo [6/8] Installing Flutter SDK...
echo Installing Flutter SDK... >> "%LOG_FILE%"
where flutter >nul 2>&1
if %errorlevel% neq 0 (
    echo Downloading Flutter SDK...
    powershell -Command "& {Invoke-WebRequest -Uri 'https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.16.5-stable.zip' -OutFile 'flutter-sdk.zip'}" 2>>"%LOG_FILE%"
    
    if exist flutter-sdk.zip (
        echo Extracting Flutter SDK...
        powershell -Command "& {Expand-Archive -Path 'flutter-sdk.zip' -DestinationPath 'C:\flutter' -Force}" 2>>"%LOG_FILE%"
        del flutter-sdk.zip
        
        REM Add Flutter to PATH
        setx PATH "%PATH%;C:\flutter\bin" /M 2>>"%LOG_FILE%"
        
        echo Flutter SDK installed successfully!
        echo Flutter SDK installed successfully >> "%LOG_FILE%"
    ) else (
        echo Flutter SDK download failed, continuing...
        echo Flutter SDK download failed >> "%LOG_FILE%"
    )
) else (
    echo Flutter already installed:
    flutter --version
    echo Flutter already installed >> "%LOG_FILE%"
)
echo.

REM Step 7: Install Python Dependencies
echo [7/8] Installing Python Dependencies...
echo Installing Python Dependencies... >> "%LOG_FILE%"

REM Refresh PATH
call refreshenv.cmd 2>nul || (
    echo Refreshing environment variables...
    for /f "usebackq tokens=2*" %%A in (`reg query HKCU\Environment /v PATH`) do set USERPATH=%%B
    for /f "usebackq tokens=2*" %%A in (`reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH`) do set SYSPATH=%%B
    set PATH=%SYSPATH%;%USERPATH%
)

REM Check if Python is available
python --version 2>>"%LOG_FILE%"
if %errorlevel% neq 0 (
    echo Python not found in PATH. Please restart your terminal or reboot.
    echo Python not found in PATH >> "%LOG_FILE%"
    goto :error
)

echo Upgrading pip...
python -m pip install --upgrade pip 2>>"%LOG_FILE%"
if %errorlevel% neq 0 (
    echo Failed to upgrade pip
    echo Failed to upgrade pip >> "%LOG_FILE%"
    goto :error
)

echo Installing desktop application dependencies...
python -m pip install -r requirements.txt 2>>"%LOG_FILE%"
if %errorlevel% neq 0 (
    echo Failed to install desktop dependencies
    echo Failed to install desktop dependencies >> "%LOG_FILE%"
    goto :error
)

echo Installing mobile backend dependencies...
cd mobile_backend
python -m pip install -r requirements.txt 2>>"%..\LOG_FILE%"
if %errorlevel% neq 0 (
    echo Failed to install mobile backend dependencies
    echo Failed to install mobile backend dependencies >> "%..\LOG_FILE%"
    cd ..
    goto :error
)
cd ..

echo Python dependencies installed successfully!
echo Python dependencies installed successfully >> "%LOG_FILE%"
echo.

REM Step 7.5: Initialize Database
echo [7.5/8] Initializing Database...
echo Initializing Database... >> "%LOG_FILE%"
python -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized successfully')" 2>>"%LOG_FILE%"
if %errorlevel% neq 0 (
    echo Database initialization failed, but application will create it on first run
    echo Database initialization failed >> "%LOG_FILE%"
) else (
    echo Database initialized successfully!
    echo Database initialized successfully >> "%LOG_FILE%"
)
echo.

REM Step 8: Create Desktop Shortcuts and Start Menu Entries
echo [8/8] Creating Desktop Shortcuts and Start Menu Entries...
echo Creating shortcuts... >> "%LOG_FILE%"

REM Create desktop shortcuts
set DESKTOP_PATH=%USERPROFILE%\Desktop
set CURRENT_PATH=%CD%

REM Desktop App Shortcut
echo Creating desktop shortcut...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP_PATH%\HUNGER Restaurant Billing.lnk'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = 'main.py'; $Shortcut.WorkingDirectory = '%CURRENT_PATH%'; $Shortcut.Description = 'HUNGER Restaurant Billing System'; $Shortcut.Save()}" 2>>"%LOG_FILE%"

REM Mobile Backend Shortcut
echo Creating mobile backend shortcut...
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%DESKTOP_PATH%\HUNGER Mobile Backend.lnk'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = 'main.py'; $Shortcut.WorkingDirectory = '%CURRENT_PATH%\mobile_backend'; $Shortcut.Description = 'HUNGER Restaurant Mobile Backend API'; $Shortcut.Save()}" 2>>"%LOG_FILE%"

REM Start Menu Entries
echo Creating start menu entries...
set START_MENU_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\HUNGER Restaurant
mkdir "%START_MENU_PATH%" 2>nul

REM Desktop App Start Menu
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU_PATH%\HUNGER Restaurant Billing.lnk'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = 'main.py'; $Shortcut.WorkingDirectory = '%CURRENT_PATH%'; $Shortcut.Description = 'HUNGER Restaurant Billing System'; $Shortcut.Save()}" 2>>"%LOG_FILE%"

REM Mobile Backend Start Menu
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU_PATH%\Mobile Backend API.lnk'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = 'main.py'; $Shortcut.WorkingDirectory = '%CURRENT_PATH%\mobile_backend'; $Shortcut.Description = 'HUNGER Restaurant Mobile Backend API'; $Shortcut.Save()}" 2>>"%LOG_FILE%"

REM Uninstaller Start Menu
powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU_PATH%\Uninstall.lnk'); $Shortcut.TargetPath = 'powershell'; $Shortcut.Arguments = '-ExecutionPolicy Bypass -File \"%CURRENT_PATH%\uninstall.ps1\"'; $Shortcut.WorkingDirectory = '%CURRENT_PATH%'; $Shortcut.Description = 'Uninstall HUNGER Restaurant Billing System'; $Shortcut.Save()}" 2>>"%LOG_FILE%"

echo Shortcuts created successfully!
echo Shortcuts created successfully >> "%LOG_FILE%"
echo.

REM Installation Complete
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo What was installed:
echo - Python 3.11.7 (64-bit)
echo - Git for Windows
echo - Visual Studio Build Tools
echo - Node.js (for development)
echo - Flutter SDK (for mobile development)
echo - SQLite Database (built-in with Python)
echo - All required Python packages
echo - Desktop shortcuts
echo - Start menu entries
echo.
echo Installation log saved to: %LOG_FILE%
echo.
echo To run the desktop application:
echo   python main.py
echo   or double-click the desktop shortcut
echo.
echo To run the mobile backend API:
echo   cd mobile_backend
echo   python main.py
echo   or double-click the mobile backend shortcut
echo.
echo First login credentials:
echo   Username: owner
echo   Password: 1234
echo.
echo The application will create the database automatically.
echo.
echo Press any key to launch the application now...
pause >nul

echo Launching HUNGER Restaurant Billing System...
python main.py

exit /b 0

:error
echo.
echo ========================================
echo Installation failed!
echo ========================================
echo.
echo Please check the installation log: %LOG_FILE%
echo.
echo Common solutions:
echo 1. Check your internet connection
echo 2. Temporarily disable antivirus
echo 3. Run this script as Administrator
echo 4. Install dependencies manually
echo.
pause
exit /b 1
