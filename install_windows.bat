@echo off
setlocal

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
  echo Python not found. Please install Python 3.11 from https://www.python.org/downloads/windows/
  pause
  exit /b 1
)

REM Install requirements
python -m pip install --upgrade pip
python -m pip install -r requirements.txt || goto :pipfail

echo Installation complete.
echo To run: python main.py
pause
exit /b 0

:pipfail
echo Failed to install dependencies.
pause
exit /b 1
