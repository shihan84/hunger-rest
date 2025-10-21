#!/usr/bin/env python3
"""
Create Fixed Installer Package
Creates a robust installer package with better error handling
"""

import os
import shutil
import zipfile
from pathlib import Path

class FixedInstallerCreator:
    def __init__(self):
        self.app_name = "HUNGER Restaurant Billing System"
        self.version = "1.0.0"
        self.install_dir = Path("dist/fixed-installer")
        self.output_dir = Path("dist")
        
    def create_installer_structure(self):
        """Create the installer directory structure"""
        print("📁 Creating fixed installer structure...")
        
        # Create main directory
        self.install_dir.mkdir(parents=True, exist_ok=True)
        
        print("✅ Fixed installer structure created")
        
    def copy_application_files(self):
        """Copy all application files"""
        print("📦 Copying application files...")
        
        # Copy desktop application
        if Path("restaurant_billing").exists():
            shutil.copytree("restaurant_billing", self.install_dir / "restaurant_billing", dirs_exist_ok=True)
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
                shutil.copy2(file, self.install_dir / file)
                print(f"✅ {file} copied")
            else:
                print(f"⚠️  {file} not found")
                
        return True
        
    def create_robust_installer(self):
        """Create a robust installer with better error handling"""
        print("📝 Creating robust installer...")
        
        installer_script = f'''@echo off
setlocal enabledelayedexpansion
REM {self.app_name} - Robust Installer
REM Complete desktop billing system installer with error handling

echo ========================================
echo {self.app_name}
echo Robust Installer v{self.version}
echo ========================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] This installer requires administrator privileges
    echo Please run as Administrator
    echo.
    pause
    exit /b 1
)

echo [INFO] Running with administrator privileges
echo.

REM Set installation directory
set "INSTALL_DIR=%PROGRAMFILES%\\{self.app_name}"
set "LOG_FILE=%INSTALL_DIR%\\install.log"

echo [INFO] Installation directory: %INSTALL_DIR%
echo.

REM Create installation directory
echo [1/8] Creating installation directory...
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%" 2>nul
    if %errorLevel% neq 0 (
        echo [ERROR] Failed to create installation directory
        pause
        exit /b 1
    )
    echo Installation directory created
) else (
    echo Installation directory already exists
)

REM Check if Python is installed
echo [2/8] Checking Python installation...
python --version >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Python is already installed
    python --version
) else (
    echo [INFO] Python not found, downloading Python 3.11.7...
    
    REM Download Python installer
    powershell -Command "try {{ Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe' -OutFile 'python-installer.exe' -UseBasicParsing }} catch {{ Write-Host 'Download failed'; exit 1 }}" 2>nul
    
    if exist python-installer.exe (
        echo [INFO] Installing Python 3.11.7 (this may take a few minutes)...
        python-installer.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0
        
        REM Wait for installation to complete
        timeout /t 30 /nobreak >nul
        
        REM Refresh PATH
        call refreshenv
        
        REM Verify installation
        python --version >nul 2>&1
        if %errorLevel% == 0 (
            echo [SUCCESS] Python installed successfully
        ) else (
            echo [ERROR] Python installation failed
            echo Please install Python 3.11+ manually from https://python.org
            pause
            exit /b 1
        )
        
        del python-installer.exe 2>nul
    ) else (
        echo [ERROR] Failed to download Python installer
        echo Please install Python 3.11+ manually from https://python.org
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
) else (
    echo [INFO] Git not found, downloading Git for Windows...
    
    REM Download Git installer
    powershell -Command "try {{ Invoke-WebRequest -Uri 'https://github.com/git-for-windows/git/releases/download/v2.42.0.windows.2/Git-2.42.0.2-64-bit.exe' -OutFile 'git-installer.exe' -UseBasicParsing }} catch {{ Write-Host 'Download failed'; exit 1 }}" 2>nul
    
    if exist git-installer.exe (
        echo [INFO] Installing Git for Windows...
        git-installer.exe /SILENT /NORESTART
        
        REM Wait for installation to complete
        timeout /t 20 /nobreak >nul
        
        REM Refresh PATH
        call refreshenv
        
        REM Verify installation
        git --version >nul 2>&1
        if %errorLevel% == 0 (
            echo [SUCCESS] Git installed successfully
        ) else (
            echo [WARNING] Git installation may have failed
        )
        
        del git-installer.exe 2>nul
    ) else (
        echo [WARNING] Failed to download Git installer
        echo Git is optional for this application
    )
)

REM Copy application files
echo [4/8] Copying application files...

REM Copy all application files with error checking
if exist "restaurant_billing" (
    xcopy "restaurant_billing" "%INSTALL_DIR%\\restaurant_billing\\" /E /I /Y /Q
    if %errorLevel% neq 0 (
        echo [ERROR] Failed to copy restaurant_billing directory
        pause
        exit /b 1
    )
    echo [SUCCESS] restaurant_billing directory copied
) else (
    echo [ERROR] restaurant_billing directory not found
    pause
    exit /b 1
)

if exist "main.py" (
    copy "main.py" "%INSTALL_DIR%\\" /Y
    if %errorLevel% neq 0 (
        echo [ERROR] Failed to copy main.py
        pause
        exit /b 1
    )
    echo [SUCCESS] main.py copied
)

if exist "requirements.txt" (
    copy "requirements.txt" "%INSTALL_DIR%\\" /Y
    if %errorLevel% neq 0 (
        echo [ERROR] Failed to copy requirements.txt
        pause
        exit /b 1
    )
    echo [SUCCESS] requirements.txt copied
)

if exist "README.md" (
    copy "README.md" "%INSTALL_DIR%\\" /Y
    echo [SUCCESS] README.md copied
)

if exist "LICENSE.txt" (
    copy "LICENSE.txt" "%INSTALL_DIR%\\" /Y
    echo [SUCCESS] LICENSE.txt copied
)

echo [SUCCESS] Application files copied

REM Install Python dependencies
echo [5/8] Installing Python dependencies...

cd /d "%INSTALL_DIR%"

REM Upgrade pip first
python -m pip install --upgrade pip --quiet --disable-pip-version-check
if %errorLevel% neq 0 (
    echo [WARNING] Failed to upgrade pip, continuing anyway
)

REM Install requirements
python -m pip install -r requirements.txt --quiet --disable-pip-version-check
if %errorLevel% neq 0 (
    echo [ERROR] Failed to install Python dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo [SUCCESS] Python dependencies installed

REM Initialize database
echo [6/8] Initializing database...

python -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized successfully')"
if %errorLevel% neq 0 (
    echo [ERROR] Database initialization failed
    echo Please check the application files and try again
    pause
    exit /b 1
)

echo [SUCCESS] Database initialized

REM Create desktop shortcut
echo [7/8] Creating desktop shortcut...

set "DESKTOP=%USERPROFILE%\\Desktop"
set "SHORTCUT=%DESKTOP%\\{self.app_name}.lnk"

REM Create shortcut using PowerShell
powershell -Command "try {{ $WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = '%INSTALL_DIR%\\main.py'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = '{self.app_name}'; $Shortcut.Save() }} catch {{ Write-Host 'Shortcut creation failed' }}" 2>nul

if exist "%SHORTCUT%" (
    echo [SUCCESS] Desktop shortcut created
) else (
    echo [WARNING] Desktop shortcut creation failed
)

REM Create start menu entry
echo [8/8] Creating start menu entry...

set "START_MENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"
set "START_SHORTCUT=%START_MENU%\\{self.app_name}.lnk"

REM Create start menu shortcut
powershell -Command "try {{ $WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_SHORTCUT%'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = '%INSTALL_DIR%\\main.py'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = '{self.app_name}'; $Shortcut.Save() }} catch {{ Write-Host 'Start menu shortcut creation failed' }}" 2>nul

if exist "%START_SHORTCUT%" (
    echo [SUCCESS] Start menu entry created
) else (
    echo [WARNING] Start menu entry creation failed
)

REM Create launcher script
echo [INFO] Creating launcher script...

echo @echo off > "%INSTALL_DIR%\\start_desktop.bat"
echo cd /d "%INSTALL_DIR%" >> "%INSTALL_DIR%\\start_desktop.bat"
echo python main.py >> "%INSTALL_DIR%\\start_desktop.bat"
echo pause >> "%INSTALL_DIR%\\start_desktop.bat"

echo [SUCCESS] Launcher script created

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

echo Press any key to launch the application now, or close this window to exit.
pause >nul

REM Launch application
echo [INFO] Launching {self.app_name}...
cd /d "%INSTALL_DIR%"
python main.py
'''
        
        with open(self.install_dir / "install.bat", "w") as f:
            f.write(installer_script)
        print("✅ Robust installer created")
        
    def create_simple_installer(self):
        """Create a simple installer for basic installation"""
        print("📝 Creating simple installer...")
        
        simple_installer = f'''@echo off
REM {self.app_name} - Simple Installer
REM Basic installation without complex error handling

echo ========================================
echo {self.app_name}
echo Simple Installer v{self.version}
echo ========================================
echo.

REM Check for administrator privileges
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] This installer requires administrator privileges
    echo Please run as Administrator
    pause
    exit /b 1
)

echo [INFO] Running with administrator privileges
echo.

REM Set installation directory
set "INSTALL_DIR=%PROGRAMFILES%\\{self.app_name}"

echo [INFO] Installation directory: %INSTALL_DIR%
echo.

REM Create installation directory
echo [1/4] Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy application files
echo [2/4] Copying application files...
xcopy "restaurant_billing" "%INSTALL_DIR%\\restaurant_billing\\" /E /I /Y /Q
copy "main.py" "%INSTALL_DIR%\\" /Y
copy "requirements.txt" "%INSTALL_DIR%\\" /Y
copy "README.md" "%INSTALL_DIR%\\" /Y
copy "LICENSE.txt" "%INSTALL_DIR%\\" /Y

REM Install Python dependencies
echo [3/4] Installing Python dependencies...
cd /d "%INSTALL_DIR%"
python -m pip install -r requirements.txt --quiet --disable-pip-version-check

REM Initialize database
echo [4/4] Initializing database...
python -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized')"

REM Create launcher script
echo @echo off > "%INSTALL_DIR%\\start_desktop.bat"
echo cd /d "%INSTALL_DIR%" >> "%INSTALL_DIR%\\start_desktop.bat"
echo python main.py >> "%INSTALL_DIR%\\start_desktop.bat"
echo pause >> "%INSTALL_DIR%\\start_desktop.bat"

echo.
echo ========================================
echo INSTALLATION COMPLETE
echo ========================================
echo.
echo [SUCCESS] {self.app_name} installed successfully!
echo.
echo Installation location: %INSTALL_DIR%
echo.
echo How to start:
echo 1. Run: %INSTALL_DIR%\\start_desktop.bat
echo 2. Or navigate to the installation directory and run: python main.py
echo.
echo Default login credentials:
echo - Username: owner
echo - Password: 1234
echo.

echo Press any key to launch the application now, or close this window to exit.
pause >nul

REM Launch application
echo [INFO] Launching {self.app_name}...
cd /d "%INSTALL_DIR%"
python main.py
'''
        
        with open(self.install_dir / "install_simple.bat", "w") as f:
            f.write(simple_installer)
        print("✅ Simple installer created")
        
    def create_readme(self):
        """Create installation README"""
        print("📖 Creating installation README...")
        
        readme_content = f"""# {self.app_name} - Fixed Installer Package

## Professional Desktop Billing System

This package provides a complete desktop billing system with multiple installation options and robust error handling.

### Features
- 🧾 **Complete Billing System**: Full restaurant billing with GST compliance
- 💰 **GST Calculation**: Automatic GST calculation and reporting
- 💳 **UPI Integration**: QR code generation for payments
- 👥 **User Management**: Role-based access control
- 📊 **Reports**: Sales reports and analytics
- 🔄 **Auto Updates**: Automatic update notifications
- 🗄️ **SQLite Database**: Built-in database, no separate installation needed

### Installation Options

#### Option 1: Robust Installer (Recommended)
- **File**: `install.bat`
- **Usage**: Right-click → "Run as Administrator"
- **Features**: 
  - Full error handling and validation
  - Automatic Python 3.11.7 installation
  - Automatic Git for Windows installation
  - Complete application setup
  - Desktop shortcuts and start menu integration

#### Option 2: Simple Installer
- **File**: `install_simple.bat`
- **Usage**: Right-click → "Run as Administrator"
- **Features**: 
  - Basic installation without complex error handling
  - Assumes Python is already installed
  - Quick setup for experienced users

### System Requirements
- Windows 7 or later
- Python 3.11+ (robust installer will install automatically)
- 4GB RAM minimum
- 500MB free disk space
- Internet connection (for dependency installation)

### Troubleshooting

#### If you get "return non-zero status 1" error:
1. **Check Administrator Privileges**: Make sure you're running as Administrator
2. **Check Python Installation**: Ensure Python 3.11+ is installed
3. **Check Internet Connection**: Required for downloading dependencies
4. **Try Simple Installer**: Use `install_simple.bat` if the robust installer fails
5. **Manual Installation**: 
   - Install Python 3.11+ from https://python.org
   - Run: `pip install -r requirements.txt`
   - Run: `python main.py`

#### Common Issues:
- **Python not found**: Install Python 3.11+ from https://python.org
- **Permission denied**: Run as Administrator
- **Network error**: Check internet connection
- **File not found**: Ensure all files are in the same directory

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
        
        zip_path = self.output_dir / f"{self.app_name.replace(' ', '-')}-Fixed-Installer.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.install_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(self.install_dir)
                    zipf.write(file_path, arc_path)
                    
        print(f"✅ ZIP package created: {zip_path}")
        return zip_path
        
    def build_installer(self):
        """Build the fixed installer"""
        print(f"🚀 Building {self.app_name} Fixed Installer Package")
        print("=" * 50)
        
        # Create installer structure
        self.create_installer_structure()
        
        # Copy application files
        if not self.copy_application_files():
            print("❌ Failed to copy application files")
            return False
            
        # Create robust installer
        self.create_robust_installer()
        
        # Create simple installer
        self.create_simple_installer()
        
        # Create README
        self.create_readme()
        
        # Create ZIP package
        zip_path = self.create_zip_package()
        
        print("\n" + "=" * 50)
        print("✅ FIXED INSTALLER PACKAGE BUILT SUCCESSFULLY")
        print("=" * 50)
        print(f"📦 Output: {zip_path}")
        print(f"📁 Size: {zip_path.stat().st_size / (1024*1024):.1f} MB")
        print("\n🎯 Features:")
        print("- Robust installer with full error handling")
        print("- Simple installer for basic installation")
        print("- Automatic Python installation")
        print("- Automatic Git installation")
        print("- Desktop shortcuts and start menu integration")
        print("- Database initialization")
        print("- Comprehensive troubleshooting guide")
        print("\n🚀 Ready for distribution!")
        print("\n💡 Usage:")
        print("1. Extract the ZIP file")
        print("2. Try install.bat first (robust installer)")
        print("3. If that fails, try install_simple.bat")
        print("4. Follow the troubleshooting guide if needed")
        
        return True

def main():
    creator = FixedInstallerCreator()
    success = creator.build_installer()
    
    if success:
        print("\n💡 Next steps:")
        print("1. Test the installer on a Windows machine")
        print("2. Upload to GitHub releases")
        print("3. Distribute to users")
    else:
        print("\n❌ Installer creation failed")
        return 1

if __name__ == "__main__":
    main()
