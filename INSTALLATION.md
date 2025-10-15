# HUNGER Restaurant Billing System - Installation Guide

## System Overview

The HUNGER Restaurant Billing System consists of three main components:
1. **Desktop Application** - Tkinter-based GUI for restaurant operations
2. **Mobile Backend API** - FastAPI server for mobile app integration
3. **Mobile App** - Flutter application for mobile devices

## Prerequisites

### System Requirements
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux
- **Python**: Version 3.11 or higher (64-bit recommended)
- **Memory**: Minimum 4GB RAM
- **Storage**: 500MB free space
- **Network**: Internet connection for initial setup and updates

### Additional Requirements for Mobile App
- **Flutter SDK**: Version 3.0.0 or higher
- **Android Studio** or **Xcode** (for mobile development)
- **Node.js** (for Flutter toolchain)

## Installation Methods

### Method 1: Quick Installation (Windows - Recommended)

#### Option A: Automated Batch Installer
1. Download the project files
2. Double-click `install_windows.bat`
3. Follow the on-screen prompts
4. The script will:
   - Detect Python installation
   - Add Python to PATH if needed
   - Install all required dependencies
   - Set up the environment

#### Option B: GUI Installer (PowerShell)
1. Right-click on `install_windows_gui.ps1`
2. Select "Run with PowerShell"
3. Click "Install" to install dependencies
4. Click "Run App" to launch the application

### Method 2: Manual Installation

#### Step 1: Install Python
1. Download Python 3.11 (64-bit) from [python.org](https://www.python.org/downloads/)
2. **Important**: Check "Add Python to PATH" during installation
3. Verify installation:
   ```bash
   python --version
   pip --version
   ```

#### Step 2: Install Desktop Application Dependencies
```bash
# Navigate to project directory
cd /path/to/hungerestaurant

# Upgrade pip
python -m pip install --upgrade pip

# Install desktop app dependencies
python -m pip install -r requirements.txt
```

#### Step 3: Install Mobile Backend Dependencies
```bash
# Navigate to mobile backend directory
cd mobile_backend

# Install mobile backend dependencies
python -m pip install -r requirements.txt
```

#### Step 4: Install Mobile App Dependencies (Optional)
```bash
# Navigate to mobile app directory
cd mobile_app

# Install Flutter dependencies
flutter pub get
```

## Platform-Specific Instructions

### Windows Installation

#### Using Official Python Installer
1. Download Python 3.11 (64-bit) from python.org
2. Run installer with "Add Python to PATH" checked
3. Use the automated installers (`install_windows.bat` or `install_windows_gui.ps1`)

#### Manual Windows Setup
```cmd
# Open Command Prompt as Administrator
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -r mobile_backend/requirements.txt
```

### macOS Installation

#### Using Official Python Installer
```bash
# Download and install Python 3.11 from python.org
# Use the full path to avoid system Python issues
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m pip install --upgrade pip
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m pip install -r requirements.txt
/Library/Frameworks/Python.framework/Versions/3.11/bin/python3 -m pip install -r mobile_backend/requirements.txt
```

#### Using Homebrew
```bash
# Install Python
brew install python@3.11

# Install dependencies
python3.11 -m pip install --upgrade pip
python3.11 -m pip install -r requirements.txt
python3.11 -m pip install -r mobile_backend/requirements.txt
```

### Linux Installation

#### Ubuntu/Debian
```bash
# Install Python and pip
sudo apt update
sudo apt install python3.11 python3.11-pip python3.11-tk

# Install dependencies
python3.11 -m pip install --upgrade pip
python3.11 -m pip install -r requirements.txt
python3.11 -m pip install -r mobile_backend/requirements.txt
```

#### CentOS/RHEL/Fedora
```bash
# Install Python and pip
sudo dnf install python3.11 python3.11-pip tkinter

# Install dependencies
python3.11 -m pip install --upgrade pip
python3.11 -m pip install -r requirements.txt
python3.11 -m pip install -r mobile_backend/requirements.txt
```

## Running the Applications

### Desktop Application
```bash
# From the main project directory
python main.py
```

### Mobile Backend Server
```bash
# From the mobile_backend directory
cd mobile_backend
python main.py

# Or on Windows, double-click start_server.bat
```

The server will start on `http://localhost:8000`

### Mobile App (Flutter)
```bash
# From the mobile_app directory
cd mobile_app
flutter run
```

## First-Time Setup

### 1. Initial Login
- **Username**: `owner`
- **Password**: `1234`
- **Role**: SUPER_ADMIN (full access)

### 2. Configuration
Edit `restaurant_billing/config.py` to customize:
- Restaurant name and legal details
- License information
- Telegram bot settings (optional)
- GST settings
- Service charge percentage

### 3. Database Setup
The SQLite database (`data/restaurant.db`) is automatically created with:
- Default GST slabs
- Sample menu items
- User accounts and permissions
- Restaurant settings

## Dependencies Overview

### Desktop Application (`requirements.txt`)
- `pillow==10.4.0` - Image processing for logos and QR codes
- `qrcode==7.4.2` - UPI QR code generation
- `python-dateutil==2.9.0.post0` - Date handling
- `num2words==0.5.13` - Number to words conversion
- `python-escpos==3.1` - Thermal printer support
- `python-telegram-bot==21.6` - Telegram notifications

### Mobile Backend (`mobile_backend/requirements.txt`)
- `fastapi==0.104.1` - Web API framework
- `uvicorn[standard]==0.24.0` - ASGI server
- `websockets==12.0` - WebSocket support
- `python-jose[cryptography]==3.3.0` - JWT authentication
- `python-multipart==0.0.6` - Form data handling
- `pydantic==2.5.0` - Data validation

### Mobile App (`mobile_app/pubspec.yaml`)
- `flutter` - Mobile framework
- `http: ^1.1.0` - HTTP client
- `web_socket_channel: ^2.4.0` - WebSocket client
- `shared_preferences: ^2.2.2` - Local storage
- `provider: ^6.1.1` - State management
- `intl: ^0.19.0` - Internationalization

## Troubleshooting

### Common Issues

#### Python Not Found
```bash
# Windows: Add Python to PATH manually
setx PATH "%PATH%;C:\Python311;C:\Python311\Scripts"

# macOS/Linux: Create symlink
sudo ln -s /usr/bin/python3.11 /usr/bin/python
```

#### Tkinter Missing (macOS)
- Use official Python installer instead of system Python
- Install tkinter separately: `brew install python-tk`

#### Permission Errors
```bash
# Use user installation
python -m pip install --user -r requirements.txt
```

#### Port Already in Use (Mobile Backend)
```bash
# Kill process using port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux
lsof -ti:8000 | xargs kill -9
```

#### Flutter Issues
```bash
# Update Flutter
flutter upgrade

# Clean and rebuild
flutter clean
flutter pub get
```

### Database Issues
- Delete `data/restaurant.db` to reset database
- Restart application to recreate with defaults

### Network Issues
- Check firewall settings
- Ensure ports 8000 (API) and 3000 (Flutter dev) are open
- Verify localhost connectivity

## Verification

### Test Desktop Application
1. Run `python main.py`
2. Login with `owner`/`1234`
3. Navigate through all menu options
4. Create a test order
5. Generate an invoice

### Test Mobile Backend
1. Start server: `cd mobile_backend && python main.py`
2. Visit `http://localhost:8000/docs` for API documentation
3. Test login endpoint with default credentials

### Test Mobile App
1. Start backend server
2. Run `cd mobile_app && flutter run`
3. Login with mobile app
4. Test order creation and real-time updates

## Security Considerations

### Production Deployment
- Change default passwords
- Use environment variables for sensitive data
- Enable HTTPS for mobile backend
- Configure proper CORS settings
- Use strong JWT secrets

### Database Security
- Regular backups of `data/restaurant.db`
- Secure file permissions
- Consider database encryption for sensitive data

## Support and Maintenance

### Updates
- Use the built-in updater (SUPER_ADMIN only)
- Or manually pull latest changes and reinstall dependencies

### Backups
- Regular backup of `data/restaurant.db`
- Backup configuration files
- Export menu and user data periodically

### Logs
- Desktop app: Check console output
- Mobile backend: Check terminal output
- Mobile app: Use Flutter debugging tools

## License Information

- **Developer**: Varchaswaa Media Pvt Ltd
- **Licensee**: HUNGER Restaurant
- **Copyright**: © All rights reserved to Varchaswaa Media Pvt Ltd
- **Usage**: Licensed for HUNGER Restaurant operations only

## Contact Support

For technical support, customization requests, or licensing inquiries:
- Contact: Varchaswaa Media Pvt Ltd
- Customization services available for:
  - GST format modifications
  - Printer integrations
  - Multi-language support
  - E-invoicing compliance
  - Additional features

---

**Note**: This installation guide covers the complete HUNGER Restaurant Billing System. Choose the installation method that best suits your environment and technical expertise.
