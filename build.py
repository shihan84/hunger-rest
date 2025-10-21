#!/usr/bin/env python3
"""
HUNGER Restaurant Billing System - Build Script
Creates packaged distributions for Windows, Linux, and macOS
"""

import os
import sys
import shutil
import subprocess
import platform
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {cmd}")
            print(f"Error: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Exception running command: {cmd}")
        print(f"Exception: {e}")
        return False

def create_virtual_environment(venv_path):
    """Create a virtual environment"""
    print(f"Creating virtual environment at {venv_path}")
    python_cmd = "python3" if platform.system() != "Windows" else "python"
    if not run_command(f"{python_cmd} -m venv {venv_path}"):
        return False
    
    # Install dependencies
    pip_cmd = f"{venv_path}/bin/pip" if platform.system() != "Windows" else f"{venv_path}/Scripts/pip"
    if not run_command(f"{pip_cmd} install --upgrade pip"):
        return False
    
    if not run_command(f"{pip_cmd} install -r requirements.txt"):
        return False
    
    if not run_command(f"{pip_cmd} install -r mobile_backend/requirements.txt"):
        return False
    
    return True

def create_launcher_scripts(dist_path, platform_name):
    """Create platform-specific launcher scripts"""
    if platform_name == "Windows":
        # Desktop launcher
        desktop_script = f"""@echo off
cd /d "%~dp0"
venv\\Scripts\\python.exe main.py
pause
"""
        with open(dist_path / "start_desktop.bat", "w") as f:
            f.write(desktop_script)
        
        # Mobile launcher
        mobile_script = f"""@echo off
cd /d "%~dp0\\mobile_backend"
..\\venv\\Scripts\\python.exe main.py
pause
"""
        with open(dist_path / "start_mobile.bat", "w") as f:
            f.write(mobile_script)
            
    else:  # Linux/macOS
        # Desktop launcher
        desktop_script = f"""#!/bin/bash
cd "$(dirname "$0")"
./venv/bin/python main.py
"""
        with open(dist_path / "start_desktop.sh", "w") as f:
            f.write(desktop_script)
        os.chmod(dist_path / "start_desktop.sh", 0o755)
        
        # Mobile launcher
        mobile_script = f"""#!/bin/bash
cd "$(dirname "$0")/mobile_backend"
../venv/bin/python main.py
"""
        with open(dist_path / "start_mobile.sh", "w") as f:
            f.write(mobile_script)
        os.chmod(dist_path / "start_mobile.sh", 0o755)

def create_install_script(dist_path, platform_name):
    """Create platform-specific install script"""
    if platform_name == "Windows":
        install_script = f"""@echo off
echo Installing HUNGER Restaurant Billing System...

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is required but not found in PATH.
    echo Please install Python 3.11+ and add it to PATH.
    pause
    exit /b 1
)

REM Initialize database
venv\\Scripts\\python.exe -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized')"

echo Installation completed!
echo To run the desktop application: start_desktop.bat
echo To run the mobile backend: start_mobile.bat
pause
"""
        with open(dist_path / "install.bat", "w") as f:
            f.write(install_script)
    else:
        install_script = f"""#!/bin/bash
echo "Installing HUNGER Restaurant Billing System..."

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3.11+ is required. Please install it first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if [[ $(echo "$python_version < 3.11" | bc -l) -eq 1 ]]; then
    echo "Python 3.11+ is required. Current version: $python_version"
    exit 1
fi

# Initialize database
./venv/bin/python -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized')"

echo "Installation completed!"
echo "To run the desktop application: ./start_desktop.sh"
echo "To run the mobile backend: ./start_mobile.sh"
"""
        with open(dist_path / "install.sh", "w") as f:
            f.write(install_script)
        os.chmod(dist_path / "install.sh", 0o755)

def build_package(platform_name):
    """Build package for specific platform"""
    print(f"Building package for {platform_name}")
    
    # Create distribution directory
    dist_path = Path(f"dist/hunger-restaurant-billing-{platform_name.lower()}")
    dist_path.mkdir(parents=True, exist_ok=True)
    
    # Copy application files
    print("Copying application files...")
    if (dist_path / "restaurant_billing").exists():
        shutil.rmtree(dist_path / "restaurant_billing")
    if (dist_path / "mobile_backend").exists():
        shutil.rmtree(dist_path / "mobile_backend")
    shutil.copytree("restaurant_billing", dist_path / "restaurant_billing")
    shutil.copytree("mobile_backend", dist_path / "mobile_backend")
    shutil.copy("main.py", dist_path)
    shutil.copy("requirements.txt", dist_path)
    shutil.copy("mobile_backend/requirements.txt", dist_path / "mobile_backend")
    
    # Copy documentation
    print("Copying documentation...")
    docs = [
        "README.md",
        "INSTALLATION_QUICK_START.md", 
        "DATABASE_INFO.md",
        "INSTALLATION_SUMMARY.md",
        "PRODUCTION_READINESS.md",
        "AUTOMATIC_UPDATES.md"
    ]
    for doc in docs:
        if Path(doc).exists():
            shutil.copy(doc, dist_path)
    
    # Copy installation scripts
    print("Copying installation scripts...")
    if platform_name == "Windows":
        scripts = [
            "install_windows.bat",
            "install_simple.bat", 
            "install_everything.bat",
            "install_everything.ps1",
            "install_with_database.bat",
            "uninstall.ps1"
        ]
        for script in scripts:
            if Path(script).exists():
                shutil.copy(script, dist_path)
    
    # Create data directory
    (dist_path / "data").mkdir(exist_ok=True)
    
    # Create virtual environment
    print("Creating virtual environment...")
    venv_path = dist_path / "venv"
    if not create_virtual_environment(venv_path):
        print("Failed to create virtual environment")
        return False
    
    # Create launcher scripts
    print("Creating launcher scripts...")
    create_launcher_scripts(dist_path, platform_name)
    
    # Create install script
    print("Creating install script...")
    create_install_script(dist_path, platform_name)
    
    # Initialize database
    print("Initializing database...")
    python_cmd = f"{venv_path}/bin/python" if platform_name != "Windows" else f"{venv_path}/Scripts/python.exe"
    if not run_command(f"{python_cmd} -c \"from restaurant_billing.db import init_db; init_db(); print('Database initialized')\"", cwd=dist_path):
        print("Warning: Database initialization failed, but application will create it on first run")
    
    print(f"Package created successfully at {dist_path}")
    return True

def create_archive(platform_name):
    """Create archive for the platform"""
    dist_path = Path(f"dist/hunger-restaurant-billing-{platform_name.lower()}")
    archive_name = f"dist/HUNGER-Restaurant-Billing-{platform_name}.zip" if platform_name == "Windows" else f"dist/HUNGER-Restaurant-Billing-{platform_name}.tar.gz"
    
    print(f"Creating archive: {archive_name}")
    
    if platform_name == "Windows":
        # Use PowerShell for Windows
        cmd = f'powershell -Command "Compress-Archive -Path \'{dist_path}\\*\' -DestinationPath \'{archive_name}\' -Force"'
    else:
        # Use tar for Linux/macOS
        cmd = f"tar -czf {archive_name} -C dist hunger-restaurant-billing-{platform_name.lower()}"
    
    if run_command(cmd):
        print(f"Archive created: {archive_name}")
        return True
    else:
        print(f"Failed to create archive: {archive_name}")
        return False

def main():
    """Main build function"""
    print("HUNGER Restaurant Billing System - Build Script")
    print("=" * 50)
    
    # Detect current platform
    current_platform = platform.system()
    if current_platform == "Darwin":
        current_platform = "macOS"
    
    print(f"Current platform: {current_platform}")
    
    # Build for current platform
    if build_package(current_platform):
        print(f"✅ Successfully built package for {current_platform}")
        
        if create_archive(current_platform):
            print(f"✅ Successfully created archive for {current_platform}")
        else:
            print(f"❌ Failed to create archive for {current_platform}")
    else:
        print(f"❌ Failed to build package for {current_platform}")
        return 1
    
    print("\nBuild completed successfully!")
    print(f"Package location: dist/hunger-restaurant-billing-{current_platform.lower()}")
    print(f"Archive location: dist/HUNGER-Restaurant-Billing-{current_platform}.zip" if current_platform == "Windows" else f"dist/HUNGER-Restaurant-Billing-{current_platform}.tar.gz")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
