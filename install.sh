#!/bin/bash
# Elefante One-Click Installer for Mac/Linux
# ==========================================

set -e

echo "============================================================"
echo "🐘 ELEFANTE INSTALLER"
echo "============================================================"
echo ""

# 1. Check for Python
if command -v python3 &> /dev/null; then
    PYTHON_CMD=python3
elif command -v python &> /dev/null; then
    PYTHON_CMD=python
else
    echo "[ERROR] Python is not installed."
    echo "Please install Python 3.10+"
    exit 1
fi

echo "[INFO] Using $($PYTHON_CMD --version)"

# 2. Create Virtual Environment
if [ ! -d ".venv" ]; then
    echo "[INFO] Creating virtual environment..."
    $PYTHON_CMD -m venv .venv
fi

# 3. Activate Virtual Environment
source .venv/bin/activate

# 4. Run Python Installer
echo "[INFO] Starting installation wizard..."
python scripts/install.py
