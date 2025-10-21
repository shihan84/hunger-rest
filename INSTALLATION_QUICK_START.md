# HUNGER Restaurant Billing System - Quick Start Installation

## For Fresh Windows 10/11 Installation

### 🚀 One-Click Installation (Recommended)

1. **Download** the project files to your computer
2. **Right-click** on `install_windows.bat` 
3. **Select** "Run as administrator"
4. **Wait** for automatic installation to complete
5. **Launch** the application when prompted

### 🎯 Alternative Installation Methods

#### Option 1: Enhanced PowerShell Installer
```cmd
# Right-click and "Run as administrator"
install_windows_complete.ps1
```
**Features:**
- Downloads and installs Python 3.11.7 automatically
- Downloads and installs Git for Windows automatically
- Creates desktop shortcuts
- Creates start menu entries
- Better error handling and progress display

#### Option 2: System Requirements Checker
```cmd
# Check if your system is ready
check_system_requirements.ps1
```
**Checks:**
- Windows version compatibility
- System architecture (64-bit required)
- Available memory and disk space
- Network connectivity
- Administrator privileges
- Existing software installations

### 📋 What Gets Installed Automatically

#### Required Software:
- **Python 3.11.7 (64-bit)** - Programming language runtime
- **Git for Windows** - Version control system
- **All Python packages** - Application dependencies

#### Application Components:
- **Desktop Application** - Main restaurant billing system
- **Mobile Backend API** - FastAPI server for mobile integration
- **Database** - SQLite database (auto-created)

#### System Integration:
- **Desktop Shortcuts** - Easy access to applications
- **Start Menu Entries** - Windows start menu integration
- **PATH Configuration** - Command line access

### 🔧 Manual Installation (If Automated Fails)

#### Step 1: Install Python
1. Download from [python.org](https://www.python.org/downloads/)
2. Run installer with "Add Python to PATH" checked
3. Verify: `python --version`

#### Step 2: Install Dependencies
```cmd
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
cd mobile_backend
python -m pip install -r requirements.txt
cd ..
```

#### Step 3: Run Application
```cmd
python main.py
```

### 🎮 First Time Setup

#### Login Credentials:
- **Username:** `owner`
- **Password:** `1234`
- **Role:** SUPER_ADMIN (full access)

#### Initial Configuration:
1. **Restaurant Settings** - Edit `restaurant_billing/config.py`
2. **Menu Items** - Add your restaurant's menu
3. **User Accounts** - Create additional user accounts
4. **Telegram Bot** - Configure notifications (optional)

### 🖥️ Running the Applications

#### Desktop Application:
```cmd
python main.py
# or double-click the desktop shortcut
```

#### Mobile Backend API:
```cmd
cd mobile_backend
python main.py
# or double-click the mobile backend shortcut
```
**API will be available at:** `http://localhost:8000`

### 🔍 Troubleshooting

#### Common Issues:

**Python Not Found:**
- Restart Command Prompt after installation
- Check PATH environment variable
- Reinstall Python with "Add to PATH" checked

**Permission Denied:**
- Run Command Prompt as Administrator
- Check antivirus exclusions
- Disable Windows Defender temporarily

**Network Issues:**
- Check internet connection
- Configure firewall to allow Python
- Disable proxy if using one

**Tkinter Errors:**
- Reinstall Python from official website
- Use Python 3.11+ (includes Tkinter)

#### Getting Help:
1. Run `check_system_requirements.ps1` for system diagnostics
2. Check Windows Event Viewer for error logs
3. Try manual installation steps
4. Contact support with error messages

### 🗑️ Uninstalling

#### Using Uninstaller:
```cmd
# Right-click and "Run as administrator"
uninstall.ps1
```

#### Manual Uninstall:
1. Delete project folder
2. Remove desktop shortcuts
3. Remove start menu entries
4. Uninstall Python packages (optional)

### 📁 File Structure After Installation

```
hungerestaurant/
├── main.py                          # Main application launcher
├── install_windows.bat              # Basic installer
├── install_windows_complete.ps1     # Enhanced installer
├── check_system_requirements.ps1    # System checker
├── uninstall.ps1                    # Uninstaller
├── requirements.txt                 # Desktop dependencies
├── restaurant_billing/              # Main application
│   ├── app.py                       # GUI application
│   ├── config.py                    # Configuration
│   ├── db.py                        # Database operations
│   └── ...
├── mobile_backend/                  # API server
│   ├── main.py                      # FastAPI server
│   └── requirements.txt             # API dependencies
├── mobile_app/                      # Flutter mobile app
├── data/                            # Database and data
│   └── restaurant.db                # SQLite database
└── invoices/                        # Generated invoices
```

### 🎯 Quick Commands Reference

```cmd
# Check system requirements
check_system_requirements.ps1

# Install everything automatically
install_windows.bat

# Enhanced installation with shortcuts
install_windows_complete.ps1

# Run desktop application
python main.py

# Run mobile backend
cd mobile_backend && python main.py

# Uninstall application
uninstall.ps1
```

### 📞 Support Information

- **Developer:** Varchaswaa Media Pvt Ltd
- **Licensee:** HUNGER Restaurant
- **System Requirements:** Windows 10/11, 4GB RAM, 1GB disk space
- **Network:** Internet required for initial installation

---

**Note:** This installation guide is designed for fresh Windows 10/11 systems. The automated installers will handle all required software installation and configuration.
