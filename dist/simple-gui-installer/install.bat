@echo off
REM HUNGER Restaurant Billing System - GUI Installer Launcher

echo ========================================
echo HUNGER Restaurant Billing System
echo Professional GUI Installer
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Python found, launching GUI installer...
    python installer_gui.py
) else (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python 3.11+ from https://python.org
    echo Then run this installer again.
    echo.
    pause
    exit /b 1
)
