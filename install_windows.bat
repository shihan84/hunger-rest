@echo off
setlocal EnableExtensions EnableDelayedExpansion

REM Detect Python
where python >nul 2>&1
if %errorlevel% neq 0 (
  echo Python not found in PATH.
  echo Please install Python 3.11 (64-bit) from https://www.python.org/downloads/windows/ and re-run this script.
  pause
  exit /b 1
)

for /f "usebackq tokens=*" %%p in (`where python`) do (
  set PY_EXE=%%p
  goto :found
)
:found
for %%d in ("%PY_EXE%") do set PY_DIR=%%~dpd
set PY_DIR=%PY_DIR:~0,-1%
set SCRIPTS_DIR=%PY_DIR%\Scripts

REM Add Python and Scripts to PATH if missing (User PATH)
for /f "tokens=2* delims==" %%A in ('wmic ENVIRONMENT where "name='Path' and username='%username%'^|%systemroot%\System32\findstr /i path" get VariableValue /value') do set USERPATH=%%B
set NEED_SAVE=0

echo %USERPATH% | find /i "%PY_DIR%" >nul || (
  echo Adding %PY_DIR% to user PATH...
  set USERPATH=%USERPATH%;%PY_DIR%
  set NEED_SAVE=1
)

echo %USERPATH% | find /i "%SCRIPTS_DIR%" >nul || (
  echo Adding %SCRIPTS_DIR% to user PATH...
  set USERPATH=%USERPATH%;%SCRIPTS_DIR%
  set NEED_SAVE=1
)

if %NEED_SAVE%==1 (
  setx PATH "%USERPATH%" >nul
  echo Updated PATH. You may need to open a new terminal for changes to take effect.
) else (
  echo PATH already contains Python directories.
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
