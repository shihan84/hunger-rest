@echo off
setlocal EnableExtensions EnableDelayedExpansion

echo ========================================
echo HUNGER Restaurant Billing System
echo Complete Installation for Windows 10/11
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

REM Check Windows version
for /f "tokens=4-5 delims=. " %%i in ('ver') do set VERSION=%%i.%%j
echo Windows Version: %VERSION%
echo.

REM Detect Python
where python >nul 2>&1
if %errorlevel% neq 0 (
  echo Python not found. Installing Python 3.11...
  echo.
  
  REM Download Python installer
  echo Downloading Python 3.11.7 (64-bit)...
  powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python-installer.exe'}"
  
  if not exist python-installer.exe (
    echo Failed to download Python installer.
    echo Please download Python 3.11 (64-bit) manually from:
    echo https://www.python.org/downloads/windows/
    pause
    exit /b 1
  )
  
  echo Installing Python 3.11.7...
  echo Please wait, this may take a few minutes...
  python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
  
  REM Wait for installation to complete
  timeout /t 30 /nobreak >nul
  
  REM Clean up installer
  del python-installer.exe
  
  REM Refresh PATH
  call refreshenv.cmd 2>nul || (
    echo Refreshing environment variables...
    for /f "usebackq tokens=2*" %%A in (`reg query HKCU\Environment /v PATH`) do set USERPATH=%%B
    for /f "usebackq tokens=2*" %%A in (`reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v PATH`) do set SYSPATH=%%B
    set PATH=%SYSPATH%;%USERPATH%
  )
  
  REM Verify Python installation
  where python >nul 2>&1
  if %errorlevel% neq 0 (
    echo Python installation failed. Please install manually from:
    echo https://www.python.org/downloads/windows/
    pause
    exit /b 1
  )
  
  echo Python installed successfully!
  echo.
)

REM Get Python version and path
for /f "usebackq tokens=*" %%p in (`where python`) do (
  set PY_EXE=%%p
  goto :found
)
:found
for %%d in ("%PY_EXE%") do set PY_DIR=%%~dpd
set PY_DIR=%PY_DIR:~0,-1%
set SCRIPTS_DIR=%PY_DIR%\Scripts

echo Python found at: %PY_EXE%
python --version
echo.

REM Check and install Git if not present
where git >nul 2>&1
if %errorlevel% neq 0 (
  echo Git not found. Installing Git...
  echo.
  
  REM Download Git installer
  echo Downloading Git for Windows...
  powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe' -OutFile 'git-installer.exe'}"
  
  if not exist git-installer.exe (
    echo Failed to download Git installer.
    echo Please download Git manually from: https://git-scm.com/download/win
    pause
    exit /b 1
  )
  
  echo Installing Git...
  git-installer.exe /SILENT /NORESTART /NOCANCEL /SP- /CLOSEAPPLICATIONS /RESTARTAPPLICATIONS /COMPONENTS="icons,ext\reg\shellhere,assoc,assoc_sh"
  
  REM Wait for installation
  timeout /t 20 /nobreak >nul
  
  REM Clean up installer
  del git-installer.exe
  
  echo Git installed successfully!
  echo.
) else (
  echo Git found: 
  git --version
  echo.
)

REM Ensure Python and Scripts are in PATH
echo %PATH% | find /i "%PY_DIR%" >nul || (
  echo Adding Python to PATH...
  setx PATH "%PATH%;%PY_DIR%" /M >nul
)

echo %PATH% | find /i "%SCRIPTS_DIR%" >nul || (
  echo Adding Python Scripts to PATH...
  setx PATH "%PATH%;%SCRIPTS_DIR%" /M >nul
)

REM Install requirements
echo Installing Python dependencies...
echo.

echo Upgrading pip...
python -m pip install --upgrade pip || goto :pipfail

echo Installing desktop application dependencies...
python -m pip install -r requirements.txt || goto :pipfail

echo Installing mobile backend dependencies...
cd mobile_backend
python -m pip install -r requirements.txt || goto :pipfail
cd ..

echo.
echo ========================================
echo Installation completed successfully!
echo ========================================
echo.
echo What was installed:
echo - Python 3.11.7 (64-bit)
echo - Git for Windows
echo - All required Python packages
echo - Desktop application dependencies
echo - Mobile backend API dependencies
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

:pipfail
echo.
echo ========================================
echo Installation failed!
echo ========================================
echo.
echo Failed to install Python dependencies.
echo This could be due to:
echo - Network connectivity issues
echo - Antivirus blocking the installation
echo - Insufficient permissions
echo.
echo Please try:
echo 1. Check your internet connection
echo 2. Temporarily disable antivirus
echo 3. Run this script as Administrator
echo 4. Install dependencies manually:
echo    python -m pip install -r requirements.txt
echo.
pause
exit /b 1
