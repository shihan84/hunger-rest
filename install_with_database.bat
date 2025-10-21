@echo off
echo ========================================
echo HUNGER Restaurant Billing System
echo Complete Installation with Database
echo ========================================
echo.

echo This installer will install:
echo - Python 3.11.7 (includes SQLite database)
echo - Git for Windows
echo - Visual Studio Build Tools
echo - Node.js (for development)
echo - Flutter SDK (for mobile development)
echo - All Python packages
echo - Initialize SQLite database
echo - Create desktop shortcuts
echo.

echo NOTE: No separate database server (MySQL/PostgreSQL) required!
echo SQLite database is built into Python and will be created automatically.
echo.

pause

REM Run the complete installation
call install_everything.bat
