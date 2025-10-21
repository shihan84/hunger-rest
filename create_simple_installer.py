#!/usr/bin/env python3
"""
Create Simple Desktop Installer
Creates a simple installer with install.bat in the root directory
"""

import os
import shutil
import zipfile
from pathlib import Path

class SimpleInstallerCreator:
    def __init__(self):
        self.app_name = "HUNGER Restaurant Billing System"
        self.version = "1.0.0"
        self.install_dir = Path("dist/simple-installer")
        self.output_dir = Path("dist")
        
    def create_installer_structure(self):
        """Create the installer directory structure"""
        print("📁 Creating simple installer structure...")
        
        # Create main directory
        self.install_dir.mkdir(parents=True, exist_ok=True)
        
        print("✅ Installer structure created")
        
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
        
    def create_installer_script(self):
        """Create the main installer script"""
        print("📝 Creating installer script...")
        
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
xcopy "restaurant_billing" "%INSTALL_DIR%\\restaurant_billing\\" /E /I /Y >> "%LOG_FILE%"
copy "main.py" "%INSTALL_DIR%\\" >> "%LOG_FILE%"
copy "requirements.txt" "%INSTALL_DIR%\\" >> "%LOG_FILE%"
copy "README.md" "%INSTALL_DIR%\\" >> "%LOG_FILE%"
copy "LICENSE.txt" "%INSTALL_DIR%\\" >> "%LOG_FILE%"

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
        
        with open(self.install_dir / "install.bat", "w") as f:
            f.write(installer_script)
        print("✅ Installer script created")
        
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

### Installation

#### Quick Start
1. **Right-click** `install.bat` and select "Run as Administrator"
2. **Follow** the installation prompts
3. **Launch** from desktop shortcut

#### System Requirements
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
        
        zip_path = self.output_dir / f"{self.app_name.replace(' ', '-')}-Simple-Installer.zip"
        
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
        print(f"🚀 Building {self.app_name} Simple Desktop Installer")
        print("=" * 50)
        
        # Create installer structure
        self.create_installer_structure()
        
        # Copy application files
        if not self.copy_application_files():
            print("❌ Failed to copy application files")
            return False
            
        # Create installer script
        self.create_installer_script()
        
        # Create README
        self.create_readme()
        
        # Create ZIP package
        zip_path = self.create_zip_package()
        
        print("\n" + "=" * 50)
        print("✅ SIMPLE DESKTOP INSTALLER BUILT SUCCESSFULLY")
        print("=" * 50)
        print(f"📦 Output: {zip_path}")
        print(f"📁 Size: {zip_path.stat().st_size / (1024*1024):.1f} MB")
        print("\n🎯 Features:")
        print("- Complete desktop billing system")
        print("- install.bat in root directory")
        print("- Automatic Python installation")
        print("- Automatic Git installation")
        print("- Desktop shortcuts")
        print("- Start menu integration")
        print("- Database initialization")
        print("\n🚀 Ready for distribution!")
        print("\n💡 Usage:")
        print("1. Extract the ZIP file")
        print("2. Right-click install.bat")
        print("3. Select 'Run as Administrator'")
        print("4. Follow the prompts")
        
        return True

def main():
    creator = SimpleInstallerCreator()
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
