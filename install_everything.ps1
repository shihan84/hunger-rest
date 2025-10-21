# HUNGER Restaurant Billing System - Complete Installation Script
# PowerShell script that installs all required software for a fresh Windows system

param(
    [switch]$SkipPython,
    [switch]$SkipGit,
    [switch]$SkipBuildTools,
    [switch]$SkipNodeJS,
    [switch]$SkipFlutter,
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
    
    try {
        $pythonVersion = python --version 2>&1
        Write-ColorOutput "Python already installed: $pythonVersion" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "Python not found. Installing Python 3.11.7..." "Yellow"
    }
    
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
    
    try {
        $gitVersion = git --version 2>&1
        Write-ColorOutput "Git already installed: $gitVersion" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "Git not found. Installing Git..." "Yellow"
    }
    
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

# Function to install Visual Studio Build Tools
function Install-BuildTools {
    Write-ColorOutput "`n=== Installing Visual Studio Build Tools ===" "Cyan"
    
    $buildToolsUrl = "https://aka.ms/vs/17/release/vs_buildtools.exe"
    $buildToolsInstaller = "vs_buildtools.exe"
    
    if (-not (Download-File -Url $buildToolsUrl -OutputPath $buildToolsInstaller -Description "Visual Studio Build Tools")) {
        Write-ColorOutput "Build Tools download failed, continuing..." "Yellow"
        return $true
    }
    
    Write-ColorOutput "Installing Visual Studio Build Tools (this may take a while)..." "Yellow"
    try {
        $process = Start-Process -FilePath $buildToolsInstaller -ArgumentList "--quiet", "--wait", "--add", "Microsoft.VisualStudio.Workload.VCTools", "--includeRecommended" -Wait -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-ColorOutput "Visual Studio Build Tools installed successfully!" "Green"
        } else {
            Write-ColorOutput "Visual Studio Build Tools installation failed, continuing..." "Yellow"
        }
        
        Remove-Item $buildToolsInstaller -Force
        return $true
    }
    catch {
        Write-ColorOutput "Error installing Build Tools: $($_.Exception.Message)" "Red"
        return $true  # Continue even if Build Tools fail
    }
}

# Function to install Node.js
function Install-NodeJS {
    Write-ColorOutput "`n=== Installing Node.js ===" "Cyan"
    
    try {
        $nodeVersion = node --version 2>&1
        Write-ColorOutput "Node.js already installed: $nodeVersion" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "Node.js not found. Installing Node.js..." "Yellow"
    }
    
    $nodeUrl = "https://nodejs.org/dist/v20.10.0/node-v20.10.0-x64.msi"
    $nodeInstaller = "nodejs-installer.msi"
    
    if (-not (Download-File -Url $nodeUrl -OutputPath $nodeInstaller -Description "Node.js")) {
        Write-ColorOutput "Node.js download failed, continuing..." "Yellow"
        return $true
    }
    
    Write-ColorOutput "Installing Node.js..." "Yellow"
    try {
        $process = Start-Process -FilePath "msiexec" -ArgumentList "/i", $nodeInstaller, "/quiet" -Wait -PassThru
        
        if ($process.ExitCode -eq 0) {
            Write-ColorOutput "Node.js installed successfully!" "Green"
        } else {
            Write-ColorOutput "Node.js installation failed, continuing..." "Yellow"
        }
        
        Remove-Item $nodeInstaller -Force
        return $true
    }
    catch {
        Write-ColorOutput "Error installing Node.js: $($_.Exception.Message)" "Red"
        return $true  # Continue even if Node.js fails
    }
}

# Function to install Flutter
function Install-Flutter {
    Write-ColorOutput "`n=== Installing Flutter SDK ===" "Cyan"
    
    try {
        $flutterVersion = flutter --version 2>&1
        Write-ColorOutput "Flutter already installed: $flutterVersion" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "Flutter not found. Installing Flutter SDK..." "Yellow"
    }
    
    $flutterUrl = "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.16.5-stable.zip"
    $flutterZip = "flutter-sdk.zip"
    $flutterPath = "C:\flutter"
    
    if (-not (Download-File -Url $flutterUrl -OutputPath $flutterZip -Description "Flutter SDK")) {
        Write-ColorOutput "Flutter SDK download failed, continuing..." "Yellow"
        return $true
    }
    
    Write-ColorOutput "Extracting Flutter SDK..." "Yellow"
    try {
        Expand-Archive -Path $flutterZip -DestinationPath $flutterPath -Force
        Remove-Item $flutterZip -Force
        
        # Add Flutter to PATH
        $currentPath = [Environment]::GetEnvironmentVariable("PATH", "Machine")
        if ($currentPath -notlike "*$flutterPath\bin*") {
            [Environment]::SetEnvironmentVariable("PATH", "$currentPath;$flutterPath\bin", "Machine")
        }
        
        Write-ColorOutput "Flutter SDK installed successfully!" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "Error installing Flutter: $($_.Exception.Message)" "Red"
        return $true  # Continue even if Flutter fails
    }
}

# Function to install Python dependencies
function Install-PythonDependencies {
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

# Function to initialize database
function Initialize-Database {
    Write-ColorOutput "`n=== Initializing Database ===" "Cyan"
    
    try {
        python -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized successfully')"
        Write-ColorOutput "Database initialized successfully!" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "Database initialization failed, but application will create it on first run" "Yellow"
        return $true  # Continue even if database init fails
    }
}

# Function to create shortcuts
function Create-Shortcuts {
    Write-ColorOutput "`n=== Creating Desktop Shortcuts and Start Menu Entries ===" "Cyan"
    
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
    
    # Start Menu Entries
    $startMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\HUNGER Restaurant"
    New-Item -ItemType Directory -Path $startMenuPath -Force | Out-Null
    
    # Desktop App Start Menu
    $desktopAppStartMenu = "$startMenuPath\HUNGER Restaurant Billing.lnk"
    $Shortcut = $WshShell.CreateShortcut($desktopAppStartMenu)
    $Shortcut.TargetPath = "python"
    $Shortcut.Arguments = "main.py"
    $Shortcut.WorkingDirectory = $currentPath
    $Shortcut.Description = "HUNGER Restaurant Billing System"
    $Shortcut.Save()
    
    # Mobile Backend Start Menu
    $mobileBackendStartMenu = "$startMenuPath\Mobile Backend API.lnk"
    $Shortcut = $WshShell.CreateShortcut($mobileBackendStartMenu)
    $Shortcut.TargetPath = "python"
    $Shortcut.Arguments = "main.py"
    $Shortcut.WorkingDirectory = "$currentPath\mobile_backend"
    $Shortcut.Description = "HUNGER Restaurant Mobile Backend API"
    $Shortcut.Save()
    
    # Uninstaller Start Menu
    $uninstallerStartMenu = "$startMenuPath\Uninstall.lnk"
    $Shortcut = $WshShell.CreateShortcut($uninstallerStartMenu)
    $Shortcut.TargetPath = "powershell"
    $Shortcut.Arguments = "-ExecutionPolicy Bypass -File `"$currentPath\uninstall.ps1`""
    $Shortcut.WorkingDirectory = $currentPath
    $Shortcut.Description = "Uninstall HUNGER Restaurant Billing System"
    $Shortcut.Save()
    
    Write-ColorOutput "Shortcuts created successfully!" "Green"
}

# Main installation process
function Start-CompleteInstallation {
    Write-ColorOutput "========================================" "Magenta"
    Write-ColorOutput "HUNGER Restaurant Billing System" "Magenta"
    Write-ColorOutput "Complete Installation for Fresh Windows" "Magenta"
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
        if (-not (Install-Python)) {
            $success = $false
        }
    }
    
    # Install Git if not skipped
    if (-not $SkipGit -and $success) {
        if (-not (Install-Git)) {
            $success = $false
        }
    }
    
    # Install Build Tools if not skipped
    if (-not $SkipBuildTools -and $success) {
        Install-BuildTools
    }
    
    # Install Node.js if not skipped
    if (-not $SkipNodeJS -and $success) {
        Install-NodeJS
    }
    
    # Install Flutter if not skipped
    if (-not $SkipFlutter -and $success) {
        Install-Flutter
    }
    
    # Install dependencies if not skipped
    if (-not $SkipDependencies -and $success) {
        if (-not (Install-PythonDependencies)) {
            $success = $false
        }
    }
    
    # Initialize database
    if ($success) {
        Initialize-Database
    }
    
    # Create shortcuts
    if ($success) {
        Create-Shortcuts
        
        Write-ColorOutput "`n========================================" "Green"
        Write-ColorOutput "Installation completed successfully!" "Green"
        Write-ColorOutput "========================================" "Green"
        Write-ColorOutput ""
        Write-ColorOutput "What was installed:" "White"
        Write-ColorOutput "- Python 3.11.7 (64-bit)" "White"
        Write-ColorOutput "- Git for Windows" "White"
        Write-ColorOutput "- Visual Studio Build Tools" "White"
        Write-ColorOutput "- Node.js (for development)" "White"
        Write-ColorOutput "- Flutter SDK (for mobile development)" "White"
        Write-ColorOutput "- SQLite Database (built-in with Python)" "White"
        Write-ColorOutput "- All required Python packages" "White"
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
Start-CompleteInstallation
