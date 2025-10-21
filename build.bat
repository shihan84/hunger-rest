@echo off
setlocal EnableExtensions EnableDelayedExpansion

echo HUNGER Restaurant Billing System - Quick Build Script
echo =====================================================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is required but not found in PATH.
    exit /b 1
)

REM Create distribution directory
echo Creating distribution directory...
mkdir dist\hunger-restaurant-billing 2>nul
mkdir dist\hunger-restaurant-billing\data 2>nul
mkdir dist\hunger-restaurant-billing\mobile_backend 2>nul

REM Copy application files
echo Copying application files...
xcopy /E /I /Y restaurant_billing dist\hunger-restaurant-billing\restaurant_billing
xcopy /E /I /Y mobile_backend dist\hunger-restaurant-billing\mobile_backend
copy main.py dist\hunger-restaurant-billing\
copy requirements.txt dist\hunger-restaurant-billing\
copy mobile_backend\requirements.txt dist\hunger-restaurant-billing\mobile_backend\

REM Copy documentation
echo Copying documentation...
copy README.md dist\hunger-restaurant-billing\ 2>nul
copy INSTALLATION_QUICK_START.md dist\hunger-restaurant-billing\ 2>nul
copy DATABASE_INFO.md dist\hunger-restaurant-billing\ 2>nul
copy INSTALLATION_SUMMARY.md dist\hunger-restaurant-billing\ 2>nul
copy PRODUCTION_READINESS.md dist\hunger-restaurant-billing\ 2>nul
copy AUTOMATIC_UPDATES.md dist\hunger-restaurant-billing\ 2>nul

REM Copy installation scripts
echo Copying installation scripts...
copy install_windows.bat dist\hunger-restaurant-billing\ 2>nul
copy install_simple.bat dist\hunger-restaurant-billing\ 2>nul
copy install_everything.bat dist\hunger-restaurant-billing\ 2>nul
copy install_everything.ps1 dist\hunger-restaurant-billing\ 2>nul
copy install_with_database.bat dist\hunger-restaurant-billing\ 2>nul
copy uninstall.ps1 dist\hunger-restaurant-billing\ 2>nul

REM Create virtual environment
echo Creating virtual environment...
python -m venv dist\hunger-restaurant-billing\venv

REM Install dependencies
echo Installing dependencies...
dist\hunger-restaurant-billing\venv\Scripts\python.exe -m pip install --upgrade pip
dist\hunger-restaurant-billing\venv\Scripts\python.exe -m pip install -r requirements.txt
dist\hunger-restaurant-billing\venv\Scripts\python.exe -m pip install -r mobile_backend\requirements.txt

REM Create launcher scripts
echo Creating launcher scripts...

REM Desktop launcher
echo @echo off > dist\hunger-restaurant-billing\start_desktop.bat
echo cd /d "%%~dp0" >> dist\hunger-restaurant-billing\start_desktop.bat
echo venv\Scripts\python.exe main.py >> dist\hunger-restaurant-billing\start_desktop.bat
echo pause >> dist\hunger-restaurant-billing\start_desktop.bat

REM Mobile launcher
echo @echo off > dist\hunger-restaurant-billing\start_mobile.bat
echo cd /d "%%~dp0\mobile_backend" >> dist\hunger-restaurant-billing\start_mobile.bat
echo ..\venv\Scripts\python.exe main.py >> dist\hunger-restaurant-billing\start_mobile.bat
echo pause >> dist\hunger-restaurant-billing\start_mobile.bat

REM Install script
echo @echo off > dist\hunger-restaurant-billing\install.bat
echo echo Installing HUNGER Restaurant Billing System... >> dist\hunger-restaurant-billing\install.bat
echo. >> dist\hunger-restaurant-billing\install.bat
echo REM Check if Python is available >> dist\hunger-restaurant-billing\install.bat
echo python --version ^>nul 2^>^&1 >> dist\hunger-restaurant-billing\install.bat
echo if %%errorlevel%% neq 0 ( >> dist\hunger-restaurant-billing\install.bat
echo     echo Python is required but not found in PATH. >> dist\hunger-restaurant-billing\install.bat
echo     pause >> dist\hunger-restaurant-billing\install.bat
echo     exit /b 1 >> dist\hunger-restaurant-billing\install.bat
echo ^) >> dist\hunger-restaurant-billing\install.bat
echo. >> dist\hunger-restaurant-billing\install.bat
echo REM Initialize database >> dist\hunger-restaurant-billing\install.bat
echo venv\Scripts\python.exe -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized')" >> dist\hunger-restaurant-billing\install.bat
echo. >> dist\hunger-restaurant-billing\install.bat
echo echo Installation completed! >> dist\hunger-restaurant-billing\install.bat
echo echo To run the desktop application: start_desktop.bat >> dist\hunger-restaurant-billing\install.bat
echo echo To run the mobile backend: start_mobile.bat >> dist\hunger-restaurant-billing\install.bat
echo pause >> dist\hunger-restaurant-billing\install.bat

REM Initialize database
echo Initializing database...
dist\hunger-restaurant-billing\venv\Scripts\python.exe -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized')"

REM Create archive
echo Creating archive...
cd dist
powershell -Command "Compress-Archive -Path 'hunger-restaurant-billing\*' -DestinationPath 'HUNGER-Restaurant-Billing-Windows.zip' -Force"
cd ..

echo Build completed successfully!
echo Package location: dist\hunger-restaurant-billing
echo Archive location: dist\HUNGER-Restaurant-Billing-Windows.zip
echo.
echo To install:
echo 1. Extract the ZIP file
echo 2. Run: install.bat
echo 3. Launch: start_desktop.bat
