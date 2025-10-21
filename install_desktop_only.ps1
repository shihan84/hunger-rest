# HUNGER Restaurant Billing System - Desktop Only Installation
# This script installs only the desktop billing software (no mobile/Flutter components)

param(
    [string]$InstallDir = "C:\HUNGER-Restaurant-Billing"
)

# Set execution policy for current session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Check for administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "[ERROR] This script requires administrator privileges" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Set up logging
$LogFile = Join-Path $InstallDir "install.log"
$ErrorActionPreference = "Continue"

function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Write-Host $logMessage
    Add-Content -Path $LogFile -Value $logMessage
}

function Test-Command {
    param([string]$Command)
    try {
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    } catch {
        return $false
    }
}

function Install-Python {
    Write-Log "[1/6] Checking Python installation..."
    
    if (Test-Command "python") {
        $pythonVersion = python --version 2>&1
        Write-Log "[INFO] Python is already installed: $pythonVersion"
        return $true
    }
    
    Write-Log "[INFO] Python not found, downloading Python 3.11.7..."
    
    $pythonUrl = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    $pythonInstaller = "python-installer.exe"
    
    try {
        Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller -UseBasicParsing
        Write-Log "[INFO] Installing Python 3.11.7 (this may take a few minutes)..."
        
        Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0" -Wait
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        if (Test-Command "python") {
            Write-Log "[SUCCESS] Python installed successfully"
            Remove-Item $pythonInstaller -Force
            return $true
        } else {
            Write-Log "[ERROR] Python installation failed"
            return $false
        }
    } catch {
        Write-Log "[ERROR] Failed to download/install Python: $($_.Exception.Message)"
        return $false
    }
}

function Install-Git {
    Write-Log "[2/6] Checking Git installation..."
    
    if (Test-Command "git") {
        $gitVersion = git --version 2>&1
        Write-Log "[INFO] Git is already installed: $gitVersion"
        return $true
    }
    
    Write-Log "[INFO] Git not found, downloading Git for Windows..."
    
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe"
    $gitInstaller = "git-installer.exe"
    
    try {
        Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller -UseBasicParsing
        Write-Log "[INFO] Installing Git for Windows..."
        
        Start-Process -FilePath $gitInstaller -ArgumentList "/SILENT", "/NORESTART" -Wait
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        if (Test-Command "git") {
            Write-Log "[SUCCESS] Git installed successfully"
            Remove-Item $gitInstaller -Force
            return $true
        } else {
            Write-Log "[ERROR] Git installation failed"
            return $false
        }
    } catch {
        Write-Log "[ERROR] Failed to download/install Git: $($_.Exception.Message)"
        return $false
    }
}

function Copy-ApplicationFiles {
    Write-Log "[3/6] Copying application files..."
    
    # Create installation directory
    if (-not (Test-Path $InstallDir)) {
        New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
    }
    
    # Copy desktop application files
    if (Test-Path "restaurant_billing") {
        Copy-Item -Path "restaurant_billing" -Destination $InstallDir -Recurse -Force
        Write-Log "[SUCCESS] Desktop application copied"
    } else {
        Write-Log "[ERROR] Desktop application files not found"
        return $false
    }
    
    # Copy configuration files
    $filesToCopy = @("requirements.txt", "main.py", "install_windows.bat")
    foreach ($file in $filesToCopy) {
        if (Test-Path $file) {
            Copy-Item -Path $file -Destination $InstallDir -Force
        }
    }
    
    Write-Log "[SUCCESS] Application files copied"
    return $true
}

function Install-Dependencies {
    Write-Log "[4/6] Installing Python dependencies..."
    
    Set-Location $InstallDir
    
    try {
        Write-Log "[INFO] Installing desktop application dependencies..."
        $result = python -m pip install -r requirements.txt --quiet --disable-pip-version-check 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "[SUCCESS] Python dependencies installed"
            return $true
        } else {
            Write-Log "[WARNING] Some dependencies may not have installed correctly"
            return $true  # Continue anyway
        }
    } catch {
        Write-Log "[WARNING] Dependency installation had issues: $($_.Exception.Message)"
        return $true  # Continue anyway
    }
}

function Initialize-Database {
    Write-Log "[5/6] Initializing database..."
    
    try {
        $result = python -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized successfully')" 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Log "[SUCCESS] Database initialized"
            return $true
        } else {
            Write-Log "[WARNING] Database initialization may have failed"
            return $true  # Continue anyway
        }
    } catch {
        Write-Log "[WARNING] Database initialization had issues: $($_.Exception.Message)"
        return $true  # Continue anyway
    }
}

function Create-Shortcuts {
    Write-Log "[6/6] Creating shortcuts and launcher..."
    
    # Create desktop shortcut
    $Desktop = [Environment]::GetFolderPath("Desktop")
    $DesktopShortcut = Join-Path $Desktop "HUNGER Restaurant Billing.lnk"
    
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($DesktopShortcut)
        $Shortcut.TargetPath = "python"
        $Shortcut.Arguments = "`"$InstallDir\main.py`""
        $Shortcut.WorkingDirectory = $InstallDir
        $Shortcut.Description = "HUNGER Restaurant Billing System"
        $Shortcut.Save()
        Write-Log "[SUCCESS] Desktop shortcut created"
    } catch {
        Write-Log "[WARNING] Desktop shortcut creation failed: $($_.Exception.Message)"
    }
    
    # Create start menu entry
    $StartMenu = [Environment]::GetFolderPath("StartMenu")
    $StartMenuShortcut = Join-Path $StartMenu "Programs\HUNGER Restaurant Billing.lnk"
    
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($StartMenuShortcut)
        $Shortcut.TargetPath = "python"
        $Shortcut.Arguments = "`"$InstallDir\main.py`""
        $Shortcut.WorkingDirectory = $InstallDir
        $Shortcut.Description = "HUNGER Restaurant Billing System"
        $Shortcut.Save()
        Write-Log "[SUCCESS] Start menu entry created"
    } catch {
        Write-Log "[WARNING] Start menu entry creation failed: $($_.Exception.Message)"
    }
    
    # Create launcher script
    $LauncherScript = Join-Path $InstallDir "start_desktop.bat"
    @"
@echo off
cd /d "$InstallDir"
python main.py
pause
"@ | Out-File -FilePath $LauncherScript -Encoding ASCII
    
    Write-Log "[SUCCESS] Launcher script created"
    return $true
}

# Main installation process
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "HUNGER Restaurant Billing System" -ForegroundColor Cyan
Write-Host "Desktop-Only Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Log "[INFO] Installation directory: $InstallDir"
Write-Log "[INFO] Log file: $LogFile"

# Run installation steps
$success = $true

if (-not (Install-Python)) { $success = $false }
if (-not (Install-Git)) { $success = $false }
if (-not (Copy-ApplicationFiles)) { $success = $false }
if (-not (Install-Dependencies)) { $success = $false }
if (-not (Initialize-Database)) { $success = $false }
if (-not (Create-Shortcuts)) { $success = $false }

# Installation complete
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "INSTALLATION COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

if ($success) {
    Write-Host "[SUCCESS] HUNGER Restaurant Billing System installed successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "What was installed:" -ForegroundColor Yellow
    Write-Host "- Python 3.11.7 (if not already present)" -ForegroundColor White
    Write-Host "- Git for Windows (if not already present)" -ForegroundColor White
    Write-Host "- Desktop billing application" -ForegroundColor White
    Write-Host "- SQLite Database (built-in with Python)" -ForegroundColor White
    Write-Host "- Desktop shortcut" -ForegroundColor White
    Write-Host "- Start menu entry" -ForegroundColor White
    Write-Host ""
    Write-Host "Installation location: $InstallDir" -ForegroundColor Yellow
    Write-Host "Log file: $LogFile" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "How to start:" -ForegroundColor Yellow
    Write-Host "1. Double-click the desktop shortcut 'HUNGER Restaurant Billing'" -ForegroundColor White
    Write-Host "2. Or run: $InstallDir\start_desktop.bat" -ForegroundColor White
    Write-Host "3. Or go to Start Menu > HUNGER Restaurant Billing" -ForegroundColor White
    Write-Host ""
    Write-Host "Default login credentials:" -ForegroundColor Yellow
    Write-Host "- Username: owner" -ForegroundColor White
    Write-Host "- Password: 1234" -ForegroundColor White
    Write-Host ""
    
    $launch = Read-Host "Press Enter to launch the application now, or type 'n' to exit"
    if ($launch -ne "n") {
        Write-Host "[INFO] Launching HUNGER Restaurant Billing System..." -ForegroundColor Cyan
        Set-Location $InstallDir
        python main.py
    }
} else {
    Write-Host "[ERROR] Installation completed with some issues" -ForegroundColor Red
    Write-Host "Please check the log file: $LogFile" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
