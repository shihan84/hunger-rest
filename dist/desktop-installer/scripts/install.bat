@echo off
REM HUNGER Restaurant Billing System - Desktop Installer
REM Complete desktop billing system installer

echo ========================================
echo HUNGER Restaurant Billing System
echo Desktop Installer v1.0.0
echo ========================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Running with administrator privileges
) else (
    echo [ERROR] This installer requires administrator privileges
    echo Please run as Administrator
    pause
    exit /b 1
)

REM Set installation directory
set "INSTALL_DIR=%PROGRAMFILES%\HUNGER Restaurant Billing System"
set "LOG_FILE=%INSTALL_DIR%\install.log"

echo [INFO] Installation directory: %INSTALL_DIR%
echo.

REM Create installation directory
echo [1/8] Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
echo Installation directory created >> "%LOG_FILE%"

REM Check if Python is installed
echo [2/8] Checking Python installation...
python --version >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Python is already installed
    python --version
    echo Python already installed >> "%LOG_FILE%"
) else (
    echo [INFO] Python not found, downloading Python 3.11.7...
    echo Downloading Python 3.11.7 >> "%LOG_FILE%"
    
    powershell -Command "& {Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python-installer.exe'}" 2>>"%LOG_FILE%"
    
    if exist python-installer.exe (
        echo [INFO] Installing Python 3.11.7 (this may take a few minutes)...
        echo Installing Python 3.11.7 >> "%LOG_FILE%"
        python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 2>>"%LOG_FILE%"
        
        REM Refresh PATH
        call refreshenv
        
        REM Verify installation
        python --version >nul 2>&1
        if %errorLevel% == 0 (
            echo [SUCCESS] Python installed successfully
            echo Python installed successfully >> "%LOG_FILE%"
        ) else (
            echo [ERROR] Python installation failed
            echo Python installation failed >> "%LOG_FILE%"
            pause
            exit /b 1
        )
        
        del python-installer.exe
    ) else (
        echo [ERROR] Failed to download Python installer
        echo Python download failed >> "%LOG_FILE%"
        pause
        exit /b 1
    )
)

REM Check if Git is installed
echo [3/8] Checking Git installation...
git --version >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Git is already installed
    git --version
    echo Git already installed >> "%LOG_FILE%"
) else (
    echo [INFO] Git not found, downloading Git for Windows...
    echo Downloading Git for Windows >> "%LOG_FILE%"
    
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe' -OutFile 'git-installer.exe'}" 2>>"%LOG_FILE%"
    
    if exist git-installer.exe (
        echo [INFO] Installing Git for Windows...
        echo Installing Git for Windows >> "%LOG_FILE%"
        git-installer.exe /SILENT /NORESTART 2>>"%LOG_FILE%"
        
        REM Refresh PATH
        call refreshenv
        
        REM Verify installation
        git --version >nul 2>&1
        if %errorLevel% == 0 (
            echo [SUCCESS] Git installed successfully
            echo Git installed successfully >> "%LOG_FILE%"
        ) else (
            echo [ERROR] Git installation failed
            echo Git installation failed >> "%LOG_FILE%"
        )
        
        del git-installer.exe
    ) else (
        echo [ERROR] Failed to download Git installer
        echo Git download failed >> "%LOG_FILE%"
    )
)

REM Copy application files
echo [4/8] Copying application files...
echo Copying application files >> "%LOG_FILE%"

REM Copy all application files
xcopy "app\*" "%INSTALL_DIR%\" /E /I /Y >> "%LOG_FILE%"

echo [SUCCESS] Application files copied
echo Application files copied >> "%LOG_FILE%"

REM Install Python dependencies
echo [5/8] Installing Python dependencies...
echo Installing Python dependencies >> "%LOG_FILE%"

cd /d "%INSTALL_DIR%"

REM Install desktop dependencies
echo [INFO] Installing desktop application dependencies...
pip install -r requirements.txt --quiet --disable-pip-version-check >> "%LOG_FILE%" 2>&1

if %errorLevel% == 0 (
    echo [SUCCESS] Python dependencies installed
    echo Python dependencies installed >> "%LOG_FILE%"
) else (
    echo [WARNING] Some dependencies may not have installed correctly
    echo Some dependencies may not have installed correctly >> "%LOG_FILE%"
)

REM Initialize database
echo [6/8] Initializing database...
echo Initializing database >> "%LOG_FILE%"

python -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized successfully')" >> "%LOG_FILE%" 2>&1

if %errorLevel% == 0 (
    echo [SUCCESS] Database initialized
    echo Database initialized >> "%LOG_FILE%"
) else (
    echo [WARNING] Database initialization may have failed
    echo Database initialization may have failed >> "%LOG_FILE%"
)

REM Create desktop shortcut
echo [7/8] Creating desktop shortcut...
echo Creating desktop shortcut >> "%LOG_FILE%"

set "DESKTOP=%USERPROFILE%\Desktop"
set "SHORTCUT=%DESKTOP%\HUNGER Restaurant Billing System.lnk"

powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = '%INSTALL_DIR%\main.py'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'HUNGER Restaurant Billing System'; $Shortcut.Save()}" >> "%LOG_FILE%" 2>&1

if exist "%SHORTCUT%" (
    echo [SUCCESS] Desktop shortcut created
    echo Desktop shortcut created >> "%LOG_FILE%"
) else (
    echo [WARNING] Desktop shortcut creation failed
    echo Desktop shortcut creation failed >> "%LOG_FILE%"
)

REM Create start menu entry
echo [8/8] Creating start menu entry...
echo Creating start menu entry >> "%LOG_FILE%"

set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "START_SHORTCUT=%START_MENU%\HUNGER Restaurant Billing System.lnk"

powershell -Command "& {$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_SHORTCUT%'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = '%INSTALL_DIR%\main.py'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = 'HUNGER Restaurant Billing System'; $Shortcut.Save()}" >> "%LOG_FILE%" 2>&1

if exist "%START_SHORTCUT%" (
    echo [SUCCESS] Start menu entry created
    echo Start menu entry created >> "%LOG_FILE%"
) else (
    echo [WARNING] Start menu entry creation failed
    echo Start menu entry creation failed >> "%LOG_FILE%"
)

REM Create launcher script
echo [INFO] Creating launcher script...
echo Creating launcher script >> "%LOG_FILE%"

echo @echo off > "%INSTALL_DIR%\start_desktop.bat"
echo cd /d "%INSTALL_DIR%" >> "%INSTALL_DIR%\start_desktop.bat"
echo python main.py >> "%INSTALL_DIR%\start_desktop.bat"
echo pause >> "%INSTALL_DIR%\start_desktop.bat"

echo [SUCCESS] Launcher script created
echo Launcher script created >> "%LOG_FILE%"

REM Installation complete
echo.
echo ========================================
echo INSTALLATION COMPLETE
echo ========================================
echo.
echo [SUCCESS] HUNGER Restaurant Billing System installed successfully!
echo.
echo What was installed:
echo - Python 3.11.7 (if not already present)
echo - Git for Windows (if not already present)
echo - Desktop billing application
echo - SQLite Database (built-in with Python)
echo - Desktop shortcut
echo - Start menu entry
echo.
echo Installation location: %INSTALL_DIR%
echo Log file: %LOG_FILE%
echo.
echo How to start:
echo 1. Double-click the desktop shortcut "HUNGER Restaurant Billing System"
echo 2. Or run: %INSTALL_DIR%\start_desktop.bat
echo 3. Or go to Start Menu ^> HUNGER Restaurant Billing System
echo.
echo Default login credentials:
echo - Username: owner
echo - Password: 1234
echo.
echo [INFO] Installation completed at %date% %time%
echo Installation completed at %date% %time% >> "%LOG_FILE%"

echo.
echo Press any key to launch the application now, or close this window to exit.
pause >nul

REM Launch application
echo [INFO] Launching HUNGER Restaurant Billing System...
cd /d "%INSTALL_DIR%"
python main.py
