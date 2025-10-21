# HUNGER Restaurant Billing System - Complete Windows Installer
# PowerShell script for fresh Windows 10/11 installation

param(
    [switch]$SkipPython,
    [switch]$SkipGit,
    [switch]$SkipDependencies,
    [switch]$LaunchApp
)

# Set execution policy for this session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Function to write colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Function to check if running as Administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Function to download file with progress
function Download-File {
    param(
        [string]$Url,
        [string]$OutputPath,
        [string]$Description
    )
    
    Write-ColorOutput "Downloading $Description..." "Yellow"
    try {
        $ProgressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $Url -OutFile $OutputPath -UseBasicParsing
        Write-ColorOutput "$Description downloaded successfully!" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "Failed to download $Description`: $($_.Exception.Message)" "Red"
        return $false
    }
}

# Function to install Python
function Install-Python {
    Write-ColorOutput "`n=== Installing Python 3.11.7 ===" "Cyan"
    
    $pythonUrl = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    $pythonInstaller = "python-installer.exe"
    
    if (-not (Download-File -Url $pythonUrl -OutputPath $pythonInstaller -Description "Python 3.11.7")) {
        return $false
    }
    
    Write-ColorOutput "Installing Python 3.11.7..." "Yellow"
    try {
        $process = Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0" -Wait -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-ColorOutput "Python installed successfully!" "Green"
            Remove-Item $pythonInstaller -Force
            return $true
        } else {
            Write-ColorOutput "Python installation failed with exit code: $($process.ExitCode)" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "Error installing Python: $($_.Exception.Message)" "Red"
        return $false
    }
}

# Function to install Git
function Install-Git {
    Write-ColorOutput "`n=== Installing Git for Windows ===" "Cyan"
    
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitInstaller = "git-installer.exe"
    
    if (-not (Download-File -Url $gitUrl -OutputPath $gitInstaller -Description "Git for Windows")) {
        return $false
    }
    
    Write-ColorOutput "Installing Git..." "Yellow"
    try {
        $process = Start-Process -FilePath $gitInstaller -ArgumentList "/SILENT", "/NORESTART", "/NOCANCEL", "/SP-", "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS", "/COMPONENTS=`"icons,ext\reg\shellhere,assoc,assoc_sh`"" -Wait -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-ColorOutput "Git installed successfully!" "Green"
            Remove-Item $gitInstaller -Force
            return $true
        } else {
            Write-ColorOutput "Git installation failed with exit code: $($process.ExitCode)" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "Error installing Git: $($_.Exception.Message)" "Red"
        return $false
    }
}

# Function to install Python dependencies
function Install-Dependencies {
    Write-ColorOutput "`n=== Installing Python Dependencies ===" "Cyan"
    
    # Refresh PATH
    $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
    
    # Check if Python is available
    try {
        $pythonVersion = python --version 2>&1
        Write-ColorOutput "Using Python: $pythonVersion" "Green"
    }
    catch {
        Write-ColorOutput "Python not found in PATH. Please restart your terminal or reboot." "Red"
        return $false
    }
    
    # Upgrade pip
    Write-ColorOutput "Upgrading pip..." "Yellow"
    try {
        python -m pip install --upgrade pip
        Write-ColorOutput "pip upgraded successfully!" "Green"
    }
    catch {
        Write-ColorOutput "Failed to upgrade pip: $($_.Exception.Message)" "Red"
        return $false
    }
    
    # Install desktop dependencies
    Write-ColorOutput "Installing desktop application dependencies..." "Yellow"
    try {
        python -m pip install -r requirements.txt
        Write-ColorOutput "Desktop dependencies installed!" "Green"
    }
    catch {
        Write-ColorOutput "Failed to install desktop dependencies: $($_.Exception.Message)" "Red"
        return $false
    }
    
    # Install mobile backend dependencies
    Write-ColorOutput "Installing mobile backend dependencies..." "Yellow"
    try {
        Set-Location mobile_backend
        python -m pip install -r requirements.txt
        Set-Location ..
        Write-ColorOutput "Mobile backend dependencies installed!" "Green"
    }
    catch {
        Write-ColorOutput "Failed to install mobile backend dependencies: $($_.Exception.Message)" "Red"
        Set-Location ..
        return $false
    }
    
    return $true
}

# Function to create desktop shortcuts
function Create-Shortcuts {
    Write-ColorOutput "`n=== Creating Desktop Shortcuts ===" "Cyan"
    
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $currentPath = Get-Location
    
    # Desktop App Shortcut
    $desktopAppShortcut = "$desktopPath\HUNGER Restaurant Billing.lnk"
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($desktopAppShortcut)
    $Shortcut.TargetPath = "python"
    $Shortcut.Arguments = "main.py"
    $Shortcut.WorkingDirectory = $currentPath
    $Shortcut.Description = "HUNGER Restaurant Billing System"
    $Shortcut.Save()
    
    # Mobile Backend Shortcut
    $mobileBackendShortcut = "$desktopPath\HUNGER Mobile Backend.lnk"
    $Shortcut = $WshShell.CreateShortcut($mobileBackendShortcut)
    $Shortcut.TargetPath = "python"
    $Shortcut.Arguments = "main.py"
    $Shortcut.WorkingDirectory = "$currentPath\mobile_backend"
    $Shortcut.Description = "HUNGER Restaurant Mobile Backend API"
    $Shortcut.Save()
    
    Write-ColorOutput "Desktop shortcuts created!" "Green"
}

# Function to create start menu entries
function Create-StartMenuEntries {
    Write-ColorOutput "`n=== Creating Start Menu Entries ===" "Cyan"
    
    $startMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\HUNGER Restaurant"
    New-Item -ItemType Directory -Path $startMenuPath -Force | Out-Null
    
    $currentPath = Get-Location
    
    # Desktop App
    $desktopAppShortcut = "$startMenuPath\HUNGER Restaurant Billing.lnk"
    $WshShell = New-Object -comObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($desktopAppShortcut)
    $Shortcut.TargetPath = "python"
    $Shortcut.Arguments = "main.py"
    $Shortcut.WorkingDirectory = $currentPath
    $Shortcut.Description = "HUNGER Restaurant Billing System"
    $Shortcut.Save()
    
    # Mobile Backend
    $mobileBackendShortcut = "$startMenuPath\Mobile Backend API.lnk"
    $Shortcut = $WshShell.CreateShortcut($mobileBackendShortcut)
    $Shortcut.TargetPath = "python"
    $Shortcut.Arguments = "main.py"
    $Shortcut.WorkingDirectory = "$currentPath\mobile_backend"
    $Shortcut.Description = "HUNGER Restaurant Mobile Backend API"
    $Shortcut.Save()
    
    # Uninstaller
    $uninstallerShortcut = "$startMenuPath\Uninstall.lnk"
    $Shortcut = $WshShell.CreateShortcut($uninstallerShortcut)
    $Shortcut.TargetPath = "powershell"
    $Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$currentPath\uninstall.ps1`""
    $Shortcut.WorkingDirectory = $currentPath
    $Shortcut.Description = "Uninstall HUNGER Restaurant Billing System"
    $Shortcut.Save()
    
    Write-ColorOutput "Start menu entries created!" "Green"
}

# Main installation process
function Start-Installation {
    Write-ColorOutput "========================================" "Magenta"
    Write-ColorOutput "HUNGER Restaurant Billing System" "Magenta"
    Write-ColorOutput "Complete Windows Installation" "Magenta"
    Write-ColorOutput "========================================" "Magenta"
    Write-ColorOutput ""
    
    # Check if running as Administrator
    if (-not (Test-Administrator)) {
        Write-ColorOutput "This script requires Administrator privileges." "Red"
        Write-ColorOutput "Please right-click and select 'Run as administrator'" "Red"
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Check Windows version
    $osVersion = [System.Environment]::OSVersion.Version
    Write-ColorOutput "Windows Version: $($osVersion.Major).$($osVersion.Minor)" "White"
    Write-ColorOutput ""
    
    $success = $true
    
    # Install Python if not skipped
    if (-not $SkipPython) {
        try {
            $pythonVersion = python --version 2>&1
            Write-ColorOutput "Python already installed: $pythonVersion" "Green"
        }
        catch {
            if (-not (Install-Python)) {
                $success = $false
            }
        }
    }
    
    # Install Git if not skipped
    if (-not $SkipGit -and $success) {
        try {
            $gitVersion = git --version 2>&1
            Write-ColorOutput "Git already installed: $gitVersion" "Green"
        }
        catch {
            if (-not (Install-Git)) {
                $success = $false
            }
        }
    }
    
    # Install dependencies if not skipped
    if (-not $SkipDependencies -and $success) {
        if (-not (Install-Dependencies)) {
            $success = $false
        }
    }
    
    # Create shortcuts and start menu entries
    if ($success) {
        Create-Shortcuts
        Create-StartMenuEntries
        
        Write-ColorOutput "`n========================================" "Green"
        Write-ColorOutput "Installation completed successfully!" "Green"
        Write-ColorOutput "========================================" "Green"
        Write-ColorOutput ""
        Write-ColorOutput "What was installed:" "White"
        Write-ColorOutput "- Python 3.11.7 (64-bit)" "White"
        Write-ColorOutput "- Git for Windows" "White"
        Write-ColorOutput "- All required Python packages" "White"
        Write-ColorOutput "- Desktop application dependencies" "White"
        Write-ColorOutput "- Mobile backend API dependencies" "White"
        Write-ColorOutput "- Desktop shortcuts" "White"
        Write-ColorOutput "- Start menu entries" "White"
        Write-ColorOutput ""
        Write-ColorOutput "First login credentials:" "Yellow"
        Write-ColorOutput "Username: owner" "Yellow"
        Write-ColorOutput "Password: 1234" "Yellow"
        Write-ColorOutput ""
        Write-ColorOutput "To run the desktop application:" "White"
        Write-ColorOutput "  python main.py" "Gray"
        Write-ColorOutput "  or double-click the desktop shortcut" "Gray"
        Write-ColorOutput ""
        Write-ColorOutput "To run the mobile backend API:" "White"
        Write-ColorOutput "  cd mobile_backend" "Gray"
        Write-ColorOutput "  python main.py" "Gray"
        Write-ColorOutput "  or double-click the mobile backend shortcut" "Gray"
        Write-ColorOutput ""
        
        if ($LaunchApp) {
            Write-ColorOutput "Launching HUNGER Restaurant Billing System..." "Yellow"
            Start-Process python -ArgumentList "main.py" -WorkingDirectory (Get-Location)
        } else {
            $launch = Read-Host "Would you like to launch the application now? (y/n)"
            if ($launch -eq "y" -or $launch -eq "Y") {
                Write-ColorOutput "Launching HUNGER Restaurant Billing System..." "Yellow"
                Start-Process python -ArgumentList "main.py" -WorkingDirectory (Get-Location)
            }
        }
    } else {
        Write-ColorOutput "`n========================================" "Red"
        Write-ColorOutput "Installation failed!" "Red"
        Write-ColorOutput "========================================" "Red"
        Write-ColorOutput ""
        Write-ColorOutput "Please check the error messages above and try again." "Red"
        Write-ColorOutput "Common solutions:" "Yellow"
        Write-ColorOutput "1. Check your internet connection" "White"
        Write-ColorOutput "2. Temporarily disable antivirus" "White"
        Write-ColorOutput "3. Run this script as Administrator" "White"
        Write-ColorOutput "4. Install dependencies manually" "White"
        Write-ColorOutput ""
    }
    
    Read-Host "Press Enter to exit"
}

# Run the installation
Start-Installation
