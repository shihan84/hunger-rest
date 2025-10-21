@echo off
REM Build Professional GUI Installer for HUNGER Restaurant Billing System

echo ========================================
echo Building Professional GUI Installer
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
    REM You can replace this with a real icon file
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

REM Build the installer
echo [INFO] Building installer...
makensis installer.nsi

if %errorLevel% == 0 (
    echo.
    echo ========================================
    echo INSTALLER BUILT SUCCESSFULLY
    echo ========================================
    echo.
    echo Output: HUNGER-Restaurant-Billing-Setup.exe
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
