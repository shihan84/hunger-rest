# HUNGER Restaurant Billing System - Uninstaller
# PowerShell script to remove the application

param(
    [switch]$KeepData,
    [switch]$Force
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

# Function to remove shortcuts
function Remove-Shortcuts {
    Write-ColorOutput "Removing desktop shortcuts..." "Yellow"
    
    $desktopPath = [Environment]::GetFolderPath("Desktop")
    $shortcuts = @(
        "$desktopPath\HUNGER Restaurant Billing.lnk",
        "$desktopPath\HUNGER Mobile Backend.lnk"
    )
    
    foreach ($shortcut in $shortcuts) {
        if (Test-Path $shortcut) {
            Remove-Item $shortcut -Force
            Write-ColorOutput "Removed: $shortcut" "Green"
        }
    }
}

# Function to remove start menu entries
function Remove-StartMenuEntries {
    Write-ColorOutput "Removing start menu entries..." "Yellow"
    
    $startMenuPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\HUNGER Restaurant"
    
    if (Test-Path $startMenuPath) {
        Remove-Item $startMenuPath -Recurse -Force
        Write-ColorOutput "Removed start menu folder: $startMenuPath" "Green"
    }
}

# Function to remove Python packages
function Remove-PythonPackages {
    Write-ColorOutput "Removing Python packages..." "Yellow"
    
    try {
        $packages = @(
            "pillow",
            "qrcode", 
            "python-dateutil",
            "num2words",
            "python-escpos",
            "python-telegram-bot",
            "fastapi",
            "uvicorn",
            "websockets",
            "python-jose",
            "python-multipart",
            "pydantic"
        )
        
        foreach ($package in $packages) {
            try {
                python -m pip uninstall $package -y 2>$null
                Write-ColorOutput "Removed package: $package" "Green"
            }
            catch {
                Write-ColorOutput "Package not found or already removed: $package" "Gray"
            }
        }
    }
    catch {
        Write-ColorOutput "Error removing Python packages: $($_.Exception.Message)" "Red"
    }
}

# Function to backup data
function Backup-Data {
    if ($KeepData) {
        Write-ColorOutput "Backing up data..." "Yellow"
        
        $backupPath = "HUNGER_Restaurant_Backup_$(Get-Date -Format 'yyyy-MM-dd_HH-mm-ss')"
        New-Item -ItemType Directory -Path $backupPath -Force | Out-Null
        
        # Backup database
        if (Test-Path "data\restaurant.db") {
            Copy-Item "data\restaurant.db" "$backupPath\restaurant.db"
            Write-ColorOutput "Database backed up to: $backupPath\restaurant.db" "Green"
        }
        
        # Backup config
        if (Test-Path "restaurant_billing\config.py") {
            Copy-Item "restaurant_billing\config.py" "$backupPath\config.py"
            Write-ColorOutput "Config backed up to: $backupPath\config.py" "Green"
        }
        
        # Backup invoices
        if (Test-Path "invoices") {
            Copy-Item "invoices" "$backupPath\invoices" -Recurse
            Write-ColorOutput "Invoices backed up to: $backupPath\invoices" "Green"
        }
        
        Write-ColorOutput "Data backup completed: $backupPath" "Green"
    }
}

# Function to remove application files
function Remove-ApplicationFiles {
    Write-ColorOutput "Removing application files..." "Yellow"
    
    $currentPath = Get-Location
    
    if (-not $KeepData) {
        # Remove data folder
        if (Test-Path "data") {
            Remove-Item "data" -Recurse -Force
            Write-ColorOutput "Removed data folder" "Green"
        }
        
        # Remove invoices folder
        if (Test-Path "invoices") {
            Remove-Item "invoices" -Recurse -Force
            Write-ColorOutput "Removed invoices folder" "Green"
        }
    }
    
    # Remove Python cache
    if (Test-Path "__pycache__") {
        Remove-Item "__pycache__" -Recurse -Force
        Write-ColorOutput "Removed Python cache" "Green"
    }
    
    if (Test-Path "restaurant_billing\__pycache__") {
        Remove-Item "restaurant_billing\__pycache__" -Recurse -Force
        Write-ColorOutput "Removed restaurant_billing cache" "Green"
    }
    
    if (Test-Path "mobile_backend\__pycache__") {
        Remove-Item "mobile_backend\__pycache__" -Recurse -Force
        Write-ColorOutput "Removed mobile_backend cache" "Green"
    }
    
    # Remove log files
    Get-ChildItem -Path . -Filter "*.log" | Remove-Item -Force
    Write-ColorOutput "Removed log files" "Green"
}

# Main uninstallation process
function Start-Uninstallation {
    Write-ColorOutput "========================================" "Magenta"
    Write-ColorOutput "HUNGER Restaurant Billing System" "Magenta"
    Write-ColorOutput "Uninstaller" "Magenta"
    Write-ColorOutput "========================================" "Magenta"
    Write-ColorOutput ""
    
    # Check if running as Administrator
    if (-not (Test-Administrator)) {
        Write-ColorOutput "This script requires Administrator privileges." "Red"
        Write-ColorOutput "Please right-click and select 'Run as administrator'" "Red"
        Read-Host "Press Enter to exit"
        exit 1
    }
    
    # Confirmation
    if (-not $Force) {
        Write-ColorOutput "This will uninstall HUNGER Restaurant Billing System." "Yellow"
        if ($KeepData) {
            Write-ColorOutput "Data will be backed up before removal." "Yellow"
        } else {
            Write-ColorOutput "All data will be permanently deleted!" "Red"
        }
        Write-ColorOutput ""
        
        $confirm = Read-Host "Are you sure you want to continue? (y/n)"
        if ($confirm -ne "y" -and $confirm -ne "Y") {
            Write-ColorOutput "Uninstallation cancelled." "Yellow"
            exit 0
        }
    }
    
    Write-ColorOutput "Starting uninstallation..." "Yellow"
    Write-ColorOutput ""
    
    # Backup data if requested
    Backup-Data
    
    # Remove shortcuts
    Remove-Shortcuts
    
    # Remove start menu entries
    Remove-StartMenuEntries
    
    # Remove Python packages
    Remove-PythonPackages
    
    # Remove application files
    Remove-ApplicationFiles
    
    Write-ColorOutput ""
    Write-ColorOutput "========================================" "Green"
    Write-ColorOutput "Uninstallation completed!" "Green"
    Write-ColorOutput "========================================" "Green"
    Write-ColorOutput ""
    
    if ($KeepData) {
        Write-ColorOutput "Data has been backed up and can be restored later." "Green"
    }
    
    Write-ColorOutput "Note: Python and Git are still installed on your system." "Yellow"
    Write-ColorOutput "If you want to remove them, please do so manually." "Yellow"
    Write-ColorOutput ""
    
    Read-Host "Press Enter to exit"
}

# Run the uninstallation
Start-Uninstallation
