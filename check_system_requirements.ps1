# HUNGER Restaurant Billing System - System Requirements Checker
# PowerShell script to verify system compatibility

# Function to write colored output
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

# Function to check Windows version
function Test-WindowsVersion {
    Write-ColorOutput "`n=== Windows Version Check ===" "Cyan"
    
    $osVersion = [System.Environment]::OSVersion.Version
    $windowsVersion = "$($osVersion.Major).$($osVersion.Minor)"
    
    Write-ColorOutput "Windows Version: $windowsVersion" "White"
    
    if ($osVersion.Major -eq 10 -and $osVersion.Minor -ge 0) {
        Write-ColorOutput "✓ Windows 10/11 detected - Compatible" "Green"
        return $true
    } elseif ($osVersion.Major -eq 6 -and $osVersion.Minor -ge 1) {
        Write-ColorOutput "⚠ Windows 7/8/8.1 detected - May work but not officially supported" "Yellow"
        return $true
    } else {
        Write-ColorOutput "✗ Unsupported Windows version - Please upgrade to Windows 10 or 11" "Red"
        return $false
    }
}

# Function to check system architecture
function Test-SystemArchitecture {
    Write-ColorOutput "`n=== System Architecture Check ===" "Cyan"
    
    $arch = [System.Environment]::GetEnvironmentVariable("PROCESSOR_ARCHITECTURE")
    Write-ColorOutput "System Architecture: $arch" "White"
    
    if ($arch -eq "AMD64") {
        Write-ColorOutput "✓ 64-bit system detected - Compatible" "Green"
        return $true
    } else {
        Write-ColorOutput "✗ 32-bit system detected - Not compatible (64-bit required)" "Red"
        return $false
    }
}

# Function to check available memory
function Test-Memory {
    Write-ColorOutput "`n=== Memory Check ===" "Cyan"
    
    $memory = Get-WmiObject -Class Win32_ComputerSystem | Select-Object -ExpandProperty TotalPhysicalMemory
    $memoryGB = [math]::Round($memory / 1GB, 2)
    
    Write-ColorOutput "Total RAM: $memoryGB GB" "White"
    
    if ($memoryGB -ge 4) {
        Write-ColorOutput "✓ Sufficient memory available" "Green"
        return $true
    } elseif ($memoryGB -ge 2) {
        Write-ColorOutput "⚠ Low memory - May experience performance issues" "Yellow"
        return $true
    } else {
        Write-ColorOutput "✗ Insufficient memory - Minimum 2GB required" "Red"
        return $false
    }
}

# Function to check available disk space
function Test-DiskSpace {
    Write-ColorOutput "`n=== Disk Space Check ===" "Cyan"
    
    $drive = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'"
    $freeSpaceGB = [math]::Round($drive.FreeSpace / 1GB, 2)
    $totalSpaceGB = [math]::Round($drive.Size / 1GB, 2)
    
    Write-ColorOutput "C: Drive - Free: $freeSpaceGB GB / Total: $totalSpaceGB GB" "White"
    
    if ($freeSpaceGB -ge 2) {
        Write-ColorOutput "✓ Sufficient disk space available" "Green"
        return $true
    } elseif ($freeSpaceGB -ge 1) {
        Write-ColorOutput "⚠ Low disk space - May need cleanup" "Yellow"
        return $true
    } else {
        Write-ColorOutput "✗ Insufficient disk space - Minimum 1GB required" "Red"
        return $false
    }
}

# Function to check network connectivity
function Test-NetworkConnectivity {
    Write-ColorOutput "`n=== Network Connectivity Check ===" "Cyan"
    
    try {
        $response = Test-NetConnection -ComputerName "www.python.org" -Port 443 -InformationLevel Quiet
        if ($response) {
            Write-ColorOutput "✓ Internet connectivity available" "Green"
            return $true
        } else {
            Write-ColorOutput "✗ No internet connectivity - Required for installation" "Red"
            return $false
        }
    }
    catch {
        Write-ColorOutput "✗ Network test failed - Please check your internet connection" "Red"
        return $false
    }
}

# Function to check if running as Administrator
function Test-Administrator {
    Write-ColorOutput "`n=== Administrator Privileges Check ===" "Cyan"
    
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    $isAdmin = $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
    
    if ($isAdmin) {
        Write-ColorOutput "✓ Running as Administrator" "Green"
        return $true
    } else {
        Write-ColorOutput "⚠ Not running as Administrator - Required for installation" "Yellow"
        Write-ColorOutput "  Please right-click and select 'Run as administrator'" "Yellow"
        return $false
    }
}

# Function to check existing Python installation
function Test-PythonInstallation {
    Write-ColorOutput "`n=== Python Installation Check ===" "Cyan"
    
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3\.(11|12)") {
            Write-ColorOutput "✓ Python $pythonVersion found - Compatible" "Green"
            return $true
        } elseif ($pythonVersion -match "Python 3\.") {
            Write-ColorOutput "⚠ $pythonVersion found - May work but Python 3.11+ recommended" "Yellow"
            return $true
        } else {
            Write-ColorOutput "⚠ $pythonVersion found - Python 3.11+ recommended" "Yellow"
            return $true
        }
    }
    catch {
        Write-ColorOutput "✗ Python not found - Will be installed automatically" "Yellow"
        return $true
    }
}

# Function to check existing Git installation
function Test-GitInstallation {
    Write-ColorOutput "`n=== Git Installation Check ===" "Cyan"
    
    try {
        $gitVersion = git --version 2>&1
        Write-ColorOutput "✓ $gitVersion found" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "✗ Git not found - Will be installed automatically" "Yellow"
        return $true
    }
}

# Function to check antivirus software
function Test-AntivirusSoftware {
    Write-ColorOutput "`n=== Antivirus Software Check ===" "Cyan"
    
    $antivirusProducts = Get-WmiObject -Namespace "root\SecurityCenter2" -Class AntiVirusProduct -ErrorAction SilentlyContinue
    
    if ($antivirusProducts) {
        foreach ($product in $antivirusProducts) {
            Write-ColorOutput "Antivirus: $($product.displayName)" "White"
        }
        Write-ColorOutput "⚠ Antivirus software detected - May need to add exclusions" "Yellow"
        Write-ColorOutput "  Add the project folder to antivirus exclusions if installation fails" "Yellow"
    } else {
        Write-ColorOutput "✓ No antivirus software detected or accessible" "Green"
    }
    
    return $true
}

# Function to check Windows Defender status
function Test-WindowsDefender {
    Write-ColorOutput "`n=== Windows Defender Check ===" "Cyan"
    
    try {
        $defenderStatus = Get-MpComputerStatus -ErrorAction SilentlyContinue
        if ($defenderStatus) {
            Write-ColorOutput "Windows Defender Status: $($defenderStatus.AntivirusEnabled)" "White"
            Write-ColorOutput "Real-time Protection: $($defenderStatus.RealTimeProtectionEnabled)" "White"
            
            if ($defenderStatus.AntivirusEnabled) {
                Write-ColorOutput "⚠ Windows Defender is active - May need to add exclusions" "Yellow"
                Write-ColorOutput "  Add the project folder to Windows Defender exclusions if needed" "Yellow"
            }
        } else {
            Write-ColorOutput "✓ Windows Defender status not accessible" "Green"
        }
    }
    catch {
        Write-ColorOutput "✓ Windows Defender check skipped" "Green"
    }
    
    return $true
}

# Function to check firewall status
function Test-FirewallStatus {
    Write-ColorOutput "`n=== Windows Firewall Check ===" "Cyan"
    
    try {
        $firewallProfiles = Get-NetFirewallProfile
        foreach ($profile in $firewallProfiles) {
            Write-ColorOutput "$($profile.Name) Profile: $($profile.Enabled)" "White"
        }
        
        Write-ColorOutput "✓ Firewall status checked" "Green"
        Write-ColorOutput "  You may need to allow Python through firewall" "Yellow"
    }
    catch {
        Write-ColorOutput "✓ Firewall check skipped" "Green"
    }
    
    return $true
}

# Main system requirements check
function Start-SystemCheck {
    Write-ColorOutput "========================================" "Magenta"
    Write-ColorOutput "HUNGER Restaurant Billing System" "Magenta"
    Write-ColorOutput "System Requirements Checker" "Magenta"
    Write-ColorOutput "========================================" "Magenta"
    
    $allChecks = @()
    
    # Run all checks
    $allChecks += Test-WindowsVersion
    $allChecks += Test-SystemArchitecture
    $allChecks += Test-Memory
    $allChecks += Test-DiskSpace
    $allChecks += Test-NetworkConnectivity
    $allChecks += Test-Administrator
    $allChecks += Test-PythonInstallation
    $allChecks += Test-GitInstallation
    $allChecks += Test-AntivirusSoftware
    $allChecks += Test-WindowsDefender
    $allChecks += Test-FirewallStatus
    
    # Summary
    Write-ColorOutput "`n========================================" "Magenta"
    Write-ColorOutput "System Requirements Summary" "Magenta"
    Write-ColorOutput "========================================" "Magenta"
    
    $passedChecks = ($allChecks | Where-Object { $_ -eq $true }).Count
    $totalChecks = $allChecks.Count
    
    Write-ColorOutput "Checks Passed: $passedChecks / $totalChecks" "White"
    
    if ($passedChecks -eq $totalChecks) {
        Write-ColorOutput "✓ System is ready for installation!" "Green"
        Write-ColorOutput ""
        Write-ColorOutput "You can now run the installation script:" "White"
        Write-ColorOutput "  install_windows.bat" "Gray"
        Write-ColorOutput "  or" "Gray"
        Write-ColorOutput "  install_windows_complete.ps1" "Gray"
    } else {
        Write-ColorOutput "⚠ Some issues detected - Please resolve before installation" "Yellow"
        Write-ColorOutput ""
        Write-ColorOutput "Common solutions:" "White"
        Write-ColorOutput "1. Run as Administrator" "Gray"
        Write-ColorOutput "2. Check internet connection" "Gray"
        Write-ColorOutput "3. Free up disk space" "Gray"
        Write-ColorOutput "4. Add antivirus exclusions" "Gray"
        Write-ColorOutput "5. Upgrade to Windows 10/11" "Gray"
    }
    
    Write-ColorOutput ""
    Read-Host "Press Enter to exit"
}

# Run the system check
Start-SystemCheck
