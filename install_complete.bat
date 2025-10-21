@echo off
echo ========================================
echo HUNGER Restaurant Billing System
echo Complete Installation Launcher
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

echo Launching PowerShell installer...
echo.

REM Launch the PowerShell installer
powershell -ExecutionPolicy Bypass -File "install_windows_complete.ps1"

pause
