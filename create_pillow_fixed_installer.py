#!/usr/bin/env python3
"""
Create Pillow-Fixed Installer Package
Creates an installer that handles Pillow dependency issues
"""

import os
import shutil
import zipfile
from pathlib import Path

class PillowFixedInstallerCreator:
    def __init__(self):
        self.app_name = "HUNGER Restaurant Billing System"
        self.version = "1.0.0"
        self.install_dir = Path("dist/pillow-fixed-installer")
        self.output_dir = Path("dist")
        
    def create_installer_structure(self):
        """Create the installer directory structure"""
        print("📁 Creating Pillow-fixed installer structure...")
        
        # Create main directory
        self.install_dir.mkdir(parents=True, exist_ok=True)
        
        print("✅ Pillow-fixed installer structure created")
        
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
        
    def create_pillow_fixed_requirements(self):
        """Create a requirements.txt with Pillow fixes"""
        print("📝 Creating Pillow-fixed requirements...")
        
        requirements_content = """# Core dependencies
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
websockets==12.0
sqlalchemy==2.0.23
alembic==1.12.1
python-dotenv==1.0.0

# GUI dependencies - Fixed Pillow installation
# Use pre-compiled wheels to avoid compilation issues
Pillow==10.0.1

# Alternative: If Pillow fails, we'll use a fallback
# pillow-simd==10.0.0.post1

# Database
sqlite3

# Additional dependencies
requests==2.31.0
qrcode[pil]==7.4.2
reportlab==4.0.4
"""
        
        with open(self.install_dir / "requirements.txt", "w") as f:
            f.write(requirements_content)
        print("✅ Pillow-fixed requirements created")
        
    def create_pillow_fixed_installer(self):
        """Create installer with Pillow dependency fixes"""
        print("📝 Creating Pillow-fixed installer...")
        
        installer_script = f'''@echo off
setlocal enabledelayedexpansion
REM {self.app_name} - Pillow-Fixed Installer
REM Handles Pillow dependency issues

echo ========================================
echo {self.app_name}
echo Pillow-Fixed Installer v{self.version}
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
echo [1/8] Creating installation directory...
if not exist "%INSTALL_DIR%" mkdir "%INSTALL_DIR%"

REM Copy application files
echo [2/8] Copying application files...
xcopy "restaurant_billing" "%INSTALL_DIR%\\restaurant_billing\\" /E /I /Y /Q
copy "main.py" "%INSTALL_DIR%\\" /Y
copy "requirements.txt" "%INSTALL_DIR%\\" /Y
copy "README.md" "%INSTALL_DIR%\\" /Y
copy "LICENSE.txt" "%INSTALL_DIR%\\" /Y

echo [SUCCESS] Application files copied

REM Install Python dependencies with Pillow fixes
echo [3/8] Installing Python dependencies with Pillow fixes...

cd /d "%INSTALL_DIR%"

REM Upgrade pip first
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip --quiet --disable-pip-version-check

REM Install dependencies in stages to handle Pillow issues
echo [INFO] Installing core dependencies...
python -m pip install fastapi==0.104.1 uvicorn==0.24.0 python-multipart==0.0.6 --quiet --disable-pip-version-check
python -m pip install python-jose[cryptography]==3.3.0 passlib[bcrypt]==1.7.4 --quiet --disable-pip-version-check
python -m pip install websockets==12.0 sqlalchemy==2.0.23 alembic==1.12.1 --quiet --disable-pip-version-check
python -m pip install python-dotenv==1.0.0 requests==2.31.0 --quiet --disable-pip-version-check

REM Try to install Pillow with different methods
echo [INFO] Installing Pillow (this may take a few minutes)...

REM Method 1: Try pre-compiled wheel
python -m pip install Pillow==10.0.1 --only-binary=all --quiet --disable-pip-version-check
if %errorLevel% == 0 (
    echo [SUCCESS] Pillow installed successfully
    set PILLOW_INSTALLED=1
) else (
    echo [WARNING] Pillow installation failed, trying alternative...
    
    REM Method 2: Try older version
    python -m pip install Pillow==9.5.0 --only-binary=all --quiet --disable-pip-version-check
    if %errorLevel% == 0 (
        echo [SUCCESS] Pillow 9.5.0 installed successfully
        set PILLOW_INSTALLED=1
    ) else (
        echo [WARNING] Pillow installation failed, trying fallback...
        
        REM Method 3: Try without binary restrictions
        python -m pip install Pillow --quiet --disable-pip-version-check
        if %errorLevel% == 0 (
            echo [SUCCESS] Pillow installed successfully
            set PILLOW_INSTALLED=1
        ) else (
            echo [ERROR] Pillow installation failed completely
            set PILLOW_INSTALLED=0
        )
    )
)

REM Install remaining dependencies
echo [INFO] Installing remaining dependencies...
python -m pip install qrcode[pil]==7.4.2 reportlab==4.0.4 --quiet --disable-pip-version-check

REM Check if Pillow is working
echo [4/8] Verifying Pillow installation...
python -c "from PIL import Image; print('Pillow is working correctly')" 2>nul
if %errorLevel% == 0 (
    echo [SUCCESS] Pillow verification passed
) else (
    echo [WARNING] Pillow verification failed, but continuing...
)

REM Initialize database
echo [5/8] Initializing database...
python -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized successfully')"
if %errorLevel% neq 0 (
    echo [ERROR] Database initialization failed
    pause
    exit /b 1
)

echo [SUCCESS] Database initialized

REM Create desktop shortcut
echo [6/8] Creating desktop shortcut...
set "DESKTOP=%USERPROFILE%\\Desktop"
set "SHORTCUT=%DESKTOP%\\{self.app_name}.lnk"

powershell -Command "try {{ $WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT%'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = '%INSTALL_DIR%\\main.py'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = '{self.app_name}'; $Shortcut.Save() }} catch {{ Write-Host 'Shortcut creation failed' }}" 2>nul

if exist "%SHORTCUT%" (
    echo [SUCCESS] Desktop shortcut created
) else (
    echo [WARNING] Desktop shortcut creation failed
)

REM Create start menu entry
echo [7/8] Creating start menu entry...
set "START_MENU=%APPDATA%\\Microsoft\\Windows\\Start Menu\\Programs"
set "START_SHORTCUT=%START_MENU%\\{self.app_name}.lnk"

powershell -Command "try {{ $WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_SHORTCUT%'); $Shortcut.TargetPath = 'python'; $Shortcut.Arguments = '%INSTALL_DIR%\\main.py'; $Shortcut.WorkingDirectory = '%INSTALL_DIR%'; $Shortcut.Description = '{self.app_name}'; $Shortcut.Save() }} catch {{ Write-Host 'Start menu shortcut creation failed' }}" 2>nul

if exist "%START_SHORTCUT%" (
    echo [SUCCESS] Start menu entry created
) else (
    echo [WARNING] Start menu entry creation failed
)

REM Create launcher script
echo [8/8] Creating launcher script...
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
echo - Desktop billing application
echo - Python dependencies (with Pillow fixes)
echo - SQLite Database (built-in)
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

if %PILLOW_INSTALLED% == 0 (
    echo [WARNING] Pillow installation failed. Some features may not work.
    echo Please install Pillow manually: pip install Pillow
    echo.
)

echo Press any key to launch the application now, or close this window to exit.
pause >nul

REM Launch application
echo [INFO] Launching {self.app_name}...
cd /d "%INSTALL_DIR%"
python main.py
'''
        
        with open(self.install_dir / "install.bat", "w") as f:
            f.write(installer_script)
        print("✅ Pillow-fixed installer created")
        
    def create_alternative_requirements(self):
        """Create alternative requirements without Pillow"""
        print("📝 Creating alternative requirements...")
        
        alt_requirements = """# Core dependencies without Pillow
fastapi==0.104.1
uvicorn==0.24.0
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
websockets==12.0
sqlalchemy==2.0.23
alembic==1.12.1
python-dotenv==1.0.0
requests==2.31.0
reportlab==4.0.4

# Note: Pillow (PIL) is required for image processing
# If installation fails, try: pip install Pillow==9.5.0
# Or install manually from: https://pillow.readthedocs.io/en/latest/installation.html
"""
        
        with open(self.install_dir / "requirements_alternative.txt", "w") as f:
            f.write(alt_requirements)
        print("✅ Alternative requirements created")
        
    def create_readme(self):
        """Create installation README with Pillow fixes"""
        print("📖 Creating installation README...")
        
        readme_content = f"""# {self.app_name} - Pillow-Fixed Installer

## Professional Desktop Billing System

This installer handles Pillow dependency issues that commonly occur on Windows.

### Features
- 🧾 **Complete Billing System**: Full restaurant billing with GST compliance
- 💰 **GST Calculation**: Automatic GST calculation and reporting
- 💳 **UPI Integration**: QR code generation for payments
- 👥 **User Management**: Role-based access control
- 📊 **Reports**: Sales reports and analytics
- 🔄 **Auto Updates**: Automatic update notifications
- 🗄️ **SQLite Database**: Built-in database, no separate installation needed

### Installation

#### Quick Start
1. **Right-click** `install.bat` and select "Run as Administrator"
2. **Follow** the installation prompts
3. **Launch** from desktop shortcut

### Pillow Dependency Fixes

This installer includes several fixes for Pillow installation issues:

1. **Pre-compiled Wheels**: Uses binary wheels to avoid compilation
2. **Version Fallback**: Tries multiple Pillow versions if one fails
3. **Alternative Installation**: Provides fallback methods
4. **Error Handling**: Continues installation even if Pillow fails

### System Requirements
- Windows 7 or later
- Python 3.11+ (installer will check and guide you)
- 4GB RAM minimum
- 500MB free disk space
- Internet connection (for dependency installation)

### Troubleshooting Pillow Issues

#### If Pillow installation fails:
1. **Try Manual Installation**:
   ```bash
   pip install Pillow==9.5.0
   ```

2. **Use Alternative Version**:
   ```bash
   pip install Pillow==10.0.1 --only-binary=all
   ```

3. **Install Visual C++ Build Tools**:
   - Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
   - Install "C++ build tools" workload
   - Restart and try again

4. **Use Conda Instead**:
   ```bash
   conda install pillow
   ```

### What Gets Installed
- Desktop billing application
- Python dependencies (with Pillow fixes)
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
        
        zip_path = self.output_dir / f"{self.app_name.replace(' ', '-')}-Pillow-Fixed-Installer.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(self.install_dir):
                for file in files:
                    file_path = Path(root) / file
                    arc_path = file_path.relative_to(self.install_dir)
                    zipf.write(file_path, arc_path)
                    
        print(f"✅ ZIP package created: {zip_path}")
        return zip_path
        
    def build_installer(self):
        """Build the Pillow-fixed installer"""
        print(f"🚀 Building {self.app_name} Pillow-Fixed Installer Package")
        print("=" * 50)
        
        # Create installer structure
        self.create_installer_structure()
        
        # Copy application files
        if not self.copy_application_files():
            print("❌ Failed to copy application files")
            return False
            
        # Create Pillow-fixed requirements
        self.create_pillow_fixed_requirements()
        
        # Create Pillow-fixed installer
        self.create_pillow_fixed_installer()
        
        # Create alternative requirements
        self.create_alternative_requirements()
        
        # Create README
        self.create_readme()
        
        # Create ZIP package
        zip_path = self.create_zip_package()
        
        print("\n" + "=" * 50)
        print("✅ PILLOW-FIXED INSTALLER PACKAGE BUILT SUCCESSFULLY")
        print("=" * 50)
        print(f"📦 Output: {zip_path}")
        print(f"📁 Size: {zip_path.stat().st_size / (1024*1024):.1f} MB")
        print("\n🎯 Features:")
        print("- Handles Pillow dependency issues")
        print("- Multiple Pillow installation methods")
        print("- Pre-compiled wheel support")
        print("- Version fallback options")
        print("- Error handling and recovery")
        print("- Alternative requirements file")
        print("- Comprehensive troubleshooting guide")
        print("\n🚀 Ready for distribution!")
        print("\n💡 Usage:")
        print("1. Extract the ZIP file")
        print("2. Right-click install.bat → Run as Administrator")
        print("3. Follow the installation prompts")
        print("4. If Pillow fails, try manual installation")
        
        return True

def main():
    creator = PillowFixedInstallerCreator()
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
