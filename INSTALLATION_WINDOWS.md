# HUNGER Restaurant Billing System - Windows Installation Guide

## Quick Start (Recommended)

### Option 1: One-Click Installation
1. **Download** the project files to your computer
2. **Double-click** `install_windows.bat`
3. **Follow** the on-screen prompts
4. **Launch** the application when installation completes

### Option 2: GUI Installer
1. **Right-click** on `install_windows_gui.ps1`
2. **Select** "Run with PowerShell"
3. **Click** "Install" to install dependencies
4. **Click** "Run App" to launch the application

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10 (version 1903 or later) or Windows 11
- **Architecture**: 64-bit (x64)
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB free space
- **Internet**: Required for initial setup and updates

### Recommended Requirements
- **Operating System**: Windows 11 (latest version)
- **RAM**: 8GB or more
- **Storage**: 2GB free space (SSD recommended)
- **Display**: 1920x1080 or higher resolution

## Step-by-Step Installation

### Step 1: Install Python

#### Download Python
1. Go to [python.org/downloads](https://www.python.org/downloads/)
2. Click "Download Python 3.11.x" (latest 3.11 version)
3. **Important**: Download the 64-bit version

#### Install Python
1. **Run** the downloaded installer as Administrator
2. **Check** "Add Python to PATH" (very important!)
3. **Check** "Install for all users" (recommended)
4. **Click** "Install Now"
5. **Wait** for installation to complete
6. **Click** "Close"

#### Verify Python Installation
1. **Open** Command Prompt (Win + R, type `cmd`, press Enter)
2. **Type**: `python --version`
3. **Should show**: `Python 3.11.x`
4. **Type**: `pip --version`
5. **Should show**: `pip 23.x.x`

### Step 2: Download Project Files

#### Option A: Direct Download
1. **Download** the project ZIP file
2. **Extract** to a folder (e.g., `C:\HUNGER_Restaurant`)
3. **Note** the folder path for later use

#### Option B: Git Clone (if you have Git)
```cmd
git clone <repository-url> C:\HUNGER_Restaurant
cd C:\HUNGER_Restaurant
```

### Step 3: Install Dependencies

#### Automated Installation (Recommended)
1. **Navigate** to the project folder
2. **Double-click** `install_windows.bat`
3. **Wait** for installation to complete
4. **Press** any key to close the window

#### Manual Installation
1. **Open** Command Prompt as Administrator
2. **Navigate** to project folder:
   ```cmd
   cd C:\HUNGER_Restaurant
   ```
3. **Upgrade** pip:
   ```cmd
   python -m pip install --upgrade pip
   ```
4. **Install** desktop dependencies:
   ```cmd
   python -m pip install -r requirements.txt
   ```
5. **Install** mobile backend dependencies:
   ```cmd
   cd mobile_backend
   python -m pip install -r requirements.txt
   cd ..
   ```

### Step 4: Launch the Application

#### Desktop Application
1. **Double-click** `main.py` or run:
   ```cmd
   python main.py
   ```

#### Mobile Backend (Optional)
1. **Double-click** `mobile_backend\start_server.bat` or run:
   ```cmd
   cd mobile_backend
   python main.py
   ```

## First-Time Setup

### Initial Login
When you first run the application:
- **Username**: `owner`
- **Password**: `1234`
- **Role**: SUPER_ADMIN (full access)

### Configure Restaurant Settings
1. **Click** "Settings" in the main menu
2. **Edit** `restaurant_billing\config.py` to customize:
   - Restaurant name and legal details
   - License information
   - Telegram bot settings (optional)
   - GST settings
   - Service charge percentage

## Windows-Specific Features

### Fullscreen Mode
- **Enable** in config: `fullscreen = True`
- **Press** Escape key to exit fullscreen
- **Recommended** for kiosk-style operation

### Windows Service (Advanced)
To run as a Windows service:
1. **Install** `pywin32`:
   ```cmd
   python -m pip install pywin32
   ```
2. **Use** Windows Service Manager or third-party tools

### Windows Startup
To start automatically with Windows:
1. **Create** a shortcut to `main.py`
2. **Copy** to Startup folder:
   - Press Win + R
   - Type: `shell:startup`
   - Paste the shortcut

## Troubleshooting Windows Issues

### Python Not Found Error
```cmd
# Check if Python is in PATH
echo %PATH%

# If not found, add manually:
setx PATH "%PATH%;C:\Python311;C:\Python311\Scripts"

# Restart Command Prompt
```

### Permission Denied Errors
1. **Run** Command Prompt as Administrator
2. **Or** use user installation:
   ```cmd
   python -m pip install --user -r requirements.txt
   ```

### Tkinter Issues
If you get `_tkinter` errors:
1. **Reinstall** Python with Tkinter support
2. **Or** install tkinter separately:
   ```cmd
   python -m pip install tk
   ```

### Antivirus False Positives
Some antivirus software may flag the application:
1. **Add** the project folder to antivirus exclusions
2. **Whitelist** `python.exe` and `main.py`

### Port Already in Use (Mobile Backend)
```cmd
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F
```

### Windows Defender SmartScreen
If Windows blocks the application:
1. **Click** "More info"
2. **Click** "Run anyway"
3. **Or** add to Windows Defender exclusions

## Windows Performance Optimization

### Disable Windows Updates During Operation
1. **Open** Windows Update settings
2. **Set** active hours to avoid interruptions
3. **Or** use Group Policy to defer updates

### Power Settings
1. **Set** power plan to "High Performance"
2. **Disable** sleep mode during business hours
3. **Keep** display on during operation

### Windows Firewall
1. **Allow** Python through Windows Firewall
2. **Allow** port 8000 for mobile backend
3. **Configure** network profile (Private/Public)

## Backup and Recovery

### Database Backup
```cmd
# Create backup
copy "data\restaurant.db" "backup\restaurant_backup_%date%.db"

# Restore from backup
copy "backup\restaurant_backup_2024-01-15.db" "data\restaurant.db"
```

### Configuration Backup
```cmd
# Backup config
copy "restaurant_billing\config.py" "backup\config_backup.py"

# Backup entire data folder
xcopy "data" "backup\data_%date%" /E /I
```

### Windows System Restore
1. **Create** system restore point before installation
2. **Use** System Restore if issues occur
3. **Location**: Control Panel > System > System Protection

## Windows-Specific Commands

### Batch Files for Common Tasks

#### Start Application
```batch
@echo off
cd /d "C:\HUNGER_Restaurant"
python main.py
pause
```

#### Start Mobile Backend
```batch
@echo off
cd /d "C:\HUNGER_Restaurant\mobile_backend"
python main.py
pause
```

#### Backup Database
```batch
@echo off
set backup_dir=C:\HUNGER_Restaurant\backup
if not exist "%backup_dir%" mkdir "%backup_dir%"
copy "C:\HUNGER_Restaurant\data\restaurant.db" "%backup_dir%\restaurant_%date:~-4,4%%date:~-10,2%%date:~-7,2%.db"
echo Backup completed
pause
```

#### Update Application
```batch
@echo off
cd /d "C:\HUNGER_Restaurant"
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r mobile_backend\requirements.txt
echo Update completed
pause
```

## Windows Registry (Advanced)

### Add to Windows Context Menu
1. **Open** Registry Editor (regedit)
2. **Navigate** to: `HKEY_CLASSES_ROOT\Directory\shell`
3. **Create** new key: "HUNGER Restaurant"
4. **Set** default value: "Open HUNGER Restaurant"
5. **Create** subkey: "command"
6. **Set** default value: `"C:\Python311\python.exe" "C:\HUNGER_Restaurant\main.py" "%1"`

### Windows Startup Registry
1. **Open** Registry Editor
2. **Navigate** to: `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
3. **Create** new String Value: "HUNGER Restaurant"
4. **Set** value: `"C:\Python311\python.exe" "C:\HUNGER_Restaurant\main.py"`

## Windows Event Logs

### Application Logs
1. **Open** Event Viewer
2. **Navigate** to: Windows Logs > Application
3. **Look** for Python-related errors
4. **Filter** by source: "Python"

### Custom Logging
Add to your batch files:
```batch
python main.py >> "logs\app_%date%.log" 2>&1
```

## Windows Service Installation (Advanced)

### Using NSSM (Non-Sucking Service Manager)
1. **Download** NSSM from nssm.cc
2. **Extract** to a folder
3. **Run** as Administrator:
   ```cmd
   nssm install "HUNGER Restaurant" "C:\Python311\python.exe" "C:\HUNGER_Restaurant\main.py"
   nssm start "HUNGER Restaurant"
   ```

### Using Windows Service Wrapper
1. **Install** pywin32: `python -m pip install pywin32`
2. **Create** service wrapper script
3. **Install** as Windows service

## Windows Security Best Practices

### User Account Control (UAC)
- **Run** as standard user for daily operations
- **Use** Administrator only for installation/updates
- **Enable** UAC for security

### Windows Defender
1. **Add** exclusions for:
   - Project folder
   - Python installation folder
   - Database files
2. **Configure** real-time protection
3. **Schedule** regular scans

### Network Security
1. **Use** Windows Firewall
2. **Configure** network profiles
3. **Enable** Windows Defender Firewall
4. **Block** unnecessary network access

## Support and Maintenance

### Windows Update
- **Schedule** updates during off-hours
- **Test** application after major Windows updates
- **Keep** Windows and Python updated

### Performance Monitoring
1. **Use** Task Manager to monitor resources
2. **Check** Windows Performance Monitor
3. **Monitor** disk space and memory usage

### Regular Maintenance
```batch
# Weekly maintenance script
@echo off
echo Running weekly maintenance...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
echo Maintenance completed
pause
```

## License and Support

- **Developer**: Varchaswaa Media Pvt Ltd
- **Licensee**: HUNGER Restaurant
- **Windows Support**: Included in license
- **Customization**: Available for Windows-specific features

---

**Note**: This guide is specifically designed for Windows users. For other operating systems, refer to the main installation guide.
