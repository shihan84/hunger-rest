@echo off
setlocal EnableExtensions EnableDelayedExpansion

echo ========================================
echo HUNGER Restaurant Billing System
echo Simple Installation for Windows
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

echo Starting simple installation...
echo This will install Python, Git, and all dependencies.
echo.

REM Create installation log
set LOG_FILE=installation_log_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt
echo Installation started at %date% %time% > "%LOG_FILE%"
echo.

REM Step 1: Install Python 3.11
echo [1/4] Installing Python 3.11
echo Installing Python 3.11... >> "%LOG_FILE%"
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo Downloading Python 3.11.7
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python-installer.exe'}" 2>>"%LOG_FILE%"
    
    if not exist python-installer.exe (
        echo Failed to download Python installer.
        echo Python download failed >> "%LOG_FILE%"
        goto :error
    )
    
    echo Installing Python 3.11.7
    python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 2>>"%LOG_FILE%"
    
    REM Wait for installation
    timeout /t 30 /nobreak >nul
    
    REM Clean up
    del python-installer.exe
    
    REM Refresh PATH
    call refreshenv.cmd 2>nul || (
        echo Refreshing environment variables
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

REM Step 2: Install Git
echo [2/4] Installing Git for Windows
echo Installing Git... >> "%LOG_FILE%"
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo Downloading Git for Windows
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe' -OutFile 'git-installer.exe'}" 2>>"%LOG_FILE%"
    
    if not exist git-installer.exe (
        echo Failed to download Git installer.
        echo Git download failed >> "%LOG_FILE%"
        goto :error
    )
    
    echo Installing Git
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

REM Step 3: Install Python Dependencies
echo [3/4] Installing Python Dependencies
echo Installing Python Dependencies... >> "%LOG_FILE%"

REM Refresh PATH
call refreshenv.cmd 2>nul || (
    echo Refreshing environment variables
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

echo Upgrading pip
python -m pip install --upgrade pip 2>>"%LOG_FILE%"
if %errorlevel% neq 0 (
    echo Failed to upgrade pip
    echo Failed to upgrade pip >> "%LOG_FILE%"
    goto :error
)

echo Installing desktop application dependencies
python -m pip install -r requirements.txt 2>>"%LOG_FILE%"
if %errorlevel% neq 0 (
    echo Failed to install desktop dependencies
    echo Failed to install desktop dependencies >> "%LOG_FILE%"
    goto :error
)

echo Installing mobile backend dependencies
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

REM Step 4: Initialize Database
echo [4/4] Initializing Database
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

REM Installation Complete
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo What was installed:
echo - Python 3.11.7 (64-bit)
echo - Git for Windows
echo - SQLite Database (built-in with Python)
echo - All required Python packages
echo.
echo Installation log saved to: %LOG_FILE%
echo.
echo To run the desktop application:
echo   python main.py
echo.
echo To run the mobile backend API:
echo   cd mobile_backend
echo   python main.py
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
