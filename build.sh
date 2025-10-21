#!/bin/bash

echo "HUNGER Restaurant Billing System - Quick Build Script"
echo "====================================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not found."
    exit 1
fi

# Create distribution directory
echo "Creating distribution directory..."
mkdir -p dist/hunger-restaurant-billing
mkdir -p dist/hunger-restaurant-billing/data
mkdir -p dist/hunger-restaurant-billing/mobile_backend

# Copy application files
echo "Copying application files..."
cp -r restaurant_billing dist/hunger-restaurant-billing/
cp -r mobile_backend dist/hunger-restaurant-billing/
cp main.py dist/hunger-restaurant-billing/
cp requirements.txt dist/hunger-restaurant-billing/
cp mobile_backend/requirements.txt dist/hunger-restaurant-billing/mobile_backend/

# Copy documentation
echo "Copying documentation..."
cp README.md dist/hunger-restaurant-billing/ 2>/dev/null || true
cp INSTALLATION_QUICK_START.md dist/hunger-restaurant-billing/ 2>/dev/null || true
cp DATABASE_INFO.md dist/hunger-restaurant-billing/ 2>/dev/null || true
cp INSTALLATION_SUMMARY.md dist/hunger-restaurant-billing/ 2>/dev/null || true
cp PRODUCTION_READINESS.md dist/hunger-restaurant-billing/ 2>/dev/null || true
cp AUTOMATIC_UPDATES.md dist/hunger-restaurant-billing/ 2>/dev/null || true

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv dist/hunger-restaurant-billing/venv

# Install dependencies
echo "Installing dependencies..."
dist/hunger-restaurant-billing/venv/bin/pip install --upgrade pip
dist/hunger-restaurant-billing/venv/bin/pip install -r requirements.txt
dist/hunger-restaurant-billing/venv/bin/pip install -r mobile_backend/requirements.txt

# Create launcher scripts
echo "Creating launcher scripts..."

# Desktop launcher
cat > dist/hunger-restaurant-billing/start_desktop.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
./venv/bin/python main.py
EOF
chmod +x dist/hunger-restaurant-billing/start_desktop.sh

# Mobile launcher
cat > dist/hunger-restaurant-billing/start_mobile.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")/mobile_backend"
../venv/bin/python main.py
EOF
chmod +x dist/hunger-restaurant-billing/start_mobile.sh

# Install script
cat > dist/hunger-restaurant-billing/install.sh << 'EOF'
#!/bin/bash
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
EOF
chmod +x dist/hunger-restaurant-billing/install.sh

# Initialize database
echo "Initializing database..."
dist/hunger-restaurant-billing/venv/bin/python -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized')"

# Create archive
echo "Creating archive..."
cd dist
tar -czf HUNGER-Restaurant-Billing-$(uname -s).tar.gz hunger-restaurant-billing/
cd ..

echo "Build completed successfully!"
echo "Package location: dist/hunger-restaurant-billing"
echo "Archive location: dist/HUNGER-Restaurant-Billing-$(uname -s).tar.gz"
echo ""
echo "To install:"
echo "1. Extract the archive"
echo "2. Run: cd hunger-restaurant-billing && ./install.sh"
echo "3. Launch: ./start_desktop.sh"
