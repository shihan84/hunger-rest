#!/usr/bin/env python3
"""
Create Complete Installer Package
Creates a comprehensive installer package for Windows deployment
"""

import os
import shutil
import zipfile
from pathlib import Path

class CompleteInstallerCreator:
    def __init__(self):
        self.app_name = "HUNGER Restaurant Billing System"
        self.version = "1.0.0"
        self.install_dir = Path("dist/complete-installer")
        self.output_dir = Path("dist")
        
    def create_installer_structure(self):
        """Create the installer directory structure"""
        print("📁 Creating complete installer structure...")
        
        # Create main directory
        self.install_dir.mkdir(parents=True, exist_ok=True)
        
        print("✅ Complete installer structure created")
        
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
        
    def create_simple_installer(self):
        """Create simple command-line installer"""
        print("📝 Creating simple installer...")
        
        installer_script = f'''@echo off
REM {self.app_name} - Simple Installer
REM Complete desktop billing system installer

echo ========================================
echo {self.app_name}
echo Simple Installer v{self.version}
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
        print("✅ Simple installer created")
        
    def create_gui_installer(self):
        """Create GUI installer"""
        print("📝 Creating GUI installer...")
        
        gui_installer_script = '''#!/usr/bin/env python3
"""
HUNGER Restaurant Billing System - GUI Installer
Professional GUI installer with progress tracking
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
import subprocess
import threading
from pathlib import Path
import shutil

class HUNGERInstaller:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("HUNGER Restaurant Billing System - Professional Installer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center the window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.root.winfo_screenheight() // 2) - (500 // 2)
        self.root.geometry(f"600x500+{x}+{y}")
        
        # Variables
        self.install_path = tk.StringVar(value=r"C:\\Program Files\\HUNGER Restaurant Billing System")
        self.install_progress = tk.DoubleVar()
        self.status_text = tk.StringVar(value="Ready to install")
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the user interface"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="HUNGER Restaurant Billing System", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        subtitle_label = ttk.Label(main_frame, text="Professional Desktop Billing System", 
                                  font=("Arial", 10))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        # Features frame
        features_frame = ttk.LabelFrame(main_frame, text="Features", padding="10")
        features_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        features_text = """• Complete Restaurant Billing System
• GST Calculation and Compliance
• UPI QR Code Generation
• User Management with Role-Based Access
• Sales Reports and Analytics
• Automatic Update Notifications
• SQLite Database (Built-in)"""
        
        ttk.Label(features_frame, text=features_text, justify=tk.LEFT).grid(row=0, column=0, sticky=tk.W)
        
        # Installation path
        path_frame = ttk.LabelFrame(main_frame, text="Installation Location", padding="10")
        path_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        ttk.Entry(path_frame, textvariable=self.install_path, width=50).grid(row=0, column=0, sticky=(tk.W, tk.E))
        ttk.Button(path_frame, text="Browse", command=self.browse_path).grid(row=0, column=1, padx=(10, 0))
        
        # Progress frame
        progress_frame = ttk.LabelFrame(main_frame, text="Installation Progress", padding="10")
        progress_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))
        
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.install_progress, 
                                          maximum=100, length=400)
        self.progress_bar.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.status_label = ttk.Label(progress_frame, textvariable=self.status_text)
        self.status_label.grid(row=1, column=0, columnspan=2)
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=(20, 0))
        
        self.install_button = ttk.Button(button_frame, text="Install", command=self.start_installation)
        self.install_button.grid(row=0, column=0, padx=(0, 10))
        
        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.root.quit)
        self.cancel_button.grid(row=0, column=1)
        
        # Configure grid weights
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
    def browse_path(self):
        """Browse for installation path"""
        path = filedialog.askdirectory(title="Select Installation Directory")
        if path:
            self.install_path.set(os.path.join(path, "HUNGER Restaurant Billing System"))
            
    def start_installation(self):
        """Start the installation process"""
        self.install_button.config(state="disabled")
        self.cancel_button.config(state="disabled")
        
        # Start installation in a separate thread
        thread = threading.Thread(target=self.install_application)
        thread.daemon = True
        thread.start()
        
    def install_application(self):
        """Install the application"""
        try:
            install_dir = Path(self.install_path.get())
            
            # Step 1: Create installation directory
            self.update_status("Creating installation directory...")
            self.update_progress(10)
            install_dir.mkdir(parents=True, exist_ok=True)
            
            # Step 2: Copy application files
            self.update_status("Copying application files...")
            self.update_progress(20)
            
            # Copy restaurant_billing module
            if Path("restaurant_billing").exists():
                shutil.copytree("restaurant_billing", install_dir / "restaurant_billing", dirs_exist_ok=True)
            
            # Copy main files
            files_to_copy = ["main.py", "requirements.txt", "README.md", "LICENSE.txt"]
            for file in files_to_copy:
                if Path(file).exists():
                    shutil.copy2(file, install_dir / file)
            
            # Step 3: Check Python installation
            self.update_status("Checking Python installation...")
            self.update_progress(30)
            
            try:
                result = subprocess.run([sys.executable, "--version"], 
                                      capture_output=True, text=True, check=True)
                python_version = result.stdout.strip()
                print(f"Python found: {python_version}")
            except subprocess.CalledProcessError:
                self.update_status("Python not found! Please install Python 3.11+")
                self.show_error("Python 3.11+ is required but not found.\\nPlease install Python from https://python.org")
                return
            
            # Step 4: Install Python dependencies
            self.update_status("Installing Python dependencies...")
            self.update_progress(50)
            
            try:
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                             check=True, capture_output=True)
                subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                             cwd=install_dir, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                self.update_status("Failed to install dependencies")
                self.show_error(f"Failed to install Python dependencies: {e}")
                return
            
            # Step 5: Initialize database
            self.update_status("Initializing database...")
            self.update_progress(70)
            
            try:
                subprocess.run([sys.executable, "-c", 
                              "from restaurant_billing.db import init_db; init_db(); print('Database initialized')"], 
                             cwd=install_dir, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                self.update_status("Database initialization failed")
                self.show_error(f"Failed to initialize database: {e}")
                return
            
            # Step 6: Create shortcuts
            self.update_status("Creating shortcuts...")
            self.update_progress(85)
            
            self.create_shortcuts(install_dir)
            
            # Step 7: Complete installation
            self.update_status("Installation completed successfully!")
            self.update_progress(100)
            
            # Show success message
            self.root.after(0, self.show_success)
            
        except Exception as e:
            self.update_status(f"Installation failed: {e}")
            self.root.after(0, lambda: self.show_error(f"Installation failed: {e}"))
            
    def create_shortcuts(self, install_dir):
        """Create desktop and start menu shortcuts"""
        try:
            # Create batch file launcher
            batch_path = install_dir / "start_desktop.bat"
            with open(batch_path, 'w') as f:
                f.write('@echo off\\n')
                f.write(f'cd /d "{install_dir}"\\n')
                f.write('python main.py\\n')
                f.write('pause\\n')
                
        except Exception as e:
            print(f"Failed to create shortcuts: {e}")
                
    def update_status(self, message):
        """Update status message"""
        self.root.after(0, lambda: self.status_text.set(message))
        print(message)
        
    def update_progress(self, value):
        """Update progress bar"""
        self.root.after(0, lambda: self.install_progress.set(value))
        
    def show_success(self):
        """Show success message"""
        messagebox.showinfo("Installation Complete", 
                           "HUNGER Restaurant Billing System has been installed successfully!\\n\\n"
                           f"Installation location: {self.install_path.get()}\\n\\n"
                           "Default login credentials:\\n"
                           "Username: owner\\n"
                           "Password: 1234\\n\\n"
                           "Click OK to launch the application.")
        
        # Launch application
        try:
            install_dir = Path(self.install_path.get())
            subprocess.Popen([sys.executable, "main.py"], cwd=install_dir)
        except Exception as e:
            print(f"Failed to launch application: {e}")
            
        self.root.quit()
        
    def show_error(self, message):
        """Show error message"""
        messagebox.showerror("Installation Error", message)
        self.install_button.config(state="normal")
        self.cancel_button.config(state="normal")
        
    def run(self):
        """Run the installer"""
        self.root.mainloop()

if __name__ == "__main__":
    # Check if running on Windows
    if sys.platform != "win32":
        print("This installer is designed for Windows only.")
        sys.exit(1)
        
    # Check for required modules
    try:
        import tkinter
    except ImportError:
        print("tkinter is required but not installed.")
        sys.exit(1)
        
    installer = HUNGERInstaller()
    installer.run()
'''
        
        with open(self.install_dir / "installer_gui.py", "w") as f:
            f.write(gui_installer_script)
        print("✅ GUI installer created")
        
    def create_gui_launcher(self):
        """Create GUI installer launcher"""
        print("📝 Creating GUI installer launcher...")
        
        gui_launcher = '''@echo off
REM HUNGER Restaurant Billing System - GUI Installer Launcher

echo ========================================
echo HUNGER Restaurant Billing System
echo Professional GUI Installer
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorLevel% == 0 (
    echo [INFO] Python found, launching GUI installer...
    python installer_gui.py
) else (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python 3.11+ from https://python.org
    echo Then run this installer again.
    echo.
    pause
    exit /b 1
)
'''
        
        with open(self.install_dir / "install_gui.bat", "w") as f:
            f.write(gui_launcher)
        print("✅ GUI installer launcher created")
        
    def create_readme(self):
        """Create installation README"""
        print("📖 Creating installation README...")
        
        readme_content = f"""# {self.app_name} - Complete Installer Package

## Professional Desktop Billing System

This package provides a complete desktop billing system with multiple installation options.

### Features
- 🧾 **Complete Billing System**: Full restaurant billing with GST compliance
- 💰 **GST Calculation**: Automatic GST calculation and reporting
- 💳 **UPI Integration**: QR code generation for payments
- 👥 **User Management**: Role-based access control
- 📊 **Reports**: Sales reports and analytics
- 🔄 **Auto Updates**: Automatic update notifications
- 🗄️ **SQLite Database**: Built-in database, no separate installation needed

### Installation Options

#### Option 1: Simple Command-Line Installer
1. **Right-click** `install.bat` and select "Run as Administrator"
2. **Follow** the installation prompts
3. **Launch** from desktop shortcut

#### Option 2: Professional GUI Installer
1. **Double-click** `install_gui.bat` to launch the GUI installer
2. **Follow** the installation wizard
3. **Launch** from desktop shortcut

### System Requirements
- Windows 7 or later
- Python 3.11+ (installers will check and guide you)
- 4GB RAM minimum
- 500MB free disk space

### What Gets Installed
- Python 3.11.7 (if not already present)
- Git for Windows (if not already present)
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
        
        zip_path = self.output_dir / f"{self.app_name.replace(' ', '-')}-Complete-Installer.zip"
        
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
        print(f"🚀 Building {self.app_name} Complete Installer Package")
        print("=" * 50)
        
        # Create installer structure
        self.create_installer_structure()
        
        # Copy application files
        if not self.copy_application_files():
            print("❌ Failed to copy application files")
            return False
            
        # Create simple installer
        self.create_simple_installer()
        
        # Create GUI installer
        self.create_gui_installer()
        
        # Create GUI launcher
        self.create_gui_launcher()
        
        # Create README
        self.create_readme()
        
        # Create ZIP package
        zip_path = self.create_zip_package()
        
        print("\n" + "=" * 50)
        print("✅ COMPLETE INSTALLER PACKAGE BUILT SUCCESSFULLY")
        print("=" * 50)
        print(f"📦 Output: {zip_path}")
        print(f"📁 Size: {zip_path.stat().st_size / (1024*1024):.1f} MB")
        print("\n🎯 Features:")
        print("- Complete desktop billing system")
        print("- Two installation options:")
        print("  • Simple installer (install.bat)")
        print("  • Professional GUI installer (install_gui.bat)")
        print("- Automatic Python installation")
        print("- Automatic Git installation")
        print("- Desktop shortcuts and start menu integration")
        print("- Database initialization")
        print("- Error handling and user guidance")
        print("\n🚀 Ready for distribution!")
        print("\n💡 Usage:")
        print("1. Extract the ZIP file")
        print("2. Choose installation method:")
        print("   • Right-click install.bat → Run as Administrator")
        print("   • Double-click install_gui.bat for GUI installer")
        print("3. Follow the installation prompts")
        print("4. Launch from desktop shortcut")
        
        return True

def main():
    creator = CompleteInstallerCreator()
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
