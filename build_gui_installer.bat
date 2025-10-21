@echo off
REM Build Professional GUI Installer for HUNGER Restaurant Billing System

echo ========================================
echo HUNGER Restaurant Billing System
echo Professional GUI Installer Builder
echo ========================================
echo.

REM Check if NSIS is installed
makensis /VERSION >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] NSIS found
    makensis /VERSION
) else (
    echo [ERROR] NSIS not found!
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

echo.
echo [INFO] Building professional GUI installer...

REM Create installer assets directory
if not exist "restaurant_billing\assets" mkdir "restaurant_billing\assets"

REM Create placeholder icon (you can replace with real icon)
if not exist "restaurant_billing\assets\icon.ico" (
    echo Creating placeholder icon...
    REM You can replace this with a real .ico file
    copy nul "restaurant_billing\assets\icon.ico" >nul 2>&1
)

REM Create LICENSE.txt if not exists
if not exist "LICENSE.txt" (
    echo Creating LICENSE.txt...
    (
        echo MIT License
        echo.
        echo Copyright ^(c^) 2024 HUNGER Restaurant Billing System
        echo.
        echo Permission is hereby granted, free of charge, to any person obtaining a copy
        echo of this software and associated documentation files ^(the "Software"^), to deal
        echo in the Software without restriction, including without limitation the rights
        echo to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        echo copies of the Software, and to permit persons to whom the Software is
        echo furnished to do so, subject to the following conditions:
        echo.
        echo The above copyright notice and this permission notice shall be included in all
        echo copies or substantial portions of the Software.
        echo.
        echo THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        echo IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        echo FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        echo AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        echo LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        echo OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        echo SOFTWARE.
    ) > LICENSE.txt
)

REM Build the installer
echo [INFO] Compiling NSIS installer...
makensis installer.nsi

if %errorLevel% == 0 (
    echo.
    echo ========================================
    echo SUCCESS! GUI Installer Created
    echo ========================================
    echo.
    echo Output: HUNGER-Restaurant-Billing-Installer.exe
    echo.
    echo Features:
    echo - Professional GUI installer
    echo - Automatic Python dependency installation
    echo - Database initialization
    echo - Desktop shortcuts
    echo - Start menu integration
    echo - Uninstaller
    echo - Registry entries
    echo.
    echo Ready for distribution!
) else (
    echo.
    echo ========================================
    echo ERROR! Installer Build Failed
    echo ========================================
    echo.
    echo Please check the NSIS script for errors.
    echo.
)

echo.
pause
