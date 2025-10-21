#!/bin/bash
echo "Installing HUNGER Restaurant Billing System..."

# Check if Python 3.11+ is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3.11+ is required. Please install it first."
    exit 1
fi

# Check Python version
python_version=$(python3 -c "import sys; print(f'3.9')")
if [[ $(echo "$python_version < 3.11" | bc -l) -eq 1 ]]; then
    echo "Python 3.11+ is required. Current version: $python_version"
    exit 1
fi

# Initialize database
./venv/bin/python -c "from restaurant_billing.db import init_db; init_db(); print('Database initialized')"

echo "Installation completed!"
echo "To run the desktop application: ./start_desktop.sh"
echo "To run the mobile backend: ./start_mobile.sh"
