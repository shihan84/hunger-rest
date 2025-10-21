#!/usr/bin/env python3
"""
Create Desktop-Only Installer
Creates a complete desktop installer with all functionality
"""

import os
import shutil
import zipfile
import subprocess
import sys
from pathlib import Path

class DesktopInstallerCreator:
    def __init__(self):
        self.app_name = "HUNGER Restaurant Billing System"
        self.version = "1.0.0"
        self.install_dir = Path("dist/desktop-installer")
        self.output_dir = Path("dist")
        
    def create_installer_structure(self):
        """Create the installer directory structure"""
        print("📁 Creating installer structure...")
        
        # Create main directories
        self.install_dir.mkdir(parents=True, exist_ok=True)
        (self.install_dir / "app").mkdir(exist_ok=True)
        (self.install_dir / "scripts").mkdir(exist_ok=True)
        (self.install_dir / "assets").mkdir(exist_ok=True)
        
        print("✅ Installer structure created")
        
    def copy_application_files(self):
        """Copy all application files"""
        print("📦 Copying application files...")
        
        # Copy desktop application
        if Path("restaurant_billing").exists():
            shutil.copytree("restaurant_billing", self.install_dir / "app" / "restaurant_billing", dirs_exist_ok=True)
            print("✅ Desktop application copied")
        else:
            print("❌ Desktop application not found")
            return False
            
        # Copy main files
        files_to_copy = [
            "main.py",
            "requirements.txt", 
            "README.md",
            "LICENSE.txt"
        ]
        
        for file in files_to_copy:
            if Path(file).exists():
                shutil.copy2(file, self.install_dir / "app" / file)
                print(f"✅ {file} copied")
            else:
                print(f"⚠️  {file} not found")
                
        return True
        
    def create_installer_scripts(self):
        """Create installation scripts"""
        print("📝 Creating installer scripts...")
        
        # Create main installer script
        installer_script = f'''@echo off
REM {self.app_name} - Desktop Installer
REM Complete desktop billing system installer

echo ========================================
echo {self.app_name}
echo Desktop Installer v{self.version}
echo ========================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Running with administrator privileges
) else (
    echo [ERROR] This installer requires administrator privileges
    echo Please run as Administrator
    pause
    exit /b 1
)

REM Set installation directory
set "INSTALL_DIR=%PROGRAMFILES%\\{self.app_name}"
set "LOG_FILE=%INSTALL_DIR%\\install.log"

echo [INFO] Installation directory: %INSTALL_DIR%
echo.

REM Create installation directory
echo [1/8] Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"
echo Installation directory created >> "%LOG_FILE%"

REM Check if Python is installed
echo [2/8] Checking Python installation...
python --version >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Python is already installed
    python --version
    echo Python already installed >> "%LOG_FILE%"
) else (
    echo [INFO] Python not found, downloading Python 3.11.7...
    echo Downloading Python 3.11.7 >> "%LOG_FILE%"
    
    powershell -Command "& {{Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python-installer.exe'}}" 2>>"%LOG_FILE%"
    
    if exist python-installer.exe (
        echo [INFO] Installing Python 3.11.7 (this may take a few minutes)...
        echo Installing Python 3.11.7 >> "%LOG_FILE%"
        python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0 2>>"%LOG_FILE%"
        
        REM Refresh PATH
        call refreshenv
        
        REM Verify installation
        python --version >nul 2>&1
        if %errorLevel% == 0 (
            echo [SUCCESS] Python installed successfully
            echo Python installed successfully >> "%LOG_FILE%"
        ) else (
            echo [ERROR] Python installation failed
            echo Python installation failed >> "%LOG_FILE%"
            pause
            exit /b 1
        )
        
        del python-installer.exe
    ) else (
        echo [ERROR] Failed to download Python installer
        echo Python download failed >> "%LOG_FILE%"
        pause
        exit /b 1
    )
)

REM Check if Git is installed
echo [3/8] Checking Git installation...
git --version >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Git is already installed
    git --version
    echo Git already installed >> "%LOG_FILE%"
) else (
    echo [INFO] Git not found, downloading Git for Windows...
    echo Downloading Git for Windows >> "%LOG_FILE%"
    
    powershell -Command "& {{Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe' -OutFile 'git-installer.exe'}}" 2>>"%LOG_FILE%"
    
    if exist git-installer.exe (
        echo [INFO] Installing Git for Windows...
        echo Installing Git for Windows >> "%LOG_FILE%"
        git-installer.exe /SILENT /NORESTART 2>>"%LOG_FILE%"
        
        REM Refresh PATH
        call refreshenv
        
        REM Verify installation
        git --version >nul 2>&1
        if %errorLevel% == 0 (
            echo [SUCCESS] Git installed successfully
            echo Git installed successfully >> "%LOG_FILE%"
        ) else (
            echo [ERROR] Git installation failed
            echo Git installation failed >> "%LOG_FILE%"
        )
        
        del git-installer.exe
    ) else (
        echo [ERROR] Failed to download Git installer
        echo Git download failed >> "%LOG_FILE%"
    )
)

REM Copy application files
echo [4/8] Copying application files...
echo Copying application files >> "%LOG_FILE%"

REM Copy all application files
xcopy "app\\*" "%INSTALL_DIR%\\" /E /I /Y >> "%LOG_FILE%"

echo [SUCCESS] Application files copied
echo Application files copied >> "%LOG_FILE%"

REM Install Python dependencies
echo [5/8] Installing Python dependencies...
echo Installing Python dependencies >> "%LOG_FILE%"

cd /d "%INSTALL_DIR%"

REM Install desktop dependencies
echo [INFO] Installing desktop application dependencies...
pip install -r requirements.txt --quiet --disable-pip-version-check >> "%LOG_FILE%" 2>&1

if %errorLevel% == 0 (
    echo [SUCCESS] Python dependencies installed
    echo Python dependencies installed >> "%LOG_FILE%"
) else (
    echo [WARNING] Some dependencies may not have installed correctly
    echo Some dependencies may not have installed correctly >> "%LOG_FILE%"
)

REM Initialize database
echo [6/8] Initializing database...
echo Initializing database >> "%LOG_FILE%"

python -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized successfully')" >> "%LOG_FILE%" 2>&1

if %errorLevel% == 0 (
    echo [SUCCESS] Database initialized
    echo Database initialized >> "%LOG_FILE%"
) else (
    echo [WARNING] Database initialization may have failed
    echo Database initialization may have failed >> "%LOG_FILE%"
)

REM Create desktop shortcut
echo [7/8] Creating desktop shortcut...
echo Creating desktop shortcut >> "%LOG_FILE%"

set "DESKTOP=%USERPROFILE%\\Desktop"
set "SHORTCUT=%DESKTOP%\\{self.app_name}.lnk"

powershell -Command "& {{$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = '%INSTALL_DIR%\\main.py'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = '{self.app_name}'; $Shortcut.Save()}}" >> "%LOG_FILE%" 2>&1

if exist "%SHORTCUT%" (
    echo [SUCCESS] Desktop shortcut created
    echo Desktop shortcut created >> "%LOG_FILE%"
) else (
    echo [WARNING] Desktop shortcut creation failed
    echo Desktop shortcut creation failed >> "%LOG_FILE%"
)

REM Create start menu entry
echo [8/8] Creating start menu entry...
echo Creating start menu entry >> "%LOG_FILE%"

set "START_MENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"
set "START_SHORTCUT=%START_MENU%\\{self.app_name}.lnk"

powershell -Command "& {{$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_SHORTCUT%'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = '%INSTALL_DIR%\\main.py'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = '{self.app_name}'; $Shortcut.Save()}}" >> "%LOG_FILE%" 2>&1

if exist "%START_SHORTCUT%" (
    echo [SUCCESS] Start menu entry created
    echo Start menu entry created >> "%LOG_FILE%"
) else (
    echo [WARNING] Start menu entry creation failed
    echo Start menu entry creation failed >> "%LOG_FILE%"
)

REM Create launcher script
echo [INFO] Creating launcher script...
echo Creating launcher script >> "%LOG_FILE%"

echo @echo off > "%INSTALL_DIR%\\start_desktop.bat"
echo cd /d "%INSTALL_DIR%" >> "%INSTALL_DIR%\\start_desktop.bat"
echo python main.py >> "%INSTALL_DIR%\\start_desktop.bat"
echo pause >> "%INSTALL_DIR%\\start_desktop.bat"

echo [SUCCESS] Launcher script created
echo Launcher script created >> "%LOG_FILE%"

REM Installation complete
echo.
echo ========================================
echo INSTALLATION COMPLETE
echo ========================================
echo.
echo [SUCCESS] {self.app_name} installed successfully!
echo.
echo What was installed:
echo - Python 3.11.7 (if not already present)
echo - Git for Windows (if not already present)
echo - Desktop billing application
echo - SQLite Database (built-in with Python)
echo - Desktop shortcut
echo - Start menu entry
echo.
echo Installation location: %INSTALL_DIR%
echo Log file: %LOG_FILE%
echo.
echo How to start:
echo 1. Double-click the desktop shortcut "{self.app_name}"
echo 2. Or run: %INSTALL_DIR%\\start_desktop.bat
echo 3. Or go to Start Menu ^> {self.app_name}
echo.
echo Default login credentials:
echo - Username: owner
echo - Password: 1234
echo.
echo [INFO] Installation completed at %date% %time%
echo Installation completed at %date% %time% >> "%LOG_FILE%"

echo.
echo Press any key to launch the application now, or close this window to exit.
pause >nul

REM Launch application
echo [INFO] Launching {self.app_name}...
cd /d "%INSTALL_DIR%"
python main.py
'''
        
        with open(self.install_dir / "scripts" / "install.bat", "w") as f:
            f.write(installer_script)
        print("✅ Installer script created")
        
        # Create PowerShell installer
        ps_installer = f'''# {self.app_name} - PowerShell Installer
# Complete desktop billing system installer

param(
    [string]$InstallDir = "${{env:PROGRAMFILES}}\\{self.app_name}"
)

# Set execution policy for current session
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process -Force

# Check for administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {{
    Write-Host "[ERROR] This installer requires administrator privileges" -ForegroundColor Red
    Write-Host "Please run PowerShell as Administrator" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}}

# Set up logging
$LogFile = Join-Path $InstallDir "install.log"
$ErrorActionPreference = "Continue"

function Write-Log {{
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $Message"
    Write-Host $logMessage
    Add-Content -Path $LogFile -Value $logMessage
}}

function Test-Command {{
    param([string]$Command)
    try {{
        $null = Get-Command $Command -ErrorAction Stop
        return $true
    }} catch {{
        return $false
    }}
}}

function Install-Python {{
    Write-Log "[1/8] Checking Python installation..."
    
    if (Test-Command "python") {{
        $pythonVersion = python --version 2>&1
        Write-Log "[INFO] Python is already installed: $pythonVersion"
        return $true
    }}
    
    Write-Log "[INFO] Python not found, downloading Python 3.11.7..."
    
    $pythonUrl = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    $pythonInstaller = "python-installer.exe"
    
    try {{
        Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller -UseBasicParsing
        Write-Log "[INFO] Installing Python 3.11.7 (this may take a few minutes)..."
        
        Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0" -Wait
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        if (Test-Command "python") {{
            Write-Log "[SUCCESS] Python installed successfully"
            Remove-Item $pythonInstaller -Force
            return $true
        }} else {{
            Write-Log "[ERROR] Python installation failed"
            return $false
        }}
    }} catch {{
        Write-Log "[ERROR] Failed to download/install Python: $($_.Exception.Message)"
        return $false
    }}
}}

function Install-Git {{
    Write-Log "[2/8] Checking Git installation..."
    
    if (Test-Command "git") {{
        $gitVersion = git --version 2>&1
        Write-Log "[INFO] Git is already installed: $gitVersion"
        return $true
    }}
    
    Write-Log "[INFO] Git not found, downloading Git for Windows..."
    
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe"
    $gitInstaller = "git-installer.exe"
    
    try {{
        Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller -UseBasicParsing
        Write-Log "[INFO] Installing Git for Windows..."
        
        Start-Process -FilePath $gitInstaller -ArgumentList "/SILENT", "/NORESTART" -Wait
        
        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
        
        if (Test-Command "git") {{
            Write-Log "[SUCCESS] Git installed successfully"
            Remove-Item $gitInstaller -Force
            return $true
        }} else {{
            Write-Log "[ERROR] Git installation failed"
            return $false
        }}
    }} catch {{
        Write-Log "[ERROR] Failed to download/install Git: $($_.Exception.Message)"
        return $false
    }}
}}

function Copy-ApplicationFiles {{
    Write-Log "[3/8] Copying application files..."
    
    # Create installation directory
    if (-not (Test-Path $InstallDir)) {{
        New-Item -ItemType Directory -Path $InstallDir -Force | Out-Null
    }}
    
    # Copy all application files
    Copy-Item -Path "app\\*" -Destination $InstallDir -Recurse -Force
    Write-Log "[SUCCESS] Application files copied"
    return $true
}}

function Install-Dependencies {{
    Write-Log "[4/8] Installing Python dependencies..."
    
    Set-Location $InstallDir
    
    try {{
        Write-Log "[INFO] Installing desktop application dependencies..."
        $result = python -m pip install -r requirements.txt --quiet --disable-pip-version-check 2>&1
        
        if ($LASTEXITCODE -eq 0) {{
            Write-Log "[SUCCESS] Python dependencies installed"
            return $true
        }} else {{
            Write-Log "[WARNING] Some dependencies may not have installed correctly"
            return $true  # Continue anyway
        }}
    }} catch {{
        Write-Log "[WARNING] Dependency installation had issues: $($_.Exception.Message)"
        return $true  # Continue anyway
    }}
}}

function Initialize-Database {{
    Write-Log "[5/8] Initializing database..."
    
    try {{
        $result = python -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized successfully')" 2>&1
        
        if ($LASTEXITCODE -eq 0) {{
            Write-Log "[SUCCESS] Database initialized"
            return $true
        }} else {{
            Write-Log "[WARNING] Database initialization may have failed"
            return $true  # Continue anyway
        }}
    }} catch {{
        Write-Log "[WARNING] Database initialization had issues: $($_.Exception.Message)"
        return $true  # Continue anyway
    }}
}}

function Create-Shortcuts {{
    Write-Log "[6/8] Creating shortcuts and launcher..."
    
    # Create desktop shortcut
    $Desktop = [Environment]::GetFolderPath("Desktop")
    $DesktopShortcut = Join-Path $Desktop "{self.app_name}.lnk"
    
    try {{
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($DesktopShortcut)
        $Shortcut.TargetPath = "python"
        $Shortcut.Arguments = "`"$InstallDir\\main.py`""
        $Shortcut.WorkingDirectory = $InstallDir
        $Shortcut.Description = "{self.app_name}"
        $Shortcut.Save()
        Write-Log "[SUCCESS] Desktop shortcut created"
    }} catch {{
        Write-Log "[WARNING] Desktop shortcut creation failed: $($_.Exception.Message)"
    }}
    
    # Create start menu entry
    $StartMenu = [Environment]::GetFolderPath("StartMenu")
    $StartMenuShortcut = Join-Path $StartMenu "Programs\\{self.app_name}.lnk"
    
    try {{
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($StartMenuShortcut)
        $Shortcut.TargetPath = "python"
        $Shortcut.Arguments = "`"$InstallDir\\main.py`""
        $Shortcut.WorkingDirectory = $InstallDir
        $Shortcut.Description = "{self.app_name}"
        $Shortcut.Save()
        Write-Log "[SUCCESS] Start menu entry created"
    }} catch {{
        Write-Log "[WARNING] Start menu entry creation failed: $($_.Exception.Message)"
    }}
    
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
}}

# Main installation process
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "{self.app_name}" -ForegroundColor Cyan
Write-Host "Desktop Installer v{self.version}" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Log "[INFO] Installation directory: $InstallDir"
Write-Log "[INFO] Log file: $LogFile"

# Run installation steps
$success = $true

if (-not (Install-Python)) {{ $success = $false }}
if (-not (Install-Git)) {{ $success = $false }}
if (-not (Copy-ApplicationFiles)) {{ $success = $false }}
if (-not (Install-Dependencies)) {{ $success = $false }}
if (-not (Initialize-Database)) {{ $success = $false }}
if (-not (Create-Shortcuts)) {{ $success = $false }}

# Installation complete
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "INSTALLATION COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

if ($success) {{
    Write-Host "[SUCCESS] {self.app_name} installed successfully!" -ForegroundColor Green
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
    Write-Host "1. Double-click the desktop shortcut '{self.app_name}'" -ForegroundColor White
    Write-Host "2. Or run: $InstallDir\\start_desktop.bat" -ForegroundColor White
    Write-Host "3. Or go to Start Menu > {self.app_name}" -ForegroundColor White
    Write-Host ""
    Write-Host "Default login credentials:" -ForegroundColor Yellow
    Write-Host "- Username: owner" -ForegroundColor White
    Write-Host "- Password: 1234" -ForegroundColor White
    Write-Host ""
    
    $launch = Read-Host "Press Enter to launch the application now, or type 'n' to exit"
    if ($launch -ne "n") {{
        Write-Host "[INFO] Launching {self.app_name}..." -ForegroundColor Cyan
        Set-Location $InstallDir
        python main.py
    }}
}} else {{
    Write-Host "[ERROR] Installation completed with some issues" -ForegroundColor Red
    Write-Host "Please check the log file: $LogFile" -ForegroundColor Yellow
}}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
'''
        
        with open(self.install_dir / "scripts" / "install.ps1", "w") as f:
            f.write(ps_installer)
        print("✅ PowerShell installer created")
        
    def create_readme(self):
        """Create installation README"""
        print("📖 Creating installation README...")
        
        readme_content = f"""# {self.app_name} - Desktop Installer

## Complete Desktop Billing System

This installer provides a complete desktop billing system with all features:

### Features
- 🧾 **Complete Billing System**: Full restaurant billing with GST compliance
- 💰 **GST Calculation**: Automatic GST calculation and reporting
- 💳 **UPI Integration**: QR code generation for payments
- 👥 **User Management**: Role-based access control
- 📊 **Reports**: Sales reports and analytics
- 🔄 **Auto Updates**: Automatic update notifications
- 🖥️ **Desktop Application**: Native Windows application

### Installation Options

#### Option 1: Batch Installer (Recommended)
1. Run `install.bat` as Administrator
2. Follow the installation prompts
3. Launch from desktop shortcut

#### Option 2: PowerShell Installer
1. Run `install.ps1` in PowerShell as Administrator
2. Follow the installation prompts
3. Launch from desktop shortcut

### System Requirements
- Windows 7 or later
- 4GB RAM minimum
- 500MB free disk space
- Internet connection (for dependency installation)

### What Gets Installed
- Python 3.11.7 (if not present)
- Git for Windows (if not present)
- Desktop billing application
- SQLite Database (built-in)
- Desktop shortcuts
- Start menu entries

### Default Login
- Username: `owner`
- Password: `1234`

### Support
- GitHub: https://github.com/shihan84/hunger-rest
- Issues: https://github.com/shihan84/hunger-rest/issues

### Version
{self.version}
"""
        
        with open(self.install_dir / "README.md", "w") as f:
            f.write(readme_content)
        print("✅ README created")
        
    def create_zip_package(self):
        """Create the final ZIP package"""
        print("📦 Creating ZIP package...")
        
        zip_path = self.output_dir / f"{self.app_name.replace(' ', '-')}-Desktop-Installer.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.install_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(self.install_dir)
                    zipf.write(file_path, arc_path)
                    
        print(f"✅ ZIP package created: {zip_path}")
        return zip_path
        
    def build_installer(self):
        """Build the complete installer"""
        print(f"🚀 Building {self.app_name} Desktop Installer")
        print("=" * 50)
        
        # Create installer structure
        self.create_installer_structure()
        
        # Copy application files
        if not self.copy_application_files():
            print("❌ Failed to copy application files")
            return False
            
        # Create installer scripts
        self.create_installer_scripts()
        
        # Create README
        self.create_readme()
        
        # Create ZIP package
        zip_path = self.create_zip_package()
        
        print("\n" + "=" * 50)
        print("✅ DESKTOP INSTALLER BUILT SUCCESSFULLY")
        print("=" * 50)
        print(f"📦 Output: {zip_path}")
        print(f"📁 Size: {zip_path.stat().st_size / (1024*1024):.1f} MB")
        print("\n🎯 Features:")
        print("- Complete desktop billing system")
        print("- Automatic Python installation")
        print("- Automatic Git installation")
        print("- Desktop shortcuts")
        print("- Start menu integration")
        print("- Database initialization")
        print("- Professional installer scripts")
        print("\n🚀 Ready for distribution!")
        
        return True

def main():
    creator = DesktopInstallerCreator()
    success = creator.build_installer()
    
    if success:
        print("\n💡 Next steps:")
        print("1. Test the installer on a Windows machine")
        print("2. Upload to GitHub releases")
        print("3. Distribute to users")
    else:
        print("\n❌ Installer creation failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
